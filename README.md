# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version loads an 18-song catalog from a CSV, scores every song against a user's stated taste profile using an additive point system, and returns the top-k matches with plain-language reasons for each pick. It also documents what happens when that scoring logic gets pushed with contradictory, missing, or invalid preferences.

---

## How Real-World Recommenders Compare

Real systems like Spotify or YouTube work on the same basic idea as this project, just with much richer data. They use **input data** — a song or video's own features (genre, tempo, audio fingerprint, topic tags) plus signals about how other users reacted to it (skip rate, watch time, likes). They combine that with **user preferences** — but instead of a user typing in "genre=pop, mood=happy" like this project does, real systems *infer* preferences from listening/watch history, search queries, and even the time of day. Finally there's **ranking/selection** — a model scores thousands or millions of candidates and returns a short ranked list, exactly like `recommend_songs` does here, just with a machine-learned scoring function instead of hand-written point rules.

The key difference from this simulation: here, "user preferences" are explicit and typed in by hand, and "input data" is a small, clean CSV. In real systems, both are inferred from noisy behavioral signals at massive scale, which is also where a lot of the bias in real recommenders creeps in — e.g., a song that already has more plays looks more "relevant" to the ranking model, which can snowball into popularity bias, similar to how "Sunrise City" snowballs to the top of every happy/high-energy query in this project just because it's the only song sitting at that exact label intersection.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

The features each song has are the  identifiers (ID, title, artist), genre, mood, energy, tempo, valence, daceability, and acousticness.

UserProfile stores the user's favorite genre, favorite modod, target energy, and whether they like acoustic songs or not (or if they prefer electronic songs).

The Recommender needs to filter the songs and return a list of songs what score based on how close it is to the UserProfile or the user's preferences. For example, if the user's favorite genre matches with the current genre of the song, then we can return a 1 for the genre_score since it is matching with the user's favorite genre or else we would return false. This would also be done for the mood_score, energy_score, and acoustic_score. Then we would calculate the toal score by calculating a weighted average where each score is multiplied by the weight of how much each feature would matter (genre = 3, mood = 2, energy = 2, acoustic = 1 where genre is the heaviest and impactful weight). The weights are summed and divided by the sum of the weights (3 + 2 + 2 + 1 = 8). We would return the songs score by returning the toal for each song and the resons list of why each song is scored a certain way so that we can complete the explain_reccomendation function.

To reccommend songs, we would first score every song based on how well it matches the User preferences (UserProfile) based of genre, mood and the features. Then we would add them up and find the weighted total to calculate the match percentage. Once every song has a total score from score_song function, we would just sort it by highest score first where the higher the score, the better the match. Then we would take the top few (k number of reccommendation) from the sorted list and these are the reccommended songs.

### Algorithm Recipe (Finalized)

Instead of a weighted average, the finalized recipe is an additive point system: points are only ever added (never subtracted), so every song's score is a simple, explainable running total.

- **+2.0 points** if the song's genre matches the user's favorite genre.
- **+1.0 point** if the song's mood matches the user's favorite mood.
- **Up to +1.5 points** for energy similarity, scaled linearly: `1.5 * (1 - abs(song.energy - user.target_energy))`. A song with energy identical to the user's target earns the full 1.5; a song with maximally different energy (a difference of 1.0) earns 0.
- **+0.5 points** if the user likes acoustic songs and the song's acousticness is above 0.6.

This makes genre the dominant signal (2.0), energy the runner-up (up to 1.5), mood a moderate signal (1.0), and acoustic preference a minor tiebreaker (0.5). Each rule that fires also appends a plain-language reason (e.g., "Matches favorite genre (rock)") to a reasons list, which `explain_recommendation` uses to justify the pick.

To recommend songs, `score_song` is run once per song to get a `(score, reasons)` pair, `recommend_songs` sorts all songs by score descending, and the top `k` are returned.

We need both a scoring rule and a ranking rule to build a recommendation system because scoring has to happen first. We cannot rank songs without measuring the scores. Then they have to be tested separately and then we can add ranking rules, and ranking turns the comparisons into an actual ordered recommendation list.

### Potential Biases

This system likely over-prioritizes genre relative to mood, since a genre match alone (2.0) beats a mood match alone (1.0), even when the mood match is emotionally a much closer fit for the user. A song that misses genre entirely can also never out-rank a same-genre song unless it wins big on energy and mood combined, so users with eclectic or mood-first taste (rather than genre-loyal taste) may get systematically weaker recommendations from this weighting.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
Loaded songs: 18

Top Recommendations for 'High-Energy Pop' {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}
==================================================
1. Sunrise City - Neon Echo (Score: 4.38)
     - genre match (+2.0)
     - mood match (+1.0)
     - energy similarity (+1.38)

2. Gym Hero - Max Pulse (Score: 3.46)
     - genre match (+2.0)
     - energy similarity (+1.46)

3. Rooftop Lights - Indigo Parade (Score: 2.29)
     - mood match (+1.0)
     - energy similarity (+1.29)

4. Backroad Anthem - Cedar & Bloom (Score: 2.05)
     - mood match (+1.0)
     - energy similarity (+1.05)

5. Storm Runner - Voltline (Score: 1.48)
     - energy similarity (+1.48)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Eight user profiles were run against the 18-song catalog: three "normal" tastes (High-Energy Pop, Chill Lofi, Deep Intense Rock) and five adversarial/edge-case profiles designed to try to break the scoring logic (conflicting mood, a genre that doesn't exist, a contradictory energy+acoustic combo, empty preferences, and an out-of-range energy value). Full output for each:

```
Loaded songs: 18

Top Recommendations for 'High-Energy Pop' {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}
==================================================
1. Sunrise City - Neon Echo (Score: 4.38)
     - genre match (+2.0)
     - mood match (+1.0)
     - energy similarity (+1.38)

2. Gym Hero - Max Pulse (Score: 3.46)
     - genre match (+2.0)
     - energy similarity (+1.46)

3. Rooftop Lights - Indigo Parade (Score: 2.29)
     - mood match (+1.0)
     - energy similarity (+1.29)

4. Backroad Anthem - Cedar & Bloom (Score: 2.05)
     - mood match (+1.0)
     - energy similarity (+1.05)

5. Storm Runner - Voltline (Score: 1.48)
     - energy similarity (+1.48)


Top Recommendations for 'Chill Lofi' {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}
==================================================
1. Library Rain - Paper Lanterns (Score: 5.00)
     - genre match (+2.0)
     - mood match (+1.0)
     - energy similarity (+1.50)
     - acoustic match (+0.5)

2. Midnight Coding - LoRoom (Score: 4.89)
     - genre match (+2.0)
     - mood match (+1.0)
     - energy similarity (+1.40)
     - acoustic match (+0.5)

3. Focus Flow - LoRoom (Score: 3.92)
     - genre match (+2.0)
     - energy similarity (+1.42)
     - acoustic match (+0.5)

4. Spacewalk Thoughts - Orbit Bloom (Score: 2.90)
     - mood match (+1.0)
     - energy similarity (+1.40)
     - acoustic match (+0.5)

5. Coffee Shop Stories - Slow Stereo (Score: 1.97)
     - energy similarity (+1.47)
     - acoustic match (+0.5)


Top Recommendations for 'Deep Intense Rock' {'genre': 'rock', 'mood': 'intense', 'energy': 0.9}
==================================================
1. Storm Runner - Voltline (Score: 4.48)
     - genre match (+2.0)
     - mood match (+1.0)
     - energy similarity (+1.48)

2. Gym Hero - Max Pulse (Score: 2.46)
     - mood match (+1.0)
     - energy similarity (+1.46)

3. Iron Reckoning - Voltline (Score: 2.42)
     - mood match (+1.0)
     - energy similarity (+1.43)

4. Pulse Overdrive - Neon Echo (Score: 1.47)
     - energy similarity (+1.47)

5. Sunrise City - Neon Echo (Score: 1.38)
     - energy similarity (+1.38)


Top Recommendations for 'Conflicting Energy/Mood' {'genre': 'pop', 'mood': 'sad', 'energy': 0.9}
==================================================
1. Gym Hero - Max Pulse (Score: 3.46)
     - genre match (+2.0)
     - energy similarity (+1.46)

2. Sunrise City - Neon Echo (Score: 3.38)
     - genre match (+2.0)
     - energy similarity (+1.38)

3. Storm Runner - Voltline (Score: 1.48)
     - energy similarity (+1.48)

4. Pulse Overdrive - Neon Echo (Score: 1.47)
     - energy similarity (+1.47)

5. Iron Reckoning - Voltline (Score: 1.43)
     - energy similarity (+1.43)


Top Recommendations for 'Nonexistent Genre' {'genre': 'death metal', 'mood': 'happy', 'energy': 0.5}
==================================================
1. Backroad Anthem - Cedar & Bloom (Score: 2.35)
     - mood match (+1.0)
     - energy similarity (+1.35)

2. Rooftop Lights - Indigo Parade (Score: 2.11)
     - mood match (+1.0)
     - energy similarity (+1.11)

3. Sunrise City - Neon Echo (Score: 2.02)
     - mood match (+1.0)
     - energy similarity (+1.02)

4. Velvet Whisper - Honey Static (Score: 1.42)
     - energy similarity (+1.42)

5. Wildflower Road - Cedar & Bloom (Score: 1.42)
     - energy similarity (+1.42)


Top Recommendations for 'Acoustic Headbanger' {'genre': 'rock', 'mood': 'intense', 'energy': 1.0, 'likes_acoustic': True}
==================================================
1. Storm Runner - Voltline (Score: 4.37)
     - genre match (+2.0)
     - mood match (+1.0)
     - energy similarity (+1.36)

2. Iron Reckoning - Voltline (Score: 2.42)
     - mood match (+1.0)
     - energy similarity (+1.42)

3. Gym Hero - Max Pulse (Score: 2.40)
     - mood match (+1.0)
     - energy similarity (+1.40)

4. Pulse Overdrive - Neon Echo (Score: 1.32)
     - energy similarity (+1.32)

5. Sunrise City - Neon Echo (Score: 1.23)
     - energy similarity (+1.23)


Top Recommendations for 'Empty Preferences' {}
==================================================
1. Sunrise City - Neon Echo (Score: 0.00)
     - no matching preferences

2. Midnight Coding - LoRoom (Score: 0.00)
     - no matching preferences

3. Storm Runner - Voltline (Score: 0.00)
     - no matching preferences

4. Library Rain - Paper Lanterns (Score: 0.00)
     - no matching preferences

5. Gym Hero - Max Pulse (Score: 0.00)
     - no matching preferences


Top Recommendations for 'Out-of-Range Energy' {'genre': 'pop', 'mood': 'happy', 'energy': 5.0}
==================================================
1. Sunrise City - Neon Echo (Score: -1.77)
     - genre match (+2.0)
     - mood match (+1.0)
     - energy similarity (+-4.77)

2. Gym Hero - Max Pulse (Score: -2.61)
     - genre match (+2.0)
     - energy similarity (+-4.61)

3. Rooftop Lights - Indigo Parade (Score: -3.86)
     - mood match (+1.0)
     - energy similarity (+-4.86)

4. Backroad Anthem - Cedar & Bloom (Score: -4.10)
     - mood match (+1.0)
     - energy similarity (+-5.10)

5. Iron Reckoning - Voltline (Score: -4.57)
     - energy similarity (+-4.57)
```

I also tried doubling the energy weight and halving the genre weight (genre `+2.0 → +1.0`, energy `1.5× → 3.0×`) to see if it would change which songs won. Surprisingly, it didn't reorder any of the top-5 lists above — only the score margins shifted. That told me the "same song wins" pattern is driven by the sparse, exact-match dataset (one song owning a rare label combination) rather than by the specific weight values. See `model_card.md`'s Evaluation section for the full pairwise comparison writeup, including a plain-language explanation of why "Gym Hero" keeps beating "Sunrise City" once mood stops being able to differentiate them.

---

## Limitations and Risks

- **Exact-string genre/mood matching.** `"pop"` and `"indie pop"` are treated as completely unrelated, and moods like `"chill"` and `"relaxed"` get no partial credit for being similar. This means users with taste that spans adjacent labels get worse recommendations than users who happen to match a label exactly.
- **The energy gap has no bounds-checking.** An out-of-range `energy` value (e.g., 5.0) isn't rejected or clamped — it just makes every song's score go deeply negative, which would look broken to a real user.
- **No diversity mechanism.** `recommend_songs` is a pure top-k sort with no guard against the top 5 all coming from the same genre or artist.
- **Still a small catalog.** 18 songs is enough to show real patterns (and real bias), but it's nowhere near enough to represent real musical taste — several genres (hip-hop, classical, metal, folk, R&B, blues, country, EDM) only have one song each, so there's no genuine competition within those genres yet.
- **No understanding of lyrics, language, or audio itself** — everything is driven by hand-labeled metadata (genre, mood, energy, etc.), not the actual sound or content of a song.

Go deeper on this in `model_card.md`.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



