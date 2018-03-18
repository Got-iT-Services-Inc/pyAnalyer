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

import sys, os, inspect, importlib

sCurPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

#For Module Libraries
sys.path.insert(0,sCurPath + '/pyConfig')
sys.path.insert(0,sCurPath + '/pyDebugger')
sys.path.insert(0,sCurPath + '/pyXML')

from Config import pyConfig
from Debug import pyDebugger
from XML import pyXMLTag
from termcolor import colored

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

      #Variables
      self.NXML = None
      self.XML_NMAPRUN = "nmaprun"

      #BEGIN!
      self.ProcessArgs(Args)
      if self.Config.Get("Debug_All") == False:
         os.system('clear')
      while self.Interpreter() == True:
           self.Debugger.Log("End of Interpretting Process",DebugLevel=self.DBLV3)

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
      self.Debugger.Log("Opening file...", DebugLevel=self.DBLV2)
      with open(opts['-i'], 'r') as fxd:
         self.Debugger.Log("Reading file...", DebugLevel=self.DBLV2)
         sData = fxd.read()
         sData = sData.replace("&#45;","-")
      self.Debugger.Log("Parsing initial XML data...", DebugLevel=self.DBLV2)
      self.NXML = pyXMLTag(sData,self.XML_NMAPRUN,self.Config.Get("Debug_All"),False)

   def Interpreter(self):
      sOpt = []
      print(colored('N','red') + colored('Analyzer','green') + ": ", end='')
      sInput = input("")
      if sInput.find(" ") > -1:
         sOpt = sInput.split(" ")
      else:
         sOpt.append(sInput)

      self.Debugger.Log("First Command: '" + str(sOpt[0]) + "'", DebugLevel=self.DBLV3)
      if sOpt[0] == "exit":
         sys.exit()
      elif sOpt[0] == "cmd":
         print("Nmap command is:")
         print("  " + self.NXML.Get_Key("args") + "\n")
         return True
      elif sOpt[0] == "dump":
         if sOpt[1] == "keys":
            print("XML Dump:")
            print(str(self.NXML.Get_Keys()))
            return True
         elif sOpt[1] == "data":
            print("Data Dump:")
            print(self.NXML.Get_Data())
            return True
         elif sOpt[1] == "children":
            print("Children Dump")
            print(str(self.NXML.Children))
            return True
      elif sOpt[0] == "reload":
         os.execv(sys.executable, ['python'] + sys.argv)
         return False
      elif sOpt[0] == "show":
         NXML = self.NXML
         if sOpt[1] == "keys":
            print("Showing keys for " + colored(NXML._sKey,'cyan') + ":")
            for key,val in NXML.Get_Keys().items():
               print("   " + colored(key,'green') + " = " + colored(val,'yellow'))
            return True
         elif sOpt[1] == "key":
            if len(sOpt) > 2:
               try:
                  print(colored(NXML._sKey,'cyan') + ".Key['" + colored(sOpt[2],'yellow') + "'] = '" + colored(NXML.Get_Keys()[sOpt[2]],'green') + "'")
               except Exception as e:
                  print(colored("**Error:",'red') + " Key " + str(e) + " does not exist")
            else:
               print(colored("**Error:",'red') + " No key name specified")
            return True
         elif sOpt[1] == "children":
            print("Showing children for " + colored(NXML._sKey,'cyan') + ":")
            for child in NXML.Children:
               print("   " + colored(child,'green'))
            return True
      elif sOpt[0] == "set":
         NXML = self.NXML
         if len(sOpt) > 3:
            if sOpt[1] == "focus":
               #FIX THIS SHIT
               print("FOCUS DAMNIT")
            elif sOpt[1] == "key":
               print("Settings key'" + colored(sOpt[2],'yellow') + " to '" + colored(sOpt[3],'green') + "'")
               NXML.Set_Key(sOpt[2],sOpt[3])
         else:
            print(colored("**Error:",'red') + " additional arguments required, ex: 'set [focus|key] [keyname] [value]'")
         return True 
      elif sOpt[0] == "help":

         if len(sOpt) < 2:
            print("Commands:")
            print("  children:  Show the names of child tags within the current tag in focus")
            print("  cmd:       Show the command run to generate the current nmap xml file")
            print("  dump:      dumps a variable unformatted to the terminal")
            print("  exit:      exit NAnalyzer")
            print("  reload:    reload NAnalyzer")
            print("  set:       sets a variable, function, view, etc.. (more info with 'help set'")
            print("  show:      show a piece of information (more info with 'help show'")
         else:
            if sOpt[1] == "set":
               print("Command: 'set'")
               print("  focus:  set the root element for data inspection")
               print("  key:    set/change the value for a key of the current element in focus")
            elif sOpt[1] == "show":
               print("Command: 'show'")
               print("  key:       show the data within a specific key of the current root element")
               print("  keys:      list all the keys and their values for the current root element")
               print("  children:  show the names of the children for the current root element ")
         return True



if __name__ == '__main__':

   #Main program loop
   while True:
       NA = NAnalyze(sys.argv)
       NA = None
