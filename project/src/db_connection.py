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

    export_cursor.commit()
    logger.info(f"Imported {product_count} products")



