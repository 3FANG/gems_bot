from loguru import logger

def create_query(connection, query: str):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except Exception as ex:
        logger.error(ex)
