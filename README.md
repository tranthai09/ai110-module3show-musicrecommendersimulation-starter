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

We need both a scoring rule and a ranking rule to build a recommendation system because scoring has to happen first. We cannot rank songs without measuring the scores. Then they have to be tested separately and then we can add ranking rules and ranking turns the comparisons into an actual ordered reccommendation list. 
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



