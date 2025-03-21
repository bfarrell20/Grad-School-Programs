from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Load AAPL and MSFT data separately
aapl_data = spark.read.option("header", "true").csv("hdfs://cluster-4290-m/user/root/AAPL_data.csv")
msft_data = spark.read.option("header", "true").csv("hdfs://cluster-4290-m/user/root/MSFT_data.csv")

# Convert the datetime column to a timestamp
aapl_data = aapl_data.withColumn("datetime", F.to_timestamp("datetime"))
msft_data = msft_data.withColumn("datetime", F.to_timestamp("datetime"))

# Create 10-day and 40-day moving averages for AAPL
window_spec = Window.orderBy("datetime").rowsBetween(-9, 0)  # For 10-day MA
aapl_data = aapl_data.withColumn("aapl_10day", F.avg("close").over(window_spec))

window_spec_40 = Window.orderBy("datetime").rowsBetween(-39, 0)  # For 40-day MA
aapl_data = aapl_data.withColumn("aapl_40day", F.avg("close").over(window_spec_40))

# Create 10-day and 40-day moving averages for MSFT
msft_data = msft_data.withColumn("msft_10day", F.avg("close").over(window_spec))
msft_data = msft_data.withColumn("msft_40day", F.avg("close").over(window_spec_40))

# Compare the moving averages and generate buy/sell signals
aapl_data = aapl_data.withColumn("signal", F.when(F.col("aapl_10day") > F.col("aapl_40day"), "buy")
                                 .when(F.col("aapl_10day") < F.col("aapl_40day"), "sell")
                                 .otherwise("hold"))

msft_data = msft_data.withColumn("signal", F.when(F.col("msft_10day") > F.col("msft_40day"), "buy")
                                 .when(F.col("msft_10day") < F.col("msft_40day"), "sell")
                                 .otherwise("hold"))

# Show the buy/sell signals
aapl_data.select("datetime", "signal").show()
msft_data.select("datetime", "signal").show()
