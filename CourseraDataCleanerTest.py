import pytest
from pyspark.sql import SparkSession

from coursera_data_cleaner import clean_coursera_data


@pytest.fixture
def spark_session():
    return SparkSession.builder \
        .master("local") \
        .appName("Coursera Data Cleaner Tests") \
        .getOrCreate()


def test_sql_classification(spark_session):
    data_file = "test_data/sql.csv"
    raw_data = spark_session.read.option('escape', '"').csv(data_file, header=True)

    clean_data = clean_coursera_data(raw_data)

    assert clean_data.count() == raw_data.count()
    categorized_rows = clean_data.filter(clean_data['Department'].isNotNull())
    assert categorized_rows.count() == 1
    for classified_row in categorized_rows.collect():
        assert classified_row['Department'] == 'Programming'
        assert classified_row['Primary Subject'] == 'SQL'


def test_departments_from_training_data(spark_session):
    data_file = "test_data/CourseraTrainingSet1.csv"
    raw_data = spark_session.read.option('escape', '"').csv(data_file, header=True)

    clean_data = clean_coursera_data(raw_data)

    matched_departments = clean_data.filter(clean_data['Expected Department'] == clean_data['Department']).count()
    assert matched_departments == clean_data.count()


def test_primary_subjects_from_training_data(spark_session):
    data_file = "test_data/CourseraTrainingSet1.csv"
    raw_data = spark_session.read.option('escape', '"').csv(data_file, header=True)

    clean_data = clean_coursera_data(raw_data)

    # TODO: count rows where 'Expected Department' matches 'Department'
    matched_primary_subjects = clean_data.filter(clean_data['Expected Primary Subject'] == clean_data['Primary Subject']).count()
    assert matched_primary_subjects == clean_data.count()