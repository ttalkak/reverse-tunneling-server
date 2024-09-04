from sqlalchemy import Column, Integer, TIMESTAMP, String
from sqlalchemy.sql import func
from .base import Base

class Domain(Base):
    __tablename__ = "principles"

    id = Column("id", Integer, primary_key=True, index=True)
    identifier = Column("identifier", String)
    display_name = Column("display_name", String)
    token = Column("token", String)
    subdomain = Column("subdomain", String)
    created_at = Column("created_at", TIMESTAMP, default=func.now())
    updated_at = Column("updated_at", TIMESTAMP, default=func.now())