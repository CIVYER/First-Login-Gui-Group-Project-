# py LIB #
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
from email.message import EmailMessage
from tkinter import ttk
import mysql.connector
import ssl
import smtplib
import secrets


# Login Functions #
import CustomFunctions

# MYsql Functions #
def db_connect():
    return CustomFunctions.db_connect()


def Pwindow(login, username, role):
    def on_close():
        CustomFunctions.create_logs(username, 'Closed Out')
        login.destroy()
    
    def logout():
        CustomFunctions.db_update_wLogin_id('login_state', 'logged_in', 0, username)
        CustomFunctions.create_logs(username, "Logged Out")
        login.deiconify()
        profile_window.destroy()

    def profile_in():
        CustomFunctions.create_logs(username, 'Entered Profile')
        home_Button.config(state=ACTIVE)
        profile_Button.config(state=DISABLED)
        dashboardNameLabel.config(text='PROFILE')
        
        bgLabel_home.place_forget()
        profile_frame.place(x=0,y=0)
        update_button.pack(side=BOTTOM)
        logout_button.pack(side=BOTTOM, pady=20)        
        



    def home_in():
        CustomFunctions.create_logs(username, 'Entered Home')
        update_logs_label()
        
        home_Button.config(state=DISABLED)
        profile_Button.config(state=ACTIVE)

        dashboardNameLabel.config(text='HOME')
        
        profile_frame.place_forget()
        update_button.pack_forget()
        logout_button.pack_forget()
        # bgLabel_profile.place_forget()
        # previous_button.place_forget()
        # next_button.place_forget()
        # heading.place_forget()
        # heading2.place_forget()
        
        bgLabel_home.place(x=0,y=0)

    login.withdraw()
    profile_window = Toplevel()
    profile_window.geometry('990x660+50+50') #bg
    profile_window.resizable(0,0)
    profile_window.iconbitmap('two.ico')
    profile_window.title('Account Information')

    # Dashboard Here
    bgHome=ImageTk.PhotoImage(file='Profile_Home.png')
    bgUser=ImageTk.PhotoImage(file='User_Profile.png')
    bgAdmin=ImageTk.PhotoImage(file='Admin_Profile.png')

    profile_frame = Frame(profile_window, width=990, height=660, bg="black")
    profile_frame.propagate(False)
    # profile_frame.place(x=0, y=0)
    
    bgLabel_home = Label(profile_window,image=bgHome)
    bgLabel_profile = Label(profile_frame)
    bgLabel_profile.place(x=0,y=0)

    dashboardFrame = Frame(profile_window, bg='white', height=500, width=227)
    dashboardFrame.propagate(False)
    dashboardFrame.place(x=42.4, y=50)

    dashboardNameLabel = Label(dashboardFrame, text="HOME", font=('ariel', 30, 'bold'), bg="white")
    dashboardNameLabel.pack(fill=BOTH)

    home_Button = Button(dashboardFrame,text='HOME',bd=0,font=('Open Sans', 15, 'bold'), bg=None, command= lambda: home_in(),cursor='hand2')
    home_Button.pack(fill=BOTH, pady=10)
    
    profile_Button = Button(dashboardFrame,text='PROFILE',bd=0,font=('Open Sans', 15, 'bold'), bg=None, command= lambda: profile_in(),cursor='hand2')
    profile_Button.pack(fill=BOTH)

    logout_button = Button(dashboardFrame ,text="Logout", font=('arial', 10, 'bold underline'),fg='BLUE',bd=0,bg='#ffffff', activebackground='grey' , activeforeground='black', cursor='hand2', width=25, command= lambda: logout())




    # Logs Here
    global offset
    global log_count

    offset = 0
    log_count = 0

    login_id = CustomFunctions.db_select_login_id(username)

    def select_all_logs():
        db = db_connect()
        c = db.cursor()

        query = 'select log_name from `log history` where login_id=%s'
        tmp = (login_id,)

        c.execute(query, tmp)
        logs = c.fetchall()

        db.commit()
        db.close()

        return logs

    def select_logs():
        db = db_connect()
        c = db.cursor()

        query = 'SELECT log_DT FROM `Log history` WHERE login_ID=%s LIMIT 20 OFFSET %s'
        tmp = (login_id, offset)

        c.execute(query, tmp)
        log_date = c.fetchall()
        db.commit()
        db.close()

        db = db_connect()
        c = db.cursor()

        query = 'SELECT log_Name FROM `Log history` WHERE login_ID=%s LIMIT 20 OFFSET %s'
        tmp = (login_id, offset)

        c.execute(query, tmp)
        log_name = c.fetchall()
        db.commit()
        db.close()

        return log_name, log_date
    
    def update_logs_label():

        log_name, log_date = select_logs()

        for i in range(20):
            date_LabelDict[i].config(text='')
            logName_LabelDict[i].config(text='')

        for i in range(len(log_name)):
            date_LabelDict[i].config(text=f'{log_date[i][0]}-')
            logName_LabelDict[i].config(text=f'{log_name[i][0]}')
        
        length = len(select_all_logs())/20

        if log_count < int(length):
            next_button.config(state=ACTIVE)
        

    def pressed_next():
        previous_button.config(state=ACTIVE)
        global offset
        global log_count

        log_count += 1

        offset = log_count * 20
        update_logs_label()

        length = len(select_all_logs())/20

        if log_count >= int(length):
            next_button.config(state=DISABLED)

    def pressed_prev():
        next_button.config(state=ACTIVE)
        global offset
        global log_count

        log_count -= 1

        if log_count <= 0:
            log_count = 0
            previous_button.config(state=DISABLED)

        offset = log_count * 20
        update_logs_label()

    log_name, log_date = select_logs()

    DTLOGframe = Frame(profile_frame, bg='#a6d9f2', width=212, height=440)
    DTLOGframe.grid_propagate(False)
    DTLOGframe.place(x = 707, y = 120)
    
    DandTLabel=Label(DTLOGframe, text='Date/Time', font=('arial', 8,'bold'), bg='#a6d9f2', fg='black')
    DandTLabel.grid(column=0, row=0)
    
    ActivitiesLabel=Label(DTLOGframe, text='Activities', font=('arial', 8,'bold'), bg='#a6d9f2', fg='black')
    ActivitiesLabel.grid(column=2, row=0)

    date_LabelDict = []
    logName_LabelDict = []


    for i in range(20):
        dateT_Label_D = Label(DTLOGframe, text='', font=('arial', 8), bg='#a6d9f2', fg='red')
        dateT_Label_D.grid(column=0, row=i+1)
        
        logName_Label_D = Label(DTLOGframe, text='', font=('arial', 8), bg='#a6d9f2', fg='red')
        logName_Label_D.grid(column=2, row=i+1)

        date_LabelDict.append(dateT_Label_D)
        logName_LabelDict.append(logName_Label_D)

    previous_button = Button(profile_frame ,text="Previous", font=('arial', 8, 'bold'),width=13,fg='white',bd=1,bg='#1E90FF', activebackground='grey' , activeforeground='black', cursor='hand2', command = lambda: pressed_prev(), state=DISABLED)
    previous_button.place(x=707,y=546)
    
    next_button = Button(profile_frame ,text="Next", font=('arial', 8, 'bold'),width=13,fg='white',bd=1,bg='#1E90FF', activebackground='grey' , activeforeground='black', cursor='hand2', command = lambda: pressed_next(), state=DISABLED)
    next_button.place(x=820,y=546)

    update_logs_label()
    

    # User Info Here
    global drop_selected_email
    drop_selected_email = CustomFunctions.db_select_one_email(username)
    
    def f_out(event, entry):
        if entry.get() == '':
            entry.insert(0, '*')
            entry.config(fg='red')

    def f_in(event, entry):
        if entry.get() == '*':
            entry.delete(0, END)
        entry.config(fg='black')

    def drop_select(event):
        global drop_selected_email
        drop_selected_email = select_email.get()
        Emailadd.delete(0, END)
        Emailadd.insert(0, drop_selected_email)
        show_profile()

    def backup():

        signup_id = CustomFunctions.db_select_signup_id(drop_selected_email)

        db = db_connect()
        c = db.cursor()

        query = 'insert into p_backup (user_ID) values(%s)'
        tmp = (signup_id,)

        c.execute(query, tmp)

        db.commit()
        db.close()

        db = db_connect()
        c = db.cursor()

        query = 'select P_Backup_ID from p_backup'

        c.execute(query)

        P_Backup_ID = c.fetchall()

        db.close()

        db = db_connect()
        c = db.cursor()

        c.execute('describe p_backup')

        table_col = c.fetchall()

        db.close()

        for i in range(len(pEntryDict)):
            db = db_connect()
            c = db.cursor()

            query = "update p_backup set " + table_col[i+2][0] + " = %s where P_Backup_ID = %s"
            tmp = (pEntryDict[i].get(), P_Backup_ID[(len(P_Backup_ID)-1)][0])

            c.execute(query, tmp)

            db.commit()
            db.close()
        db = db_connect()
        c = db.cursor()

        query = "update p_backup set b_Date =curdate() where P_Backup_ID = %s"
        tmp = (P_Backup_ID[(len(P_Backup_ID)-1)][0],)

        c.execute(query, tmp)

        db.commit()
        db.close()
        

    def update():
        
        backup()
        empty = False
        for i in range(len(pEntryDict)):
            if pEntryDict[i].get() == '' or pEntryDict[i].get() == '*':
                empty = True
                break
            else:
                empty = False

        for i in range(len(pEntryDict)):
            if pEntryDict[i].get() == '':
                pEntryDict[i].config(fg='red')
                pEntryDict[i].insert(0, '*')

        if empty == True:
            messagebox.showerror('Error', 'Fill Up Highlighted Red', parent = profile_window)
        else:
            db = db_connect()
            c = db.cursor()
            c.execute('describe `user profile`')
            table_col = c.fetchall()
            db.close()

            for i in range(4, 19):
                CustomFunctions.db_update_wLogin_id('`user profile`',str(table_col[i][0]), pEntryDict[i-4].get(), drop_selected_email)
            if drop_selected_email == user_email:
                messagebox.showinfo('Success', 'Updated Own Profile', parent = profile_window)
                CustomFunctions.create_logs(username, 'UD Own Profile')
            else:
                messagebox.showinfo('Success', "Updated Other's Profile", parent = profile_window)
                CustomFunctions.create_logs(username, 'UD Other Profile')
            update_logs_label()
    def show_profile():

        signup_id = CustomFunctions.db_select_signup_id(drop_selected_email)

        db = db_connect()
        c = db.cursor()

        c.execute(f"select * from `user profile` where login_id={signup_id}")

        user_profile = c.fetchall()

        db.close()

        try:
            for i in range(len(pEntryDict)):
                pEntryDict[i].delete(0, END)
                pEntryDict[i].insert(0, user_profile[0][i+4])
                pEntryDict[i].config(fg='black')
        except:
            for i in range(len(pEntryDict)):
                pEntryDict[i].delete(0, END)


    nameFrame = Frame(profile_frame, width=230, height=23, bg = 'white')
    nameFrame.pack_propagate(False)
    nameFrame.place(x=700, y=63)
    user_email = CustomFunctions.db_select_one_email(username)

    if role == 'ADMIN':
        email_d = []
        emails = CustomFunctions.db_select_all_email()

        for i in range(len(emails)):
            email_d.append(emails[i][0])

        bgLabel_profile.config(image=bgAdmin)

        select_email = StringVar()
        select_email.set(f"{user_email}")
        drop= OptionMenu(nameFrame, select_email, *email_d, command = lambda event: drop_select(event))
        drop.config(bd=0, bg='white')
        drop.pack(fill=BOTH)

    else:
        bgLabel_profile.config(image=bgUser)
        nameLabel=Label(nameFrame, text=f'{user_email}', font=('arial',9,'bold'), bg='white', fg='grey28')
        nameLabel.pack(fill=BOTH)

    update_button = Button(dashboardFrame ,text="Update", font=('arial', 10, 'bold'),fg='white',bd=1,bg='#1067ec', activebackground='grey' , activeforeground='black', cursor='hand2', width=25, command= lambda: update())

    heading=Label(profile_frame,text='Account Information',font=('Bahnschrift',16,'bold') ,bg='#bce9ff',fg='#4078d8')
    heading.place(x=390,y=70)
    heading2=Label(profile_frame,text='Residential Address',font=('Bahnschrift',16,'bold') ,bg='#bce9ff',fg='#4078d8')
    heading2.place(x=390,y=400)    
    
    pEntryDict = []

    LnameLabel=Label(profile_frame, text='Last Name', font=('arial', 8), bg='#bce9ff', fg='grey28')
    LnameLabel.place(x=300, y=114)
    
    Lname=Entry(profile_frame, width=28, font=('ariel', 8), bg='white',bd=0, fg='black')
    Lname.place(x=305,y=137)

    Lname.bind('<FocusIn>', lambda event, entry = Lname: f_in(event, entry))
    Lname.bind('<FocusOut>', lambda event, entry = Lname: f_out(event, entry))
    pEntryDict.append(Lname)
    
    FnameLabel=Label(profile_frame, text='First Name', font=('arial', 8), bg='#bce9ff', fg='grey28')
    FnameLabel.place(x=495, y=114)
    
    Fname=Entry(profile_frame, width=26, font=('ariel', 8), bg='white',bd=0, fg='black')
    Fname.place(x=500,y=137)

    Fname.bind('<FocusIn>', lambda event, entry = Fname: f_in(event, entry))
    Fname.bind('<FocusOut>', lambda event, entry = Fname: f_out(event, entry))    
    pEntryDict.append(Fname)

    MnameLabel=Label(profile_frame, text='Middle Name', font=('arial', 8), bg='#bce9ff', fg='grey28')
    MnameLabel.place(x=300, y=175)
    
    Mname=Entry(profile_frame, width=28, font=('ariel', 8), bg='white',bd=0, fg='black')
    Mname.place(x=305,y=198)

    Mname.bind('<FocusIn>', lambda event, entry = Mname: f_in(event, entry))
    Mname.bind('<FocusOut>', lambda event, entry = Mname: f_out(event, entry))
    pEntryDict.append(Mname)

    birthLabel=Label(profile_frame, text='Date of Birth', font=('arial', 8), bg='#bce9ff', fg='grey28')
    birthLabel.place(x=495, y=175)
    
    birth=Entry(profile_frame, width=26, font=('ariel', 8), bg='white',bd=0, fg='black')
    birth.place(x=500,y=198)

    birth.bind('<FocusIn>', lambda event, entry = birth: f_in(event, entry))
    birth.bind('<FocusOut>', lambda event, entry = birth: f_out(event, entry))
    pEntryDict.append(birth)

    GenderLabel=Label(profile_frame, text='Gender', font=('arial', 8), bg='#bce9ff', fg='grey28')
    GenderLabel.place(x=300, y=232)
    
    Gender=Entry(profile_frame, width=11, font=('ariel', 8), bg='white',bd=0, fg='black')
    Gender.place(x=303,y=254)

    Gender.bind('<FocusIn>', lambda event, entry = Gender: f_in(event, entry))
    Gender.bind('<FocusOut>', lambda event, entry = Gender: f_out(event, entry))
    pEntryDict.append(Gender)

    BirthplaceLabel=Label(profile_frame, text='Place of Birth', font=('arial', 8), bg='#bce9ff', fg='grey28')
    BirthplaceLabel.place(x=393, y=232)
    
    BirthP=Entry(profile_frame, width=23, font=('ariel', 8), bg='white',bd=0, fg='black')
    BirthP.place(x=398,y=254)

    BirthP.bind('<FocusIn>', lambda event, entry = BirthP: f_in(event, entry))
    BirthP.bind('<FocusOut>', lambda event, entry = BirthP: f_out(event, entry))
    pEntryDict.append(BirthP)
    
    CivilStatLabel=Label(profile_frame, text='Civil Status', font=('arial', 8), bg='#bce9ff', fg='grey28')
    CivilStatLabel.place(x=556, y=232)
    
    Cs=Entry(profile_frame, width=16, font=('ariel', 8), bg='white',bd=0, fg='black')
    Cs.place(x=561,y=254)

    Cs.bind('<FocusIn>', lambda event, entry = Cs: f_in(event, entry))
    Cs.bind('<FocusOut>', lambda event, entry = Cs: f_out(event, entry))
    pEntryDict.append(Cs)
    
    NationalityLabel=Label(profile_frame, text='Nationality', font=('arial', 8), bg='#bce9ff', fg='grey28')
    NationalityLabel.place(x=300, y=283)
    
    Nationality=Entry(profile_frame, width=23, font=('ariel', 8), bg='white',bd=0, fg='black')
    Nationality.place(x=305,y=307)

    Nationality.bind('<FocusIn>', lambda event, entry = Nationality: f_in(event, entry))
    Nationality.bind('<FocusOut>', lambda event, entry = Nationality: f_out(event, entry))
    pEntryDict.append(Nationality)
    
    ReligionLabel=Label(profile_frame, text='Religion', font=('arial', 8), bg='#bce9ff', fg='grey28')
    ReligionLabel.place(x=467, y=283)
    
    Religion=Entry(profile_frame, width=31, font=('ariel', 8), bg='white',bd=0, fg='black')
    Religion.place(x=470,y=307)

    Religion.bind('<FocusIn>', lambda event, entry = Religion: f_in(event, entry))
    Religion.bind('<FocusOut>', lambda event, entry = Religion: f_out(event, entry))
    pEntryDict.append(Religion)
    
    EmailAddLabel=Label(profile_frame, text='Email Address', font=('arial', 8), bg='#bce9ff', fg='grey28')
    EmailAddLabel.place(x=300, y=332)
    
    Emailadd=Entry(profile_frame, width=28, font=('ariel', 8), bg='white',bd=0, fg='black')
    Emailadd.place(x=305,y=356)

    Emailadd.insert(0, drop_selected_email)
    
    ContactLabel=Label(profile_frame, text='Contact', font=('arial', 8), bg='#bce9ff', fg='grey28')
    ContactLabel.place(x=493, y=332)
    
    ContactNo=Entry(profile_frame, width=26, font=('ariel', 8), bg='white',bd=0, fg='black')
    ContactNo.place(x=500,y=356)

    ContactNo.bind('<FocusIn>', lambda event, entry = ContactNo: f_in(event, entry))
    ContactNo.bind('<FocusOut>', lambda event, entry = ContactNo: f_out(event, entry))
    pEntryDict.append(ContactNo)
    
    AddressLabel=Label(profile_frame, text='Address', font=('arial', 8), bg='#bce9ff', fg='grey28')
    AddressLabel.place(x=300, y=436)
    
    Address=Entry(profile_frame, width=58, font=('ariel', 8), bg='white',bd=0, fg='black')
    Address.place(x=305,y=459)

    Address.bind('<FocusIn>', lambda event, entry = Address: f_in(event, entry))
    Address.bind('<FocusOut>', lambda event, entry = Address: f_out(event, entry))
    pEntryDict.append(Address)
    
    RegionLabel=Label(profile_frame, text='Region', font=('arial', 8), bg='#bce9ff', fg='grey28')
    RegionLabel.place(x=300, y=485)
    
    MRegion=Entry(profile_frame, width=28, font=('ariel', 8), bg='white',bd=0, fg='black')
    MRegion.place(x=305,y=508)

    MRegion.bind('<FocusIn>', lambda event, entry = MRegion: f_in(event, entry))
    MRegion.bind('<FocusOut>', lambda event, entry = MRegion: f_out(event, entry))
    pEntryDict.append(MRegion)
    
    CityLabel=Label(profile_frame, text='City', font=('arial', 8), bg='#bce9ff', fg='grey28')
    CityLabel.place(x=495, y=485)
    
    City=Entry(profile_frame, width=26, font=('ariel', 8), bg='white',bd=0, fg='black')
    City.place(x=500,y=508)

    City.bind('<FocusIn>', lambda event, entry = City: f_in(event, entry))
    City.bind('<FocusOut>', lambda event, entry = City: f_out(event, entry))
    pEntryDict.append(City)
    
    BarangayLabel=Label(profile_frame, text='Barangay', font=('arial', 8), bg='#bce9ff', fg='grey28')
    BarangayLabel.place(x=300, y=532)
    
    Barangay=Entry(profile_frame, width=28, font=('ariel', 8), bg='white',bd=0, fg='black')
    Barangay.place(x=305,y=555)

    Barangay.bind('<FocusIn>', lambda event, entry = Barangay: f_in(event, entry))
    Barangay.bind('<FocusOut>', lambda event, entry = Barangay: f_out(event, entry))
    pEntryDict.append(Barangay)
    
    ZipLabel=Label(profile_frame, text='Zip Code', font=('arial', 8), bg='#bce9ff', fg='grey28')
    ZipLabel.place(x=495, y=532)
    
    ZipCode=Entry(profile_frame, width=26, font=('ariel', 8), bg='white',bd=0, fg='black')
    ZipCode.place(x=500,y=555)

    ZipCode.bind('<FocusIn>', lambda event, entry = ZipCode: f_in(event, entry))
    ZipCode.bind('<FocusOut>', lambda event, entry = ZipCode: f_out(event, entry))
    pEntryDict.append(ZipCode)

    show_profile()
    home_in()

    profile_window.protocol("WM_DELETE_WINDOW", on_close)
    profile_window.mainloop()

# Pwindow(Tk(), 'b', 'ADMIN')