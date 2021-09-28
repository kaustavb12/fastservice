from pydantic import BaseSettings

class Settings(BaseSettings):
    service_name: str
    service_description: str

    fastservice_postgres_user: str
    fastservice_postgres_passwd: str
    fastservice_postgres_host: str
    fastservice_postgres_db: str
    fastservice_postgres_ssl_mode: str = "disable"
    fastservice_postgres_min_size: str = "1"
    fastservice_postgres_max_size: str = "2"
    
    # AUTH0 related configs
    auth0_domain: str
    api_identifier: str
    algorithms: str
    m2m_user: str
    api_client_id: str
    api_client_secret: str
    
    logging_level: str
    log_type: str = "STDOUT"

    origins: str

    class Config:
        env_file = '/env_config'
        env_file_encoding = 'utf-8'
        secrets_dir = '/run/secrets'