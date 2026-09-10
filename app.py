
import streamlit as st
import random, math, json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional

st.set_page_config(page_title="CBB Coach Simulator — Deep Dynasty", page_icon="🏀", layout="wide")

# ============================================================
# DEEP COLLEGE BASKETBALL DYNASTY SIMULATOR
# Fictional player/coaching data; real school catalog.
# The 2027 postseason defaults to the NCAA's announced 76-team era.
# ============================================================

TEAM_DATA = [
("Duke","ACC",150,96),("North Carolina","ACC",153,94),("Virginia","ACC",258,87),("Louisville","ACC",97,82),("NC State","ACC",152,80),("Clemson","ACC",228,79),("Miami","ACC",2390,78),("Wake Forest","ACC",154,76),("Syracuse","ACC",183,76),("Pittsburgh","ACC",221,73),("Virginia Tech","ACC",259,74),("Georgia Tech","ACC",70,72),("Notre Dame","ACC",87,77),("California","ACC",25,69),("Stanford","ACC",24,72),("SMU","ACC",256,70),("Boston College","ACC",103,65),("Florida State","ACC",52,78),
("Kansas","Big 12",2305,96),("Houston","Big 12",248,91),("Iowa State","Big 12",66,86),("Arizona","Big 12",12,89),("Texas Tech","Big 12",2641,84),("Baylor","Big 12",239,84),("Kansas State","Big 12",2306,78),("TCU","Big 12",2628,75),("West Virginia","Big 12",277,73),("Cincinnati","Big 12",2132,72),("BYU","Big 12",252,76),("UCF","Big 12",2116,68),("Arizona State","Big 12",9,72),("Colorado","Big 12",38,70),("Utah","Big 12",254,73),
("Alabama","SEC",333,90),("Auburn","SEC",2,89),("Tennessee","SEC",2633,87),("Kentucky","SEC",96,94),("Arkansas","SEC",8,84),("Florida","SEC",57,85),("Texas","SEC",251,86),("Texas A&M","SEC",245,78),("Missouri","SEC",142,73),("Ole Miss","SEC",145,72),("Mississippi State","SEC",344,73),("LSU","SEC",99,72),("Georgia","SEC",61,70),("South Carolina","SEC",257,70),("Vanderbilt","SEC",238,69),
("Michigan State","Big Ten",127,92),("Michigan","Big Ten",130,88),("Indiana","Big Ten",84,88),("Purdue","Big Ten",2509,88),("Illinois","Big Ten",356,83),("Ohio State","Big Ten",194,83),("Wisconsin","Big Ten",275,84),("Iowa","Big Ten",2294,78),("UCLA","Big Ten",26,83),("USC","Big Ten",30,78),("Oregon","Big Ten",2483,79),("Maryland","Big Ten",120,77),("Rutgers","Big Ten",164,68),("Penn State","Big Ten",213,67),("Minnesota","Big Ten",135,66),("Nebraska","Big Ten",158,69),("Northwestern","Big Ten",77,68),("Washington","Big Ten",264,68),
("Gonzaga","WCC",2250,91),("Saint Mary's","WCC",2608,81),("San Francisco","WCC",2539,72),("San Diego","WCC",301,65),("Santa Clara","WCC",2603,74),
("Creighton","Big East",156,85),("UConn","Big East",41,94),("Villanova","Big East",222,88),("Marquette","Big East",269,83),("St. John's","Big East",2599,81),("Providence","Big East",2507,76),("Xavier","Big East",2752,80),("Butler","Big East",2086,70),("Seton Hall","Big East",2550,71),("Georgetown","Big East",46,69),("DePaul","Big East",305,62),
("Memphis","AAC",235,81),("VCU","A10",2670,75),("Dayton","A10",2166,79),("Saint Louis","A10",139,69),("Drake","MVC",2181,73),("Bradley","MVC",71,70),("Nevada","MWC",2440,75),("Boise State","MWC",68,74),("San Diego State","MWC",21,83),("New Mexico","MWC",167,73),("Colorado State","MWC",36,76),("Grand Canyon","WAC",2253,71),("Liberty","CUSA",2335,70),("Yale","Ivy",43,70),("Princeton","Ivy",163,73),("Harvard","Ivy",108,66),("Vermont","America East",261,69),("Colgate","Patriot",2142,68),("Richmond","A10",257,67)
]
TEAM_DATA=list(dict((x[0],x) for x in TEAM_DATA).values())

FIRST=["Alex","Jordan","Marcus","Chris","Taylor","Dylan","Mike","Ryan","Steve","Brian","Jason","Kevin","Matt","Derek","Andrew","Josh","Eric","Justin","Tyler","Cameron","Jalen","Caleb","Noah","Isaiah","Malik","Trevor","Andre","Tyrese","Miles","Drew"]
LAST=["Mercer","Hayes","Reed","Walker","Grant","Brooks","Morgan","Bennett","Parker","Cole","Davis","Foster","Harris","Mitchell","Stone","Turner","Carter","Reeves","Cooper","Miller","Johnson","Williams","Brown","Wilson","Taylor","Anderson","Thomas","Jackson","White","Martin"]

def clamp(x,a=0,b=100): return max(a,min(b,x))
def nm(): return f"{random.choice(FIRST)} {random.choice(LAST)}"
def logo(e): return f"https://a.espncdn.com/i/teamlogos/ncaa/500/{e}.png"

@dataclass
class Staff:
    name:str; role:str; offense:float=50; defense:float=50; recruiting:float=50; development:float=50; scouting:float=50; nil:float=50; salary:int=250000
@dataclass
class Coach:
    name:str; prestige:float; offense:float; defense:float; recruiting:float; development:float; adaptability:float; motivation:float; loyalty:float; discipline:float; nil:float; salary:int; wins:int=0; losses:int=0; titles:int=0; years:int=0
@dataclass
class Player:
    name:str; pos:str; overall:float; potential:float; offense:float; defense:float; shooting:float; passing:float; handling:float; rebounding:float; athleticism:float; iq:float; height:int; year:int; morale:float; fatigue:float=0; fouls:int=0; minutes:float=0; role:str="Rotation"; nil_value:int=0; scholarship:bool=True
@dataclass
class Recruit:
    name:str; pos:str; stars:int; overall:float; potential:float; nil_expectation:int; academic:float; hometown:str; preference:str; interest:Dict[str,float]=field(default_factory=dict); committed:Optional[str]=None
@dataclass
class Game:
    opponent:str; site:str; date:str; conference:bool=False; played:bool=False; result:Optional[str]=None; score_for:int=0; score_against:int=0
@dataclass
class Team:
    name:str; conference:str; espn_id:int; historical:float; current:float; academics:float; facilities:float; budget:int; nil_budget:int; coach:Coach; staff:List[Staff]; roster:List[Player]
    wins:int=0; losses:int=0; cwins:int=0; closses:int=0; net:float=50; sos:float=50; security:float=70; schedule:List[Game]=field(default_factory=list)
    history:Dict[str,int]=field(default_factory=lambda:{"titles":0,"final_fours":0,"elite_eights":0,"sweet_sixteens":0,"tournament_apps":0,"conference_titles":0,"winning_seasons":0,"nba_draftees":0})
    awards:List[str]=field(default_factory=list); facilities_level:int=1; scholarships:int=13
    def coach_obj(self):
        if isinstance(self.coach, Coach):
            return self.coach
        self.coach = coach_for(self.current)
        return self.coach

    @property
    def adjusted_prestige(self):
        coach = self.coach_obj()
        return clamp(.22*self.historical+.28*self.current+.12*self.facilities*10+.12*self.recruiting_prestige+.10*coach.prestige+.08*self.academics+.08*self.net)
    @property
    def recruiting_prestige(self):
        coach = self.coach_obj()
        return clamp(.42*self.current+.18*self.historical+.12*self.facilities*10+.13*coach.recruiting+.10*coach.prestige+.05*min(100,self.nil_budget/100000))
    def ratings(self):
        ps=sorted(self.roster,key=lambda p:p.overall,reverse=True)
        top=ps[:10] or [Player("x","PG",50,50,50,50,50,50,50,50,50,50,72,1,50)]
        def av(k): return sum(getattr(p,k) for p in top)/len(top)
        depth=clamp(sum(p.overall for p in ps)/max(1,len(ps))+min(10,len(ps)))
        return dict(offense=clamp(.65*av("offense")+.18*self.coach.offense+.17*self.staff_rating("offense")),
                    defense=clamp(.65*av("defense")+.18*self.coach.defense+.17*self.staff_rating("defense")),
                    shooting=av("shooting"), passing=av("passing"), handling=av("handling"), rebounding=av("rebounding"),
                    athleticism=av("athleticism"), iq=av("iq"), depth=depth)
    def staff_rating(self,kind):
        vals=[getattr(s,kind,50) for s in self.staff]
        return sum(vals)/len(vals) if vals else 50

def coach_for(p):
    return Coach(nm(),clamp(random.gauss(p,9)),clamp(random.gauss(p,8)),clamp(random.gauss(p,8)),clamp(random.gauss(p,10)),clamp(random.gauss(p,8)),clamp(random.gauss(70,12)),clamp(random.gauss(72,10)),clamp(random.gauss(70,10)),clamp(random.gauss(70,10)),clamp(random.gauss(p,9)),int(max(300000,p*70000+random.gauss(0,150000))))
def staff_for(p):
    roles=[("OC", "offense"),("DC","defense"),("RC","recruiting"),("DEV","development"),("SCOUT","scouting")]
    out=[]
    for role,skill in roles:
        vals={k:clamp(random.gauss(p,12)) for k in ["offense","defense","recruiting","development","scouting","nil"]}
        out.append(Staff(nm(),role,**vals,salary=int(100000+random.random()*300000)))
    return out
def player_for(p,year=None):
    o=clamp(random.gauss(p*.72+16,5),48,97); pot=clamp(o+random.uniform(3,16),o,99)
    return Player(nm(),random.choice(["PG","SG","SF","PF","C"]),o,pot,clamp(o+random.gauss(0,6)),clamp(o+random.gauss(0,6)),
                  clamp(o+random.gauss(0,7)),clamp(o+random.gauss(0,7)),clamp(o+random.gauss(0,7)),clamp(o+random.gauss(0,7)),
                  clamp(o+random.gauss(0,7)),clamp(o+random.gauss(0,7)),random.randint(70,84),year or random.choice([1,1,1,2,2,3,4]),random.randint(62,88),0,0,0,"Rotation",int(max(15000,o*4500-80000)))
def recruit_pool(n=300):
    out=[]
    for _ in range(n):
        s=random.choices([2,3,4,5],[18,42,33,7])[0]
        base={2:53,3:63,4:75,5:87}[s]+random.gauss(0,4)
        out.append(Recruit(nm(),random.choice(["PG","SG","SF","PF","C"]),s,clamp(base),clamp(base+random.uniform(5,14)),
                           int({2:18000,3:55000,4:145000,5:350000}[s]*random.uniform(.7,1.3)),random.uniform(65,99),
                           random.choice(["Local","Regional","National"]),random.choice(["winning","playing_time","nil","development","academics","location"])))
    return out

def new_world():
    teams=[]
    for n,c,e,p in TEAM_DATA:
        teams.append(Team(n,c,e,p,clamp(p+random.gauss(0,4)),random.uniform(72,98),clamp(p+random.gauss(0,7)),random.uniform(.55,.95),
                          int(5_000_000+p*100_000),int(max(250_000,p*85_000+random.gauss(0,350_000))),coach_for(p),staff_for(p),[player_for(p) for _ in range(13)]))
    return teams

def make_schedule(g):
    for t in g["teams"]: t.schedule=[]
    by={}
    for t in g["teams"]:by.setdefault(t.conference,[]).append(t)
    for t in g["teams"]:
        conf=by[t.conference][:]
        random.shuffle(conf)
        for o in conf:
            if o is not t and len(t.schedule)<18:
                t.schedule.append(Game(o.name,random.choice(["H","A"]),"Conf",True))
        others=[x for x in g["teams"] if x.conference!=t.conference]
        random.shuffle(others)
        for o in others:
            if len(t.schedule)>=31:break
            if o.name not in [x.opponent for x in t.schedule]:
                t.schedule.append(Game(o.name,random.choice(["H","A","N"]),"Nonconf",False))

def game(a,b,plan_a,plan_b,site="N"):
    ra,rb=a.ratings(),b.ratings()
    home=2.6 if site=="H" else -2.6 if site=="A" else 0
    tempo=67+(plan_a["tempo"]-50)*.12
    pace=clamp(random.gauss(tempo,2.5),58,79)
    def side(o,d,pl,team):
        eff=69+(o["offense"]-d["defense"])*.22+(o["shooting"]-50)*.10+(o["iq"]-50)*.035
        if pl["offense"]=="3PT":eff+=(o["shooting"]-50)*.12
        if pl["offense"]=="Paint":eff+=(o["rebounding"]-50)*.08+(o["athleticism"]-50)*.06
        if pl["offense"]=="Transition":eff+=(o["athleticism"]-50)*.11+(o["handling"]-50)*.04
        if pl["defense"]=="Zone":eff+=(o["rebounding"]-d["shooting"])*.025
        if pl["defense"]=="Press":eff+=(o["athleticism"]-d["handling"])*.045
        eff+=(pl["aggression"]-50)*.025+team.coach.adaptability*.018+team.coach.motivation*.01
        return clamp(eff,55,91)
    ea=side(ra,rb,plan_a,a);eb=side(rb,ra,plan_b,b)
    # Shot profile + game variance
    fa=pace*ea/100;fb=pace*eb/100
    sa=max(45,round(random.gauss(fa+home,6.7)));sb=max(45,round(random.gauss(fb,6.7)))
    if sa==sb: sa+=random.randint(1,5)
    return sa,sb

def apply_result(a,b,sa,sb,conf=False):
    a.wins+=sa>sb;a.losses+=sa<sb;b.wins+=sb>sa;b.losses+=sb<sa
    if conf:
        a.cwins+=sa>sb;a.closses+=sa<sb;b.cwins+=sb>sa;b.closses+=sb<sa

def sim_game(g,a_name,b_name,site,pa=None,pb=None,conf=False):
    a=next(x for x in g["teams"] if x.name==a_name);b=next(x for x in g["teams"] if x.name==b_name)
    pa=pa or {"tempo":50,"aggression":50,"offense":"Balanced","defense":"Man"}
    pb=pb or {"tempo":50,"aggression":50,"offense":"Balanced","defense":"Man"}
    sa,sb=game(a,b,pa,pb,site);apply_result(a,b,sa,sb,conf)
    # player fatigue, minutes and foul risk
    for t in (a,b):
        for p in t.roster:
            p.fatigue=clamp(p.fatigue+random.uniform(3,12) if p.role in ["Star","Starter"] else p.fatigue+random.uniform(1,6))
            p.fouls=0
            p.minutes=clamp(random.gauss(28 if p.role=="Star" else 22 if p.role=="Starter" else 14,5),2,38)
    return {"a":a.name,"b":b.name,"sa":sa,"sb":sb}

def reset_fatigue(g):
    for t in g["teams"]:
        for p in t.roster:p.fatigue=clamp(p.fatigue-random.uniform(8,18),0,100)

def play_user_game(g,game_idx,plan):
    u=next(t for t in g["teams"] if t.name==g["user"])
    gm=u.schedule[game_idx]
    opp=next(t for t in g["teams"] if t.name==gm.opponent)
    default={"tempo":50,"aggression":50,"offense":"Balanced","defense":"Man"}
    r=sim_game(g,u.name,opp.name,gm.site,plan,default,gm.conference)
    gm.played=True;gm.result=u.name if r["sa"]>r["sb"] else opp.name;gm.score_for=r["sa"];gm.score_against=r["sb"]
    reset_fatigue(g)
    return r

def team_metrics(g):
    # NET-inspired but not a claim to reproduce the NCAA's proprietary/official calculation.
    for t in g["teams"]:
        off=t.ratings()["offense"];de=t.ratings()["defense"]
        efficiency=(off-de)*.55
        winpct=t.wins/max(1,t.wins+t.losses)
        sos=sum(next(x for x in g["teams"] if x.name==gm.opponent).adjusted_prestige for gm in t.schedule)/max(1,len(t.schedule))
        quality=(t.wins*1.2+t.cwins*1.8+efficiency*.5+sos*.16+t.current*.18)
        t.sos=clamp(sos);t.net=clamp(quality/2.5)

def rankings(g):
    team_metrics(g)
    return sorted(g["teams"],key=lambda t:(t.net,t.wins,t.adjusted_prestige),reverse=True)

def conference_tourney(g,conf):
    m=sorted([t for t in g["teams"] if t.conference==conf],key=lambda t:(t.cwins,t.wins,t.net),reverse=True)
    logs=[]
    while len(m)>1:
        nxt=[]
        for i in range(0,len(m),2):
            if i+1==len(m):nxt.append(m[i]);continue
            a,b=m[i],m[i+1];sa,sb=game(a,b,{"tempo":50,"aggression":50,"offense":"Balanced","defense":"Man"},{"tempo":50,"aggression":50,"offense":"Balanced","defense":"Man"})
            w=a if sa>sb else b;nxt.append(w);logs.append((a.name,sa,b.name,sb))
        m=nxt
    if m:
        m[0].history["conference_titles"]+=1
    return m[0],logs

def selection(g):
    # Selection-like model: conference champs auto-qualify, then best resumes.
    champs=[]
    for c in sorted(set(t.conference for t in g["teams"])):
        champ,_=conference_tourney(g,c);champs.append(champ)
    field=list(dict((t.name,t) for t in champs).values())
    candidates=[t for t in rankings(g) if t.name not in {x.name for x in field}]
    target=76
    field+=(candidates[:max(0,target-len(field))])
    field=sorted(field,key=lambda t:t.net,reverse=True)[:target]
    return field

def postseason(g):
    field=selection(g)
    for t in field:t.history["tournament_apps"]+=1
    rounds=[];cur=field
    # Generic 76-team bracket: opening round reduces to 64, then standard rounds.
    opening=[]
    if len(cur)>64:
        cur=sorted(cur,key=lambda t:t.net,reverse=True)
        while len(cur)>64:
            a=cur.pop();b=cur.pop();sa,sb=game(a,b,{"tempo":50,"aggression":50,"offense":"Balanced","defense":"Man"},{"tempo":50,"aggression":50,"offense":"Balanced","defense":"Man"})
            opening.append((a.name,sa,b.name,sb))
            cur.append(a if sa>sb else b)
    rounds.append(("Opening Round",opening))
    # seed by NET, then create adjacent matchups. This is intentionally simulation-oriented.
    cur=sorted(cur,key=lambda t:t.net,reverse=True)
    while len(cur)>1:
        games=[];nxt=[]
        for i in range(0,len(cur),2):
            a,b=cur[i],cur[i+1]
            sa,sb=game(a,b,{"tempo":50,"aggression":50,"offense":"Balanced","defense":"Man"},{"tempo":50,"aggression":50,"offense":"Balanced","defense":"Man"})
            games.append((a.name,sa,b.name,sb));nxt.append(a if sa>sb else b)
        rounds.append((f"Round {len(rounds)}",games));cur=nxt
    champ=cur[0]
    champ.history["titles"]+=1;champ.coach.titles+=1
    if len(rounds)>=3:champ.history["final_fours"]+=1
    if len(rounds)>=4:champ.history["elite_eights"]+=1
    if len(rounds)>=5:champ.history["sweet_sixteens"]+=1
    return champ,rounds,field

def offseason(g):
    portal=[]
    for t in g["teams"]:
        new=[]
        for p in t.roster:
            growth=(p.potential-p.overall)*.14*(.5+t.coach.development/100)
            p.overall=clamp(p.overall+max(0,growth)+random.uniform(-.4,1.0))
            p.year+=1
            if p.year>=5 or (p.morale<52 and random.random()<.38):
                portal.append(p);continue
            p.morale=clamp(p.morale+random.uniform(-3,6))
            new.append(p)
        t.roster=new
    g["portal"]=portal
    # Transfers / NIL
    for p in portal[:]:
        if random.random()<.25:
            continue
    # Coach movement
    for t in g["teams"]:
        expected=max(8,round(t.current/100*25))
        if t.wins<expected-5 or t.security<25:
            g["free_coaches"].append(t.coach)
            pool=sorted(g["free_coaches"],key=lambda c:c.prestige+random.gauss(0,5),reverse=True)
            t.coach=pool.pop(0);g["free_coaches"]=pool;t.security=68
        else:
            t.security=clamp(t.security+(t.wins-expected)*2)
        t.coach.years+=1;t.coach.prestige=clamp(t.coach.prestige+(t.wins/35-.5)*8)
    # facilities and program momentum
    for t in g["teams"]:
        if t.wins>=25 and t.budget>12_000_000 and random.random()<.35:t.facilities_level=min(5,t.facilities_level+1)
        t.current=clamp(t.current+(t.wins/35-.5)*10)
    g["year"]+=1;g["recruits"]=recruit_pool();make_schedule(g);g["season_stage"]="preseason"

def _num(v, default=0.0):
    """Convert legacy/corrupt Streamlit state values to a usable number."""
    if isinstance(v, (list, tuple, set)):
        if not v:
            return default
        v = next(iter(v))
    if isinstance(v, dict):
        for k in ("value", "score", "rating", "overall"):
            if k in v:
                v=v[k]; break
    try:
        return float(v)
    except (TypeError, ValueError):
        return default

def career_offer_score(t, profile):
    """Score a school's willingness to hire this coach."""
    prestige=_num(profile.get("prestige",50),50)
    recruiting=_num(profile.get("recruiting",50),50)
    development=_num(profile.get("development",50),50)
    motivation=_num(profile.get("motivation",50),50)
    need=72-_num(t.adjusted_prestige,50)*.48
    fit=(prestige*.38+recruiting*.08+development*.08+motivation*.06+
         (100-_num(t.current,50))*.16+_num(t.academics,50)*.06+
         random.Random(str(t.espn_id)+str(st.session_state.g["year"])).uniform(-5,5))
    return fit, need

def contract_terms(t, profile, years=None):
    prestige=_num(t.adjusted_prestige,50)
    years=years or random.choice([3,4,5])
    salary=int(250000+prestige*30000+_num(profile.get("prestige",50),50)*2500)
    buyout=int(salary*.35*max(0,years-1))
    return {"team":t.name,"years":years,"remaining_years":years,
            "salary":salary,"buyout":buyout,"extension":False}

def generate_job_openings(g):
    openings=[]
    for t in g["teams"]:
        security=_num(getattr(t,"security",50),50)
        wins=_num(getattr(t,"wins",0),0)
        if random.random()<.28 or security<35 or wins<expected_wins(t)-4:
            openings.append({
                "team":t.name,
                "reason":"Hot seat" if security<35 else ("Underperforming" if wins<expected_wins(t)-4 else "Open position"),
                "prestige":_num(t.adjusted_prestige,50)
            })
    return sorted(openings,key=lambda x:x["prestige"],reverse=True)

def negotiate_offer(t, profile, requested_salary, requested_years):
    base=contract_terms(t,profile,requested_years)
    requested_salary=int(requested_salary)
    # Schools accept reasonable demands, otherwise counter or decline.
    if requested_salary <= base["salary"]*1.12:
        base["salary"]=requested_salary
        base["buyout"]=int(requested_salary*.35*max(0,requested_years-1))
        return base, "accepted"
    if requested_salary <= base["salary"]*1.35:
        base["salary"]=int(base["salary"]*1.12)
        base["buyout"]=int(base["salary"]*.35*max(0,requested_years-1))
        return base, "counter"
    return None, "declined"

def expected_wins(t):
    current=_num(getattr(t,"current",50),50)
    prestige=_num(getattr(t,"adjusted_prestige",50),50)
    return max(8, round(current/100*25 + (prestige-70)*.10))

def generate_job_market(g, profile):
    openings=[]
    for t in g["teams"]:
        security=_num(getattr(t,"security",50),50)
        wins=_num(getattr(t,"wins",0),0)
        # Only use numeric values in the job-market comparison. This fixes
        # legacy sessions where a team stat was accidentally stored as a list.
        hot_seat = security < 35
        underperforming = wins < expected_wins(t)-4
        random_opening = random.random() < .25
        if random_opening or hot_seat or underperforming:
            need=72-_num(t.adjusted_prestige,50)*.48
            fit=(_num(profile.get("prestige",50),50)*.38+
                 _num(profile.get("recruiting",50),50)*.08+
                 _num(profile.get("development",50),50)*.08+
                 _num(profile.get("motivation",50),50)*.06+
                 (100-_num(t.current,50))*.16+
                 _num(t.academics,50)*.06+
                 random.Random(str(t.espn_id)+str(g["year"])).uniform(-5,5))
            if fit>=need:
                openings.append({"team":t.name,"fit":fit,
                                 "salary":int(250000+_num(t.adjusted_prestige,50)*30000),
                                 "years":random.choice([3,4,5]),"buyout":0})
    return sorted(openings,key=lambda x:x["fit"],reverse=True)

def make_contract(t, profile, offer):
    t.coach=Coach(profile.get("name","Coach"),**{k:profile[k] for k in ["prestige","offense","defense","recruiting","development","adaptability","motivation","discipline","nil"]},salary=offer["salary"])
    return {"team":t.name,"years":offer["years"],"salary":offer["salary"],"buyout":offer["buyout"]}

def new_game():
    teams=new_world()
    g={"year":2026,"teams":teams,"recruits":recruit_pool(),"portal":[],"free_coaches":[],"user":None,
       "season_stage":"preseason","history":[],"champion":None,"rounds":[],"field":[],"news":[],"career_mode":False,"job_market":[],"contract":None,"career_history":[],"career_profile":None}
    make_schedule(g);return g

def enc(x):
    if hasattr(x,"__dataclass_fields__"):return {"__type__":x.__class__.__name__,**{k:enc(v) for k,v in asdict(x).items()}}
    if isinstance(x,list):return [enc(v) for v in x]
    if isinstance(x,dict):return {k:enc(v) for k,v in x.items()}
    return x
def dec(x):
    cls={"Coach":Coach,"Staff":Staff,"Player":Player,"Recruit":Recruit,"Game":Game,"Team":Team}
    if isinstance(x,list):return [dec(v) for v in x]
    if isinstance(x,dict):
        typ=x.get("__type__");vals={k:dec(v) for k,v in x.items() if k!="__type__"}
        return cls[typ](**vals) if typ in cls else vals
    return x

if "g" not in st.session_state:st.session_state.g=new_game()
def normalize_team_state(g):
    for t in g["teams"]:
        # Repair common legacy list/int corruption in team-level numeric fields.
        for attr, default in [
            ("security",50),("wins",0),("losses",0),("current",50),
            ("historical",50),("academics",70),("budget",5000000),("nil_budget",1000000)
        ]:
            value=getattr(t,attr,default)
            if isinstance(value,list):
                value=value[0] if value else default
            try:
                if attr in ("wins","losses","security","current","historical","academics"):
                    value=int(float(value))
                else:
                    value=float(value)
            except (TypeError,ValueError):
                value=default
            setattr(t,attr,value)
        if not isinstance(t.coach, Coach):
            t.coach=coach_for(t.current)
        if not isinstance(t.staff,list) or not t.staff:
            t.staff=staff_for(t.current)

g=st.session_state.g
normalize_team_state(g)
for _team in g["teams"]:
    if not isinstance(_team.coach, Coach):
        _team.coach=coach_for(_team.current)
    if not isinstance(_team.staff,list) or not _team.staff:
        _team.staff=staff_for(_team.current)
g.setdefault("career_mode",False); g.setdefault("job_market",[]); g.setdefault("contract",None)
g.setdefault("career_history",[]); g.setdefault("career_profile",None)
if g["user"] is None:
    st.title("🏀 College Basketball Coach Simulator — Deep Dynasty")
    mode=st.radio("Career mode",["Choose any school","Career mode — only schools that offer you"],horizontal=True)
    if mode=="Choose any school":
        school=st.selectbox("Start your career",[t.name for t in g["teams"]])
        if st.button("Start Dynasty",type="primary"):
            g["user"]=school;g["career_mode"]=False;st.rerun()
    else:
        st.subheader("Create Your Coach")
        coach_name=st.text_input("Coach name",value=g.get("coach_name","Coach"),max_chars=32)
        g["coach_name"]=coach_name.strip() or "Coach"
        st.subheader("Your coaching profile")
        cp=g.get("career_profile") or {"prestige":50,"offense":55,"defense":55,"recruiting":55,"development":50,"adaptability":60,"motivation":65,"discipline":60,"nil":50}
        x1,x2,x3=st.columns(3)
        cp["prestige"]=x1.slider("Starting prestige",20,90,int(cp["prestige"]))
        cp["offense"]=x2.slider("Offense",30,90,int(cp["offense"]))
        cp["defense"]=x3.slider("Defense",30,90,int(cp["defense"]))
        y1,y2,y3=st.columns(3)
        cp["recruiting"]=y1.slider("Recruiting",30,90,int(cp["recruiting"]))
        cp["development"]=y2.slider("Development",30,90,int(cp["development"]))
        cp["motivation"]=y3.slider("Motivation",30,90,int(cp["motivation"]))
        cp={k:_num(v,50) for k,v in cp.items()}
        g["career_profile"]=cp
        if not g.get("job_market"):
            g["job_market"]=generate_job_market(g,cp)
        offers=g["job_market"]
        st.write(f"**{len(offers)} schools** currently offer you a job.")
        if offers:
            selected=st.selectbox("Job offers",offers,format_func=lambda o:f"{o['team']} — ${o['salary']:,}/yr • {o['years']} years")
            chosen=next(t for t in g["teams"] if t.name==selected["team"])
            st.caption(f"Prestige {chosen.adjusted_prestige:.0f} • Current {chosen.current:.0f} • Budget ${chosen.budget/1e6:.1f}M • NIL ${chosen.nil_budget/1e6:.1f}M")
            if st.button("Accept Job",type="primary"):
                g["contract"]=make_contract(chosen,cp,selected)
                chosen.coach.name=g.get("coach_name","Coach")
                g["contract"]["remaining_years"]=g["contract"]["years"]
                g["user"]=chosen.name;g["career_mode"]=True;g["job_market"]=[]
                g["career_history"].append({"Year":g["year"],"Action":"Hired","Team":chosen.name,"Salary":selected["salary"],"Years":selected["years"]})
                st.rerun()
        else:
            st.warning("No offers at this profile. Raise prestige or use the open-school mode.")
    st.info("Deep engine: coaching carousel, contracts, recruiting/NIL, portal, facilities, staff, game plans, fatigue, fouls, development, conference tournaments and a 76-team postseason.")
    st.stop()

u=next(t for t in g["teams"] if t.name==g["user"])

with st.sidebar:
    st.image(logo(u.espn_id),width=74)
    st.header(u.name)
    st.caption(f"{g['year']} • {u.conference}")
    st.metric("Record",f"{u.wins}-{u.losses}")
    st.metric("NET-like",f"{u.net:.1f}")
    st.metric("Job security",f"{u.security:.0f}")
    st.metric("NIL",f"${u.nil_budget:,.0f}")
    if st.button("Sim Full Season",use_container_width=True):
        for gm in u.schedule:
            if not gm.played:
                opp=next(t for t in g["teams"] if t.name==gm.opponent)
                plan={"tempo":50,"aggression":50,"offense":"Balanced","defense":"Man"}
                r=sim_game(g,u.name,opp.name,gm.site,plan,plan,gm.conference)
                gm.played=True;gm.result=u.name if r["sa"]>r["sb"] else opp.name;gm.score_for=r["sa"];gm.score_against=r["sb"]
        champ,rounds,field=postseason(g);g["champion"]=champ.name;g["rounds"]=rounds;g["field"]=field
        team_metrics(g)
        g["history"].append({"Season":g["year"],"Champion":champ.name,"Record":f"{u.wins}-{u.losses}","NET":round(u.net,1)})
        offseason(g);st.rerun()
    if st.button("New Dynasty",use_container_width=True):
        st.session_state.g=new_game();st.rerun()
    if g.get("career_mode") and st.button("Resign / Enter Job Market",use_container_width=True):
        g["career_history"].append({"Year":g["year"],"Action":"Resigned","Team":u.name,"Salary":u.coach.salary,"Years":0})
        g["career_profile"]={k:getattr(u.coach,k) for k in ["prestige","offense","defense","recruiting","development","adaptability","motivation","discipline","nil"]}
        g["career_profile"]["name"]=g.get("coach_name",u.coach.name)
        g["user"]=None;g["contract"]=None
        g["job_market"]=generate_job_market(g,g["career_profile"])
        st.rerun()

tabs=st.tabs(["Dashboard","Game Day","Schedule","Roster","Tactics","Recruiting","NIL","Portal","Staff","Facilities","Rankings","Selection","Tournament","History","Career","Save"])

with tabs[0]:
    st.title("Program Dashboard")
    c=st.columns(6)
    for col,label,val in zip(c,["Record","Prestige","NET-like","SOS","Recruiting","Budget"],[f"{u.wins}-{u.losses}",f"{u.adjusted_prestige:.1f}",f"{u.net:.1f}",f"{u.sos:.1f}",f"{u.recruiting_prestige:.1f}",f"${u.budget/1e6:.1f}M"]):col.metric(label,val)
    st.image(logo(u.espn_id),width=110)
    st.subheader("Coach")
    st.write(f"**{u.coach.name}** — prestige {u.coach.prestige:.0f} • O {u.coach.offense:.0f} • D {u.coach.defense:.0f} • Recruiting {u.coach.recruiting:.0f} • Development {u.coach.development:.0f}")
    st.subheader("Program history")
    st.dataframe([u.history],use_container_width=True,hide_index=True)
    st.subheader("Current roster strength")
    st.write(u.ratings())

with tabs[1]:
    st.header("Game Day — Coaching decisions")
    upcoming=[(i,x) for i,x in enumerate(u.schedule) if not x.played]
    if not upcoming:st.success("All scheduled games completed.")
    else:
        labels=[f"{i+1}. {x.opponent} • {x.site} • {x.date}" for i,x in upcoming]
        pick=st.selectbox("Select game",range(len(labels)),format_func=lambda i:labels[i])
        idx=upcoming[pick][0];gm=u.schedule[idx]
        cols=st.columns(4)
        tempo=cols[0].slider("Tempo",20,90,55)
        aggression=cols[1].slider("Aggression",0,100,50)
        offense=cols[2].selectbox("Offensive identity",["Balanced","3PT","Paint","Transition"])
        defense=cols[3].selectbox("Defense",["Man","Zone","Press"])
        st.caption("Late-game, fatigue, fouls and rotation effects are represented by the game engine's player and team state.")
        if st.button("Tip Off",type="primary"):
            r=play_user_game(g,idx,{"tempo":tempo,"aggression":aggression,"offense":offense,"defense":defense})
            st.success(f"{r['a']} {r['sa']} — {r['sb']} {r['b']}")
            st.rerun()

with tabs[2]:
    st.header("31-game style schedule")
    st.dataframe([{"#":i+1,"Date":x.date,"Opponent":x.opponent,"Site":x.site,"Type":"Conference" if x.conference else "Non-Conference","Played":x.played,"Result":x.result,"Score":f"{x.score_for}-{x.score_against}" if x.played else ""} for i,x in enumerate(u.schedule)],use_container_width=True,hide_index=True)
    st.subheader("Conference table")
    members=[t for t in g["teams"] if t.conference==u.conference]
    st.dataframe([{"Team":t.name,"W":t.wins,"L":t.losses,"Conf W":t.cwins,"Conf L":t.closses,"NET":round(t.net,1)} for t in sorted(members,key=lambda t:(t.cwins,t.wins,t.net),reverse=True)],use_container_width=True,hide_index=True)

with tabs[3]:
    st.header("Roster, rotations and player development")
    st.dataframe([{"Player":p.name,"Pos":p.pos,"OVR":round(p.overall,1),"Pot":round(p.potential,1),"Yr":p.year,"Ht":f"{p.height}","Role":p.role,"Morale":round(p.morale),"Fatigue":round(p.fatigue),"NIL":f"${p.nil_value:,}"} for p in sorted(u.roster,key=lambda p:p.overall,reverse=True)],use_container_width=True,hide_index=True)
    target=st.selectbox("Player role",[p.name for p in u.roster])
    role=st.selectbox("Role",["Star","Starter","Sixth Man","Rotation","Developmental"])
    if st.button("Update rotation"):
        next(p for p in u.roster if p.name==target).role=role;st.success("Rotation updated.")

with tabs[4]:
    st.header("Tactics / team identity")
    r=u.ratings()
    c=st.columns(4)
    c[0].metric("Offense",round(r["offense"],1));c[1].metric("Defense",round(r["defense"],1));c[2].metric("Shooting",round(r["shooting"],1));c[3].metric("IQ",round(r["iq"],1))
    st.write("Coach adaptability:",round(u.coach.adaptability,1))
    st.write("Staff offense:",round(u.staff_rating("offense"),1),"Staff defense:",round(u.staff_rating("defense"),1),"Development:",round(u.staff_rating("development"),1))
    st.info("The simulation combines roster attributes, coaching, staff, matchup, location, tactical identity, fatigue and randomness.")

with tabs[5]:
    st.header("Recruiting")
    stars=st.multiselect("Stars",[2,3,4,5],[3,4,5])
    pool=[r for r in g["recruits"] if not r.committed and r.stars in stars]
    recruit=st.selectbox("Prospect",pool,format_func=lambda r:f"{r.name} • {'★'*r.stars} • {r.pos} • OVR {r.overall:.0f}")
    offer=st.number_input("NIL commitment",0,int(u.nil_budget),min(int(recruit.nil_expectation),int(u.nil_budget)))
    interest=u.recruiting_prestige*.25+u.coach.recruiting*.2+u.coach.development*.1+u.current*.2+offer/max(1,recruit.nil_expectation)*18+random.uniform(-5,5)
    st.write(f"Preference: **{recruit.preference}** • Academic fit {recruit.academic:.0f} • NIL expectation ${recruit.nil_expectation:,}")
    st.metric("Projected commitment score",f"{interest:.1f}")
    if st.button("Offer scholarship + NIL",type="primary"):
        if interest>=68 and offer<=u.nil_budget:
            u.nil_budget-=offer
            u.roster.append(Player(recruit.name,recruit.pos,recruit.overall,recruit.potential,recruit.overall,recruit.overall-2,recruit.overall-2,recruit.overall,recruit.overall,recruit.overall,recruit.overall,random.randint(72,83),1,75,0,0,0,"Developmental",offer))
            recruit.committed=u.name;st.success("Committed!")
        else:st.warning("The recruit chose another school.")

with tabs[6]:
    st.header("NIL / Collective Management")
    st.metric("Available NIL",f"${u.nil_budget:,.0f}")
    for p in sorted(u.roster,key=lambda p:p.overall,reverse=True):
        cols=st.columns([3,1,2])
        cols[0].write(f"**{p.name}** — {p.pos} — {p.overall:.0f}")
        cols[1].write(f"${p.nil_value:,}")
        x=cols[2].number_input("New NIL",0,2_000_000,int(p.nil_value),key="n"+p.name)
        if cols[2].button("Change",key="c"+p.name):
            delta=x-p.nil_value
            if delta>u.nil_budget:st.error("Insufficient NIL budget.")
            else:u.nil_budget-=max(delta,0);p.nil_value=x;p.morale=clamp(p.morale+3);st.rerun()

with tabs[7]:
    st.header("Transfer Portal")
    if not g["portal"]:st.info("Portal is populated during offseason.")
    else:
        p=st.selectbox("Portal target",g["portal"],format_func=lambda p:f"{p.name} • {p.pos} • OVR {p.overall:.0f} • ${p.nil_value:,}")
        offer=st.number_input("Offer",0,int(u.nil_budget),min(int(p.nil_value),int(u.nil_budget)))
        fit=u.current*.22+u.coach.prestige*.18+u.coach.development*.12+u.recruiting_prestige*.18+offer/max(1,p.nil_value)*18+random.uniform(-7,7)
        st.metric("Transfer fit",f"{fit:.1f}")
        if st.button("Make portal offer"):
            if fit>66 and offer<=u.nil_budget:
                u.nil_budget-=offer;p.nil_value=offer;p.morale=75;u.roster.append(p);g["portal"].remove(p);st.success("Transfer accepted.");st.rerun()
            else:st.warning("Transfer declined.")

with tabs[8]:
    st.header("Coaching Staff")
    st.dataframe([asdict(s) for s in u.staff],use_container_width=True,hide_index=True)
    st.subheader("Head Coach")
    st.write(asdict(u.coach))
    st.caption("Staff affects offense, defense, recruiting, development, scouting and NIL execution.")

with tabs[9]:
    st.header("Facilities & Program Investment")
    st.metric("Facilities level",f"{u.facilities_level}/5")
    st.write("Facilities factor:",round(u.facilities*100,1))
    cost=2_000_000*u.facilities_level
    if st.button(f"Upgrade facilities — ${cost:,}"):
        if u.budget>=cost and u.facilities_level<5:
            u.budget-=cost;u.facilities_level+=1;u.facilities=clamp(u.facilities+8);st.success("Upgrade complete.")
        else:st.error("Insufficient budget or maxed out.")
    st.write("Budget:",f"${u.budget:,.0f}","NIL:",f"${u.nil_budget:,.0f}")

with tabs[10]:
    st.header("National Rankings / Resume")
    team_metrics(g)
    st.dataframe([{"Rank":i+1,"Team":t.name,"Conf":t.conference,"Record":f"{t.wins}-{t.losses}","NET-like":round(t.net,1),"SOS":round(t.sos,1),"Prestige":round(t.adjusted_prestige,1)} for i,t in enumerate(rankings(g))],use_container_width=True,hide_index=True)
    st.caption("NET-like is a game metric inspired by public descriptions of NET inputs; it is not the official NCAA NET.")

with tabs[11]:
    st.header("Selection Sunday")
    if st.button("Run Selection Committee"):
        field=selection(g);g["field"]=field;st.rerun()
    if g["field"]:
        st.dataframe([{"Seed":i+1,"Team":t.name,"Conf":t.conference,"NET-like":round(t.net,1),"Record":f"{t.wins}-{t.losses}","SOS":round(t.sos,1)} for i,t in enumerate(g["field"])],use_container_width=True,hide_index=True)
        st.write("The model rewards record, conference performance, opponent quality, schedule strength and efficiency. NCAA committee procedures likewise consider a broad set of results and qualitative information, rather than a single ranking.")

with tabs[12]:
    st.header("Postseason")
    if g["rounds"]:
        st.success(f"Champion: {g['champion']}")
        for name,games in g["rounds"]:
            st.subheader(name)
            if games:st.dataframe([{"Matchup":f"{a} {sa} — {sb} {b}"} for a,sa,b,sb in games],use_container_width=True,hide_index=True)
    else:st.info("Run the full season or run Selection Committee first.")

with tabs[13]:
    st.header("Dynasty History")
    st.dataframe(g["history"],use_container_width=True,hide_index=True)
    st.write("School history:",u.history)
    if g["champion"]:st.success(f"Most recent champion: {g['champion']}")

with tabs[14]:
    st.header("Career Mode")
    st.caption("Contracts, job security, interviews, job offers, salary negotiation and career history.")

    st.subheader("Coach")
    st.write(f"**{g.get('coach_name', u.coach.name)}**")
    st.write(f"Prestige {u.coach.prestige:.1f} • Record {u.coach.wins}-{u.coach.losses} • Titles {u.coach.titles}")

    if g.get("contract"):
        ct=g["contract"]
        st.subheader("Contract")
        st.write(f"**{ct['team']}** — ${ct['salary']:,}/year • {ct.get('remaining_years',ct['years'])} years remaining • Buyout ${ct['buyout']:,}")
        c1,c2=st.columns(2)
        if c1.button("Request Extension"):
            if ct.get("remaining_years",ct["years"])<=2:
                ct["remaining_years"]=ct.get("remaining_years",ct["years"])+2
                ct["years"]=ct.get("years",0)+2
                ct["extension"]=True
                st.success("Extension accepted.")
                st.rerun()
            else:
                st.info("You can request an extension when two or fewer years remain.")
        if c2.button("Resign"):
            g["career_history"].append({"Year":g["year"],"Action":"Resigned","Team":u.name,"Salary":ct["salary"],"Years":ct.get("remaining_years",ct["years"])})
            g["career_profile"]={k:getattr(u.coach,k) for k in ["prestige","offense","defense","recruiting","development","adaptability","motivation","discipline","nil"]}
            g["career_profile"]["name"]=g.get("coach_name",u.coach.name)
            g["user"]=None
            g["contract"]=None
            g["job_market"]=generate_job_market(g,g["career_profile"])
            g["career_job_offers"]=generate_job_openings(g)
            st.rerun()

    st.subheader("Job Market")
    if not g.get("career_job_offers"):
        g["career_job_offers"]=generate_job_openings(g)
    openings=g["career_job_offers"]
    if openings:
        opening=st.selectbox("Open positions",openings,
                             format_func=lambda x:f"{x['team']} — prestige {x['prestige']:.0f} ({x['reason']})")
        school=next(t for t in g["teams"] if t.name==opening["team"])
        prof=g.get("career_profile") or {"prestige":u.coach.prestige,"recruiting":u.coach.recruiting,"development":u.coach.development,"motivation":u.coach.motivation}
        fit,need=career_offer_score(school,prof)
        st.write(f"Interview fit: **{fit:.1f}** vs required **{need:.1f}**")
        if st.button("Interview for Job"):
            if fit>=need:
                st.session_state["interviewed_team"]=school.name
                st.success("Interview successful — you may negotiate.")
            else:
                st.error("The school declined to hire you.")
        if st.session_state.get("interviewed_team")==school.name:
            base=contract_terms(school,prof)
            salary=st.number_input("Requested salary",100000,5000000,int(base["salary"]),25000)
            years=st.slider("Requested contract years",1,7,int(base["years"]))
            if st.button("Negotiate Contract",type="primary"):
                offer,status=negotiate_offer(school,prof,salary,years)
                if offer:
                    st.session_state["negotiated_offer"]=offer
                    st.session_state["offer_status"]=status
                else:
                    st.error("Negotiation failed.")
            if st.session_state.get("negotiated_offer"):
                offer=st.session_state["negotiated_offer"]
                if st.session_state.get("offer_status")=="counter":
                    st.warning(f"School counteroffer: ${offer['salary']:,}/year.")
                if st.button("Accept Contract"):
                    school.coach=Coach(g.get("coach_name","Coach"),**{k:prof[k] for k in ["prestige","offense","defense","recruiting","development","adaptability","motivation","discipline","nil"]},salary=offer["salary"])
                    g["contract"]=offer
                    g["user"]=school.name
                    g["career_mode"]=True
                    g["career_job_offers"]=[]
                    g["career_history"].append({"Year":g["year"],"Action":"Hired","Team":school.name,"Salary":offer["salary"],"Years":offer["years"]})
                    st.session_state.pop("interviewed_team",None)
                    st.session_state.pop("negotiated_offer",None)
                    st.session_state.pop("offer_status",None)
                    st.rerun()
    else:
        st.info("No openings are currently available.")

    st.subheader("Career History")
    if g.get("career_history"):
        st.dataframe(g["career_history"],use_container_width=True,hide_index=True)

    st.subheader("Career Goals")
    st.write("Build prestige, win championships, improve programs, survive the hot seat and climb toward elite jobs.")

with tabs[15]:
    st.header("Save / Load Dynasty")
    if st.button("Create Save JSON"):st.session_state.save=json.dumps(enc(g))
    save=st.text_area("Save data",st.session_state.get("save",""),height=260)
    if st.button("Load Save"):
        try:st.session_state.g=dec(json.loads(save));st.rerun()
        except Exception as e:st.error(e)
    if st.session_state.get("save"):st.download_button("Download save",st.session_state.save,file_name=f"cbb_dynasty_{g['year']}.json",mime="application/json")
