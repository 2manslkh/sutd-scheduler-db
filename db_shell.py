# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 13:32:57 2019

@author: kengh
"""
import sys

def main(argv):
    while(True):
        user_input = input("What is your name?")
        print("hello, " + user_input)
    
if __name__ == "__main__":
   main(sys.argv[0:])