import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://robot:robotpass@db:3306/robotdb'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
