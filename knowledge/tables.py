from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class KnowledgeSchema(Base):
    __tablename__ = 'knowledge'
    id = Column(Integer, primary_key=True)
    question = Column(String(256), nullable=False)
    category = Column(String(256), nullable=False)
    answer = Column(String(1024), nullable=True)
    links = Column(String(2056), nullable=True)
    countries = Column(String(2056), nullable=True)
    additional_answers = Column(String(2056), nullable=True)
    additional_links = Column(String(2056), nullable=True)
    date_created = Column(DateTime, default=datetime.utcnow)

    def __init__(self,
                 question=None,
                 category=None,
                 answer=None,
                 links=None,
                 countries=None,
                 additional_answers=None,
                 additional_links=None):
        self.question = question
        self.category = category
        self.answer = answer
        self.links = links
        self.countries = countries
        self.additional_answers = additional_answers
        self.additional_links = additional_links

    def __repr__(self):
        return self.id


class LogsSchema(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    type = Column(String(256), nullable=False)
    message = Column(String(5120), nullable=False)
    info = Column(String(2056), nullable=True)
    date_created = Column(DateTime, default=datetime.utcnow)

    def __init__(self,
                 type=None,
                 message=None,
                 info=None):
        self.type = type
        self.message = message
        self.info = info

    def __repr__(self):
        return self.id
