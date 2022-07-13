class Config():
    SECRET_KEY = 'FJedj@jwd!'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_DATABASE_HOST ='localhost'
    MYSQL_DATABASE_USER ='root'
    MYSQL_DATABASE_PASSWORD ='root'
    MYSQL_DATABASE_DB ='madretierra'
    


config = {
    'development': DevelopmentConfig
}