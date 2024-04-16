import org.apache.spark.sql.{SparkSession, Row}
import org.apache.spark.sql.types.{StructType, StringType}

object WordCountDataFrame {
  def main(args: Array[String]): Unit = {
    // Create SparkSession
    val spark = SparkSession.builder()
      .appName("WordCountDataFrame")
      .master("local[*]") // Set master URL to run Spark locally
      .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    val data = Seq("Hello world", "Hello Spark", "Spark is awesome")

    // Convert the sequence of strings to a sequence of Rows
    val rows = data.map(Row(_))

    val schema = new StructType().add("text", StringType)


    val textDF = spark.createDataFrame(spark.sparkContext.parallelize(rows), schema)

    import spark.implicits._
    val wordsDF = textDF.selectExpr("explode(split(text, ' ')) as word")

    val wordCountDF = wordsDF.groupBy("word").count().sort($"count".desc)

    wordCountDF.show()

    spark.stop()
  }
}
