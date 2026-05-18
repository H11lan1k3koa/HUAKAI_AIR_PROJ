from flask import Flask, request, jsonify, session, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pyotp
import datetime, uuid, string

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

#lib / bridge for postgresql
import psycopg2 

from dotenv import load_dotenv
import os
# Load environment variables from .env
load_dotenv()
# Fetch variables
DATABASE_URL = os.getenv("DATABASE_URL")
# Connect to the database
conn = psycopg2.connect(DATABASE_URL)

#Cursor object that lets you work with sql commands
cur=conn.cursor()

#============##DATABASE SCHEMA##===============

#=======##**SPRINT1 T1**##=========================
#USERS table
cur.execute("""
            CREATE TABLE USERS(
            user_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
            last_name VARCHAR(50) NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            dob DATE NOT NULL,
            password VARCHAR(255) NOT NULL,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(255) NOT NULL,
            mobile TEXT NOT NULL)""")


#FLIGHTS table
cur.execute("""
            CREATE TABLE FLIGHTS(
            flight_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
            flight_num VARCHAR(20) NOT NULL,
            departure_city TEXT NOT NULL,
            departure_state TEXT NOT NULL,
            departure_country TEXT NOT NULL,
            departure_time TIMETZ NOT NULL,
            arrival_city TEXT NOT NULL,
            arrival_state TEXT NOT NULL,
            arrival_country TEXT NOT NULL,
            arrival_time TIMETZ NOT NULL,
            seats SMALLINT NOT NULL,
            price REAL NOT NULL,
            cancelled BOOL DEFAULT FALSE)""")

#PAYMENTS table
cur.execute("""
            CREATE TABLE PAYMENTS(
            payment_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
            pmt_datetime TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL,
            amount REAL NOT NULL,
            card_last_4 TEXT NOT NULL,
            card_type TEXT NOT NULL)""")

#AGENTS table
cur.execute("""
            CREATE TABLE AGENTS(
            agent_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            email VARCHAR(255) NOT NULL,
            start_date DATE NOT NULL)""")

#NOTIFICATIONS table
cur.execute("""
            CREATE TABLE NOTIFICATIONS(
            notif_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            user_id UUID REFERENCES USERS(USER_ID),
            email VARCHAR(255) NOT NULL,
            mobile TEXT NOT NULL,
            email_notification_successful BOOL DEFAULT FALSE,
            mobile_notification_successful BOOL DEFAULT FALSE)""")

#RESERVATIONS table
cur.execute("""
            CREATE TABLE RESERVATIONS(
            reservation_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
            user_id UUID REFERENCES USERS(USER_ID),
            flight_id UUID REFERENCES FLIGHTS(FLIGHT_ID),
            book_datetime TIMESTAMP NOT NULL,
            status TEXT NOT NULL,
            payment_id UUID REFERENCES PAYMENTS(PAYMENT_ID),
            agent_id UUID REFERENCES AGENTS(AGENT_ID))""")

