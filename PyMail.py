from tkinter import *
from email.message import EmailMessage
import ssl
import smtplib
import imghdr
import imaplib
import email
from tkinter import filedialog as fd
from tkinter import messagebox, simpledialog

#Functions
def compose():
    #Get Info
    your_email = simpledialog.askstring('Email', 'What is your email?')
    receiver = simpledialog.askstring('Recipients', 'Who do you want to send it to?')
    password = simpledialog.askstring('Password', 'What is your password?')
    subject = simpledialog.askstring('Subject', 'What is the subject?')
    body = simpledialog.askstring('Body', 'What do you want to say?')

    #Technical Module Things
    email = EmailMessage()
    email['From'] = your_email
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(body)

    #Adding Images
    fileif = simpledialog.askstring('File', 'Do you want to attach an image? [y/n]')
    if fileif == 'y':
        file = fd.askopenfilename()
        with open(file, 'rb') as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
            file_name = f.name
            email.add_attachment(file_data, maintype="image", subtype=file_type, filename=file_name)

    elif fileif == 'n':
        pass

    send = simpledialog.askstring('Send', 'Type in any key to send.')
    
    #Server Stuff
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(your_email, password)
        server.sendmail(your_email, receiver, email.as_string())

    messagebox.showinfo('Success', 'Success')

def read_emails():
    imap_server = "imap.gmail.com"
    email_address = simpledialog.askstring('Email', 'What is your email?')
    password = simpledialog.askstring('Password', 'What is your password')
    
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(email_address, password)

    messagebox.showinfo('WARNING', 'This will read every email in your inbox. It may take a while to list them all out. Please consider limiting the size of your inbox on mail.google.com')
    

    imap.select("Inbox")

    _, msgnums = imap.search(None, "ALL")


    for msgnum in msgnums[0].split():


        _, data = imap.fetch(msgnum, "(RFC822)")

        message = email.message_from_bytes(data[0][1])

        print(f"From: {message.get('From')}")
        print(f"BCC: {message.get('BCC')}")
        print(f"Date: {message.get('Date')}")
        print(f"Subject: {message.get('Subject')}")
		
        print("Content:")
        for part in message.walk():
            if part.get_content_type() == 'text/plain':
                print(part.as_string())

        print("===========================")
	
	contin = simpledialog.askstring("Continue? [y/n]")
	if contin == 'y':
		pass
	else:
		break
	
        
    

#Create Window
screen = Tk()
window_title = screen.title('PyMail')
canvas = Canvas(screen, width=400, height=275)
canvas.pack()

#Title/Logo
title = Label(screen, text="PyMail", font=(None, 60))
canvas.create_window(200,70, window=title)

#Menu Option Buttons
send_btn = Button(screen, text="Compose Email", command=compose)
read_btn = Button(screen, text="Read Emails", command=read_emails)
canvas.create_window(200,130, window=send_btn)
canvas.create_window(200,170, window=read_btn)

#Text
criteria = Label(screen, text="This service uses gmail.", font=(None, 10))
canvas.create_window(200,250, window=criteria)

screen.mainloop
