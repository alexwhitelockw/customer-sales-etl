import pandas as pd

from src.utils.utils import (
    check_for_duplicates,
    check_for_missing_values,
    one_hot_encode
)


if __name__ == "__main__":
    product_details = pd.read_csv("data/source/product_details.csv")

    product_details.columns = [
        column_name.replace("-", "_").lower()
        for column_name in product_details.columns
    ]

    product_details = one_hot_encode(product_details, "category")
    product_details = one_hot_encode(product_details, "sub_category")

    # Check whether missing values are present in the data
    missing_values = check_for_missing_values(product_details)

    # Flag whether there are missing values present in the product records
    if any(missing_value > 0 for missing_value in missing_values):
        print("There are missing values in the dataset")

    # Check for duplicates and print if any are present
    product_details = check_for_duplicates(product_details)

    product_details.to_csv("data/transformed/product_details.csv", index=False)
