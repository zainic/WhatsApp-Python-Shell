from openwa import WhatsAPIDriver
import numpy as np
import matplotlib.pyplot as plt
import time
import os, sys
import random
import cv2

# function for interrupt detection
def detect(timer):
    try:
        print('no')
        time.sleep(timer)
        return False
    except KeyboardInterrupt as e:
        return True

# Execute code
def run(code):
    try:
        exec(code)
        output = "success"
    except Exception as e:
        output = str(e)
        print(e)
        print(type(e))
    return output

# Initial Login
driver = WhatsAPIDriver()
chat_id = "120363041488034042@g.us"
exit = False

# Check Login
while driver.wait_for_login() == False:
    print("The user currently not login")
    time.sleep(5)
    
# User already login
print("The user has been login")

while True:
    # Check if server still connected
    if not driver.is_connected():
        print("Connecting To Server")
        if detect(2):
            exit = True
            break
        continue
    
    # Check if there are new message
    while True:
        new_messages = driver.get_unread_messages_in_chat(chat_id, include_me=True)
        if not driver.is_connected():
            print("Connecting To Server")
            if detect(2):
                exit = True
                break
            continue
        if len(new_messages) == 0:
            print("No messages Detected")
            if detect(1):
                exit = True
                break
        else:
            print("Message Detected")
            break
            
    # Check exit
    if exit:
        break
    
    # Get command message and run it
    for message in new_messages:
        # Check the command keyword
        if message.type in ['image','video','sticker']:
            continue
        if message.content[0] == "\\":
            command = message.content.split('\n')
            first_line = command[0].split()
        else:
            continue
        
        if first_line[0] == '\\run':
            code = "\n".join(command[1:])
            output = run(code)
            message.reply_message(output)
            
            
        
            
            
    