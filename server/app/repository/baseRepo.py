from sqlalchemy.orm import Session


#Users for now

class BaseRepository:
    def __init__(self, session : Session) -> None:
        self.session = session


