import pandas as pd 
import numpy as np
from src.data.data_ingestion import data_ingestion
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def data_validation(data:pd.DataFrame):
    try:
      customer_data = data.copy()
      duplicates = customer_data.duplicated().sum()
      logging.info(f"the total number of duplicate is {duplicates}")
      dupplicate_transaction = customer_data["TransactionID"].duplicated().sum()
      logging.info(f"the total number of duplicate transactions is {dupplicate_transaction}")

      unique_customers = customer_data["CustomerID"].nunique()
      logging.info(f"the total number of unique values is {unique_customers}")

      gender_distribution = customer_data["CustGender"].value_counts()
      logging.info(f"the distribution of gender is {gender_distribution}")
      
      missing_values = customer_data.isnull().sum()
      logging.info(f"the total number of missing values is {missing_values}")
      
      customer_data = customer_data.dropna()
      logging.info(f"missing values successfully dropped if there is any.")
      
      customer_data["TransactionDate"] = pd.to_datetime(customer_data["TransactionDate"], errors="coerce")
      logging.info(f"transaction date has been successfully validated and the transaction data has been handled")
      logging.info(f"the dataset info after validation is {customer_data.info()}") 
      return customer_data
     
    except Exception as e:
        logging.error(f"error occurred during data validation {e}")

customer_data = data_ingestion()
data_validation(customer_data)  