# WhatsApp-Python-Shell v1.0
Create python shell in WhatsApp. It's allow us to connect the phone and PC using WhatsApp

## Requirement
1. Python version 3.8 or above 

    https://www.python.org/downloads/

2. Installed the geckodriver

    https://sourceforge.net/projects/geckodriver.mirror/

3. Installed this following python modules:

    ```
    python-dateutil>=2.6.0
    selenium>=3.4.3
    six>=1.10.0
    openwa 
    python-axolotl
    cryptography
    numpy
    matplotlib
    typing
    Pillow
    requests
    python-magic
    ```
    
4. Stable Internet Connection
    
## How to Setup

### Step 1
Clone this github

    git clone https://github.com/zainic/WhatsApp-Python-Shell.git
    
To your local repository, then
    
    cd WhatsApp-Python-Shell

### Step 2
Open python shell inside command prompt

Your command prompt appearance would be look like this
    
![python-shell](https://user-images.githubusercontent.com/96677002/176366207-d251a6ae-9cfb-4915-8f5c-911b369a7ec7.png)

### Step 3
Import the main program

    from main import *

This will immediately open the web-driver and login with QR code

### Step 4
Input your chat id and target chat id it could be group or personal chat

If you didnt know the target chat id, just enter it empty 

How to get chat id is write this on your python shell

* To get all chat ids in your WhatsApp : `driver.get_all_chats()` 
    
* To only get all groups : `driver.get_all_groups()` 
    
### Step 5
If you already input all ids in the first time, to run the bot just run this function

    start()
    
if you want other people use this bot in group, add `only_me=False` parameter, `True` as default 

    start(only_me=False)

If you haven't input the target chat id, add `chat_id` parameter

    start(chat_id="your_chat_id_target")

`your_chat_id_target` fill with your target chat id

After that you can run the command in your WhatsApp

## How to Use It

### run
This function allows us to run python program like in command prompt or shell.


Ex :

```
\run
f = lambda x: x+5
y = f(5)
print(y)
```

(the code should be in the next line after initial command.)
                
the output would be:

`10`

and it'll send to WhatsApp.
                

- If there is an exception, it'll send the exception and the type of exception.

- If you declare function and want call it later write `global function` before define the function.

### runs

This function similar to run command but it allow us to send to specific person.

It can be multiple of them.
                
Ex :

```
\runs chat_id1 chat_id2 chat_id3
f = lambda x: x+5
y = f(5)
print(y)
```
                
(the output code will be send to those id and it can be more than 3)
                
the output would be:

`10`

and it'll send to those id
                
- If there is an exception, it'll send the exception and the type of exception to the place where the bot at.

- If you declare function and want call it later write 'global function' before define the function.

### add
This function allows us to add our own command using WhatsApp.
                
Ex:

```
\add function
def function(input1, input2):
  result = int(input1) + int(input2)
  output = result/2
  return output
```

(The function variable should be matched)
                
To run your function in WhatsApp, it should be

`\function input1 input2` 

note : remenber all input from WhatsApp are string.
                
Ex:

`\function 10 20`

The output should be

`15`
                
### open_dir

This function allows us to explore our PC's folder using WhatsApp.

It will disable other function while you use it except run command.
                
Ex:

`\open_dir file_path`
                    
(the default file_path is current github directory as ".")
                
To navigate your path you can use cd function like bash

`\cd name_folder` 

note : if file doesn't exist it won't move.
                
To send the file from current dir (use "" for each file)

`\send "name_file1" "name_file2"`

note : if you want to send folder, you need to archive it first.
                
To exit the explorer type this command

`\quit`

### sticker

This function will allow us to convert any image into sticker in WhatsApp.
                
Ex:

`\sticker` 

(send it first)  
                
Then, it will wait the command sender to upload the image.
                
It should return picture into sticker once they send the image.

### change

This function allow us to change the target of bot or move the bot's place.
                
To move into personal chat:

`\change number_id@c.us`

Ex :

`\change 6281234567890@c.us`
                
To move into group:

`\change group_id@g.us`

Ex :

`\change 120363041488034042@g.us`

### ban

This function allow us to ban someone from using this bot.
                
To ban the number:

`\ban number_id@c.us`

Ex :

`\ban 6281234567890@c.us`

### whitelist

This function allow us to remove someone from banned using this bot.
                
To remove number from ban:

`\whitelist number_id@c.us`

Ex :

`\whitelist 6281234567890@c.us`

### home

`\home`

Bot move to user id.
                
It prevent spamming from group.
                
### exit

`\exit`

Exit the connection to driver.
