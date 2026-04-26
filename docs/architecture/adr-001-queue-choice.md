# ADR-001: Queue technology selection (RQ vs Celery)

## Status
Accepted

## Context

The system requires asynchronous background processing for:
- fetching training data from Strava API
- handling large sync operations (onboarding + historical data backfill)
- processing data in batches under external API rate limits

The system is expected to handle:
- moderate workload (hundreds to low thousands of jobs per batch)
- strict external API rate limits (Strava API)
- retry and backoff handling
- separation between API layer and background processing

I need a queue system that is simple to implement, easy to operate locally, and sufficient for the MVP stage.

---

## Options considered

### 1. Celery
Pros:
- advanced scheduling capabilities
- built-in retry mechanisms
- robust ecosystem
- production proven at scale

Cons:
- higher complexity
- more configuration overhead (brokers, workers, routing)
- steeper learning curve
- unnecessary overhead for current MVP scope

---

### 2. RQ (Redis Queue)
Pros:
- minimal setup (Redis + Python)
- simple mental model (function-based jobs)
- fast development speed
- easy local development with Docker
- sufficient for MVP-level workloads

Cons:
- no built-in advanced scheduling
- limited retry/routing features (must be implemented manually)
- no native priority system (requires multiple queues or custom logic)

Jobs are defined as Python functions executed by worker processes consuming Redis queues.

---

## Decision

I chose **RQ (Redis Queue)** as the job processing system for the MVP.

---

## Rationale

RQ is sufficient because:
- workload is not high-throughput
- external API (Strava) is the main bottleneck, not internal queue processing
- simplicity is prioritized over advanced orchestration
- missing features (priority, retry, rate limiting) can be implemented at application level

I explicitly accept that:
- priority handling will be implemented via separate queues (high / low)
- retry logic will be implemented in worker code
- rate limiting will be implemented as a custom mechanism (e.g. Redis-based limiter)

---

## Consequences

### Positive:
- faster MVP development
- lower system complexity
- easier debugging and local development
- clear separation of concerns (API → queue → worker → DB)

### Negative:
- manual implementation of features commonly provided by Celery
- potential need for migration if system scales significantly
- more responsibility in worker logic (retry, rate limiting)

---

## Future considerations

If system complexity increases (e.g. multi-region processing, high throughput, complex scheduling), I may consider migrating to:
- Celery
- or distributed task systems (e.g. Temporal, Airflow for pipelines)

For now, this is explicitly out of scope.