from . import auth
from flask import render_template
from .forms import LoginForm, RegistrationForm
from ..models import User
from flask_login import login_user, login_required, current_user, logout_user
from flask import request, url_for, redirect, flash
from .. import db
import random
from ..email import send_email


@auth.before_app_request
def before_request():
    """
    This function is registered as a `before_app_request` handler,
    meaning it will be executed before each incoming request.
    """

    # Check if the current user is authenticated (logged in).
    if current_user.is_authenticated:

        # Call the `ping()` method on the current user object,
        # which updates the user's last seen timestamp.
        current_user.ping()

        # If the user is not yet confirmed (email verification pending),
        # and the current request is not related to the 'auth' blueprint
        # (user authentication and account management),
        # and the current request is not for a static file,
        if not current_user.confirmed \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':

            # Redirect the user to the 'unconfirmed' endpoint
            # within the 'auth' blueprint, which typically displays
            # a message indicating that the user's account is unconfirmed.
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():

    # Check if the user is anonymous or already confirmed
    if current_user.is_anonymous or current_user.confirmed:

        # If anonymous or already confirmed, redirect to the main index page
        return redirect(url_for('main.index'))

    # If not anonymous and not confirmed, render the 'unconfirmed.html'
    # template
    return render_template('auth/unconfirmed.html')


@auth.route('/', methods=['GET', 'POST'])
def login():
    # Check if the user is already authenticated (logged in)
    if current_user.is_authenticated:
        # Redirect to the main index page
        return redirect(url_for('main.index'))

    form = LoginForm()  # Create an instance of the LoginForm class

    # Check if the form has been submitted and passes validation
    if form.validate_on_submit():
        # Retrieve the user from the database based on the entered email
        user = User.query.filter_by(email=form.email.data.lower()).first()

        # Check if the user exists and the entered password is correct
        if user is not None and user.verify_password(form.password.data):
            login_user(user, True)   # Log in the user

            # Get the 'next' URL parameter from the request
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                # Set the 'next' URL to the main index page if not provided or
                # not valid
                next = url_for('main.index')
            return redirect(next)  # Redirect to the 'next' URL

        # Display an error message for invalid username or password
        flash('Invalid username or password.')

    # Render the login template, passing the form object
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    # Logs out the user
    logout_user()

    # Displays a flash message to indicate successful logout
    flash('You have been logged out.')

    # Redirects the user to the login page
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def register():
    # Create an instance of the RegistrationForm
    form = RegistrationForm()

    if form.validate_on_submit():
        # Generate a unique username using the first 5 characters of the email
        username = ''.join(random.choice(
            form.email.data[:5]) for _ in range(len(form.email.data[:5])))

        # Create a new User object with the submitted form data
        user = User(
            email=form.email.data.lower(),
            username=username,
            password=form.password.data)

        # Add the user to the database session and commit the changes
        db.session.add(user)
        db.session.commit()

        # Generate a confirmation token for the user
        token = user.generate_confirmation_token()

        # Send a confirmation email to the user's email address
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)

        # Flash a message to indicate that a confirmation email has been sent
        flash('A confirmation email has been sent to you by email.')

        # Redirect the user to the login page
        return redirect(url_for('auth.login'))

    # Render the signup.html template with the registration form
    return render_template('auth/signup.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    # Check if the user is already confirmed
    if current_user.confirmed:

        # Redirect to the main index page
        return redirect(url_for('main.index'))

    # Attempt to confirm the user's account using the provided token
    if current_user.confirm(token):
        db.session.commit()  # Commit the changes to the database

        # Display a success message
        flash('You have confirmed your account. Thanks!')
    else:
        # Display an error message
        flash('The confirmation link is invalid or has expired.')

    return redirect(url_for('main.index'))  # Redirect to the main index page


@auth.route('/confirm')
@login_required
def resend_confirmation():
    # Generate a new confirmation token for the current user
    token = current_user.generate_confirmation_token()

    # Send a confirmation email to the user's email address
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)

    # Display a flash message to the user
    flash('A new confirmation email has been sent to you by email.')

    # Redirect the user to the index page of the main blueprint
    return redirect(url_for('main.index'))
