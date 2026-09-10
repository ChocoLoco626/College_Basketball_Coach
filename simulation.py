
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
    others=[t for t in teams if t.name!=team.name]; random.shuffle(others)
    conf=[t for t in others if t.conference==team.conference][:10]
    non=[t for t in others if t not in conf][:12]
    games=[]
    for t in conf:
        games += [Game(t.name,"Home",f"{year}-01-{random.randint(1,28):02d}",True,importance=1.3),
                  Game(t.name,"Away",f"{year}-02-{random.randint(1,28):02d}",True,importance=1.3)]
    for t in non:
        games.append(Game(t.name,random.choice(["Home","Away","Neutral"]),
                          f"{year}-{random.choice([11,12]):02d}-{random.randint(1,28):02d}"))
    team.schedule=games[:32]; return team.schedule

def advance_week(team):
    for p in team.roster:
        p.fatigue=max(0,p.fatigue-12)
        if p.injured:
            p.injury_weeks=max(0,p.injury_weeks-1)
            if p.injury_weeks<=0: p.injured=False
        p.morale=clamp(p.morale+random.uniform(-2,2))
    return team


def national_rankings(teams):
    rows=[]
    for t in teams:
        played=t.wins+t.losses
        win_pct=t.wins/max(1,played)
        strength=t.adjusted_prestige*0.35+t.ratings()["overall"]*0.45+win_pct*100*0.20
        rows.append({"Team":t.name,"Conference":t.conference,"Record":f"{t.wins}-{t.losses}",
                     "Win%":round(win_pct,3),"NET-like":round(strength,1),
                     "SOS":round(t.adjusted_prestige*.55+t.ratings()["overall"]*.45,1)})
    return sorted(rows,key=lambda x:(x["NET-like"],x["Win%"]),reverse=True)

def conference_standings(teams, conference):
    members=[t for t in teams if t.conference==conference]
    rows=[]
    for t in members:
        rows.append({"Team":t.name,"W":t.conference_wins,"L":t.conference_losses,
                     "Pct":round(t.conference_wins/max(1,t.conference_wins+t.conference_losses),3),
                     "Overall":f"{t.wins}-{t.losses}","Prestige":round(t.adjusted_prestige,1)})
    return sorted(rows,key=lambda x:(x["W"],x["Pct"]),reverse=True)

def national_results(teams):
    return sorted([{"Team":t.name,"Conference":t.conference,"Record":f"{t.wins}-{t.losses}",
                    "NET-like":round(t.adjusted_prestige*.45+t.ratings()["overall"]*.55,1),
                    "Postseason":t.tournament_result or "—"} for t in teams],
                  key=lambda x:x["NET-like"],reverse=True)
