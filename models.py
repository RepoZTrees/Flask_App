import random
 
import faker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, BLOB, Date, Boolean, Table
from sqlalchemy.orm import sessionmaker, relationship
 
Base = declarative_base()
 
class Customer(Base):
    __tablename__ = "customers_list"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    jdate = Column(Date)
    address = Column(String)
    email = Column(String)
    invoices = relationship('Invoice', backref="customer")
 
class Invoice(Base):
    __tablename__ = "customer_invoices"
    id = Column(Integer, primary_key = True)
    particulars = Column(String)
    date = Column(Date)
    amount = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customers_list.id'))
 
def create_db():
    url = "postgres:///flask_invoices"
    # url = "sqlite:///invoice_db.sqlite"
    engine = create_engine(url)
    Base.metadata.create_all(engine)
 
def get_session():
    url = "postgres:///flask_invoices"
    # url = "sqlite:///invoice_db.sqlite"
    engine = create_engine(url)
    Session = sessionmaker(bind = engine)
    session = Session()
    return session
 
def main():
    create_db()
    f = faker.Faker()
    session = get_session()
    for i in range(100):
        c = Customer(name = f.name(),
                     jdate = f.date(),
                     address = f.address(),
                     email = f.email())
        session.add(c)
        for j in range(5):
            invoice = Invoice(particulars = f.sentence(),
                              date = f.date(),
                              amount = random.randint(10, 99),
                              customer = c)
            session.add(invoice)
    session.commit()
                               
     
 
if __name__ == "__main__":
    main()