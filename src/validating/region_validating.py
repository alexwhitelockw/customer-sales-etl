import pandas as pd

from src.utils.utils import validate_numeric_columns


if __name__ == "__main__":
    region_details = pd.read_csv("data/transformed/region_details.csv")

    # Check if Region ID is Numeric
    validate_numeric_columns(region_details, "region_id")

    region_details.to_csv("data/validated/region_details.csv", index=False)
