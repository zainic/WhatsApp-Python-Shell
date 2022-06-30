logs = {
    '1.0' : {
        'Description' : "Create python shell in WhatsApp. It's allow us to connect the phone and PC using WhatsApp. We can take any file from our PC without even we touch it again. The full tutorial and how to setup the bot is on my github https://github.com/zainic/WhatsApp-Python-Shell",
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
}