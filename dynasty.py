import random
from models import *
from simulation import simulate_game, team_strength
from career import generate_job_market, end_season, fired

AWARDS=["National Player of the Year","Conference Player of the Year","Freshman of the Year","Sixth Man of the Year"]

def reset_season(team):
    team.wins=team.losses=team.conference_wins=team.conference_losses=0
    team.tournament_result=""
    team.schedule=[]
    for p in team.roster:
        p.fouls=0; p.minutes=0; p.fatigue=0; p.morale=clamp(p.morale+random.uniform(-4,4))
        p.year={"FR":"SO","SO":"JR","JR":"SR","SR":"GR"}.get(p.year,"GR")
    return team

def offseason_roster(team):
    # Graduates and exhausted eligibility leave; seniors can return as GR at a lower rate.
    remaining=[]; departed=[]
    for p in team.roster:
        if p.year=="GR" or (p.year=="SR" and random.random()<.75): departed.append(p); continue
        remaining.append(p)
    team.roster=remaining
    # Development during offseason
    for p in team.roster:
        growth=random.uniform(.4,2.2) + max(0,team.coach.development-55)/80
        p.overall=min(p.potential,p.overall+growth)
        p.morale=clamp(p.morale+random.uniform(2,8))
        p.transfer_risk=max(0,p.transfer_risk-random.uniform(3,12))
    return departed

def preseason(team):
    team.schedule=[]
    team.wins=team.losses=team.conference_wins=team.conference_losses=0
    team.security=clamp(team.security+2)
    # modest annual current-prestige regression toward adjusted roster strength
    team.current=clamp(team.current + (team.ratings()["overall"]-team.current)*.12)

def simulate_other_games(teams,user_name=None):
    # Lightweight world simulation: updates enough results to make standings/job market dynamic.
    for t in teams:
        if t.name==user_name: continue
        strength=team_strength(t)
        wins=max(0,min(30,int(random.gauss(12+(strength-60)*.35,4))))
        t.wins=wins; t.losses=32-wins
        t.conference_wins=max(0,min(16,int(wins*0.42+random.gauss(0,2))))
        t.conference_losses=max(0,16-t.conference_wins)
        t.current=clamp(t.current+(wins-16)*.18)

def conference_tournament(team,teams):
    conf=[t for t in teams if t.conference==team.conference]
    conf.sort(key=lambda x:(x.wins,x.adjusted_prestige),reverse=True)
    seed=next((i+1 for i,t in enumerate(conf) if t.name==team.name),len(conf))
    team.conference_tournament_seed=seed
    # user plays up to three rounds against generated opponents.
    rounds=max(1,min(3,len(conf)//4))
    wins=0
    for r in range(rounds):
        opps=[t for t in conf if t.name!=team.name]
        opp=random.choice(opps)
        pf,pa=simulate_game(team,opp,tempo=68,aggression=60,defense="Balanced")
        if pf>pa: wins+=1
        else: break
    team.tournament_result="Conference Champion" if wins==rounds else ("Conference Final" if wins==rounds-1 and rounds>1 else "Conference Tournament")
    return wins

def ncaa_selection(teams):
    ranked=sorted(teams,key=lambda t:(t.wins*1.7+t.conference_wins*1.2+t.adjusted_prestige*.55+t.current*.4),reverse=True)
    selected=ranked[:68]
    for i,t in enumerate(selected):
        t.ncaa_seed=max(1,min(16,1+i//4))
    return selected

def ncaa_tournament(team,teams):
    field=ncaa_selection(teams)
    if team not in field:
        team.tournament_result="NCAA Bubble Miss"
        return team.tournament_result
    seed=team.ncaa_seed
    wins=0
    # Seed-adjusted expected wins, with randomness and current strength.
    expected=max(0,min(6,4.8-(seed-1)*.23+(team.ratings()["overall"]-70)*.07))
    wins=max(0,min(6,int(random.gauss(expected,.9))))
    labels={0:"Round of 68/First Four",1:"Round of 64",2:"Round of 32",3:"Sweet 16",4:"Elite Eight",5:"Final Four",6:"Champion"}
    team.tournament_result=labels[wins]
    return team.tournament_result

def season_awards(team,teams):
    allp=[p for t in teams for p in t.roster]
    if not allp:return []
    best=max(allp,key=lambda p:p.overall+p.potential*.15+p.morale*.05)
    awards=[]
    if best in team.roster: awards.append({"award":"National Player of the Year","player":best.name})
    top=max(team.roster,key=lambda p:p.overall,default=None)
    if top: awards.append({"award":"Team MVP","player":top.name})
    return awards

def finish_season(g):
    user=next((t for t in g["teams"] if t.name==g.get("user")),None)
    if not user:return
    simulate_other_games(g["teams"],user.name)
    conference_tournament(user,g["teams"])
    ncaa_tournament(user,g["teams"])
    awards=season_awards(user,g["teams"])
    history={"season":f"{g['year']}-{str(g['year']+1)[-2:]}","record":f"{user.wins}-{user.losses}",
             "conference":f"{user.conference_wins}-{user.conference_losses}",
             "result":user.tournament_result,"prestige":round(user.adjusted_prestige,1),"awards":", ".join(a["award"] for a in awards)}
    user.history.append(history)
    if user.tournament_result=="Champion": user.coach.titles+=1
    end_season(user,g["career_profile"])
    cp=g["career_profile"]
    user.coach.prestige=cp.prestige; user.coach.name=cp.name
    # Program trajectory
    delta=(user.wins-user.losses)*.12 + (5 if "Final Four" in user.tournament_result or user.tournament_result=="Champion" else 0)
    user.current=clamp(user.current+delta)
    user.security=clamp(user.security + (user.wins-16)*1.1 + (7 if user.tournament_result=="Champion" else 0))
    g["season_awards"]=awards; g["last_season"]=history
    g["contract_expired"]=bool(g.get("contract") and g["contract"].remaining_years<=0)
    g["season_stage"]="offseason"

def advance_offseason(g):
    user=next((t for t in g["teams"] if t.name==g.get("user")),None)
    if not user:return
    departed=offseason_roster(user)
    # Portal pool is produced by the whole world after rosters change.
    pool=[]
    for t in g["teams"]:
        if t is user: continue
        for p in list(t.roster):
            if p.transfer_risk>35 and random.random()<.10:
                t.roster.remove(p); pool.append(p)
    g["transfer_pool"]=pool
    # Budget/operations reset and contract burns a year.
    user.budget=int(user.budget + max(0,user.adjusted_prestige*35000))
    user.nil_budget=int(user.nil_budget + max(0,user.boosters*5000))
    if g.get("contract"):
        g["contract"].remaining_years=max(0,g["contract"].remaining_years-1)
    g["departed_players"]=departed
    g["year"]+=1
    g["season_stage"]="preseason"
    g["recruit_pool"]=[]
    g["job_market"]=generate_job_market(g["teams"],g["career_profile"])
    for t in g["teams"]: preseason(t)
    from teams import generate_recruits
    g["recruit_pool"]=generate_recruits(g["teams"],100)
    if fired(user):
        g["fired"]=True; g["user"]=None
        g["career_profile"].prestige=clamp(g["career_profile"].prestige-2)
    return departed
