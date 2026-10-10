from app.core.database import Base, engine
from app.core.models import User 
#Post, Follow


def create_tables():
    Base.metadata.create_all(bind= engine)