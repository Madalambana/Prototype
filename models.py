from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, column
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Molest(Base):
    __tablename__ = "molest"
    pid = Column(Integer, primary_key=True, nullable=False)
    firstName = Column(String,)
    lastName = Column(String)
    ethicinity = Column(String, nullable=False)
    contact = Column(Integer)
    Id = Column(String)
    location = Column(String)
    postal = Column(Integer)
    report = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))

class GBV(Base):
    __tablename__ = "gbv"
    pid = Column(Integer, primary_key=True, nullable=False)
    firstName = Column(String,)
    lastName = Column(String)
    gender = Column(String)
    ethicinity = Column(String, nullable=False)
    contact = Column(Integer)
    Id = Column(String)
    location = Column(String)
    postal = Column(Integer)
    report = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))


class Assist(Base):
    __tablename__ = "assist"
    pid = Column(Integer, primary_key=True, nullable=False)
    firstName = Column(String,)
    location = Column(String)
    postal = Column(Integer)
    contact = Column(Integer)
    report = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))