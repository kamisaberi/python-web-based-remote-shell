#!/usr/bin/python
print("Content-type: text/html\n\n")
print("<html>")
print("<head>")
print("<title>Python Query Params</title>")
print("</head>")
print("<body>")

import os


def init():
    # read the url
    params = os.environ.get('QUERY_STRING')
    print("params", params)

    print(
        "Click this url that has params in address: <a href='https://pythoninhtmlexamples.com/files/python-query-params/index.py?id=5&fname=kelly&lastname=schnerde'>https://pythoninhtmlexamples.com/files/python-query-params/index.py?id=5&fname=kelly&lastname=schnerde</a><br><br>")

    print(
        "Click this url that has <b>NO</b> params in address: <a href='https://pythoninhtmlexamples.com/files/python-query-params/index.py'>https://pythoninhtmlexamples.com/files/python-query-params/index.py</a><br><br>")

    print("<br><br><br>********************************************************<br><br><br>")

    # res = params.split('=')  # TESTS THAT THERE IS A QUERY STRING
    #
    # # display based on if params were sent
    # if str(res) == "['']":
    #     print('no query params')
    #     print('<br>')
    # else:
    #     print('some params were passed - show them')
    #     print('<br>')
    #     # searchParams is an array of type [['key','value'],['key','value']]
    #     searchParams = [i.split('=') for i in params.split('&')]  # parse query string
    #     for key, value in searchParams:
    #         print('<b>' + key + '</b>: ' + value + '<br>\n')


# start here:
init()

print("</body>")
print("</html>")
