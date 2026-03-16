# PachaMix: A Narrative Teaching Script for Big Data

## Purpose of This Document

This document turns the course into a semester-long story led by two recurring characters:

- `Mathias`, the peccary
- `Yunguri`, the llama

The story is designed to make the course more memorable without sacrificing rigor. The jokes, callbacks, and character dynamics make the material more human, but every chapter remains tightly connected to the actual technical goals of the course:

- Big Data and advanced analytics
- supervised and unsupervised learning
- the curse of dimensionality
- dimensionality reduction with PCA, SVD, and t-SNE
- clustering with K-means and DBSCAN
- recommendation systems
- graph analytics and PageRank
- deployment, monitoring, and productization

This script is intentionally more extensive than a standard lecture outline because each teaching week has `4 hours of class time`:

- `2 theoretical hours`
- `2 practical/laboratory hours`

The result is not a literal theater script, but a `teaching screenplay`: story beats, dialogue, jokes, transitions, mathematical hooks, and lab framing.

---

## Main Premise

Mathias and Yunguri are friends who want to build `PachaMix`, a smart playlist and song recommendation assistant for university students.

Mathias wants PachaMix to create the perfect playlist for every situation:

- studying
- coding
- walking across campus in dramatic weather
- recovering from exams
- pretending to understand jazz

Yunguri, who is far more skeptical, agrees to help only if they build the system correctly:

- with clear questions
- with solid mathematics
- with reliable data
- with methods that scale
- with enough discipline that the system does not recommend "sad violin raincore" to someone searching for "songs for a birthday barbecue"

They will work with:

- `audio features`
- `lyrics-derived features`
- `playlist co-occurrence data`
- eventually, `song networks`

Their journey becomes the narrative backbone of the course.

---

## Character Profiles

## Mathias the Peccary

Mathias is enthusiastic, brave, impulsive, and completely convinced that every problem can be solved with either:

- more data
- one extra scatterplot
- or a heroic amount of confidence

He loves patterns, dashboards, shortcuts, and saying things like:

> "How hard can it be? It is just music with numbers."

He is wrong often enough to be useful.

He is the embodiment of the student's first instinct:

- curious
- practical
- slightly overconfident
- ready to run code before defining the problem

## Yunguri the Llama

Yunguri is precise, dry, funny, and deeply suspicious of bad assumptions.

She believes in:

- definitions before models
- models before hype
- and proofs before celebration

She says things like:

> "That is not a result. That is an emotionally optimistic spreadsheet."

and:

> "I only spit on two things: weak coffee and unjustified conclusions."

She is the embodiment of methodological rigor:

- careful
- structured
- mathematically grounded
- allergic to hand-waving

## Their Dynamic

Mathias generates momentum.

Yunguri generates validity.

Mathias says:

> "Let us deploy it tonight."

Yunguri replies:

> "We have not even defined the loss function."

That tension is the engine of the entire course.

---

## Recurring Running Jokes

These jokes can be reused throughout the semester so the story feels continuous rather than episodic.

- `The Spit Test`: Yunguri says a claim does or does not "pass the spit test," meaning it survives skeptical scrutiny.
- `Mathias versus Dimensionality`: every time the feature space becomes too large, Mathias says, "Excellent, more dimensions means more knowledge," and Yunguri looks into the camera of the collective classroom soul.
- `Suspiciously Specific Playlist Names`: Mathias keeps creating ridiculous target playlists like:
  - "Songs for finishing a report at 2:13 a.m."
  - "Music for pretending you understand eigenvectors"
  - "Acoustic optimism with statistically significant melancholy"
- `Llama Compliance`: Yunguri repeatedly reminds Mathias that "a recommendation engine is not a horoscope generator."
- `The Heroic Scatterplot`: Mathias keeps believing that one more plot will explain everything.

---

## Data Narrative for the Semester

Inside the story, PachaMix is built from publicly usable music-related data categories:

- `audio descriptors` for sound and mood
- `lyrics-derived textual features` for semantic content
- `playlist co-occurrence data` for behavioral structure
- `song networks` built from playlist relationships

This is important because the story must feel real:

- students can imagine the system
- the methods connect naturally
- the network chapter grows out of the recommendation chapter instead of appearing from nowhere

---

## Semester Arc at a Glance

### Arc 1. Framing the Problem

Weeks `1-2`

Mathias and Yunguri decide what they are actually trying to build and what kind of analytical problems they are facing.

### Arc 2. Fighting High Dimensionality

Weeks `3-5`

They discover that song, lyric, and playlist data live in large, noisy, high-dimensional spaces, and they need mathematical tools to survive.

### Arc 3. Discovering Structure

Weeks `6-7`

They use clustering to identify groups of songs, styles, or listening moods.

### Arc 4. Recommending Music

Weeks `8-10`

They move from describing songs to recommending them.

### Arc 5. Seeing Music as a Network

Weeks `11-12`

They discover that songs are not only vectors. They are also nodes in a graph created by shared playlist behavior.

### Arc 6. Making the System Real

Weeks `13-14`

They realize that a model is not a product until it can run, serve, and be monitored.

---

## Teaching Format for Every Week

Each weekly script follows the same rhythm:

1. `Cold open`
   A funny or memorable short exchange.
2. `Theory story`
   The narrative event that motivates the mathematical idea.
3. `Mathematical checkpoint`
   The exact concept that must be proved, derived, or justified.
4. `Lab mission`
   The practical activity as part of the story.
5. `Closing hook`
   The unresolved problem that leads into next week.

You can perform the dialogue directly, paraphrase it, or just use it as a teaching voice.

---

# Arc 1: Framing the Problem

## Week 1. Welcome to PachaMix: Big Data, Advanced Analytics, and Data Science

## Episode Goal

Introduce the characters, the product idea, and the distinction between Big Data, analytics, data science, and machine learning.

## Cold Open

> Mathias: "I have a genius idea. A playlist assistant for students."
>
> Yunguri: "That sentence has committed no crime yet. Continue."
>
> Mathias: "It will know whether a student needs music for studying, coding, heartbreak, gym, or public transport despair."
>
> Yunguri: "So your product strategy is emotional surveillance with a nice interface."
>
> Mathias: "Exactly."
>
> Yunguri: "No. But it is at least a project."

## Theory Story

Mathias arrives with a chaotic folder called `songs_final_FINAL_v8_really_final.csv`.

Yunguri opens it, sighs, and asks the class:

> "Before we build anything, what problem are we solving?"

This is the ideal moment to introduce:

- Big Data as a context of scale and complexity
- advanced analytics as the broader decision-making toolkit
- data science as the workflow that combines statistics, computation, and domain understanding
- machine learning as one family of methods within data science

Narrative framing:

Mathias thinks PachaMix is simply "an app that recommends songs."

Yunguri insists they must decompose the problem:

- What data do we have?
- What data do we wish we had?
- What question are we answering?
- What decision will the system support?
- What counts as success?

## Suggested Lecture Beats for the 2 Theory Hours

### Scene 1. Why This Is a Big Data Story

Mathias imagines collecting:

- song metadata
- audio descriptors
- lyric features
- playlist interactions
- user histories

Yunguri points out that the challenge is not only `how much` data there is, but also:

- how varied it is
- how quickly it changes
- how noisy it is
- and how expensive it can be to process

This opens the door to the `5Vs` and to the idea that many real-world systems fail not because the idea is bad, but because the data situation is messy.

### Scene 2. Analytics Is Not One Thing

Mathias asks:

> "Can we just do machine learning?"

Yunguri replies:

> "That is like entering a kitchen and asking whether we can just do knives."

Now distinguish:

- descriptive analytics: what is happening in listening behavior?
- diagnostic analytics: why do some playlists become popular?
- predictive analytics: what song is likely to be played next?
- prescriptive analytics: what should PachaMix recommend right now?

### Scene 3. Product Question versus Modeling Question

Mathias proposes:

> "Let us predict vibes."

Yunguri says:

> "That phrase belongs in prison."

Then translate vague product language into technical language:

- "songs with similar mood" becomes a feature-space similarity problem
- "make better playlists" becomes a ranking or recommendation problem
- "understand styles" becomes clustering or representation learning

## Mathematical Checkpoint

Use the board to formalize:

- data scale versus algorithmic scale
- memory footprint calculations
- throughput and latency examples
- why a method that works on `10,000` rows may fail on `10,000,000`

You can even give Mathias a tiny numerical disaster:

> Mathias: "I loaded everything into memory."
>
> Yunguri: "And?"
>
> Mathias: "The laptop made a sound I had not heard before."

## Lab Mission

`Mission: Audit the data before making promises.`

Students work as PachaMix's first technical team.

Tasks:

- inspect a song dataset
- identify feature types
- identify missing values
- estimate memory and storage cost
- define three different analytical questions from the same data

Possible in-story instruction:

> Yunguri: "If you do not know what each column means, then you are not doing analytics. You are decorating confusion."

## Closing Hook

Mathias leaves class excited:

> "Fine. Next week we classify, regress, cluster, reduce, and maybe deploy."

Yunguri pauses:

> "Next week we first learn the difference between supervised and unsupervised learning."

Mathias:

> "So no deployment?"

Yunguri:

> "You may deploy your expectations downward."

---

## Week 2. What Kind of Learning Problem Is This?

## Episode Goal

Introduce supervised and unsupervised learning and place recommendation problems inside the wider machine learning landscape.

## Cold Open

> Mathias: "I have solved it. PachaMix is supervised learning."
>
> Yunguri: "What is the label?"
>
> Mathias: "Good music."
>
> Yunguri: "That is not a label. That is a diplomatic incident."

## Theory Story

Mathias wants one grand model for everything.

Yunguri explains that not all learning problems are alike. Some have targets, others do not. Some predict, others discover structure.

The discussion becomes:

- if we predict whether a user will like a song, that is closer to supervised learning
- if we group songs by similarity, that is unsupervised
- if we compress audio or lyric features, that is representation learning or dimensionality reduction
- if we rank candidate songs, the task may look like recommendation or information retrieval

## Suggested Lecture Beats for the 2 Theory Hours

### Scene 1. Supervised Learning

Mathias asks for examples.

Yunguri gives them:

- predict a user rating
- classify whether a song belongs to a mood label
- forecast whether a playlist will be skipped quickly

Now define:

- features
- targets
- train set
- validation set
- test set

### Scene 2. Unsupervised Learning

Mathias says:

> "So unsupervised means the model just vibes alone."

Yunguri:

> "No. It means the structure is not given to you for free."

Now explain:

- clustering
- dimensionality reduction
- latent structure discovery

### Scene 3. Why Recommendation Is a Hybrid World

This is where the story gets useful.

PachaMix will eventually need:

- content-based recommendation
- collaborative filtering
- latent factors
- ranking

So the class sees early that recommendation is not a single algorithm but a family of approaches.

## Mathematical Checkpoint

At this point, formalize:

- supervised learning as minimizing a loss over labeled examples
- unsupervised learning as optimizing structure criteria without explicit targets
- the difference between prediction error and structure quality

Useful board-level comparison:

- regression: minimize MSE
- classification: minimize a classification loss or define a decision rule
- clustering: minimize within-group dispersion or optimize density connectivity

## Lab Mission

`Mission: Separate the learning tasks.`

Students receive several PachaMix scenarios and must classify them:

- supervised
- unsupervised
- recommendation/ranking
- data preparation problem

Then they run:

- one simple supervised model
- one simple unsupervised workflow

The point is not performance. The point is `problem framing`.

## Closing Hook

Mathias now believes everything is under control.

That is the precise moment Yunguri introduces the next disaster:

> "Your song vectors have thousands of features."

Mathias smiles:

> "Excellent. More features means more intelligence."

Yunguri turns to the class:

> "And that, students, is how dimensionality begins to ruin a perfectly good afternoon."

---

# Arc 2: Fighting High Dimensionality

## Week 3. The Curse of Dimensionality Arrives and Immediately Causes Problems

## Episode Goal

Show why high-dimensional data breaks naive intuition and why similarity becomes unreliable.

## Cold Open

> Mathias: "I made a feature vector with tempo, energy, danceability, acousticness, lyric counts, n-grams, embeddings, playlist statistics, and 2,000 extra columns just in case."
>
> Yunguri: "That is not a feature space. That is a cry for help."

## Theory Story

Mathias tries to compare songs using distance.

At first it sounds sensible:

- songs with similar features should be close
- songs with different features should be far

Then Yunguri asks:

> "Close in what dimension?"

The class discovers that in high-dimensional spaces:

- points become sparse
- nearest and farthest neighbors look less different
- geometric intuition collapses
- more data is often required to say anything meaningful

The emotional tone of the episode should be:

- funny panic from Mathias
- calm mathematical demolition from Yunguri

## Suggested Lecture Beats for the 2 Theory Hours

### Scene 1. Why More Features Can Hurt

Mathias believes each extra feature adds nuance.

Yunguri explains that extra features can also add:

- noise
- sparsity
- instability
- overfitting risk

### Scene 2. Geometry Stops Behaving Nicely

Use the image of:

- a hypercube
- a hypersphere

Yunguri explains that volume behaves strangely in higher dimensions.

Mathias says:

> "So you are telling me the geometry becomes philosophical."

Yunguri:

> "No. I am telling you it becomes expensive."

### Scene 3. Distance Concentration

This is the central dramatic moment.

If nearest and farthest distances become too similar, then many distance-based methods lose discriminative power.

That connects directly to:

- K-nearest neighbors
- clustering
- recommendation by similarity

## Mathematical Checkpoint

Work through:

- volume comparison of hypercube versus hypersphere
- distance concentration intuition
- why pairwise distance contrast decreases
- why sample requirements grow with dimension

This week should feel like the course's first major proof-based wake-up call.

## Lab Mission

`Mission: Measure the curse.`

Students simulate points in increasing dimensions and calculate:

- mean pairwise distances
- nearest-neighbor distances
- farthest-neighbor distances
- contrast ratios

Then they apply the same idea to a real music-feature dataset.

## Closing Hook

Mathias, now visibly humbled, asks:

> "So how do we escape?"

Yunguri smiles for the first time in several slides:

> "We reduce dimension, carefully, and with linear algebra."

---

## Week 4. PCA: Compressing Music Without Completely Losing Its Soul

## Episode Goal

Teach PCA as the first systematic response to high dimensionality.

## Cold Open

> Mathias: "Can we keep all the information and also reduce the dimensions?"
>
> Yunguri: "Can we keep all the cake and also eat it?"
>
> Mathias: "That sounds like a yes if we believe in ourselves."
>
> Yunguri: "It sounds like a constrained optimization problem."

## Theory Story

Mathias wants to compress the song data without destroying useful structure.

Yunguri proposes:

- center the data
- analyze variance
- find the directions that preserve the most information

Now PCA appears as a mathematically elegant answer:

- not magic
- not arbitrary
- a principled projection

## Suggested Lecture Beats for the 2 Theory Hours

### Scene 1. Variance as Information Proxy

Mathias asks why variance matters.

Yunguri explains that dimensions with little variation may contribute less to distinguishing items, while directions of large variance often capture stronger structure.

This is a good moment to emphasize that PCA is useful, but its assumptions must be understood.

### Scene 2. The Covariance Matrix Becomes a Character

Treat the covariance matrix almost like a plot reveal:

> "The data were noisy. The dimensions were many. Then the covariance matrix entered the room."

The class can laugh, but then immediately move into:

- covariance
- eigenvectors
- eigenvalues
- projection

### Scene 3. Principal Components as Best Directions

Mathias asks:

> "So PCA finds the best angle to look at the music?"

Yunguri:

> "Surprisingly, that is one of your better summaries."

## Mathematical Checkpoint

Derive PCA from:

- variance maximization under a norm constraint
- the Rayleigh quotient intuition
- the eigenvalue problem

This is a central week for board work.

Students should feel that the method is `proved`, not merely announced.

## Lab Mission

`Mission: Build the first compressed version of PachaMix's song universe.`

Tasks:

- standardize data if appropriate
- compute covariance
- extract principal components
- visualize songs in 2D
- interpret whether clusters or trends begin to appear

## Closing Hook

Mathias is thrilled:

> "Amazing. PCA fixed everything."

Yunguri:

> "It fixed enough to continue. Please do not confuse that with everything."

She then introduces:

- SVD
- low-rank approximation
- and the fact that nonlinear structure may require different tools

---

## Week 5. SVD, t-SNE, and the Difference Between Compression and Visualization

## Episode Goal

Show that not all dimensionality reduction methods solve the same problem.

## Cold Open

> Mathias: "I used t-SNE. The clusters look beautiful."
>
> Yunguri: "Do they mean anything?"
>
> Mathias: "They are beautiful."
>
> Yunguri: "That is not the same answer."

## Theory Story

PachaMix now has many possible representations of music.

Mathias wants the prettiest picture.

Yunguri wants the most defensible method.

This week is about distinguishing goals:

- compression
- denoising
- latent structure
- local neighborhood visualization

## Suggested Lecture Beats for the 2 Theory Hours

### Scene 1. SVD as Structured Factorization

Present SVD as a broader matrix factorization tool with geometric meaning.

Mathias:

> "So the matrix is decomposed into cleaner pieces?"

Yunguri:

> "Yes. For once, that is exactly correct."

Connect SVD to:

- PCA
- low-rank approximation
- compression

### Scene 2. t-SNE as a Visualization Tool

Mathias falls in love with a colorful 2D embedding.

Yunguri explains:

- t-SNE preserves local neighborhoods better than global geometry
- it is excellent for visual exploration
- it is not automatically the right representation for production pipelines

This is pedagogically valuable because it trains students not to confuse a beautiful plot with a deployable method.

### Scene 3. Methodological Discipline

This scene matters:

> Mathias: "If the plot looks right, it is right."
>
> Yunguri: "That sentence does not pass the spit test."

Now compare:

- PCA for linear variance-based reduction
- SVD for factorization and low-rank structure
- t-SNE for local visualization

## Mathematical Checkpoint

Cover:

- singular values
- truncated SVD
- reconstruction error
- local probability preservation intuition in t-SNE

The important pedagogical message:

`Different methods preserve different notions of structure.`

## Lab Mission

`Mission: Compare representations, not just plots.`

Students:

- apply PCA
- apply SVD
- apply t-SNE
- compare reconstruction, interpretability, and visual separability

They should answer:

- which method is best for compression?
- which for visualization?
- which for downstream clustering?

## Closing Hook

Mathias now says:

> "Good. We have reduced the dimensions. Now the songs will obviously organize themselves."

Yunguri:

> "No. Now we must ask how to group them."

Cue clustering.

---

# Arc 3: Discovering Structure

## Week 6. K-means: The Peccary Divides the Musical Universe into K Buckets

## Episode Goal

Teach K-means as the first clustering method and expose both its elegance and fragility.

## Cold Open

> Mathias: "I have decided there are exactly seven types of songs."
>
> Yunguri: "Based on what?"
>
> Mathias: "A feeling."
>
> Yunguri: "That feeling is not convex optimization."

## Theory Story

Mathias wants labeled music moods without doing the labor of labeling.

Yunguri introduces clustering:

- no labels
- discover structure
- group songs by proximity in feature space

K-means is ideal because it is intuitive, elegant, and flawed in teachable ways.

## Suggested Lecture Beats for the 2 Theory Hours

### Scene 1. Why Clustering Is Tempting

Students immediately understand the appeal:

- "study songs"
- "gym songs"
- "sleepy songs"
- "songs for writing code badly but confidently"

### Scene 2. Objective Function First

Yunguri refuses to proceed without the objective:

- minimize within-cluster squared distance

This is a major methodological signal:

`Algorithms are optimization procedures, not rituals.`

### Scene 3. Lloyd's Algorithm

Mathias likes the iterative logic:

- assign points
- recompute centroids
- repeat

Yunguri points out:

- initialization matters
- local minima exist
- cluster shape assumptions matter

## Mathematical Checkpoint

Derive:

- the SSE objective
- why centroid updates minimize squared distance within a cluster
- why each iteration does not increase the objective

This is one of the most satisfying derivations in the course because it feels computational and mathematical at the same time.

## Lab Mission

`Mission: Build PachaMix's first mood map.`

Students:

- run K-means on reduced song features
- test multiple values of `k`
- visualize clusters
- inspect songs inside clusters

Encourage classroom humor:

If a cluster contains lullabies, metal, and club remixes, Yunguri can say:

> "Congratulations. You have discovered the genre of methodological despair."

## Closing Hook

Mathias says:

> "Some clusters are weird."

Yunguri:

> "Yes. K-means assumes the world is kinder than it really is."

Next week introduces a method that can handle strange shapes and noise.

---

## Week 7. DBSCAN: Because Not Every Cluster Wants to Be a Circle

## Episode Goal

Teach density-based clustering and compare it with centroid-based assumptions.

## Cold Open

> Mathias: "K-means says these songs belong together."
>
> Yunguri: "Do they?"
>
> Mathias: "Not emotionally."
>
> Yunguri: "Then perhaps geometry is trying to tell you something."

## Theory Story

Mathias notices that some songs form irregular groups:

- niche instrumental tracks
- noisy outliers
- transitional songs between genres

Yunguri introduces `DBSCAN` as a method that asks:

- where is data dense?
- what belongs to a dense region?
- what should be treated as noise?

## Suggested Lecture Beats for the 2 Theory Hours

### Scene 1. Why K-means Fails on Strange Shapes

Use examples:

- elongated clusters
- crescent-shaped groups
- scattered outliers

### Scene 2. Core, Border, and Noise Points

This is a perfect storytelling week because the categories sound almost social:

- core points are the regulars
- border points attend the party but stand near the exit
- noise points arrived at the wrong event and refuse to leave

### Scene 3. Choosing Parameters

Mathias asks:

> "What are epsilon and minPts?"

Yunguri:

> "The price we pay for flexibility."

Now explain:

- local density
- reachability
- sensitivity of results to parameter choice

## Mathematical Checkpoint

Formalize:

- epsilon-neighborhoods
- density connectivity
- reachability
- differences in assumptions between K-means and DBSCAN

Then compare validation:

- silhouette
- Davies-Bouldin
- visual and domain interpretation

## Lab Mission

`Mission: Detect real musical structure and isolate noise.`

Students:

- compare K-means and DBSCAN on the same feature space
- identify outliers
- investigate songs that DBSCAN marks as noise
- decide which method better serves PachaMix's mood discovery

## Closing Hook

Mathias now says:

> "Excellent. We can group songs. But how do we recommend them?"

Yunguri:

> "First by content. Then by behavior. Eventually by admitting that no single method is enough."

---

# Arc 4: Recommending Music

## Week 8. Content-Based Recommendation: Recommend Songs by What They Are

## Episode Goal

Build a recommender from song properties such as audio and lyric features.

## Cold Open

> Mathias: "I have a brilliant rule. If a student likes one sad acoustic song, we recommend forty more."
>
> Yunguri: "That is not personalization. That is emotional recursion."

## Theory Story

Mathias wants PachaMix to recommend songs using only song descriptions:

- audio
- lyrics
- metadata

Yunguri explains that this is content-based recommendation.

If users and items can both be represented in feature space, we can rank songs by similarity.

This week works especially well because it connects directly to previous material:

- high-dimensional features
- dimensionality reduction
- similarity

## Suggested Lecture Beats for the 2 Theory Hours

### Scene 1. Build the Item Profile

What is a song mathematically?

Possible answers:

- a vector of acoustic attributes
- a vector of lyric weights
- a combination of both

### Scene 2. Build the User Profile

Mathias asks:

> "What is a user profile?"

Yunguri:

> "A summary of past preferences, ideally less chaotic than the user."

Then construct:

- average feature vectors
- weighted profiles from liked songs
- candidate scoring rules

### Scene 3. Strengths and Weaknesses

Content-based systems are:

- interpretable
- cold-start friendly for new items

But they also suffer from:

- overspecialization
- feature dependence
- limited discovery

## Mathematical Checkpoint

Cover:

- cosine similarity
- dot product
- feature weighting
- TF-IDF if lyrics are involved
- top-k ranking logic

This should feel computationally concrete and conceptually accessible.

## Lab Mission

`Mission: Make PachaMix recommend songs based on the songs themselves.`

Students:

- represent songs with features
- build user profiles
- compute similarity scores
- produce ranked song lists

Encourage them to inspect strange recommendations.

Mathias may proudly present:

> "Good news. The model recommends funeral piano pieces after acoustic folk songs."

Yunguri:

> "The model has discovered sadness, but not nuance."

## Closing Hook

Yunguri explains that song content is only half the story.

The other half is:

- what users actually listen to
- what songs co-occur in behavior
- and what collective taste reveals

---

## Week 9. Collaborative Filtering: Recommend Songs by What People Do

## Episode Goal

Teach user-based and item-based collaborative filtering.

## Cold Open

> Mathias: "What if we ignore the songs and just copy the taste of people who seem cool?"
>
> Yunguri: "Methodologically reckless. Socially realistic."

## Theory Story

Mathias notices that users often reveal patterns that song features alone do not capture.

Examples:

- songs that are very different acoustically may appear together in playlists
- some genres cross over through listener behavior
- some recommendations are socially emergent rather than content-driven

This is the perfect entry to collaborative filtering.

## Suggested Lecture Beats for the 2 Theory Hours

### Scene 1. User-Based Logic

If two users have similar histories, maybe one user's liked songs can inform the other's recommendations.

### Scene 2. Item-Based Logic

If two songs are often liked by similar users, maybe they are recommendation neighbors even when their raw features differ.

### Scene 3. Sparsity and Cold Start

Mathias asks:

> "What if the user is new?"

Yunguri:

> "Then the matrix knows nothing, and we must be honest about it."

## Mathematical Checkpoint

Formalize:

- user-item matrices
- cosine similarity
- Pearson correlation
- weighted rating prediction
- reliability issues in sparse spaces

This is a strong week to emphasize the difference between:

- similarity in content space
- similarity in behavior space

## Lab Mission

`Mission: Make PachaMix learn from listening behavior.`

Students:

- construct a user-item interaction matrix
- compute user or item similarity
- generate collaborative recommendations
- compare predictions with content-based results

## Closing Hook

Mathias is delighted:

> "Now we have two recommenders."

Yunguri:

> "Which means we are finally ready to admit that one alone is not enough."

---

## Week 10. Hybrid Recommendation and Matrix Factorization: The Playlist Gets Smarter

## Episode Goal

Show why hybrid approaches are often best, and introduce latent-factor thinking.

## Cold Open

> Mathias: "What if we combine everything?"
>
> Yunguri: "That depends. Are you combining methods or just stacking optimism?"

## Theory Story

By now PachaMix has:

- content-based recommendation
- collaborative recommendation

Each helps where the other struggles.

Yunguri proposes a more mature system:

- combine content signals
- combine user behavior
- learn latent structures

This is the week where the recommender becomes a serious system.

## Suggested Lecture Beats for the 2 Theory Hours

### Scene 1. Why Hybrid Models Work

Content helps when:

- items are new
- features are rich

Collaborative filtering helps when:

- behavior data is rich
- feature design is imperfect

The hybrid strategy emerges naturally.

### Scene 2. Latent Factors

Mathias asks:

> "So there are hidden dimensions of taste?"

Yunguri:

> "Yes. And unlike your playlist titles, some of them may actually be real."

Now introduce:

- matrix factorization
- low-rank structure
- latent preferences

### Scene 3. Optimization Again

Bring the course back to its methodological center:

- objective function
- regularization
- gradient updates

## Mathematical Checkpoint

Derive:

- regularized factorization objective
- intuitive gradient steps
- low-rank interpretation

This week should make students feel that recommendation is no longer just heuristic. It is now optimization and representation learning.

## Lab Mission

`Mission: Build the most mature version of PachaMix so far.`

Students:

- compare content-based, collaborative, and latent-factor models
- inspect successes and failures
- discuss which system they would trust in production

## Closing Hook

Mathias thinks the case is closed.

Then Yunguri notices something unexpected:

some songs become important not because of their features or ratings alone, but because of their position inside the `playlist ecosystem`.

The network arc begins.

---

# Arc 5: Seeing Music as a Network

## Week 11. Graph Analytics Foundations: Songs Are Not Only Vectors, They Are Also Nodes

## Episode Goal

Introduce graph representations using songs and playlists.

## Cold Open

> Mathias: "I thought songs were rows in a table."
>
> Yunguri: "They are. Until they become nodes in a graph."
>
> Mathias: "Can data have two personalities?"
>
> Yunguri: "Only the interesting data."

## Theory Story

Mathias notices that some songs repeatedly appear together in playlists.

Yunguri proposes a new representation:

- `node` = song
- `edge` = two songs appear together in the same playlist
- `weight` = how often they co-occur

This is the crucial move that makes the network chapter feel natural.

The question becomes:

- which songs are central?
- which songs connect otherwise separate communities?
- which songs act as bridges between moods or genres?

## Suggested Lecture Beats for the 2 Theory Hours

### Scene 1. From Table to Graph

Show how the same dataset can be represented as:

- a matrix of features
- a matrix of interactions
- a graph of co-occurrence

This is a beautiful methodological moment because it demonstrates that representation choices create different analytical possibilities.

### Scene 2. Basic Graph Concepts

Introduce:

- nodes
- edges
- directed and undirected graphs
- weighted edges
- degree
- paths
- connectivity

### Scene 3. Random Walk Intuition

Mathias asks:

> "If I jump from song to song through playlists, what happens?"

Yunguri:

> "That question is unexpectedly good."

Now move toward:

- transition probabilities
- random walks
- importance propagation

## Mathematical Checkpoint

Work through:

- adjacency matrices
- degree normalization
- stochastic matrices
- Markov intuition

The goal is to prepare students for PageRank without rushing.

## Lab Mission

`Mission: Build the PachaMix song graph.`

Students:

- create a co-occurrence graph from playlists
- compute degree or simple centrality measures
- inspect songs with high connectivity
- identify possible bridge songs

## Closing Hook

Mathias asks:

> "So popularity is not just play count?"

Yunguri:

> "Exactly. Some songs matter because important songs point to them."

That line leads directly to PageRank.

---

## Week 12. PageRank on the Playlist Graph: The Mathematics of Musical Importance

## Episode Goal

Teach PageRank as a graph ranking algorithm using song networks rather than web pages.

## Cold Open

> Mathias: "At last, an algorithm that tells us which songs are the kings of the graph."
>
> Yunguri: "Or queens. Or central stochastic entities. Let us not let the notation become feudal."

## Theory Story

Mathias assumes the most connected songs are the most important.

Yunguri complicates that intuition:

- not all links are equally informative
- being connected to important songs matters
- random walks provide a principled ranking interpretation

This is where the network chapter becomes elegant.

The playlist graph now behaves like a structured system of recommendations flowing through listening behavior.

## Suggested Lecture Beats for the 2 Theory Hours

### Scene 1. PageRank as a Recursive Definition

Important songs are connected to other important songs.

Mathias:

> "So importance depends on importance?"

Yunguri:

> "Yes. Welcome to fixed-point thinking."

### Scene 2. Damping and Teleportation

This is a wonderful storytelling moment:

> Mathias: "What if the random listener gets stuck?"
>
> Yunguri: "Then we let them teleport. Mathematics occasionally allows drama."

Now explain:

- damping
- dangling nodes
- uniqueness
- convergence

### Scene 3. Why This Matters for PachaMix

Song centrality can support:

- playlist seeding
- bridge-song discovery
- popularity beyond raw count
- structural recommendation features

## Mathematical Checkpoint

Derive or explain carefully:

- the PageRank fixed-point equation
- the role of the transition matrix
- the role of damping
- power iteration
- why convergence is expected

This should be one of the mathematically richest weeks of the semester.

## Lab Mission

`Mission: Rank songs by structural importance.`

Students:

- run PageRank on the playlist graph
- inspect top-ranked songs
- compare PageRank with simple degree counts
- discuss whether the most central songs are also the most interesting recommendation seeds

## Closing Hook

Mathias is proud:

> "We have features, clusters, recommenders, and graph rankings. We are done."

Yunguri looks at the class with the compassion of someone about to assign infrastructure.

> "No. We have a research prototype."

Next comes deployment.

---

# Arc 6: Making the System Real

## Week 13. From Notebook to Pipeline: PachaMix Learns to Behave Like a System

## Episode Goal

Show students that models must become reproducible workflows before they become products.

## Cold Open

> Mathias: "The notebook works."
>
> Yunguri: "On whose machine?"
>
> Mathias: "Mine."
>
> Yunguri: "And when you restart?"
>
> Mathias: "...we do not need negativity."

## Theory Story

This week is where the course matures.

Mathias learns the uncomfortable truth:

- a notebook is not a product
- an impressive plot is not deployment
- a manual sequence of cells is not a pipeline

Yunguri reframes the work:

- define inputs
- define outputs
- define preprocessing
- define artifacts
- define evaluation checkpoints
- make the process repeatable

## Suggested Lecture Beats for the 2 Theory Hours

### Scene 1. Why Good Models Fail in Practice

Use examples:

- inconsistent preprocessing
- missing feature versioning
- hidden notebook state
- code that only works in one environment

### Scene 2. Batch versus Streaming

Mathias imagines real-time recommendation for every student instantly.

Yunguri asks whether the product actually needs:

- real-time inference
- periodic batch recomputation
- or a hybrid design

### Scene 3. Pipeline Thinking

Students should begin thinking like system designers:

- ingest
- clean
- transform
- train
- evaluate
- publish

## Mathematical Checkpoint

Connect systems ideas back to measurable concepts:

- latency
- throughput
- resource constraints
- reproducibility
- drift

The key message:

`Engineering constraints are quantitative too.`

## Lab Mission

`Mission: Convert a PachaMix notebook into a repeatable pipeline.`

Students:

- refactor one workflow
- define data dependencies
- define outputs and artifacts
- specify evaluation checkpoints

Possible joke:

> Yunguri: "If the only deployment strategy is 'run all cells and hope,' then what you have built is not a pipeline. It is a ritual."

## Closing Hook

Mathias asks:

> "Fine. The pipeline runs. Are we done now?"

Yunguri:

> "Can it serve recommendations? Can it be monitored? Can we detect drift? Can we explain failure?"

Mathias:

> "I miss Week 1."

---

## Week 14. Serving, Monitoring, and the Final Defense of PachaMix

## Episode Goal

Close the course by integrating analytics, mathematics, and engineering into one coherent product story.

## Cold Open

> Mathias: "At last. We deploy."
>
> Yunguri: "At last. We deploy responsibly."
>
> Mathias: "That sounds slower."
>
> Yunguri: "That sounds employed."

## Theory Story

PachaMix now exists as:

- a recommendation idea
- a modeling stack
- a graph ranking system
- a pipeline

But Yunguri insists that the final lesson is not about code alone. It is about judgment.

Students must ask:

- when should a recommendation be served?
- how do we monitor quality?
- what if data drift changes user behavior?
- what if the system over-recommends a narrow style?
- how do we explain why a song was recommended?

## Suggested Lecture Beats for the 2 Theory Hours

### Scene 1. Serving Recommendations

Discuss:

- batch recommendation generation
- online ranking
- API service concepts
- retrieval plus ranking

### Scene 2. Monitoring and Drift

Mathias wants to celebrate.

Yunguri interrupts him with every operational nightmare:

- degraded recommendation quality
- stale profiles
- shifting listening patterns
- broken feature pipelines

The class should see monitoring as part of the scientific method of operating a system.

### Scene 3. Final Comparative Reflection

Now compare all methods studied:

- PCA/SVD/t-SNE
- K-means/DBSCAN
- content-based/collaborative/hybrid recommendation
- graph centrality/PageRank

This lets the semester close with synthesis rather than fragmentation.

## Mathematical Checkpoint

Discuss:

- uncertainty and repeated-run variability
- confidence intervals where appropriate
- monitoring thresholds
- trade-offs between relevance, diversity, novelty, and stability

Students should leave understanding that operational quality is also something to reason about quantitatively.

## Lab Mission

`Mission: Defend PachaMix as if it were a real product.`

Students:

- present one version of the system
- explain the data representation
- explain the algorithms used
- justify the mathematical choices
- discuss deployment and monitoring assumptions

This is the capstone moment.

## Final Closing Scene

Mathias stands in front of the finished prototype.

> Mathias: "So what did we build?"

Yunguri replies:

> "Not just a playlist tool. A full analytical system."

Mathias:

> "With linear algebra, optimization, graph theory, and deployment?"

Yunguri:

> "Yes."

Mathias:

> "That seems like a lot just to recommend songs."

Yunguri:

> "That is the entire point of the course."

Then one final callback:

> Mathias: "Does the final system pass the spit test?"

Yunguri pauses.

> "Mostly."

And for Yunguri, that is practically a standing ovation.

---

## Optional Instructor Notes

## How to Use Humor Without Losing Rigor

- Let Mathias say the naive thing many students are thinking.
- Let Yunguri correct him with precision, not cruelty.
- Use the jokes to create memory anchors for the mathematics.
- Repeat the callbacks across the semester so the narrative feels cumulative.

## Best Use of the Story in Class

- open each class with a `2-5 minute dialogue`
- return to the characters when introducing definitions
- use Mathias for intuitive mistakes
- use Yunguri for methodological correction
- end with a narrative cliffhanger for the next week

## Why This Story Works

The story is effective because it mirrors how real projects actually unfold:

- the problem starts vague
- the data are messy
- the first model is naive
- geometry becomes difficult
- methods must be compared
- recommendation requires multiple approaches
- graphs reveal hidden structure
- deployment forces discipline

In other words, Mathias and Yunguri are not decorations. They are a pedagogical device for making the methodology memorable.

---

## One-Line Summaries for Fast Recall

- `Week 1`: The friends define the product and learn that analytics starts with questions, not code.
- `Week 2`: They separate supervised from unsupervised learning and stop calling everything "AI."
- `Week 3`: High-dimensional data attacks the project.
- `Week 4`: PCA saves the project with linear algebra.
- `Week 5`: SVD and t-SNE teach that not every map preserves the same truth.
- `Week 6`: K-means groups songs, sometimes beautifully, sometimes hilariously badly.
- `Week 7`: DBSCAN rescues irregular structure and teaches density.
- `Week 8`: Content-based recommendation learns songs from what they are.
- `Week 9`: Collaborative filtering learns songs from what listeners do.
- `Week 10`: Hybrid recommendation combines evidence and grows up.
- `Week 11`: Songs become nodes in a playlist graph.
- `Week 12`: PageRank reveals structural musical importance.
- `Week 13`: The prototype becomes a pipeline.
- `Week 14`: The pipeline becomes a defendable system.
