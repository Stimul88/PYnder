import os.path
import configparser
import models as m
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker


class PYnder_DB:
    def __init__(self):
        self.engine = sq.create_engine(self.get_db_config("db.ini"))
        self.delete_structure()
        self.create_structure()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_pk(self, table_, id_: str) -> int:
        """
        Function searches for a PK in mentioned table_ using id_
        :param table_ table object with parameter, e.g. m.VKUser.id
        :param id_: VK ID:
        :return: PK ID or -1 if not found
        """

        with self.session as db:
            my_query = db.query(table_).filter_by(vk_id=id_)
            if my_query.count == 0:
                return -1
            else:
                return my_query.first()[0]

    def is_in_favorite(self, vk_user_id_: str, vk_owner_id_: str) -> bool:
        """
        Function checks is there a VK User in Owner's Favorites
        :param vk_user_id_: User's VK ID
        :param vk_owner_id_: Owner's VK ID
        :return: True if in Favorites, False otherwise
        """
        with self.session as db:
            user_pk_ = self.get_pk(m.VKUser.id, vk_user_id_)
            if user_pk_ == -1:
                return False
            my_query = db.query(m.Favorite.user_id).filter_by(user_id=user_pk_)
            if my_query.count() == 0:
                return False
            owner_pk_ = self.get_pk(m.Owner.id, vk_owner_id_)
            if owner_pk_ == -1:
                return False
            my_query = db.query(m.Favorite.owner_id).filter_by(owner_id=owner_pk_)
            if my_query.count() == 0:
                return False
            return True

    def delete_favorite(self, vk_user_id_: str, vk_owner_id_: str):
        """
        :param vk_user_id_: str(50) - VK User ID to be removed
        :param vk_owner_id_: str(50) - Owner's VK ID
        """

        # checking is this record exists, if not - exiting

        with self.session as db:
            my_query = db.query(m.VKUser.id).filter_by(vk_id=vk_user_id_)
            if my_query.count() == 0:
                return
            user_pk_ = my_query.first()[0]
            my_query = db.query(m.Favorite.user_id).filter_by(user_id=user_pk_)
            if my_query.count() == 0:
                return

            my_query = db.query(m.Owner.id).filter_by(vk_id=vk_owner_id_)
            if my_query.count() == 0:
                return
            owner_pk_ = my_query.first()[0]
            my_query = db.query(m.Favorite.owner_id).filter_by(owner_id=owner_pk_)
            if my_query.count() == 0:
                return

            db.query(m.Favorite).filter_by(
                user_id=user_pk_, owner_id=owner_pk_
            ).delete()
            db.commit()

            # checking are there any other owners who added same VK ID into the favorites
            # if no - removing VK ID from other tables
            my_query = db.query(m.Favorite.user_id).filter_by(user_id=vk_user_id_)
            if my_query.count() == 0:
                db.query(m.Photo).filter_by(user_id=user_pk_).delete()
                db.commit()
                db.query(m.VKUser).filter_by(vk_id=vk_user_id_).delete()
                db.commit()

    def get_db_config(self, ini_file: str = "db.ini") -> str:
        """
        Function reads from ini file following parameters from section [DataBase]:\n
        IP = IP address where DB is running in general format, e.g. 127.0.0.1\n
        Port = database port, e.g. 5432\n
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

        config = configparser.ConfigParser()
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

    def create_structure(self):
        """
        Function creates table structure described in models.py\n
        :return: None\n
        """

        print("Creating structure")
        m.Base.metadata.create_all(self.engine)

    def delete_structure(self):
        """
        Function deletes all current structure along with the data\n
        :return: None\n
        """

        print("Deleting structure")
        m.Base.metadata.drop_all(self.engine)

    def add_owner(self, owner_id_: str) -> bool:
        """
        Function uploads record to the database\n
        :param owner_id_: str(50) - owner ID
        :return: boolean - True if record was uploaded, False if not (already exists)
        """
        with self.session as db:
            my_query = db.query(m.Owner.vk_id).filter_by(vk_id=owner_id_)
            if my_query.count() == 0:
                my_record = m.Owner(vk_id=owner_id_)
                db.add(my_record)
                db.commit()
                print(f"Owner {owner_id_} added")
                return True
        return False

    def add_favorite(self, new_record: dict, vk_owner_id_: str):
        """
        :param new_record:dictionary{
            vk_id:str(50),
            first_name:str(20),
            last_name:str(20),
            city(20):str,
            sex:bool,
            birth_date:date,
            url:str,
            images[['image_1.jpg, likes_1], ['image_2.jpg, likes_2], ['image_3.jpg, likes_3]]
            }
        :param vk_owner_id_: str(50) - Owner's VK ID
        """

        with self.session as db:
            my_query = db.query(m.VKUser.vk_id).filter_by(vk_id=new_record["vk_id"])
            is_user_exists = my_query.count() != 0
            if not is_user_exists:
                # adding IDs into the table VKUsers if not exists
                my_record = m.VKUser(
                    vk_id=new_record["vk_id"],
                    first_name=new_record["first_name"],
                    last_name=new_record["last_name"],
                    city=new_record["city"],
                    sex=new_record["sex"],
                    birth_date=new_record["birth_date"],
                    url=new_record["url"],
                )
                db.add(my_record)
                db.commit()
                print(f'Record for user {new_record["vk_id"]} added')

            # Getting primary keys for the Favorite table
            my_query = db.query(m.Owner.id).filter_by(vk_id=vk_owner_id_)
            owner_pk = my_query.first()[0]
            my_query = db.query(m.VKUser.id).filter_by(vk_id=new_record["vk_id"])
            user_pk = my_query.first()[0]

            if not is_user_exists:
                # adding photos into the table Photo if user not exists
                for image in new_record["images"]:
                    my_record = m.Photo(user_id=user_pk, url=image[0], likes=image[1])
                    db.add(my_record)
                    db.commit()
                    print(f"Image {image[0]} added")

            # adding IDs into the table Favorite
            my_record = m.Favorite(user_id=user_pk, owner_id=owner_pk)
            db.add(my_record)
            db.commit()
            print(f"Favorite record added")

    def import_test_data(self):
        owner_id = "1_owner"
        self.add_owner(owner_id)
        vk_user_dict = {
            "vk_id": "a781362360",
            "first_name": "Test",
            "last_name": "User",
            "city": "Москва",
            "sex": True,
            "birth_date": "30.06.1979",
            "url": "https://vk.com/781362360",
            "images": [["image1.jpg", 12], ["image2.jpg", 11], ["image3.jpg", 55]],
        }
        self.add_favorite(vk_user_dict, owner_id)

        owner_id = "1_owner"
        self.add_owner(owner_id)
        vk_user_dict = {
            "vk_id": "a781362360",
            "first_name": "Test",
            "last_name": "User",
            "city": "Москва",
            "sex": True,
            "birth_date": "30.06.1979",
            "url": "https://vk.com/781362360",
            "images": [["image1.jpg", 12], ["image2.jpg", 11], ["image3.jpg", 55]],
        }
        self.add_favorite(vk_user_dict, owner_id)

        owner_id = "2_owner"
        self.add_owner(owner_id)
        vk_user_dict = {
            "vk_id": "a123",
            "first_name": "Test_2",
            "last_name": "User_2",
            "city": "Toronto",
            "sex": False,
            "birth_date": "30.06.1979",
            "url": "https://vk.com/a123",
            "images": [
                ["image1_2.jpg", 12],
                ["image2_2.jpg", 11],
                ["image3_3.jpg", 55],
            ],
        }
        self.add_favorite(vk_user_dict, owner_id)

        owner_id = "3_owner"
        self.add_owner(owner_id)
        vk_user_dict = {
            "vk_id": "a781362360",
            "first_name": "Test",
            "last_name": "User",
            "city": "Москва",
            "sex": True,
            "birth_date": "30.06.1979",
            "url": "https://vk.com/781362360",
            "images": [["image1.jpg", 12], ["image2.jpg", 11], ["image3.jpg", 55]],
        }
        self.add_favorite(vk_user_dict, owner_id)

        owner_id = "4_owner"
        self.add_owner(owner_id)
        vk_user_dict = {
            "vk_id": "222",
            "first_name": "Test",
            "last_name": "User",
            "city": "Washington",
            "sex": False,
            "birth_date": "30.06.1979",
            "url": "https://vk.com/222",
            "images": [["image1.jpg", 12], ["image2.jpg", 11], ["image3.jpg", 55]],
        }
        self.add_favorite(vk_user_dict, owner_id)
