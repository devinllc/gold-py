from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QDoubleSpinBox,
                             QComboBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from src.database.models import Customer
from sqlalchemy.orm import Session

class CustomerForm(QDialog):
    def __init__(self, parent=None, customer=None):
        super().__init__(parent)
        self.customer = customer  # Store the customer if updating
        self.setup_ui()
        if customer:  # If updating, populate the form
            self.populate_form()

    def populate_form(self):
        """Populate form fields with customer data"""
        self.name_input.setText(self.customer.customer_name)
        self.phone_input.setText(self.customer.phone_number or "")
        self.email_input.setText(self.customer.email or "")
        self.address_input.setText(self.customer.address or "")
        self.state_input.setText(self.customer.state or "")
        self.gold_type_input.setCurrentText(self.customer.gold_type or "")
        self.gold_quality_input.setCurrentText(self.customer.gold_quality or "")
        self.weight_input.setValue(float(self.customer.gold_weight or 0))
        self.price_input.setValue(float(self.customer.price_per_gram or 0))
        self.discount_percent_input.setValue(float(self.customer.discount_percentage or 0))
        self.payment_input.setCurrentText(self.customer.payment_mode or "")
        self.notes_input.setText(self.customer.notes or "")
        
        if self.customer.purchase_date:
            self.date_input.setDate(self.customer.purchase_date)

    def setup_ui(self):
        self.setWindowTitle("Add New Customer")
        self.setMinimumWidth(500)
        layout = QVBoxLayout(self)

        # Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Phone
        phone_layout = QHBoxLayout()
        phone_label = QLabel("Phone:")
        self.phone_input = QLineEdit()
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_input)
        layout.addLayout(phone_layout)

        # Email
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        layout.addLayout(email_layout)

        # Address
        address_layout = QHBoxLayout()
        address_label = QLabel("Address:")
        self.address_input = QLineEdit()
        address_layout.addWidget(address_label)
        address_layout.addWidget(self.address_input)
        layout.addLayout(address_layout)

        # State
        state_layout = QHBoxLayout()
        state_label = QLabel("State:")
        self.state_input = QLineEdit()
        state_layout.addWidget(state_label)
        state_layout.addWidget(self.state_input)
        layout.addLayout(state_layout)

        # Purchase Date
        date_layout = QHBoxLayout()
        date_label = QLabel("Purchase Date:")
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_input)
        layout.addLayout(date_layout)

        # Gold Type
        gold_type_layout = QHBoxLayout()
        gold_type_label = QLabel("Gold Type:")
        self.gold_type_input = QComboBox()
        self.gold_type_input.addItems(['24K', '22K', '18K'])
        gold_type_layout.addWidget(gold_type_label)
        gold_type_layout.addWidget(self.gold_type_input)
        layout.addLayout(gold_type_layout)

        # Gold Quality
        gold_quality_layout = QHBoxLayout()
        gold_quality_label = QLabel("Gold Quality:")
        self.gold_quality_input = QComboBox()
        self.gold_quality_input.addItems(['Pure', 'Standard', 'Premium'])
        gold_quality_layout.addWidget(gold_quality_label)
        gold_quality_layout.addWidget(self.gold_quality_input)
        layout.addLayout(gold_quality_layout)

        # Gold Weight
        weight_layout = QHBoxLayout()
        weight_label = QLabel("Gold Weight (g):")
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(0, 10000)
        self.weight_input.setDecimals(3)
        weight_layout.addWidget(weight_label)
        weight_layout.addWidget(self.weight_input)
        layout.addLayout(weight_layout)

        # Price per gram
        price_layout = QHBoxLayout()
        price_label = QLabel("Price (₹/g):")
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 100000)
        self.price_input.setDecimals(2)
        price_layout.addWidget(price_label)
        price_layout.addWidget(self.price_input)
        layout.addLayout(price_layout)

        # Discount Percentage
        discount_percent_layout = QHBoxLayout()
        discount_percent_label = QLabel("Discount (%):")
        self.discount_percent_input = QDoubleSpinBox()
        self.discount_percent_input.setRange(0, 100)
        self.discount_percent_input.setDecimals(2)
        discount_percent_layout.addWidget(discount_percent_label)
        discount_percent_layout.addWidget(self.discount_percent_input)
        layout.addLayout(discount_percent_layout)

        # Payment Mode
        payment_layout = QHBoxLayout()
        payment_label = QLabel("Payment Mode:")
        self.payment_input = QComboBox()
        self.payment_input.addItems(['Cash', 'UPI', 'Bank Transfer', 'Card'])
        payment_layout.addWidget(payment_label)
        payment_layout.addWidget(self.payment_input)
        layout.addLayout(payment_layout)

        # Notes
        notes_layout = QHBoxLayout()
        notes_label = QLabel("Notes:")
        self.notes_input = QLineEdit()
        notes_layout.addWidget(notes_label)
        notes_layout.addWidget(self.notes_input)
        layout.addLayout(notes_layout)

        # Connect signals for auto-calculation
        self.weight_input.valueChanged.connect(self.calculate_amounts)
        self.price_input.valueChanged.connect(self.calculate_amounts)
        self.discount_percent_input.valueChanged.connect(self.calculate_amounts)

        # Total Amount (calculated)
        total_layout = QHBoxLayout()
        total_label = QLabel("Total Amount (₹):")
        self.total_label = QLabel("0.00")
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_label)
        layout.addLayout(total_layout)

        # Discount Amount (calculated)
        discount_amount_layout = QHBoxLayout()
        discount_amount_label = QLabel("Discount Amount (₹):")
        self.discount_amount_label = QLabel("0.00")
        discount_amount_layout.addWidget(discount_amount_label)
        discount_amount_layout.addWidget(self.discount_amount_label)
        layout.addLayout(discount_amount_layout)

        # Final Amount (calculated)
        final_amount_layout = QHBoxLayout()
        final_amount_label = QLabel("Final Amount (₹):")
        self.final_amount_label = QLabel("0.00")
        final_amount_layout.addWidget(final_amount_label)
        final_amount_layout.addWidget(self.final_amount_label)
        layout.addLayout(final_amount_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_customer)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def calculate_amounts(self):
        weight = self.weight_input.value()
        price = self.price_input.value()
        discount_percent = self.discount_percent_input.value()
        
        total = weight * price
        discount_amount = total * (discount_percent / 100)
        final_amount = total - discount_amount
        
        self.total_label.setText(f"{total:.2f}")
        self.discount_amount_label.setText(f"{discount_amount:.2f}")
        self.final_amount_label.setText(f"{final_amount:.2f}")

    def get_customer_data(self):
        """Get the current form data as a dictionary"""
        try:
            # Get values from inputs
            name = self.name_input.text().strip()
            if not name:
                QMessageBox.warning(self, "Validation Error", "Customer name is required")
                return None

            # Create customer data dictionary
            customer_data = {
                'customer_name': name,
                'phone_number': self.phone_input.text().strip(),
                'email': self.email_input.text().strip(),
                'address': self.address_input.text().strip(),
                'state': self.state_input.text().strip(),
                'purchase_date': self.date_input.date().toPyDate(),
                'gold_type': self.gold_type_input.currentText(),
                'gold_quality': self.gold_quality_input.currentText(),
                'gold_weight': self.weight_input.value(),
                'price_per_gram': self.price_input.value(),
                'discount_percentage': self.discount_percent_input.value(),
                'payment_mode': self.payment_input.currentText(),
                'notes': self.notes_input.text().strip()
            }

            # Calculate amounts
            customer_data['total_amount'] = customer_data['gold_weight'] * customer_data['price_per_gram']
            customer_data['discount_amount'] = (customer_data['total_amount'] * customer_data['discount_percentage']) / 100
            customer_data['final_amount'] = customer_data['total_amount'] - customer_data['discount_amount']

            return customer_data
        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", "Please enter valid numbers for weight, price, and discount")
            return None
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to get customer data: {str(e)}")
            return None

    def save_customer(self):
        try:
            # Just validate and accept the dialog
            # The parent window will handle the actual saving
            customer_data = self.get_customer_data()
            if customer_data:
                self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to validate customer data: {str(e)}") 