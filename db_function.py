import os.path
import configparser
from configparser import ConfigParser as CP
import models as m


def get_db_config(ini_file: str = 'db.ini') -> str:
    """
    Function reads from ini file following parameters from section [DataBase]:\n
    IP = IP address where DB is running in general format, e.g. 127.0.0.1\n
    Port = database port in common format, e.g. 5432\n
    DBName = database name\n
    User = username\n
    Password = password\n
    :param ini_file: .ini filename with path if necessary, by default - db.ini\n
    :return: DSN string for sqlalchemy engine creation:\n
    postgresql://{db_user}:{db_pwd}@{db_ip}:{db_port}/{db_name}\n
    """

    if not os.path.exists(ini_file):
        print(f'Configuration file \'{ini_file}\' not found.')
        exit()

    config = CP()
    config.read(ini_file)
    try:
        db_ip = config.get('DataBase', 'IP')
        db_port = config.get('DataBase', 'Port')
        db_name = config.get('DataBase', 'DBName')
        db_user = config.get('DataBase', 'User')
        db_pwd = config.get('DataBase', 'Password')
    except configparser.Error as error_msg:
        print(f'Error occurred. {error_msg}')
        exit()

    return f'postgresql://{db_user}:{db_pwd}@{db_ip}:{db_port}/{db_name}'


def create_structure(engine):
    """
    Function creates table structure described in models.py\n
    :param engine: SQLAlchemy engine\n
    :return: None\n
    """

    m.Base.metadata.create_all(engine)


def delete_structure(engine):
    """
    Function deletes all current structure alongwith the data\n
    :param engine: SQLAlchemy engine\n
    :return: None\n
    """

    m.Base.metadata.drop_all(engine)
