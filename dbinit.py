from blog_app.DBManager import DBManager

manager = DBManager()
manager.init_db()
manager.close()