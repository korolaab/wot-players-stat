import requests
import json
import clickhouse_driver
import time

Korben_medal="medalBobKorbenDallas"
Lebwa_medal="medalBobLebwa"
Yusha_medal="medalBobYusha"
Amway_medal="medalBobAmway921"
medals=[Korben_medal,Lebwa_medal,Yusha_medal,Amway_medal]

with open("app_id.txt","r") as f:
    app_id = f.read()
with open("clickhouse_host.json") as f:
    host = json.loads(f.read())  


def get_account_id(nicknames):
        json_data =requests.get("https://api.worldoftanks.ru/wot/account/list/?application_id={}&type=exact&search={}".format(app_id,','.join(nicknames))).text
        raw_data= json.loads(json_data)
        if(raw_data["status"]=="ok"):
            return raw_data["data"]
        else:
            return []
def get_bb_medal(ids_list):
    json_data=requests.get("https://api.worldoftanks.ru/wot/account/achievements/?application_id={}&fields=achievements%2C&account_id={}".format(app_id,','.join(str(e)
    for e in ids_list))).text
    raw_data=json.loads(json_data)
    ids={}
    if(raw_data["status"] == "ok"):
        for i in ids_list:
            if(raw_data["data"][str(i)] != None):
                ids[str(i)]={"medal":"No_data"}
                for medal in medals:                
                    if(medal in raw_data["data"][str(i)]["achievements"]):
                        ids[str(i)]["medal"]=medal                    
                        break
    return ids
                
def get_stat(ids):
    json_data=requests.get("https://api.worldoftanks.ru/wot/account/info/?application_id={}&account_id={}&fields=statistics.all".format(app_id,','.join(str(e) for e in [*ids]))).text
    raw_data=json.loads(json_data)
    accounts = []
    if(raw_data["status"]=="ok"):
        for i in [*ids]:
            if("wins" in raw_data["data"][i]["statistics"]["all"]):
                accounts.append({'id':int(i),
                                "bb_team":ids[i]['medal'],
                                'wins':raw_data["data"][i]["statistics"]["all"]["wins"],
                                'losses':raw_data["data"][i]["statistics"]["all"]["losses"],
                                'draws':raw_data["data"][i]["statistics"]["all"]["draws"],
                                'avg_xp':raw_data["data"][i]["statistics"]["all"]["battle_avg_xp"],
                                'total_damage':raw_data["data"][i]["statistics"]["all"]["damage_dealt"]})
            else: #if i is press account or something get wrong
                accounts.append({'id':int(i),
                                'bb_team':"No_data",
                                'wins':0,
                                'losses':0,
                                'draws':0,
                                'avg_xp':0,
                                'total_damage':0})

    return accounts

def write_to_db(accounts):
        log = client.execute("INSERT INTO wot.player_stat VALUES",accounts,types_check=True)
        return log
client = clickhouse_driver.Client(host=host["ip"])

with open("last_account_id.txt","r") as f:
    last_account_id = int(f.read())# read last accoutn id
ids_list=list(range(last_account_id,last_account_id+100))
acc_bb_medals = get_bb_medal(ids_list)
accounts = get_stat(acc_bb_medals)
write_to_db(accounts)
with open("last_account_id.txt","w") as f:
    f.write(str(last_account_id+100))
