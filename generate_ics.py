import pandas as pd
from datetime import datetime, timedelta

def create_ics_event(summary, start_time, duration, location, description):
    dtstamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    dtstart = start_time.strftime("%Y%m%dT%H%M%S")
    dtend = (start_time + duration).strftime("%Y%m%dT%H%M%S")
    uid = f"{dtstart}-{summary.replace(' ', '')}@modshockey"
    return f"""BEGIN:VEVENT
UID:{uid}
DTSTAMP:{dtstamp}
DTSTART;TZID=Australia/Perth:{dtstart}
DTEND;TZID=Australia/Perth:{dtend}
SUMMARY:{summary}
LOCATION:{location}
DESCRIPTION:{description}
END:VEVENT
"""

df = pd.read_csv("fixtures.csv")
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format="%Y-%m-%d %H:%M")
filtered_df = df[
    df['Division'].str.contains("Division 8 \(Black\) Men", case=False) &
    (df['Home Team'].str.contains("Mods-OGM", case=False) | df['Away Team'].str.contains("Mods-OGM", case=False)) &
    (df['Datetime'] > datetime.now())
]

ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\n"

for _, row in filtered_df.iterrows():
    summary = f"{row['Home Team']} vs {row['Away Team']}"
    start_time = row['Datetime']
    duration = timedelta(minutes=90)
    location = f"{row['Venue']} - {row['Sub-venue']}"
    description = f"Round {row['Round Number']} - {row['Division']}"
    ics_content += create_ics_event(summary, start_time, duration, location, description)

ics_content += "END:VCALENDAR"

with open("MODS_OGM_Fixtures.ics", "w", encoding="utf-8") as f:
    f.write(ics_content)
