# SkillChronicle: A Personal Learning Tracker
#### Video Demo:  https://youtu.be/01fQq6_JEEE

SkillChronicle is a web-based application designed to help users set, track, and achieve their learning goals. Whether you're learning a new language, mastering coding, or pursuing any other skill, SkillChronicle provides an organized way to manage your progress.

## Features:
- **User Authentication**: Secure system to register, login, and logout.
- **Goal Management**: Add learning goals.
- **Progress Tracking**: Log progress updates with notes.
- **SKill List**: Note skills with details.
- **View**: View goals, progress details, and skill list of the logged in user.

## Project Structure:
- `app.py`: Main application file containing routes and logic.
- `models.py`: Defines database schemas for users, goals, skills, and progress logs.
- `templates/`: Contains HTML templates for the frontend.
- `static/`: Contains the CSS file for styling the app.
- `instance/`: Contains the SQLite3 database file, instance.db for storing data.
- `venv/`: Contains the virtual environment for the project, isolating dependencies and managing Python packages.
- `flask_session/`: Automatically stores the session data on the filesystem.
- `requirements.txt`: Lists dependencies required for the application.
- `README.md`: This page that describes the whole project.

## Design Choices:
- **Framework**: Flask was chosen for its simplicity and lightweight design, aligning well with the project’s scope. And because I just learned this microframework from CS50!
- **Database**: SQLite3 provides a compact and efficient solution for local development.
- **Frontend**: HTML and CSS was used for the user-friendly interface.

## Setup Instructions:
1. Clone the repository: `git clone <repo-url>`
2. Navigate to the project directory: `cd SkillChronicle`
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

## app.py

The app.py file serves as the central hub of the SkillChronicle application. It is responsible for configuring and orchestrating the app's backend logic and managing user interactions. Below is an overview of its key functions:

1. Application Setup and Configuration
- Flask Initialization: Initializes the Flask application and sets up a secure secret key for session management.
- Session Configuration: Configures Flask sessions to use the filesystem instead of cookies, ensuring secure and temporary session storage.
- Database Integration: Integrates the SQLite database using SQLAlchemy and initializes it with models defined in models.py.

2. User Authentication
- Login Management: Provides a /login route to authenticate users based on their credentials. Valid credentials establish a session for the user.
- Registration: Offers a /register route to create new user accounts. Passwords are securely hashed before storage.
- Logout: Implements a /logout route to clear user session data and redirect to the login page.
- Access Control: Implements a login_required decorator to restrict access to certain routes for authenticated users only.

3. CRUD Operations for Goals, Skills, and Progress
- Add New Goals: The /add_goal route allows logged-in users to create goals with a title and description, linked to their user account.
- Add New Skills: The /add_skill route lets users define skills with a name and description.
- Track Progress: The /add_progress route enables users to log progress updates tied to specific goals.

4. Data Display
- View Data: The /view route fetches and displays goals, skills, and progress entries associated with the logged-in user.
- Dynamic Templates: Uses Jinja2 templates (e.g., view.html, add_goal.html) to dynamically render data and forms for user interaction.

5. Error Handling
- Captures and handles exceptions gracefully during database operations, ensuring the app remains user-friendly and informative when issues arise.

6. Utility Functions
- Session Management: Stores and retrieves user-specific data (e.g., user_id, username) in session variables.
- Reusable Decorators: The login_required decorator simplifies the enforcement of authentication checks on protected routes.

7. Local Development
- Runs the Flask application locally with debug mode enabled, streamlining development by providing detailed error messages and live code reloading.

## models.py

The models.py file defines the database structure and its relationships using SQLAlchemy. It acts as the blueprint for the database by specifying the models (tables) and their attributes (columns) in an object-oriented way. Here's what it does in detail:

### Overview of models.py

1. SQLAlchemy Initialization:
- The db object is initialized as an instance of SQLAlchemy, allowing interaction with the database.

2. Defining Models:
- Models are Python classes that map to database tables.
- Each class corresponds to a table, and each class attribute represents a column in that table.

### Models Defined in models.py

1. User Model:
- Represents the users of the application.
- Attributes:
   - id: A unique identifier for each user (Primary Key).
   - username: The unique username of the user.
   - email: The user's email address.
   - password: A hashed version of the user's password.
- Purpose:
   - Used to store and manage user authentication and identification.

2. Goal Model:
- Represents the goals created by users.
- Attributes:
   - id: A unique identifier for each goal (Primary Key).
   - title: The title or name of the goal.
   - description: A detailed description of the goal.
- Purpose:
   - Stores data related to the goals users want to track.

3. Progress Model:
- Represents progress updates for specific goals.
- Attributes:
   - id: A unique identifier for each progress entry (Primary Key).
   - date: The date the progress was logged.
   - description: A brief summary of the progress made.
- Purpose:
   - Tracks incremental progress for goals.

4. Skill Model:
- Represents the skills users want to track or improve.
- Attributes:
   - id: A unique identifier for each skill (Primary Key).
   - name: The name of the skill.
   - description: An optional description providing additional details about the skill.
- Purpose:
   - Stores data about specific skills users are tracking or improving.

### Role in the Application

- The models.py file is crucial for defining how data is stored, and retrieved within the application.
- It works alongside Flask's database configuration (defined in app.py) to ensure the data model is consistent and accessible.
- Relationships between users, goals, progress, and skills are defined here to maintain data integrity and enable efficient queries.

## Templates Directory

The `templates/` directory contains all the HTML files used for rendering the front-end of the application. These files use Jinja2 templating syntax, allowing dynamic content to be injected from Flask routes. Below is a breakdown of the HTML pages and their purposes:

1. **`base.html`**
   - **Purpose**: Serves as the main layout template for the application.
   - **Features**:
     - Includes a common structure like the `<head>` section, navigation bar, and footer.
     - Other templates extend this file to maintain consistent design across pages.

2. **`index.html`**
   - **Purpose**: Acts as the home page after users log in.
   - **Features**:
     - Displays a personalized welcome message or dashboard content.
     - Links to other functionalities like adding goals, skills, or viewing progress.

3. **`login.html`**
   - **Purpose**: Provides the interface for users to log in to the application.
   - **Features**:
     - Includes fields for entering the username and password.
     - Displays error messages if the login credentials are invalid.

4. **`register.html`**
   - **Purpose**: Allows new users to register for the application.
   - **Features**:
     - Contains fields for username, email, and password input.
     - Validates input and displays error messages for incomplete or invalid fields.

5. **`add_goal.html`**
   - **Purpose**: Provides a form to create a new goal.
   - **Features**:
     - Contains input fields for goal title and description.
     - Allows users to submit data, which is saved in the database.

6. **`add_skill.html`**
   - **Purpose**: Provides a form to add a new skill.
   - **Features**:
     - Includes input fields for the skill name and description.
     - Sends the data to the backend for storage.

7. **`add_progress.html`**
   - **Purpose**: Allows users to log progress for a specific goal.
   - **Features**:
     - Provides fields for entering progress details and associating it with a goal.
     - Sends data to the backend for storage.

8. **`view.html`**
   - **Purpose**: Displays an overview of the user's goals, skills, and progress.
   - **Features**:
     - Dynamically renders data fetched from the database.
     - Ensures only the logged-in user’s data is shown.

---

### Role of the Templates Directory
The `templates/` directory, combined with Flask’s routing and Jinja2 templating, ensures a seamless integration between the backend logic and the user interface. Each HTML page is designed to handle a specific functionality of the app, making it user-friendly and intuitive.

SkillChronicle is a beginner-friendly project showcasing the fundamentals of web development while helping users track their skills and progress.
