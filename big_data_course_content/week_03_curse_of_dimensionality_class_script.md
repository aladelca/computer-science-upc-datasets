# Week 3 Class Script - The Curse of Dimensionality

## Purpose

This is an instructor-facing lecture script for Week 3.
It is aligned with:

- `big_data_course_content/week_03_curse_of_dimensionality.md`
- `big_data_course_content/notebooks/week_03_curse_of_dimensionality.ipynb`
- `big_data_course_content/presentations/week_3.pdf`
- `big_data_course_content/presentations/week_3.pptx`

The script is written in English and is designed for a class that combines:

- a theory block with strong mathematical emphasis
- a guided notebook block with empirical verification
- a clear bridge into Week 4 on PCA

The goal is not only to say that high-dimensional spaces are difficult, but to show exactly why they are difficult, where the mathematics appears, and how the notebook verifies the theory.

---

## Session Goals

By the end of the class, students should be able to:

1. Explain why geometric intuition breaks down in high dimension.
2. Derive the volume ratio between the inscribed hypersphere and the surrounding hypercube.
3. Derive the expected squared Euclidean distance between two random points in `[0,1]^d`.
4. Explain distance concentration and why it damages distance-based methods.
5. Distinguish between dense and sparse high-dimensional regimes.
6. Explain why sample complexity grows rapidly with dimension.
7. Connect the theory to the PachaMix audio and lyrics representations.
8. Justify why dimensionality reduction is structural rather than cosmetic.

---

## Class Structure

Recommended total duration: about `3.5` to `4` hours

- `Theory lecture`: `1h 45m` to `2h`
- `Notebook-guided practice`: `1h 30m` to `2h`

If the class must be shorter, keep the theory core and assign the later notebook extensions as independent work.

---

## Assets to Open Before Class

Open these in advance:

- the Week 3 presentation
- the Week 3 notebook
- the week markdown file

The presentation gives the narrative rhythm.
The markdown gives the course-level theory.
The notebook gives the verification layer.

---

## Instructor Tone

This week should feel like the first real mathematical warning shot of the semester.
The tone is:

- playful in the opening
- rigorous in the middle
- empirical in the notebook
- strategic in the closing

Mathias and Yunguri are not decoration.
They are there to stage the main intellectual conflict:

- Mathias says: "More features means more information."
- Yunguri says: "Only if the geometry remains useful."

That conflict is the whole week.

---

## Detailed Teaching Script

## Part 1. Opening and Motivation

### Slides `1-6`

### Instructor objective

Establish the problem emotionally before formalizing it mathematically.

### What to say

"Today is the first week where the course becomes explicitly geometric. Up to this point, students can still believe that more columns are almost always an advantage. This week we begin to dismantle that belief carefully."

"Mathias thinks feature engineering is always beneficial. He keeps adding tempo, energy, danceability, lyrics, embeddings, playlist statistics, and whatever else he can find. Yunguri immediately asks the correct question: what kind of geometry have you just created?"

"That is the heart of the curse of dimensionality. It is not just that there are many columns. It is that distance, neighborhood, and local structure begin to behave in ways that are unintuitive and sometimes operationally useless."

### Classroom questions

Ask:

- "If I add 500 more features, what do you expect to improve?"
- "What assumptions are you making when you say similar points should be close?"
- "Close according to what metric, after what preprocessing, in what representation?"

### Transition line

"Now let us stop speaking vaguely and look at what these feature spaces actually mean for PachaMix."

---

## Part 2. The PachaMix Anchor

### Slide `7`

### Instructor objective

Ground the abstract discussion in the actual course datasets.

### What to say

"In this repo, `pachamix_audio_core` has hundreds of numeric descriptors per track. That is already enough for pairwise distances to become expensive and unstable. And if we move to lyrics, bag-of-words and TF-IDF spaces are even larger and often sparse."

"So this is not a fake textbook problem. It is our real problem. If we want song similarity, clustering, or recommendation, we must ask whether ambient high-dimensional distance still deserves our trust."

### Important clarification

Say explicitly:

"High dimension is not automatically a disaster. The disaster begins when we use naive geometric intuition as if the space were still 2D or 3D."

---

## Part 3. Intuition Failure in 2D Versus 100D

### Slide `8`

### Instructor objective

Show that visual intuition and high-dimensional geometry do not align.

### What to say

"In 2D, we can often point to a nearest neighbor and feel that the result makes sense. In high dimension, the ranking exists, but the meaning of that ranking weakens."

"The problem is not that distances disappear. Distances still exist. In fact, they often get larger. The problem is that nearest and farthest distances become less different relative to the scale of the space."

### Mini-blackboard explanation

Write:

`distance exists != distance is informative`

Then say:

"A method can still compute a nearest neighbor while that nearest neighbor is only marginally nearer than many alternatives. That is the beginning of operational trouble."

---

## Part 4. Hypercube Versus Hypersphere

### Slides `9-10`

### Instructor objective

Prove that high-dimensional volume behaves in a way that breaks low-dimensional intuition.

### What to say

"We start with a geometric fact that is famous for good reason. Consider the unit ball inside the cube `[-1,1]^d`. In low dimension, the ball feels like a substantial part of the cube. In high dimension, that intuition dies."

Write on the board:

$$
V_d(1) = \frac{\pi^{d/2}}{\Gamma\left(\frac{d}{2}+1\right)}
$$

and

$$
\operatorname{Vol}([-1,1]^d) = 2^d.
$$

Then write:

$$
\frac{V_d(1)}{2^d}
=
\frac{\pi^{d/2}}{2^d \Gamma\left(\frac{d}{2}+1\right)}.
$$

### Mathematical verification

At this point, do not only state the limit.
Show a real asymptotic argument.

Use Stirling's approximation:

$$
\Gamma\left(\frac{d}{2}+1\right)
\sim
\sqrt{\pi d}\left(\frac{d}{2e}\right)^{d/2}.
$$

Substitute it:

$$
\frac{\pi^{d/2}}{2^d \Gamma\left(\frac{d}{2}+1\right)}
\sim
\frac{1}{\sqrt{\pi d}}
\left(\frac{\pi e}{2d}\right)^{d/2}.
$$

Then say:

"The factor `(\pi e / (2d))^(d/2)` goes to zero very fast as `d` increases. So the inscribed ball becomes a vanishing fraction of the cube."

### Interpretation to emphasize

"In high dimension, most of the volume is not where our low-dimensional intuition expects it to be. This is one reason neighborhoods become strange. 'Near the center' and 'near the boundary' stop behaving the way we picture them."

### Check-for-understanding question

Ask:

- "Does the ball become smaller?"

Then answer it yourself:

"No. The ball is not shrinking in its own definition. What shrinks is its volume share relative to the surrounding cube."

---

## Part 5. Expected Squared Distance

### Slide `11`

### Instructor objective

Derive an exact benchmark that can later be checked numerically in the notebook.

### What to say

"The next question is not about volume. It is about distance. Suppose `x` and `y` are independent uniform random points in `[0,1]^d`. What is the expected squared Euclidean distance between them?"

Write:

$$
\|x-y\|_2^2 = \sum_{j=1}^d (x_j-y_j)^2.
$$

Take expectation:

$$
\mathbb{E}\|x-y\|_2^2
=
\sum_{j=1}^d \mathbb{E}(x_j-y_j)^2.
$$

Now verify one coordinate carefully.

Let `X, Y ~ Unif([0,1])` independently.
Then:

$$
\mathbb{E}(X-Y)^2
=
\operatorname{Var}(X-Y)
=
\operatorname{Var}(X)+\operatorname{Var}(Y)
=
\frac{1}{12}+\frac{1}{12}
=
\frac{1}{6}.
$$

Therefore:

$$
\mathbb{E}\|x-y\|_2^2 = d\cdot \frac{1}{6} = \frac{d}{6}.
$$

### Interpretation to say out loud

"This result matters because it tells us something exact. Distances are not merely noisy or mysterious. On average, squared distances grow linearly with dimension."

"So high-dimensional trouble is not the absence of distance. It is the combination of large distances with weak contrast."

---

## Part 6. Stronger Concentration Explanation

### Slides `12-13`

### Instructor objective

Move from exact expectation to the more subtle issue of relative concentration.

### What to say

"Now we sharpen the argument. It is not enough to know that distances grow. We must explain why they become less useful."

Start from:

$$
S_d = \|x-y\|_2^2 = \sum_{j=1}^d Z_j
\quad\text{where}\quad
Z_j=(x_j-y_j)^2.
$$

We already know:

$$
\mathbb{E}[Z_j] = \frac{1}{6}.
$$

For a stronger check, state:

$$
\mathbb{E}[Z_j^2] = \mathbb{E}(x_j-y_j)^4 = \frac{1}{15},
$$

so

$$
\operatorname{Var}(Z_j)
=
\frac{1}{15} - \left(\frac{1}{6}\right)^2
=
\frac{7}{180}.
$$

Hence:

$$
\mathbb{E}[S_d] = \frac{d}{6},
\qquad
\operatorname{Var}(S_d) = d\cdot \frac{7}{180}.
$$

Now compute the coefficient of variation:

$$
\frac{\sqrt{\operatorname{Var}(S_d)}}{\mathbb{E}[S_d]}
=
\frac{\sqrt{7d/180}}{d/6}
=
\frac{\sqrt{7/5}}{\sqrt{d}}.
$$

### Why this matters

Say:

"This is the key point. Relative fluctuation shrinks like `1/sqrt(d)`. So the distance values become more tightly concentrated around a typical value. That is the mathematical core behind the heuristic that nearest and farthest points become less distinguishable."

Then connect to the slide formula:

$$
\frac{\max_i d(x,x_i)-\min_i d(x,x_i)}{\min_i d(x,x_i)} \to 0
$$

in many high-dimensional regimes.

### Important caveat

Say explicitly:

"This is a heuristic summary, not a universal theorem for every dataset under every metric. The exact statement depends on the distribution and representation. But the practical message is robust: distance ranking weakens in many high-dimensional settings."

---

## Part 7. Why Methods Break

### Slide `14`

### Instructor objective

Translate the mathematics into machine-learning consequences.

### What to say

"Now let us stop being abstract. If nearest and farthest distances become relatively close, then what breaks?"

State each item carefully:

- `K-nearest neighbors`: ranking becomes fragile because local neighborhoods are weakly separated
- `clustering`: cluster assignments depend heavily on preprocessing, metric choice, and noise
- `recommendation`: a 'nearest song' may be a metric artifact rather than a meaningful neighbor

### Suggested line

"The curse is not only geometric. It is operational. It changes which algorithms are reliable."

---

## Part 8. Short Reset

### Slide `15`

Use this as a visual pause.

Say:

"At this point, students usually say: fine, high dimension is annoying. But we still need a sharper distinction, because not all high-dimensional spaces fail in exactly the same way."

---

## Part 9. Dense Versus Sparse High-Dimensional Spaces

### Slides `16-17`

### Instructor objective

Differentiate audio-style dense vectors from lyric-style sparse vectors.

### What to say

"Dense and sparse spaces are both high-dimensional, but the mechanism of failure is not identical."

"In dense audio vectors, many coordinates contribute small amounts to Euclidean distance."

"In sparse lyric vectors, overlap of supports becomes decisive. Two documents may be almost orthogonal simply because they use different rare tokens."

### Important clarification

Say:

"Sparsity does not save us from the curse. It changes the geometry, but it does not automatically restore meaningful neighborhoods."

### Link to notebook

"This is why the notebook treats the audio matrix and the lyric matrix separately instead of pretending one metric behaves identically in both settings."

---

## Part 10. Sample Complexity

### Slide `18`

### Instructor objective

Make students confront the exponential dependence on dimension.

### What to say

"Suppose we want resolution `\varepsilon` in every coordinate of a unit hypercube. A naive covering argument says we need roughly"

$$
\left(\frac{1}{\varepsilon}\right)^d
$$

cells.

"This is not a polished statistical minimax theorem. It is a crude covering argument. But that is precisely why it is pedagogically useful. It makes the exponential dependence visible immediately."

### Numerical check

Use the slide table:

- for `\varepsilon = 0.5` and `d = 10`, we already need `1024` cells
- for `\varepsilon = 0.1` and `d = 10`, we need `10^{10}` cells

Then say:

"This is why saying 'we will just collect more samples' is often intellectually lazy. How many more? In high dimension, the answer can be absurdly many."

---

## Part 11. Feature Selection Versus Dimensionality Reduction

### Slide `19`

### Instructor objective

Prevent a common conceptual error before PCA arrives.

### What to say

"There are two different responses to high dimensionality, and students often confuse them."

Define them clearly:

- `feature selection`: keep a subset of original coordinates
- `dimensionality reduction`: build new coordinates as combinations of the old ones

Then say:

"Feature selection says some variables are dispensable. Dimensionality reduction says useful structure may be spread across many variables, but concentrated near a lower-dimensional subspace or manifold."

"Week 4 will focus on PCA because our audio features are engineered families. We do not want to assume that the useful information lives in a tiny handpicked subset."

---

## Part 12. Emotional Close and Transition to PCA

### Slides `20-24`

### Instructor objective

End the week with the correct strategic answer: representation, not despair.

### What to say

"The conclusion of Week 3 is not that geometry is impossible. The conclusion is that raw ambient geometry is often the wrong geometry."

"That is why Yunguri's answer is not 'give up.' It is 'change the representation carefully.'"

"Next week we begin the first systematic escape route: PCA. PCA will not solve every problem, but it will give us a principled linear way to compress variance into fewer directions."

Final line:

"Week 3 harms your geometric intuition. Week 4 rebuilds it with linear algebra."

---

## Notebook Script

This section is the speaking script for the practice block.

## Notebook Step 1. Simulate random points in increasing dimensions

### Corresponding notebook cells

- Markdown cell: "Guided notebook"
- Code cell: `distance_summary(...)`

### What to say

"We now move from the board to the machine. The purpose is not to produce pretty plots. The purpose is to verify a geometric claim numerically."

"We simulate random points in dimensions `2, 10, 50, 100, 500`. For each dimension, we compute mean pairwise distance, nearest-neighbor distance, farthest-neighbor distance, and a contrast statistic."

### What to ask students

- "Which statistic should grow?"
- "Which statistic should shrink relatively?"
- "What exactly are we treating as the signal of the curse?"

### Critical interpretation

"Do not let students say 'the curse is visible' unless they specify what statistic made it visible."

---

## Notebook Step 2. Visualize contrast-ratio decay

### Corresponding notebook cells

- Markdown cell: "Visualize the contrast-ratio decay"
- Plot from `sim_df`

### What to say

"This plot is the empirical version of the distance-concentration discussion. It shows that as dimension grows, the relative gap between nearest and farthest distances tends to shrink."

"A metric can continue to exist while becoming less discriminative."

### Instructor warning

"Do not oversell a single plot. This is a descriptive confirmation, not a universal proof."

---

## Notebook Step 3. Verify expected squared-distance growth

### Corresponding notebook cells

- Markdown cell: "Verify the expected squared-distance growth"
- Code cell: `expected_squared_distance_demo(...)`

### What to say

"This is the cleanest theoretical checkpoint of the notebook because the benchmark is exact: `d/6`."

"Students should compare empirical and theoretical values and explain why they align. If they only say 'the numbers are close,' that is not enough. They must connect the observation to the derivation."

### What to ask

- "Why is the benchmark exact?"
- "Why are we checking squared distance instead of only distance?"

Expected answer:

"Because squared Euclidean distance decomposes additively over coordinates, which makes the expectation analytically tractable."

---

## Notebook Step 4. Repeat the experiment on real audio data

### Corresponding notebook cells

- Markdown cell: "Repeat the experiment on real audio data"
- Code cell loading `pachamix_audio_core`

### What to say

"Now we stop living in synthetic geometry and move into an actual feature matrix. We standardize the numeric audio features before Euclidean analysis because otherwise scale effects can dominate the geometry."

"This is an important methodological point: if preprocessing changes the geometry, then preprocessing is part of the model."

### What to emphasize

- metric used: Euclidean
- preprocessing used: standardization
- data regime: dense numeric feature matrix

---

## Notebook Step 5. Optional lyric-space extension

### Corresponding notebook cells

- Markdown cell: "Optional lyric-space extension"
- code building the lyric token representation

### What to say

"Here we test the claim that sparse text spaces fail differently, not magically. Vocabulary overlap becomes a central issue. Rare terms can destabilize similarity."

"Students must explicitly say whether they are using Euclidean or cosine logic. If they fail to name the metric, they are skipping the actual geometry."

---

## Notebook Step 6. Additional practice example

### Corresponding notebook cells

- Markdown cell: "Additional Practice Example"
- code using `contrast_stat(X, metric)`

### What to say

"This section protects us from one of the most common bad habits in machine learning education: discussing the curse of dimensionality as though it were independent of metric choice."

"Change one thing at a time: metric, standardization, dense versus sparse representation. Then explain what changed and why."

### Good instructor question

"If cosine and Euclidean produce different contrast behavior, which part of the pipeline changed: the data, the geometry, or both?"

Correct answer:

"The data matrix stayed the same, but the geometry changed because the metric changed."

---

## Mathematical Board Checks

Use these if you want a more rigorous board segment than the slides alone provide.

## Check 1. One-coordinate variance calculation

Write:

$$
\operatorname{Var}(X)=\frac{1}{12}, \qquad X\sim \mathrm{Unif}([0,1]).
$$

Then:

$$
\operatorname{Var}(X-Y)=\operatorname{Var}(X)+\operatorname{Var}(Y)=\frac{1}{6}.
$$

Because `E[X-Y]=0`, this also gives:

$$
\mathbb{E}(X-Y)^2=\frac{1}{6}.
$$

This is the cleanest route to the expected squared-distance formula.

## Check 2. Relative concentration via coefficient of variation

Write:

$$
S_d=\sum_{j=1}^d Z_j,
\quad
\mathbb{E}[Z_j]=\frac{1}{6},
\quad
\operatorname{Var}(Z_j)=\frac{7}{180}.
$$

Then:

$$
\frac{\sqrt{\operatorname{Var}(S_d)}}{\mathbb{E}[S_d]}
=
\frac{\sqrt{7/5}}{\sqrt{d}}.
$$

Say:

"This is not yet the full nearest-neighbor theorem, but it explains why relative distance variation shrinks as dimension grows."

## Check 3. Stirling-based asymptotic for the hyperball ratio

Write:

$$
\Gamma\left(\frac{d}{2}+1\right)
\sim
\sqrt{\pi d}\left(\frac{d}{2e}\right)^{d/2}.
$$

Substitute and simplify to:

$$
\frac{V_d(1)}{2^d}
\sim
\frac{1}{\sqrt{\pi d}}
\left(\frac{\pi e}{2d}\right)^{d/2}.
$$

Then say:

"The ratio collapses super-fast because `d` appears in the denominator of the base and also inside the exponent."

## Check 4. Covering-number intuition

Write:

$$
N(\varepsilon)\approx \left(\frac{1}{\varepsilon}\right)^d.
$$

Then say:

"This argument is crude but strategically correct. High-dimensional local coverage becomes combinatorially expensive."

---

## Common Student Errors and Corrections

## Error 1

Student says:

"High-dimensional data is bad."

Correct it with:

"Name the mechanism. Is the problem weak distance contrast, sparse overlap, scale sensitivity, or sample complexity?"

## Error 2

Student says:

"We standardized, so the problem is solved."

Correct it with:

"Standardization may remove one distortion, but it does not restore discriminative neighborhoods automatically."

## Error 3

Student says:

"The nearest neighbor exists, so it is meaningful."

Correct it with:

"Existence is not the issue. Informative separation is the issue."

## Error 4

Student says:

"Sparse vectors are easy because most entries are zero."

Correct it with:

"Sparse geometry changes the problem; it does not eliminate it."

## Error 5

Student says:

"More rows will fix everything."

Correct it with:

"How many more? In high dimension, required coverage can grow exponentially."

---

## Closing Message for the Instructor

If the week goes well, students should leave with a very specific discomfort:

- they should distrust naive similarity in raw high-dimensional space
- they should understand that the distrust is mathematical, not stylistic
- they should be ready to accept PCA as a principled response rather than a decorative plotting tool

The last sentence of the class should point directly to Week 4:

> "Now that we understand why raw high-dimensional geometry can fail, we are ready to study how PCA builds a better linear representation."
