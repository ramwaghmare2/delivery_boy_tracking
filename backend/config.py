import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/delivery_boy_tracking'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    KAFKA_SERVER = 'delivery_boy_kafka:9094'
