import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Settings:
    # Default DB URI for PostgreSQL
    DATABASE_URL: str = os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:password@localhost:5432/manager_core"
    )


settings = Settings()
