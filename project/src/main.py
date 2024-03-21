from settings import *
from db_connection import *
def main():
    logger.info("Loading raw data")

    logger.info("Moving processed data table: Product into database")
    import_product()

    

def import_data():
    return

if __name__ == "__main__":
    main()
