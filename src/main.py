"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from recommender import load_songs, recommend_songs

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONGS_CSV = os.path.join(PROJECT_ROOT, "data", "songs.csv")


USER_PROFILES = {
    # Distinct, internally-consistent tastes
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},

    # Adversarial / edge-case profiles
    # Contradicts itself: high energy target but a "sad" mood no song has.
    "Conflicting Energy/Mood": {"genre": "pop", "mood": "sad", "energy": 0.9},
    # Genre that doesn't exist in the catalog at all.
    "Nonexistent Genre": {"genre": "death metal", "mood": "happy", "energy": 0.5},
    # Wants max energy AND acoustic songs, which are typically opposites.
    "Acoustic Headbanger": {"genre": "rock", "mood": "intense", "energy": 1.0, "likes_acoustic": True},
    # Empty preferences - every song should score 0 with no matches.
    "Empty Preferences": {},
    # Energy value outside the normal 0-1 range.
    "Out-of-Range Energy": {"genre": "pop", "mood": "happy", "energy": 5.0},
}


def main() -> None:
    songs = load_songs(SONGS_CSV)
    print(f"Loaded songs: {len(songs)}")

    for profile_name, user_prefs in USER_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\nTop Recommendations for '{profile_name}' {user_prefs}")
        print("=" * 50)
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} - {song['artist']} (Score: {score:.2f})")
            for reason in explanation.split(", "):
                print(f"     - {reason}")
            print()


if __name__ == "__main__":
    main()
