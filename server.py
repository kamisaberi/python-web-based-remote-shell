# first of all import the socket library
import socket
import os
import time
import urllib
import subprocess
import sys, os, io
from subprocess import call
import subprocess
import webshell
import utility
from constant import *
import traitant
import env

# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', sys.argv[1], sys.argv[2])

try:
    if os.path.exists(sys.argv[1].strip()):
        env.web_shell = sys.argv[1]
    if sys.argv[2].isnumeric():
        env.port = int(sys.argv[2])

except:
    print("ERROR, please launch server again using valid data")
    exit(0)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created")
sock.bind((env.server_addr, env.port))
print("socket binded to %s" % (env.port))
sock.listen(5)
print("socket is listening")

activeChildren = []


def now():  # current time on server
    return time.ctime(time.time())


def reapChildren():  # reap any dead child processes
    while activeChildren:  # else may fill up system table
        pid, stat = os.waitpid(0, os.WNOHANG)  # don't hang if no child exited
        if not pid: break
        activeChildren.remove(pid)


def handleClient(connection):  # child process: reply, exit
    time.sleep(5)  # simulate a blocking activity
    while 1:  # read, write a client socket
        data = connection.recv(1024)  # till eof when socket closed
        if not data: break
        connection.send('Echo=>%s at %s' % (data, now()))
    connection.close()
    os._exit(0)


while True:
    c, addr = sock.accept()
    print('Got connection from', addr)
    data = ""

    # TODO START fork version
    reapChildren()  # clean up exited children now
    childPid = os.fork()  # copy this process
    if childPid == 0:  # if in child process: handle
        handleClient(c)
    else:  # else: go accept next connect
        activeChildren.append(childPid)  # add to active child pid list
    # TODO fork version END

    recvstr = c.recvfrom(4096)[0].decode("utf-8")
    c.send(bytes(webshell.render(recvstr), 'utf-8'))

    c.close()
