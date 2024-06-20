import pandas as pd

from src.utils.utils import validate_product_id


if __name__ == "__main__":
    product_details = pd.read_csv("data/transformed/product_details.csv")

    # Check if Product ID aligns with standard format
    validate_product_id(product_details, "product_id")

    product_details.to_csv("data/validated/product_details.csv", index=False)
