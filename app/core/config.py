from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "YT Stream API"
    VERSION: str = "1.0.0"

    ALLOWED_HOSTS: list[str] = [
        "youtube.com",
        "youtu.be",
        "music.youtube.com",
    ]

    ALLOWED_ORIGINS: list[str] = ["*"]

    YDL_FORMAT: str = "bestaudio"
    YDL_QUIET: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()