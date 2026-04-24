# Training Analyzer

## Overview

Training Analyzer is a backend system designed to collect, process, and analyze endurance training data from external fitness platforms.

The system focuses on building a scalable data pipeline that transforms raw activity data into meaningful performance metrics and contextual insights. It also includes an AI-powered analysis layer for generating higher-level interpretations of training load and athlete progression.

The architecture is provider-agnostic, starting with Strava as the initial data source, but designed to support additional fitness platforms in the future.

---

## Core Idea

The goal of this project is not only to store training data, but to build a complete processing pipeline:

* ingest raw activity data
* compute structured performance metrics
* analyze trends over time
* generate contextual insights using AI

---

## System Architecture

The system is built using a modular, event-driven architecture:

### 1. Data Ingestion Layer

* OAuth2 authentication with external fitness platforms
* Incremental synchronization of training data
* Historical backfill support (limited window)
* Raw data storage without early transformation

### 2. Processing Layer

* Computation of training metrics (load, intensity, trends)
* Rolling window analysis (short-term and long-term views)
* Background job processing with priority handling (HIGH / LOW)

### 3. Intelligence Layer (AI)

* AI-powered interpretation of processed training data
* Cost-aware usage of external AI providers
* Rate limiting and caching of generated insights
* Provider abstraction (e.g. Gemini, Groq)

---

## Data Flow

1. User registers and connects external fitness account via OAuth
2. System securely stores access tokens
3. Initial synchronization fetches last 42 days of activity data
4. Background jobs progressively backfill historical data (up to 1 year)
5. Raw activity data is stored in PostgreSQL
6. Processing layer computes training metrics
7. AI service generates insights based on processed data
8. Insights are cached and persisted for future retrieval

---

## Key Design Principles

* Separation of ingestion, processing, and analysis layers
* Asynchronous background processing via job system
* Priority-based task execution (onboarding vs backfill)
* Rate limit awareness for external APIs
* AI as an interpretation layer, not a core computation engine
* Cache-first approach for expensive operations

---

## Technology Stack

* FastAPI (API layer)
* PostgreSQL (data storage)
* Background worker system (job processing)
* External fitness APIs (e.g. Strava)
* External AI providers (Gemini, Groq or others)

---

## AI Integration

The AI layer is used to generate contextual insights from structured training data.

Key characteristics:

* AI does not process raw data directly
* Inputs are pre-aggregated metrics and summaries
* Requests are rate-limited to control costs
* Results are cached to avoid redundant calls
* Provider abstraction allows switching AI models

---

## Project Status

This project is currently in early design and implementation phase.

The primary focus is to establish a clean and scalable architecture before expanding functionality.

