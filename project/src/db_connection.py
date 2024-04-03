import pandas as pd
import pyodbc
import sqlite3
from settings import *
from utils import *


DB = {"servername": "DESKTOP-OF0CT86\SQLEXPRESS",
      "database": "greatoutdoors"}

export_conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + DB['servername'] + 
                             ';DATABASE=' + DB['database'] + ';Trusted_Connection=yes')

export_cursor = export_conn.cursor()

logger.info("Opening local database: go_sales.sqlite")
sales_db = sqlite3.connect("Databases/GreatOutdoors/go_sales.sqlite")

sales_db = sqlite3.connect("Databases/GreatOutdoors/go_sales.sqlite")


product = pd.read_sql_query("SELECT * FROM product;", sales_db)
country = pd.read_sql_query("SELECT * FROM country;", sales_db)
product_line = pd.read_sql_query("SELECT * FROM product_line;", sales_db)

sales_branch = pd.read_sql_query("SELECT * FROM sales_branch;", sales_db)
retailer_site = pd.read_sql_query("SELECT * FROM retailer_site;", sales_db)
product_type = pd.read_sql_query("SELECT * FROM product_type;", sales_db)
returns = pd.read_sql_query("SELECT * FROM returned_item;", sales_db)
order_details = pd.read_sql_query("SELECT * FROM order_details;", sales_db)
sales_staff = pd.read_sql_query("SELECT * FROM sales_staff;", sales_db)
order_header = pd.read_sql_query("SELECT * FROM order_header;", sales_db)
returned_item  = pd.read_sql_query("SELECT * FROM returned_item;", sales_db)
return_reason  = pd.read_sql_query("SELECT * FROM return_reason;", sales_db)
target = pd.read_sql_query("SELECT * FROM SALES_TARGETData;", sales_db)
order_method = pd.read_sql_query("SELECT * FROM order_method;", sales_db)

staff_db = sqlite3.connect("Databases/GreatOutdoors/go_staff.sqlite")
course = pd.read_sql_query("SELECT * FROM course;", staff_db)
training = pd.read_sql_query("SELECT * FROM training;", staff_db)
satisfaction = pd.read_sql_query("SELECT * FROM satisfaction;", staff_db)
satisfaction_type = pd.read_sql_query("SELECT * FROM satisfaction_type;", staff_db)
sales_staff_go_staff = pd.read_sql_query("SELECT * FROM sales_staff;", staff_db)


crm_db = sqlite3.connect("Databases/GreatOutdoors/go_crm.sqlite")
age_group = pd.read_sql_query("SELECT * FROM age_group;", crm_db)


def import_product():
    # Product
    transformed_product = []

    transformed_product = product.merge(product_type, 'inner', 'PRODUCT_TYPE_CODE').merge(product_line, 'inner', 'PRODUCT_LINE_CODE').rename(columns={
    "INTRODUCTION_DATE": "INTRODUCTION_DATE_date",
    "PRODUCT_TYPE_CODE": "PRODUCT_TYPE_CODE",
    "PRODUCTION_COST": "PRODUCTION_COST_number",
    "MARGIN": "MARGIN_NUMBER",
    "PRODUCT_IMAGE": "PRODUCT_IMAGE_image",
    "LANGUAGE": "LANGUAGE_language",
    "PRODUCT_TYPE_EN": "PRODUCT_TYPE_name",
    "DESCRIPTION": "DESCRIPTION_description",
    }).drop(columns="TRIAL888_x", axis=1).drop(columns="TRIAL888_y", axis=1).drop(columns="TRIAL888", axis=1)

    product_count = 0
    for index, row in transformed_product.iterrows():
        try:
            query = f"INSERT INTO Product VALUES ({row['PRODUCT_NUMBER']},  '{row['PRODUCT_NAME']}', '{ convert_date_format(row['INTRODUCTION_DATE_date']) }', {row['PRODUCT_TYPE_CODE']}, '{row['PRODUCT_TYPE_name']}', {row['PRODUCT_LINE_CODE']}, '{row['PRODUCT_LINE_EN']}', {row['PRODUCTION_COST_number']}, {row['MARGIN_NUMBER']},'{row['PRODUCT_IMAGE_image']}', '{row['LANGUAGE_language']}', '{escape_single_quotes(row['DESCRIPTION_description'])}');"
            export_cursor.execute(query)
            product_count += 1
        except pyodbc.Error as e:
            logger.error(f"Failed to load Product with ID: {row['PRODUCT_NUMBER']}")
            logger.error(query)
            logger.error(e)
            exit(-1)

    export_cursor.commit()
    logger.info(f"Imported {product_count} products")

def import_orders():
    # Order
    merged_df = pd.merge(order_header, order_details, on='ORDER_NUMBER', how='inner')
    order = pd.merge(merged_df, returned_item, on='ORDER_DETAIL_CODE', how = 'left')

    order_count = 0
    for index, row in order.iterrows():
        try:
            query = f"INSERT INTO orders VALUES ({row['ORDER_NUMBER']},  '{escape_single_quotes(row['RETAILER_NAME'])}', '{row['ORDER_DATE']}', {get_day(row['ORDER_DATE'])}, {get_month(row['ORDER_DATE'])}, {get_year(row['ORDER_DATE'])}, {row['ORDER_DETAIL_CODE']}, {row['PRODUCT_NUMBER']}, {row['QUANTITY']}, {row['UNIT_COST']}, {row['UNIT_PRICE']}, {row['UNIT_SALE_PRICE']}, {row['RETURN_CODE'] if row['RETURN_CODE'] == 'nan' else 'NULL' }, '{convert_date_format(strip_time_from_string(row['RETURN_DATE'])) if convert_date_format(strip_time_from_string(row['RETURN_DATE'])) != "NULL" else '1-1-1970' }', {row['RETURN_REASON_CODE'] if row['RETURN_REASON_CODE'] == 'nan' else "NULL"}, {row['RETURN_QUANTITY'] if row['RETURN_QUANTITY'] == 'nan' else "NULL"}, {row['ORDER_METHOD_CODE']}, {row['SALES_STAFF_CODE']}, {row['SALES_BRANCH_CODE']}, {row['RETAILER_SITE_CODE']});"
            export_cursor.execute(query)
            order_count += 1
        except pyodbc.Error as e:
            logger.error(f"Failed to load order with ID: {row['ORDER_NUMBER']}")
            logger.error(query)
            logger.error(e)
            exit(-1)

    export_cursor.commit()
    logger.info(f"Imported {order_count} orders")

def import_order_method():
    order_method_count = 0
    for index, row in order_method.iterrows():
        try:
            query = f"INSERT INTO order_method VALUES ({row['ORDER_METHOD_CODE']}, '{row['ORDER_METHOD_EN']}');"
            export_cursor.execute(query)
            order_method_count += 1
        except pyodbc.Error as e:
            logger.error(f"Failed to load order method with ID: {row['ORDER_METHOD_CODE']}")
            logger.error(query)
            logger.error(e)
            exit(-1)

    export_cursor.commit()
    logger.info(f"Imported {order_method_count} order method(s)")

def import_course():
    course_count = 0
    for index, row in course.iterrows():
        try:
            query = f"INSERT INTO course VALUES ({row['COURSE_CODE']}, '{row['COURSE_DESCRIPTION']}');"
            export_cursor.execute(query)
            course_count += 1
        except pyodbc.Error as e:
            logger.error(f"Failed to load course with ID: {row['COURSE_CODE']}")
            logger.error(query)
            logger.error(e)
            exit(-1)

    export_cursor.commit()
    logger.info(f"Imported {course_count} course(s)")

def import_satisfaction_type():
    satisfaction_type_count = 0
    for index, row in satisfaction_type.iterrows():
        try:
            query = f"INSERT INTO satisfaction_type VALUES ({row['SATISFACTION_TYPE_CODE']}, '{row['SATISFACTION_TYPE_DESCRIPTION']}');"
            export_cursor.execute(query)
            satisfaction_type_count += 1
        except pyodbc.Error as e:
            logger.error(f"Failed to load satisfaction type with index: {index}")
            logger.error(query)
            logger.error(e)
            exit(-1)

    export_cursor.commit()
    logger.info(f"Imported {satisfaction_type_count} satisfaction type(s)")

def import_satisfaction():
    satisfaction_count = 0
    for index, row in satisfaction.iterrows():
        try:
            query = f"INSERT INTO satisfaction VALUES ({row['YEAR']}, {row['SALES_STAFF_CODE']},{row['SATISFACTION_TYPE_CODE']});"
            export_cursor.execute(query)
            satisfaction_count += 1
        except pyodbc.Error as e:
            logger.error(f"Failed to load satisfaction with index: {index}")
            logger.error(query)
            logger.error(e)
            exit(-1)

    export_cursor.commit()
    logger.info(f"Imported {satisfaction_count} satisfaction entries")

def import_training():
    training_count = 0
    for index, row in training.iterrows():
        try:
            query = f"INSERT INTO training VALUES ({row['YEAR']}, {row['SALES_STAFF_CODE']}, {row['COURSE_CODE']});"
            export_cursor.execute(query)
            training_count += 1
        except pyodbc.Error as e:
            logger.error(f"Failed to load training with index: {index}")
            logger.error(query)
            logger.error(e)
            exit(-1)

    export_cursor.commit()
    logger.info(f"Imported {training_count} training entries")

def import_sales_branch():
    sales_branch_count = 0
    # print(sales_branch)
    for index, row in sales_branch.iterrows():
        try:
            query = f"INSERT INTO sales_branch VALUES ({row['SALES_BRANCH_CODE']}, '{escape_single_quotes(row['ADDRESS1'])}', '{row['ADDRESS2']}', '{row['CITY']}', '{row['REGION']}', '{row['POSTAL_ZONE']}', {row['COUNTRY_CODE']});"
            export_cursor.execute(query)
            sales_branch_count += 1
        except pyodbc.Error as e:
            logger.error(f"Failed to load sales branch with index: {index}")
            logger.error(query)
            logger.error(e)
            exit(-1)

    export_cursor.commit()
    logger.info(f"Imported {sales_branch_count} sale branch(es)")

def import_sales_staff():
    sales_staff_count = 0
    for index, row in sales_staff_go_staff.iterrows():
        try:
            query = f"INSERT INTO sales_staff VALUES ({row['SALES_STAFF_CODE']}, '{escape_single_quotes(row['FIRST_NAME'])}', '{row['LAST_NAME']}', '{row['POSITION_EN']}', '{row['WORK_PHONE']}', '{row['EXTENSION']}', '{row['FAX']}', '{row['EMAIL']}',  '{row['DATE_HIRED']}',{row['SALES_BRANCH_CODE']}, {row['MANAGER_CODE']});"
            export_cursor.execute(query)
            sales_staff_count += 1
        except pyodbc.Error as e:
            logger.error(f"Failed to load sales staff with index: {index}")
            logger.error(query)
            logger.error(e)
            exit(-1)

    export_cursor.commit()
    logger.info(f"Imported {sales_staff_count} sales staff entries")


def import_country():
    country_count = 0
    country = pd.read_sql_query("SELECT * FROM country;", sales_db)
    country_crm = pd.read_sql_query("SELECT * FROM country;", crm_db)

    country = country.merge(country_crm, how='inner', on="COUNTRY_CODE")
    for index, row in country.iterrows():
        try:
            query = f"INSERT INTO country VALUES ({row['COUNTRY_CODE']}, '{escape_single_quotes(row['LANGUAGE'])}', '{row['CURRENCY_NAME']}', '{row['COUNTRY_EN']}', '{row['FLAG_IMAGE']}', {row['SALES_TERRITORY_CODE']});"
            export_cursor.execute(query)
            country_count += 1
        except pyodbc.Error as e:
            logger.error(f"Failed to load country with index: {index}")
            logger.error(query)
            logger.error(e)
            exit(-1)

    export_cursor.commit()
    logger.info(f"Imported {country_count} countries")

def import_age_group():
    age_group_count = 0
    for index, row in age_group.iterrows():
        try:
            query = f"INSERT INTO age_group VALUES ({row['AGE_GROUP_CODE']}, {row['UPPER_AGE']}, {row['LOWER_AGE']});"
            export_cursor.execute(query)
            age_group_count += 1
        except pyodbc.Error as e:
            logger.error(f"Failed to load age group with index: {index}")
            logger.error(query)
            logger.error(e)
            exit(-1)

    export_cursor.commit()
    logger.info(f"Imported {age_group_count} age group(s)")


def import_sales_target_data():
    target_data_count = 0
    for index, row in target.iterrows():
        try:
            query = f"INSERT INTO SALES_TargetData VALUES ({row['Id']}, {row['SALES_STAFF_CODE']}, {row['SALES_YEAR']}, {row['SALES_PERIOD']}, '{escape_single_quotes(row['RETAILER_NAME'])}', {row['PRODUCT_NUMBER']}, {row['SALES_TARGET']}, {row['RETAILER_CODE']});"
            export_cursor.execute(query)
            target_data_count += 1
        except pyodbc.Error as e:
            logger.error(f"Failed to load target data entry with index: {target_data_count}")
            logger.error(query)
            logger.error(e)
            exit(-1)

    export_cursor.commit()
    logger.info(f"Imported {target_data_count} target data entries")












