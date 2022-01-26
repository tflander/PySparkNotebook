from pyspark.sql.functions import udf,col
from pyspark.sql.types import StringType


def clean_coursera_data(spark_session, raw_data_frame):
    raw_data_frame.registerTempTable('raw_data')
    department = udf(lambda course_name: determine_department(course_name), StringType())

    # new_df = spark_session.sql('SELECT *, department(null) AS Department FROM raw_data')
    new_df = raw_data_frame.withColumn('Department', department(col('Course Name')))

    return new_df


def determine_department(course_name: str):
    if 'sql' in course_name.lower():
        return 'Programming'
    return None
