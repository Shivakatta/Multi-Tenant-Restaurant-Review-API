## Multi-Tenant Restaurant Review API

A scalable backend system that enables multiple restaurants (tenants) to collect, store, and analyze customer feedback with strict data isolation and feature-based access control.

---

## Overview

This project implements a **multi-tenant architecture** where each restaurant operates independently with isolated data storage. The system supports **feature tiers** (basic vs premium), including optional sentiment analysis and advanced insights.

Key capabilities:

* Tenant-based data isolation
* Feature flag system
* Mock AWS services (DynamoDB, S3)
* Sentiment analysis integration
* REST-like API handler logic
* Comprehensive unit and integration testing

---

##  Architecture

```
POST /api/feedback
  → Tenant Resolution (API key)
  → Feature Check (sentiment enabled?)
  → Sentiment Analysis (optional)
  → Store in DynamoDB (tenant-scoped)
  → Return response

GET /api/restaurants/{tenant_id}/insights
  → Fetch tenant feedback
  → Compute analytics
  → Return insights
```

---

##  Project Structure

```
multi-tenant-restaurant-feedback/
├── src/
│   ├── api/               # API orchestration logic
│   ├── models/            # Data models (Tenant, Feedback)
│   ├── storage/           # Mock DynamoDB & S3
│   ├── external/          # Sentiment service
│   └── utils/             # Logger & exceptions
├── tests/                 # Unit & integration tests
├── config/                # Tenant configuration
├── README.md
├── requirements.txt
└── .gitignore
```

---

##  Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd multi-tenant-restaurant-feedback
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

##  Running Tests

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

**Coverage Target:**

* Unit tests: ≥ 90%
* Overall: ≥ 80%

---

##  Usage Example

```python
from src.api.feedback_handler import FeedbackHandler
from src.storage.dynamodb_client import DynamoDBClient
from src.storage.s3_client import S3Client
from src.external.sentiment_service import SentimentService

handler = FeedbackHandler(
    DynamoDBClient(),
    S3Client(),
    SentimentService()
)

result = handler.submit_feedback(
    api_key="pk_pizza_abc123",
    customer_name="John Doe",
    rating=5,
    comment="Amazing pizza!"
)

print(result)
```

### Example Response

```json
{
  "feedback_id": "uuid",
  "tenant_id": "pizza-palace-123",
  "rating": 5,
  "sentiment": {
    "score": 0.85,
    "label": "positive"
  },
  "created_at": "2026-02-22T10:00:00Z",
  "message": "Thank you for your feedback!"
}
```

---

##  Insights Example

```python
insights = handler.get_restaurant_insights("pk_pizza_abc123")
print(insights)
```

```json
{
  "tenant_id": "pizza-palace-123",
  "restaurant_name": "Pizza Palace",
  "total_feedback": 10,
  "average_rating": 4.3,
  "rating_distribution": {
    "5": 5,
    "4": 3,
    "3": 1,
    "2": 1,
    "1": 0
  },
  "sentiment_summary": {
    "average_score": 0.6,
    "positive_count": 6,
    "neutral_count": 2,
    "negative_count": 2
  }
}
```

---

##  Architecture Decisions

### 1. Multi-Tenant Isolation

* Data is stored as:

  ```python
  { tenant_id: [feedback_items] }
  ```
* Ensures **strict isolation**
* No cross-tenant data leakage possible

---

### 2. Dependency Injection

* All services (DB, S3, sentiment) are injected into the handler
* Benefits:

  * Easy testing (mocking)
  * Loose coupling
  * Better maintainability

---

### 3. Feature Flags

* Tenant features defined in config:

  ```json
  "features": {
    "sentiment_analysis": true
  }
  ```
* Enables:

  * Tier-based functionality
  * Easy future feature expansion

---

### 4. Mock AWS Services

* DynamoDB → in-memory dictionary
* S3 → JSON storage in memory

**Why?**

* No external dependencies
* Faster tests
* Simulates real-world patterns

---

### 5. Error Handling Strategy

* Validation errors → user-facing exceptions
* External failures → graceful fallback
* Sentiment API failure → does NOT block feedback submission

---

##  Trade-offs

| Decision           | Trade-off                         |
| ------------------ | --------------------------------- |
| In-memory DB       | Not persistent but fast & simple  |
| Mock sentiment API | Not accurate but testable         |
| No real HTTP API   | Simpler scope, faster development |
| No caching         | Easier logic but less optimized   |

---

##  Testing Strategy

### Covered Areas:

* Tenant isolation
* Data validation
* Sentiment logic
* API flow (integration tests)
* Edge cases (invalid input, empty data)

### Tools:

* `pytest`
* Mocking (`monkeypatch`)

---

##  Git Workflow

* Feature branches used for development
* Clean commit history with meaningful messages
* Merge conflicts resolved manually

Example:

```
feat: implement tenant-isolated DynamoDB client
feat: add sentiment analysis integration
feat: add structured logging
merge: resolve conflict between logging and error handling
```

---

##  Bonus Features (Optional)

* 1 Caching (tenant lookup)
* 2 Rate limiting per tenant
* 3 FastAPI/Flask server
* 4CI/CD pipeline

---

##  Future Improvements

* Replace mock DB with real DynamoDB
* Add authentication middleware
* Add pagination for feedback
* Implement real sentiment API
* Add dashboard UI

---

##  Assumptions

* API keys are trusted and secure
* In-memory storage is acceptable for this exercise
* Sentiment analysis is optional per tenant

---

##  Conclusion

This project demonstrates:

* Multi-tenant system design
* Clean architecture with separation of concerns
* Robust testing practices
* Real-world backend engineering patterns

---

##  Submission

* GitHub repository link
* Test coverage report
* Git history (`git log --oneline --graph`)

---

