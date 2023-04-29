import db_function as dbf

my_pynder = dbf.PYnder_DB(rebuild=True)

print(my_pynder.get_favorite("owner_1"))
my_pynder.delete_favorite("user_1", "owner_1")
print(my_pynder.get_favorite("owner_1"))
my_pynder.add_favorite(
    {
        "vk_id": "user_44",
        "first_name": "Test_44",
        "last_name": "User_44",
        "city": "Washington",
        "sex": 2,
        "birth_date": "30.06.1979",
        "url": "https://vk.com/222",
        "images": [
            {"url": "image51.jpg", "likes": 12},
            {"url": "image52.jpg", "likes": 12},
            {"url": "image53.jpg", "likes": 12},
        ],
    },
    "owner_1",
)
print(my_pynder.get_favorite("owner_1"))
