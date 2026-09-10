
import random
from models import *

def recruit_interest(team,recruit,coach):
    base=team.recruiting_prestige
    fit=coach.recruiting*.25+coach.nil*.08+team.academics*.08+team.facilities_level*1.2
    star_bonus=recruit.stars*3
    return clamp(base*.48+fit+star_bonus-recruit.nil_demand/15000)

def update_interest(team,recruits):
    for r in recruits:
        r.interest[team.name]=round(recruit_interest(team,r,team.coach),1)
    return sorted(recruits,key=lambda x:x.interest.get(team.name,0),reverse=True)

def offer_recruit(team,recruit):
    if team.nil_budget<recruit.nil_demand: return False
    interest=recruit.interest.get(team.name,0)
    if interest<55: return False
    recruit.committed_to=team.name
    team.nil_budget-=recruit.nil_demand
    p=Player(recruit.name,recruit.position,recruit.overall,recruit.potential,
             recruit.overall,recruit.overall,recruit.overall,recruit.overall,
             recruit.overall,recruit.overall,recruit.overall,recruit.overall,
             random.choice([72,74,76,78,80]),"FR",80,nil_value=recruit.nil_demand,stars=recruit.stars)
    team.roster.append(p)
    return True

def process_transfer_portal(teams):
    pool=[]
    for t in teams:
        keep=[]
        for p in t.roster:
            if p.transfer_risk>70 and random.random()<.30:
                pool.append(p)
            else: keep.append(p)
        t.roster=keep
    random.shuffle(pool)
    return pool

def transfer_offer(team,player):
    if team.nil_budget<player.nil_value: return False
    if team.recruiting_prestige+random.uniform(-10,10)<55: return False
    team.nil_budget-=player.nil_value
    player.commitment=team.name
    player.transfer_risk=10
    team.roster.append(player)
    return True
