from bs4 import BeautifulSoup
import pandas as pd
import re


def convert_txt_to_csv(filepath: str) -> pd.DataFrame:
    """Convert a tab-delimited text file to a CSV (pandas DataFrame).

    Parameters:
    filepath -- Filepath to txt data file

    Returns:
    A Pandas DataFrame containing the data from the text file.
    """
    try:

        with open(filepath, "r") as f:
            data = f.readlines()

        # Clean and split data
        data = [re.split(r"\t|\n", line.strip()) for line in data]

        # Extract column names and build dataframe
        column_names = data.pop(0)

        if len(column_names) < len(data[0]):
            column_names.insert(0, "index")

        data = pd.DataFrame(data=data, columns=column_names)

        return data

    except FileNotFoundError as e:
        print(f"File Not Found: {e}")
    except ValueError as e:
        print(f"Data could not be converted to CSV: {e}")


def convert_xml_to_csv(filepath: str) -> pd.DataFrame:
    """Convert XML file to a CSV (pandas DataFrame).

    Parameters:
    filepath -- Filepath to xml data file

    Returns:
    A Pandas DataFrame containing the data from the xml file.
    """

    try:

        with open(filepath) as f:
            data = BeautifulSoup(f.read(), "xml")

        # Locate all row instances within XML
        rows = [row for row in data.find_all("row")]

        # Initialise empty list for full data
        full_data = []

        # Iterate over each row, extracting column name and value
        for row in rows:
            row_data = {}
            for child in row.children:
                data_value = child.get_text().strip()
                if data_value:
                    row_data.update(
                        {child.name: data_value}
                    )
            full_data.append(row_data)

        full_data = pd.DataFrame(full_data)

        return full_data

    except FileNotFoundError as e:
        print(f"File Not Found: {e}")
    except ValueError as e:
        print(f"Data could not be converted to CSV: {e}")


def convert_json_to_csv(filepath: str) -> pd.DataFrame:
    """Convert JSON file to a CSV (pandas DataFrame).

    Parameters:
    filepath -- Filepath to JSON data file

    Returns:
    A Pandas DataFrame containing the data from the JSON file.
    """

    try:
        data = pd.read_json(filepath)

        return data

    except FileNotFoundError as e:
        print(f"File Not Found: {e}")
    except ValueError as e:
        print(f"Data could not be converted to CSV: {e}")


def convert_xlsx_to_csv(filepath: str) -> pd.DataFrame:
    """Convert XLSX file to a CSV (pandas DataFrame).

    Parameters:
    filepath -- Filepath to XLSX data file

    Returns:
    A Pandas DataFrame containing the data from the XLSX file.
    """

    try:

        excel_book = pd.ExcelFile(filepath)

        if len(excel_book.sheet_names) > 1:
            print("There is more than one sheet contained in the Excel file.")

        full_data = pd.DataFrame()

        # Iterate over sheets in Excel Book and concat into DataFrame
        for sheet in excel_book.sheet_names:
            data = excel_book.parse(sheet_name=sheet)
            full_data = pd.concat([
                full_data, data
            ])

        return full_data

    except FileNotFoundError as e:
        print(f"File Not Found: {e}")
    except ValueError as e:
        print(f"Data could not be converted to CSV: {e}")


def read_csv_file(filepath: str) -> pd.DataFrame:
    """Read CSV File and Adjust Formatting.

    Parameters:
    filepath -- Filepath to CSV data file

    Returns:
    A Pandas DataFrame containing the data from the CSV file.
    """
    try:
        with open(filepath) as f:
            data = [line.split(",") for line in f.readlines()]
            data = [[value.strip() for value in line if value.strip()] for line in data]

        # Remove the last line containing extraction details
        data.pop(-1)

        # Iterate over initial elements and remove them as they are extraction
        # details
        i = 0
        while i < 6:
            data.pop(0)
            i += 1

        # Column Names are the first list element
        column_names = data.pop(0)

        data = pd.DataFrame(data=data, columns=column_names)

        return data

    except FileNotFoundError as e:
        print(f"File Not Found: {e}")
    except ValueError as e:
        print(f"Data could not be converted to CSV: {e}")


if __name__ == "__main__":

    # Read, Convert, and Save Customer Details to CSV
    customer_details = convert_xlsx_to_csv("data/raw/cust.xlsx")
    customer_details.to_csv("data/source/customer_details.csv")

    # Read, Convert, and Save Invoice Details to CSV
    invoice_details = convert_xml_to_csv("data/raw/invoice.xml")
    invoice_details.to_csv("data/source/invoice_details.csv")

    # Read, Convert, and Save Product Details to CSV
    product_details = convert_json_to_csv("data/raw/product.json")
    product_details.to_csv("data/source/product_details.csv")

    # Read, Convert, and Save Region Details to CSV
    region_details = convert_txt_to_csv("data/raw/regiontxt")
    region_details.to_csv("data/source/region_details.csv")

    # Read, Convert, and Save Shipping Details to CSV
    shipping_details = read_csv_file("data/raw/shippuingaddress_20240521.csv.csv")
    shipping_details.to_csv("data/source/shipping_details.csv")
