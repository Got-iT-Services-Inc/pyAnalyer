#! /usr/bin/env python3
#############################################################
# Title: Come up with something good			    #
# Description: takes the xml output of nmap and does stuff  #
#   with it						    #
#                                                           #
# Version:                                                  #
#   * Version 1.0 03/05/2018 RC                             #
#                                                           #
# Author: Richard Cintorino (c) Richard Cintorino 2018      #
#############################################################

import sys, os, inspect

sCurPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

#For Module Libraries
sys.path.insert(0,sCurPath + '/pyConfig')
sys.path.insert(0,sCurPath + '/pyDebugger')

from Config import pyConfig
from Debug import pyDebugger

class NAnalyze:

   def __init__(self,Args=None):
      self.Debugger = pyDebugger(self,True,False)
      self.Debugger.Log("Starting NAnalyzer, nmap scan analyzer...")
      self.Debugger.Log("Intializing Configuration Class...")
      self.Config = pyConfig(sCurPath + "/config.ini",True)
      self.Debugger.__LogToFile = self.Config.Get("Debug_File")
      self.Debugger.SetDebugLevel(self.Config.Get("Debug_Level"))

      #Set Debug Levels
      self.DBLV1 = "INFO"
      self.DBLV2 = "VERBOSE"
      self.DBLV3 = "DEBUG"
      self.DBLV4 = ""
      self.DBLV5 = ""
      self.DBLV6 = "DUMP"
      self.DBLVWARN = "WARNNING"

      #BEGIN!
      self.ProcessArgs(Args)

   def ProcessArgs(self,Args):
      self.Debugger.Log("Processing command line arguments...",DebugLevel=self.DBLV1)
      self.Debugger.Log("Command line arguments are: '" + str(Args) + "'", DebugLevel=self.DBLV3)
      opts = {}  # Empty dictionary to store key-value pairs.
      while Args:  # While there are arguments left to parse...
         if Args[0][0] == '-':  # Found a "-name value" pair.
            opts[Args[0]] = Args[1]  # Add key and value to the dictionary.
         Args = Args[1:]  # Reduce the argument list by copying it starting from index 1.
      if not '-i' in opts:
         opts['-i'] = input("Enter the file you want to process: ")
      self.Debugger.Log("Processing input file '" + opts['-i'] + "'...", DebugLevel=self.DBLV1)


if __name__ == '__main__':

   #Main program loop
   NA = NAnalyze(sys.argv)
