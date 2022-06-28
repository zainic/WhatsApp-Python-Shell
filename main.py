from ast import arguments
from openwa import WhatsAPIDriver
import numpy as np
import matplotlib.pyplot as plt
import time
import io
import inspect
import os, sys
import random
import cv2

# function for interrupt detection
def detect(timer):
    try:
        print('no')
        time.sleep(timer)
        return False
    except KeyboardInterrupt:
        return True

# Execute code
def run(code):
    try:
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        exec(code)
        
        sys.stdout = old_stdout
        
        output = new_stdout.getvalue()
        print(output)
    except Exception as e:
        output = str(e)
        print(e)
        print(type(e))
    return output

# Initial Login
driver = WhatsAPIDriver()
chat_id = "120363041488034042@g.us"
exit = False
LIST_COMMANDS = []

# Check Login
while driver.wait_for_login() == False:
    print("The user currently not login")
    time.sleep(5)
    
# User already login
print("The user has been login")

def main():
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
            
            for code_command in LIST_COMMANDS:
                exec(code_command)
            
            if first_line[0] == '\\run':
                """
                This function allows us to run python program like in command prompt or shell
                
                Ex :
                '\run
                f = lambda x: x+5
                y = f(5)
                print(y)'
                
                (without using '' and the code should be in the next line after initial command)
                
                the output would be:
                10
                and it'll send to WhatsApp
                
                If there is an exception, it'll send the exception and the type of exception
                """
                code = "\n".join(command[1:])
                output = run(code)
                message.reply_message(str(output))
                
            if first_line[0] == '\\add':
                """
                This function allows us to add our own command using WhatsApp
                
                Ex:
                '\add function output
                def function(input1, input2):
                    result = input1 + input2
                    output = result/2
                    return output'
                    
                (without using '' and the code should be in the next line after initial command)
                (The function and output variable should be matched)
                
                To run your function in WhatsApp, it should be
                '\function input1 input2' 
                
                Ex:
                '\function 10 20'
                The output should be
                15
                """
                code = "\n".join(command[1:])
                # post-processing to create function
                name_function = first_line[1]
                output = first_line[2]
                params = inspect.getfullargspec(name_function).args
                n = len(params)
                docs = f"""
                if first_line[0] == '\\{name_function}':
                    Arg = ''
                    if len(first_line[1:]) != 0:
                        for i, param in enumerate(first_line[1:]):
                            Arg += param
                            if i < {n}-1:
                                Arg += ','
                    old_stdout = sys.stdout
                    new_stdout = io.StringIO()
                    sys.stdout = new_stdout
                    
                    output_function = {name_function}(Arg)
                    print(output_function)
                    
                    sys.stdout = old_stdout
                    
                    output = new_stdout.getvalue()
                    message.reply_message(str(output))
                """
                LIST_COMMANDS.append(docs)
            
            
            
            
        
            
            
    