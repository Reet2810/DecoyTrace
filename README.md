# DecoyTrace

**DecoyTrace** is a honeytoken-based attack detection and response system designed to detect unauthorized interactions with decoy resources and support security investigation and response.

## Project Overview

The overall DecoyTrace workflow is:

**Generate Honeytokens → Deploy → Detect Interaction → Generate Alert → Correlate Related Activity → Analyze Risk → SOC/Incident Response Containment**

The project is being developed incrementally, with each phase focusing on a specific part of this workflow.

## Current Phase — Phase 5: Risk Scoring

DecoyTrace is currently in **Phase 5 — Risk Scoring**.

The goal of this phase is to evaluate correlated security activity and assign a risk level based on characteristics of the observed activity.

Phase 5 is currently **in development**. The initial risk-scoring design uses four activity characteristics:

* Number of Events
* Number of Unique Honeytokens
* Token Type
* Token Sensitivity

The planned scoring approach is **weighted and deterministic**, with individual feature contributions combined to produce an explainable risk score.

The exact feature weights, score range, and risk-level thresholds are still being designed and will be documented after they are finalized, implemented, and tested.

## Project Status

| Phase    | Description                      | Status            |
| -------- | -------------------------------- | ----------------- |
| Phase 1  | Proof of Concept                 | ✅ Complete        |
| Phase 2  | Persistent Honeytoken Management | ✅ Complete        |
| Phase 3A | Attacker Simulation              | ✅ Complete        |
| Phase 3B | Kali/Docker Attacker Environment | ⏸️ Deferred       |
| Phase 4  | Event Correlation                | ✅ Complete        |
| Phase 5  | Risk Scoring                     | 🚧 In Development |
| Phase 6  | Response & Containment           | 🔜 Planned        |
| Phase 7  | Cloud Security Integration       | 🔜 Planned        |

### Phase 1 — Proof of Concept

Implemented and tested:

* Unique decoy URL generation
* Decoy interaction detection
* IP address, User-Agent, and timestamp collection
* SQLite-based event storage
* Invalid token rejection
* Security alert generation

### Phase 2 — Persistent Honeytoken Management

Implemented and tested:

* Persistent honeytoken storage
* Unique token identification
* Token creation timestamps
* Token status tracking
* Triggered token state

### Phase 3A — Attacker Simulation

Implemented and tested:

* Reconnaissance simulation
* Resource discovery
* File inspection
* Credential-related keyword detection
* Honeytoken extraction
* Simulated interaction with the DecoyTrace endpoint
* Event persistence and alert generation

### Phase 3B — Kali/Docker Attacker Environment

A dedicated Kali/Docker attacker environment was considered for attacker simulation but is currently **deferred**.

### Phase 4 — Event Correlation

Implemented and tested:

* Chronological security event retrieval
* Time-based event correlation
* A **3-minute correlation window**
* Grouping of related events into attacker activity
* Identification of isolated or unrelated events
* Activity context including event count, source IP, start time, end time, duration, and event IDs

Phase 4 extends DecoyTrace beyond individual event detection by identifying security events that may belong to the same attacker activity sequence.

### Phase 5 — Risk Scoring

**Status: In Development**

The objective of Phase 5 is to evaluate correlated attacker activity and assign a risk level based on relevant characteristics of the observed activity.

The initial scoring features are:

1. **Number of Events** — represents the intensity of activity.
2. **Number of Unique Honeytokens** — represents the breadth of interaction across decoy resources.
3. **Token Type** — represents what the honeytoken represents, such as a generic, credential, or configuration resource.
4. **Token Sensitivity** — represents the relative importance of the accessed honeytoken, such as low, medium, or high sensitivity.

The planned scoring model is **weighted and deterministic**. Individual feature contributions will be combined to produce a transparent risk score that can be explained in terms of the observed activity.

The exact weights, score range, and risk-level thresholds are still being designed.

Implementation details will be added as the risk-scoring functionality is developed and verified.

## Architecture

The current DecoyTrace detection pipeline is:

```text
Honeytoken Generation
        ↓
Honeytoken Deployment
        ↓
Interaction Detection
        ↓
Event Logging
        ↓
Alert Generation
        ↓
Event Correlation
        ↓
Risk Scoring
        ↓
Response / Containment
```

The architecture will evolve as additional detection, analysis, response, and cloud capabilities are implemented.

## Repository Structure

```text
DecoyTrace/
├── .gitignore
├── README.md
├── app.py
├── correlation.py
├── view_db.py
├── attacker_lab/
│   └── ...
└── ...
```

The repository structure will evolve as development progresses.

## Planned Development

Future phases will expand DecoyTrace toward a more complete security monitoring and response platform.

Planned areas include:

* Risk-based prioritization of detected activity
* Security response and containment mechanisms
* Additional attacker simulation environments
* Cloud security integration
* Cloud telemetry integration
* Further SOC-oriented investigation and response capabilities

Features will be documented here only after they are implemented and tested.

## Disclaimer

DecoyTrace is being developed as a cybersecurity project for learning, research, and controlled testing. Any testing involving deceptive resources or attack detection should be performed only in environments where appropriate authorization has been obtained.
