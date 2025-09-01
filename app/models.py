from database import Base
from sqlalchemy import Column,Integer,DATE,Text


class POST(Base):
    __tablename__ = 'posts'
    __table_args__ = {'schema': 'post'}

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(Text)
    dashboard = Column(Text)
    dashboard_url = Column(Text)
    indicators = Column(Text)
    date = Column(DATE)




