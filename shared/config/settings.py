# shared/config/settings.py

from dotenv import load_dotenv
import os

# Load .env file automatically when imported
load_dotenv()

class Settings:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # Redis & Vector DB
    REDIS_URL = os.getenv("REDIS_URL")
    VECTOR_DB_URL = os.getenv("WEAVIATE_URL")

    # Auth
    INTERNAL_SERVICE_TOKEN = os.getenv("INTERNAL_SERVICE_TOKEN")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

    # Blockchain
    BLOCKCHAIN_RPC_URL = os.getenv("BLOCKCHAIN_RPC_URL")
    BLOCKCHAIN_PRIVATE_KEY = os.getenv("BLOCKCHAIN_PRIVATE_KEY")

settings = Settings()
