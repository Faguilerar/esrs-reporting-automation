"""
Data Collection Module
Reads data from multiple Excel files and consolidates for ESRS reporting
"""

import pandas as pd
import glob
import os
from datetime import datetime
import yaml

class DataCollector:
    def __init__(self, config_path='config/config.yaml'):
        """Initialize data collector with configuration"""
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.data_folder = self.config['data_sources']['excel_folder']
        self.file_pattern = self.config['data_sources']['file_pattern']
        
    def find_excel_files(self):
        """Find all Excel files in the data folder"""
        pattern = os.path.join(self.data_folder, self.file_pattern)
        files = glob.glob(pattern)
        print(f"Found {len(files)} Excel files")
        return files
    
    def read_excel_file(self, filepath):
        """Read an Excel file and return all sheets as a dictionary"""
        try:
            excel_file = pd.ExcelFile(filepath)
            data = {}
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(filepath, sheet_name=sheet_name)
                data[sheet_name] = df
                print(f"  - Loaded sheet: {sheet_name} ({len(df)} rows)")
            
            return data
        except Exception as e:
            print(f"Error reading {filepath}: {str(e)}")
            return None
    
    def collect_all_data(self):
        """Collect data from all Excel files"""
        all_data = {}
        files = self.find_excel_files()
        
        for filepath in files:
            filename = os.path.basename(filepath)
            print(f"\nProcessing: {filename}")
            
            file_data = self.read_excel_file(filepath)
            if file_data:
                all_data[filename] = file_data
        
        return all_data
    
    def organize_by_esrs_module(self, all_data):
        """Organize collected data by ESRS module"""
        esrs_data = {module: [] for module in self.config['esrs_modules']}
        
        for filename, sheets in all_data.items():
            for sheet_name, df in sheets.items():
                # Try to identify ESRS module from sheet name
                for module in self.config['esrs_modules']:
                    if module.upper() in sheet_name.upper():
                        esrs_data[module].append({
                            'source': filename,
                            'sheet': sheet_name,
                            'data': df
                        })
                        break
        
        return esrs_data
    
    def save_processed_data(self, esrs_data):
        """Save processed data to the processed folder"""
        output_folder = 'data/processed'
        os.makedirs(output_folder, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for module, data_list in esrs_data.items():
            if data_list:
                # Combine all dataframes for this module
                combined_df = pd.concat([item['data'] for item in data_list], 
                                       ignore_index=True)
                
                output_file = os.path.join(output_folder, 
                                          f'{module}_processed_{timestamp}.xlsx')
                combined_df.to_excel(output_file, index=False)
                print(f"Saved {module} data to {output_file}")
        
        return timestamp

if __name__ == "__main__":
    # Test the data collector
    collector = DataCollector()
    all_data = collector.collect_all_data()
    esrs_data = collector.organize_by_esrs_module(all_data)
    timestamp = collector.save_processed_data(esrs_data)
    print(f"\nData collection complete! Timestamp: {timestamp}")
