import os
import subprocess
command = 'ls -l | grep -e "hello word" || echo "empty directory'
print(os.execvp('sh', ['sh', '-c', command]))
# k =  subprocess.check_call(command)
# print(k)
