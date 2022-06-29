from openwa import WhatsAPIDriver
import numpy as np
import matplotlib.pyplot as plt
import time
import io
import inspect
import os, sys
import re

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
        fail = True
    except Exception as e:
        sys.stdout = old_stdout
        output = str(e)
        print(e)
        print(type(e))
        fail = True
    return output, fail

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
            if detect(5):
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

user_id = input("Input your number using your country code for first digit and end with @c.us \nEx : 6281349237723@c.us (62 for Indonesia)\ninput here :")
chat_id = input("Input your group id or chat id for place the bot\nThe instruction to get the id would be on README\ninput here :")

def start(only_me = True, chat_id = chat_id, user_id = user_id):
    # if only_me set to be True, only you can use this command
    # chat_id can be customized
    banned_id = []
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
            try:
                if message.content[0] == "\\":
                    if only_me == True and sender_id != user_id:
                        print("This user can't use the bot")
                        continue
                    if sender_id in banned_id:
                        print("user banned")
                        message.reply_message(f"sorry sir {sender_id} you have been banned")
                        continue
                    command = message.content.split('\n')
                    first_line = command[0].split()
                else:
                    continue
            except Exception as e:
                print(e)
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
                print("Exit the bot")
                break
            
            if first_line[0] == '\\home':
                """
                Bot move to user id
                It prevent spamming from group
                """
                chat_id = user_id
            
            if first_line[0] == '\\ban':
                """
                This function allow us to ban someone from using this bot
                
                To ban the number:
                '\ban number_id@c.us'
                Ex :
                '\ban 6281234567890@c.us'
                
                (without using '')
                """
                if first_line[1] != user_id:
                    banned_id.append(first_line[1])
                    message.reply_message(f"successfully ban {first_line[1]}")
                else:
                    message.reply_message(f"failed to ban {first_line[1]} because he's the creator")
            
            if first_line[0] == '\\whitelist':
                """
                This function allow us to remove someone from banned using this bot
                
                To whitelist/unban the number:
                '\whitelist number_id@c.us'
                Ex :
                '\whitelist 6281234567890@c.us'
                
                (without using '')
                """
                if sender_id == user_id:
                    if first_line[1] in banned_id:
                        banned_id.remove(first_line[1])
                        message.reply_message(f"whitelist {first_line[1]}")
                    else:
                        print("the number is not in banned list")
                        message.reply_message(f"{first_line[1]} is not in banned list")
                else:
                    message.reply_message(f"You are not allowed whitelist someone")
            if first_line[0] == '\\change':
                """
                This function allow us to change the target of bot or move the bot's place
                
                To move into personal chat:
                '\change number_id@c.us'
                Ex :
                '\change 6281234567890@c.us'
                
                To move into group:
                '\change group_id@g.us'
                Ex :
                '\change 120363041488034042@g.us'
                
                (without using '')
                """
                new_chat_id = first_line[1]
                id_type = new_chat_id[-4:]
                if id_type == "c.us":
                    stat = driver.check_number_status(new_chat_id).status
                    if stat == 200:
                        chat_id = new_chat_id
                        message.reply_message(f"Success to move to {new_chat_id}")
                        print("Success to move")
                    else:
                        message.reply_message(f"Failed to move to {new_chat_id} because user inactive or invalid number")
                        print("User inactive or not valid number")
                elif id_type == "g.us":
                    member = driver.group_get_participants_ids(new_chat_id)
                    if len(member) > 0:
                        chat_id = new_chat_id
                        message.reply_message(f"Success to move to {new_chat_id}")
                        print("Success to move")
                    else:
                        message.reply_message(f"Failed to move to {new_chat_id} because of not participant of this group or invalid group")
                        print("You are not participant of this group or invalid group")
                else:
                    message.reply_message(f"Cannot move to {new_chat_id} because of invalid id")
                    print("Failed to move the bot because of invalid id")
            
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
                output, _ = run(code)
                message.reply_message(str(output))
                
            if first_line[0] == '\\runs':
                """
                This function similar to run command but it allow us to send to specific person.
                It can be multiple of them.
                
                Ex :
                '\runs chat_id1 chat_id2 chat_id3
                f = lambda x: x+5
                y = f(5)
                print(y)'
                
                (without using '' and the output code will be send to those id)
                (can be more than 3)
                
                the output would be:
                10
                and it'll send to those id
                
                - If there is an exception, it'll send the exception and the type of exception
                - If you declare function and want call it later write 'global function' before define the function
                """
                code = "\n".join(command[1:])
                output, fail = run(code)
                if fail:
                    message.reply_message(str(output) + "\nNot continue sending message")
                    continue
                i = 0
                total = len(first_line[1:])
                for id_number in first_line[1:]:
                    try:
                        driver.chat_send_message(id_number, str(output))
                        i += 1
                    except:
                        print(f"Failed to send to {id_number}")
                message.reply_message(f"sent {i} from {total} detected")
                
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
                
                To send the file from current dir (use "" for each file)
                '\send "name_file1" "name_file2"'
                note : if you want to send folder, you need to archive it first
                
                To exit the explorer type this command
                '\quit'
                
                """
                try:
                    regex = r'"([^\"]*)"'
                    path_folder = re.search(regex, cmd[0]).groups()[0]
                    directory = os.path.join(path_folder)
                    _ = os.listdir(directory)
                except:
                    try:
                        message.reply_message(f"directory {path_folder} is doesn't exist")
                    except:
                        pass    
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
                        try:
                            if msg.content[0] == "\\":
                                if only_me == True and sender_id2 != user_id:
                                    print("This user can't use the bot")
                                    continue
                                cmd = msg.content.split('\n')
                                first = cmd[0].split()
                            else:
                                continue
                        except Exception as e:
                            print(e)
                            continue
                            
                        if first[0] == '\\quit':
                            """
                            Exit the virtual explorer
                            """
                            quit = True
                            break
                        
                        elif first[0] == '\\run':
                            """
                            Run python command
                            """
                            code = "\n".join(cmd[1:])
                            output, _ = run(code)
                            msg.reply_message(str(output))
                        
                        elif first[0] == '\\cd':
                            """
                            Open the folder or navigate the explorer
                            """
                            show = True
                            regex = r'"([^\"]*)"'
                            temp_dir = directory
                            try:
                                folder = re.search(regex, cmd[0]).groups()[0]
                            except:
                                folder = first[1]
                            directory = os.path.join(directory, folder)
                            print(f"current directory {directory}")
                            
                        elif first[0] == "\\send":
                            """
                            Send file from current dir
                            """
                            regex = r'"([^\"]*)"'
                            files = re.findall(regex, cmd[0])
                            for file in files:
                                try:
                                    path = os.path.join(directory, file)
                                    print(f"Sending {file} to WhatsApp")
                                    driver.send_media(path, chat_id, str(file))
                                    print("File sent successfully")
                                except:
                                    msg.reply_message(f"file {file} is doesn't exist or file is not support to send")
                                    print("Failed to send file")
                                    
                print("Quitting the explorer")
                msg.reply_message("Quitting the explorer")
                
            if first_line[0] == "\\sticker":
                """
                This function will allow us to convert any image into sticker in WhatsApp
                
                Ex:
                \sticker 
                (send it first)  
                
                Then
                it will wait the command sender to upload the image
                
                it should return picture into sticker once they send the image
                """ 
                sender_id = message.sender.id
                while True:
                    time.sleep(4)
                    pictures = driver.get_unread_messages_in_chat(chat_id, include_me=True)
                    msgs = [msg.sender.id for msg in pictures]
                    pic_check = [X.type == 'image' or X.type == 'video' for X in pictures]
                    if message.sender.id in msgs and any(pic_check) == True:
                        print("Picture was detected")
                        break
                    print("No pictures were detected")
                    
                for picture in pictures:
                    name = picture.filename
                    try:
                        _ = os.listdir(os.path.join(".","temp"))
                    except FileNotFoundError:
                        os.mkdir(os.path.join(".","temp"))
                    try:
                        print("Try to download the image to local directory")
                        picture.save_media(os.path.join(".","temp"), force_download=True)
                    except:
                        print("Failed to download")
                        message.reply_message("Failed to download file because couldn't connect to server")
                        continue
                    path = os.path.join(".", "temp", name)
                    i = 1
                    print("Uploading the sticker")
                    while i <= 5:
                        try:
                            print("Trying number " + str(i))
                            driver.send_image_as_sticker(path, chat_id)
                            break
                        except:
                            print("Failed to upload")
                            i += 1
                    if i > 5:
                        print("Maximum trial exceed")
