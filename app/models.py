from sqlalchemy import Column, Integer, String, Text
from database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(Text, nullable=False)
    short_hash = Column(String(10), unique=True, nullable=False)

