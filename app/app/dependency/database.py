from databases import Database
from . import config_settings as config

def generateURL(username: str, password: str, host: str, database: str, ssl_mode:str, min_size: str, max_size: str):
    return 'postgres://' + username + ":" + password + "@" + host + "/" + database + "?sslmode=" + ssl_mode + "&min_size=" + min_size +"&max_size=" + max_size

def connectDatabase():
    env_config = config.Settings()
    username = env_config.fastservice_postgres_user
    password = env_config.fastservice_postgres_passwd
    host = env_config.fastservice_postgres_host
    database = env_config.fastservice_postgres_db
    ssl_mode = env_config.fastservice_postgres_ssl_mode
    min_size = env_config.fastservice_postgres_min_size
    max_size = env_config.fastservice_postgres_max_size
    url = generateURL(username, password, host, database, ssl_mode, min_size, max_size)
    return Database(url)

db = connectDatabase()