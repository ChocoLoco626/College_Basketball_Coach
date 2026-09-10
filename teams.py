
from models import *
import random

TEAM_DATA=[
("Duke","ACC","150",96),("North Carolina","ACC","153",95),("Kansas","Big 12","2305",95),
("Kentucky","SEC","96",94),("UConn","Big East","41",91),("Gonzaga","WCC","2250",89),
("Houston","Big 12","248",88),("Arizona","Big 12","12",88),("Michigan State","Big Ten","127",87),
("Villanova","Big East","222",87),("UCLA","Big Ten","26",90),("Indiana","Big Ten","84",88),
("Arkansas","SEC","8",82),("Tennessee","SEC","2633",84),("Alabama","SEC","333",80),
("Iowa State","Big 12","66",82),("Baylor","Big 12","239",84),("Creighton","Big East","156",84),
("Marquette","Big East","269",82),("Texas Tech","Big 12","2641",80),("Auburn","SEC","2",82),
("Florida","SEC","57",81),("Illinois","Big Ten","356",84),("Purdue","Big Ten","2509",86),
("Wisconsin","Big Ten","275",84),("Oregon","Big Ten","2483",80),("San Diego State","Mountain West","21",76),
("Memphis","AAC","235",76),("VCU","A10","2670",72),("Dayton","A10","2168",74),
("Boise State","Mountain West","68",70),("Nevada","Mountain West","2440",69),
("Liberty","CUSA","2335",69),("Saint Mary's","WCC","2608",73),("New Mexico","Mountain West","167",68),
("Grand Canyon","WAC","2253",65),("Drake","MVC","2181",65),("Princeton","Ivy","163",66),
("Yale","Ivy","43",65),("Vermont","America East","261",62),("UC Irvine","Big West","300",63),
("Furman","SoCon","231",61),("Lipscomb","ASUN","288",58),("Wofford","SoCon","2747",58),
("North Dakota State","Summit","2449",55),("South Dakota State","Summit","2569",56),
("Northern Iowa","MVC","2460",57),("Montana State","Big Sky","147",54),("UC San Diego","Big West","302",57)
]

def make_player(team,i):
    base=max(48,min(84,int(team.current-19+random.randint(0,25))))
    return Player(f"{team.name} Player {i+1}",["PG","SG","SF","PF","C"][i%5],base,
        min(99,base+random.randint(3,18)),base+random.randint(-4,4),base+random.randint(-4,4),
        base+random.randint(-5,5),base+random.randint(-5,5),base+random.randint(-4,5),
        base+random.randint(-5,5),base+random.randint(-3,5),base+random.randint(-3,5),
        random.choice([72,74,76,78,80,82]),random.choice(["FR","SO","JR","SR"]),random.randint(65,90),
        stars=max(1,min(5,round((base-45)/8))),nil_value=random.randint(25000,300000),
        transfer_risk=random.randint(5,30))

def make_teams():
    out=[]; seen=set()
    for n,c,e,p in TEAM_DATA:
        if n in seen: continue
        seen.add(n)
        t=Team(name=n,conference=c,espn_id=e,historical=p,current=clamp(p+random.gauss(0,3)),
                facilities_level=max(3,min(10,int(p/12))),budget=5_000_000+int(p*100_000),
                nil_budget=500_000+int(p*80_000),academics=clamp(65+p*.15),security=clamp(58+p*.32))
        t.coach=Coach("Head Coach",prestige=clamp(p*.55))
        t.roster=[make_player(t,i) for i in range(13)]
        t.staff=[Staff("Assistant Coach","Assistant",random.randint(45,75),150000,"General",3,3)]
        out.append(t)
    return out

def generate_recruits(teams, count=80):
    names=["Jayden Williams","Marcus Carter","Derrick Johnson","Ethan Brooks","Caleb Miller","Isaiah Thomas",
           "Jordan Davis","Malachi Brown","Tyrese Jackson","Cooper Wilson","Noah Anderson","Camden Lewis"]
    pos=["PG","SG","SF","PF","C"]; out=[]
    for i in range(count):
        stars=random.choices([2,3,4,5],[20,45,28,7])[0]
        overall=48+stars*7+random.randint(-4,5)
        out.append(Recruit(f"{random.choice(names)} {i+1}",random.choice(pos),stars,overall,
                           min(99,overall+random.randint(5,18)),random.randint(55,95),
                           random.randint(50000,700000),{}))
    return out
