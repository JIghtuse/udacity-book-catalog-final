from secrets import DB_SECRET
DATABASE_PATH = "postgresql://catalog:{}@localhost/catalog".format(DB_SECRET)
