#!/usr/bin/env python3
"""
Watch an Excel/CSV file for changes and automatically re-generate wine-data.json.
Usage:
  pip install pandas watchdog
  python watch_and_convert.py "My Cellar.csv" wine-data.json
"""
import time
import sys
import os
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ExcelEventHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path):
        self.input_path = os.path.abspath(input_path)
        self.output_path = output_path
        self._last_modified = None

    def on_modified(self, event):
        # Debounce multiple events
        if event.src_path != self.input_path:
            return
        try:
            mtime = os.path.getmtime(self.input_path)
            if self._last_modified == mtime:
                return
            self._last_modified = mtime
            print(f"Detected change in '{self.input_path}' at {time.ctime(mtime)}, regenerating JSON...")
            # Load and fix iWine BOM column
            df = pd.read_csv(self.input_path, encoding='latin-1')
            df = df.rename(columns={"ï»¿iWine": "iWine"})
            if 'Type' in df.columns:
                df['Type'] = df['Type'].replace({'Red - Fortified': 'Red - Sweet/Dessert'})
            else:
                print("Warning: 'Type' column not found in input file.")
            # Use the corrected column list, including 'Value'
            cols = ['Producer', 'Type', 'Country', 'MasterVarietal', 'Wine', 'Region', 'Appellation', 'Vintage', 'iWine', 'Value']
            missing_cols = [col for col in cols if col not in df.columns]
            if missing_cols:
                print(f"Warning: Missing columns in input file: {missing_cols}")
            df_selected = df[[col for col in cols if col in df.columns]]
            # Write JSON
            output_json_path = os.path.abspath(self.output_path)
            df_selected.to_json(output_json_path, orient='records', indent=2)
            print(f"Successfully wrote {len(df_selected)} records to '{output_json_path}'")
        except Exception as e:
            print(f"Error processing '{self.input_path}': {e}")

if __name__ == '__main__':
    input_path = sys.argv[1] if len(sys.argv) > 1 else 'My Cellar.csv'
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'wine-data.json'

    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}")
        sys.exit(1)

    event_handler = ExcelEventHandler(input_path, output_path)
    observer = Observer()
    watch_dir = os.path.dirname(os.path.abspath(input_path)) or '.'
    observer.schedule(event_handler, path=watch_dir, recursive=False)
    observer.start()
    print(f"Watching '{input_path}' for changes. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
