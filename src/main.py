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


def main() -> None:
    songs = load_songs(SONGS_CSV)
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop Recommendations")
    print("=" * 50)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} - {song['artist']} (Score: {score:.2f})")
        for reason in explanation.split(", "):
            print(f"     - {reason}")
        print()


if __name__ == "__main__":
    main()
