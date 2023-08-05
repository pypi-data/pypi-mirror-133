#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Chia Wei Lim
# Created Date: 2021-12-08
# version ='1.0'
# ---------------------------------------------------------------------------
"""Logging for file analysis"""
# ---------------------------------------------------------------------------
import os
import logging
from .customdatetime import CustomDateTime

class CustomLog:
    """
    Create logs 
    DEBUG < INFO < WARNING < ERROR < CRITICAL
    """

    logformat = {'notebook': '%(asctime)s %(levelname)s: %(message)s', 'script': '%(asctime)s %(levelname)s %(filename)s:%(lineno)s - %(funcName)s(): %(message)s'}

    def __init__(self, logfile = None,logpath = None, loglevel = logging.INFO, suppressmessage = False, isnotebook = False):

        if logpath is None: 

            logpath = os.path.abspath(os.getcwd())

        elif os.path.exists(logpath) is False:

            newpath = os.path.abspath(os.getcwd())

            if not suppressmessage:
                
                print("Log path assigned not exist. Reassign to current path: " + newpath)

            logpath = newpath

        if logfile is None:

            logfile = CustomDateTime().now() + ".log"#create with current date and time if not specified

        logfullpath = os.path.join(logpath, logfile)
        
        logging.basicConfig(filename = logfullpath, 
            level = loglevel,
            format= self.logformat["notebook"] if isnotebook is True else self.logformat["script"],
            datefmt='%Y-%m-%d %H:%M:%S') 
        
        if not suppressmessage:
            print("Loggingfile at " + logfullpath)

    def add_line_separator(self):

        logging.info('---------------------------------------------------------------------------')

    def debug(self, message):
        
        logging.debug(message)

    def info(self, message):
        
        logging.info(message)

    def warning(self, message):
        
        logging.warning(message)

    def error(self, message):
        
        logging.error(message)

    def critical(self, message):
        
        logging.critical(message)

