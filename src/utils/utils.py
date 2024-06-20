from datetime import date
import numpy as np
import pandas as pd
import re


def check_for_missing_values(dataframe: pd.DataFrame) -> np.array:
    """Check for missing values in the dataframe and return an array containing the count of missing values."""
    missing_values = dataframe.isna().sum().values

    return missing_values


def check_for_duplicates(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Check for duplicate rows in the dataframe, print and return a dataframe with these removed."""
    duplicated_rows = (
        dataframe
        .loc[dataframe.duplicated()]
    )

    if not duplicated_rows.empty:
        print("Duplicates present in data.")
        print(duplicated_rows)

    # Remove duplicated rows
    dataframe = dataframe.drop_duplicates()
    print("Duplicates Removed, if present.")

    return dataframe


def one_hot_encode(dataframe: pd.DataFrame, column: str) -> pd.DataFrame:
    """Create one-hot encoded columns based on the provided categorical variable contained in the dataframe."""
    one_hot = pd.get_dummies(dataframe[column], prefix=column, prefix_sep="_")
    dataframe = dataframe.drop(column, axis=1)
    dataframe = dataframe.join(one_hot)

    return dataframe


def standardise_customer_id(dataframe: pd.DataFrame) -> pd.DataFrame:
    """"""
    for index, value in dataframe["customer_id"].items():
        id_length = len(value)
        while id_length < 18:
            value += "0"
            id_length = len(value)

        dataframe.at[index, "customer_id"] = value

    return dataframe


def standardise_date_format(dataframe: pd.DataFrame, column: str) -> pd.DataFrame:
    """"""
    dataframe[column] = pd.to_datetime(dataframe[column], format="%d/%m/%Y")

    return dataframe


def validate_customer_id(dataframe: pd.DataFrame, column: str) -> None:
    """Perform check to ensure customer ID is in the correct format"""
    for customer_id in dataframe[column]:
        if re.match(r"^[A-Za-z]{2}(?=-)", customer_id) is None or re.search(r"[0-9]{15}$", customer_id) is None:
            raise ValueError("Customer ID does not start with two letters or does not end with 15 trailing numerical characters.")


def validate_date_columns(dataframe: pd.DataFrame, column: str) -> None:
    """Perform check to ensure date column is in the correct format"""
    for date_value in dataframe[column]:
        if not isinstance(date_value, date) and date_value is not pd.NA:
            raise ValueError(f"{column} column is not of Date Type.")


def validate_numeric_columns(dataframe: pd.DataFrame, column: str) -> None:
    """Perform check to ensure numeric column is in the correct format"""
    for value in dataframe[column]:
        if not isinstance(value, (int, float)) and value is not pd.NA:
            raise ValueError(f"{column} is not numeric.")


def validate_product_id(dataframe: pd.DataFrame, column: str) -> None:
        """Perform check to ensure Product ID meets required format"""
        for product_id in dataframe[column]:
            if re.match(r"^[A-Z]{3}/[A-Z]{3}-[0-9]{6}", product_id) is None:
                raise ValueError("Product ID does not align with format")
