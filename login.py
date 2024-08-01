from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

def login():
    if userentry.get()=='' or passentry.get()=='':
        messagebox.showerror('Error','Fields cannot be empty')
    elif userentry.get()=='Sanjh' and passentry.get()=='4321':
        messagebox.showinfo('Success', 'Welcome to Student Management System')
        wd.destroy()
        import sms
    else:
        messagebox.showwarning('Wrong Entries','Enter correct Username or Password')


# Window 
wd = Tk()

wd.geometry('1200x600+90+70')
wd.resizable(False, False)

wd.title('Login Page')
icon = PhotoImage(file='icon.png')
wd.wm_iconphoto(False, icon)

bgImg = ImageTk.PhotoImage(file='bgimg.jpg')
bgLabel = Label(wd, image=bgImg)
bgLabel.place(x=0, y=0)

# login box
loginframe = Frame(wd, pady=20)
loginframe.place(x= 400, y= 150)

logoimg = PhotoImage(file='logoimg.png')
logolabel = Label(loginframe, image= logoimg)
logolabel.grid(row=0, column=0, columnspan=2, pady=10)

# Username
userimg = PhotoImage(file='user.png')
userlabel = Label(loginframe, image=userimg, text='Username', compound=LEFT, font=('times new roman', 16, 'bold'))
userlabel.grid(row=1,column=0, padx=20)

userentry = Entry(loginframe, font=('times new roman', 14, 'bold'), bd= 5, fg='#36648B')
userentry.grid(row=1, column=1, padx=20)

# Password
passimg = PhotoImage(file='password.png')
passlabel = Label(loginframe, image=passimg, text='Password', compound=LEFT, font=('times new roman', 16, 'bold'))
passlabel.grid(row=2,column=0, pady=10, padx=20)

passentry = Entry(loginframe, font=('times new roman', 14, 'bold'), bd= 5, fg='#36648B')
passentry.grid(row=2, column=1, padx=20, pady=20)


# login Button 
loginbutton = Button(loginframe, text="Login", padx=20, bg='#27408B', font=('times new roman', 12, 'bold'), fg='white', activebackground='#4876FF', cursor='hand2', command=login)
loginbutton.grid(row=3, column=0, columnspan=2)





wd.mainloop()