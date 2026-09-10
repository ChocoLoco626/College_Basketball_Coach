
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import random

SAVE_SCHEMA_VERSION=2

def clamp(x,lo=0,hi=100): return max(lo,min(hi,float(x)))

@dataclass
class Player:
    name:str; pos:str; overall:float; potential:float
    offense:float; defense:float; shooting:float; passing:float
    handling:float; rebounding:float; athleticism:float; iq:float
    height:int; year:str; morale:float
    fatigue:float=0; fouls:int=0; minutes:float=0
    role:str="Rotation"; nil_value:int=0; scholarship:bool=True
    stars:int=3; hometown:str="USA"; commitment:Optional[str]=None
    transfer_risk:float=10; injured:bool=False; injury_weeks:int=0

@dataclass
class Coach:
    name:str; prestige:float=50; offense:float=55; defense:float=55
    recruiting:float=55; development:float=50; adaptability:float=60
    motivation:float=65; discipline:float=60; loyalty:float=55; nil:float=50
    salary:int=300000; wins:int=0; losses:int=0; titles:int=0

@dataclass
class Staff:
    name:str; role:str; rating:float=50; salary:int=100000
    specialty:str="General"; recruiting_bonus:float=0; development_bonus:float=0

@dataclass
class Game:
    opponent:str; site:str; date:str; conference:bool=False
    played:bool=False; result:Optional[str]=None; points_for:int=0; points_against:int=0
    importance:float=1.0

@dataclass
class Recruit:
    name:str; position:str; stars:int; overall:int; potential:int
    academics:int; nil_demand:int; interest:Dict[str,float]=field(default_factory=dict)
    committed_to:Optional[str]=None

@dataclass
class Contract:
    team:str; years:int; remaining_years:int; salary:int; buyout:int
    extension:bool=False

@dataclass
class CareerProfile:
    name:str="Coach"; prestige:float=35; offense:float=55; defense:float=55
    recruiting:float=55; development:float=50; adaptability:float=60
    motivation:float=65; discipline:float=60; loyalty:float=55; nil:float=50
    career_wins:int=0; career_losses:int=0; championships:int=0

@dataclass
class Team:
    name:str; conference:str; espn_id:str; historical:float; current:float
    facilities_level:int=5; budget:int=5_000_000; nil_budget:int=1_000_000
    academics:float=75; security:float=60
    coach:Coach=field(default_factory=lambda:Coach("Head Coach"))
    roster:List[Player]=field(default_factory=list); staff:List[Staff]=field(default_factory=list)
    schedule:List[Game]=field(default_factory=list); history:List[dict]=field(default_factory=list)
    recruits:List[Recruit]=field(default_factory=list); transfers:List[Player]=field(default_factory=list)
    wins:int=0; losses:int=0; conference_wins:int=0; conference_losses:int=0
    tournament_result:str=""; fan_support:float=65; boosters:float=60
    conference_tournament_seed:int=0; ncaa_seed:int=0; probation:bool=False

    @property
    def adjusted_prestige(self):
        return clamp(.30*self.historical+.32*self.current+.14*self.facilities_level*10+
                      .12*self.academics+.12*self.fan_support)

    @property
    def recruiting_prestige(self):
        return clamp(.40*self.current+.16*self.historical+.14*self.facilities_level*10+
                      .14*self.nil_budget/100000+.08*self.academics+.08*self.boosters)

    def ratings(self):
        ps=sorted([p for p in self.roster if isinstance(p,Player) and not p.injured],
                  key=lambda p:p.overall,reverse=True)[:10]
        if not ps: return {"overall":50,"offense":50,"defense":50,"depth":40}
        avg=lambda k:sum(getattr(p,k,50) for p in ps)/len(ps)
        depth=sum(p.overall for p in self.roster if isinstance(p,Player))/max(1,len(self.roster))
        return {"overall":round(.78*avg("overall")+.22*depth,1),
                "offense":round(avg("offense"),1),"defense":round(avg("defense"),1),
                "depth":round(depth,1)}
