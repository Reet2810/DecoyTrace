# DecoyTrace

**DecoyTrace** is a honeytoken-based attack detection and response system designed to detect unauthorized interactions with decoy resources and support security investigation and response.

## Project Overview

The overall DecoyTrace workflow is:

**Generate Honeytokens → Deploy → Detect Interaction → Generate Alert → Correlate Related Activity → Analyze Risk → SOC/Incident Response Containment**

The project is being developed incrementally, with each phase focusing on a specific part of this workflow.

## Current Phase — Phase 5: Risk Scoring

DecoyTrace is currently in **Phase 5 — Risk Scoring**.

Phase 5 evaluates correlated security activity and assigns an explainable risk score and risk level based on characteristics of the observed activity.

The finalized scoring model is **weighted and deterministic** and consists of three scoring components:

* Event Activity Score
* Honeytoken Diversity Score
* Resource Score

These components are combined to produce a final risk score from **0 to 100**, which is mapped to one of four risk levels:

* Low
* Medium
* High
* Critical

Phase 5 risk scoring has been implemented and integrated with the existing Phase 4 event correlation system.

## Project Status

| Phase    | Description                      | Status      |
| -------- | -------------------------------- | ----------- |
| Phase 1  | Proof of Concept                 | ✅ Complete  |
| Phase 2  | Persistent Honeytoken Management | ✅ Complete  |
| Phase 3A | Attacker Simulation              | ✅ Complete  |
| Phase 3B | Kali/Docker Attacker Environment | ⏸️ Deferred |
| Phase 4  | Event Correlation                | ✅ Complete  |
| Phase 5  | Risk Scoring                     | ✅ Complete  |
| Phase 6  | Response & Containment           | 🔜 Planned  |
| Phase 7  | Cloud Security Integration       | 🔜 Planned  |

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
* Activity context including:

  * Event count
  * Source IP
  * Start time
  * End time
  * Duration
  * Event IDs

Two events are considered related when they originate from the same source IP and occur within the defined 3-minute correlation window.

The correlation logic uses a continuous-chain approach to group related events into attacker activity sequences.

Phase 4 extends DecoyTrace beyond individual event detection by identifying security events that may belong to the same attacker activity sequence.

### Phase 5 — Risk Scoring

**Status: Complete**

The objective of Phase 5 is to evaluate correlated attacker activity and assign an explainable risk level.

The finalized scoring model uses three components.

#### 1. Event Activity Score — 20 points maximum

| Number of Events | Points |
| ---------------- | ------ |
| 1                | 4      |
| 2                | 6      |
| 3                | 8      |
| 4                | 10     |
| 5                | 12     |
| 6                | 14     |
| 7                | 16     |
| 8                | 18     |
| 9+               | 20     |

This score represents the intensity of activity within a correlated activity group.

#### 2. Honeytoken Diversity Score — 30 points maximum

| Unique Honeytokens | Points |
| ------------------ | ------ |
| 1                  | 6      |
| 2                  | 12     |
| 3                  | 18     |
| 4                  | 24     |
| 5+                 | 30     |

The score is based on the number of **unique honeytokens** involved in an activity, rather than the total number of events.

This represents the breadth of interaction across decoy resources.

#### 3. Resource Score — 50 points maximum

The resource score combines the honeytoken's type and sensitivity.

**Token Type Base Score**

| Token Type    | Base Score |
| ------------- | ---------- |
| Generic       | 10         |
| Configuration | 20         |
| Credential    | 30         |

**Sensitivity Modifier**

| Sensitivity | Modifier |
| ----------- | -------- |
| Low         | +0       |
| Medium      | +10      |
| High        | +20      |

Therefore:

**Resource Score = Token Type Base Score + Sensitivity Modifier**

If multiple honeytokens are involved in an activity, the **highest resource score** among those honeytokens is used.

The maximum resource score is **50**.

#### Final Risk Score

```text
Risk Score =
Event Activity Score
+ Honeytoken Diversity Score
+ Resource Score
```

Maximum possible score: **100**

#### Risk Levels

| Score  | Risk Level |
| ------ | ---------- |
| 0–24   | Low        |
| 25–49  | Medium     |
| 50–74  | High       |
| 75–100 | Critical   |

The scoring model is deterministic and explainable. It provides an assessment of observed activity and is not intended to represent a probability or proof of malicious intent.

### Phase 5 Integration

The Phase 5 scoring system is integrated with the Phase 4 correlation pipeline.

The current flow is:

```text
Security Events
      ↓
Event Correlation
      ↓
Correlated Activities
      ↓
Event Activity Score
      ↓
Honeytoken Diversity Score
      ↓
Resource Score
      ↓
Final Risk Score
      ↓
Risk Level
```

Each correlated activity can now be evaluated using:

* Event Activity Score
* Honeytoken Diversity Score
* Resource Score
* Final Risk Score
* Risk Level

The existing Phase 4 correlation logic remains responsible for generating the correlated activities, while the Phase 5 scoring logic evaluates those activities.

## Architecture

The current DecoyTrace detection and analysis pipeline is:

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

The architecture will evolve as additional response and cloud capabilities are implemented.

## Technology Stack

* Python 3.12.6
* Flask
* SQLite

## Token Metadata

Honeytokens currently maintain the following metadata in the SQLite database:

```text
id
token
created_at
status
type
sensitivity
```

Valid token types:

```text
generic
configuration
credential
```

Valid sensitivity levels:

```text
low
medium
high
```

All combinations of token type and sensitivity are independently valid.

For example:

```text
generic + low
generic + high
configuration + medium
credential + low
credential + high
```

The `/decoy` route supports token metadata through query parameters, for example:

```text
/decoy?type=credential&sensitivity=medium
```

The selected metadata is stored with the generated honeytoken and is later used by the Phase 5 resource scoring logic.

## Repository Structure

```text
DecoyTrace/

├── .gitignore
├── README.md
├── app.py
├── correlation.py
├── risk_scoring.py
├── view_db.py
├── attacker_lab/
│   └── ...
└── ...
```

### `correlation.py`

Contains the Phase 4 event correlation functionality, including:

* `are_events_related()`
* `create_activity_groups()`
* Event retrieval from SQLite
* Correlated activity generation
* Activity context generation

The existing correlation algorithm uses the 3-minute same-source-IP correlation logic.

### `risk_scoring.py`

Contains the Phase 5 risk-scoring functionality, including:

* `calculate_event_score(event_count)`
* `calculate_token_score(activity)`
* `calculate_resource_score(activity)`
* `calculate_risk_score(activity)`
* `get_risk_level(score)`

The resource scoring function retrieves token type and sensitivity from the SQLite `tokens` table.

## Planned Development

Future phases will expand DecoyTrace toward a more complete security monitoring and response platform.

Planned areas include:

* Risk-based prioritization of detected activity
* Security response and containment mechanisms
* Additional attacker simulation environments
* Cloud security integration
* Cloud telemetry integration
* SOC-oriented investigation and response capabilities
* Automated response mechanisms

Features will be documented here only after they are implemented and tested.

## Disclaimer

DecoyTrace is being developed as a cybersecurity project for learning, research, and controlled testing. Any testing involving deceptive resources or attack detection should be performed only in environments where appropriate authorization has been obtained.
