
# College Basketball Coach Simulator — v3 Deep Dynasty

This is the deeper Streamlit starter engine.

## Included

### Program universe
- Real college programs from a representative Division I catalog
- ESPN team IDs and logo URL references
- Historical prestige
- Current prestige
- Adjusted program prestige
- Facilities
- Academics
- Budget
- NIL budget
- Conference identity

### Coaching
- Head-coach prestige
- Offensive/defensive coaching
- Recruiting
- Player development
- Adaptability
- Motivation
- Discipline
- NIL ability
- Loyalty
- Career wins/losses/titles/years
- Job security
- Coaching carousel
- Staff: OC, DC, recruiting, development, scouting

### Basketball engine
- Team offensive/defensive ratings
- Player-level attributes
- Shot profile
- Pace/tempo
- Aggression
- Balanced / 3PT / Paint / Transition offense
- Man / Zone / Press defense
- Home/away/neutral effects
- Fatigue
- Fouls
- Minutes
- Player roles
- Morale
- Player development
- Matchup effects

### Dynasty systems
- Schedule generation
- Conference standings
- Conference tournaments
- Selection model
- 76-team postseason framework
- National rankings
- Resume/SOS/NET-like metric
- Program history
- Coach history
- Facilities upgrades
- Staff
- NIL
- Recruiting
- Transfer portal
- Player progression
- Coach firings/hiring
- JSON saves

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notes

The app uses real school names and ESPN team IDs/logo URL references. Generated player/coach ratings are fictional.

The 2027 NCAA men's tournament is scheduled to be the first 76-team tournament; this build therefore supports a 76-team postseason model by default. The game's selection logic is a simulation, not an implementation of the NCAA committee's exact internal process.

The game's "NET-like" rating is intentionally an approximation inspired by public NCAA descriptions of NET inputs. It is not the official NCAA NET.

## Next engineering targets

For a production-grade version:
1. Expand the catalog to all Division I schools.
2. Add exact current conference alignment as a versioned data file.
3. Add real current rosters from an appropriately licensed/allowed data source.
4. Build a true possession-by-possession engine.
5. Add substitution AI, foul trouble, timeouts, two-for-one logic and late-game clock management.
6. Add scholarship limits, redshirts, eligibility, transfers and recruiting classes.
7. Add complete conference tournament formats.
8. Add NIT and other postseason events.
9. Add a proper 76-team opening-round/bracket placement algorithm.
10. Add player awards, all-conference teams, national awards and NBA draft/agent system.
11. Add conference realignment and media-rights economics.
12. Add coaching contracts, buyouts, extensions and staff poaching.
