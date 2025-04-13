import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="0f23ff75d88046b5b46b650eab91e08c",
                                               client_secret="fddebf9a075247cc850fbe08c0c9d56a",
                                               redirect_uri="http://localhost:1234/callback",
                                               scope="playlist-modify-public playlist-modify-private"))

# Mapping of note names to key indices
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

def get_track_uris(playlist_link):
    """Extract track URIs from the given playlist link."""
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    results = sp.playlist_tracks(playlist_URI)
    track_uris = [track["track"]["uri"] for track in results["items"]]
    return track_uris

def get_audio_features(track_uris):
    """Retrieve audio features for a list of track URIs."""
    features = sp.audio_features(track_uris)
    return features

def round_tempo(tempo):
    """Round the tempo to the nearest integer."""
    return round(tempo)

def filter_tracks(features, key=None, tempo=None, time_signature=None):
    """Filter tracks based on key, tempo, and time signature."""
    filtered_tracks = []
    for feature in features:
        if feature is not None:  # Handle tracks with no features
            match_key = key is None or feature['key'] == key
            if tempo is not None:
                feature_tempo = round_tempo(feature['tempo'])
                match_tempo = abs(feature_tempo - tempo) < 5  # Allow some variance
            else:
                match_tempo = True
            match_time_signature = time_signature is None or feature['time_signature'] == time_signature

            if match_key and match_tempo and match_time_signature:
                filtered_tracks.append(feature)
    return filtered_tracks

def create_playlist(name, track_uris):
    """Create a new Spotify playlist with the given track URIs."""
    user_id = sp.current_user()["id"]
    new_playlist = sp.user_playlist_create(user_id, name)
    sp.playlist_add_items(new_playlist['id'], track_uris)
    return new_playlist['external_urls']['spotify']

def create_custom_playlist(playlist_link, note_name, tempo, time_signature):
    """Create a custom playlist based on specified audio features."""
    # Convert note name to key index
    key = NOTE_MAP.get(note_name.upper())
    if key is None:
        return f"Invalid note name: {note_name}. Please use a valid note name."

    track_uris = get_track_uris(playlist_link)
    features = get_audio_features(track_uris)
    filtered_tracks = filter_tracks(features, key=key, tempo=tempo, time_signature=time_signature)

    if not filtered_tracks:
        return "No tracks matched the criteria."

    # Extract URIs from filtered tracks
    filtered_uris = [track['uri'] for track in filtered_tracks]

    # Create a new playlist with the specified name format
    playlist_name = f"{note_name.upper()}, {tempo}BPM"
    new_playlist_link = create_playlist(playlist_name, filtered_uris)

    # Print the audio features of each song in the new playlist
    print("Audio Features of Tracks in the New Playlist:")
    for track in filtered_tracks:
        print(f"Track URI: {track['uri']}, Key: {track['key']}, Tempo: {track['tempo']}, Time Signature: {track['time_signature']}")

    return f"New playlist created: {new_playlist_link}"

# Example usage
playlist_link = "https://open.spotify.com/playlist/0HcxSs1gpnIqDghws7t24w?si=1120888305324bdb"
note_name = "F#"  # Note name (e.g., "C", "D#", "A", etc.)
tempo = 144  # Desired tempo
time_signature = 4  # Desired time signature

new_playlist = create_custom_playlist(playlist_link, note_name, tempo, time_signature)
print(new_playlist)
