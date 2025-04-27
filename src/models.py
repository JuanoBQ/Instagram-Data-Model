from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Relaciones
    # Follower
    follower: Mapped[List["Follower"]] = relationship(
        "Follower", back_populates="user")
    # Post
    post: Mapped[List["Post"]] = relationship(
        "Post", back_populates="user", cascade="all, delete-orphan")
    # Comment
    comment: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active
        }


class Follower(db.Model):
    __tablename__ = 'follower'

    user_from_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_to_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="follower")

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }


class Media(db.Model):
    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }


class Post(db.Model):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_to_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="post")

    # Media
    media: Mapped[List["Media"]] = relationship(
        "Media", back_populates="post", cascade="all, delete-orphan")
    # Comment
    comment: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "user_to_id": self.user_to_id
        }


class Comment(db.Model):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(50), nullable=False)
    autor_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="comment")
    post: Mapped["Post"] = relationship("Post", back_populates="comment")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "autor_id": self.autor_id,
            "post_id": self.post_id
        }
