import socket
import sys
import time
from random import randint

ipList = []
#load previous
logRead = open("ip-blacklist.log", 'r')
lines = logRead.readlines()
logRead.close()
for line in lines:
    line = line.rstrip('\n')
    print("loading ip: \"" + line + '"')
    ipList.append(line)


#C2
taunts = ["Go away, researcher!", "I see what you doin", "Hey, stop dissecting my malware. You'll ruin my RaaS  :'(", "You will never crack WannaSigh!"]
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(("127.0.0.1", 18610))
print("Socket binding operation completed")

serv.listen(5)
while(True):
#    try:
    conn, addr = serv.accept()
    print("Connected with " + addr[0] + ':' + str(addr[1]))

    recvIntro = conn.recv(1024).decode()
    print("recieved: \"" + recvIntro + '\"')

    conditMet = True
    if('_' in recvIntro):
        signat = recvIntro.split('_')[1]
        if('.' in signat):
            cnt = signat.count('.')
            if(cnt == 3):
                if(not(signat in ipList)):
                    ipList.append(signat)
                    cmd = "echo "+signat+" >> ip-blacklist.log"
                    os.system(cmd)
                else:
                    conditMet = False
            else:
                conditMet = False
        else:
            conditMet = False
    else:
        conditMet = False

    if(conditMet):
        epochInt = int(time.time())
        sendStr = "1618617746"
    else:
        sendStr = taunts[randint(0,3)]

    sendBts = str.encode(sendStr)
    conn.send(sendBts)
    print("sent: \"" + sendStr + '\"')

    conn.close()
