import sys

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, BooleanType, DateType, TimestampType
from pyspark.sql.functions import col, when

def read_existing_data(spark):
    # Function body
    # Read existing data from PostgreSQL
    existing_data_df = spark.read.format("jdbc") \
        .option("url", "jdbc:postgresql://ec2-3-9-191-104.eu-west-2.compute.amazonaws.com:5432/testdb") \
        .option("dbtable", "member_schemes") \
        .option("driver", "org.postgresql.Driver") \
        .option("user", "consultants") \
        .option("password", "WelcomeItc@2022") \
        .load()
    return existing_data_df

if __name__ == '__main__':
    spark = SparkSession.builder.master("local[*]").appName("Member Schemes").enableHiveSupport().getOrCreate()
    sc = spark.sparkContext

    # Define the schema for member data
    member_schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("family_id", StringType(), True),
        StructField("member_id", StringType(), True),
        StructField("scheme_id", StringType(), True),
        StructField("sent_approve", IntegerType(), True),
        StructField("scheme_alooted_date", TimestampType(), True),
        StructField("zone", StringType(), True),
        StructField("district_id", StringType(), True),
        StructField("block_code", StringType(), True),
        StructField("ward_village_code", StringType(), True),
        StructField("othersubscheme", StringType(), True),
        StructField("scheme_comment", StringType(), True),
        StructField("otherdepartment", StringType(), True),
        StructField("otherscheme", StringType(), True),
        StructField("scheme_department_id", StringType(), True),
        StructField("sch_cat_dep_rel_id", StringType(), True),
        StructField("newdepart_id", IntegerType(), True),
        StructField("newschm_id", IntegerType(), True),
        StructField("reject_status", IntegerType(), True),
        StructField("approved_by_district_user_id", StringType(), True),
        StructField("rejected_by_district_user_id", StringType(), True),
        StructField("sention_remarks", StringType(), True),
        StructField("sention_status", IntegerType(), True),
        StructField("sanction_date", TimestampType(), True),
        StructField("noscheme", IntegerType(), True),
        StructField("transfer_from_dep", StringType(), True),
        StructField("transfer_from_scheme", StringType(), True),
        StructField("transfer_from_dist", StringType(), True),
        StructField("loan_amount", StringType(), True),
        StructField("incomeIncreaseUpto", StringType(), True),
        StructField("radiobuttonStatus", StringType(), True),
        StructField("member_scheme_active", BooleanType(), True)
    ])

    # Read member data
    member_df = spark.read.option("header", True).schema(member_schema).csv(sys.argv[1])

    # Read existing data
    existing_data_df = read_existing_data(spark)

    # Data transformation and filtering
    member_df = member_df.withColumn("age_category", when(col("age") < 18, "Child")
                                     .when((col("age") >= 18) & (col("age") < 60), "Adult")
                                     .otherwise("Senior"))

    # Drop 'otherdepartment' column
    col_to_drop = ['otherdepartment']
    member_df = member_df.drop(*col_to_drop)

    # Identify new or updated records based on a unique identifier
    unique_identifier = ['id', 'user_id', 'family_id', 'member_id']  # Modify this as per your requirements
    new_records_df = member_df.join(existing_data_df, unique_identifier, "left_anti")

    # Append new records to existing data
    updated_data_df = existing_data_df.union(new_records_df)

    # Show transformed DataFrame
    updated_data_df.show()

    # Write updated member data to PostgreSQL
    updated_data_df.write.format("jdbc") \
        .mode("overwrite") \
        .option("url", "jdbc:postgresql://ec2-3-9-191-104.eu-west-2.compute.amazonaws.com:5432/testdb") \
        .option("dbtable", "member_schemes") \
        .option("driver", "org.postgresql.Driver") \
        .option("user", "consultants") \
        .option("password", "WelcomeItc@2022") \
        .save()

    # Write updated member data to Hive
    updated_data_df.write.mode("overwrite").option("header", True).saveAsTable("itc_project.member_schemes")

    # Stop Spark session
    spark.stop()
