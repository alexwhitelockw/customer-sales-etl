import pandas as pd


from src.utils.utils import (
    check_for_duplicates,
    check_for_missing_values
)


if __name__ == "__main__":
    region_details = pd.read_csv("data/source/region_details.csv")

    region_details = region_details.drop(columns="index")

    region_details.columns = region_details.columns.str.lower()

    # Check whether missing values are present in the data
    missing_values = check_for_missing_values(region_details)

    # Following the validation of Shipping details, Austria and Mongolia
    # are associated with the incorrect region. Updating here.

    region_details.loc[(region_details["country"] == "Austria") & (region_details["market"] == "EMEA"), "region"] = "Central"
    region_details.loc[(region_details["country"] == "Austria") & (region_details["market"] == "EMEA"), "market"] = "EU"

    region_details.loc[(region_details["country"] == "Mongolia") & (region_details["market"] == "EMEA"), "region"] = "North Asia"
    region_details.loc[(region_details["country"] == "Mongolia") & (region_details["market"] == "EMEA"), "region"] = "APAC"

    region_duplicates = region_details.loc[region_details[["state", "country", "market", "region"]].duplicated(), "region_id"]

    region_details = region_details.loc[~region_details["region_id"].isin(region_duplicates)]

    # Flag whether there are missing values present in the region records
    if any(missing_value > 0 for missing_value in missing_values):
        print("There are missing values in the dataset")

    # Check for duplicates and print if any are present
    region_details = check_for_duplicates(region_details)

    region_details.to_csv("data/transformed/region_details.csv", index=False)
