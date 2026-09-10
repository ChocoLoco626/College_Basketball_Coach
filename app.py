
import streamlit as st
from models import *
from teams import *
from simulation import *
from recruiting import *
from career import *
from save_system import *
from dynasty import *

st.set_page_config(page_title="College Basketball Coach Simulator",page_icon="🏀",layout="wide")
if "g" not in st.session_state: st.session_state.g=new_game()
g=migrate_game_state(st.session_state.g); st.session_state.g=g

st.sidebar.title("🏀 Coach Simulator")
if st.sidebar.button("New Dynasty",use_container_width=True):
    st.session_state.g=new_game(); st.rerun()
st.sidebar.write(f"Season **{g['year']}-{str(g['year']+1)[-2:]}**")
st.sidebar.write(f"Engine schema **v{g['schema_version']}**")

if g.get("user"):
    user=next(t for t in g["teams"] if t.name==g["user"])
else: user=None

tabs=st.tabs(["Career","Dashboard","Season Hub","Game Day","Recruiting","Transfer Portal","Schedule","Team","Staff","History"])

with tabs[0]:
    st.header("Career Mode")
    g["coach_name"]=st.text_input("Coach name",g.get("coach_name","Coach"),max_chars=32) or "Coach"
    if not g.get("career_started"):
        tier=st.radio("Starting prestige — locked after starting",
                      ["Entry: 35","Mid Major: 50","High Major: 65"],horizontal=True)
        start=int(tier.split(":")[1])
        if st.button("Start Career",type="primary"):
            g["career_started"]=True; g["career_mode"]=True
            g["career_profile"]=CareerProfile(g["coach_name"],prestige=start)
            g["job_market"]=generate_job_market(g["teams"],g["career_profile"])
            st.rerun()
    else:
        cp=g["career_profile"]; cp.name=g["coach_name"]
        c=st.columns(4); c[0].metric("Prestige",f"{cp.prestige:.1f}"); c[1].metric("Career W",cp.career_wins)
        c[2].metric("Career L",cp.career_losses); c[3].metric("Titles",cp.championships)
        if user:
            st.success(f"You currently coach **{user.name}**.")
            if g.get("contract_expired"): st.warning("Your contract has expired. You may pursue another eligible opening.")
        st.subheader("Coaching Carousel")
        if st.button("Refresh Job Market"): g["job_market"]=generate_job_market(g["teams"],cp); st.rerun()
        if g["job_market"]:
            choice=st.selectbox("Eligible openings",g["job_market"],
                format_func=lambda x:f"{x['team']} | {x['tier']} | Fit {x['fit']} | ${x['salary']:,}")
            t=next(t for t in g["teams"] if t.name==choice["team"])
            st.caption(f"Program prestige {t.adjusted_prestige:.0f} • Historical {t.historical:.0f} • Current {t.current:.0f}")
            if st.button("Accept Job",type="primary"):
                cp.name=g["coach_name"]
                t.coach=Coach(cp.name,cp.prestige,cp.offense,cp.defense,cp.recruiting,cp.development,
                              cp.adaptability,cp.motivation,cp.discipline,cp.loyalty,cp.nil,choice["salary"])
                g["contract"]=make_contract(t,choice); g["user"]=t.name; g["job_market"]=[]; st.rerun()
        else: st.info("No eligible openings. Refresh the market as the season changes.")

with tabs[1]:
    if user:
        st.header(user.name)
        c=st.columns(6)
        vals=[f"{user.wins}-{user.losses}",f"{user.adjusted_prestige:.0f}",f"{user.ratings()['overall']:.0f}",
              f"{user.ratings()['offense']:.0f}",f"{user.ratings()['defense']:.0f}",f"${user.nil_budget:,}"]
        for col,label,val in zip(c,["Record","Prestige","Roster","Offense","Defense","NIL"],vals): col.metric(label,val)
        st.write(f"**Coach:** {user.coach.name} • Prestige {user.coach.prestige:.0f} • Security {user.security:.0f}")
        st.progress(user.security/100,"Job Security")
        st.subheader("Program History")
        st.dataframe(user.history,use_container_width=True,hide_index=True)
    else: st.info("Start Career and accept an eligible job.")

with tabs[3]:
    if user:
        if g.get("season_stage")!="regular_season":
            st.info(f"Game Day is unavailable during the {g.get('season_stage','preseason')} stage. Use Season Hub to advance.")
        else:
            pending=[x for x in user.schedule if not x.played]
            if not pending:
                g["season_stage"]="postseason"; st.rerun()
            else:
                gm=pending[0]; opp=next(t for t in g["teams"] if t.name==gm.opponent)
                st.header(f"Game Day — {gm.site} vs {opp.name}")
                a=st.columns(3)
                tempo=a[0].slider("Tempo",55,82,68); aggression=a[1].slider("Offensive aggression",30,90,60)
                defense=a[2].selectbox("Defense",["Conservative","Balanced","Aggressive"])
                st.write(f"Opponent strength: **{opp.ratings()['overall']:.1f}**")
                if st.button("Play Game",type="primary"):
                    pf,pa,win=play_game(user,opp,gm.site,tempo,aggression,defense)
                    gm.played=True; gm.result="W" if win else "L"; gm.points_for=pf; gm.points_against=pa
                    if gm.conference:
                        user.conference_wins+=int(win); user.conference_losses+=int(not win)
                    user.security=clamp(user.security+(1.0 if win else -.8))
                    for p in user.roster:
                        p.fatigue=clamp(p.fatigue+random.uniform(3,12)); p.morale=clamp(p.morale+(2 if win else -2))
                        if random.random()<.025:
                            p.injured=True; p.injury_weeks=random.randint(1,5)
                    if all(x.played for x in user.schedule): g["season_stage"]="postseason"
                    st.success(f"{'WIN' if win else 'LOSS'} — {pf}-{pa}")
                    st.rerun()
    else: st.info("Take a job first.")

with tabs[4]:
    if user:
        st.header("Recruiting & NIL")
        pool=update_interest(user,g["recruit_pool"])
        c=st.columns(3); c[0].metric("Recruiting Prestige",f"{user.recruiting_prestige:.1f}")
        c[1].metric("NIL Budget",f"${user.nil_budget:,}"); c[2].metric("Coach Recruiting",f"{user.coach.recruiting:.0f}")
        st.dataframe([{"Name":r.name,"Pos":r.position,"Stars":r.stars,"OVR":r.overall,"Potential":r.potential,
                       "Interest":r.interest.get(user.name,0),"NIL":f"${r.nil_demand:,}"} for r in pool[:30]],
                     use_container_width=True,hide_index=True)
        names=[r.name for r in pool if r.interest.get(user.name,0)>=55][:20]
        if names:
            selected=st.selectbox("Recruit to pursue",names)
            r=next(x for x in pool if x.name==selected)
            if st.button("Offer Scholarship + NIL"):
                if offer_recruit(user,r): st.success(f"{r.name} committed!"); st.rerun()
                else: st.error("Recruiting/NIL requirements not met.")
    else: st.info("Take a job first.")

with tabs[5]:
    if user:
        st.header("Transfer Portal")
        pool=g.get("transfer_pool",[])
        if not pool:
            pool=process_transfer_portal(g["teams"]); g["transfer_pool"]=pool
        st.write(f"Available players: **{len(pool)}**")
        if pool:
            p=st.selectbox("Portal player",pool,key="portal_player",format_func=lambda x:f"{x.name} — {x.pos} — OVR {x.overall} — NIL ${x.nil_value:,}")
            if st.button("Offer Portal NIL"):
                if transfer_offer(user,p): g["transfer_pool"]=[x for x in pool if x is not p]; st.success("Player transferred in."); st.rerun()
                else: st.error("Player rejected the offer or NIL budget is insufficient.")
        if st.button("Regenerate Portal"):
            g["transfer_pool"]=process_transfer_portal(g["teams"]); st.rerun()
    else: st.info("Take a job first.")

with tabs[6]:
    if user:
        if not user.schedule: generate_schedule(user,g["teams"],g["year"])
        st.dataframe([vars(x) for x in user.schedule],use_container_width=True,hide_index=True)
    else: st.info("Take a job first.")

with tabs[7]:
    if user:
        st.header("Roster & Development")
        st.dataframe([{"Name":p.name,"Pos":p.pos,"OVR":p.overall,"Pot":p.potential,"Year":p.year,"Morale":round(p.morale),
                       "Fatigue":round(p.fatigue),"NIL":f"${p.nil_value:,}","Stars":p.stars,"Injured":p.injured}
                      for p in user.roster],use_container_width=True,hide_index=True)
        if st.button("Develop Players"):
            bonus=(user.coach.development+sum(s.development_bonus for s in user.staff))/120
            for p in user.roster: p.overall=min(p.potential,p.overall+random.uniform(.2,1.2)*bonus)
            st.success("Development session complete."); st.rerun()
    else: st.info("Take a job first.")

with tabs[8]:
    if user:
        st.header("Staff & Facilities")
        st.dataframe([vars(s) for s in user.staff],use_container_width=True,hide_index=True)
        c=st.columns(3)
        if c[0].button("Hire Assistant"):
            cost=150000+user.adjusted_prestige*5000
            if user.budget>=cost:
                user.budget-=int(cost); user.staff.append(Staff(f"Assistant {len(user.staff)+1}","Assistant",
                    random.randint(50,82),int(cost),"Recruiting",random.randint(1,6),random.randint(1,5))); st.rerun()
        if c[1].button("Upgrade Facilities"):
            cost=750000+user.facilities_level*300000
            if user.facilities_level<10 and user.budget>=cost:
                user.budget-=cost; user.facilities_level+=1; st.rerun()
        c[2].metric("Facilities",user.facilities_level)
    else: st.info("Take a job first.")

with tabs[9]:
    if user:
        st.header("Program History")
        if user.history: st.dataframe(user.history,use_container_width=True,hide_index=True)
        else: st.info("Your season history will appear here.")
    else: st.info("Take a job first.")
with tabs[2]:
    st.header("Season Hub")
    if user:
        stage=g.get("season_stage","preseason")
        c=st.columns(5)
        c[0].metric("Stage",stage.title()); c[1].metric("Record",f"{user.wins}-{user.losses}")
        c[2].metric("Contract",f"{g['contract'].remaining_years if g.get('contract') else 0} yrs")
        c[3].metric("Budget",f"${user.budget:,}"); c[4].metric("NIL",f"${user.nil_budget:,}")
        st.divider()
        if stage=="preseason":
            st.subheader("Preseason")
            st.write("Set your roster, staff, NIL strategy and schedule before opening night.")
            if not user.schedule:
                generate_schedule(user,g["teams"],g["year"])
            st.write(f"**{len(user.schedule)} games scheduled.**")
            if st.button("Begin Regular Season",type="primary"):
                g["season_stage"]="regular_season"; g["season_started"]=True; st.rerun()
        elif stage=="regular_season":
            played=sum(x.played for x in user.schedule); total=len(user.schedule)
            st.progress(played/max(1,total),text=f"Regular season: {played}/{total} games")
            st.info("Play games from the Game Day tab. The season automatically advances when all scheduled games are complete.")
            if played>=total and total:
                g["season_stage"]="postseason"; st.rerun()
        elif stage=="postseason":
            st.subheader("Postseason")
            st.write("Your conference tournament and NCAA tournament are ready.")
            if st.button("Run Postseason",type="primary"):
                finish_season(g); st.rerun()
        elif stage=="offseason":
            st.subheader("Offseason")
            if g.get("last_season"):
                st.write(g["last_season"])
            st.write("Graduation, player development, transfers, budgets and the coaching carousel are processed together.")
            if g.get("contract_expired"): st.warning("Your contract has expired. A new deal can be negotiated through the Career tab.")
            if g.get("season_awards"): st.write("Awards:",g["season_awards"])
            if st.button("Advance to Next Season",type="primary"):
                advance_offseason(g); st.rerun()
        if g.get("fired"):
            st.error("You were fired. Return to Career to select a new eligible job.")
            if st.button("Open Career Job Market"): g["fired"]=False; g["career_started"]=True; g["job_market"]=generate_job_market(g["teams"],g["career_profile"]); st.rerun()
    else:
        st.info("Start Career and accept a job to enter the dynasty loop.")


