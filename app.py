from flask import (
Flask,
render_template,
request,
redirect,
session
)

import sqlite3
import pandas as pd
import joblib
import os


app = Flask(__name__)

app.secret_key="SOS"


DATABASE="database/users.db"



os.makedirs(
"database",
exist_ok=True
)


def init_db():

    conn=sqlite3.connect(
    DATABASE
    )

    cursor=conn.cursor()



    cursor.execute(

'''
CREATE TABLE IF NOT EXISTS users(

id INTEGER PRIMARY KEY,

username TEXT,

password TEXT

)

'''

)


    cursor.execute(

'''
CREATE TABLE IF NOT EXISTS incidents(

id INTEGER PRIMARY KEY,

username TEXT,

incident TEXT,

severity TEXT,

response INTEGER

)

'''

)

    conn.commit()

    conn.close()


init_db()


model=joblib.load(
"models/emergency_model.pkl"
)



@app.route('/')

def home():

    return render_template(
    "index.html"
    )




@app.route('/signup',

methods=['POST'])

def signup():

    username=request.form[
    'username'
    ]

    password=request.form[
    'password'
    ]


    conn=sqlite3.connect(
    DATABASE
    )

    cursor=conn.cursor()


    cursor.execute(

"INSERT INTO users(username,password) VALUES(?,?)",

(username,password)

)


    conn.commit()

    conn.close()


    return redirect('/')




@app.route('/login',

methods=['POST'])

def login():

    username=request.form[
    'username'
    ]


    password=request.form[
    'password'
    ]


    conn=sqlite3.connect(
    DATABASE
    )

    cursor=conn.cursor()


    cursor.execute(

"SELECT * FROM users WHERE username=? AND password=?",

(username,password)

)


    user=cursor.fetchone()


    if user:

        session['username']=username

        return redirect(
        '/dashboard'
        )


    return "Invalid"




@app.route('/dashboard')

def dashboard():

    df=pd.read_excel(

"datasets/emergency_data.xlsx"

)


    total=len(df)


    return render_template(

"dashboard.html",

total=total

)



@app.route('/predict',

methods=['POST'])

def predict():

    incident=int(

request.form[
'incident'
]

)


    age=int(

request.form[
'age'
]

)


    response=int(

request.form[
'response'
]

)


    nearby=int(

request.form[
'nearby'
]

)



    prediction=model.predict(

[[

incident,

age,

response,

nearby

]]

)


    severity=prediction[0]


    return render_template(

"dashboard.html",

prediction=severity

)



@app.route('/logout')

def logout():

    session.clear()

    return redirect('/')



if __name__=="__main__":

    app.run(

debug=True

)