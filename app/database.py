from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
import time
import psycopg2
from urllib.parse import quote

password = 'Sustain@2023'
encoded_password = quote(password, safe='')

#SQL_ALCHEMY_DATABASE_URL = 'postgresql://<username>:<password><@ip-address/hostname>/<database_name>'
SQL_ALCHEMY_DATABASE_URL = f'postgresql://postgres:{encoded_password}@localhost/fastapi'
engine = create_engine(SQL_ALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host = "localhost", database="fastapi", user= "postgres",
#                     password ="Sustain@2023", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection is Successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error:", error)
#         time.sleep(2)


