import subprocess
import os
import utility

def run(command):
    if not command:
        raise Exception("Invalid Command")
    else:
        p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        out, err = p.communicate()
        return out


def run2(data):
    out = ""
    try:
        # print("RUN START")
        out = subprocess.check_output(data,stderr=subprocess.STDOUT, shell=True).decode("utf-8")
        # print("OUT:" , out)
        if isinstance(out , list) or  isinstance(out , tuple):
            return out[len(out)-1]
        else:
            return out
    except subprocess.CalledProcessError as e:
        # print("EXCEPT START")
        out = e.args[len(e.args)-1]

    return out

def run3(data):
    return os.execvp('sh', ['sh', '-c', data]).decode("utf-8")

def run4(data):
    proc = subprocess.Popen(data, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ""
    while (True):
        line = proc.stdout.readline()
        line = line.decode()
        if (line == ""): break
        output += line
    return output.decode("utf-8")
def run5(data):
    result = subprocess.run(data, stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8")

def parse_commands(command):
    # print("command in parse:" , command)
    cmms= command.strip().split("|")
    comms=[]
    for cmm in cmms :
        comms.extend(cmm.strip().split(";"))

    splited_commands = []
    for comm in comms:
        cmm_splts = comm.strip().split()
        splited_commands.append(cmm_splts)
        # cmm_args = []
        # cmm_name = cmm_splts[0]
        # if len(cmm_splts) > 1:
            # cmm_args= cmm_splts[1:]
    print("splited commands in parse :" , splited_commands)
    return splited_commands
        
def run_commands(commands):
    commands = utility.decode_form_encoded(commands)
    output= ""
    print("COMMANDS:", commands)
    for command in parse_commands(commands) :
        # print("COMMAND:" , command)
        out=  run2(command)
        # print("OUT INSIDE RUN:", out)
        if isinstance(out , list) or isinstance(out , tuple) :
            output+= "\r\n" + out[len(out)-1]
        else :
            output+= "\r\n" + out
    return output

def retrieve_form_data(rcvs):
    data1 = ""
    session_id1 = ""
    lines = rcvs.strip().split("\n")
    for line in lines:
        if line.strip().find("cmd") == 0:
            data1 = line.strip().split("=")[1].strip().split("&")[0].strip()
            break
    for line in lines:
        if line.strip().find("session") != -1:
            session_id1 = line.strip().split("=")[2].strip()
            break
    return data1, session_id1
