from flask_app import app
from flask_app.models.users import User
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def login_reg():
    return render_template('index.html')

@app.route('/register', methods = ['POST'])
def new_user():
    if not User.validate_user(request.form):
        return redirect('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['passw'])
        print('Hash:', pw_hash)
        data = {
            'firstn': request.form['firstn'],
            'lastn': request.form['lastn'],
            'email': request.form['email'],
            'passw': pw_hash,
            'confirm_pw': pw_hash
        }
        user = User.create_user(data)
        print('New user: ', user)
        session['user_id'] = user
        return redirect('/accountshow')

@app.route('/login', methods = ['POST'])
def login_user():
    data = {
        "email": request.form['email']}
    db_user = User.login_user(data)
    if not db_user:
        flash("Invalid login credentials!")
        return redirect('/')
    if not bcrypt.check_password_hash(db_user.password, request.form['passw']):
        flash("Invalid login credentials!")
        return redirect('/')
    session['user_id'] = db_user.id
    return redirect('/accountshow')


@app.route('/accountshow')
def account_page():
    if 'user_id' in session:
        acct_user = User.get_user(session['user_id'])
        return render_template('account_page.html', acct_user = acct_user)
    return redirect('/')

@app.route('/logout')
def logout_user():
    session.clear()
    print('session is cleared!')
    return redirect('/')


