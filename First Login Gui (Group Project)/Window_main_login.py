# py LIB #
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import mysql.connector
from email.message import EmailMessage
import ssl
import smtplib
import secrets


# Wndows #
import Window_Register
import Window_ChangePass
import Window_Verification
import Window_Profile

# Login Functions #
import CustomFunctions

# MYsql Functions #
def db_connect():
    return CustomFunctions.db_connect()

db = db_connect()
mycursor = db.cursor()

query = 'delete from p_backup where b_date < now() - interval 30 DAY'

mycursor.execute(query)
db.commit()
db.close()

def hide():
    openeye.config(file='closeye.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)

def show():
    openeye.config(file='openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)

def FocusedIn(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)
        passwordEntry.config(show='*')

def FocusedOut(event):
    if passwordEntry.get() == '':
        passwordEntry.insert(0, 'Password')
        passwordEntry.config(show='')
        openeye.config(file = 'closeye.png')
        eyeButton.config(command = show)

def press_login():
    db = db_connect()
    c = db.cursor()

    login_id = CustomFunctions.db_select_login_id(usernameEntry.get())

    if usernameEntry.get() == 'Username' or passwordEntry.get() == 'Password':
        messagebox.showerror('Error', 'Fill All Entry First', parent = login)
    elif login_id == None:
        messagebox.showerror('Error', 'Username Does Not Exist', parent = login)
    else:
        query = 'select accountType from account_type where account_typeID = %s'
        tmp = (login_id,)

        c.execute(query, tmp)
        acc_type = c.fetchone()

        query = 'select login_password from `log in` where login_id = %s'
        tmp = (login_id,)

        c.execute(query, tmp)
        acc_password = c.fetchone()

        db.commit()
        db.close()

        if passwordEntry.get() == acc_password[0]:
            CustomFunctions.db_update_wLogin_id('login_state', 'logged_in', 1, usernameEntry.get())
            CustomFunctions.create_logs(usernameEntry.get(), "Logged In")
            if acc_type[0] == 'ADMIN':
                Window_Profile.Pwindow(login, usernameEntry.get(), 'ADMIN')
            else:
                Window_Profile.Pwindow(login, usernameEntry.get(), 'CLIENT')
        else:
            messagebox.showerror('Error', 'Incorrect Password', parent = login)

def press_create_account():
    Window_Register.register(login)

def pressed_forgot_password():
    Window_ChangePass.cp_window(login)

# Login Window Settings #
login = Tk()
login.geometry('990x660+50+50') #bg
login.resizable(0,0)
login.iconbitmap('two.ico')
login.title('Login Page')
bgImage=ImageTk.PhotoImage(file='Login.png') #picture file name here, send help joshhh
 
bgLabel = Label(login,image=bgImage)
bgLabel.place(x=0,y=0)
 
usernameEntry=Entry(login, width=25, font=('Microsoft Yahei UI Light', 14, 'bold'),bg = '#e6e6e6', bd=0, fg='black')
usernameEntry.place(x=580,y=257)
usernameEntry.insert(0, 'Username')
 
usernameEntry.bind('<FocusIn>', lambda event, name = usernameEntry: CustomFunctions.FocusedIn(event, name))
usernameEntry.bind('<FocusOut>', lambda event, name = usernameEntry, id = 0: CustomFunctions.FocusedOut(event, name, id))
 
passwordEntry=Entry(login, width =25, font=('Microsoft Yahei UI Light', 14, 'bold'),bg='#e1ecff',bd=0, fg='black')
passwordEntry.place(x=580,y=337)
passwordEntry.insert(0, 'Password')
 
passwordEntry.bind('<FocusIn>', lambda event: FocusedIn(event))
passwordEntry.bind('<FocusOut>', lambda event:FocusedOut(event))
 
openeye=PhotoImage(file = 'closeye.png') #openeye.png
eyeButton=Button(login,image=openeye, bd=0,activebackground = '#a6d9f2',cursor = 'hand2',bg='#e1ecff',command = show)
eyeButton.place(x=860, y=337)
 
forgetButton=Button(login,text = 'Forgot Password?', bd=0,bg='#ffffff',activebackground = '#e1ecff',cursor = 'hand2',font=('Microsoft Yahei UI Light', 9, 'bold') , fg='#224481', activeforeground='firebrick', command = lambda: pressed_forgot_password())
forgetButton.place(x=760, y=385)
 
loginButton=Button(login, text='Login', font=('Open Sans', 10, 'bold'), fg='white', bg='#224481', activebackground='grey' , activeforeground='black', cursor='hand2',bd=0,width=31, height=2,command= lambda: press_login())
loginButton.place(x=588,y=450)

signupLabel=Label(login, text='Dont have an account?', font=('Open Sans',9,'bold'), fg='black',bg='#ffffff')
signupLabel.place(x=598, y=530)
 
newaccountButton=Button(login, text='Create new one', font=('Open Sans', 9, 'bold underline'), fg='#224481', bg='#ffffff', activebackground='#bce9ff' , activeforeground='black', cursor='hand2', bd=0, command = lambda: press_create_account())
newaccountButton.place(x=735,y=530)

db = db_connect()
c = db.cursor()

query = 'select logged_in from login_state'

c.execute(query)
logged_in = c.fetchall()
count = None

for i in range(len(logged_in)):
    if logged_in[i][0] == 1:
        count = i+1

if count != None:
    db = db_connect()
    c = db.cursor()

    query = 'select login_username from `log in` where login_id = %s'
    tmp = (count,)

    c.execute(query, tmp)
    username = c.fetchone()

    query = 'select login_password from `log in` where login_id = %s'
    tmp = (count,)

    c.execute(query, tmp)
    password = c.fetchone()
    
    db.commit()
    db.close

    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    hide()
    usernameEntry.insert(0, username[0])
    passwordEntry.insert(0, password[0])

    press_login()

login.mainloop()