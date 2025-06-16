from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Rules table
class Rule(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    rule_json = Column(Text) # Armazena a regra em formato JSON

# Representation of an user's system
class DataEndpoint(BaseModel):
    endpoint_identifier: str
    space_quota: int
    space_used: int
    associated_email: str
    last_access: datetime

# Representation of a rule
class RuleInput(BaseModel):
    rule_json: Dict[str, Any]