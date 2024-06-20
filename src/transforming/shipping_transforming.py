import pandas as pd


from src.utils.utils import (
    check_for_duplicates,
    check_for_missing_values,
    standardise_customer_id,
    standardise_date_format
)


def identify_slash_in_post_code(dataframe: pd.DataFrame) -> pd.Series:
    """Check dataframe rows for postal codes that contain a date"""
    return dataframe["postal_code"].str.contains(r"/", regex=True, na=False)


if __name__ == "__main__":
    shipping_details = pd.read_csv("data/source/shipping_details.csv")

    shipping_details = shipping_details.loc[shipping_details["id"].notna()]

    shipping_details = shipping_details.rename(
        columns={
            "id": "shipping_id",
            "customerid": "customer_id",
            "effstart": "effective_start",
            "effend": "effective_end",
            "streetadd": "street_address"
        }
    )

    # Fix Customer ID Column --------------------

    # Subset data to identify customer IDs that do not follow the standard conversion (AB-123)
    incorrect_customer_id = (
        shipping_details.loc[shipping_details["customer_id"].str.contains("[A-Z]{2}-[0-9]+(?=[A-Z])+", regex=True)]
    )

    # Split customer ID into customer ID and city based on whether letters are found after the numbers
    incorrect_customer_id.loc[:, "customer_id"] = incorrect_customer_id["customer_id"].str.split(r"[0-9](?=[A-Z])", regex=True)

    # Boolean logic to idenitfy whether postal code contains letters
    post_code_address = incorrect_customer_id["postal_code"].str.contains(r"[A-Za-z]", regex=True, na=False)

    # Update street address with postal code where postal code contains letters
    incorrect_customer_id.loc[post_code_address, "street_address"] = incorrect_customer_id.loc[:, "postal_code"]
    incorrect_customer_id.loc[post_code_address, "postal_code"] = pd.NA

    # Shift values in columns by 1 place to align values
    incorrect_customer_id.loc[:, ["city", "state", "country", "postal_code", "effective_start"]] = (
        incorrect_customer_id[["city", "state", "country", "postal_code", "effective_start"]]
        .shift(axis=1)
    )

    # Identify rows where a date is contained in the postal code (presence of slash)
    slash_in_postal_code = identify_slash_in_post_code(incorrect_customer_id)

    # For rows with slash in postal code, shift column subset by 1
    incorrect_customer_id.loc[slash_in_postal_code, ["postal_code", "effective_start", "effective_end"]] = (
            incorrect_customer_id.loc[slash_in_postal_code, ["postal_code", "effective_start", "effective_end"]]
            .shift(axis=1)
        )

    # Assign split customer ID and city to respective columns
    incorrect_customer_id.loc[:, "city"] = incorrect_customer_id["customer_id"].apply(lambda x: x[1])
    incorrect_customer_id.loc[:, "customer_id"] = incorrect_customer_id["customer_id"].apply(lambda x: x[0])

    # Replace Data in main table with corrected customer ID data

    shipping_details = shipping_details.drop(index=incorrect_customer_id.index)

    shipping_details = pd.concat([
        shipping_details, incorrect_customer_id
    ])

    # Fix Remaining Data ------------------------

    # There is an instance of an address being split across the two date (start and end) columns
    # This identifies the row and joins the strings together
    suite_end_date = shipping_details["effective_end"].str.startswith("Suite", na=False)

    shipping_details.loc[:, "street_address"] = (
        shipping_details
        .loc[suite_end_date]
        .apply(lambda x: " ".join([x["effective_start"], x["effective_end"]]), axis=1)
    )

    shipping_details.loc[suite_end_date, "effective_end"] = pd.NA  # Replace suite with NA

    # Identify rows where postal code and effective start have dates, but effective end has an address
    rows_with_slash_and_letter = (
        (shipping_details["postal_code"].str.contains(r"/", regex=True, na=False)) &
        (shipping_details["effective_start"].str.contains(r"/", regex=True, na=False)) &
        (shipping_details["effective_end"].str.contains(r"[A-Z]", regex=True, na=False))
    )

    # Shift details along one column to align with correct headings
    shipping_details.loc[rows_with_slash_and_letter, ["postal_code", "effective_start", "effective_end", "street_address"]] = (
        shipping_details.loc[
            rows_with_slash_and_letter,
            ["postal_code", "effective_start", "effective_end", "street_address"]].shift(axis=1)
    )

    # Identify rows without a date in postal code, but a date in effective start and address in effective end
    rows_without_slash_and_with_letter = (
        (shipping_details["postal_code"].str.contains(r"[0-9](?!/)", regex=True, na=False)) &
        (shipping_details["effective_start"].str.contains(r"/", regex=True, na=False)) &
        (shipping_details["effective_end"].str.contains(r"[A-Z]", regex=True, na=False))
    )

    # Shift address from effective end column into street address column
    shipping_details.loc[rows_without_slash_and_with_letter, "street_address"] = (
        shipping_details.loc[
            rows_without_slash_and_with_letter,
            "effective_end"]
    )

    # Replace any address with NA in the effective end column
    shipping_details.loc[rows_without_slash_and_with_letter, "effective_end"] = pd.NA

    # Identify rows with a slash in postal code and address in effective start
    rows_with_slash_and_with_letter = (
        (shipping_details["postal_code"].str.contains(r"/", regex=True, na=False)) &
        (shipping_details["effective_start"].str.contains(r"[A-Z]", regex=True, na=False))
    )

    # Shift address from effective start column into street address column
    shipping_details.loc[rows_with_slash_and_with_letter, "street_address"] = (
        shipping_details.loc[
            rows_with_slash_and_with_letter,
            "effective_start"]
    )

    # Shift date in postal code to effective start column
    shipping_details.loc[rows_with_slash_and_with_letter, "effective_start"] = (
        shipping_details.loc[
            rows_with_slash_and_with_letter,
            "postal_code"]
    )

    # Replace any dates in postal code with NA
    shipping_details.loc[rows_with_slash_and_with_letter, "postal_code"] = pd.NA

    # Identify dates in postal code column
    slash_in_postal_code = identify_slash_in_post_code(shipping_details)

    # Shift columns to the right for rows where postal code still contains a date
    shipping_details.loc[slash_in_postal_code, ["postal_code", "effective_start", "effective_end"]] = (
        shipping_details.loc[slash_in_postal_code, ["postal_code", "effective_start", "effective_end"]]
        .shift(axis=1)
    )

    # Standardise Customer ID to algin with other Tables
    shipping_details = standardise_customer_id(shipping_details)

    # Convert Shipping ID to an Int
    shipping_details["shipping_id"] = shipping_details["shipping_id"].astype("int")

    # Clean text and date columns
    shipping_details["effective_start"] = shipping_details["effective_start"].str.replace(r"[\"\']+", "", regex=True)  # Remove punctuation from anywhere
    shipping_details["effective_end"] = shipping_details["effective_end"].str.replace(r"[\"\']+", "", regex=True)

    shipping_details["city"] = shipping_details["city"].str.replace(r"^[\"]+", "", regex=True)  # Remove punctuation from start only
    shipping_details["state"] = shipping_details["state"].str.replace(r"^[\"]+", "", regex=True)
    shipping_details["country"] = shipping_details["country"].str.replace(r"^[\"]+", "", regex=True)

    # Remaining address in Postal Code column
    address_in_postal_code = shipping_details["postal_code"].str.contains(r"[A-Za-z]", regex=True, na=False)

    shipping_details.loc[address_in_postal_code, "street_address"] = shipping_details.loc[address_in_postal_code, "postal_code"]
    shipping_details.loc[address_in_postal_code, "postal_code"] = pd.NA

    # Convert date columns to actual date object
    shipping_details = standardise_date_format(shipping_details, "effective_start")
    shipping_details = standardise_date_format(shipping_details, "effective_end")

    # Replace missing values with NA
    shipping_details.loc[shipping_details["postal_code"].isna(), "postal_code"] = pd.NA

    # Update Country Details
    # A small subset of countries are referenced more than once due to acronym use.
    # To ensure alignment with shipping, they are changed here.
    shipping_details.loc[shipping_details["country"].isin(["US", "USA", "United States of America"]), "country"] = "United States"
    shipping_details.loc[shipping_details["country"].isin(["UK"]), "country"] = "United Kingdom"
    shipping_details.loc[shipping_details["country"].isin(["NZ"]), "country"] = "New Zealand"

    # Check and remove duplicates
    shipping_details = check_for_duplicates(shipping_details)

    # Check whether missing values are present in the data
    missing_values = check_for_missing_values(shipping_details)

    # Flag whether there are missing values present in the shipping records
    if any(missing_value > 0 for missing_value in missing_values):
        print("There are missing values in the dataset")
        print(missing_values)

    # Add Region Code
    region_details = pd.read_csv("data/transformed/region_details.csv")

    region_details = region_details[["state", "country", "region_id"]]

    shipping_details = shipping_details.merge(region_details, how="left", on=["state", "country"], validate="many_to_many")

    # Merging Region Details causes a problem of duplicated rows.
    # In one instance "Lopez Island" is associated with six different countries
    duplicated_shipping_id = shipping_details.loc[shipping_details["shipping_id"].duplicated(), "shipping_id"]

    # Flag rows where shipping ID is duplicated
    shipping_details.loc[shipping_details["shipping_id"].isin(duplicated_shipping_id), "is_duplicated_shipping_id"] = 1

    shipping_details.to_csv("data/transformed/shipping_details.csv", index=False)
