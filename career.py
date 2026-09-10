
import random
from models import *

def job_tier(p):
    if p>=90:return "Blue Blood"
    if p>=82:return "Elite High Major"
    if p>=72:return "High Major"
    if p>=62:return "Mid Major"
    if p>=52:return "Low Major"
    return "Entry Level"

def eligible_job(team_prestige,coach_prestige):
    return coach_prestige>=max(30,team_prestige-28)

def generate_job_market(teams,coach):
    out=[]
    for t in teams:
        if not eligible_job(t.adjusted_prestige,coach.prestige): continue
        if random.random()<.38 or t.security<40 or t.wins<8:
            fit=coach.prestige*.42+coach.recruiting*.12+coach.development*.10+coach.motivation*.08+(100-t.current)*.16+t.academics*.12
            out.append({"team":t.name,"tier":job_tier(t.adjusted_prestige),"fit":round(fit,1),
                        "salary":int(250000+t.adjusted_prestige*30000),"years":random.choice([3,4,5])})
    return sorted(out,key=lambda x:x["fit"],reverse=True)

def make_contract(team,offer):
    return Contract(team.name,offer["years"],offer["years"],offer["salary"],int(offer["salary"]*.35*max(0,offer["years"]-1)))

def end_season(team,profile):
    delta=(team.wins-16)*.65+(team.conference_wins-5)*.45+(8 if team.tournament_result in ["Champion","Final Four"] else 0)
    profile.prestige=clamp(profile.prestige+delta*.20)
    profile.career_wins+=team.wins; profile.career_losses+=team.losses
    if team.tournament_result=="Champion": profile.championships+=1
    return profile

def fired(team):
    expected=max(10,int(team.current*.23))
    return team.wins<expected and team.security<48
