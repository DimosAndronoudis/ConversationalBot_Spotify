#
# # See this guide on how to implement these action:
# # https://rasa.com/docs/rasa/custom-actions
#
#
# # actions.py
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import SlotSet, FollowupAction
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
#
#
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="0f23ff75d88046b5b46b650eab91e08c",
#                                                client_secret="fddebf9a075247cc850fbe08c0c9d56a",
#                                                redirect_uri="http://localhost:1234/callback",
#                                                scope="playlist-modify-public playlist-modify-private"))
#
# NOTE_MAP = {
#     "C": 0,
#     "C#": 1,
#     "D": 2,
#     "D#": 3,
#     "E": 4,
#     "F": 5,
#     "F#": 6,
#     "G": 7,
#     "G#": 8,
#     "A": 9,
#     "A#": 10,
#     "B": 11
# }
#
# class ActionCreateSpotifyPlaylist(Action):
#
#     def name(self) -> str:
#         return "action_create_spotify_playlist"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: dict) -> list:
#
#         playlist_link = tracker.get_slot("playlist_link")
#         note_name = tracker.get_slot("note_name")
#         tempo = tracker.get_slot("tempo")
#         time_signature = tracker.get_slot("time_signature")
#
#         # Convert note name to key index
#         key = NOTE_MAP.get(note_name.upper())
#         if key is None:
#             dispatcher.utter_message(text=f"Invalid note name: {note_name}. Please use a valid note name.")
#             return []
#
#         # Function calls to extract and filter tracks
#         track_uris = self.get_track_uris(playlist_link)
#         features = self.get_audio_features(track_uris)
#         filtered_tracks = self.filter_tracks(features, key=key, tempo=int(tempo), time_signature=int(time_signature))
#
#         if not filtered_tracks:
#             dispatcher.utter_message(text="No tracks matched the criteria.")
#             return []
#
#         # Extract URIs from filtered tracks
#         filtered_uris = [track['uri'] for track in filtered_tracks]
#
#         # Create a new playlist with the specified name format
#         playlist_name = f"{note_name.upper()}, {tempo}BPM"
#         new_playlist_link = self.create_playlist(playlist_name, filtered_uris)
#
#         dispatcher.utter_message(text=f"New playlist created: {new_playlist_link}")
#         dispatcher.utter_message(text="Okay! Your new playlist is ready. You can check it out in your account on Spotify! Do you want another one?")
#
#         return [FollowupAction(name="action_check_user_response")]
#
#     def get_track_uris(self, playlist_link):
#         playlist_URI = playlist_link.split("/")[-1].split("?")[0]
#         results = sp.playlist_tracks(playlist_URI)
#         track_uris = [track["track"]["uri"] for track in results["items"]]
#         return track_uris
#
#     def get_audio_features(self, track_uris):
#         features = sp.audio_features(track_uris)
#         return features
#
#     def round_tempo(self, tempo):
#         return round(tempo)
#
#     def filter_tracks(self, features, key=None, tempo=None, time_signature=None):
#         filtered_tracks = []
#         for feature in features:
#             if feature is not None:
#                 match_key = key is None or feature['key'] == key
#                 if tempo is not None:
#                     feature_tempo = self.round_tempo(feature['tempo'])
#                     match_tempo = abs(feature_tempo - tempo) < 5
#                 else:
#                     match_tempo = True
#                 match_time_signature = time_signature is None or feature['time_signature'] == time_signature
#
#                 if match_key and match_tempo and match_time_signature:
#                     filtered_tracks.append(feature)
#         return filtered_tracks
#
#     def create_playlist(self, name, track_uris):
#         user_id = sp.current_user()["id"]
#         new_playlist = sp.user_playlist_create(user_id, name)
#         sp.playlist_add_items(new_playlist['id'], track_uris)
#         return new_playlist['external_urls']['spotify']
#
#
# class ActionCheckUserResponse(Action):
#
#     def name(self) -> str:
#         return "action_check_user_response"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: dict) -> list:
#
#         user_response = tracker.latest_message.get('text').lower()
#
#         if "yes" in user_response:
#             dispatcher.utter_message(text="Great! Let's create another playlist. Please provide the details.")
#             return [FollowupAction(name="action_create_spotify_playlist")]
#         elif "no" in user_response:
#             dispatcher.utter_message(text="Ok, have fun listening!")
#             return []
#         else:
#             dispatcher.utter_message(text="I didn't understand. Do you want another playlist?")
#             return []
#
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API authorization
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="0f23ff75d88046b5b46b650eab91e08c",
                                               client_secret="fddebf9a075247cc850fbe08c0c9d56a",
                                               redirect_uri="http://localhost:1234/callback",
                                               scope="playlist-modify-public playlist-modify-private"))

# Map note names to key indices
NOTE_MAP = {
    "C": 0,
    "C#": 1,
    "D": 2,
    "D#": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "G": 7,
    "G#": 8,
    "A": 9,
    "A#": 10,
    "B": 11
}

class ActionCreateSpotifyPlaylist(Action):

    def name(self) -> str:
        return "action_create_spotify_playlist"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        # Extract slots
        playlist_link = tracker.get_slot("playlist_link")
        note_name = tracker.get_slot("note_name")
        tempo = tracker.get_slot("tempo")
        time_signature = tracker.get_slot("time_signature")

        # Convert note name to key index
        key = NOTE_MAP.get(note_name.upper())
        if key is None:
            dispatcher.utter_message(text=f"Invalid note name: {note_name}. Please use a valid note name.")
            return []

        # Extract and filter tracks
        track_uris = self.get_track_uris(playlist_link)
        features = self.get_audio_features(track_uris)
        filtered_tracks = self.filter_tracks(features, key=key, tempo=int(tempo), time_signature=int(time_signature))

        if not filtered_tracks:
            dispatcher.utter_message(text="No tracks matched the criteria.")
            return []

        # Extract URIs from filtered tracks
        filtered_uris = [track['uri'] for track in filtered_tracks]

        # Create a new playlist with the specified name format
        playlist_name = f"{note_name.upper()}, {tempo}BPM"
        new_playlist_link = self.create_playlist(playlist_name, filtered_uris)

        # Inform the user that the playlist is created and conclude the conversation
        dispatcher.utter_message(text=f"New playlist created: {new_playlist_link}")
        dispatcher.utter_message(text="Okay! Have fun listening!")

        return []

    def get_track_uris(self, playlist_link):
        playlist_URI = playlist_link.split("/")[-1].split("?")[0]
        results = sp.playlist_tracks(playlist_URI)
        track_uris = [track["track"]["uri"] for track in results["items"]]
        return track_uris

    def get_audio_features(self, track_uris):
        features = sp.audio_features(track_uris)
        return features

    def round_tempo(self, tempo):
        return round(tempo)

    def filter_tracks(self, features, key=None, tempo=None, time_signature=None):
        filtered_tracks = []
        for feature in features:
            if feature is not None:
                match_key = key is None or feature['key'] == key
                if tempo is not None:
                    feature_tempo = self.round_tempo(feature['tempo'])
                    match_tempo = abs(feature_tempo - tempo) < 5
                else:
                    match_tempo = True
                match_time_signature = time_signature is None or feature['time_signature'] == time_signature

                if match_key and match_tempo and match_time_signature:
                    filtered_tracks.append(feature)
        return filtered_tracks

    def create_playlist(self, name, track_uris):
        user_id = sp.current_user()["id"]
        new_playlist = sp.user_playlist_create(user_id, name)
        sp.playlist_add_items(new_playlist['id'], track_uris)
        return new_playlist['external_urls']['spotify']

