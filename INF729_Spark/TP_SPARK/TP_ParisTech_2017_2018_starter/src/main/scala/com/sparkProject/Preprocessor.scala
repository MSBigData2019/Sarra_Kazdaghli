package com.sparkProject

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.udf
import org.apache.spark.sql.DataFrame

object Preprocessor {

  def main(args: Array[String]): Unit = {

    // Des réglages optionels du job spark. Les réglages par défaut fonctionnent très bien pour ce TP
    // on vous donne un exemple de setting quand même
    val conf = new SparkConf().setAll(Map(
      "spark.scheduler.mode" -> "FIFO",
      "spark.speculation" -> "false",
      "spark.reducer.maxSizeInFlight" -> "48m",
      "spark.serializer" -> "org.apache.spark.serializer.KryoSerializer",
      "spark.kryoserializer.buffer.max" -> "1g",
      "spark.shuffle.file.buffer" -> "32k",
      "spark.default.parallelism" -> "12",
      "spark.sql.shuffle.partitions" -> "12"
    ))

    // Initialisation de la SparkSession qui est le point d'entrée vers Spark SQL (donne accès aux dataframes, aux RDD,
    // création de tables temporaires, etc et donc aux mécanismes de distribution des calculs.)
    val spark = SparkSession
      .builder
      .config(conf)
      .config("spark.master", "local")
      .appName("TP_spark")
      .getOrCreate()

    import spark.implicits._

    /** *****************************************************************************
      *
      * TP 2
      *
      *       - Charger un fichier csv dans un dataFrame
      *       - Pre-processing: cleaning, filters, feature engineering => filter, select, drop, na.fill, join, udf, distinct, count, describe, collect
      *       - Sauver le dataframe au format parquet
      *
      * if problems with unimported modules => sbt plugins update
      *
      * *******************************************************************************/

    println("hello world ! from Preprocessor")

    val df = spark.read
      .option("header", "true")
      .option("inferSchema", "true") // try to infer the data types of each column
      .csv("train_clean.csv")

    // df.take(5).foreach(println)


    println("number of rows is " + df.count)

    println("number of columns is " + df.columns.size)

    df.show(5)

    val dff = df.withColumn("goal", df.col("goal").cast("int"))
      .withColumn("backers_count", df.col("backers_count").cast("int"))
      .withColumn("final_status", df.col("final_status").cast("int"))
      .withColumn("deadline" , $"deadline".cast("Int"))
      .withColumn("state_changed_at", $"state_changed_at".cast("Int"))
      .withColumn("created_at", $"created_at".cast("Int"))
      .withColumn("launched_at", $"launched_at".cast("Int"))


    dff.printSchema()

    // 2 Cleaning
    dff.select("goal", "backers_count", "final_status").describe().show()

    // for the column name , some values are missing (**********)
    // for the columns deadline, state_changed_at, created at, launched_at aren't in the form of date
    val df0 = dff.dropDuplicates("project_id").na.drop()

//    dff.groupBy("disable_communication").count.orderBy($"count".desc).show(100)
//    dff.groupBy("country").count.orderBy($"count".desc).show(100)
//    dff.groupBy("currency").count.orderBy($"count".desc).show(100)
//    //dff.select("deadline").dropDuplicates.show()
//    dff.groupBy("state_changed_at").count.orderBy($"count".desc).show(100)
//    dff.groupBy("backers_count").count.orderBy($"count".desc).show(100)
//    dff.select("goal", "final_status").show(30)
//    dff.groupBy("country", "currency").count.orderBy($"count".desc).show(50)



    println("number of  rows after 1rst cleaning is " + df0.count)

    println("number of columns after 1rst cleaning is " + df0.columns.size)

    val df1 = df0.drop("disable_communication")

    df1.show(5)

    val df2 = df1.drop("backers_count", "state_changed_at")

    df2.show(5)

    df2.filter(df2("country")==="False").groupBy("currency").count.orderBy("count").show(50)

    val value_country = udf{(country: String, currency: String) =>
      if (country == "False")
         currency
      else
        country
    }

    val value_currency = udf{(currency: String)=>
      if (currency != null && currency.length != 3)
        null
      else
        currency
  }
    val dfCountry: DataFrame = df2
      .withColumn("country2", value_country($"country", $"currency"))
      .withColumn("currency2", value_currency($"currency"))
      .drop("country", "currency")

    dfCountry.show(5)

    dfCountry.groupBy("final_status").count().orderBy($"count".desc).show()

    val value_status = udf { (v: Integer) =>
      if (v != 0 || v != 1)
        0
      else
        v
    }
    val dfClass: DataFrame = dfCountry
        .withColumn("final_status", value_status($"final_status"))

    dfClass.show(10)

  }
}
