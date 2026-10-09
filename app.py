from flask import Flask
from routes.student_routes import student_routes
from routes.fees_routes import fees_routes

app = Flask(__name__)


@app.route("/")
def home():
    return "Student Management System"


app.register_blueprint(student_routes)
app.register_blueprint(fees_routes)


if __name__ == "__main__":
    app.run(debug=True)