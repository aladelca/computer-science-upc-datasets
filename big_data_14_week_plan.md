# Big Data Course Content Plan

## Course Basis

This plan is derived from the syllabus in [UG-202520_1ACC0221-Big data.pdf](./UG-202520_1ACC0221-Big%20data.pdf).

## Related Materials

- [Compact weekly table](./big_data_14_week_plan_table.md)
- [Narrative teaching script: PachaMix with Mathias and Yunguri](./big_data_pachamix_narrative_script.md)
- [Dataset generation guide for PachaMix](./big_data_dataset_generation_plan.md)

The original syllabus spans 16 weeks, but its content units map naturally to 14 instructional weeks. This plan assumes:

- `14 teaching weeks`
- `4 hours per week`
- `2 theoretical hours + 2 practical/laboratory hours per week`
- `Weeks 15 and 16 reserved for performance evaluation, final project delivery, and final exam`

## Pedagogical Focus

The course is designed with two explicit priorities:

- `Mathematical verification`: every major algorithm is taught from its objective function, derivation, convergence logic, or linear algebraic/statistical foundation.
- `Applicability`: every week includes a laboratory component in Python using `Anaconda`, `Google Colab`, `Kaggle`, and progressively `Spark`-style large-scale workflows.

---

## Compact Weekly Table

This version is intended for quick reuse in `Word`, `PowerPoint`, or a course planning sheet.

| Week | Main Topic | Theory Focus (2h) | Mathematical Verification Focus | Practice/Lab Focus (2h) |
| --- | --- | --- | --- | --- |
| 1 | Big Data, Advanced Analytics, and Data Science | Big Data, data science, ML, AI, analytics types, 5Vs, industrial motivation | Complexity, throughput, memory footprint, data scale versus model scale | Environment setup, dataset inspection, analytics problem framing |
| 2 | Supervised and Unsupervised Learning | Classification, regression, clustering, dimensionality reduction, learning pipeline, large-scale workflows | Loss functions, MSE, generalization, train/validation/test logic | Simple supervised and unsupervised notebooks, workflow comparison |
| 3 | Curse of Dimensionality | High-dimensional geometry, sparsity, distance concentration, effects on learning | Hypercube versus hypersphere, contrast loss, sample complexity intuition | Distance concentration simulation, sparse data analysis |
| 4 | PCA | Variance, covariance, orthogonal projection, PCA intuition | PCA derivation, constrained optimization, eigenvalue problem | Covariance computation, PCA implementation, 2D projection |
| 5 | SVD, t-SNE, and Other Reduction Methods | SVD, relation to PCA, t-SNE, random projections, UMAP comparison | Low-rank approximation, singular values, reconstruction error, neighborhood preservation | PCA/SVD comparison, t-SNE visualization, embedding analysis |
| 6 | Clustering with K-means | Prototype-based clustering, Lloyd's algorithm, initialization, scalability | SSE objective, monotonic descent, centroid optimality | K-means from scratch and with libraries, sensitivity analysis |
| 7 | Clustering with DBSCAN and Validation | Density-based clustering, core/border/noise points, method comparison | Density-connectivity, epsilon/minPts, silhouette and validation metrics | K-means versus DBSCAN on structured datasets |
| 8 | Content-Based Recommendation | Personalization, item features, user profiles, ranking | Cosine similarity, TF-IDF, scoring functions, overspecialization limits | Content-based recommender construction and top-k evaluation |
| 9 | Collaborative Filtering | User-based and item-based recommenders, sparsity, cold start | Cosine/Pearson similarity, weighted prediction, baseline correction | Neighborhood-based recommender and RMSE/MAE evaluation |
| 10 | Hybrid Recommendation and Matrix Factorization | Mixed recommenders, latent factors, regularization, scalability | Matrix factorization objective, SGD updates, low-rank interpretation | Hybrid and latent-factor recommender comparison |
| 11 | Graph Analytics Foundations | Graph representation, centrality, connectivity, random walks | Markov chains, stochastic matrices, transition probabilities | Centrality computation and random walk experiments |
| 12 | PageRank | Ranking on graphs, damping, dangling nodes, power iteration | Fixed-point equation, convergence, dominant eigenvector interpretation | PageRank implementation and convergence analysis |
| 13 | Deployment I: Pipelines | Batch versus streaming, reproducibility, APIs, scheduled workflows | Latency, throughput, drift, reproducibility metrics | Convert notebooks into reproducible pipelines |
| 14 | Deployment II: Serving and Monitoring | Serving, monitoring, fairness, explainability, operational decision-making | Error propagation, confidence intervals, monitoring thresholds | Capstone integration and technical defense |

---

## Dataset Strategy for the Semester

The most feasible course design is to use a `modular dataset stack`, not a single giant merged music table.

This is the recommended structure:

- `Audio and metadata layer`
  Use the `FMA` dataset for Weeks `1-7` to teach exploratory analysis, high-dimensional geometry, PCA, SVD, t-SNE, and clustering.
- `Lyrics layer`
  Use the `musiXmatch lyrics dataset for the Million Song Dataset` for lyric-derived representations, `TF-IDF`, and content-based recommendation features.
- `Behavior layer`
  Use `Playlist2vec` table exports for collaborative filtering, playlist continuation, and graph construction.
- `Network layer`
  Derive a `song co-occurrence graph` from playlist membership data and use it in Weeks `11-12` for graph analytics and `PageRank`.

This is preferable to forcing all weeks to depend on one merged source because:

- it keeps the data legally and operationally cleaner
- it avoids fragile record linkage between unrelated catalogs
- it allows small local subsets for laptops and larger subsets for Colab/Spark
- it preserves the narrative coherence of `PachaMix` without pretending the entire semester must come from one perfectly linked table

## Important Source Constraint

As of `March 15, 2026`, the course should **not** rely on the Spotify Web API for audio features as a core teaching dependency.

Reasons:

- Spotify's developer policy explicitly prohibits using Spotify Platform content to train machine learning or AI models
- the official `Get Track's Audio Features` endpoint is deprecated for new use cases

For that reason, the recommended course data design is:

- `FMA` for audio features
- `musiXmatch/MSD` for lyric features
- `Playlist2vec` for playlist behavior and graph analytics

## Recommended Derived Course Datasets

By the start of the semester, prepare the following processed teaching datasets:

- `pachamix_audio_core.parquet`
  From `FMA tracks.csv + features.csv (+ echonest.csv if desired)`, used for Weeks `1-7`
- `pachamix_lyrics_bow.parquet`
  From `musiXmatch/MSD`, used for lyric vectors and content-based recommendation experiments
- `pachamix_playlist_events.parquet`
  From `Playlist2vec` exports or `MPD`, one row per `(playlist, track)` interaction
- `pachamix_song_graph_edges.parquet`
  Weighted song-song co-occurrence graph derived from playlists
- `pachamix_small/`, `pachamix_medium/`, and `pachamix_spark/`
  Pre-sized classroom versions for local Python, Colab, and Spark demonstrations

For a detailed creation workflow, see [big_data_dataset_generation_plan.md](./big_data_dataset_generation_plan.md).

If you use the local toolkit in this workspace, the datasets can be generated through the `pachamix_data` CLI described in [README.md](./README.md). The implementation is intentionally `structured-data first`:

- metadata tables
- audio-feature tables
- lyrics token/count tables
- playlist interaction tables
- graph edge tables

It does **not** rely on `mp3` files or waveform processing during the course dataset build process.

---

## Week-by-Week Plan

### Week 1. Introduction to Big Data, Advanced Analytics, and Data Science

**Theory (2 hours)**

- Big Data as the computational substrate of modern analytics
- Relationship between `data science`, `advanced analytics`, `machine learning`, and `artificial intelligence`
- Types of analytics: descriptive, diagnostic, predictive, and prescriptive
- The `5Vs` of Big Data and why classical single-machine workflows fail at scale
- Industrial motivation: recommendation, fraud detection, ranking, forecasting, and behavioral analytics

**Mathematical verification focus**

- Order-of-growth analysis for storage and computation
- Basic throughput and latency calculations
- Computational feasibility analysis: number of records, number of features, memory footprint, and transfer cost
- Formal distinction between data size, model complexity, and algorithmic complexity

**Practice/Lab (2 hours)**

- Environment setup in Python, Colab, and Kaggle
- Exploratory analysis of a real dataset
- First technical exercise: characterize the problem as descriptive, predictive, or prescriptive
- Quick estimation task: determine whether the dataset can be processed on a laptop or requires distributed tooling

**Expected learning outcome**

Students distinguish Big Data from general data analysis, place machine learning inside the broader analytics workflow, and justify computational needs quantitatively.

---

### Week 2. Machine Learning Foundations: Supervised and Unsupervised Learning

**Theory (2 hours)**

- What it means for a machine to learn from data
- Supervised learning: classification and regression
- Unsupervised learning: clustering, dimensionality reduction, and association patterns
- Learning pipeline: data, features, objective function, training, validation, and inference
- Role of Big Data platforms such as Hadoop and Spark in large-scale learning workflows

**Mathematical verification focus**

- Objective functions and loss functions
- Regression loss: mean squared error
- Classification loss and decision boundaries at a conceptual level
- Overfitting, generalization, and train/validation/test separation
- Formal comparison between optimization in supervised and unsupervised settings

**Practice/Lab (2 hours)**

- Compare a simple supervised problem and a simple unsupervised problem in Python
- Build a first end-to-end notebook: preprocessing, training, and evaluation
- Discuss what changes when the same workflow must scale to millions of examples

**Expected learning outcome**

Students classify learning problems correctly, interpret their objective functions, and understand where Big Data infrastructure enters the workflow.

---

### Week 3. The Curse of Dimensionality: Geometry, Distance, and Sample Complexity

**Theory (2 hours)**

- High-dimensional feature spaces in text, images, recommender systems, and behavioral data
- Sparsity and distance concentration
- Why nearest-neighbor intuition degrades in high dimension
- Effects on prediction, clustering, similarity search, and generalization

**Mathematical verification focus**

- Volume comparison between the `d`-dimensional hypercube and the `d`-dimensional hypersphere
- Distance concentration and contrast loss
- Basic sample complexity intuition as dimension grows
- Why pairwise distances become less informative

**Practice/Lab (2 hours)**

- Simulate distance concentration numerically
- Compare nearest and farthest neighbor distances as dimension increases
- Analyze a sparse high-dimensional dataset and observe practical failure modes

**Expected learning outcome**

Students explain the curse of dimensionality mathematically and identify its impact on machine learning performance.

---

### Week 4. Linear Dimensionality Reduction I: PCA and the Geometry of Variance

**Theory (2 hours)**

- Why dimensionality reduction is needed
- Covariance matrix, variance, correlation, and orthogonal projections
- Principal Component Analysis as a variance-maximizing projection
- Geometric interpretation of principal directions

**Mathematical verification focus**

- Derivation of PCA as a constrained optimization problem
- Maximization of projected variance under the unit-norm constraint
- Emergence of the eigenvalue problem `Σw = λw`
- Explained variance as an ordered spectral decomposition

**Practice/Lab (2 hours)**

- Compute covariance matrices from data
- Implement PCA step by step in Python
- Visualize the effect of projection onto the first two principal components

**Expected learning outcome**

Students derive PCA from first principles and explain why eigenvectors of the covariance matrix define optimal linear directions.

---

### Week 5. Linear and Nonlinear Dimensionality Reduction II: SVD, t-SNE, and Neighbor-Preserving Embeddings

**Theory (2 hours)**

- Singular Value Decomposition as a matrix factorization framework
- Relationship between `PCA` and `SVD`
- `t-SNE` as a neighborhood-preserving visualization method
- Brief comparison with alternative methods such as random projections or `UMAP`
- When dimensionality reduction is appropriate for compression, denoising, visualization, or downstream learning

**Mathematical verification focus**

- SVD factorization and low-rank approximation
- Connection between singular values and explained energy
- Reconstruction error under truncated decompositions
- Probabilistic neighborhood preservation in `t-SNE`
- Technical caveat: `t-SNE` is excellent for visualization, but it is not usually the first choice for production-time feature reduction at scale

**Practice/Lab (2 hours)**

- Apply PCA and SVD to the same dataset and compare reconstructions
- Use `t-SNE` for 2D visualization of high-dimensional data
- Compare linear and nonlinear embeddings in terms of interpretability and stability

**Expected learning outcome**

Students distinguish between compression-oriented and visualization-oriented dimensionality reduction methods and justify their use mathematically.

---

### Week 6. Clustering I: K-means and Prototype-Based Clustering

**Theory (2 hours)**

- Clustering as unsupervised structure discovery
- K-means objective and geometric intuition
- Lloyd’s algorithm: assignment step and centroid update step
- Initialization, local minima, and sensitivity to outliers
- Large-scale variants such as mini-batch K-means

**Mathematical verification focus**

- Derivation of the sum of squared errors objective
- Proof that each Lloyd step does not increase the objective
- Interpretation of centroids as minimizers of within-cluster squared distance
- Within-cluster variance decomposition

**Practice/Lab (2 hours)**

- Implement K-means from scratch and with a library
- Compare several values of `k`
- Study the effect of initialization and scaling on clustering output

**Expected learning outcome**

Students derive the K-means algorithm, implement it correctly, and interpret both its strengths and its failure modes.

---

### Week 7. Clustering II: DBSCAN, Density-Based Reasoning, and Cluster Validation

**Theory (2 hours)**

- Limitations of centroid-based clustering
- Density-based clustering with `DBSCAN`
- Core points, border points, and noise points
- Comparison between `K-means` and `DBSCAN`
- Cluster validation and model selection

**Mathematical verification focus**

- Density-connectivity and reachability
- Role of `epsilon` and `minPts`
- Silhouette score, Davies-Bouldin index, and qualitative validation under arbitrary-shaped clusters
- Formal comparison of assumptions made by K-means and DBSCAN

**Practice/Lab (2 hours)**

- Apply `K-means` and `DBSCAN` to the same dataset
- Detect outliers and non-spherical structures
- Validate cluster quality quantitatively and visually

**Expected learning outcome**

Students select an appropriate clustering method based on data geometry and justify the decision mathematically.

---

### Week 8. Recommendation Systems I: Content-Based Recommendation

**Theory (2 hours)**

- Recommendation as a ranking and personalization problem
- Content-based recommendation using item attributes and user profiles
- Vector-space representations for items and users
- Similarity-driven retrieval and ranking

**Mathematical verification focus**

- Cosine similarity, dot product, and normalized similarity
- Feature weighting schemes such as `TF-IDF`
- Scoring functions for ranking candidate items
- Formal limitations of pure content-based systems: overspecialization and feature dependence

**Practice/Lab (2 hours)**

- Build a basic content-based recommender
- Represent items with features and derive user profiles
- Evaluate top-`k` recommendation quality with simple ranking metrics

**Expected learning outcome**

Students implement a content-based recommender and explain the mathematical role of vector representations and similarity measures.

---

### Week 9. Recommendation Systems II: User-Based and Item-Based Collaborative Filtering

**Theory (2 hours)**

- Collaborative filtering from user-item interactions
- User-based and item-based neighborhood models
- Sparse rating matrices and implicit feedback
- Cold-start and sparsity problems

**Mathematical verification focus**

- Cosine similarity and Pearson correlation
- Weighted average prediction formulas
- Reliability of similarity estimates under sparsity
- Bias correction and baseline predictors

**Practice/Lab (2 hours)**

- Build a user-based or item-based recommender
- Evaluate predictions using `RMSE` and `MAE`
- Compare user-based and item-based behavior on sparse data

**Expected learning outcome**

Students implement a neighborhood-based recommender and justify similarity and prediction choices mathematically.

---

### Week 10. Recommendation Systems III: Hybrid Models and Matrix Factorization

**Theory (2 hours)**

- Hybrid recommendation strategies: combining content signals and collaborative signals
- Latent factor models and matrix factorization
- Low-rank structure in user-item matrices
- Regularization, overfitting, and scalability
- Why mixed algorithms often outperform purely content-based or purely neighborhood-based approaches

**Mathematical verification focus**

- Derivation of the regularized matrix factorization objective
- Gradient updates for stochastic gradient descent
- Interpretation of matrix factorization as low-rank approximation with missing data
- Comparison between neighborhood methods and latent-factor methods

**Practice/Lab (2 hours)**

- Implement a simple latent-factor recommender
- Compare content-based, user-based, and hybrid/matrix-factorization approaches
- Analyze convergence and regularization effects

**Expected learning outcome**

Students explain why hybrid recommendation is often the most practical solution and derive a matrix factorization model from its optimization objective.

---

### Week 11. Graph Analytics I: Graph Representation, Centrality, and Random Walks

**Theory (2 hours)**

- Graphs in Big Data: web graphs, social graphs, interaction graphs
- Directed graphs and adjacency matrices
- Degree, path, connectivity, and centrality
- Random walk intuition as preparation for ranking on graphs

**Mathematical verification focus**

- Stochastic matrices and Markov chains
- Stationary distribution concept
- Transition probabilities on directed graphs
- Interpretation of graph traversal as linear algebra over adjacency structures

**Practice/Lab (2 hours)**

- Build a small directed graph
- Compute centrality measures and simple random walks
- Compare graph-based summaries on a small network dataset

**Expected learning outcome**

Students move comfortably between graph-theoretic, probabilistic, and matrix-based views of network data.

---

### Week 12. Graph Analytics II: PageRank and Large-Scale Graph Ranking

**Theory (2 hours)**

- PageRank as importance propagation on a graph
- Damping factor and teleportation
- Dangling nodes and reducibility issues
- Power iteration method
- Large-scale graph processing considerations

**Mathematical verification focus**

- Derivation of the PageRank fixed-point equation
- Why damping ensures existence and uniqueness of the ranking vector
- Convergence intuition for power iteration
- Interpretation of PageRank as the dominant eigenvector of a modified transition matrix

**Practice/Lab (2 hours)**

- Implement PageRank on a larger graph dataset
- Analyze the effect of the damping factor
- Measure convergence speed and ranking stability

**Expected learning outcome**

Students justify the convergence behavior of PageRank and interpret the role of damping in both theory and practice.

---

### Week 13. Deployment I: From Analytical Notebook to Big Data Pipeline

**Theory (2 hours)**

- Why prototypes fail in production
- Batch pipelines versus streaming pipelines
- Data preprocessing pipelines, feature persistence, and reproducibility
- Model packaging, APIs, and scheduled workflows
- Introduction to deployment with Spark jobs, cloud notebooks, and service-oriented inference

**Mathematical verification focus**

- Latency, throughput, and memory as engineering constraints
- Offline versus online evaluation
- Stability, drift, and reproducibility as measurable system properties
- Cost-performance tradeoffs in large-scale pipelines

**Practice/Lab (2 hours)**

- Convert one prior notebook into a reproducible pipeline
- Define inputs, outputs, artifacts, and evaluation checkpoints
- Prepare a minimal deployment-ready workflow

**Expected learning outcome**

Students understand that a mathematically correct model is not enough, and they can structure a Big Data workflow for reproducible execution.

---

### Week 14. Deployment II: Serving, Monitoring, and Technical Decision-Making

**Theory (2 hours)**

- Serving predictions or recommendations in production
- Monitoring model quality, data drift, and system health
- Reproducibility, fairness, explainability, and responsible deployment
- Comparative analysis of the course methods from an operational perspective
- Translating model outputs into product or business decisions

**Mathematical verification focus**

- Comparison of objective functions across dimensionality reduction, clustering, recommendation, and graph ranking
- Error propagation and uncertainty interpretation in deployed systems
- Confidence intervals, repeated-run variability, and monitoring thresholds
- Model selection under operational constraints

**Practice/Lab (2 hours)**

- Capstone integration exercise
- Students package one analytical method into a simplified production scenario
- Short technical defense centered on mathematical justification, scalability, and deployability

**Expected learning outcome**

Students integrate analytical, mathematical, and systems perspectives and defend end-to-end methodological decisions with technical rigor.

---

## Suggested Assessment Alignment with the Syllabus

To remain consistent with the syllabus evaluation structure, the following alignment is recommended:

- `TB1` in Week 3: Big Data foundations, advanced analytics, learning paradigms, and the curse of dimensionality
- `TB2` in Week 5: PCA, SVD, and dimensionality reduction methods
- `TP1` in Week 7: clustering with K-means and DBSCAN
- `EA1` in Week 8: partial exam covering Weeks 1 to 7
- `TB3` in Week 10: recommendation systems, including content-based, collaborative, and hybrid approaches
- `TB4` in Week 12: graph analytics and PageRank
- `DD1` in Week 15: performance evaluation based on project presentation
- `TF1` in Week 15: final project submission
- `EB1` in Week 16: final examination with emphasis on mathematical justification and applied reasoning

---

## Recommended Teaching Principle

For each week, structure the session as follows:

1. `Theoretical block`
   - Formal definition of the problem
   - Mathematical model or derivation
   - Interpretation of assumptions and limitations

2. `Practical block`
   - Implementation in Python
   - Empirical verification with data
   - Interpretation of outputs in a real-world context

This ensures the course remains technically robust, mathematically grounded, and professionally applicable.
