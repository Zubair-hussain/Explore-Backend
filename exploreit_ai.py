# exploreit_ai.py - WEEKLY FRESH EVENTS + ZERO USER DATA ON SERVER
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExploreItAI:
    def __init__(self):
        self.cities = ["Karachi", "Lahore", "Islamabad", "Faisalabad", "Rawalpindi", "Multan", "Peshawar", "Quetta", "Hyderabad", "Sialkot"]
        self.events_data = self.generate_weekly_events()
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=600)
        texts = (self.events_data['title'] + " " + self.events_data['category'] + " " + self.events_data['city'] + " " + self.events_data['description'])
        self.event_vectors = self.vectorizer.fit_transform(texts.tolist())
        logger.info(f"Generated {len(self.events_data)} FRESH events for week {datetime.now().isocalendar()[1]}")

    def generate_weekly_events(self):
        # Events refresh every week automatically
        week_num = datetime.now().isocalendar()[1]
        np.random.seed(week_num)  # Same all week, new next Monday!

        categories = ["Art & Culture", "Music", "Food", "Comedy", "Workshop", "Sports", "Tech", "Festival", "Exhibition", "Kids", "Business", "Wellness"]
        base_titles = [
            "Art n Craft Show", "Live Music Night", "Food Festival", "Standup Comedy", "Photography Workshop",
            "Cultural Mela", "Book Fair", "Jazz Evening", "Startup Weekend", "Yoga Retreat", "Street Food Mela"
        ]

        events = []
        base_date = datetime(2025, 11, 19)

        for i in range(450):
            city = np.random.choice(self.cities, p=[0.28, 0.22, 0.16, 0.08, 0.06, 0.05, 0.04, 0.04, 0.04, 0.03])
            days = np.random.randint(0, 100)
            event_date = base_date + timedelta(days=days)
            hour = np.random.randint(9, 22)

            events.append({
                "event_id": f"evt_w{week_num}_{i}",
                "title": f"{np.random.choice(base_titles)} {city}",
                "category": np.random.choice(categories),
                "date": event_date.strftime("%a, %d %b, %Y - %I:%M %p"),
                "start_datetime": event_date.replace(hour=hour).isoformat() + "+05:00",
                "end_datetime": None,
                "venue": f"{city} Expo Center" if i % 4 == 0 else f"{city} Cultural Complex",
                "venue_address": f"{city}, Pakistan",
                "city": city,
                "description": f"Amazing {np.random.choice(categories).lower()} event happening in {city}! Join thousands of people.",
                "url": f"https://exploreit.pk/event/w{week_num}_{i}",
                "image_source": f"https://picsum.photos/id/{(i + week_num * 10) % 1000}/800/600",
                "status": "Upcoming"
            })

        return pd.DataFrame(events)

    def search(self, query: str):
        if not query.strip(): return []
        query_vec = self.vectorizer.transform([query.lower()])
        scores = cosine_similarity(query_vec, self.event_vectors)[0]
        results = []
        for idx, score in enumerate(scores):
            if score > 0.1:
                event = self.events_data.iloc[idx].to_dict()
                event["relevance_score"] = round(float(score), 3)
                results.append(event)
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:20]

    def get_all_events(self):
        return self.events_data.sample(frac=1).head(120).to_dict('records')  # Shuffled fresh feed