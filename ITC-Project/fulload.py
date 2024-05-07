import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, BooleanType, DateType, TimestampType

if __name__ == '__main__':
    # Initialize Spark session
    spark = SparkSession.builder.master("local[*]").appName("Member Schemes").enableHiveSupport().getOrCreate()
    
    # Define Spark context
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

    # Read member data from CSV
    try:
        members_data_frame = spark.read.csv(sys.argv[1], header=True, schema=member_schema, nullValue="NULL")
    except Exception as e:
        print("Error occurred while reading the CSV file:", e)
        sys.exit(1)

    # Write member data to CSV
    try:
        members_data_frame.coalesce(1).write.mode("overwrite").option("header", True).csv(sys.argv[2])
    except Exception as e:
        print("Error occurred while writing data to CSV:", e)
        sys.exit(1)

    # Write member data to PostgreSQL
    try:
        members_data_frame.write.format("jdbc") \
            .mode("overwrite") \
            .option("url", "jdbc:postgresql://ec2-3-9-191-104.eu-west-2.compute.amazonaws.com:5432/testdb") \
            .option("dbtable", "member_schemes1") \
            .option("driver", "org.postgresql.Driver") \
            .option("user", "consultants") \
            .option("password", "WelcomeItc@2022") \
            .save()
    except Exception as e:
        print("Error occurred while writing data to PostgreSQL:", e)
        sys.exit(1)

    # Write member data to Hive
    try:
        members_data_frame.write.mode("overwrite").option("header", True).saveAsTable("itc_project.member_schemes")
    except Exception as e:
        print("Error occurred while writing data to Hive:", e)
        sys.exit(1)

    # Stop Spark session
    spark.stop()

