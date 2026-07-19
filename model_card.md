# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**VibeMatch 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

VibeMatch picks 5 songs from a small catalog that best match a person's stated taste. You tell it a favorite genre, a favorite mood, a target energy level, and whether you like acoustic songs. It scores every song and hands back the top 5, with a short list of reasons for each pick.

It assumes you already know your own taste and can describe it with those four simple labels. It does not learn from your listening history or ask follow-up questions. This is a classroom project, not a real product. It is meant to show how a simple recommender works, not to power an actual app.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Every song has a genre, a mood, an energy level, and a few other traits like how "acoustic" it sounds. Every user has a favorite genre, a favorite mood, a target energy level, and whether they like acoustic songs.

To score a song, the system hands out points one at a time. If the song's genre matches your favorite genre, it gets points. If the mood matches, it gets more points. If the song's energy is close to the energy you asked for, it gets a few points too, and the closer the match, the more points it earns. If you said you like acoustic songs and the song is acoustic enough, it gets a small bonus. All these points just add up, never subtract, so the total score is easy to explain: "this song scored high because it matched your genre, your mood, and had close-to-right energy."

Once every song has a score, the system just sorts them from highest to lowest and hands back the top few. I also tried doubling the energy points and cutting the genre points in half, just to see what would change. Surprisingly, the same top songs still won most of the time, which taught me the ranking has more to do with which single song happens to match multiple things at once than with the exact point values chosen.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog only has 10 songs. That's tiny — small enough that testing by hand and reading every row is easy, but too small to really show off a recommender.

The genres are: pop, lofi, rock, ambient, jazz, synthwave, indie pop, and lofi again (two lofi songs). The moods are: happy, chill, intense, relaxed, moody, and focused. Most genres and moods only show up once or twice, so there is barely any overlap between songs.

I didn't add or remove any rows, I used the starter data as-is. Because the catalog is so small, whole chunks of musical taste are just missing. There's no metal, no classical, no hip-hop, and no truly sad or angry mood. If a user's taste doesn't match one of the exact labels already in the file, the system has nothing good to give them.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works best for users whose taste lines up cleanly with the exact labels in the dataset. The Chill Lofi profile is a good example: it wants lofi, chill, low energy, and acoustic songs, and the top 5 results were genuinely the calmest, most acoustic songs in the whole catalog. That matched my intuition perfectly.

It's also good at showing its work. Every recommendation comes with a plain list of reasons, like "genre match" or "energy similarity," so you can see exactly why a song was picked instead of just trusting a black box.

It also handles missing or bad matches without crashing. If a user asks for a genre or mood that isn't in the catalog, the system doesn't error out, it just quietly ranks on whatever signals are left. That's a reasonable fallback even if it's not perfect.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

During experiments, "Sunrise City" ranked first for nearly every high-energy, positive-mood profile because it is the only song in the 10-track catalog whose `genre` field is exactly `"pop"` and whose `mood` field is exactly `"happy"` at the same time. This happens because genre and mood are scored with strict string equality rather than any notion of similarity, so a song like "Rooftop Lights" (`genre="indie pop"`) gets zero genre credit against a `genre="pop"` preference even though the two labels are obviously related. The system therefore over-favors whichever single song happens to sit at the exact intersection of a user's stated genre and mood, rather than genuinely ranking the closest overall matches. Even after doubling the energy weight and halving the genre weight, this same song still won every affected profile, which suggests the bias comes from the sparse, exact-match dataset rather than from the specific weight values chosen. Users whose taste spans adjacent-but-not-identical labels (e.g., both "chill" and "relaxed" moods) are systematically underserved, since the scoring model can only reward exact label matches.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

### Profiles Tested

Three "normal" taste profiles and five "adversarial" edge-case profiles were run through `recommend_songs` and the top 5 results were inspected for each:

- **High-Energy Pop** (`genre=pop, mood=happy, energy=0.9`)
- **Chill Lofi** (`genre=lofi, mood=chill, energy=0.35, likes_acoustic=True`)
- **Deep Intense Rock** (`genre=rock, mood=intense, energy=0.9`)
- **Conflicting Energy/Mood** (`genre=pop, mood=sad, energy=0.9`) — no song in the catalog has `mood="sad"`
- **Nonexistent Genre** (`genre=death metal, mood=happy, energy=0.5`) — no song has that genre
- **Acoustic Headbanger** (`genre=rock, mood=intense, energy=1.0, likes_acoustic=True`) — contradictory combo
- **Empty Preferences** (`{}`) — no signal at all
- **Out-of-Range Energy** (`genre=pop, mood=happy, energy=5.0`) — invalid input outside 0–1

For each, I checked whether the #1 result made intuitive sense given the stated taste, and whether the reasons list actually explained the ranking.

### What Surprised Me

The biggest surprise was that the *same handful of songs* (especially "Sunrise City" and "Gym Hero") kept reappearing at or near the top across very different profiles, even ones that shouldn't obviously prefer them. Doubling the energy weight and halving the genre weight didn't reorder any top-5 list — it only changed the point margins — which told me the bias comes from the small, sparse dataset (only one song sits at the intersection of `pop` + `happy`) rather than from the specific weights I chose. I was also surprised that the energy formula has no input validation: an out-of-range `energy=5.0` silently produced negative total scores instead of erroring or clamping, which would confuse a real user with no warning that their input was invalid.

### Pairwise Comparisons

- **High-Energy Pop vs. Deep Intense Rock** — Both target the same energy (0.9), but swapping genre/mood from pop/happy to rock/intense completely changes the winner, from "Sunrise City" to "Storm Runner." This makes sense: energy is identical, so genre and mood become the only tie-breakers, and each profile pulls toward the one song that actually matches its genre+mood combo.

- **High-Energy Pop vs. Chill Lofi** — These sit at opposite ends of the energy spectrum (0.9 vs. 0.35) and pick entirely different genres. The results flip completely, with fast pop/EDM-style tracks on top for the high-energy profile and slow lofi tracks with high acousticness on top for the chill profile. This is the clearest "sanity check" pass: the energy term is doing its job of separating high-tempo, high-energy taste from low-energy, mellow taste.

- **High-Energy Pop vs. Conflicting Energy/Mood** — This pair is the direct answer to "why does Gym Hero keep showing up for people who just want Happy Pop?" Both profiles want `genre=pop` at `energy=0.9`, but the second profile asks for `mood=sad`, a mood no song has. Because no song can ever earn the mood point in that case, "Sunrise City" loses the +1.0 mood bonus that let it beat "Gym Hero" in the Happy Pop profile. Once mood stops being a deciding factor, the two pop songs are ranked purely on how close their energy is to 0.9 — and "Gym Hero" (energy 0.93) is a hair closer to 0.9 than "Sunrise City" (energy 0.82), so it edges ahead. In plain terms: Gym Hero is a slightly more "intense" pop song, so any time a listener's stated mood can't actually be matched by anything in the catalog, the system quietly falls back to "closest energy," and that tiny energy difference is enough to make Gym Hero win instead of the song that actually "feels happy."

- **Nonexistent Genre vs. High-Energy Pop** — Asking for a genre that doesn't exist in the catalog (`death metal`) doesn't crash or return nothing; it just silently drops the genre signal and ranks on mood + energy alone, surfacing "Rooftop Lights" and "Sunrise City" (both `mood="happy"`) instead of anything genre-appropriate. This is reasonable fallback behavior, but it never tells the user their genre request couldn't be honored — the explanation just omits a genre-match line rather than flagging the miss.

- **Acoustic Headbanger vs. Chill Lofi** — Both ask for `likes_acoustic=True`, but Acoustic Headbanger also demands `energy=1.0`, which is a contradiction (loud, high-energy rock songs are almost never highly acoustic in this dataset). The result confirms the contradiction: no acoustic bonus shows up until the #5 slot, because the top rock/intense matches simply aren't acoustic, and the formula doesn't reward "close enough" trade-offs — the acoustic songs that could have partially satisfied this listener get crowded out entirely by the energy and mood terms.

- **Empty Preferences vs. everything else** — With no preferences at all, every song ties at a score of 0.0, and the "winner" is just whichever song happens to appear first in `songs.csv`. This is expected given a purely additive scoring system, but it's a real limitation: a brand-new user with no stated taste gets an arbitrary, insertion-order recommendation rather than something like a popularity-based or diverse default list.

- **Out-of-Range Energy vs. High-Energy Pop** — Same genre/mood target as High-Energy Pop, but with an invalid `energy=5.0`. Instead of erroring, every song's energy term goes deeply negative, and the ranking is decided almost entirely by whichever song has the *highest* real energy (since that minimizes the now-huge gap to 5.0) plus whatever genre/mood points it can still earn. The ordering ends up similar to the valid High-Energy Pop case, but every score is negative, which would look broken or alarming to a real user even though the relative ranking is arguably still "reasonable."

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

I'd add "fuzzy" genre and mood matching, so "pop" and "indie pop" count as related instead of totally different, and "chill" and "relaxed" get partial credit for being similar moods. I'd also let users set an energy range instead of one exact number, so someone who just wants "high energy" doesn't get penalized for not hitting one precise target.

I'd improve the explanations by also telling users when something they asked for wasn't available, like "no songs matched your genre, so we ranked by mood and energy instead," instead of just silently dropping that signal.

I'd add a diversity rule so the top 5 aren't all from the same genre or artist, even when one genre scores highest. And I'd add a bigger, more varied dataset so users with less common tastes (metal, hip-hop, sad songs) actually have something good to get recommended.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I learned that a recommender doesn't need to be complicated to show real bias. This one is just a handful of "if it matches, add points" rules, and it still ended up favoring one song over and over just because that song happened to sit at the exact overlap of two labels.

The most interesting thing I found was that changing the weights barely changed anything. I expected doubling the energy weight to shake up the rankings a lot, but the same songs kept winning. That taught me the dataset itself, not just the math, decides a lot of what a recommender can and can't do.

This changed how I think about real recommendation apps. If a small demo dataset can create an obvious favorite, a real streaming app's much bigger, messier dataset could easily be doing the same thing to real users, just harder to notice. Now I'd want to know not just "what are the weights" but "what does the data actually look like" before trusting any recommender's fairness.
