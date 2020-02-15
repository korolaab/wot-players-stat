import requests
import json
import clickhouse_driver
import time

Korben_medal="medalBobKorbenDallas"
Lebwa_medal="medalBobLebwa"
Yusha_medal="medalBobYusha"
Amway_medal="medalBobAmway921"
medals=[Korben_medal,Lebwa_medal,Yusha_medal,Amway_medal]

with open(folder+"app_id","r") as f:
    app_id = f.read()
with open(folder+"clickhouse_host.json") as f:
    db = json.load(f.read())  


def get_account_id(nicknames):
        json_data =requests.get("https://api.worldoftanks.ru/wot/account/list/?application_id={}&type=exact&search={}".format(app_id,','.join(nicknames))).text
        raw_data= json.loads(json_data)
        if(raw_data["status"]=="ok"):
            return raw_data["data"]
        else:
            return []
def get_bb_medal(ids):
    json_data=requests.get("https://api.worldoftanks.ru/wot/account/achievements/?application_id={}&fields=achievements%2C&account_id={}".format(app_id,','.join(str(e) for e in [*ids]))).text
    raw_data=json.loads(json_data)
    if(raw_data["status"] == "ok"):
        for i in [*ids]:
            for medal in medals:                
                if(medal in raw_data["data"][str(i)]["achievements"]):
                    ids[i]["medal"]=medal                    
                    break
    return ids
                
def get_stat(ids):
    json_data=requests.get("https://api.worldoftanks.ru/wot/account/info/?application_id={}&account_id={}&fields=statistics.all".format(app_id,','.join(str(e) for e in [*ids]))).text
    raw_data=json.loads(json_data)
    if(raw_data["status"]=="ok"):
        for i in [*ids]:
            ids[i]["wins"]=raw_data["data"][str(i)]["statistics"]["all"]["wins"]
            ids[i]["losses"]=raw_data["data"][str(i)]["statistics"]["all"]["losses"]
            ids[i]["draws"]=raw_data["data"][str(i)]["statistics"]["all"]["draws"]
            ids[i]["battle_avg_xp"]=raw_data["data"][str(i)]["statistics"]["all"]["battle_avg_xp"]
            ids[i]["damage_dealt"]=raw_data["data"][str(i)]["statistics"]["all"]["damage_dealt"]
    return ids

