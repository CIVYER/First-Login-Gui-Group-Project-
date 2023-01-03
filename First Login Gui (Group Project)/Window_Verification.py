# py LIB #
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import mysql.connector
from email.message import EmailMessage
import ssl
import smtplib
import secrets

import CustomFunctions

def db_connect(): 
    return CustomFunctions.db_connect()

def in_code(receiver_in):
    # Email Verification
    gmail_user = 'auth.group2@gmail.com'
    gmail_password = 'tinidqskatqnlllh'
    receiver = receiver_in

    verification_code = secrets.token_urlsafe(4)
    
    subject = 'Verification Code'

    body = "Your Verification Code is: " + str(verification_code)

    em = EmailMessage()
    em['From'] = gmail_user
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()



    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(gmail_user, gmail_password)
            smtp.sendmail(gmail_user, receiver, em.as_string())
    except:
        return "INVALID EMAIL"
    
    return verification_code  

def back(previous_win, main_win):
    previous_win.deiconify()
    main_win.destroy()
    

def client(login_win, main_win, user_email, user_username, user_password, acc_type, action, code):
    def submit():
        if ver_entry.get() == ver_code:
            if action == 'CP':

                db = db_connect()
                c = db.cursor()

                query='UPDATE `Log in` SET login_Password=%s WHERE login_Username=%s'
                tmp = (user_password, user_username)

                c.execute(query, tmp)

                db.commit()
                db.close()

                db = db_connect()
                c = db.cursor()

                login_id = CustomFunctions.db_select_login_id(user_username)

                query = 'insert into `forgot password`(user_id, login_id, verification_id) values(%s, %s, %s)'
                tmp = (login_id, login_id, login_id)

                c.execute(query, tmp)

                db.commit()
                db.close()

                CustomFunctions.create_logs(user_email,'Changed Password')
                
            if action == 'REG':

                # insert username & password
                db = db_connect()
                c = db.cursor()

                query = 'insert into `log in`(login_username, login_password) values(%s,%s)'
                tmp = (user_username, user_password)

                c.execute(query, tmp)

                db.commit()
                db.close()

                # insert account type (ADMIN/CLIENT)
                db = db_connect()
                c = db.cursor()

                query = 'insert into account_type(accountType) values(%s)'
                tmp = (acc_type,)

                c.execute(query, tmp)

                db.commit()
                db.close()

                # insert 1st verification code
                db = db_connect()
                c = db.cursor()

                query = 'insert into verification(verification_code) values(%s)'
                tmp = (ver_code,)

                c.execute(query, tmp)

                db.commit()
                db.close()

                # insert email verification_id, login_id
                login_id = CustomFunctions.db_select_login_id(user_username)
                db = db_connect()
                c = db.cursor()

                query = 'insert into `sign up`(email, verification_id, login_id) values(%s,%s,%s)'
                tmp = (user_email, login_id, login_id)

                c.execute(query, tmp)

                db.commit()
                db.close()

                # insert login state
                db = db_connect()
                c = db.cursor()

                query = 'insert into login_state(login_id, logged_in) values(%s,%s)'
                tmp = (login_id, 0)

                c.execute(query, tmp)

                db.commit()
                db.close()

                # insert profile id's
                db = db_connect()
                c = db.cursor()

                query = 'insert into `user profile`(login_id, signup_id, account_typeid) values(%s, %s, %s)'
                tmp = (login_id, login_id, login_id)

                c.execute(query, tmp)

                db.commit()
                db.close()

                CustomFunctions.create_logs(user_username, 'Signed Up')




            login_win.deiconify()
            if action == 'CP':
                messagebox.showinfo('Success', 'Succesfully Changed Your Password',parent=login_win)
            else:
                messagebox.showinfo('Success', 'You Succesfully Created An Account',parent=login_win)
                
            main_win.destroy()
            verify_Window.destroy()
        else:
            messagebox.showerror('Error', 'The Code You Have Entered Does Not Match The One Sent To Your Email',parent=verify_Window)

    if acc_type == 'ADMIN':
        ver_code = code
    else:
        ver_code = in_code(user_email)

    print('client:', ver_code)

    if ver_code == 'INVALID EMAIL':
        messagebox.showerror('Error', 'Invalid Email or Slow Internet Connection',parent=main_win)
    else:
        main_win.withdraw()

        verify_Window = Toplevel()
        verify_Window.title('Verification')
        verify_Window.geometry('990x660+50+50') #bg
        verify_Window.iconbitmap('two.ico')
        verify_Window.resizable(0,0)

        bgImage=ImageTk.PhotoImage(file='Verificatoin.png')

        bgLabel = Label(verify_Window,image=bgImage)
        bgLabel.place(x=0,y=0)
                        
        ver_entry=Entry(verify_Window, font=('ariel', 13, 'bold'), bg='#e6e6e6', width=25,bd=0, fg='black')
        ver_entry.place(x=150,y=222)

        submit_button = Button(verify_Window, text="Submit", font=('Open Sans', 10, 'bold'),fg='white', bg='#224481', activebackground='grey' , activeforeground='black', cursor='hand2',bd=0, command = lambda: submit())
        submit_button.place(x=415,y=220)

        verify_Window.protocol("WM_DELETE_WINDOW", lambda prev_win = main_win, main_win = verify_Window: back(prev_win, main_win))
        verify_Window.mainloop()

def admin(login_win, main_win, user_email, user_username, user_password, action):

    def submit():
        if admin_entry.get() == ver_code:    
            verify_admin.destroy()
            client(login_win, main_win, user_email, user_username, user_password, 'ADMIN', action, ver_inv)
        else:
            messagebox.showerror('Error', "The Code You Have Entered Does Not Match The One Sent To Admin's Email",parent=verify_admin)

    ver_inv = in_code(user_email)

    if ver_inv == 'INVALID EMAIL':
        messagebox.showerror('Error', 'Invalid Email or Slow Internet Connection',parent=main_win)
    else:
        ver_code = in_code('auth.group2@gmail.com')
        print("admin:", ver_code)
        main_win.withdraw()

        verify_admin = Toplevel()
        verify_admin.title('Verification')
        verify_admin.geometry('439x272+50+50') #bg
        verify_admin.iconbitmap('two.ico')
        verify_admin.resizable(0,0)

        bgImage=ImageTk.PhotoImage(file='admin_verification.png')

        bgLabel = Label(verify_admin,image=bgImage)
        bgLabel.place(x=0,y=0)


        admin_entry = Entry(verify_admin, font=('ariel', 16, 'bold'), bg='#e6e6e6', width=25,bd=0, fg='black')
        admin_entry.place(x=69, y=130)

        submit_button = Button(verify_admin, text="Submit", font=('Open Sans', 15, 'bold'),fg='black', bg='white', cursor='hand2',bd=0,width=35, command = lambda: submit())
        submit_button.place(x=6,y=194)    

        verify_admin.protocol("WM_DELETE_WINDOW", lambda prev_win = main_win, main_win = verify_admin: back(prev_win, main_win))
        verify_admin.mainloop()
