from pyspark.sql.functions import udf,col
from pyspark.sql.types import StringType


def clean_coursera_data(raw_data_frame):
    raw_data_frame.registerTempTable('raw_data')
    primary_subject_fn = udf(lambda course_name: determine_primary_subject(course_name), StringType())
    department_fn = udf(lambda primary_subject: determine_department(primary_subject), StringType())

    new_df = raw_data_frame\
        .withColumn('Primary Subject', primary_subject_fn(col('Course Name')))\
        .withColumn('Department', department_fn(col('Primary Subject')))

    return new_df


def determine_primary_subject(course_name: str):
    if 'sql' in course_name.lower():
        return 'SQL'
    return None


def determine_department(primary_subject: str):
    if primary_subject == 'SQL':
        return 'Programming'
    return None
