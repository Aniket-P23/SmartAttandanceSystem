# import modules

from tkinter import *
from PIL import ImageTk,Image
import os


from MyQR import myqr
import os
import base64
import pybase64
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import sys
import time








def generateqr():
    f = open('students.txt', 'r')
    lines = f.read().split("\n")
    print(lines)
    for i in range(0, len(lines)):
        data = lines[i].encode()
        name = base64.b64encode(data)
        version, level, qr_name = myqr.run(
            str(name),
            level='H',
            version=1,

        # background

        picture='bg.jpg',
        colorized=True,
        contrast=1.0,
        brightness=1.0,
        save_name=str(lines[i] + '.bmp'),
        save_dir=os.getcwd()
    )





def sendqr():
    from selenium import webdriver
    from time import sleep

    driver = webdriver.Chrome()
    driver.get('https://web.whatsapp.com/')

    name = input('Enter the name of user or group : ')
    filepath = input('Enter your filepath (images/video): ')

    input('Enter anything after scanning QR code')

    user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
    user.click()

    attachment_box = driver.find_element_by_xpath('//div[@title = "Attach"]')
    attachment_box.click()

    image_box = driver.find_element_by_xpath(
        '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
    image_box.send_keys(filepath)

    sleep(3)

    send_button = driver.find_element_by_xpath('//span[@data-icon="send-light"]')
    send_button.click()







def takeattendance():
    cap = cv2.VideoCapture(0)

    names = []

    # function for writing the data into text file
    fob = open('attendence.txt', 'a+')

    def enterData(z):
        if z in names:
            pass
        else:
            names.append(z)
            z = ''.join(str(z))
            fob.write(z + '\n')
        return names

    print('Reading...')

    # function for check the data is present or not
    def checkData(data):
        data = str(data)
        if data in names:
            print('Already Present')
        else:
            print('\n' + str(len(names) + 1) + '\n' + 'present done')
            enterData(data)

    while True:
        _, frame = cap.read()
        decodedObjects = pyzbar.decode(frame)
        for obj in decodedObjects:
            checkData(obj.data)
            time.sleep(1)

        cv2.imshow("Smart Attendance System", frame)

        # closing the program when s is pressed
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.destroyAllWindows()
            break

    fob.close()


#Designing window for registration

def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")

    register_screen.configure(background="red")


    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Please enter details below", bg="green").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="green", command=register_user).pack()


# Designing window for login

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login",bg="green").pack()
    Label(login_screen, text="").pack()

    login_screen.configure(background="red")


    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command=login_verify,bg="green").pack()




# Implementing event on register button

def register_user():
    username_info = username.get()
    password_info = password.get()

    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()


# Implementing event on login button

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()

        else:
            password_not_recognised()

    else:
        user_not_found()


# Designing popup for login success

def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Welcome")
    login_success_screen.geometry("300x250")
    Label(login_success_screen, text="Login Success | Choose following operations",bg="yellow").pack()
    Button(login_success_screen, text="Generate QR Code/id",height="2", width="30", command=generateqr,bg="green").pack()
    Button(login_success_screen, text="Send QR Code/id",height="2", width="30", command=sendqr,bg="green").pack()
    Button(login_success_screen, text="Take Attendance", height="2", width="30", command=takeattendance,bg="green").pack()

    login_success_screen.configure(background="red")


    #Button(text="Teacher Registration", height="2", width="30", command=register).pack()




# Designing popup for login invalid password

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()


# Designing popup for user not found

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()


# Deleting popups

def delete_login_success():
    login_success_screen.destroy()


def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()


# Designing Main(first) window

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Smart Attendance System")

    main_screen.configure(background="red")



    Label(text="Smart Attendance System", bg="green", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Teacher Login", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Teacher Registration", height="2", width="30", command=register).pack()




    main_screen.mainloop()


main_account_screen()