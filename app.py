from flask import redirect, render_template, Flask, request, jsonify, session, url_for
from models import db, User, Goal, Progress, Skill
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os

# Configure application
app = Flask(__name__)

app.secret_key = os.urandom(24)  # Generates a secure random key

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skillchronicle.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

# Initialize database
db.init_app(app)

# Create tables (run this only once)
with app.app_context():
    db.create_all()


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

# Index route


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            # Check for missing form fields
            if not username or not password:
                return "Please fill in all the fields."

            # Query the user from the database
            user = User.query.filter_by(username=username).first()

            # Check if user exists and password is correct
            if user and check_password_hash(user.password, password):
                session['username'] = user.username  # Save the session for the user
                session['user_id'] = user.id  # Save the user's ID in the session
                return redirect('/')
            else:
                return "Invalid username or password."
        except Exception as e:
            print(f"Error: {e}")  # Output error in the terminal
            return f"There was an error with your request: {e}"  # Display more specific error
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            # Print the values being received
            print(f"Received username: {username}, email: {email}")

            # Check for missing form fields
            if not username or not email or not password:
                return "Please fill in all the fields."

            # Hash the password
            hashed_password = generate_password_hash(password)

            # Create a new user
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()  # Commit to the database
            return redirect('/')
        except Exception as e:
            print(f"Error: {e}")  # Output error in the terminal
            return f"There was an error with your request: {e}"  # Display more specific error
    return render_template('register.html')


@app.route('/add_goal', methods=['GET', 'POST'])
@login_required
def add_goal():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        user_id = session.get('user_id')  # Use session to get the user_id

        if not title:
            return render_template('add_goal.html', error="Title is required.")

        new_goal = Goal(title=title, description=description, user_id=user_id)
        try:
            db.session.add(new_goal)
            db.session.commit()
            return redirect("/view")  # Redirect to the view page after adding the goal
        except Exception as e:
            db.session.rollback()
            return f"There was an error adding the goal: {str(e)}"
    return render_template('add_goal.html')

# Route to add progress for a skill


@app.route('/add_skill', methods=['GET', 'POST'])
@login_required
def add_skill():
    if request.method == 'POST':
        try:
            title = request.form['title']
            if not title:
                return render_template('add_skill.html', error="Title is required.")

            skill_description = request.form['description']
            user_id = session.get('user_id')  # Use session to get the user_id
            # Create a new skill entry
            new_skill = Skill(
                name=title,
                description=skill_description,
                user_id=user_id
            )
            db.session.add(new_skill)
            db.session.commit()  # Commit to the database
            return redirect('/view')  # Redirect to the view page after adding the skill
        except Exception as e:
            print(f"Error: {e}")  # Output error in the terminal
            return "There was an error with your request."

    return render_template('add_skill.html')

# Route to add progress for a goal


@app.route('/add_progress', methods=['GET', 'POST'])
@login_required
def add_progress():
    if request.method == 'POST':
        try:
            progress_detail = request.form['progress_detail']
            goal_id = request.form['goal_id']
            if not progress_detail:
                return render_template('add_progress.html', error="Details required.")

            current_date = datetime.now()  # Get the current date and time
            # Create a new progress entry
            user_id = session.get('user_id')

            new_progress = Progress(
                description=progress_detail,
                goal_id=goal_id,
                date=current_date,
                user_id=user_id  # Assign the date
            )
            db.session.add(new_progress)
            db.session.commit()  # Commit to the database
            return redirect('/view')  # Redirect to the view page after adding the progress
        except Exception as e:
            print(f"Error: {e}")  # Output error in the terminal
            return "There was an error with your request."
    return render_template('add_progress.html')


# Route to view all data
@app.route('/view')
@login_required
def view_data():
    user_id = session.get('user_id')  # Get the logged-in user's ID
    goals = Goal.query.filter_by(user_id=user_id).all()
    progresses = Progress.query.filter_by(user_id=user_id).all()
    skills = Skill.query.filter_by(user_id=user_id).all()
    return render_template('view.html', goals=goals, progresses=progresses, skills=skills)

# Route to logout


@app.route('/logout')
@login_required
def logout():
    # Clear the session to log out the user
    session.clear()  # logged-in user's ID and username cleared
    return redirect('/login')


# Run the app
if __name__ == '__main__':
    app.run(debug=True)

''' To generate the file
OpenAI ChatGPT was used with a lot of prompts.
A lot of bugs needed to get solved.

Github Co-pilot was used to resolve some issues in VS Code including
"Module not found," setting the path variable, python interpreter, etc.
The style50 button on CS50's codespace was useful'''
