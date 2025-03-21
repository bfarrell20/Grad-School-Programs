from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Stock Analysis") \
    .getOrCreate()

# Load AAPL and MSFT data separately
aapl_data = spark.read.option("header", "true").csv("hdfs://cluster-4290-m/user/root/AAPL_data.csv")
msft_data = spark.read.option("header", "true").csv("hdfs://cluster-4290-m/user/root/MSFT_data.csv")

# Convert the datetime column to a timestamp
aapl_data = aapl_data.withColumn("datetime", F.to_timestamp("datetime"))
msft_data = msft_data.withColumn("datetime", F.to_timestamp("datetime"))

# Select relevant columns (datetime, close price) for filtering
aaplPrice = aapl_data.select("datetime", "close")
msftPrice = msft_data.select("datetime", "close")

# Create window specification for moving averages
window_spec_10 = Window.orderBy("datetime").rowsBetween(-9, 0)  # 10-day moving average
window_spec_40 = Window.orderBy("datetime").rowsBetween(-39, 0)  # 40-day moving average

# Compute the 10-day and 40-day moving averages for AAPL
aaplPrice = aaplPrice.withColumn("moving_avg_10", F.avg("close").over(window_spec_10)) \
                     .withColumn("moving_avg_40", F.avg("close").over(window_spec_40))

# Compute the 10-day and 40-day moving averages for MSFT
msftPrice = msftPrice.withColumn("moving_avg_10", F.avg("close").over(window_spec_10)) \
                     .withColumn("moving_avg_40", F.avg("close").over(window_spec_40))

# Generate signals for AAPL
aaplPrice = aaplPrice.withColumn("signal", 
                                 F.when(F.col("moving_avg_10") > F.col("moving_avg_40"), "buy")
                                  .when(F.col("moving_avg_10") < F.col("moving_avg_40"), "sell")
                                  .otherwise("hold"))

# Generate signals for MSFT
msftPrice = msftPrice.withColumn("signal", 
                                 F.when(F.col("moving_avg_10") > F.col("moving_avg_40"), "buy")
                                  .when(F.col("moving_avg_10") < F.col("moving_avg_40"), "sell")
                                  .otherwise("hold"))

# Add symbol column to each stream
aaplPrice = aaplPrice.withColumn("symbol", F.lit("AAPL"))
msftPrice = msftPrice.withColumn("symbol", F.lit("MSFT"))

# Combine both AAPL and MSFT signals
combined_signals = aaplPrice.union(msftPrice)

# Create the formatted output column for buy/sell signals
formatted_signals = combined_signals.withColumn(
    "formatted_output",
    F.concat(F.col("datetime").cast("string"), 
             F.lit(" "), 
             F.col("signal"), 
             F.lit(" "), 
             F.col("symbol"))
)

# Output the formatted signals
formatted_signals.show(truncate=False)
