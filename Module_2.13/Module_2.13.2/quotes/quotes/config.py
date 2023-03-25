from pydantic import BaseSettings


class Settings(BaseSettings):
    engine: str
    name: str
    user: str
    password: str
    host: str
    port: str

    email_backend: str
    email_host: str
    email_port: str
    email_starttls: bool
    email_use_ssl: bool
    email_use_tls: bool
    email_host_user: str
    email_host_password: str
    default_from_email: str

    secret_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
