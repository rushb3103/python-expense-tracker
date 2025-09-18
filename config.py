import os

class Config:
    SECRET_KEY = "fgh/35t#%2grt"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://expensetracker_policeman:e2ff141ef5f5771ddda38f3fd762709e9334e510@q0rsi6.h.filess.io:3307/expensetracker_policeman"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://rushnb10_rushit:Rushit@2002@localhost/rushnb10_expensedb"
    # SQLALCHEMY_DATABASE_URI = "sqlite:///expenses.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024   # 5 MB
    
    
    
