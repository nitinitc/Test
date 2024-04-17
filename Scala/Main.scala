package nitinspark

import org.apache.spark.{SparkConf, SparkContext}

object Main {
  def main(args: Array[String]): Unit = {
    // Create a SparkConf object to configure Spark
    val sparkConf = new SparkConf()
    sparkConf.set("spark.app.name","FirstDFDemo")

    // Create a SparkContext to run Spark operations
    //val sc = new SparkContext(sparkConf)


    val sc = new SparkContext( master = "yarn" , appName ="FirstDFDemo")
    // Read input text file from the command line arguments

    val rdd11 = sc.textFile(args(0))

    // Split each line into words
    val rdd2 = rdd11.flatMap(x => x.split(" "))

    // Convert each word to lowercase and map it to (word, 1) tuple
    val rdd3 = rdd2.map(x => (x.toLowerCase, 1))

    // Reduce by key to count the occurrences of each word and sort by the count
    val rdd4 = rdd3.reduceByKey((x, y) => x + y).sortBy(_._2)

    // Collect the result (word count pairs) and print
    val res = rdd4.collect()
    //res.foreach(println)


    //val wordCountsRDD = rdd11
     // .flatMap(_.split("\\s+")) // Split each line into words
     // .map(word => (word, 1))   // Map each word to a tuple (word, 1)
    //  .reduceByKey(_ + _)       // Reduce by key to count occurrences of each word

    // Save the word counts to the output path
    val outputPath = args(1)
    rdd4.saveAsTextFile(outputPath)

    // Stop the SparkContext
    //sc.stop()
  }
}
