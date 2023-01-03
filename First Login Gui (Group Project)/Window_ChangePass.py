# py LIB #
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import mysql.connector
from email.message import EmailMessage
import ssl
import smtplib
import secrets

import Window_Verification
import CustomFunctions

def back(main_win, prev_win):
    prev_win.deiconify()
    main_win.destroy()


def cp_window(login_win):
    def submit():
        user = username.get()
        user_email = CustomFunctions.db_select_one_email(user)
        if user_email == None:
            messagebox.showerror('Error', 'Username Does Not Exist',parent=forgot_pass)
        else:
            if username.get() == '' or password.get() == '' or conpass.get() == '':
                messagebox.showerror('Error', 'Fill up all empty boxes',parent=forgot_pass)
            elif password.get() != conpass.get():
                messagebox.showerror('Error', 'Password Confirmation Does Not Match The Password',parent=forgot_pass)
            else:
                if user[0] == '@':
                    Window_Verification.admin(login_win, forgot_pass, user_email, user, password.get(), 'CP')
                else:
                    Window_Verification.client(login_win, forgot_pass, user_email, user, password.get(), 'CLIENT', 'CP', None)

    login_win.withdraw()
    forgot_pass= Toplevel()
    forgot_pass.title('Change Password')
    forgot_pass.geometry('990x660+50+50') #bg
    forgot_pass.iconbitmap('two.ico')
    forgot_pass.resizable(0,0)

    bgImage=ImageTk.PhotoImage(file='Forgot_Password.png')

    bgLabel = Label(forgot_pass,image=bgImage)
    bgLabel.place(x=0,y=0)

    userLabel=Label(forgot_pass, text='Username', font=('arial', 10), bg='#e6e6e6', fg='grey28')
    userLabel.place(x=560, y=245)

    username=Entry(forgot_pass, width=25, font=('ariel', 11), bg='#e6e6e6',bd=0, fg='black')
    username.place(x=580,y=265)


    passLabel=Label(forgot_pass, text='New Password', font=('arial', 10), bg='#e1ecff', fg='grey28')
    passLabel.place(x=560, y=324)

    password=Entry(forgot_pass, width=25, font=('ariel', 11), bg='#e1ecff',bd=0, fg='black')
    password.place(x=580,y=345)


    conpassLabel=Label(forgot_pass, text='Confirm Password', font=('arial', 10), bg='#e1ecff', fg='grey28')
    conpassLabel.place(x=560, y=407)

    conpass=Entry(forgot_pass, width=25, font=('ariel', 11), bg='#e1ecff',bd=0, fg='black')
    conpass.place(x=580,y=427)


    submitButton=Button(forgot_pass, text='Submit', font=('Open Sans', 10, 'bold'), fg='white', bg='#224481', activebackground='grey', activeforeground='black', cursor='hand2',bd=0,width=31, height=2, command= lambda: submit())
    submitButton.place(x=590,y=477)

    backButton=Button(forgot_pass, text='Back', font=('Open Sans', 10, 'bold'), fg='white', bg='#224481', activebackground='grey', activeforeground='black', cursor='hand2',bd=0,width=20, height=2, command = lambda main = forgot_pass, prev = login_win: back(main, prev))
    backButton.place(x=635,y=522)

    forgot_pass.protocol("WM_DELETE_WINDOW", lambda main = forgot_pass, prev = login_win: back(main, prev))
    forgot_pass.mainloop()