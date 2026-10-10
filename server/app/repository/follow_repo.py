import uuid
from typing import List

from .baseRepo import BaseRepository
from app.core.models import Follow, User


class FollowRepository(BaseRepository):
    def follow(self, follower_id: uuid.UUID, following_id: uuid.UUID) -> Follow:
        follow = Follow(follower_id=follower_id, following_id=following_id)
        self.session.add(follow)
        self.session.commit()
        self.session.refresh(follow)
        return follow

    def unfollow(self, follower_id: uuid.UUID, following_id: uuid.UUID) -> bool:
        follow = (
            self.session.query(Follow)
            .filter_by(follower_id=follower_id, following_id=following_id)
            .first()
        )
        if not follow:
            return False
        self.session.delete(follow)
        self.session.commit()
        return True

    def is_following(self, follower_id: uuid.UUID, following_id: uuid.UUID) -> bool:
        return (
            self.session.query(Follow)
            .filter_by(follower_id=follower_id, following_id=following_id)
            .first()
            is not None
        )

    def get_followers(self, user_id: uuid.UUID) -> List[User]:
        return (
            self.session.query(User)
            .join(Follow, Follow.follower_id == User.id)
            .filter(Follow.following_id == user_id)
            .all()
        )

    def get_following(self, user_id: uuid.UUID) -> List[User]:
        return (
            self.session.query(User)
            .join(Follow, Follow.following_id == User.id)
            .filter(Follow.follower_id == user_id)
            .all()
        )

    def follower_count(self, user_id: uuid.UUID) -> int:
        return self.session.query(Follow).filter_by(following_id=user_id).count()

    def following_count(self, user_id: uuid.UUID) -> int:
        return self.session.query(Follow).filter_by(follower_id=user_id).count()