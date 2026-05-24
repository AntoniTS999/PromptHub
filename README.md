# PromptHub

📌 PromptHub

PromptHub is a platform for storing, discovering, and sharing AI prompts.

🚀 Features
Superuser Controls
Only a superuser can manage categories (create, update, delete), and can also delete any prompt or user account. This ensures full administrative control and content moderation.
User Profile Management
Users can access a personal panel from the sidebar to update or delete their profile.
Prompt Management
Authors can update their own prompts. Prompts can be deleted either by their author or by a superuser.
Ratings System
Users can rate prompts only from the detailed prompt view. Each user can rate a given prompt only once to maintain data integrity.
🛠️ Technologies Used
Django 6.0.5
Python 3.12+
Bootstrap 4
SQLite
Django Crispy Forms
Class-Based Views (CBV)
Custom User Model (AbstractUser)
Django ORM
Pagination
Unit Tests
⚙️ Setup Instructions

Follow these steps to run the project locally:

1. Clone the repository
git clone <repository_url>
cd prompthub
2. Create and activate virtual environment
🐧 macOS / Linux:
python -m venv env
source env/bin/activate
🪟 Windows (CMD / PowerShell):
python -m venv env
env\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Apply database migrations
python manage.py migrate
5. Load test data (optional)

If you want to run the project with sample data for testing purposes, you can load the provided JSON fixture:

python manage.py loaddata data.json

⚠️ Make sure the file data.json is located in your project directory or a valid fixtures path.

6. Create a superuser
python manage.py createsuperuser

⚠️ Default development credentials (only for local testing):
Username: admin
Password: 123456789

7. Run development server
python manage.py runserver
🌐 Access the app

Open in browser:

http://127.0.0.1:8000/
🔐 Security Notes
Only superusers can manage categories.
Users can only edit or delete their own profiles.
Authors can manage their own prompts.
Both authors and superusers can delete prompts.
Ratings are restricted to one per user per prompt.
Ratings are only available from the prompt detail page.
📌 Notes

This project uses a role-based access system to ensure secure and structured interaction between users, authors, and administrators.