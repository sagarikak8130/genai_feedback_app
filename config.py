import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

# Validate required environment variables
if not all([OPENAI_API_KEY, MONGO_URI, DB_NAME, COLLECTION_NAME]):
    raise ValueError("Missing required environment variables. Please check your .env file.")
