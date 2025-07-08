# users/views.py
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from companyblog import db
from companyblog.models import User, BlogPost
from companyblog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from companyblog.users.picture_handler import add_profile_pic

users = Blueprint('users',__name__)

# register
@users.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Thanks for registering! You can now log in.', 'success')
        return redirect(url_for('users.login'))
    
    # If POST with errors, flash each one
    if request.method == 'POST':
        for field_name, error_list in form.errors.items():
            field = getattr(form, field_name)
            for error in error_list:
                # e.g. "Password: Passwords must match!"
                flash(f"{field.label.text}: {error}", 'danger')
    
    return render_template('register.html',form=form)

# login
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # Only enter here if CSRF passes and fields all validate
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # 1) No such email
        if user is None:
            flash('No account found with that email. Please register first.', 'danger')
            return redirect(url_for('users.login'))

        # 2) Email exists but wrong password
        if not user.check_password(form.password.data):
            flash('Incorrect password. Please try again.', 'danger')
            return redirect(url_for('users.login'))

        # 3) Good credentials!  Log in and redirect
        login_user(user)
        flash('Logged in successfully!', 'success')
        next_page = request.args.get('next', '')
        if not next_page.startswith('/'):
            next_page = url_for('core.index')
        return redirect(next_page)

    # If they POSTed but failed WTForms validators (e.g. blank or bad email format)
    if request.method == 'POST':
        for field_name, error_list in form.errors.items():
            label = getattr(form, field_name).label.text
            for error in error_list:
                flash(f"{label}: {error}", 'danger')
        return redirect(url_for('users.login'))

    # GET — just show the form
    return render_template('login.html', form=form)



# logout
@users.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('core.index'))

# account (update UserForm)
@users.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated!')
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html', profile_image=profile_image,form=form)


# user's list of Blog posts
@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_posts.html',blog_posts=blog_posts,user=user)
