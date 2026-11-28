import pandas as pd

# 1. Define file paths and names
raw_path = "d:/Final Raw Data/Raw"
clean_path = "d:/Final Raw Data/Raw/cleaned_data"

files = [
    "DimCustomer",
    "DimProduct",
    "DimSalesRep",
    "DimStore",
    "FactCommissionRules",
    "FactSales",
    "FactSalesTargets",
]

# 2. Reading CSV files into DataFrames
dataframes = {}
for name in files:
    dataframes[name] = pd.read_csv(f"{raw_path}/{name}.csv", low_memory=False)
    print(f"{name} Loaded Successfully")


# 3. Show the first few rows of each Table
for name, df in dataframes.items():
    print(f"\n{name} DataFrame:")
    print(df.shape)
    print(df.info())
    print(df.head())

# Search for negative values in FactSales
df = dataframes["FactSales"]

negative_rows = df[df["Quantity"] < 0]

if  not negative_rows.empty:
    print(f"Found {len(negative_rows)} rows containing negative values:")
    print(negative_rows.to_string())
else:
    print("No negative values found in FactSales.")

# 3. General Cleaning (Trimming whitespace, converting to title case, removing duplicates and nulls)
excluded_title_cols = {"SKU", "CommissionPlanID", "CommissionBasis"}
for name, df in dataframes.items():
    text_columns = df.select_dtypes(include=["object", "string"]).columns
    for col in text_columns:
        df[col] = df[col].str.strip()
        if col not in excluded_title_cols:
            df[col] = df[col].str.title()

    df.drop_duplicates(inplace=True)
    df.dropna(how="all", inplace=True)

# 4. Convert negative values to positive in the 'Quantity' column of FactSales
dataframes["FactSales"]["Quantity"] = dataframes["FactSales"]["Quantity"].abs()
print("\nFactSales: Converted negative values in 'Quantity' to positive.")

# 5. Save the cleaned files
for name, df in dataframes.items():
    df.to_csv(f"{clean_path}/{name}.csv", index=False)
    print(f"{name} Saved Successfully")