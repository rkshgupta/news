
from pydantic import BaseModel

class News(BaseModel):
    headline: str
    link: str
    source: str
