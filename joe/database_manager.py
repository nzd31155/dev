"""

Script contains functions for interacting with the backend postgresDB.

"""

import pymysql
import joe.config as _cfg


def connect_db(dbname):
    """
    
    Generic database connection function.
    
    :param dbname: 
    :return: database connection
    """

    if dbname != _cfg.DATABASE_CONFIG['dbname']:
        raise ValueError("Couldn't not find DB with given name")
    conn = pymysql.connect(host=_cfg.DATABASE_CONFIG['host'],
                           user=_cfg.DATABASE_CONFIG['user'],
                           password=_cfg.DATABASE_CONFIG['password'],
                           db=_cfg.DATABASE_CONFIG['dbname'])
    return conn
