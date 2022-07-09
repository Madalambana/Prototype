from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



#Local Testing 
#SQLALCHEMY_DATABASE_URL = '<postgres>://database_username:<password>@<ip-address>:<datanase_name>'

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:jpxfrd32@localhost:5432/wsu'

#Hosting means
#SQLALCHEMY_DATABASE_URL = f'<postgresql>://database_username:<password>@<ip-address>:<port-number>/<table>'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:    
        yield db
    finally:
        db.close()