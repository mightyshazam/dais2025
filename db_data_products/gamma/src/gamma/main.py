from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import greatest
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import StringType, TimestampType, LongType
import pandas as pd
from datetime import timedelta, datetime
from pyspark.sql.functions import concat, col, when


table = "dais2025.gamma.things"
def get_table(spark: SparkSession, table: str) -> DataFrame:
    return spark.read.schema(StructType([
        StructField("id", LongType(), False),
        StructField("content", StringType(), False),
        StructField("created", TimestampType(), False),
    ])).table(table)

def write_to_table(spark: SparkSession, df: DataFrame, table_name: str):
    df.write.format("delta").mode("overwrite").saveAsTable(table_name)
    print(f"Written to {table_name}")
    return


# Create a new Databricks Connect session. If this fails,
# check that you have configured Databricks Connect correctly.
# See https://docs.databricks.com/dev-tools/databricks-connect.html.
def get_spark() -> SparkSession:
    try:
        from databricks.connect import DatabricksSession
        return DatabricksSession.builder.getOrCreate()
    except ImportError:
        return SparkSession.builder.getOrCreate()

def get_most_recent_update(df: DataFrame) -> datetime:
    df.agg({"created": "max"}).first()["max(created)"]

def check_run_history(alpha: DataFrame, beta: DataFrame):
    alpha_most_recent: datetime = get_most_recent_update(alpha)
    beta_most_recent: datetime = get_most_recent_update(beta)
    difference = alpha_most_recent - beta_most_recent
    if abs(difference.total_seconds) > 3600:
        # This is where we can return false to avoid running
        print("The time difference between runs is more than an hour.")
    return True

def main():
    spark = get_spark()
    
    a = get_table(spark, "dais2025.alpha.things")
    b = get_table(spark, "dais2025.beta.things")
    if not check_run_history(a, b):
        print("Aborting transform due to stale data")
        return

    joined = a.join(b, "id", "inner")
    
    data = (joined
                .select(a.id.alias("id"), a.id.alias("alpha_id"), 
                        b.id.alias("beta_id"), 
                        concat(a.content, b.content).alias("content"),
                        greatest(a.created, b.created).alias("created")))
    write_to_table(spark, data, table)
    dbutils.jobs.taskValues.set(key = "verify_promise", value = True)


if __name__ == '__main__':
    main()