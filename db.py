import db_function as dbf

my_pynder = dbf.PYnder_DB(rebuild=True)


# print(my_pynder.is_in_favorite("user_2", "owner_3"))

print(my_pynder.get_favorite('owner_1'))
my_pynder.delete_favorite('user_1', 'owner_1')
print(my_pynder.get_favorite('owner_1'))
