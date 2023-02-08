#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Presenter Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Production"

from InquirerPy import prompt, inquirer, get_style
from InquirerPy.validator import NumberValidator
from termcolor import colored

class Inquiry(object):
    """
    All kind of display methods.
    """

    def __init__(self):
        """
        Constructor - As of now, nothing have to initialize.
        """
        pass

    def ask_text(self, message=None):
        """
        This method will ask a text based question
        and revert with key value based answer.
        """
        def ask(count, message):
            if count == 3:
                print(colored("You have lost all 3 attempts, Please try again.", 'red', attrs=['bold']))
            else:
                try:
                    style = get_style({"question": "#1FFF00", "answer": "#00B2FF"}, style_override=False)
                    name = inquirer.text(message=message, style=style).execute()
                    if not name:
                        count = count +1
                        print(colored("Try Again!", 'yellow', attrs=['bold']))
                        return ask(count, message)
                    else:
                        return name
                except KeyboardInterrupt:
                    count = count +1
                    return ask(count, message)
               
        response = ask(0, message)
        return response

