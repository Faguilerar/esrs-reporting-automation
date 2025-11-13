# esrs-reporting-automation
ESRS reporting automation system - Extracts data from Excel/Sheets and generates complete PDF reports
# ESRS Reporting Automation

Automated system for generating ESRS (European Sustainability Reporting Standards) compliant PDF reports from Excel data.

## Features

- ✅ Reads data from multiple Excel files
- ✅ Supports all ESRS modules (E1-E5, S1-S4, G1)
- ✅ Automatic KPI calculations
- ✅ Professional PDF report generation
- ✅ Configurable via YAML

## Project Structure
```
esrs-reporting-automation/
│
├── data/
│   ├── raw/              # Place your Excel files here
│   └── processed/        # Processed data (auto-generated)
│
├── scripts/
│   ├── data_collection.py    # Data extraction
│   ├── calculations.py       # KPI calculations
│   └── report_generator.py   # PDF generation
│
├── templates/            # Report templates (future use)
├── output/              # Generated PDF reports
├── config/
│   └── config.yaml      # Configuration file
│
├── main.py              # Main script to run
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Installation

1. **Clone this repository**
```bash
git clone https://github.com/YOUR_USERNAME/esrs-reporting-automation.git
cd esrs-reporting-automation
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure the system**
   - Edit `config/config.yaml`
   - Update company name and reporting period

## Usage

### Step 1: Prepare Your Data

Place your Excel files in the `data/raw/` folder. 

**Excel File Structure:**
- Use sheet names that include ESRS module codes (E1, E2, E3, etc.)
- Examples: "E1_Climate_Data", "Emissions_E1", "S1_Workforce"

**Expected Columns (examples):**

For E1 (Climate):
- `emissions_scope1`
- `emissions_scope2`
- `emissions_scope3`

For E5 (Circular Economy):
- `waste_generated`
- `waste_recycled`

*(Customize column names in the calculation scripts)*

### Step 2: Run the System
```bash
python main.py
```

### Step 3: Get Your Report

Find your PDF report in the `output/` folder!

## Customization

### Adjust Calculations

Edit `scripts/calculations.py` to modify KPI formulas based on your data structure.

### Modify PDF Layout

Edit `scripts/report_generator.py` to change report design, colors, and layout.

### Change Configuration

Edit `config/config.yaml` to:
- Select which ESRS modules to include
- Change company information
- Adjust file patterns

## Excel File Examples

### Example 1: Single file with multiple sheets
```
sustainability_data_2024.xlsx
  ├── E1_Emissions
  ├── E3_Water
  └── S1_Employees
```

### Example 2: Multiple files
```
data/raw/
  ├── climate_data_e1.xlsx
  ├── pollution_e2.xlsx
  └── workforce_s1.xlsx
```

## Troubleshooting

**No data found?**
- Check that Excel files are in `data/raw/`
- Ensure sheet names contain module codes (E1, E2, etc.)

**PDF generation fails?**
- Install reportlab: `pip install reportlab`
- Check write permissions in `output/` folder

**Wrong calculations?**
- Verify column names in your Excel match those in `calculations.py`
- Update column mappings as needed

## Requirements

- Python 3.8+
- pandas
- openpyxl
- reportlab
- PyYAML

## License

MIT License - Feel free to modify and use for your organization.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Contact

For questions or support, please open an issue on GitHub.

---

**Note:** This is a template system. Customize the calculations and report layout according to your specific ESRS disclosure requirements.
