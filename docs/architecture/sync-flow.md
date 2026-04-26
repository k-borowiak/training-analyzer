# Sync Flow

This document describes how data flows through the system — from user onboarding to ongoing synchronization.

---

## 🧠 1. Initial onboarding flow

User flow:

User → Login via Strava (OAuth)
→ Redirect to FastAPI callback
→ Exchange code for tokens
→ Store tokens in database
→ Enqueue initial sync job
→ Worker fetches activities from Strava API
→ Store raw activities in PostgreSQL
→ Process activities into metrics
→ (optional) Generate AI insights

---

## 🔄 2. Subsequent sync

Triggered manually or automatically:

API request (manual trigger)
→ Enqueue sync job
→ Worker fetches new activities
→ Update raw data in DB
→ Recompute metrics if needed

---

## ⏳ 3. Future improvements

- Scheduled sync (cron / scheduler)
- Retry failed jobs
- Incremental sync based on sync_state
- API rate limit handling

---

## 📌 Notes

- FastAPI only triggers jobs
- Worker handles Strava API communication
- PostgreSQL stores raw + processed data
- AI layer is optional