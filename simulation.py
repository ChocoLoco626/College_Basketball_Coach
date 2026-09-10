
import random
from models import *

def team_strength(t):
    r=t.ratings(); c=t.coach
    return r["overall"]*.60+c.prestige*.08+c.offense*.07+c.defense*.07+c.motivation*.05+c.adaptability*.05+r["depth"]*.08

def simulate_game(home,away,tempo=68,aggression=60,defense="Balanced"):
    hs=team_strength(home); aw=team_strength(away)
    tactical=(home.coach.offense*(aggression-50)/300 + home.coach.defense*(60-aggression)/400)
    diff=(hs-aw)*.72+2.5+tactical
    pace=max(58,min(78,tempo))
    total=pace+random.gauss(0,7)
    home_score=max(42,int(random.gauss(total/2+diff/2,8)))
    away_score=max(42,int(random.gauss(total/2-diff/2,8)))
    if home_score==away_score: home_score+=1
    return home_score,away_score

def play_game(user,opp,site="Home",tempo=68,aggression=60,defense="Balanced"):
    if site=="Away": pf,pa=simulate_game(opp,user,tempo,aggression,defense); pf,pa=pa,pf
    else: pf,pa=simulate_game(user,opp,tempo,aggression,defense)
    win=pf>pa; user.wins+=int(win); user.losses+=int(not win)
    user.coach.wins+=int(win); user.coach.losses+=int(not win)
    return pf,pa,win

def generate_schedule(team,teams,year):
    others=[t for t in teams if t.name!=team.name]
    random.shuffle(others)
    conf=[t for t in others if t.conference==team.conference]
    games=[]; used=[]
    # Double round robin against available conference opponents, capped to 18.
    for t in conf:
        if len(games)>=18: break
        games += [Game(t.name,"Home",f"{year}-01-{random.randint(1,28):02d}",True,importance=1.3),
                  Game(t.name,"Away",f"{year}-02-{random.randint(1,28):02d}",True,importance=1.3)]
    # Fill to a 30-game regular season with non-conference opponents.
    non=[t for t in others if t.conference!=team.conference]
    random.shuffle(non)
    i=0
    while len(games)<30 and (non or others):
        pool=non if non else others
        t=pool[i%len(pool)]; i+=1
        site=random.choice(["Home","Away","Neutral"])
        games.append(Game(t.name,site,f"{year}-{random.choice([11,12]):02d}-{random.randint(1,28):02d}",False,importance=1.0))
        if i>len(pool)*3 and not non: break
    team.schedule=games[:30]
    return team.schedule

def advance_week(team):
    for p in team.roster:
        p.fatigue=max(0,p.fatigue-12)
        if p.injured:
            p.injury_weeks=max(0,p.injury_weeks-1)
            if p.injury_weeks<=0: p.injured=False
        p.morale=clamp(p.morale+random.uniform(-2,2))
    return team
