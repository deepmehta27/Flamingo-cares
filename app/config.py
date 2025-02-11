import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# AWS Credentials - Use environment variables for security
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")  # Optional if using temporary credentials
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")  # Optional if using a different region

## OPENAI CREDENTIALS
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL =  os.getenv("OPENAI_BASE_URL")