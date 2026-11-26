import re
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import Users
from app.extension import db

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+$")
USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_.-]{3,20}$")

auth_bp = Blueprint('auth', __name__)

def validate_auth(data, is_signup=True):

    if not isinstance(data, dict) or not data:
        return None, (jsonify({
            "error": "Invalid input data. Expected a non-empty JSON object."
        }), 400)

    email = data.get('email')
    password = data.get('password')

    if not isinstance(email, str) or not isinstance(password, str):
        return None, (jsonify({
            "error": "Invalid email or password. Expected string values."
        }), 400)
    
    email = email.strip().lower()

    if not EMAIL_REGEX.match(email):
        return None, (jsonify({
            "error": "Invalid email format."
        }), 400)

    if not password or not password.strip():
        return None, (jsonify({
            "error": "Please provide a non-empty value for the password."
        }), 400)

    cleaned_data = {
        "email": email,
        "password": password
    }

    if is_signup:
        username = data.get('username')

        if not isinstance(username, str):
            return None, (jsonify({
                "error": "Invalid username. Expected a string value."
            }), 400)

        username = username.strip()
        if not USERNAME_REGEX.match(username):
            return None, (jsonify({
                "error": "Invalid username format. Username must be 3-20 characters long and can contain letters, numbers, underscores, hyphens, and periods."
            }), 400)

        if len(password) < 8:
            return None, (jsonify({
                "error": "Password must be at least 8 characters long."
            }), 400)

        if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return None, (jsonify({
                "error": "Password must contain at least one letter and one number and special character."
            }), 400)

        cleaned_data["username"] = username

    return cleaned_data, None


@auth_bp.route('/signup', methods=['POST'])
def signup():

    if not request.is_json:
        return jsonify({
            "error": "Missing JSON in request"
        }), 415

    cleaned, error = validate_auth(request.get_json(silent=True), is_signup=True)

    if error:
        return error

    existing_user = Users.query.filter_by(username=cleaned['username'], email=cleaned['email']).first()

    if existing_user:
        return jsonify({
            "error": "User already exists."
        }), 409

    hashed_password = generate_password_hash(cleaned['password'])
    
    new_user = Users(
        username = cleaned['username'],
        email = cleaned['email'],
        password = hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "msg": "User created successfully"
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():

       if not request.is_json:
            return jsonify({
                "error": "Missing JSON in request"
            }), 415

       cleaned, error = validate_auth(request.get_json(silent=True), is_signup=False)

       if error:
           return error

       user = Users.query.filter_by(email=cleaned['email']).first()

       if not user:
           return jsonify({
               "error": "Invalid email or password."
           }), 401

       if not check_password_hash(user.password, cleaned['password']):
          return jsonify({
              "error": "Invalid email or password."
          }), 401

       token = create_access_token(identity=str(user.id))

       return jsonify({
           "msg": "Login successfully.",
           "token": token
       }), 200

@auth_bp.route('/logout', methods=['POST'])