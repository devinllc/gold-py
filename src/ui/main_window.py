from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QLineEdit,
                             QLabel, QMessageBox, QHeaderView, QFileDialog, QApplication)
from PyQt5.QtCore import Qt
from src.ui.customer_form import CustomerForm
from src.database.models import Customer, init_db, Session
import pandas as pd
from datetime import datetime
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_customers()

    def get_db_session(self):
        return Session()

    def setup_ui(self):
        self.setWindowTitle("Gold Purchase Management System")
        self.setMinimumSize(1200, 600)  # Increased width to accommodate buttons

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or phone...")
        self.search_input.textChanged.connect(self.search_customers)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(14)  # Added 2 columns for buttons
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "Phone", "Email", "Address", "State",
            "Gold Type", "Gold Quality", "Gold Weight (g)",
            "Price (₹/g)", "Total Amount (₹)", "Final Amount (₹)",
            "Update", "Delete"  # New columns for buttons
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Set fixed width for button columns
        self.table.setColumnWidth(12, 80)  # Update button column
        self.table.setColumnWidth(13, 80)  # Delete button column
        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add New Customer")
        add_button.clicked.connect(self.show_add_customer_form)
        import_button = QPushButton("Import from Excel")
        import_button.clicked.connect(self.import_from_excel)
        button_layout.addWidget(add_button)
        button_layout.addWidget(import_button)
        layout.addLayout(button_layout)

    def load_customers(self):
        session = self.get_db_session()
        try:
            customers = session.query(Customer).all()
            self.table.setRowCount(len(customers))
            
            for row, customer in enumerate(customers):
                # Add customer data
                self.table.setItem(row, 0, QTableWidgetItem(str(customer.id)))
                self.table.setItem(row, 1, QTableWidgetItem(customer.customer_name))
                self.table.setItem(row, 2, QTableWidgetItem(customer.phone_number or ""))
                self.table.setItem(row, 3, QTableWidgetItem(customer.email or ""))
                self.table.setItem(row, 4, QTableWidgetItem(customer.address or ""))
                self.table.setItem(row, 5, QTableWidgetItem(customer.state or ""))
                self.table.setItem(row, 6, QTableWidgetItem(customer.gold_type or ""))
                self.table.setItem(row, 7, QTableWidgetItem(customer.gold_quality or ""))
                self.table.setItem(row, 8, QTableWidgetItem(f"{customer.gold_weight:.3f}"))
                self.table.setItem(row, 9, QTableWidgetItem(f"{customer.price_per_gram:.2f}"))
                self.table.setItem(row, 10, QTableWidgetItem(f"{customer.total_amount:.2f}"))
                self.table.setItem(row, 11, QTableWidgetItem(f"{customer.final_amount:.2f}"))
                
                # Add update button
                update_btn = QPushButton("Update")
                update_btn.clicked.connect(lambda checked, c=customer: self.update_customer(c))
                self.table.setCellWidget(row, 12, update_btn)
                
                # Add delete button
                delete_btn = QPushButton("Delete")
                delete_btn.clicked.connect(lambda checked, c=customer: self.delete_customer(c))
                self.table.setCellWidget(row, 13, delete_btn)
        finally:
            session.close()

    def search_customers(self):
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            show_row = False
            # Search in name, phone, and email columns
            for col in range(3):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)

    def show_add_customer_form(self):
        try:
            form = CustomerForm(self)
            if form.exec_():
                try:
                    # Get the customer data from the form
                    customer_data = form.get_customer_data()
                    if customer_data:
                        # Create new customer using the main window's session
                        session = self.get_db_session()
                        try:
                            customer = Customer(**customer_data)
                            session.add(customer)
                            session.commit()
                            self.load_customers()  # Refresh the table
                        except Exception as e:
                            session.rollback()
                            raise e
                        finally:
                            session.close()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to create customer: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to show customer form: {str(e)}")

    def import_from_excel(self):
        try:
            # Open file dialog to select Excel or CSV file
            file_name, _ = QFileDialog.getOpenFileName(
                self,
                "Select File",
                "",
                "All Supported Files (*.xlsx *.xls *.csv);;Excel Files (*.xlsx *.xls);;CSV Files (*.csv)"
            )
            
            if not file_name:
                logger.info("No file selected")
                return

            logger.info(f"Selected file: {file_name}")

            # Read file based on extension
            file_ext = os.path.splitext(file_name)[1].lower()
            try:
                if file_ext == '.csv':
                    logger.info("Reading CSV file...")
                    df = pd.read_csv(file_name)
                else:
                    logger.info("Reading Excel file...")
                    df = pd.read_excel(file_name)
                
                logger.info(f"Successfully read file. Found {len(df)} rows")
                logger.info(f"Columns in file: {df.columns.tolist()}")
                
            except Exception as e:
                logger.error(f"Error reading file: {str(e)}")
                QMessageBox.critical(self, "File Read Error", f"Could not read file: {str(e)}")
                return
            
            # Validate required columns
            required_columns = ['customer_name', 'phone_number', 'email', 'address', 'state',
                              'purchase_date', 'gold_type', 'gold_quality', 'gold_weight',
                              'price_per_gram', 'total_amount', 'discount_percentage',
                              'discount_amount', 'final_amount', 'payment_mode']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                logger.error(f"Missing columns: {missing_columns}")
                QMessageBox.warning(
                    self,
                    "Invalid File Format",
                    f"File must contain these columns: {', '.join(required_columns)}\n"
                    f"Missing columns: {', '.join(missing_columns)}"
                )
                return

            # Process each row silently
            session = self.get_db_session()
            try:
                success_count = 0
                error_count = 0
                for index, row in df.iterrows():
                    try:
                        # Convert row to dictionary and handle NaN values
                        customer_data = {k: (v if pd.notna(v) else '') for k, v in row.items()}
                        
                        # Convert date string to datetime if needed
                        if isinstance(customer_data.get('purchase_date'), str):
                            try:
                                customer_data['purchase_date'] = pd.to_datetime(customer_data['purchase_date'])
                            except:
                                customer_data['purchase_date'] = datetime.now()
                        
                        # Convert numeric fields
                        for field in ['gold_weight', 'price_per_gram', 'total_amount', 
                                    'discount_percentage', 'discount_amount', 'final_amount']:
                            if field in customer_data and customer_data[field]:
                                try:
                                    customer_data[field] = float(customer_data[field])
                                except:
                                    customer_data[field] = 0.0
                        
                        # Create new customer record
                        customer = Customer(**customer_data)
                        session.add(customer)
                        success_count += 1
                        
                        # Commit every 100 records to avoid memory issues
                        if success_count % 100 == 0:
                            logger.info(f"Committed {success_count} records so far...")
                            session.commit()
                            
                    except Exception as e:
                        error_count += 1
                        logger.error(f"Error importing row {index + 1}: {str(e)}")
                        session.rollback()
                        continue

                # Final commit for remaining records
                session.commit()
                logger.info(f"Import completed. Successfully imported {success_count} records. Failed: {error_count}")
                
                # Show a brief message about the import
                if error_count > 0:
                    QMessageBox.information(self, "Import Complete", 
                        f"Successfully imported {success_count} records.\n"
                        f"Failed to import {error_count} records.\n"
                        "Check the logs for details.")
                else:
                    QMessageBox.information(self, "Import Complete", 
                        f"Successfully imported {success_count} records.")
                
                # Refresh the table to show new data
                self.load_customers()
                
            finally:
                session.close()

        except Exception as e:
            logger.error(f"Import failed: {str(e)}")
            QMessageBox.critical(self, "Import Error", f"Failed to import file: {str(e)}")

    def update_customer(self, customer):
        try:
            # Get a fresh session and customer instance
            session = self.get_db_session()
            try:
                # Get a fresh instance of the customer
                customer_to_update = session.query(Customer).get(customer.id)
                if not customer_to_update:
                    QMessageBox.critical(self, "Error", "Customer not found in database")
                    return

                # Create and show the form with the fresh customer instance
                form = CustomerForm(self, customer_to_update)
                if form.exec_():
                    try:
                        # Get the updated data from the form
                        updated_data = form.get_customer_data()
                        if updated_data:
                            # Update the customer in the current session
                            for key, value in updated_data.items():
                                setattr(customer_to_update, key, value)
                            session.commit()
                            self.load_customers()  # Refresh the table
                    except Exception as e:
                        session.rollback()
                        raise e
                else:
                    # Form was cancelled, rollback any changes
                    session.rollback()
            finally:
                session.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update customer: {str(e)}")

    def delete_customer(self, customer):
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete customer {customer.customer_name}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            session = self.get_db_session()
            try:
                # Get a fresh instance of the customer
                customer_to_delete = session.query(Customer).get(customer.id)
                if customer_to_delete:
                    session.delete(customer_to_delete)
                    session.commit()
                    self.load_customers()  # Refresh the table
                else:
                    QMessageBox.critical(self, "Error", "Customer not found in database")
            except Exception as e:
                session.rollback()
                QMessageBox.critical(self, "Error", f"Failed to delete customer: {str(e)}")
            finally:
                session.close()

    def closeEvent(self, event):
        event.accept() 