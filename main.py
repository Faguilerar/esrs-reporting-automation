"""
Main Script - ESRS Reporting Automation
Orchestrates the complete reporting process
"""

import sys
import os
from datetime import datetime

# Add scripts folder to path
sys.path.append('scripts')

from data_collection import DataCollector
from calculations import ESRSCalculator
from report_generator import ESRSReportGenerator

def main():
    """Main execution function"""
    print("=" * 60)
    print("ESRS REPORTING AUTOMATION")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # Step 1: Collect data
        print("\n[STEP 1] Collecting data from Excel files...")
        print("-" * 60)
        collector = DataCollector()
        all_data = collector.collect_all_data()
        esrs_data = collector.organize_by_esrs_module(all_data)
        
        if not any(esrs_data.values()):
            print("\nWARNING: No data found! Please check:")
            print("  1. Excel files are in the 'data/raw' folder")
            print("  2. Sheet names contain ESRS module codes (E1, E2, etc.)")
            return
        
        # Step 2: Calculate metrics
        print("\n[STEP 2] Calculating ESRS metrics...")
        print("-" * 60)
        calculator = ESRSCalculator()
        all_metrics = calculator.calculate_all_metrics(esrs_data)
        
        # Print calculated metrics
        for module, metrics in all_metrics.items():
            if metrics:
                print(f"\n{module} Metrics:")
                for key, value in metrics.items():
                    print(f"  - {key}: {value}")
        
        # Step 3: Generate report
        print("\n[STEP 3] Generating PDF report...")
        print("-" * 60)
        generator = ESRSReportGenerator()
        report_path = generator.generate_report(all_metrics)
        
        # Success message
        print("\n" + "=" * 60)
        print("✓ PROCESS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"Report saved to: {report_path}")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        print("\nPlease check:")
        print("  1. All required files are in place")
        print("  2. Excel files have correct format")
        print("  3. config.yaml is properly configured")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
