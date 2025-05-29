from sqlalchemy import Column, Integer, String, Float, DateTime, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create the SQLAlchemy engine
engine = create_engine('sqlite:///gold_purchases.db')

# Create a session factory
Session = sessionmaker(bind=engine)

# Create the base class for declarative models
Base = declarative_base()

def init_db():
    Base.metadata.create_all(engine)
    return Session()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    last_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    phone_number = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    remark = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.first_name} {self.last_name}')>"

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    customer_name = Column(String(100), nullable=False)
    phone_number = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    state = Column(String(50))
    purchase_date = Column(DateTime, default=datetime.now)
    gold_type = Column(String(50))
    gold_quality = Column(String(50))
    gold_weight = Column(Float)
    price_per_gram = Column(Float)
    total_amount = Column(Float)
    discount_percentage = Column(Float)
    discount_amount = Column(Float)
    final_amount = Column(Float)
    payment_mode = Column(String(50))
    notes = Column(Text)

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.customer_name}', phone='{self.phone_number}')>" 