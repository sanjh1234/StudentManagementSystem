from tkinter import *
from tkinter import ttk, messagebox,filedialog
import time
import pymysql
import pandas

# functions
def iexit():
    result = messagebox.askyesno('Confirm','Do you want to EXIT?')
    if result:
        root.destroy()
    else:
        pass



def topleveldata(title,buttontext,command):
    global screen, idEntry, mobileEntry, nameEntry, emailEntry, addressEntry, genderEntry, dobEntry

    screen = Toplevel()
    screen.grab_set()
    screen.title(title)
    icon = PhotoImage(file='icon.png')
    screen.wm_iconphoto(False, icon)
    screen.resizable(False,False)
    screen.geometry('350x500+200+100')

    idLabel = Label(screen, text='ID', font=('arial', 12, 'bold'))
    idLabel.grid(row=0, column=0, padx=20, pady=20)
    idEntry = Entry(screen, font=('arial', 12, 'bold'))
    idEntry.grid(row=0,column=1, padx = 10)
    nameLabel = Label(screen, text='Name', font=('arial', 12, 'bold'))
    nameLabel.grid(row=1, column=0, padx=20, pady=20)
    nameEntry = Entry(screen, font=('arial', 12, 'bold'))
    nameEntry.grid(row=1,column=1, padx = 10)
    mobileLabel = Label(screen, text='Phone', font=('arial', 12, 'bold'))
    mobileLabel.grid(row=2, column=0, padx=20, pady=20)
    mobileEntry = Entry(screen, font=('arial', 12, 'bold'))
    mobileEntry.grid(row=2,column=1, padx = 10)
    emailLabel = Label(screen, text='Email', font=('arial', 12, 'bold'))
    emailLabel.grid(row=3, column=0, padx=20, pady=20)
    emailEntry = Entry(screen, font=('arial', 12, 'bold'))
    emailEntry.grid(row=3,column=1, padx = 10)
    addressLabel = Label(screen, text='Address', font=('arial', 12, 'bold'))
    addressLabel.grid(row=4, column=0, padx=20, pady=20)
    addressEntry = Entry(screen, font=('arial', 12, 'bold'))
    addressEntry.grid(row=4,column=1, padx = 10)
    genderLabel = Label(screen, text='Gender', font=('arial', 12, 'bold'))
    genderLabel.grid(row=5, column=0, padx=20, pady=20)
    genderEntry = Entry(screen, font=('arial', 12, 'bold'))
    genderEntry.grid(row=5,column=1, padx = 10)
    dobLabel = Label(screen, text='D.O.B', font=('arial', 12, 'bold'))
    dobLabel.grid(row=6, column=0, padx=20, pady=20)
    dobEntry = Entry(screen, font=('arial', 12, 'bold'))
    dobEntry.grid(row=6,column=1, padx = 10)

    stdbutton = Button(screen, text=buttontext, command = command, bg='#27408B', fg='white', font=('arial', 10, 'bold'), activebackground='#4876FF', cursor='hand2')
    stdbutton.grid(row=7,columnspan=2)

    if title == 'Update Student':
        indexing = stdTable.focus()
        
        content = stdTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        mobileEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])


def exportdata():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = stdTable.get_children()
    newlist = []
    for index in indexing:
        content = stdTable.item(index)
        datalist = content['values']
        newlist.append(datalist)

    table = pandas.DataFrame(newlist, columns=['Id','Name','Mobile','Email','Address','Gender','D-O-B','Data Modified','Time Modified'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved successfully')

    


def removestudent():
    indexing=stdTable.focus()
    print(indexing)
    content=stdTable.item(indexing)
    contentid = content['values'][0]
    query = 'delete from student where id=%s'
    mycursor.execute(query, contentid)
    con.commit()
    messagebox.showinfo('Deleted', f'Student ID {contentid} is deleted successfully')
    query = 'select * from student'
    mycursor.execute(query)
    fetcheddata=mycursor.fetchall()
    stdTable.delete(*stdTable.get_children())
    for data in fetcheddata:
        stdTable.insert('',END,values=data)



def updatedata():
    query = 'update student set name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date=%s, time=%s where id=%s'
    mycursor.execute(query,(nameEntry.get(),mobileEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get(),date,currtime,idEntry.get()))
    con.commit()
    messagebox.showinfo('Success',f'Student Id {idEntry.get()} is modified successfully', parent=screen)
    screen.destroy()
    showstudent()



def showstudent():
    query = 'select * from student'
    mycursor.execute(query)
    fetcheddata=mycursor.fetchall()
    stdTable.delete(*stdTable.get_children())
    for data in fetcheddata:
        stdTable.insert('',END,values=data)



def searchdata():
    query = 'select *from student where id=%s or name=%s or mobile=%s or email=%s or address=%s or gender=%s or dob=%s'
    mycursor.execute(query,(idEntry.get(), nameEntry.get(), mobileEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get()))
    stdTable.delete(*stdTable.get_children())
    fetcheddata=mycursor.fetchall()
    for data in fetcheddata:
        stdTable.insert('',END,values=data)



def adddata():
    if idEntry.get() == '' or nameEntry.get() == '' or mobileEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '' or emailEntry.get() == '':
        messagebox.showerror('Error', 'All Fields Are Required',parent = screen)

    else:
        try:
            query='insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(idEntry.get(), nameEntry.get(), mobileEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get(), date, currtime))
            con.commit()
            result = messagebox.askyesno('Data added successfully', 'Do you want to clean the form?', parent=screen)
            if result:
                idEntry.delete(0,END)
                nameEntry.delete(0,END)
                mobileEntry.delete(0,END)
                emailEntry.delete(0,END)
                addressEntry.delete(0,END)
                genderEntry.delete(0,END)
                dobEntry.delete(0,END)
            else:
                pass
        except:
            messagebox.showerror('Error', 'Id cannot be repeated', parent = screen)
            return

        query = 'select *from student'
        mycursor.execute(query)
        fetcheddata=mycursor.fetchall()
        stdTable.delete(*stdTable.get_children())
        for data in fetcheddata:
            stdTable.insert('',END,values=data)


def connectDatabase():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(host=hostEntry.get(), user = userEntry.get(), password = passEntry.get())
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Invalid Details', parent = connectWindow)
            return

        try:
            query = 'create database studentmanagementsystem'
            mycursor.execute(query)
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
            query = 'create table student(id int not null primary key, name varchar(30), mobile varchar(10), email varchar(30), address varchar(100), gender varchar(20), dob varchar(20), date varchar(50), time varchar(50))'
            mycursor.execute(query)
        except:
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
            
        messagebox.showinfo('Success', 'Database Connection is Successful', parent = connectWindow)
        connectWindow.destroy()
        addButton.config(state=NORMAL)
        searchButton.config(state=NORMAL)
        updateButton.config(state=NORMAL)
        showButton.config(state=NORMAL)
        removeButton.config(state=NORMAL)
        exportButton.config(state=NORMAL)


    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('350x200+500+200')
    connectWindow.title('Database Connection')
    icon = PhotoImage(file='icon.png')
    connectWindow.wm_iconphoto(False, icon)
    connectWindow.resizable(0,0)

    hostLabel = Label(connectWindow, text='Host Name', font=('arial', 12, 'bold'), padx=20, pady=20)
    hostLabel.grid(row=0, column=0)

    hostEntry = Entry(connectWindow, font=('arial', 12), bd = 2)
    hostEntry.grid(row=0, column=1)

    userLabel = Label(connectWindow, text='User Name', font=('arial', 12, 'bold'), padx=20)
    userLabel.grid(row=1, column=0)

    userEntry = Entry(connectWindow, font=('arial', 12), bd = 2)
    userEntry.grid(row=1, column=1)

    passLabel = Label(connectWindow, text='Password', font=('arial', 12, 'bold'), padx=20, pady=20)
    passLabel.grid(row=2, column=0)

    passEntry = Entry(connectWindow, font=('arial', 12), bd = 2)
    passEntry.grid(row=2, column=1)

    connectButton = Button(connectWindow, text='Connect', command=connect, bg='#27408B', fg='white', font=('arial', 10, 'bold'), activebackground='#4876FF', cursor='hand2')
    connectButton.grid(row=3,columnspan=2)


count=0
text=''
def slider():
    global text,count
    if count==len(title):
        count=0
        text=''
    text=text+title[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(400,slider)


def clock():
    global date, currtime
    date = time.strftime('%d/%m/%Y')
    currtime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\nTime: {currtime}')
    datetimeLabel.after(1000, clock)



# GUI
root=Tk()

root.geometry('1200x600+90+70')
root.resizable(False,False)

root.title('Student Management System')
icon = PhotoImage(file='icon.png')
root.wm_iconphoto(False, icon)

# Date&Time 
datetimeLabel = Label(root, text='hi', font=('times new roman', 12, 'bold'), fg='dimgray')
datetimeLabel.place(x=20,y=20)
clock()
title = "Student's Table"
sliderLabel = Label(root, text=title, font=('arial', 30, 'bold'), fg='#27408B', width=12)
sliderLabel.place(x=450,y=20)
slider()

# connect button 
connectButton= Button(root, text='Connect Database', command=connectDatabase, bg='#27408B', fg='white', font=('arial', 10, 'bold'), activebackground='#4876FF', cursor='hand2')
connectButton.place(x=1000,y=20)

# left rectangle
leftFrame = Frame(root, bg='#7D9EC0')
leftFrame.place(x=30, y=100, width=200, height=470)

addButton=Button(leftFrame, text='Add Student', width=20, state=DISABLED, command=lambda :topleveldata('Add Student', 'Add Student', adddata))
addButton.grid(row=0,column=0, pady=35)

searchButton=Button(leftFrame, text='Search Student', width=20, state=DISABLED, command=lambda :topleveldata('Search Student', 'Search', searchdata))
searchButton.grid(row=1,column=0)

showButton=Button(leftFrame, text='Show Student', width=20, state=DISABLED, command=showstudent)
showButton.grid(row=2,column=0, pady=35)

updateButton=Button(leftFrame, text='Update Student', width=20, state=DISABLED, command=lambda :topleveldata('Update Student', 'Update', updatedata))
updateButton.grid(row=3,column=0)

removeButton=Button(leftFrame, text='Remove Student', width=20, state=DISABLED, command=removestudent)
removeButton.grid(row=4,column=0, pady=35)

exportButton=Button(leftFrame, text='Export Data', width=20, state=DISABLED, command=exportdata)
exportButton.grid(row=5,column=0)

exitButton=Button(leftFrame, text='Exit', width=20, command=iexit)
exitButton.grid(row=6,column=0, pady=35, padx=25)


# right rectangle
rightframe = Frame(root, bg='#CDC9C9')
rightframe.place(x=260, y=100, width=910, height=470)

scrollBarX = Scrollbar(rightframe, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightframe, orient=VERTICAL)


stdTable = ttk.Treeview(rightframe,columns=('Id','Name','Mobile','Email','Address','Gender','DOB','Added Date','Added Time'), xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command=stdTable.xview)
scrollBarY.config(command=stdTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

stdTable.pack(fill=BOTH, expand=1)

stdTable.heading('Id', text='Id')
stdTable.heading('Name', text='Name')
stdTable.heading('Mobile', text='Mobile No.')
stdTable.heading('Email', text='Email')
stdTable.heading('Address', text='Address')
stdTable.heading('Gender', text='Gender')
stdTable.heading('DOB', text='DOB')
stdTable.heading('Added Date', text='Added Date')
stdTable.heading('Added Time', text='Added Time')

stdTable.column('Id',width=70,anchor=CENTER)
stdTable.column('Name',width=300,anchor=CENTER)
stdTable.column('Mobile',width=200,anchor=CENTER)
stdTable.column('Email',width=350,anchor=CENTER)
stdTable.column('Address',width=450,anchor=CENTER)
stdTable.column('Gender',width=100,anchor=CENTER)
stdTable.column('DOB',width=150,anchor=CENTER)
stdTable.column('Added Date',width=150,anchor=CENTER)
stdTable.column('Added Time',width=150,anchor=CENTER)

style = ttk.Style()
style.configure('Treeview', rowheight=40, font=('arial', 10, 'bold'), foreground='blue4', background='grey88')
style.configure('Treeview.Heading', font=('times new roman',15,'bold'))

stdTable.config(show='headings')

root.mainloop()