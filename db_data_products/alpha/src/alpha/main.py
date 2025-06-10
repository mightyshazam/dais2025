from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import max
import pandas as pd
from datetime import timedelta, datetime

table = "dais2025.alpha.things"
def write_to_table(spark: SparkSession, df: DataFrame, table_name: str):
    df.write.format("delta").mode("overwrite").saveAsTable(table_name)
    print(f"Written to {table_name}")
    return

def main():
    spark = get_spark()
    
    data = pd.DataFrame({
        "id": range(1, 1001),
        "content": [str(x) for x in range(1, 1001)],
        "created": pd.date_range(datetime.now() - timedelta(days=1), datetime.now(), 1000),
    })
    
    write_to_table(spark, spark.createDataFrame(data), table)


# Create a new Databricks Connect session. If this fails,
# check that you have configured Databricks Connect correctly.
# See https://docs.databricks.com/dev-tools/databricks-connect.html.
def get_spark() -> SparkSession:
    try:
        from databricks.connect import DatabricksSession
        return DatabricksSession.builder.getOrCreate()
    except ImportError:
        return SparkSession.builder.getOrCreate()


if __name__ == '__main__':
    main()