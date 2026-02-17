from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Wordle"
    url_words: str = 'https://www.ime.usp.br/~pf/dicios/br-utf8.txt'
    data_dir: str = 'data/'
    words_filename: str = 'words.txt'

    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()
