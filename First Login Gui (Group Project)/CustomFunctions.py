# py LIB #
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import mysql.connector
from email.message import EmailMessage
import ssl
import smtplib
import secrets

def db_connect():
    db = mysql.connector.connect(
    host ='localhost',
    user='root',
    password ='1234',
    database ='project_database'
    ) 
    return db
###########SQL SECTION#############
def describe():
    db = db_connect()
    c = db.cursor()

    c.execute('describe `sign up`')

    a = c.fetchall()

    db.close()

    print(a)
# describe()
###########SQL SECTION#############
def db_select_login_id(username):
    db = db_connect()
    c = db.cursor()

    query = 'select login_id from `log in` where login_username=%s'
    tmp = (username,)
    c.execute(query, tmp)

    login_id = c.fetchone()

    try:
        return login_id[0]
    except:
        return login_id

def db_select_signup_id(email):
    db = db_connect()
    c = db.cursor()

    query = 'select signup_id from `sign up` where email=%s'
    tmp = (email,)
    c.execute(query, tmp)

    signup_id = c.fetchone()

    return signup_id[0]

def db_select_all_email():
    db = db_connect()
    c = db.cursor()

    query = 'select email from `sign up`'

    c.execute(query)

    emails = c.fetchall()

    db.commit()
    db.close()

    return emails

def db_select_one_email(username):
    
    login_id = db_select_login_id(username)
    db = db_connect()
    c = db.cursor()

    if login_id != None:
        query = 'select email from `sign up` where login_id=%s'
        tmp = (login_id,)
        c.execute(query, tmp)

        emails = c.fetchone()

        db.commit()
        db.close()

        return emails[0]
    else:
        return None

def db_select_all_username():
    db = db_connect()
    c = db.cursor()

    query = 'select login_username from `log in`'

    c.execute(query)

    usernames = c.fetchall()

    db.commit()
    db.close()

    return usernames

def create_logs(username_or_email, Log_Name):
    
    id = None

    login_id = db_select_login_id(username_or_email)
    id = login_id
    
    if id == None:
        signup_id = db_select_signup_id(username_or_email)
        id = signup_id


    db = db_connect()
    c = db.cursor()

    query = 'INSERT INTO `Log history` (Log_Name, Signup_ID, login_ID) VALUES(%s,%s,%s)'
    tmp = (Log_Name, id, id)

    c.execute(query,tmp)
    db.commit()
    db.close()        

def db_update_wLogin_id(table_name, column_name, column_value, username_or_email):
    id = None

    login_id = db_select_login_id(username_or_email)
    id = login_id
    
    if id == None:
        signup_id = db_select_signup_id(username_or_email)
        id = signup_id
    
    db = db_connect()
    c = db.cursor()

    query = 'update ' + table_name + ' set ' + column_name + ' = %s where login_id = %s'
    tmp =(column_value , id)

    try:
        c.execute(query, tmp)
    except:
        return print('error column does not exist')

    db.commit()
    db.close()

##################################################
###############  normal functions  ###############
##################################################

def FocusedIn(event, name):
    if name.get() == 'Username':
        name.delete(0, END)
    if name.get() == 'Email':
        name.delete(0, END)
    if name.get() == 'Password':
        name.delete(0, END)
    if name.get() == 'Confirm Password':
        name.delete(0, END)

def FocusedOut(event, name, id):
    if name.get() == '' and id == 0:
        name.insert(0, 'Username')
    if name.get() == '' and id == 1:
        name.insert(0, 'Email')
    if name.get() == '' and id == 2:
        name.insert(0, 'Password')
    if name.get() == '' and id == 3:
        name.insert(0, 'Confirm Password')
