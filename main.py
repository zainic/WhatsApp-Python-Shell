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

"""
This Program allow us to run the python code and return the output into WhatsApp.
Even you can create your own command in WhatsApp.

BIG CAUTION:
IF YOU ARE NOT CAREFULL THIS PROGRAM COULD CRASH YOUR ENTIRE PC.
BE CAREFULL WHATEVER WHOM YOU GONNA USE THIS PROGRAM WITH.
USE THIS PROGRAM WITH WHOEVER YOU TRUST.
"""

# function for interrupt detection
def detect(timer):
    try:
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
        sys.stdout = old_stdout
        output = str(e)
        print(e)
        print(type(e))
    return output

# Check new message
def check_new_message(driver, chat_id, include_me=True, exit=False):
    while True:
        new_messages = driver.get_unread_messages_in_chat(chat_id, include_me)
        if not driver.is_connected():
            print("Connecting To Server")
            if detect(2):
                exit = True
                break
            continue
        if len(new_messages) == 0:
            print("No messages Detected")
            if detect(3):
                exit = True
                break
        else:
            print("Message Detected")
            break
    return exit, new_messages

LIST_COMMANDS = []

def login():
    # Initial Login
    global driver
    driver = WhatsAPIDriver()

    # Check Login
    while driver.wait_for_login() == False:
        print("The user currently not login")
        time.sleep(5)
        
    # User already login
    print("The user has been login")
    return driver

driver = login()

def main(only_me = True, chat_id = "628568002060@c.us"):
    # if only_me set to be True, only you can use this command
    # chat_id can be customized
    exit = False
    while not exit:
        # Check if server still connected
        if not driver.is_connected():
            print("Connecting To Server")
            if detect(2):
                exit = True
                break
            continue
        
        # Check if there are new message
        exit, new_messages = check_new_message(driver, chat_id)
        
        # Get command message and run it
        for message in new_messages:
            sender_id = message.sender.id
            # Check the command keyword
            if message.type in ['image','video','sticker']:
                continue
            if message.content[0] == "\\":
                if only_me == True and sender_id != "628568002060@c.us":
                    print("This user can't use the bot")
                    continue
                command = message.content.split('\n')
                first_line = command[0].split()
            else:
                continue
            
            for i, code_command in enumerate(LIST_COMMANDS):
                """
                Checked the custom command
                """
                old_stdout = sys.stdout
                try:
                    exec(code_command)
                except Exception as e:
                    message.reply_message("The command couldn't run because of " + str(e) + "\nThe command removed from list")
                sys.stdout = old_stdout
                    
            
            if first_line[0] == '\\exit':
                """
                Exit the connection to driver
                """
                exit = True
                break
            
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
                
                - If there is an exception, it'll send the exception and the type of exception
                - If you declare function and want call it later write 'global function' before define the function
                """
                code = "\n".join(command[1:])
                output = run(code)
                message.reply_message(str(output))
                
            if first_line[0] == '\\add':
                """
                This function allows us to add our own command using WhatsApp
                
                Ex:
                '\add function
                def function(input1, input2):
                    result = int(input1) + int(input2)
                    output = result/2
                    return output'
                    
                (without using '' and the code should be in the next line after initial command)
                (The function variable should be matched)
                
                To run your function in WhatsApp, it should be
                '\function input1 input2' 
                note : remenber all input from WhatsApp are string
                
                Ex:
                '\function 10 20'
                The output should be
                15
                """
                code = "\n".join(command[1:])
                name_function = first_line[1]
                exec("global " + name_function)
                try:
                    exec(code)
                except Exception as e:
                    E = "Failed to run the code because of " + str(e)
                    print(E)
                    message.reply_message(str(E))
                    continue
                # post-processing to create function
                params = inspect.getfullargspec(eval(name_function)).args
                n = len(params)
                docs = f"""if first_line[0] == '\\\\{name_function}':
                    Arg = []
                    if len(first_line[1:]) != 0:
                        for param in first_line[1:]:
                            Arg.append(param)
                            
                    new_stdout = io.StringIO()
                    sys.stdout = new_stdout
                    
                    print({name_function}(*Arg))
                    
                    output = new_stdout.getvalue()
                    message.reply_message(str(output))
                """
                LIST_COMMANDS.append(docs)
                print(f"command {name_function} with parameters {params} was created")
            
            if first_line[0] == '\\open_dir':
                """
                This function allows us to explore our PC's folder using WhatsApp
                It will disable other function while you use it except run command
                
                Ex:
                '\open_dir file_path'
                    
                (without using '' and the default file_path is current github directory as ".")
                
                To navigate your path you can use cd function like bash
                '\cd name_folder' 
                note : if file doesn't exist it won't move
                
                To exit the explorer type this command
                '\quit'
                
                """
                try:
                    directory = os.path.join(first_line[1])
                except:
                    directory = os.path.join('.')
                show = True
                quit = False 
                msg = message
                while not quit:
                    if show:
                        old_stdout = sys.stdout
                        new_stdout = io.StringIO()
                        sys.stdout = new_stdout
                        try:
                            for i in os.listdir(directory):
                                print(i)
                        except:
                            print('failed to open directory')
                            directory = temp_dir
                        sys.stdout = old_stdout
                        output = new_stdout.getvalue()
                        msg.reply_message(str(output))
                        show = False
                    
                    # Check local new message
                    quit, messages = check_new_message(driver, chat_id, exit = quit)
                    
                    for msg in messages:
                        sender_id2 = msg.sender.id
                        # Check the command keyword
                        if msg.type in ['image','video','sticker']:
                            continue
                        if msg.content[0] == "\\":
                            if only_me == True and sender_id2 != "628568002060@c.us":
                                print("This user can't use the bot")
                                continue
                            cmd = msg.content.split('\n')
                            first = cmd[0].split()
                        else:
                            continue
                        
                        if first[0] == '\\quit':
                            """
                            Exit the virtual explorer
                            """
                            quit = True
                            break
                        
                        if first[0] == '\\run':
                            """
                            Run python command
                            """
                            code = "\n".join(cmd[1:])
                            output = run(code)
                            msg.reply_message(str(output))
                        
                        if first[0] == '\\cd':
                            """
                            Open the folder or navigate the explorer
                            """
                            show = True
                            temp_dir = directory
                            directory = os.path.join(directory, first[1])
                
                print("Quitting the explorer")
                msg.reply_message("Quitting the explorer")