import os
from dotenv import load_dotenv

load_dotenv(override=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DATABASE = "Apex_trust_customer_transactions"   
MONGO_COLLECTION = "Apex_Customer"
