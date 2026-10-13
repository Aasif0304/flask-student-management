import os
from flask import Flask
from flask_migrate import Migrate
from sqlalchemy.engine import URL

from routes.student_routes import student_routes
from routes.fees_routes import fees_routes
from routes.auth_routes import auth_routes
from models.migration_models import db, Student, Fee, User
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)
app = Flask(__name__)

database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "student_management"),
)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return "Student Management System"


app.register_blueprint(student_routes)
app.register_blueprint(fees_routes)
app.register_blueprint(auth_routes)


if __name__ == "__main__":
    app.run(debug=True)