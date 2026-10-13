from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, Numeric, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(100), nullable=False)


class Fee(db.Model):
    __tablename__ = "fees"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(
        db.Integer,
        ForeignKey("students.id"),
        unique=True,
        nullable=True
    )
    total_fees = db.Column(Numeric(10, 2), nullable=False)
    paid_fees = db.Column(
        Numeric(10, 2),
        nullable=False,
        server_default="0"
    )
    pending_fees = db.Column(Numeric(10, 2), nullable=False)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(Text, nullable=False)
    role = db.Column(
        db.String(20),
        nullable=False,
        server_default="USER"
    )

    __table_args__ = (
        CheckConstraint(
            "role IN ('ADMIN', 'USER')",
            name="users_role_check"
        ),
    )