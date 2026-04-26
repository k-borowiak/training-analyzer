# Data Model (High-Level)

Core entities in the system:

---

## users
- Application users
- Can connect external providers (e.g. Strava)

---

## provider_tokens
- OAuth tokens (access + refresh)
- Linked to user + provider
- Used for API authentication

---

## raw_activities
- Raw data from Strava
- Source of truth
- Immutable after ingestion

---

## metrics
- Derived data from activities
- Used for analysis & API queries
- Recomputable

---

## sync_state
- Tracks last sync timestamp
- Enables incremental sync
- Prevents duplicates

---

## ai_insights
- AI-generated summaries
- Optional layer
- Can be regenerated

---

## Relationships (high level)

User → provider_tokens  
User → raw_activities  
User → metrics  
User → sync_state  
User → ai_insights  

---

## Source of truth

- raw_activities → primary data
- metrics → derived data
- ai_insights → disposable layer