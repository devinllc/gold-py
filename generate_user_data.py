#!/usr/bin/env python3
import csv
from faker import Faker
import random
import os

def generate_sample_users(num_records=100):
    fake = Faker('en_IN')  # Using Indian locale for more realistic data
    users = []
    
    for _ in range(num_records):
        # Generate a full name and split it into parts
        full_name = fake.name().split()
        if len(full_name) >= 3:
            first_name = full_name[0]
            middle_name = full_name[1]
            last_name = ' '.join(full_name[2:])
        elif len(full_name) == 2:
            first_name = full_name[0]
            middle_name = ''
            last_name = full_name[1]
        else:
            first_name = full_name[0]
            middle_name = ''
            last_name = fake.last_name()

        user = {
            'last_name': last_name,
            'first_name': first_name,
            'middle_name': middle_name,
            'phone_number': fake.phone_number(),
            'email': fake.email(),
            'address': fake.address(),
            'remark': random.choice(['', 'VIP', 'Regular', 'New', 'Preferred']) if random.random() < 0.3 else ''
        }
        users.append(user)
    
    return users

def save_to_csv(data, filename='sample_users.csv'):
    fieldnames = ['last_name', 'first_name', 'middle_name', 'phone_number', 'email', 'address', 'remark']
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"Successfully generated {len(data)} user records")
        print(f"File saved as: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"Error saving file: {str(e)}")

if __name__ == "__main__":
    try:
        print("Generating sample user data...")
        users = generate_sample_users(100)  # Generate 100 sample users
        save_to_csv(users)
    except Exception as e:
        print(f"Error: {str(e)}") 