import pandas as pd

from src.utils.utils import validate_customer_id


if __name__ == "__main__":
    customer_details = pd.read_csv("data/transformed/customer_details.csv")

    # Check customer ID format to ensure it aligns with the standard
    validate_customer_id(customer_details, "customer_id")

    customer_details.to_csv("data/validated/customer_details.csv", index=False)
