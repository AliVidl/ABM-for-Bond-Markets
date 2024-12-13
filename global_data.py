
# Copyright (c) 2023 Alicia Vidler
# Licensed under the MIT License


import pandas as pd
import os


global_df = pd.DataFrame(columns=[
    "Run", "Step Number", "Status", "Unique ID", "Capability",
    "Metabolism Sug Bolism", "Metabolism Spice Bolism",
    "Accumulations Sugar", "Accumulations Spice",
    "Welfare Sug", "Welfare SPICE",
    "Pos", "MRS", "Price", "TradePartnerUID"
])


def append_to_df(row):
    global global_df
    # Convert row to DataFrame if it's not already one
    if not isinstance(row, pd.DataFrame):
        row = pd.DataFrame([row])
    global_df = pd.concat([global_df, row], ignore_index=True)

def write_to_csv(file_path="test2.csv"):
    global global_df
    if not global_df.empty:
        file_exists = os.path.exists(file_path)
        global_df.to_csv(file_path, mode='a', header=not file_exists, index=False)
        global_df = global_df.iloc[0:0]  # Clear the DataFrame after writing

