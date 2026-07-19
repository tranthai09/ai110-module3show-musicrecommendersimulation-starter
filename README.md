# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...

Loaded songs: 10

Top Recommendations
==================================================
1. Sunrise City - Neon Echo (Score: 4.47)
     - genre match (+2.0)
     - mood match (+1.0)
     - energy similarity (+1.47)

2. Gym Hero - Max Pulse (Score: 3.30)
     - genre match (+2.0)
     - energy similarity (+1.30)

3. Rooftop Lights - Indigo Parade (Score: 2.44)
     - mood match (+1.0)
     - energy similarity (+1.44)

4. Night Drive Loop - Neon Echo (Score: 1.42)
     - energy similarity (+1.42)

5. Storm Runner - Voltline (Score: 1.33)
     - energy similarity (+1.33)
     
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



