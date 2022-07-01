logs = {
    '1.0' : {
        'Description' : "Create python shell in WhatsApp. It's allow us to connect the phone and PC using WhatsApp. We can take any file from our PC without even we touch it again. The full tutorial and how to setup the bot is on my github https://github.com/zainic/WhatsApp-Python-Shell",
        'Changes' : [
            "It has no changes yet"
        ],
        'Added Commands' : {
            'help' : 'Show list of command and its utility.',
            'home' : 'Place or move the bot to user id or operator id',
            'change' : 'Move the bot to specific number or group id',
            'run' : 'Run python code and send the output to whatsapp.',
            'runs' : 'Similar to run but it can be multiple number.',
            'add' : 'Create your own command here.',
            'ban' : 'Ban number id from using this bot command',
            'whitelist' : 'Unban number id for using this bot command again',
            'sticker' : 'Make sticker from any image the command sender sent',
            'open_dir' : 'Open directory like explorer.',
            'cd' : 'Subcommand from open_dir to navigate the explorer.',
            'send' : 'Subcommand from open_dir to send file from current dir.',
            'quit' : 'Subcommand from open_dir to quit the explorer.',
            'exit' : 'Exit the bot.'
        },
        'Fixed Bugs' : [
            'This is early version of WhatsApp Bot, The bugs fixes will described in next update',
        ],
        'Known bugs' : [
            'The open_dir command output is not align.',
            'The message sometimes detected twice, so the output also twice.',
            'The runs command sometimes failed to send the message.',
        ],
    },
    '1.1' : {
        'Description' : "Hey there, Now the bot can be placed in multiple chat room or groups. The operator (someone that can control the bot) can be multiple. This update mostly for security things and operator only command. Also now you can see the version log by using \\version command to see how the program was developed. There is also some bug fixes from previous version",
        'Changes' : [
            "The command home, exit, change, ban, and whitelist now only can be used by operator.",
            "Change chat_id variable to list since it now can be more than one place.",
            "Create version logs",
            "Operator can be multiple",
        ],
        'Added Commands' : {
            'version' : 'Show list of version and its change logs.',
            'duplicate' : 'Duplicate the place of bot.',
            'remove' : 'Show list of version and its change logs.',
            'toggle_only_me' : 'Toggle the only me variable for using the bot.',
            'version' : 'Show list of version and its change logs.',
            'add_op' : 'Add someone to being operator',
            'remove_op' : 'remove someone from being operator',
        },
        'Fixed Bugs' : [
            'The open_dir command output is now aligned.',
            'The message no longer sometimes detected twice.'
        ],
        'Known bugs' : [
            'The runs command sometimes failed to send the message.',
            'When sending files from PC often to be failed.',
        ],
    },
}