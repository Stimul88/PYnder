import os.path
import configparser
from configparser import ConfigParser as CP
import models as m


def get_db_config(ini_file: str = "db.ini") -> str:
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
        print(f"Configuration file '{ini_file}' not found.")
        exit()

    config = CP()
    config.read(ini_file)
    try:
        db_ip = config.get("DataBase", "IP")
        db_port = config.get("DataBase", "Port")
        db_name = config.get("DataBase", "DBName")
        db_user = config.get("DataBase", "User")
        db_pwd = config.get("DataBase", "Password")
    except configparser.Error as error_msg:
        print(f"Error occurred. {error_msg}")
        exit()

    return f"postgresql://{db_user}:{db_pwd}@{db_ip}:{db_port}/{db_name}"


def create_structure(engine):
    """
    Function creates table structure described in models.py\n
    :param engine: SQLAlchemy engine\n
    :return: None\n
    """

    print("Creating structure")
    m.Base.metadata.create_all(engine)


def delete_structure(engine):
    """
    Function deletes all current structure along with the data\n
    :param engine: SQLAlchemy engine\n
    :return: None\n
    """

    print("Deleting structure")
    m.Base.metadata.drop_all(engine)


def upload_vk_record(session_1, new_record: dict, new_images: dict) -> bool:
    """
    Function uploads record to the database\n
    :param session_1: sessionmaker object
    :param new_record:
    dictionary{vk_user_id:str, first_name:str,last_name:str,city:str,sex:bool,birth_date:date,url:str}
    :param new_images:
    dictionary{vk_user_id:str, images:list[url:str,likes:int]}
    :return: boolean - True if record was uploaded, False if not
    """
    with session_1 as db:
        if is_exists(
            session_1, m.VKUser.vk_user_id, "vk_user_id", new_record["vk_user_id"]
        ):
            return False
        my_record = m.VKUser(
            vk_user_id=new_record["vk_user_id"],
            first_name=new_record["first_name"],
            last_name=new_record["last_name"],
            city=new_record["city"],
            sex=new_record["sex"],
            birth_date=new_record["birth_date"],
            url=new_record["url"],
        )
        db.add(my_record)
        db.commit()
        for image in new_images["images"]:
            my_record = m.Photo(
                vk_user_id=new_images["vk_user_id"], url=image[0], likes=image[1]
            )
            db.add(my_record)
            db.commit()


def upload_owner_record(session_1, new_record: dict) -> bool:
    """
    Function uploads record to the database\n
    :param session_1: sessionmaker object
    :param new_record:
    dictionary{user_id:str}
    :return: boolean - True if record was uploaded, False if not
    """
    with session_1 as db:
        if is_exists(
            session_1, m.Owner.vk_owner_id, "vk_owner_id", new_record["vk_owner_id"]
        ):
            return False
        my_record = m.Owner(vk_owner_id=new_record["vk_owner_id"])
        db.add(my_record)
        db.commit()
    return True


def upload_favourite_record(session_1, new_record: dict) -> bool:
    """
    :param session_1: sessionmaker object
    :param new_record:
    dictionary{vk_user_id: str, owner_id:int}
    :return: boolean - True if record was uploaded, False if not
    """
    with session_1 as db:
        is_user = is_exists(
            session_1, m.Favourite.vk_user_id, "vk_user_id", new_record["vk_user_id"]
        )
        is_vk = is_exists(
            session_1, m.Favourite.vk_owner_id, "vk_owner_id", new_record["vk_owner_id"]
        )
        if is_vk or is_user:
            return False
        my_record = m.Favourite(
            vk_user_id=new_record["vk_user_id"], vk_owner_id=new_record["vk_owner_id"]
        )
        db.add(my_record)
        db.commit()
        return True


def is_exists(session_2, source_, property_: str, value_: str) -> bool:
    """
    :param session_2: sessionmaker object
    :param source_: Table and property object
    :param property_: property name: str
    :param value_: value to be checked
    :return: True if value already exists, False if not
    """
    my_filter = {property_: value_}
    my_query = session_2.query(source_).filter_by(**my_filter)
    return len(my_query.all()) != 0
