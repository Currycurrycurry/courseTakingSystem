from django.db import connection
from selectCourse.logs.logger import logger
from selectCourse.constants.errorConstants import *


def dictfetchone(cursor):
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row is None:
        return None
    else:
        tmp = list(row)
        return dict(zip(columns,tmp))
       
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns,row))
        for row in cursor.fetchall()
    ]

def select_one_sql(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        return row
    except Exception as e:
        logger.error(sql)
        logger.error(e)
        connection.rollback()
        return SELECT_ONE_SQL_ERROR

def select_many_sql(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.dictfetchall()
        return rows
    except Exception as e:
        logger.error(sql)
        logger.error(e)
        connection.rollback()
        return SELECT_MANY_SQL_ERROR

def insert_sql(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        return EXECUTE_SUCCESSFULLY
    except Exception as e:
        logger.error(sql)
        logger.error(e)
        connection.rollback()
        return INSERT_SQL_ERROR

def insert_sql(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        return EXECUTE_SUCCESSFULLY
    except Exception as e:
        logger.error(sql)
        logger.error(e)
        connection.rollback()
        return INSERT_SQL_ERROR

def delete_sql(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        return EXECUTE_SUCCESSFULLY
    except Exception as e:
        logger.error(sql)
        logger.error(e)
        connection.rollback()
        return DELETE_SQL_ERROR

def update_sql(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        return EXECUTE_SUCCESSFULLY
    except Exception as e:
        logger.error(sql)
        logger.error(e)
        connection.rollback()
        return UPDATE_SQL_ERROR

   