import pandas as pd

from src.utils.utils import (
    validate_customer_id,
    validate_numeric_columns,
    validate_date_columns
)


if __name__ == "__main__":
    shipping_details = pd.read_csv("data/transformed/shipping_details.csv")

    # Check Shipping ID is Numeric
    validate_numeric_columns(shipping_details, "shipping_id")

    # Check Customer ID is standardised
    validate_customer_id(shipping_details, "customer_id")

    # Check Postal Code is Numeric
    validate_numeric_columns(shipping_details, "postal_code")

    # Check Date columns to ensure they are in the correct format

    shipping_details.loc[:, "effective_start"] = pd.to_datetime(shipping_details["effective_start"])
    shipping_details.loc[:, "effective_end"] = pd.to_datetime(shipping_details["effective_end"])

    validate_date_columns(shipping_details, "effective_start")
    validate_date_columns(shipping_details, "effective_end")

    # Check Region ID is Numeric
    validate_numeric_columns(shipping_details, "region_id")

    # Check Duplicated Shipping ID flag
    duplicated_shipping_id = shipping_details.loc[shipping_details["is_duplicated_shipping_id"] == 1]

    duplicated_shipping_id.loc[:, "region_id_count"] = duplicated_shipping_id.groupby(["shipping_id"])["region_id"].transform("nunique")

    multiple_region_ids = duplicated_shipping_id.loc[duplicated_shipping_id["region_id_count"] == 2, "shipping_id"]  # There appears to be a problem
    # with region IDs as certain countries are found in multiple regions
    single_region_id = duplicated_shipping_id.loc[duplicated_shipping_id["region_id_count"] == 1, "shipping_id"]  # There is a single instance where
    # a street address is attributed to multiple countries -- Analamanga is assigned to Morocco, Brazil, Denmark, but is found in Madagascar

    # For the incorrect country assignment (Madagascar), the rows with missing Region ID will be dropped, which
    # will correct the wrong country assignment, but two rows will still be present due to the city column.

    shipping_details = shipping_details.loc[shipping_details["region_id"].notna()]

    # Add description for duplication
    shipping_details.loc[shipping_details["shipping_id"].isin(single_region_id), "duplicate_reason"] = "Shipping Associated with Two Cities"
    shipping_details.loc[shipping_details["shipping_id"].isin(multiple_region_ids), "duplicate_reason"] = "Shipping Associated with Two Regions"

    # Flag Missing Address
    shipping_details.loc[shipping_details["street_address"].isna(), "is_missing_address"] = 1

    shipping_details.to_csv("data/validated/shipping_details.csv", index=False)
