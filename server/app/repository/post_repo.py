import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from .baseRepo import BaseRepository
from app.core.models import Post


class PostRepository(BaseRepository):
    def create(self, owner_id: uuid.UUID, caption: Optional[str], image_url: str) -> Post:
        post = Post(owner_id=owner_id, caption=caption, image_url=image_url)
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post

    def get_by_id(self, post_id: uuid.UUID) -> Optional[Post]:
        return self.session.query(Post).filter(Post.id == post_id).first()

    def get_all(self, skip: int = 0, limit: int = 20) -> List[Post]:
        return (
            self.session.query(Post)
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_owner(self, owner_id: uuid.UUID) -> List[Post]:
        return (
            self.session.query(Post)
            .filter(Post.owner_id == owner_id)
            .order_by(Post.created_at.desc())
            .all()
        )

    def mark_embedded(self, post_id: uuid.UUID) -> None:
        post = self.get_by_id(post_id)
        if post:
            post.has_embedding = True
            self.session.commit()

    def delete(self, post_id: uuid.UUID, owner_id: uuid.UUID) -> bool:
        """Only deletes if owner_id matches — prevents deleting someone else's post."""
        post = self.get_by_id(post_id)
        if not post or post.owner_id != owner_id:
            return False
        self.session.delete(post)
        self.session.commit()
        return True