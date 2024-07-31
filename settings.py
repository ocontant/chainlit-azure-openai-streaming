import os
from pydantic_settings import BaseSettings, SettingsConfigDict
import dotenv


env_path = ".env"
# Validate file access
if not os.path.exists(env_path):
    print(f"Error: {env_path} file not found.")
    raise FileNotFoundError
dotenv.load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: str
    AZURE_OPENAI_CHAT_MODEL_NAME: str
    AZURE_OPENAI_CHAT_DEPLOYMENT_VERSION: str
    LOCATION: str
    UNIT: str

    model_config = SettingsConfigDict(
        env_file=str(env_path),
        env_prefix="",
        case_sensitive=True,
    )


if __name__ == "__main__":
    settings = Settings()

    if not os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"):
        print("Error: Environment variables not loaded correctly.")
    else:
        print("Environment variables loaded with os.getenv")
        print(
            "os.getenv.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: ",
            os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        )
        print("")

        try:
            settings = Settings()

            print("Environment variables loaded using Pydantic Settings:")
            print(
                f"AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: {settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME}"
            )
        except Exception as e:
            print("Error loading settings using Pydantic:", e)
