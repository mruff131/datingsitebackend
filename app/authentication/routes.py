from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

# imports for flask login 
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])  # get user info and submit/post it to db
def signup():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            print("hello")

            email = form.email.data
            password = form.password.data
            
            print(email, password)

            user = User(email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'User-created')
            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_up.html', form=form) 



@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()   # from the requests on this form we are checking to see who has access

    try:
        if request.method == 'POST' and form.validate_on_submit():
            # sets email & pw equal to data from form
            email = form.email.data 
            password = form.password.data
            print(email, password) # only for debugging purposes

            logged_user = User.query.filter(User.email == email).first() # checks database for email

            if logged_user and check_password_hash(logged_user.password, password):  # pulls pw and unhashes to check for match
                login_user(logged_user)
                flash('You have successfully logged into your account.')
                return redirect(url_for('site.profile'))
            else:
                flash('The password or email you entered is incorrect.')

    except:
        raise Exception('Invalid form data, doublecheck your form.')
    return render_template('sign_in.html', form = form)
    

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))
    




