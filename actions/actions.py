
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# actions.py

import random
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, List, Text

class ActionRecommendMusic(Action):
    """Recommends music based on user preferences."""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_recommend_music"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:

        # Mapping of genres to lists of artists
        genre_artists = {
            "funk": ["James Brown", "Parliament-Funkadelic", "Chic"],
            "rock": ["The Rolling Stones", "Led Zeppelin", "Nirvana"],
            "pop": ["Michael Jackson", "Madonna", "Taylor Swift"]
        }

        # Extract the specified genre from the user's message
        genre = tracker.get_slot("genre")

        if genre:
            if genre in genre_artists:
                # Randomly select an artist from the specified genre
                selected_artist = random.choice(genre_artists[genre])
                dispatcher.utter_message(f"Sure! I'll play some {genre} by {selected_artist}.")
            else:
                dispatcher.utter_message("I'm not familiar with that genre. Can you specify another one?")
        else:
            dispatcher.utter_message("I'm not sure what you're looking for. Can you specify a genre or artist?")

        return []










