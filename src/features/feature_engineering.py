import pandas as pd
import numpy as np
from datetime import datetime
from src.data.data_ingestion import data_ingestion
from src.data.data_validation import data_validation
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class feature_eng:
    def calculate_rfm_metrics(data: pd.DataFrame):
        try:
            reference_date = data['TransactionDate'].max() + pd.Timedelta(days=1)
            print(f"Reference date for Recency calculation: {reference_date.date()}")

            # Calculate RFM metrics for each customer
            rfm_data = data.groupby('CustomerID').agg({
                'TransactionDate': lambda x: (reference_date - x.max()).days,   # Recency
                'TransactionID': 'count',                                       # Frequency
                'TransactionAmount': 'sum'                                      # Monetary
            }).reset_index()
            rfm_data.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
            logging.info(f"the RFM data has been successfully created:\n {rfm_data.head()}")

            customer_demographics = data.groupby('CustomerID').agg({
                'CustomerDOB': 'first',
                'CustGender': 'first',
                'CustLocation': 'first',
                'CustAccountBalance': 'last',
            }).reset_index()
            logging.info(f"the customer demographics data has been successfully created:\n {customer_demographics.head()}")

            rfm_data = rfm_data.merge(customer_demographics, on='CustomerID', how='left')
            logging.info(f"the merged RFM_data has been successfully created:\n {rfm_data.head()}")
            return rfm_data
        except Exception as e:
            logging.error(f"error occurred while calculating and creating the RFM metrics & Data {e}")

    def calculating_rfm_scores(data: pd.DataFrame):
        try:
            # Create RFM scores (1-5 scale)
            # Recency: lower recency = better (more recent)
            data['R_Score'] = pd.qcut(data['Recency'], q=5, labels=[5, 4, 3, 2, 1])

            # Frequency: higher frequency = better
            data['F_Score'] = pd.qcut(data['Frequency'], q=5, labels=[1, 2, 3, 4, 5])

            # Monetary: higher monetary = better
            data['M_Score'] = pd.qcut(data['Monetary'], q=5, labels=[1, 2, 3, 4, 5])
            data['R_Score', 'F_Score', 'M_Score'] = data[['R_Score', 'F_Score', 'M_Score']].astype(int)
            data['RFM_Score'] = data['R_Score'] + data['F_Score'] + data['M_Score']
            logging.info("Rfm scores has been successfully calculated...")
            logging.info(f"{data.head()}")
            return data
        except Exception as e:
            logging.error(f"error occurred while calculating the RFM scores... {e}")

customer_data = data_ingestion()
customer_data =data_validation(customer_data)
feature_engineering = feature_eng
customer_data =feature_engineering.calculate_rfm_metrics(customer_data)
customer_data =feature_engineering.calculating_rfm_scores(customer_data)


