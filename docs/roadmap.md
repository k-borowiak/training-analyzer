# Roadmap

## 🎯 Goal

Build a backend system for collecting, processing, and analyzing training data from Strava using asynchronous jobs and an AI-based insights layer.

The system is designed as a modular pipeline:
- API layer (FastAPI)
- async processing (queue + worker)
- data storage (PostgreSQL)
- analysis layer (AI service)

---

## 📍 Current status

The project is in the early development phase.

The repository already includes:
- initial documentation,
- architecture draft,
- and early project structure.

The next step is to implement the first end-to-end working flow.

---

## 🧱 Phase 0 — Architecture & planning

**Goal:** define a clear system structure before implementation

- [x] Define high-level architecture
- [x] Identify core components (API, queue, worker, DB, AI service)
- [x] Decide on queue technology: **Redis + RQ**
- [x] Define MVP data model (users, tokens, activities)
- [x] Add architecture diagram
- [x] Add roadmap and documentation

---

## ⚙️ Phase 1 — Foundation

**Goal:** prepare a runnable local environment

- [ ] Initialize FastAPI application
- [ ] Add PostgreSQL integration
- [ ] Configure environment variables
- [ ] Set up Docker and docker-compose
- [ ] Add basic logging
- [ ] Run API and PostgreSQL together in local development

---

## 🔐 Phase 2 — Authentication (Strava OAuth)

**Goal:** connect a user account with Strava

- [ ] Implement OAuth redirect endpoint
- [ ] Handle callback and token exchange
- [ ] Store access and refresh tokens in PostgreSQL
- [ ] Create user model
- [ ] Implement token refresh logic

**Result:** user is connected and tokens are persisted

---

## 🔄 Phase 3 — Data ingestion (Worker)

**Goal:** fetch training data asynchronously

- [ ] Introduce job queue and worker runtime
- [ ] Implement worker process (separate runtime)
- [ ] Trigger sync job after authentication
- [ ] Fetch activities from Strava API
- [ ] Handle pagination and incremental sync
- [ ] Handle API rate limits
- [ ] Store raw activities in PostgreSQL
- [ ] Track sync state

**Result:** activities are fetched and stored in DB

---

## 🧮 Phase 4 — Processing layer

**Goal:** transform raw data into usable metrics

- [ ] Define the first derived training metrics
- [ ] Compute metrics from stored activities
- [ ] Store processed data in database
- [ ] Separate ingestion logic from processing logic
- [ ] Add job prioritization (sync vs processing)

**Result:** structured training data is available

---

## 🌐 Phase 5 — API layer

**Goal:** expose data to the user

- [ ] Implement `GET /activities`
- [ ] Add filtering (date, type, etc.)
- [ ] Implement `GET /metrics`
- [ ] Return sync status information
- [ ] Add validation and error handling

**Result:** user can query their data via API

---

## 🤖 Phase 6 — AI insights

**Goal:** generate higher-level training insights

- [ ] Implement AI service layer
- [ ] Add provider abstraction (external / local models)
- [ ] Build prompt generation based on metrics
- [ ] Generate basic training insights
- [ ] Store AI results in database
- [ ] Add caching and rate limiting

**Result:** data is enriched with AI-generated insights

---

## ☁️ Phase 7 — Deployment

**Goal:** run the system in a cloud environment

- [ ] Containerize API, worker, and DB
- [ ] Configure environment-based deployment
- [ ] Define the first AWS deployment approach
- [ ] Set up logging and monitoring
- [ ] Validate a minimal cloud deployment setup

**Result:** system runs outside local development

---

## 🚀 Future improvements

- [ ] Scheduled background sync
- [ ] Strava webhooks integration
- [ ] Multi-user support
- [ ] Advanced training metrics (FTP, zones, trends)
- [ ] Data reprocessing pipeline
- [ ] Frontend dashboard