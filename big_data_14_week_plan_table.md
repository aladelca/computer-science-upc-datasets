# Big Data Course 14-Week Plan: Compact Table

This table is a compact, paste-ready version of the course plan derived from [UG-202520_1ACC0221-Big data.pdf](./UG-202520_1ACC0221-Big%20data.pdf).

Assumptions:

- `14 teaching weeks`
- `4 hours per week`
- `2 theoretical hours + 2 practical/laboratory hours per week`
- `Weeks 15 and 16 reserved for evaluation and final assessment`

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
