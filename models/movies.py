from sqlalchemy import Table,Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class movies(Base):
    __tablename__ = 'movies'

    id = Column('id',Integer(),primary_key=True)  
    name = Column('name',String(40)) 
    video_url = Column('url_video',String(100)) 
    image_url = Column('url_image',String(100))  
