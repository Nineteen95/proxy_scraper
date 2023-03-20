from sqlalchemy import Column, Integer, String, DateTime, create_engine, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

# создаем базу данных
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}')
Base = declarative_base()


# модель данных для прокси-сервера
class Proxy(Base):
    __tablename__ = 'proxies'

    id = Column(Integer, primary_key=True)
    ip = Column(String(20))
    port = Column(Integer)
    protocol = Column(String(10))
    status = Column(String(10), default='OK')  # новое поле для статуса
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Proxy(ip='{self.ip}', port='{self.port}', protocol='{self.protocol}', status='{self.status}')>"


# модель данных для лога
class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    message = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Log(message='{self.message}', created_at='{self.created_at}')>"

# создаем таблицы в базе данных
Base.metadata.create_all(engine)
