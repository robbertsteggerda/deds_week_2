from settings import *
from db_connection import *
import sys

def main():
   
    
    if len(sys.argv) > 1 and sys.argv[1] == '--drop-all':
        query = f"DELETE FROM course; DELETE FROM order_method; DELETE FROM orders; DELETE FROM Product; DELETE FROM Retailer; DELETE FROM retailer_site; DELETE FROM sales_branch; DELETE FROM sales_staff; DELETE FROM SALES_TargetData; DELETE FROM SALESDATA; DELETE FROM satisfaction; DELETE FROM satisfaction_type; DELETE FROM training; DELETE FROM sales_staff; DELETE FROM country; DELETE FROM age_group; DROP TRIGGER IF EXISTS update_fsk_after_order_insert;"
        export_cursor.execute(query)
        export_cursor.commit()
    
    # if sys.argv[1] == '--surrogate-test':
    #     query = f"INSERT INTO sales_staff  (SALES_STAFF_CODE_PK,FIRST_NAME,LAST_NAME, POSITION_EN, WORK_PHONE, EXTENSION, FAX, EMAIL, DATE_HIRED_DATE, SALES_BRANCH_CODE, MANAGER_CODE) VALUES ({row['SALES_STAFF_CODE']}, '{escape_single_quotes(row['FIRST_NAME'])}', '{row['LAST_NAME']}', '{row['POSITION_EN']}', '{row['WORK_PHONE']}', '{row['EXTENSION']}', '{row['FAX']}', '{row['EMAIL']}',  '{row['DATE_HIRED']}',{row['SALES_BRANCH_CODE']}, {row['MANAGER_CODE']});"
    #     export_cursor.execute(query)
    #     export_cursor.commit()
    
    
    
    logger.info("Loading raw data")

    logger.info("Moving processed data table: Product into database")
    import_product()

    logger.info("Moving processed data table: Product Type into database")
    import_product_type()

    

    logger.info("Moving processed data table: Order Method into database")
    import_order_method()

    logger.info("Moving processed data table: Course into database")
    import_course()
    
    logger.info("Moving processed data table: Training into database")
    import_training()

    logger.info("Moving processed data table: Satisfaction_Type into database")
    import_satisfaction_type()

    logger.info("Moving processed data table: Satisfaction into database")
    import_satisfaction()

    logger.info("Moving processed data table: Sales Branch into database")
    import_sales_branch()

    logger.info("Moving processed data table: Sales Staff into database")
    import_sales_staff()

    logger.info("Moving processed data table: Country into database")
    import_country()

    logger.info("Moving processed data table: Age Group into database")
    import_age_group()

    logger.info("Moving processed data table: Sales Target Data into database")
    import_sales_target_data()

    logger.info("Moving processed data table: Order into database")
    import_orders()

    
    logger.info("Moving processed data table: Retailer Site Data into database")
    import_retailer_site_data()

# (RETAILER_SITE_code,RETAILER_TYPE_code,RETAILER_TYPE_en,RETAILER_code,RETAILER_name,RETAILER_company_name,RETAILER_CONTACT_code,RETAILER_HEADQUARTERS_phone,RETAILER_HEADQUARTERS_fax,RETAILER_HEADQUARTERS_segment_code,COUNTRY_code, REGION_name, CITY_name, RETAILER_SITE_address1, RETAILER_SITE_address2, POSTAL_ZONE_text, ACTIVE_INDICATOR_code) 
    

    


    logger.success("Imported all tables!")


def import_data():
    return

if __name__ == "__main__":
    main()
