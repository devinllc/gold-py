# Gold Purchase Management System

A desktop application for managing gold purchase records, built with Python, PyQt5, and SQLAlchemy.

## Features

- Add, update, and delete customer records
- Import customer data from Excel (.xlsx, .xls) and CSV files
- Search customers by name, phone, or email
- Track gold purchases with detailed information
- Calculate total amounts, discounts, and final amounts automatically
- Modern and user-friendly interface

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Windows 10 or higher

## Installation

1. Clone or download this repository to your local machine

2. Open Command Prompt (cmd) and navigate to the project directory:
```cmd
cd path\to\gold
```

3. Create a virtual environment (recommended):
```cmd
python -m venv venv
```

4. Activate the virtual environment:
```cmd
venv\Scripts\activate
```

5. Install required packages:
```cmd
pip install -r requirements.txt
```

## Running the Application

1. Make sure your virtual environment is activated:
```cmd
venv\Scripts\activate
```

2. Run the application:
```cmd
python src\main.py
```

## Database Setup

The application uses SQLite as its database. The database file (`gold.db`) will be created automatically when you first run the application.

If you need to reset the database:
1. Delete the `gold.db` file from the project directory
2. Restart the application

## Importing Data

The application supports importing customer data from:
- Excel files (.xlsx, .xls)
- CSV files (.csv)

Required columns in the import file:
- customer_name
- phone_number
- email
- address
- state
- purchase_date
- gold_type
- gold_quality
- gold_weight
- price_per_gram
- total_amount
- discount_percentage
- discount_amount
- final_amount
- payment_mode

## Troubleshooting

1. If you get a "Module not found" error:
   - Make sure you have activated the virtual environment
   - Verify that all requirements are installed: `pip install -r requirements.txt`

2. If the application fails to start:
   - Check if Python 3.8 or higher is installed: `python --version`
   - Ensure all dependencies are installed correctly
   - Check the application logs for detailed error messages

3. If database operations fail:
   - Make sure you have write permissions in the project directory
   - Try deleting the `gold.db` file and restart the application

## Support

For any issues or questions, please:
1. Check the troubleshooting section above
2. Review the application logs
3. Create an issue in the repository

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Project Structure
```
gold/
├── src/
│   ├── main.py              # Main application entry point
│   ├── database/
│   │   ├── models.py        # Database models
│   │   └── database.py      # Database connection and setup
│   └── ui/
│       ├── main_window.py   # Main window UI
│       └── customer_form.py # Customer data entry form
├── requirements.txt         # Project dependencies
└── README.md               # This file
``` 

PYTHONPATH=/Users/vramesh/Developer/production/gold python3 src/main.py
python3 generate_user_data.py



exe on windows--
pip install pyinstaller





## Creating a Windows Executable (.exe)

You can create a standalone Windows executable for this application using [PyInstaller](https://pyinstaller.org/). This allows you to run the app on any Windows machine without requiring Python to be installed.

### Step-by-Step Instructions

1. **Install PyInstaller**
   (Make sure your virtual environment is activated)
   ```cmd
   pip install pyinstaller
   ```

2. **Navigate to your project directory**
   ```cmd
   cd path\to\gold
   ```

3. **Run PyInstaller on the entry script**
   The entry point for this app is `run.py` in the project root:
   ```cmd
   pyinstaller --onefile --windowed run.py
   ```
   - `--onefile`: Bundles everything into a single .exe file
   - `--windowed`: Hides the console window (for GUI apps)

4. **Find your executable**
   After the build completes, look in the `dist` folder. You will see `run.exe`.

5. **Test the executable**
   Double-click `run.exe` in the `dist` folder to launch the application.

### Notes
- If your app uses data files (e.g., .db, .csv), you may need to copy them into the same folder as the .exe, or use the `--add-data` option in PyInstaller. See the [PyInstaller docs](https://pyinstaller.org/en/stable/usage.html#adding-data-files) for details.
- If you get errors, check the `dist` and `build` folders for logs, or run PyInstaller without `--windowed` to see error messages.
- You only need to run PyInstaller once per new version or code change.

## Database Setup

The application uses SQLite as its database. The database file (`gold.db`) will be created automatically when you first run the application.

If you need to reset the database:
1. Delete the `gold.db` file from the project directory
2. Restart the application

## Importing Data

The application supports importing customer data from:
- Excel files (.xlsx, .xls)
- CSV files (.csv)

Required columns in the import file:
- customer_name
- phone_number
- email
- address
- state
- purchase_date
- gold_type
- gold_quality
- gold_weight
- price_per_gram
- total_amount
- discount_percentage
- discount_amount
- final_amount
- payment_mode

## Troubleshooting

1. If you get a "Module not found" error:
   - Make sure you have activated the virtual environment
   - Verify that all requirements are installed: `pip install -r requirements.txt`

2. If the application fails to start:
   - Check if Python 3.8 or higher is installed: `python --version`
   - Ensure all dependencies are installed correctly
   - Check the application logs for detailed error messages

3. If database operations fail:
   - Make sure you have write permissions in the project directory
   - Try deleting the `gold.db` file and restart the application

## Support

For any issues or questions, please:
1. Check the troubleshooting section above
2. Review the application logs
3. Create an issue in the repository

