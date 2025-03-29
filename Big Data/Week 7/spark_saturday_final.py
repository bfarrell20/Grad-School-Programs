from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, lag, when, lit, input_file_name, round
from pyspark.sql.window import Window

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("StockTradingStrategy") \
    .getOrCreate()

# Read all CSV files from HDFS directory
stock_df = spark.read.csv(
    "hdfs:///user/root/stock_data/",
    header=True,
    inferSchema=True
)

# Add symbol column based on filename
stock_df = stock_df.withColumn(
    "filename", input_file_name()
).withColumn(
    "symbol",
    when(
        col("filename").contains("AAPL"), "AAPL"
    ).when(
        col("filename").contains("MSFT"), "MSFT"
    ).otherwise("UNKNOWN")
).drop("filename")

# Verify we have both symbols
print("Distinct symbols found:")
stock_df.select("symbol").distinct().show()

# Define window specs for moving averages
window_10 = Window.partitionBy("symbol").orderBy("datetime").rowsBetween(-9, 0)
window_40 = Window.partitionBy("symbol").orderBy("datetime").rowsBetween(-39, 0)

# Calculate moving averages
stock_with_ma = stock_df.withColumn("ma_10", avg("close").over(window_10)) \
                       .withColumn("ma_40", avg("close").over(window_40))

# Function to generate trading signals with share calculations
def generate_trades(df):
    window_spec = Window.partitionBy("symbol").orderBy("datetime")
    return df.withColumn("prev_ma_10", lag("ma_10", 1).over(window_spec)) \
            .withColumn("prev_ma_40", lag("ma_40", 1).over(window_spec)) \
            .withColumn("signal",
                when(
                    (col("prev_ma_10") <= col("prev_ma_40")) & 
                    (col("ma_10") > col("ma_40")), "buy"
                ).when(
                    (col("prev_ma_10") >= col("prev_ma_40")) & 
                    (col("ma_10") < col("ma_40")), "sell"
                ).otherwise(None)
            ) \
            .withColumn("shares", round(lit(100000)/col("close"))) \
            .filter(col("signal").isNotNull()) \
            .select(
                "datetime",
                "symbol",
                "close",
                "signal",
                "shares"
            )

# Generate trades
trades_df = generate_trades(stock_with_ma)

# Format output as requested
formatted_trades = trades_df.rdd.map(
    lambda row: f"({row['datetime']} {row['signal']} {row['symbol']}) - {row['shares']} shares @ ${row['close']:.2f}"
).collect()

# Save results to HDFS
trades_df.write.mode("overwrite") \
    .option("header", "true") \
    .csv("hdfs:///user/root/stock_trades/")

# Print formatted trades
print("\nTrading Recommendations ($100K per trade):")
for trade in formatted_trades:
    print(trade)

# Sample output:
# (2021-01-04 11:30:00 buy AAPL) - 758 shares @ $132.06
# (2021-01-05 14:45:00 sell AAPL) - 742 shares @ $134.75
# (2021-01-04 10:15:00 buy MSFT) - 459 shares @ $217.89
# (2021-01-05 15:30:00 sell MSFT) - 447 shares @ $223.71