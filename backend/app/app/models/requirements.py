from sqlalchemy import Column, Integer, String, DateTime,Text, ForeignKey
from sqlalchemy.dialects.mysql.types import TINYINT
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Requirements(Base):
    id = Column(Integer,primary_key="True")
    name = Column(String(250))
    created_by = Column(Integer,ForeignKey("user.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    status = Column(TINYINT,comment="1->active,-1->deleted")

    lead = relationship("Lead",back_populates="requirements")
    user = relationship("User",back_populates="requirements")