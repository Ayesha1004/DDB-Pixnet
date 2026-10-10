import uuid
from .baseRepo import BaseRepository
from app.core.models import User
from app.core.schema import UserCreate, UserLogin, UserOut
from app.core.security import hash_password
#making for a user for now

class UserRepository(BaseRepository):
    def create_user(self, user_data: UserCreate):
        newUser = User(
             username = user_data.username,
             email = user_data.email,
             password_hash = hash_password(user_data.password) 
        ) #dumping the data we get from schema to model User

        self.session.add(instance = newUser) #add the python object to the session
        self.session.commit() #permanently save the object into db
        self.session.refresh(instance = newUser)

        return newUser

    def user_exists_by_email(self, email: str) -> bool:
        user = self.session.query(User).filter_by(email=email).first()
        return bool(user)

    def get_by_email(self, email: str) -> User:
            user = self.session.query(User).filter_by(email=email).first()
            return user
    def user_exists_by_username(self, username: str) -> bool:
            user = self.session.query(User).filter_by(username=username).first()
            return bool(user)
    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self.session.query(User).filter_by(id=user_id).first()

    def get_by_username(self, username: str) -> User | None:
        return self.session.query(User).filter_by(username=username).first()

    def update_avatar(self, user_id: uuid.UUID, avatar_url: str) -> User:
        user = self.get_by_id(user_id)
        user.avatar_url = avatar_url
        self.session.commit()
        self.session.refresh(user)
        return user

    