import pandas as pd

from src.utils.utils import (
    check_for_duplicates,
    check_for_missing_values,
    one_hot_encode,
    standardise_customer_id,
    standardise_date_format
)


def round_float_values(dataframe: pd.DataFrame, column: str) -> pd.DataFrame:
    """"""
    dataframe[column] = dataframe[column].round(2)

    return dataframe


if __name__ == "__main__":
    invoice_details = pd.read_csv("data/source/invoice_details.csv")

    # Column names are using snake case, but are in title format so transform to lower
    invoice_details.columns = invoice_details.columns.str.lower()

    # Transform date columns to ensure standardised format
    invoice_details = standardise_date_format(invoice_details, "order_date")
    invoice_details = standardise_date_format(invoice_details, "ship_date")

    # Convert Categorical variables to one-hot encoding
    invoice_details = one_hot_encode(invoice_details, "ship_mode")
    invoice_details = one_hot_encode(invoice_details, "order_priority")

    # Round Sale values to 2 digits to ensure consistency
    invoice_details = round_float_values(invoice_details, "sale_value")
    invoice_details = round_float_values(invoice_details, "profit")
    invoice_details = round_float_values(invoice_details, "shipping_cost")

    # Standardise customer ID

    invoice_details = standardise_customer_id(invoice_details)

    # Check whether missing values are present in the data
    missing_values = check_for_missing_values(invoice_details)

    # Flag whether there are missing values present in the invoice records
    if any(missing_value > 0 for missing_value in missing_values):
        print("There are missing values in the dataset")

    # Check for duplicates and print if any are present
    invoice_details = check_for_duplicates(invoice_details)

    invoice_details.to_csv("data/transformed/invoice_details.csv", index=False)
