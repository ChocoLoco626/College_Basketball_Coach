
from models import *
from teams import make_teams

def normalize_player(p):
    if not isinstance(p,Player): return None
    defaults={"potential":p.overall,"morale":75,"fatigue":0,"fouls":0,"minutes":0,"role":"Rotation",
              "nil_value":0,"scholarship":True,"stars":3,"hometown":"USA","commitment":None,
              "transfer_risk":10,"injured":False,"injury_weeks":0}
    for k,v in defaults.items():
        if not hasattr(p,k): setattr(p,k,v)
    return p

def migrate_game_state(g):
    if not isinstance(g,dict): return None
    g.setdefault("schema_version",1); g.setdefault("year",2026); g.setdefault("season_stage","preseason")
    g.setdefault("career_mode",False); g.setdefault("career_started",False); g.setdefault("coach_name","Coach")
    g.setdefault("career_profile",None); g.setdefault("contract",None); g.setdefault("career_history",[])
    g.setdefault("job_market",[]); g.setdefault("recruit_pool",[]); g.setdefault("transfer_pool",[])
    g.setdefault("last_season",None); g.setdefault("season_awards",[]); g.setdefault("season_started",False)
    g.setdefault("fired",False); g.setdefault("departed_players",[]); g.setdefault("contract_expired",False)
    for t in g.get("teams",[]):
        t.roster=[normalize_player(p) for p in getattr(t,"roster",[]) if normalize_player(p)]
        while len(t.roster)<13:
            from teams import make_player
            t.roster.append(make_player(t,len(t.roster)))
        if not hasattr(t,"recruits"): t.recruits=[]
        if not hasattr(t,"transfers"): t.transfers=[]
        if not hasattr(t,"fan_support"): t.fan_support=65
        if not hasattr(t,"boosters"): t.boosters=60
        if not hasattr(t,"security"): t.security=60
        if not hasattr(t,"budget"): t.budget=5_000_000
        if not hasattr(t,"nil_budget"): t.nil_budget=1_000_000
    g["schema_version"]=SAVE_SCHEMA_VERSION
    return g

def new_game():
    from teams import make_teams,generate_recruits
    teams=make_teams()
    return {"schema_version":SAVE_SCHEMA_VERSION,"year":2026,"season_stage":"preseason",
            "teams":teams,"career_mode":False,"career_started":False,"coach_name":"Coach",
            "career_profile":None,"contract":None,"career_history":[],"job_market":[],
            "recruit_pool":generate_recruits(teams),"transfer_pool":[]}
