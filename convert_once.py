#!/usr/bin/env python3
"""
Convert a CSV to JSON once and exit.
Usage:
  python convert_once.py "My Cellar.csv" wine-data.json
"""
import sys
import pandas as pd

def convert(input_path, output_path):
    # → Use utf-8-sig for UTF-8 with/without BOM; switch to cp1252 if needed
    df = pd.read_csv(input_path, encoding='cp1252')
    if 'Type' in df.columns:
        df['Type'] = df['Type'].replace({'Red - Fortified': 'Red - Sweet/Dessert'})
    cols = ['Producer', 'Type', 'Country', 'MasterVarietal',
            'Wine', 'Region', 'Appellation', 'Vintage', 'iWine']
    df_selected = df[[c for c in cols if c in df.columns]]
    # → Preserve real unicode in output
    df_selected.to_json(
        output_path,
        orient='records',
        indent=2,
        force_ascii=False
    )
    print(f"Wrote {len(df_selected)} records to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_once.py INPUT.csv OUTPUT.json")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
