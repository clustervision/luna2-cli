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
import sys

class Inquiry(object):
    """
    All kind of display methods.
    """

    def __init__(self):
        """
        Constructor - As of now, nothing have to initialize.
        """
        self.styledict = {
            "questionmark": "#F91A00",
            "answermark": "#F91A00",
            "question": "#1FFF00",
            "answered_question": "#1FFF00",
            "answer": "#00B2FF",
            "input": "#00B2FF"
            }
        self.style = get_style(self.styledict, style_override=False)

    def ask_text(self, message=None):
        """
        This method will ask a text based question
        and revert with key value based answer.
        """
        def ask(count, message):
            if count == 3:
                print(colored("You have lost all 3 attempts, Please try again.", 'red', attrs=['bold']))
                sys.exit(0)
            else:
                try:
                    name = inquirer.text(message=message, style= self.style).execute()
                    if not name:
                        print(colored("Try Again!", 'yellow', attrs=['bold']))
                        count = count +1
                        return ask(count, message)
                    else:
                        return name
                except KeyboardInterrupt:
                    print(colored("Exited! Try Again, with new Inputs.", 'red', attrs=['bold']))
                    sys.exit(0)
               
        response = ask(0, message)
        return response


    def ask_number(self, message=None):
        """
        This method will ask a text based question
        and revert with key value based answer.
        """
        def ask(count, message):
            if count == 3:
                print(colored("You have lost all 3 attempts, Please try again.", 'red', attrs=['bold']))
                sys.exit(0)
            else:
                try:
                    name = inquirer.text(message=message, style= self.style, validate=NumberValidator()).execute()
                    if not name:
                        print(colored("Try Again!", 'yellow', attrs=['bold']))
                        count = count +1
                        return ask(count, message)
                    else:
                        return name
                except KeyboardInterrupt:
                    print(colored("Exited! Try Again, with new Inputs.", 'red', attrs=['bold']))
                    sys.exit(0)
               
        response = ask(0, message)
        return response


    def ask_confirm(self, message=None):
        """
        This method will ask a text based question
        and revert with key value based answer.
        """
        response = False
        try:
            response = inquirer.confirm(message=message, style= self.style, default=False).execute()
        except KeyboardInterrupt:
            print(colored("Exited! Try Again, with new Inputs.", 'red', attrs=['bold']))
            sys.exit(0)
        return response