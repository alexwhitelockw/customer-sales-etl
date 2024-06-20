import pandas as pd
import re


from src.utils.utils import (
    check_for_duplicates,
    check_for_missing_values,
    one_hot_encode,
    standardise_customer_id
)


def update_column_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Rename columns in the dataframe to more descriptive names."""
    dataframe = (
        dataframe
        .rename(
            columns={
                "cusid": "customer_id",
                "cusnm": "customer_name",
                "sgmnt": "customer_segment"
            }
        )
    )

    return dataframe


def clean_customer_id(dataframe: pd.DataFrame) -> pd.DataFrame:
    """"""
    try:
        dataframe["customer_id"] = (
            dataframe["customer_id"]
            .apply(lambda x: re.search(r"\w{2}-[0-9]+", x).group(0))
        )

        return dataframe

    except KeyError as e:
        print(f"Column not present: {e}")


if __name__ == "__main__":

    # Read Customer Details data
    customer_details = pd.read_csv("data/source/customer_details.csv")

    # Change column names for Customer Details
    customer_details = update_column_names(customer_details)

    # Check whether missing values are present in the data
    missing_values = check_for_missing_values(customer_details)

    # Flag whether there are missing values present in the customer records
    if any(missing_value > 0 for missing_value in missing_values):
        print("There are missing values in the dataset")

    # Check for duplicates and print if any are present
    customer_details = check_for_duplicates(customer_details)

    # Convert categorical variable to one-hot encoding representation
    customer_details = one_hot_encode(customer_details, "customer_segment")

    # Remove initial 3 values from customer ID and standardise ID for future joining
    customer_details = clean_customer_id(customer_details)
    customer_details = standardise_customer_id(customer_details)

    customer_details.to_csv("data/transformed/customer_details.csv", index=False)
