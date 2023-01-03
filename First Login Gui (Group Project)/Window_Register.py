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
import Window_Verification

# FUNCTIONS
import CustomFunctions

# MYsql Functions #
def db_connect():
    return CustomFunctions.db_connect()

def back(main_win, prev_win):
    prev_win.deiconify()
    main_win.destroy()

def register(login):
    
    def FocusedIn(event):
        passwordEntry.config(show='')
        if passwordEntry.get() == 'Password':
            passwordEntry.delete(0, END)

    def FocusedOut(event):
        passwordEntry.config(show='*')
        if passwordEntry.get() == '':
            passwordEntry.insert(0, 'Password')
            passwordEntry.config(show='')

    def not_filled():
        messagebox.showerror('Error', 'Incomplete Entry',parent=create_acc)

    def pressed_verify():

        database_email = CustomFunctions.db_select_all_email()
        database_username = CustomFunctions.db_select_all_username()
        email_username = [False, False]

        for i in range(len(database_email)):
            if database_email[i][0] == emailEntry.get():
                email_username[0] = True
                break
            if database_username[i][0] == usernameEntry.get():
                email_username[1] = True
                break                
            

        if emailEntry.get() == 'Email' or emailEntry.get() == '':
            not_filled()
        elif usernameEntry.get() == 'Username' or usernameEntry.get() == '':
            not_filled()
        elif passwordEntry.get() == 'Password' or passwordEntry.get() == '':
            not_filled()
        elif conpasswordEntry.get() == 'Confirm Password' or conpasswordEntry.get() == '':
            not_filled()
        elif conpasswordEntry.get() != passwordEntry.get():
            messagebox.showerror('Error', 'Confirm Password and Password Does Not Match',parent=create_acc)
        elif email_username[0] == True:
            messagebox.showerror('Error', 'Email is Already Registered',parent=create_acc)
        elif email_username[1] == True:
            messagebox.showerror('Error', 'Username is Already Registered',parent=create_acc)
        else:
            username = usernameEntry.get()
            if username[0] == '@':
                Window_Verification.admin(login, create_acc, emailEntry.get(), username, passwordEntry.get(), 'REG')
            else:
                Window_Verification.client(login, create_acc, emailEntry.get(), usernameEntry.get(), passwordEntry.get(), 'CLIENT', 'REG', None)

    login.withdraw()
    create_acc= Toplevel()
    create_acc.title('Create Account')
    create_acc.geometry('990x660+50+50') #bg
    create_acc.iconbitmap('two.ico')
    create_acc.resizable(0,0)
   
    bgImage=ImageTk.PhotoImage(file='create.png')
 
    bgLabel = Label(create_acc,image=bgImage)
    bgLabel.place(x=0,y=0)
 
    emailEntry=Entry(create_acc, width=25, font=('Microsoft Yahei UI Light', 14, 'bold'), bg='#e6e6e6', bd=0, fg='black')
    emailEntry.place(x=123,y=240)
    emailEntry.insert(0, 'Email')
 
    emailEntry.bind('<FocusIn>', lambda event, name = emailEntry: CustomFunctions.FocusedIn(event, name))
    emailEntry.bind('<FocusOut>', lambda event, name = emailEntry, id = 2: CustomFunctions.FocusedOut(event, name, id))
   
    usernameEntry=Entry(create_acc, width=25, font=('Microsoft Yahei UI Light', 14, 'bold'), bg='#e6e6e6', bd=0, fg='black')
    usernameEntry.place(x=123,y=300)
    usernameEntry.insert(0, 'Username')
 
    usernameEntry.bind('<FocusIn>', lambda event, name = usernameEntry: CustomFunctions.FocusedIn(event, name))
    usernameEntry.bind('<FocusOut>', lambda event, name = usernameEntry, id = 0: CustomFunctions.FocusedOut(event, name, id))
 
    passwordEntry=Entry(create_acc, width =25, font=('Microsoft Yahei UI Light', 14, 'bold'), bg='#e1ecff',bd=0, fg='black')
    passwordEntry.place(x=123,y=358)
    passwordEntry.insert(0, 'Password')

    passwordEntry.bind('<FocusIn>', lambda event: FocusedIn(event))
    passwordEntry.bind('<FocusOut>', lambda event: FocusedOut(event))
 
    conpasswordEntry=Entry(create_acc, width =25, font=('Microsoft Yahei UI Light', 14, 'bold'),bg='#e1ecff',bd=0, fg='black')
    conpasswordEntry.place(x=123,y=418)
    conpasswordEntry.insert(0, 'Confirm Password')
 
    conpasswordEntry.bind('<FocusIn>', lambda event, name = conpasswordEntry: CustomFunctions.FocusedIn(event, name))
    conpasswordEntry.bind('<FocusOut>', lambda event, name = conpasswordEntry, id =3: CustomFunctions.FocusedOut(event, name, id))
 
    verifyButton=Button(create_acc, text='Verify', font=('Open Sans', 10, 'bold'), fg='white', bg='#224481', activebackground='grey' , activeforeground='black', cursor='hand2',bd=0,width=31, height=2, command= lambda: pressed_verify())
    verifyButton.place(x=155,y=470)

    backButton=Button(create_acc, text='Back', font=('Open Sans', 10, 'bold'), fg='white', bg='#224481', activebackground='grey' , activeforeground='black', cursor='hand2',bd=0,width=20, height=2, command= lambda main = create_acc, prev = login: back(main, prev))
    backButton.place(x=197,y=515)

    create_acc.protocol("WM_DELETE_WINDOW", lambda main = create_acc, prev = login: back(main, prev))
    create_acc.mainloop()
