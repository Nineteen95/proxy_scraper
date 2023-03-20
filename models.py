from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
PGDATA = os.environ.get("PGDATA")

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Proxy(Base):
    __tablename__ = 'proxies'

    class Proxy(Base):
        __tablename__ = 'proxies'

        id = Column(Integer, primary_key=True)
        ip = Column(String, unique=True)
        port = Column(String)
        country = Column(String)
        anonymity = Column(String)
        created_at = Column(DateTime, default=datetime.datetime.utcnow)
        updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
        status = Column(String, default="unchecked")

    def __repr__(self):
        return f"<Proxy(id={self.id}, ip_address='{self.ip_address}', port={self.port}, is_https={self.is_https})>"
