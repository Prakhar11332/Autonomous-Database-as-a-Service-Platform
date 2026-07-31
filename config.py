"""
Central config object. Every engine reads settings from here instead of
calling os.environ directly, so there's one place to see every knob the
platform has.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Control plane DB (stores metadata ABOUT tenant databases, not the
    # tenant data itself)
    control_plane_db_url: str = (
        "postgresql+asyncpg://dbaas_admin:change_me_in_env@localhost:5432/dbaas_control_plane"
    )

    redis_url: str = "redis://localhost:6379/0"

    jwt_secret_key: str = "replace_with_a_long_random_string"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    docker_host: str = "unix:///var/run/docker.sock"

    tenant_port_range_start: int = 15000
    tenant_port_range_end: int = 16000
    default_tenant_memory_limit: str = "512m"
    default_tenant_cpu_limit: float = 0.5

    backup_storage_path: str = "./backups"
    backup_retention_count: int = 5

    prometheus_url: str = "http://localhost:9090"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
