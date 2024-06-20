import pandas as pd
import re

from src.utils.utils import (
    validate_customer_id,
    validate_date_columns,
    validate_numeric_columns,
    validate_product_id
)


if __name__ == "__main__":
    invoice_details = pd.read_csv("data/transformed/invoice_details.csv")

    # Check order ID format to ensure it aligns with standard
    for order_id in invoice_details["order_id"]:
        if re.match(r"^[A-Z]{2}", order_id) is None:
            raise ValueError("Order ID does not start with two letters.")

    # Check if line number is above 0
    if invoice_details["line_no"].min() < 1:
        raise ValueError("Line number less than lower bound of 1.")

    # Check if date columns are in the correct format

    invoice_details["order_date"] = pd.to_datetime(invoice_details["order_date"])
    invoice_details["ship_date"] = pd.to_datetime(invoice_details["ship_date"])

    validate_date_columns(invoice_details, "order_date")
    validate_date_columns(invoice_details, "ship_date")

    # Check customer ID format to ensure it aligns with standard
    validate_customer_id(invoice_details, "customer_id")

    # Check product ID format to ensure it aligns with standard
    validate_product_id(invoice_details, "product_id")

    # Check if sale value is numeric
    validate_numeric_columns(invoice_details, "sale_value")

    # Check quantity value to ensure above 0
    if invoice_details["quantity"].min() < 1:
        raise ValueError("Quantity exceeds lower bound.")

    # Check if profit and shipping cost columns are numeric
    validate_numeric_columns(invoice_details, "profit")
    validate_numeric_columns(invoice_details, "shipping_cost")

    # Check if the discount falls within the upper and lower bound
    if invoice_details["discount"].min() < 0 or invoice_details["discount"].max() > 1:
        raise ValueError("Discount exceeds lower or upper bounds.")

    invoice_details.to_csv("data/validated/invoice_details.csv", index=False)
