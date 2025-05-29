#!/usr/bin/env python3

import sys
import os
import csv
import random
from datetime import datetime, timedelta

try:
    from faker import Faker
except ImportError:
    print("Faker package is not installed. Installing it now...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Faker==20.1.0"])
    from faker import Faker

def generate_sample_data(num_records=2000):
    try:
        # Initialize Faker for generating realistic data
        fake = Faker('en_IN')  # Using Indian locale for more realistic Indian names and addresses

        # Define possible values for various fields
        gold_types = ['24K', '22K', '18K']
        gold_qualities = ['Pure', 'Standard', 'Premium']
        payment_modes = ['Cash', 'UPI', 'Bank Transfer', 'Card']
        states = ['Karnataka', 'Maharashtra', 'Tamil Nadu', 'Kerala', 'Andhra Pradesh', 
                'Telangana', 'Gujarat', 'Delhi', 'West Bengal', 'Rajasthan']
        
        print("Generating sample data...")
        # Generate data
        data = []
        for i in range(num_records):
            if i % 200 == 0:  # Progress indicator
                print(f"Generated {i} records...")
                
            # Generate a random date within the last 2 years
            random_days = random.randint(0, 730)  # 730 days = 2 years
            purchase_date = (datetime.now() - timedelta(days=random_days)).strftime('%Y-%m-%d')
            
            # Generate random gold weight between 1 and 1000 grams
            gold_weight = round(random.uniform(1, 1000), 3)
            
            # Generate random price per gram between 5000 and 7000
            price_per_gram = round(random.uniform(5000, 7000), 2)
            
            # Calculate total amount
            total_amount = round(gold_weight * price_per_gram, 2)
            
            # Generate random discount between 0 and 5%
            discount_percentage = round(random.uniform(0, 5), 2)
            discount_amount = round(total_amount * (discount_percentage / 100), 2)
            final_amount = round(total_amount - discount_amount, 2)
            
            # Generate customer data
            customer_data = {
                'customer_name': fake.name(),
                'phone_number': fake.phone_number(),
                'email': fake.email(),
                'address': fake.address().replace('\n', ', '),
                'state': random.choice(states),
                'purchase_date': purchase_date,
                'gold_type': random.choice(gold_types),
                'gold_quality': random.choice(gold_qualities),
                'gold_weight': gold_weight,
                'price_per_gram': price_per_gram,
                'total_amount': total_amount,
                'discount_percentage': discount_percentage,
                'discount_amount': discount_amount,
                'final_amount': final_amount,
                'payment_mode': random.choice(payment_modes),
                'notes': fake.sentence() if random.random() < 0.3 else ''  # 30% chance of having notes
            }
            data.append(customer_data)
        
        return data
    except Exception as e:
        print(f"Error generating data: {str(e)}")
        raise

def save_to_csv(data, filename='sample_customer_data.csv'):
    try:
        # Define the field names (column headers)
        fieldnames = [
            'customer_name', 'phone_number', 'email', 'address', 'state',
            'purchase_date', 'gold_type', 'gold_quality', 'gold_weight',
            'price_per_gram', 'total_amount', 'discount_percentage',
            'discount_amount', 'final_amount', 'payment_mode', 'notes'
        ]
        
        print(f"Writing data to {filename}...")
        # Write to CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"Successfully generated {len(data)} records in {filename}")
        print(f"File location: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"Error saving to CSV: {str(e)}")
        raise

if __name__ == '__main__':
    try:
        print("Starting data generation...")
        # Generate 2000 records
        sample_data = generate_sample_data(2000)
        
        # Save to CSV
        save_to_csv(sample_data)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1) 