# Semester Group Assignment Brief

## Title

Semester Project: Domain Discovery, Recommendation, and Graph Intelligence

## Purpose

This assignment is designed to run across the full 14-week cycle of the course.
It is not a single-model project.
It is a cumulative technical project that forces students to practice:

- data acquisition
- schema design
- feature engineering
- dimensionality reduction
- clustering
- recommendation or ranking
- graph analytics
- reproducible pipelines
- technical reporting and final defense

The project must be technical first.
The written report matters, but the strongest submissions will be judged by the quality of the data pipeline, the rigor of the experiments, and the reproducibility of the artifacts.

## Core Project Shape

Every team must build a project with the following layers:

1. `catalog layer`
- the main entity table
- examples: posts, profiles, recipes, products, songs, businesses, papers, events, courses

2. `feature layer`
- numeric, categorical, text, temporal, or graph-derived features

3. `interaction or co-occurrence layer`
- examples: clicks, ratings, saves, baskets, reviews, shared tags, co-mentions, follows, lists, sessions, playlists

4. `graph layer`
- examples: item-item, hashtag-hashtag, skill-skill, business-business, paper-paper, user-item projection, career transition graph

5. `pipeline layer`
- a reproducible build path from raw data to processed data to analysis artifacts

Projects that stop at basic supervised learning will be considered incomplete for this course.

## Allowed Project Tracks

Teams may choose one of the following:

### Track A: Public Dataset Project

Use one or more public datasets from Kaggle, government/open data portals, official research releases, or platform-sanctioned exports.

Examples:

- news recommendation
- local business analytics
- recipe recommendation
- niche e-commerce recommendation
- academic-paper intelligence
- event discovery
- book or game recommendation

### Track B: Build-Your-Own Dataset

Create a dataset from public websites or APIs, subject to legality and platform rules.
This track is strongly encouraged when the team wants a more original domain.

Examples:

- startup tools
- local cultural events
- podcast catalogs
- indie games
- open course catalogs
- scientific software libraries
- board game communities

### Track C: Instagram Content Intelligence

Use Instagram data only through approved means:

- data exports from consenting participants
- business or creator account analytics
- platform-approved API access

Suggested problem framing:

- cluster content styles
- analyze engagement patterns
- recommend hashtags, content themes, or posting strategies
- build hashtag or mention graphs

### Track D: LinkedIn Career and Skill Intelligence

Use LinkedIn data only through approved means:

- data exports from consenting participants
- page-admin analytics if the team has valid access
- approved API access where available

Suggested problem framing:

- normalize and cluster career paths
- build skill graphs
- rank skills, roles, or career transitions
- recommend skill-development directions or role families

### Track E: Cross-Platform Project

Combine multiple sources when the team can justify the match.

Examples:

- Instagram plus LinkedIn personal-brand analytics
- local-business reviews plus social media content
- publication metadata plus citation graph plus author skills

This track is harder and should only be approved if the team can explain the data alignment clearly.

## Strongly Recommended Project Types

The best fit for this course is a `discovery and recommendation system`.

That means the final output should answer questions such as:

- Which items are similar?
- Which items belong to the same latent segment?
- Which items should be recommended next?
- Which entities are central in the graph?
- Which changes in content or behavior are associated with better outcomes?

## Forbidden or Weak Project Choices

The following are not acceptable:

- Titanic
- Iris
- Penguins
- MNIST used as a standard teaching exercise
- any tiny classroom dataset with no meaningful engineering challenge
- any project with only one flat CSV and no pipeline
- any project with only screenshots and no reproducible code

The following are technically possible but weak for this course unless extended substantially:

- plain salary prediction with one table only
- plain house-price regression with one table only
- any project without either an interaction layer or a graph layer

## Team Size

Recommended team size:

- `3 to 5` students per team

Each team must assign at least these roles, even if one student covers more than one:

- data engineering lead
- modeling and evaluation lead
- reporting and presentation lead

## Dataset Rules

Every team must satisfy all of the following:

1. Use a dataset that is non-trivial in size, structure, or preprocessing difficulty.
2. Provide a data dictionary.
3. Document all source URLs and provenance.
4. Explain why the chosen dataset supports the second half of the course, not just the first half.
5. Avoid trivial benchmark datasets.
6. If the dataset is too large, define a justified working subset.
7. If multiple sources are combined, document the matching logic.

## Ethics and Platform Rules

These rules are mandatory.

### General

- No unauthorized scraping of private or access-controlled data.
- No use of personal data without clear participant consent.
- No redistribution of raw personal data collected from participants.
- Sensitive identifiers must be anonymized or hashed in processed artifacts unless explicit permission is documented.

### Instagram

Instagram-based projects are allowed only when the data comes from:

- consenting participant exports
- consenting business or creator account analytics
- platform-approved API access

Teams must not scrape private profiles or bypass platform restrictions.

### LinkedIn

LinkedIn-based projects are allowed only when the data comes from:

- consenting participant exports
- page-admin data with valid access
- platform-approved API access

Teams must not scrape personal profiles without permission.

### Required Ethics Note

Each milestone must include a short section named `Ethics and Access Note` that states:

- where the data came from
- why the team is allowed to use it
- what personal-data risks exist
- how those risks were reduced

## Required Repository Structure

Each team repository must include a structure equivalent to this:

```text
project/
  data/
    raw/
    interim/
    processed/
  notebooks/
  src/
  reports/
  artifacts/
  README.md
  requirements.txt or pyproject.toml
```

The exact names may vary, but the separation between raw, processed, code, and reports must be explicit.

## Required Technical Artifacts

Each team must produce:

1. one ingestion script or pipeline
2. one processed dataset directory
3. one data dictionary
4. one feature-building script or notebook
5. one evaluation script
6. one graph-construction script
7. one runbook explaining how to reproduce the outputs
8. one final demo artifact
- this may be a notebook, CLI, small dashboard, or small API

Notebook-only projects are not enough.
At least part of the workflow must be executable from scripts or commands.

## Mandatory Milestones

The project has partial deliverables in Weeks 3, 5, 7, 10, 12, and 14.

### Week 3: Dataset Charter and Processed Dataset V1

Objective:

- prove that the team has a valid domain, a valid data source, and a reproducible first dataset build

Required deliverables:

1. one project proposal
- domain
- problem statement
- expected product question
- why the dataset is suitable for the course

2. one source inventory
- source URLs
- licenses or access conditions
- raw file formats
- estimated size

3. one schema draft
- entity tables
- keys
- expected joins

4. one processed dataset V1
- at least one cleaned table saved to disk

5. one data dictionary draft

6. one scale analysis
- rows
- columns
- missingness
- sparsity or memory estimate

7. one ethics and access note

Technical expectation:

- the ingestion must run from a documented command

### Week 5: Representation and Dimensionality Report

Objective:

- move from raw tables to meaningful representations

Required deliverables:

1. one feature matrix or matrices
- numeric
- text
- categorical encoding
- temporal features if relevant

2. one dimensionality-reduction report
- PCA and/or SVD
- optional t-SNE for visualization

3. one comparison table
- explained variance or retained energy
- reconstruction error where appropriate

4. one visualization set
- at least two meaningful plots

5. one short technical interpretation
- what was learned about dimensionality, redundancy, or feature quality

Technical expectation:

- the feature-building pipeline must be reproducible

### Week 7: Clustering and Validation Report

Objective:

- segment the domain and validate whether the segmentation is meaningful

Required deliverables:

1. one clustering experiment with K-means
2. one clustering experiment with DBSCAN or another justified density method
3. one validation table
- silhouette
- inertia or density-related metrics
- interpretation limits

4. one cluster-profile analysis
- what characterizes the clusters

5. one failure analysis
- what did not cluster well and why

Technical expectation:

- the team must show parameter sweeps, not only one hand-picked result

### Week 10: Recommendation, Ranking, or Predictive Decision Engine

Objective:

- connect the technical work to a decision or ranking task

Required deliverables:

1. one baseline system
- content-based, popularity-based, or another simple baseline

2. one stronger system
- collaborative filtering
- matrix factorization
- hybrid ranking
- predictive ranking
- or another justified advanced model

3. one offline evaluation report
- metrics
- candidate-pool definition
- comparison against baselines

4. one error analysis
- strong cases
- failure cases

5. one explanation of whether the project is:
- recommendation
- ranking
- prediction
- segmentation feeding ranking

Technical expectation:

- teams must explain their evaluation protocol clearly
- if they claim a hybrid system, they must document the data alignment

### Week 12: Graph Analytics and Centrality Report

Objective:

- formalize the graph induced by the domain and use it for structural analysis

Required deliverables:

1. one graph definition
- nodes
- edges
- weights
- directionality

2. one graph-construction script

3. one graph report
- connected components
- degree or weighted degree
- centrality or PageRank

4. one comparison section
- graph ranking versus popularity or model-based ranking

5. one interpretation note
- what graph structure means in the domain

Technical expectation:

- graph definition choices must be justified

### Week 14: Final Integrated Delivery and Defense

Objective:

- deliver the complete system and defend its coherence

Required deliverables:

1. one final technical report
2. one reproducible repository
3. one runbook
4. one final presentation
5. one final demo artifact
6. one monitoring or operationalization plan
7. one limitations and future-work section

Technical expectation:

- the project must run from documented steps
- the team must show final processed artifacts and outputs, not only slides

## Final Report Structure

The final report should contain:

1. problem statement
2. domain context
3. dataset sources and access conditions
4. schema and data dictionary
5. preprocessing and feature engineering
6. dimensionality and representation analysis
7. clustering analysis
8. recommendation or ranking system
9. graph analytics
10. evaluation protocol
11. pipeline and reproducibility
12. ethics and limitations
13. final conclusions


## Detailed Evaluation Criteria

### Data Engineering

The team will be evaluated on:

- correctness of ingestion
- schema clarity
- quality of processed data
- quality of data dictionary
- handling of missing values, duplicates, and joins

### Modeling and Analysis

The team will be evaluated on:

- representation quality
- parameter justification
- baseline comparisons
- metric rigor
- interpretation quality

### Graph and Advanced Layer

The team will be evaluated on:

- validity of graph construction
- correctness of centrality or PageRank analysis
- connection between graph results and product question

### Engineering and Reproducibility

The team will be evaluated on:

- repo structure
- clear commands
- saved artifacts
- rerunnable workflow
- evidence that the project does not rely on hidden notebook state

### Final Defense

The team will be evaluated on:

- coherence between objective, data, model, and evaluation
- clarity of technical decisions
- honesty about limitations
- quality of oral defense and technical answers

## Suggested Topic Proposals

These are strong examples, not an exhaustive list.

### Proposal 1: News Recommendation and Topic Graph

Build a system that:

- represents articles using text features
- models click behavior or reading behavior
- recommends articles
- builds an entity or topic graph

### Proposal 2: Local Business Discovery Engine

Build a system that:

- models businesses, reviews, categories, and neighborhoods
- clusters businesses
- recommends businesses
- builds business-business or category graphs

### Proposal 3: Recipe Recommendation and Ingredient Graph

Build a system that:

- represents recipes from ingredients and instructions
- clusters recipe styles
- recommends recipes
- builds an ingredient graph

### Proposal 4: Instagram Content Intelligence

Build a system that:

- represents posts and captions
- predicts or ranks engagement potential
- clusters content strategies
- builds hashtag or mention graphs

### Proposal 5: LinkedIn Career and Skill Intelligence

Build a system that:

- normalizes roles and skills
- clusters professional profiles or role families
- ranks important skills
- builds skill or career-transition graphs

### Proposal 6: Niche E-commerce Recommender

Build a system that:

- models products, metadata, reviews, and interactions
- clusters products
- recommends products
- builds product co-occurrence or co-purchase graphs

### Proposal 7: Academic Paper Discovery System

Build a system that:

- represents papers using titles, abstracts, topics, and citations
- clusters research themes
- recommends papers
- ranks papers, authors, or venues through graph methods

## Project Approval Rule

No project is approved until the instructor confirms that:

1. the dataset is non-trivial
2. the data source is allowed
3. the second-half course topics are feasible on the chosen data
4. the team has a credible build plan

Teams whose topic is too weak at Week 3 may be required to pivot.

## Minimum Technical Standard for Passing

To pass the project, a team must show all of the following:

- a real processed dataset
- at least one rigorous feature representation
- at least one clustering experiment
- at least one ranking or recommendation experiment
- at least one graph analysis
- a reproducible build path

If any of these layers is missing, the project may be graded as incomplete.

## Final Note to Students

Do not choose a project because it looks easy.
Choose a project whose data structure can survive the entire semester.

The right question is not:

> Can we train one model on this data?

The right question is:

> Can we build a coherent data product from ingestion to ranking to graph analysis to final defense?
