import socket
import csv
import requests
import config as cfg
import time
import os
from datetime import datetime

monitors = []

os.chdir(os.path.realpath(os.path.dirname(__file__)))

SMTPhelo = "220"
SMTPok = "250"
SMTPdata = "354"
SMTPquit = "221"

class monitor():
    def __init__(self, ip, id, plug, name):
        self.ip = ip
        self.id = id
        self.plug = plug
        self.name = name

# parsing config file and building monitor list
with open('monitors.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        print("adding " + row["ip"]+","+ row["id"]+","+row["plug"]+","+row["name"])
        monitors.append(monitor(row["ip"], row["id"], row["plug"], row["name"]))
        line_count += 1
    print(f'Processed {line_count} lines.')

while True:
    try:
        #make socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((cfg.cfg["SMTPip"], int(cfg.cfg["SMTPport"])))
        s.listen(1)
        while 1:
            conn, addr = s.accept()
            print("Connection from "+str(addr))
            for x in monitors:
                #look if the connected device is configured, if yes then proceed
                if addr[0] == x.ip:
                    now = datetime.now()
                    print("Reporting event at: "+now.strftime("%d/%m/%Y %H:%M:%S"))
                    ShinobiUrl = "http://" + cfg.cfg["ShinobiHost"] + ":" + cfg.cfg["ShinobiPort"] + "/" + cfg.cfg["APIkey"] + "/motion/" + cfg.cfg["GroupKey"] + "/" + x.id
                    # print(ShinobiUrl)
                    JsonData = "data={\'plug\':\'"+x.plug+"\',\'name\':\'"+x.name+"\',\'reason\':\'motion\',\'confidence\':200}"
                    # print(JsonData)
                    r = requests.get(ShinobiUrl, JsonData)
                    if str(r.json()) == str("{\'ok\': True}"):
                        print("event reported")
                    else:
                        print("event reporting error ")
                        print(r.json())

            conn.send(SMTPhelo.encode())
            conn.close()
    except:
        print("socket error")
        time.sleep(5)
conn.close()
