from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, window, split, lag, when
from pyspark.sql.window import Window

# Initialize Spark Session
spark = SparkSession.builder.appName("StockPriceAnalysis").getOrCreate()

# Read streaming data from socket
stock_stream = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# Parse incoming data (datetime, symbol, price)
stock_stream = stock_stream.withColumn("data", split(stock_stream["value"], ",")) \
    .withColumn("datetime", col("data").getItem(0)) \
    .withColumn("symbol", col("data").getItem(1)) \
    .withColumn("price", col("data").getItem(2).cast("double")) \
    .select("datetime", "symbol", "price")

# Split into AAPL and MSFT price streams
aapl_price = stock_stream.filter(col("symbol") == "AAPL")
msft_price = stock_stream.filter(col("symbol") == "MSFT")

# Define window specs with partitioning for performance
symbol_window = Window.partitionBy("symbol").orderBy("datetime")

# Compute moving averages with optimized windows
aapl_10day = aapl_price.withColumn(
    "moving_avg_10", 
    avg("price").over(symbol_window.rowsBetween(-9, 0))  # 10-day MA
)

aapl_40day = aapl_price.withColumn(
    "moving_avg_40", 
    avg("price").over(symbol_window.rowsBetween(-39, 0))  # 40-day MA
)

msft_10day = msft_price.withColumn(
    "moving_avg_10", 
    avg("price").over(symbol_window.rowsBetween(-9, 0))
)

msft_40day = msft_price.withColumn(
    "moving_avg_40", 
    avg("price").over(symbol_window.rowsBetween(-39, 0))
)

# Detect Buy/Sell signals (crossovers)
def generate_signals(df):
    return df.join(
        df.withColumn("prev_10", lag("moving_avg_10").over(symbol_window))
          .withColumn("prev_40", lag("moving_avg_40").over(symbol_window)),
        ["datetime", "symbol", "price", "moving_avg_10", "moving_avg_40"]
    ).withColumn("signal",
        when(
            (col("prev_10") <= col("prev_40")) & 
            (col("moving_avg_10") > col("moving_avg_40")), "buy"
        ).when(
            (col("prev_10") >= col("prev_40")) & 
            (col("moving_avg_10") < col("moving_avg_40")), "sell"
        ).otherwise("hold")
    ).select("datetime", "price", "moving_avg_10", "moving_avg_40", "signal", "symbol")

# Generate signals for both stocks
aapl_signals = generate_signals(aapl_10day.join(aapl_40day, ["datetime", "symbol", "price"]))
msft_signals = generate_signals(msft_10day.join(msft_40day, ["datetime", "symbol", "price"]))

# Format output as required: (datetime signal symbol)
formatted_output = aapl_signals.union(msft_signals) \
    .withColumn("formatted_output", 
        col("datetime").cast("string") + " " + 
        col("signal") + " " + 
        col("symbol")
    ) \
    .select("datetime", "price", "moving_avg_10", "moving_avg_40", "signal", "symbol", "formatted_output")

# Output to console
query = formatted_output.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()