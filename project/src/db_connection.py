import pandas as pd
import pyodbc
import sqlite3
from settings import *
from utils import *


DB = {"servername": "DESKTOP-1416MJP\SQLEXPRESS",
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

staff_db = sqlite3.connect("Databases/GreatOutdoors/go_staff.sqlite")
course = pd.read_sql_query("SELECT * FROM course;", staff_db)
training = pd.read_sql_query("SELECT * FROM training;", staff_db)
satisfaction = pd.read_sql_query("SELECT * FROM satisfaction;", staff_db)
satisfaction_type = pd.read_sql_query("SELECT * FROM satisfaction_type;", staff_db)
sales_staff_go_staff = pd.read_sql_query("SELECT * FROM sales_staff;", staff_db)


crm_db = sqlite3.connect("Databases/GreatOutdoors/go_crm.sqlite")
age_group = pd.read_sql_query("SELECT * FROM age_group;", crm_db)
retailer = pd.read_sql_query("SELECT * FROM retailer;", crm_db)
retailer_type = pd.read_sql_query("SELECT * FROM retailer_type;", crm_db)



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

def import_product_type():
    # Product Type

    product_count = 0
    for index, row in product_type.iterrows():
        try:
            query = f"INSERT INTO PRODUCT_TYPE VALUES ({row['PRODUCT_TYPE_CODE']}, {row['PRODUCT_LINE_CODE']},  '{row['PRODUCT_TYPE_EN']}');"
            export_cursor.execute(query)
            product_count += 1
        except pyodbc.Error as e:
            logger.error(f"Failed to load Product Line with ID: {row['PRODUCT_TYPE_CODE']}")
            logger.error(query)
            logger.error(e)
            exit(-1)

    export_cursor.commit()
    logger.info(f"Imported {product_count} product types")



def import_orders():
    # Order
    merged_df = pd.merge(order_header, order_details, on='ORDER_NUMBER', how='inner')
    order = pd.merge(merged_df, returned_item, on='ORDER_DETAIL_CODE', how = 'left').merge(returned_item, how='left', left_on="ORDER_DETAIL_CODE", right_on="ORDER_DETAIL_CODE")

    order = order.drop(['RETURN_DATE_x', 'RETURN_REASON_CODE_x', 'RETURN_QUANTITY_x'], axis=1).rename(columns={
    "ORDER_DETAIL_CODE_x": "ORDER_DETAIL_CODE",
    "RETURN_REASON_CODE_y": "RETURN_REASON_CODE",
    "RETURN_QUANTITY_y": "RETURN_QUANTITY",
    "RETURN_DATE_y": "RETURN_DATE",
    "RETURN_CODE_y": "RETURN_CODE"
    })
    # print(order.loc[order['ORDER_NUMBER'] == "1229", :])

    # print(order.columns)

    order_count = 0
    for index, row in order.iterrows():
        try:
            return_date = convert_date_format(strip_time_from_string(row['RETURN_DATE'])) if convert_date_format(strip_time_from_string(row['RETURN_DATE'])) != "NULL" else "NULL"
            return_code = row['RETURN_CODE'] if row['RETURN_CODE'] != 'nan' else 'NULL'
            return_reason_code = row['RETURN_REASON_CODE'] if row['RETURN_REASON_CODE'] != 'nan' else 'NULL'
            return_quantity = row['RETURN_QUANTITY'] if row['RETURN_QUANTITY'] != 'nan' else 'NULL'
            
            
            # print(f"return code: {row['RETURN_CODE']}")
            # print(f"return reason code: {row['RETURN_REASON_CODE']}")
            # print(f"return quantity: {row['RETURN_QUANTITY']}")


            if return_date != "NULL": # date is available
                query = f"INSERT INTO orders (order_number_pk, retailer_name, order_date, order_day, order_month, order_year, order_detail_code, order_detail_product_number, order_detail_quantity, order_detail_unit_cost, order_detail_unit_price, order_detail_unit_sale_price, return_code, return_date, return_reason_code, return_quantity, order_method_code, sales_staff_code_fk, sales_staff_code_fsk, sales_branch_code, retailer_site_code) VALUES ({row['ORDER_NUMBER']}, '{escape_single_quotes(row['RETAILER_NAME'])}', '{row['ORDER_DATE']}', {get_day(row['ORDER_DATE'])}, {get_month(row['ORDER_DATE'])}, {get_year(row['ORDER_DATE'])}, {row['ORDER_DETAIL_CODE']}, {row['PRODUCT_NUMBER']}, {row['QUANTITY']}, {row['UNIT_COST']}, {row['UNIT_PRICE']}, {row['UNIT_SALE_PRICE']}, {return_code}, '{return_date}', {return_reason_code}, {return_quantity}, {row['ORDER_METHOD_CODE']}, {row['SALES_STAFF_CODE']}, {row['SALES_STAFF_CODE']}, {row['SALES_BRANCH_CODE']}, {row['RETAILER_SITE_CODE']});"
            else:    
                query = f"INSERT INTO orders (order_number_pk, retailer_name, order_date, order_day, order_month, order_year, order_detail_code, order_detail_product_number, order_detail_quantity, order_detail_unit_cost, order_detail_unit_price, order_detail_unit_sale_price, return_code, return_date, return_reason_code, return_quantity, order_method_code, sales_staff_code_fk, sales_staff_code_fsk, sales_branch_code, retailer_site_code) VALUES ({row['ORDER_NUMBER']}, '{escape_single_quotes(row['RETAILER_NAME'])}', '{row['ORDER_DATE']}', {get_day(row['ORDER_DATE'])}, {get_month(row['ORDER_DATE'])}, {get_year(row['ORDER_DATE'])}, {row['ORDER_DETAIL_CODE']}, {row['PRODUCT_NUMBER']}, {row['QUANTITY']}, {row['UNIT_COST']}, {row['UNIT_PRICE']}, {row['UNIT_SALE_PRICE']}, {row['RETURN_CODE'] if row['RETURN_CODE'] == 'nan' else 'NULL' }, {return_date}, {row['RETURN_REASON_CODE'] if row['RETURN_REASON_CODE'] == 'nan' else "NULL"}, {row['RETURN_QUANTITY'] if row['RETURN_QUANTITY'] == 'nan' else "NULL"}, {row['ORDER_METHOD_CODE']}, {row['SALES_STAFF_CODE']}, {row['SALES_STAFF_CODE']}, {row['SALES_BRANCH_CODE']}, {row['RETAILER_SITE_CODE']});"
            if(row['ORDER_NUMBER'] == '1229'):
                print(row)
                print(row['RETURN_CODE'])
            if(order_count > 43060):
                print(query)
            export_cursor.execute(query)
            order_count += 1
        except pyodbc.Error as e:
            logger.error(f"Failed to load order with ID: {row['ORDER_NUMBER']}")
            logger.error(query)
            logger.error(e)
            exit(-1)

    # install trigger after importing (faster import)

    install_trigger = "CREATE TRIGGER update_fsk_after_order_insert ON orders AFTER INSERT AS BEGIN UPDATE o SET o.SALES_STAFF_CODE_FSK = ss.SALES_STAFF_CODE_SK FROM orders o INNER JOIN inserted i ON o.SALES_STAFF_CODE_FK = i.SALES_STAFF_CODE_FK INNER JOIN (SELECT sales_staff.SALES_STAFF_CODE_PK, MAX(sales_staff.SALES_STAFF_CODE_SK) AS MAX_SALES_STAFF_CODE_SK FROM sales_staff INNER JOIN inserted ON sales_staff.SALES_STAFF_CODE_PK = inserted.SALES_STAFF_CODE_FK WHERE sales_staff.timestmp <= inserted.tstamp GROUP BY sales_staff.SALES_STAFF_CODE_PK) ss_max ON i.SALES_STAFF_CODE_FK = ss_max.SALES_STAFF_CODE_PK INNER JOIN sales_staff ss ON ss.SALES_STAFF_CODE_PK = ss_max.SALES_STAFF_CODE_PK AND ss.SALES_STAFF_CODE_SK = ss_max.MAX_SALES_STAFF_CODE_SK WHERE o.tstamp = i.tstamp; END;"
    export_cursor.execute(install_trigger)
    export_cursor.commit()
    logger.info("Installed Trigger: update_fsk_after_order_insert")
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
            query = f"INSERT INTO sales_staff (SALES_STAFF_CODE_PK,SALES_STAFF_FIRST_NAME,SALES_STAFF_LAST_NAME,SALES_STAFF_POSITION_EN,SALES_STAFF_WORK_PHONE,SALES_STAFF_EXTENSION,SALES_STAFF_FAX,SALES_STAFF_EMAIL,SALES_STAFF_DATE_HIRED_DATE,SALES_STAFF_SALES_BRANCH_CODE, SALES_STAFF_MANAGER_CODE) VALUES ({row['SALES_STAFF_CODE']}, '{escape_single_quotes(row['FIRST_NAME'])}', '{row['LAST_NAME']}', '{row['POSITION_EN']}', '{row['WORK_PHONE']}', '{row['EXTENSION']}', '{row['FAX']}', '{row['EMAIL']}',  '{row['DATE_HIRED']}',{row['SALES_BRANCH_CODE']}, {row['MANAGER_CODE']});"
            export_cursor.execute(query)

            if(row['SALES_STAFF_CODE'] == '27'):
                print(query)
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

def import_retailer_site_data():
    retailer_site_data_count = 0
    fully_merged_retailer_site = retailer_site.merge(right=retailer, how='inner', on="RETAILER_CODE").merge(right=retailer_type, how='inner', on="RETAILER_TYPE_CODE" ).drop(["TRIAL219", "TRIAL222", "TRIAL888"], axis=1)
    
    # print(fully_merged_retailer_site.columns)
    for index, row in fully_merged_retailer_site.iterrows():
        try:
            # print(row)
            query = f"INSERT INTO retailer_site (RETAILER_SITE_CODE,RETAILER_TYPE_CODE,RETAILER_TYPE_EN,RETAILER_CODE,RETAILER_COMPANY_NAME,RETAILER_CONTACT_code,RETAILER_HEADQUARTERS_phone,RETAILER_HEADQUARTERS_fax,RETAILER_HEADQUARTERS_segment_code, RETAILER_SITE_COUNTRY_code, RETAILER_SITE_REGION_name, RETAILER_SITE_CITY_name, RETAILER_SITE_address1, RETAILER_SITE_address2, RETAILER_SITE_POSTAL_ZONE_text, ACTIVE_INDICATOR_code) VALUES ({row['RETAILER_SITE_CODE']}, {row['RETAILER_TYPE_CODE']}, '{row['RETAILER_TYPE_EN']}', {row['RETAILER_CODE']}, '{escape_single_quotes(row['COMPANY_NAME'])}', 0, 0, 0,0,{row['COUNTRY_CODE']},'{row['REGION']}','{escape_single_quotes(row['CITY'])}',0,0,0,0);"
            # print(query)
            export_cursor.execute(query)
            retailer_site_data_count += 1
    
        except pyodbc.Error as e:
            logger.error(f"Failed to load retailer site entry with index: {retailer_site_data_count}")
            logger.error(query)
            logger.error(e)
            exit(-1)

    export_cursor.commit()
    logger.info(f"Imported {retailer_site_data_count} retailer site entries")

# def import_retailer():
#     retailer_data_count = 0
#     fully_merged_retailer_site = retailer_site.merge(right=retailer, how='inner', on="RETAILER_CODE").merge(right=retailer_type, how='inner', on="RETAILER_TYPE_CODE" ).drop(["TRIAL219", "TRIAL222", "TRIAL888"], axis=1)
    
#     # print(fully_merged_retailer_site.columns)
#     for index, row in fully_merged_retailer_site.iterrows():
#         try:
#             # print(row)
#             query = f"INSERT INTO retailer_site (RETAILER_SITE_CODE,RETAILER_TYPE_CODE,RETAILER_TYPE_EN,RETAILER_CODE,RETAILER_COMPANY_NAME,RETAILER_CONTACT_code,RETAILER_HEADQUARTERS_phone,RETAILER_HEADQUARTERS_fax,RETAILER_HEADQUARTERS_segment_code,COUNTRY_code, REGION_name, CITY_name, RETAILER_SITE_address1, RETAILER_SITE_address2, POSTAL_ZONE_text, ACTIVE_INDICATOR_code) VALUES ({row['RETAILER_SITE_CODE']}, {row['RETAILER_TYPE_CODE']}, '{row['RETAILER_TYPE_EN']}', {row['RETAILER_CODE']}, '{escape_single_quotes(row['COMPANY_NAME'])}', 0, 0, 0,0,{row['COUNTRY_CODE']},'{row['REGION']}','{escape_single_quotes(row['CITY'])}',0,0,0,0);"
#             # print(query)
#             export_cursor.execute(query)
#             retailer_data_count += 1
    
#         except pyodbc.Error as e:
#             logger.error(f"Failed to load retailer site entry with index: {retailer_data_count}")
#             logger.error(query)
#             logger.error(e)
#             exit(-1)

#     export_cursor.commit()
#     logger.info(f"Imported {retailer_data_count} retailer site entries")




def import_return_reason():
    return_reason_count = 0

    for index, row in return_reason.iterrows():
        try:
            print(row)
            query = f"INSERT INTO return_reason (RETURN_REASON_CODE,RETURN_REASON_DESCRIPTION) VALUES ({row['RETURN_REASON_CODE']}, '{row['RETURN_DESCRIPTION_EN']}');"
            # print(query)
            export_cursor.execute(query)
            return_reason_count += 1
    
        except pyodbc.Error as e:
            logger.error(f"Failed to load return reason entry with index: {return_reason_count}")
            logger.error(query)
            logger.error(e)
            exit(-1)

    export_cursor.commit()
    logger.info(f"Imported {return_reason_count} return reason entries")


# CREATE TRIGGER update_fsk_after_order_insert
# ON orders
# AFTER INSERT
# AS
# BEGIN
#     UPDATE o
#     SET o.SALES_STAFF_CODE_FSK = ss.SALES_STAFF_CODE_SK
#     FROM orders o
#     INNER JOIN inserted i ON o.SALES_STAFF_CODE_FK = i.SALES_STAFF_CODE_FK
#     INNER JOIN (
#         SELECT sales_staff.SALES_STAFF_CODE_PK, MAX(sales_staff.SALES_STAFF_CODE_SK) AS MAX_SALES_STAFF_CODE_SK
#         FROM sales_staff
#         INNER JOIN inserted ON sales_staff.SALES_STAFF_CODE_PK = inserted.SALES_STAFF_CODE_FK
#         WHERE sales_staff.timestmp <= inserted.tstamp
#         GROUP BY sales_staff.SALES_STAFF_CODE_PK
#     ) ss_max ON i.SALES_STAFF_CODE_FK = ss_max.SALES_STAFF_CODE_PK
#     INNER JOIN sales_staff ss ON ss.SALES_STAFF_CODE_PK = ss_max.SALES_STAFF_CODE_PK AND ss.SALES_STAFF_CODE_SK = ss_max.MAX_SALES_STAFF_CODE_SK
#     WHERE o.tstamp = i.tstamp;
# END;




# INSERT INTO sales_staff (SALES_STAFF_CODE_PK,FIRST_NAME,LAST_NAME,POSITION_EN,WORK_PHONE,EXTENSION,FAX,EMAIL,DATE_HIRED_DATE,SALES_BRANCH_CODE, MANAGER_CODE) VALUES (100, 'Tuomasso', 'Savolainen', 'Level 2 Sales Representative', '+358(0)17 - 433 127', '825', '+358(0)17 - 433 129', 'TSavolainen@grtd123.com',  '23-Jul-1998 12:00:00 AM',31, 18)







