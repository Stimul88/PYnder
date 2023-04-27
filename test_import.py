import db_function as dbf


def import_test_data(session_):
    owner_id = '1'
    dbf.add_owner(session_, owner_id)
    owner_id = '1'
    dbf.add_owner(session_, owner_id)
    owner_id = '2'
    dbf.add_owner(session_, owner_id)
    owner_id = '3'
    dbf.add_owner(session_, owner_id)
    owner_id = '4'
    dbf.add_owner(session_, owner_id)

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
    dbf.add_favorite(session_, vk_user_dict, owner_id)

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
    dbf.add_favorite(session_, vk_user_dict, owner_id)

    vk_user_dict = {
        "vk_id": "a123",
        "first_name": "Test_2",
        "last_name": "User_2",
        "city": "Toronto",
        "sex": False,
        "birth_date": "30.06.1979",
        "url": "https://vk.com/a123",
        "images": [["image1_2.jpg", 12], ["image2_2.jpg", 11], ["image3_3.jpg", 55]],
    }
    dbf.add_favorite(session_, vk_user_dict, owner_id)

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
    dbf.add_favorite(session_, vk_user_dict, owner_id)

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
    dbf.add_favorite(session_, vk_user_dict, owner_id)
