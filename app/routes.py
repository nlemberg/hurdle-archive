from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, GameForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from sqlalchemy.sql import not_
from app.models import User, Game, UserGame


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    games = [
        {'id': 233, 'status': 'won'},
        {'id': 555, 'status': 'lost'}
    ]
    return render_template('user.html', user=user, games=games)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/game_<game_id>', methods=['GET', 'POST'])
@login_required
def game(game_id):
    game = db.first_or_404(sa.select(Game)
                           .where(Game.id == game_id)
                           .filter(
        not_(sa.select(UserGame)
             .where(UserGame.user_id == current_user.id)
             .where(UserGame.game_id == game_id)
             .exists())
    ))

    form = GameForm()

    if form.validate_on_submit():

        if form.guess.data == game.solution:
            game_played = UserGame(
                game_id=game_id, user_id=current_user.id, status='won')
            db.session.add(game_played)
            db.session.commit()
            flash('Congrats, you won!')
            return redirect(url_for('game', game_id=game.id))
        else:
            flash('Try again')

    return render_template('game.html', game=game, form=form)

# @app.route('/game_<game_id>', methods=['GET', 'POST'])
# @login_required
# def game(game_id):
#     game = db.first_or_404(sa.select(Game).where(Game.id == game_id))
#     attempts = 8

#     form = GameForm()
#     if attempts > 0:
#         if form.validate_on_submit():
#             attempts -= 1
#             if form.guess == game.solution:
#                 game_played = UserGame(
#                     game_id=game_id, user_id=current_user, status='won')
#                 db.session.add(game_played)
#                 db.session.commit()
#                 flash('Congrats, you won!')
#                 print(attempts)
#                 # return redirect(url_for('game', game_id=game.id))
#             else:
#                 flash('Try again')
#                 print(attempts)
#                 # return redirect(url_for('game', game_id=game.id))
#     else:
#         game_played = UserGame(
#             game_id=game_id, user_id=current_user, status='lost')
#         db.session.add(game_played)
#         db.session.commit()
#         flash("You're out of tries. Play another game!")
#         # return redirect(url_for('game', game_id=game.id))

#     return render_template('game.html', game=game, form=form, attempts=attempts)
