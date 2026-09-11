import sqlite3
from datetime import datetime,timedelta
correlation_window = timedelta(minutes=3)

def are_events_related(event_a, event_b):
    ip_a = event_a[2]
    ip_b = event_b[2]

    time_a = datetime.fromisoformat(event_a[4])
    time_b = datetime.fromisoformat(event_b[4])

    time_difference = abs(time_b - time_a)

    if ip_a == ip_b and time_difference <= correlation_window:
        return True
    return False

def create_activity_groups(events):
    activities = []
    for event in events:
        added_to_activity = False
        for activity in activities:
            last_event = activity[-1]
            if are_events_related(last_event, event):
                activity.append(event)
                added_to_activity = True
                break
        if not added_to_activity:
            activities.append([event])

    return activities

connection = sqlite3.connect('decoytrace.db')

events = connection.execute(
    "SELECT * FROM events ORDER BY timestamp ASC"
).fetchall()

connection.close()

activities = create_activity_groups(events)

for i, activity in enumerate(activities, start=1):
    print(f"\nActivity {i}:")

    for event in activity:
        print(f"    Event {event[0]}")