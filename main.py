# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 13:32:57 2019

@author: kengh
"""
import sys
from db_helper import db_helper

def main(argv):
    login_db = db_helper("login_database.json")
    login_db = login_db.data[list(login_db.data.keys())[0]]
    users = list(login_db.keys())
    print("SUTD DATABASE SCHEDULER LOGIN\n")
    
    while(True):
        
        username = input("username:")
        if username in users:
            print("hello, " + username)
            password = input ("password:")
            if str(password) == login_db[username]["password"]:
                print("login success")
                print("Welcome, {} {}, you have level {} access."
                      .format(login_db[username]["First Name"],
                      login_db[username]["Last Name"],
                      login_db[username]["Admin Level"]))
            else:
                print("login failure")
        else:
            print("invalid user")
    
if __name__ == "__main__":
   main(sys.argv[0:])