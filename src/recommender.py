import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song against user preferences using an additive point system, returning (score, reasons)."""
    score = 0.0
    reasons = []

    favorite_genre = user_prefs.get("genre")
    if favorite_genre is not None and song.get("genre") == favorite_genre:
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    favorite_mood = user_prefs.get("mood")
    if favorite_mood is not None and song.get("mood") == favorite_mood:
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        energy_points = 1.5 * (1 - abs(song.get("energy", 0.0) - target_energy))
        score += energy_points
        reasons.append(f"energy similarity (+{energy_points:.2f})")

    if user_prefs.get("likes_acoustic") and song.get("acousticness", 0.0) > 0.6:
        score += 0.5
        reasons.append(f"acoustic match (+0.5)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song with score_song and returns the top k, sorted by score descending."""
    def to_result(song):
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no matching preferences"
        return song, score, explanation

    scored = [to_result(song) for song in songs]
    ranked = sorted(scored, key=lambda result: result[1], reverse=True)
    return ranked[:k]
