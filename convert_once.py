#!/usr/bin/env python3
import sys
import os
import pandas as pd

if __name__ == '__main__':
    input_path = sys.argv[1] if len(sys.argv) > 1 else 'My Cellar.csv'
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'wine-data.json'

    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}")
        sys.exit(1)

    try:
        df = pd.read_csv(input_path, encoding='UTF-8')
        df = df.rename(columns={"ï»¿iWine": "iWine"})
        if 'Type' in df.columns:
            df['Type'] = df['Type'].replace({'Red - Fortified': 'Red - Sweet/Dessert'})
        else:
            print("Warning: 'Type' column not found in input file.")
        cols = ['Producer', 'Type', 'Country', 'MasterVarietal', 'Wine', 'Region', 'Appellation', 'Vintage', 'iWine', 'Value']
        missing_cols = [col for col in cols if col not in df.columns]
        if missing_cols:
            print(f"Warning: Missing columns in input file: {missing_cols}")
        df_selected = df[[col for col in cols if col in df.columns]]
        output_json_path = os.path.abspath(output_path)
        df_selected.to_json(output_json_path, orient='records', indent=2)
        print(f"Successfully wrote {len(df_selected)} records to '{output_json_path}'")
    except Exception as e:
        print(f"Error processing '{input_path}': {e}")
        sys.exit(1)
