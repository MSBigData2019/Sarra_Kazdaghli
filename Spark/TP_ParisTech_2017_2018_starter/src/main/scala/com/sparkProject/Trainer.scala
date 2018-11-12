package com.sparkProject

import org.apache.spark.SparkConf
import org.apache.spark.ml.feature.{CountVectorizer, IDF, OneHotEncoder, RegexTokenizer, StopWordsRemover, StringIndexer, VectorAssembler}
import org.apache.spark.sql.{SaveMode, SparkSession}
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.tuning.{ParamGridBuilder, TrainValidationSplit}
import org.apache.spark.ml.evaluation.MulticlassClassificationEvaluator

object Trainer {

  def main(args: Array[String]): Unit = {

    val conf = new SparkConf().setAll(Map(
      "spark.scheduler.mode" -> "FIFO",
      "spark.speculation" -> "false",
      "spark.reducer.maxSizeInFlight" -> "48m",
      "spark.serializer" -> "org.apache.spark.serializer.KryoSerializer",
      "spark.kryoserializer.buffer.max" -> "1g",
      "spark.shuffle.file.buffer" -> "32k",
      "spark.default.parallelism" -> "12",
      "spark.sql.shuffle.partitions" -> "12",
      "spark.driver.maxResultSize" -> "2g"
    ))

    val spark = SparkSession
      .builder
      .config(conf)
      .appName("TP_spark")
      .getOrCreate()


    /** *****************************************************************************
      *
      * TP 3
      *
      *       - lire le fichier sauvegarder précédemment
      *       - construire les Stages du pipeline, puis les assembler
      *       - trouver les meilleurs hyperparamètres pour l'entraînement du pipeline avec une grid-search
      *       - Sauvegarder le pipeline entraîné
      *
      * if problems with unimported modules => sbt plugins update
      *
      * *******************************************************************************/

    println("hello world ! from Trainer")

    val data = spark.read.parquet("prepared_trainingset")

    data.show(10)

    // Splits sentences into words
    val tokenizer = new RegexTokenizer()
      .setPattern("\\W+")
      .setGaps(true)
      .setInputCol("text")
      .setOutputCol("tokens")

    // Drops all stop words (I, the, a ..)
    val remover = new StopWordsRemover()
      .setInputCol("tokens")
      .setOutputCol("filtered")

    // Converts tokens to vectors of token counts [nb of tokens, indexes, count of tokens]
    val cvModel = new CountVectorizer()
      .setInputCol("filtered")
      .setOutputCol("featuresset")

    // Down weights columns that appear too frequently in a corpus
    val idf = new IDF().setInputCol("featuresset").setOutputCol("tfidf")

    // Sets an index for a string
    val indexer = new StringIndexer()
      .setInputCol("country2")
      .setOutputCol("country_indexed")
      .setHandleInvalid("skip")


    val indexer2 = new StringIndexer()
      .setInputCol("currency2")
      .setOutputCol("currency_indexed")
      .setHandleInvalid("skip")

    // Encodes a column of category to a column of binary vectors (the sum of vectors equals 1)
    val encoder = new OneHotEncoder()
      .setInputCol("country_indexed")
      .setOutputCol("country_onehot")

    val encoder2 = new OneHotEncoder()
      .setInputCol("currency_indexed")
      .setOutputCol("currency_onehot")

    // Assembles columns to one column with vector of values
    val assembler = new VectorAssembler()
      .setInputCols(Array("tfidf", "days_campaign", "hours_prepa", "goal", "country_onehot", "currency_onehot"))
      .setOutputCol("features")

    val lr = new LogisticRegression()
      .setElasticNetParam(0.0)
      .setFitIntercept(true)
      .setFeaturesCol("features")
      .setLabelCol("final_status")
      .setStandardization(true)
      .setPredictionCol("predictions")
      .setRawPredictionCol("raw_predictions")
      .setThresholds(Array(0.7, 0.3))
      .setTol(1.0e-6)
      .setMaxIter(300)

    val pipeline = new Pipeline()
      .setStages(Array(tokenizer, remover, cvModel, idf, indexer, indexer2, encoder, encoder2, assembler, lr))

    // Fit the pipeline
    val model = pipeline.fit(data)

    val rescaledData = model.transform(data)

    rescaledData.select("features", "raw_predictions", "probability", "predictions").show(10)

    // Random split data into testing and training
    val splits = data.randomSplit(Array(0.9, 0.1))
    val training = splits(0).cache()
    val test = splits(1)

    // We use a ParamGridBuilder to construct a grid of parameters to search over.
    // TrainValidationSplit will try all combinations of values and determine best model using
    // the evaluator.
    val paramGrid = new ParamGridBuilder()
      .addGrid(lr.regParam, Array(0.00000001, 0.000001, 0.0001, 0.001))
      .addGrid(cvModel.minDF, Array(55.0, 75.0, 95.0))
      .build()

    val f1_eval = new MulticlassClassificationEvaluator().setLabelCol("final_status").setPredictionCol("predictions").setMetricName("f1")

    // A TrainValidationSplit requires an Estimator, a set of Estimator ParamMaps, and an Evaluator.
    val trainValidationSplit = new TrainValidationSplit()
      .setEstimator(pipeline)
      .setEvaluator(f1_eval)
      .setEstimatorParamMaps(paramGrid)
      .setTrainRatio(0.7)


    // Run train validation split, and choose the best set of parameters.
     val pipelineFitModel = trainValidationSplit.fit(training)

    // Make predictions on test data. model is the model with combination of parameters
    // that performed best.
     val df_WithPredictions = pipelineFitModel.transform(test)

    val f1_score = f1_eval.evaluate(df_WithPredictions)

    println("Le f1 score est", f1_score )


    df_WithPredictions.groupBy("final_status", "predictions").count().show()

    pipelineFitModel.write.overwrite().save("Best Model")

  }

}

