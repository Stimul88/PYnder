import db_function as dbf

my_pynder = dbf.PYnder_DB(rebuild=True)

# my_pynder.delete_favorite("222", "4")
# print(my_pynder.is_in_favorite("user_2", "owner_3"))

print(my_pynder.get_favorite('owner_1'))
