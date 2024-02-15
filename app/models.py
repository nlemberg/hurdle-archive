from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))

    user_games: so.WriteOnlyMapped['UserGame'] = so.relationship(
        back_populates='player')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_games(self):
        return (
            sa.select(UserGame)
            # .join(Game)
            .where(UserGame.user_id == self.id)
            .order_by(UserGame.id)
        )


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Game(db.Model):
    __tablename__ = 'games'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    solution: so.Mapped[str] = so.mapped_column(sa.String(5))

    user_games: so.WriteOnlyMapped['UserGame'] = so.relationship(
        back_populates='game_played')

    def __repr__(self):
        return f'<Game {self.solution}>'


class UserGame(db.Model):
    __tablename__ = 'user_games'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('users.id'), index=True)
    game_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('games.id'), index=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(10))
    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))

    player: so.Mapped[User] = so.relationship(back_populates='user_games')
    game_played: so.Mapped[Game] = so.relationship(back_populates='user_games')

    def __repr__(self):
        return f'<UserGame {self.status}>'

############################################################################

# from datetime import datetime, timezone
# from typing import Optional
# import sqlalchemy as sa
# import sqlalchemy.orm as so
# from app import db


# class User(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)
#     username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
#                                                 unique=True)
#     password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
#     created_at: so.Mapped[datetime] = so.mapped_column(
#         index=True, default=lambda: datetime.now(timezone.utc))

#     userGames: so.WriteOnlyMapped['userGame'] = so.relationship(
#         back_populates='user')

#     def __repr__(self):
#         return '<User {}>'.format(self.username)


# class Game(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)
#     solution: so.Mapped[str] = so.mapped_column(sa.String(5))

#     userGames: so.WriteOnlyMapped['userGame'] = so.relationship(
#         back_populates='game')

#     def __repr__(self):
#         return '<Game {}>'.format(self.solution)


# class UserGame(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)
#     user_id: so.Mapped[int] = so.mapped_column(
#         sa.ForeignKey(User.id), index=True)
#     game_id: so.Mapped[int] = so.mapped_column(
#         sa.ForeignKey(Game.id), index=True)
#     status: so.Mapped[str] = so.mapped_column(sa.String(10))
#     played_at: so.Mapped[datetime] = so.mapped_column(
#         index=True, default=lambda: datetime.now(timezone.utc))

#     user: so.Mapped[User] = so.relationship(back_populates='userGames')
#     game: so.Mapped[Game] = so.relationship(back_populates='userGames')

#     def __repr__(self):
#         return '<UserGame {}>'.format(self.status)
