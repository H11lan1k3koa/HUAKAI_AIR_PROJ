#import regular expressions for pattern matching, text manipulation for email checking
import re
#request - grab data from client, jsonify - turn python into json format (for sending btwn server & webpage)
from flask import Flask, request, jsonify
#for password schema
from password_validator import PasswordValidator
from passlib.hash import bcrypt

#lib / bridge for postgresql
import psycopg2 
from dotenv import load_dotenv
import os

#create instance of Flask class
app = Flask(__name__)

##password schema##
password_schema = PasswordValidator()
password_schema \
    .min(12) \
    .has().uppercase() \
    .has().lowercase() \
    .has().digits() \
    .has().symbols()

# Load environment variables from .env
load_dotenv()
# Fetch variables
DATABASE_URL = os.getenv("DATABASE_URL")
#connect to db
conn = psycopg2.connect(DATABASE_URL)

#Cursor object that lets you work with sql commands
cur=conn.cursor()

#==================##**SPRINT1 T2**##===============
#backend reg w/ input validation, verify info is in valid format, pw strength & unique

#creates 'register' route for post requests
@app.route('/register', methods=['POST'])

#define register function
def register():
    data = request.json
    if not data:
        return jsonify({'Error': 'Missing request'}), 400
    
    ##check if required fields have input##
    required_fields = ['first_name', 'last_name', 'email', 'password', 'username', 'dob', 'mobile']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'Error': f'{field} is required'}), 400

    ##validate email format##
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, data['email']):
        return jsonify({'Error': 'Invalid email format'}), 400 
    
    ##check password complexity##
    if not password_schema.validate(data['password']):
        return jsonify({'Error': 'Password must be a minimum of 12 characters and include at least one l upper case, 1 lower case, 1 number, and 1 special character'}), 400

    ##password hash & salt##
    password_hash = bcrypt.hash(data['password'])

    ##check if user exists##
    cur.execute("SELECT USER_ID FROM USERS WHERE EMAIL = %s OR USERNAME = %s",
                (data['email'], data['username']))
    if cur.fetchone():
        return jsonify({'Error': 'User already exists'}), 409
    
    #replace plaintext pw w/ pw hash
    password = password_hash

    cur.execute(
        """
        INSERT INTO USERS 
        (last_name, first_name, dob, password, username, email, mobile) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            data['last_name'],
            data['first_name'],
            data['dob'],
            password_hash,
            data['username'],
            data['email'],
            data['mobile']
        )
    )
    conn.commit()

    return jsonify({'message': 'Your account was successfully created'}), 201





