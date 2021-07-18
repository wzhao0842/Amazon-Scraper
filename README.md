# Amazon-Tracker Description and User Guide

A desktop GUI application for tracking and search products in Amazon (using Python)

Language: Python
Required Install Libraries: selenium, smtplib, threading, Pillow
Idea:   GUI using tkinter, Backend using selenium to scrap the html code in the website. The data of two main utilities, search and track, are stored 
in two different json files. All files for this application are in the same folder, be careful when choosing where the folder is downloaded, because the path is
important. 

(Go to stack overflow for any questions)
(After you download it from github in your local disk)
Steps in How To Use:
# 1. Install Python

Python is a programming language. By installing it in your computer through terminal, you can run any executable files with the suffix ".py" by simply type
"python <your filename>".  ex: "python script.py"

Go to https://python.org.
Click Downloads on the top menu bar and download the newest version of Python (make sure download the correct type base on your system, Windows, Mac, or Linux)
Go to your terminal or command line and type "python --version", if you see the python version pops up, then you are good to go.

# 2. Install pip

pip is a installation tool of python, with "pip" you can install any libraries in python.
if your python version is the newest, or downloaded from python.org recently, otherwise, I recommend you to check out this installation guide website:
https://pip.pypa.io/en/stable/installing/

Nice, you finally make to here! Almost done, hold on!
  
# 3. Install Libraries
 
In your terminal, give the following commands one by one. 
pip install selenium
pip install threading
pip install Pillow 
pip install smtplib
  
# 4. Download a Google Chrome version 89 
  
  Why? Because this application use this specific Chrome version as search engine, it's also faster and consuming less computational power. 
  
  Go to this website and download, make sure to choose the 64 bit one. https://chrome.softwaredownload.co.in/chrome-89-0-4389. Be careful the Path. 
  
# 5. Edit the Path in the Program
  
Go click the frontend.py and backend.py, change where the comment need you to change. 
How to get the path of a file? 
  1. open terminal
  2. open file in UI 
  3. drag that file to terminal
  4. you will see the path of that file

# 6. All Installation Done!
  Run your Application by typing "python frontend.py" in terminal. If you want to stop it, click ctrl-d or ctrl-z.
  
Note: further updates will be included. If you having any questions, you can reachout to my email wzhao0842@gmail, I will be answer you back in 48 hours.




