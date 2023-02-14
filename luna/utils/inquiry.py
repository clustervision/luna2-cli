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

import os
import sys
from InquirerPy import inquirer, get_style
from termcolor import colored

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

    def ask_text(self, message=None, update=None):
        """
        This method will ask a text based question
        and revert with key value based answer.
        """
        def ask(count, message, update):
            if count == 3:
                error_message = "You have lost all 3 attempts, Please try again."
                print(colored(error_message, 'red', attrs=['bold']))
                sys.exit(0)
            else:
                try:
                    name = inquirer.text(message=message, style= self.style).execute()
                    if update:
                        return name
                    if not name:
                        print(colored("Try Again!", 'yellow', attrs=['bold']))
                        count = count +1
                        return ask(count, message, update)
                    else:
                        return name
                except KeyboardInterrupt:
                    print(colored("Exited! Try Again, with new Inputs.", 'red', attrs=['bold']))
                    sys.exit(0)
        response = ask(0, message, update)
        return response


    def ask_number(self, message=None, update=None):
        """
        This method will ask a text based question
        and revert with key value based answer.
        """
        def ask(count, message, update):
            if count == 3:
                error_message = "You have lost all 3 attempts, Please try again."
                print(colored(error_message, 'red', attrs=['bold']))
                sys.exit(0)
            else:
                try:
                    name = inquirer.number(
                        message = message,
                        style = self.style,
                        # validate = NumberValidator(),
                        default = None
                    ).execute()
                    if update:
                        return name
                    if not name:
                        print(colored("Try Again!", 'yellow', attrs=['bold']))
                        count = count +1
                        return ask(count, message, update)
                    else:
                        return name
                except KeyboardInterrupt:
                    print(colored("Exited! Try Again, with new Inputs.", 'red', attrs=['bold']))
                    sys.exit(0)
        response = ask(0, message, update)
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


    def ask_secret(self, message=None, update=None):
        """
        This method will ask a text based question
        and revert with key value based answer.
        """
        def ask(count, message, update):
            if count == 3:
                error_message = "You have lost all 3 attempts, Please try again."
                print(colored(error_message, 'red', attrs=['bold']))
                sys.exit(0)
            else:
                try:
                    name = inquirer.secret(
                        message = message,
                        style = self.style,
                        transformer=lambda _: "[hidden]"
                    ).execute()
                    if update:
                        return name
                    if not name:
                        print(colored("Try Again!", 'yellow', attrs=['bold']))
                        count = count +1
                        return ask(count, message, update)
                    else:
                        return name
                except KeyboardInterrupt:
                    print(colored("Exited! Try Again, with new Inputs.", 'red', attrs=['bold']))
                    sys.exit(0)
        response = ask(0, message, update)
        return response


    def ask_select(self, message=None, choices=None):
        """
        This method will provide some choices to
        select the desired input.
        """
        response = False
        try:
            response = inquirer.select(
                message = message,
                style = self.style,
                choices = choices,
                default = None,
            ).execute()
        except KeyboardInterrupt:
            print(colored("Exited! Try Again, with new Inputs.", 'red', attrs=['bold']))
            sys.exit(0)
        return response


    def ask_file(self, message=None, update=None):
        """
        This method will ask a text based question
        and revert with key value based answer.
        """
        def ask(count, message, update):
            if count == 3:
                error_message = "You have lost all 3 attempts, Please try again."
                print(colored(error_message, 'red', attrs=['bold']))
                sys.exit(0)
            else:
                try:
                    home_path = "/" if os.name == "posix" else "C:\\"
                    name = inquirer.filepath(message=message, style= self.style, default=home_path).execute()
                    if update:
                        return name
                    if not name:
                        print(colored("Try Again!", 'yellow', attrs=['bold']))
                        count = count +1
                        return ask(count, message, update)
                    else:
                        return name
                except KeyboardInterrupt:
                    print(colored("Exited! Try Again, with new Inputs.", 'red', attrs=['bold']))
                    sys.exit(0)
        response = ask(0, message, update)
        return response
