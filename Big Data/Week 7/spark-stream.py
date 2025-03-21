from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, window

# Initialize Spark Session
spark = SparkSession.builder.appName("StockPriceAnalysis").getOrCreate()

# Read streaming data from netcat
stock_stream = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# Parse incoming data (datetime, symbol, price)
from pyspark.sql.functions import split

stock_stream = stock_stream.withColumn("data", split(stock_stream["value"], ",")) \
    .withColumn("datetime", col("data").getItem(0)) \
    .withColumn("symbol", col("data").getItem(1)) \
    .withColumn("price", col("data").getItem(2).cast("double")) \
    .select("datetime", "symbol", "price")

# Split into AAPL and MSFT price streams
aapl_price = stock_stream.filter(col("symbol") == "AAPL")
msft_price = stock_stream.filter(col("symbol") == "MSFT")

# Compute 10-day and 40-day moving averages
aapl_10day = aapl_price.withColumn("aapl10Day", avg("price").over(window("datetime", "10 days")))
aapl_40day = aapl_price.withColumn("aapl40Day", avg("price").over(window("datetime", "40 days")))

msft_10day = msft_price.withColumn("msft10Day", avg("price").over(window("datetime", "10 days")))
msft_40day = msft_price.withColumn("msft40Day", avg("price").over(window("datetime", "40 days")))

# Detect Buy/Sell signals
from pyspark.sql.functions import lag, when
from pyspark.sql.window import Window

windowSpec = Window.partitionBy("symbol").orderBy("datetime")

buy_sell_aapl = aapl_10day.join(aapl_40day, ["datetime", "symbol", "price"]) \
    .withColumn("prev_aapl10", lag("aapl10Day").over(windowSpec)) \
    .withColumn("prev_aapl40", lag("aapl40Day").over(windowSpec)) \
    .withColumn("signal",
        when((col("prev_aapl10") <= col("prev_aapl40")) & (col("aapl10Day") > col("aapl40Day")), "BUY")
        .when((col("prev_aapl10") >= col("prev_aapl40")) & (col("aapl10Day") < col("aapl40Day")), "SELL")
    ) \
    .select("datetime", "symbol", "signal")

buy_sell_msft = msft_10day.join(msft_40day, ["datetime", "symbol", "price"]) \
    .withColumn("prev_msft10", lag("msft10Day").over(windowSpec)) \
    .withColumn("prev_msft40", lag("msft40Day").over(windowSpec)) \
    .withColumn("signal",
        when((col("prev_msft10") <= col("prev_msft40")) & (col("msft10Day") > col("msft40Day")), "BUY")
        .when((col("prev_msft10") >= col("prev_msft40")) & (col("msft10Day") < col("msft40Day")), "SELL")
    ) \
    .select("datetime", "symbol", "signal")

# Output to console
query = buy_sell_aapl.union(buy_sell_msft) \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
