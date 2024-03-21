from settings import *
from db_connection import *
def main():
    logger.info("Loading raw data")

    logger.info("Moving processed data table: Product into database")
    import_product()

    logger.info("Moving processed data table: Order into database")
    import_orders()

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

    


    logger.success("Imported all tables!")
    


    


    

    

    

def import_data():
    return

if __name__ == "__main__":
    main()
