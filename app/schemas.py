from pydantic import BaseModel
import datetime

class Posts(BaseModel):
    topic:str
    dashboard_url:str
    indicators:str
    date:datetime


class UpdatePost(BaseModel):
    topic: str = None
    dashboard_url:str = None
    indicators: str = None
    date: datetime = None

    
