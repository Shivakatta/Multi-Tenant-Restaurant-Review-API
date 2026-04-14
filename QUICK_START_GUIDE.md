# Developer Exercise - Quick Start Guide

This guide will help you set up the coding exercise in under 10 minutes.

---

## Step 1: Create Project Structure (5 minutes)

Run these commands in your terminal:

```bash
# Create project folder
mkdir restaurant-review-api
cd restaurant-review-api

# Initialize Git
git init

# Create folder structure
mkdir -p src/api src/storage src/external src/models src/utils
mkdir -p tests/fixtures
mkdir -p config

# Create __init__.py files (for Python package structure)
touch src/__init__.py
touch src/api/__init__.py
touch src/storage/__init__.py
touch src/external/__init__.py
touch src/models/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py

# Create empty Python files
touch src/models/tenant.py
touch src/models/feedback.py
touch src/storage/dynamodb_client.py
touch src/storage/s3_client.py
touch src/external/sentiment_service.py
touch src/api/feedback_handler.py
touch src/utils/logger.py
touch src/utils/exceptions.py

# Create test files
touch tests/test_dynamodb_client.py
touch tests/test_sentiment_service.py
touch tests/test_feedback_handler.py

# Create config files
touch config/tenant_registry.json
touch README.md
touch requirements.txt
touch .gitignore
```

---

## Step 2: Create .gitignore File (1 minute)

Copy this content into `.gitignore`:

```
# Python
venv/
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Environment
.env
.env.local
```

---

## Step 3: Create requirements.txt (1 minute)

Copy this content into `requirements.txt`:

```
# Core dependencies
pytest>=7.4.0
pytest-cov>=4.1.0

# Optional - only if you want to use them
pydantic>=2.5.0        # For data models (alternative to dataclasses)
```

That's it! No external AWS libraries needed - you'll use in-memory mocks.

---

## Step 4: Set Up Python Environment (2 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 5: Verify Setup (1 minute)

Run this command to check everything is working:

```bash
pytest tests/ -v
```

You should see:

```
collected 0 items

==================== no tests ran in 0.03s ====================
```

Perfect! Now you're ready to start coding.

---

## Step 6: First Commit (< 1 minute)

```bash
git add .
git commit -m "chore: initial project structure"
```

---

## Development Workflow

### When implementing each part:

1. **Create a feature branch**
   ```bash
   git checkout -b feature/data-models
   ```

2. **Write the code**
   - Start with data models (easiest)
   - Then storage layer
   - Then external services
   - Finally, API handler

3. **Run tests frequently**
   ```bash
   pytest tests/ -v
   ```

4. **Commit your work**
   ```bash
   git add .
   git commit -m "feat: implement tenant data model"
   ```

5. **Merge to main**
   ```bash
   git checkout main
   git merge feature/data-models
   ```

---

## Running Tests with Coverage

Check how much of your code is tested:

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

This will show:
- Which lines of code are tested ✅
- Which lines are missing coverage ❌

Aim for **80%+ coverage**.

---

## Debugging Tips

### If pytest can't find your modules:

```bash
# Run from project root directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Mac/Linux
set PYTHONPATH=%PYTHONPATH%;%cd%         # Windows

pytest tests/ -v
```

### If imports are failing:

Make sure you have `__init__.py` in all folders:
```
src/
├── __init__.py          ← Must exist
├── api/
│   └── __init__.py      ← Must exist
├── models/
│   └── __init__.py      ← Must exist
```

### If tests are failing:

1. Read the error message carefully
2. Add print statements to see what's happening
3. Run a single test: `pytest tests/test_dynamodb_client.py::TestDynamoDBClient::test_save_and_retrieve_feedback -v`
4. Ask ChatGPT/Copilot for help

---

## Quick Reference: Common Commands

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_dynamodb_client.py -v

# Run specific test method
pytest tests/test_dynamodb_client.py::TestDynamoDBClient::test_tenant_isolation -v

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html

# Open coverage report in browser
open htmlcov/index.html  # Mac
start htmlcov/index.html  # Windows

# Check Git status
git status

# View Git history
git log --oneline --graph

# Create new branch
git checkout -b feature/name

# Merge branch
git checkout main
git merge feature/name
```

---

## What to Build First?

**Recommended Order (4-6 hours):**

### Hour 1: Data Models (Part 1)
- ✅ `src/models/tenant.py`
- ✅ `src/models/feedback.py`
- ✅ Write basic tests to verify serialization works

### Hour 2: Storage Layer (Part 2)
- ✅ `src/storage/dynamodb_client.py`
- ✅ `src/storage/s3_client.py`
- ✅ Write unit tests for storage layer
- ✅ **Git:** Commit this as "feat: implement storage layer"

### Hour 3: External Services (Part 3)
- ✅ `src/external/sentiment_service.py`
- ✅ Write tests for sentiment analysis
- ✅ **Git:** Commit this as "feat: add sentiment analysis"

### Hour 4: API Handler (Part 4)
- ✅ `src/api/feedback_handler.py`
- ✅ Implement `submit_feedback()` method
- ✅ Implement `get_restaurant_insights()` method
- ✅ **Git:** Commit this as "feat: implement API handler"

### Hour 5: Integration Tests (Part 5)
- ✅ `tests/test_feedback_handler.py`
- ✅ Write end-to-end tests
- ✅ Verify coverage is >80%
- ✅ **Git:** Commit this as "test: add integration tests"

### Hour 6: Documentation & Git (Parts 6-7)
- ✅ Write README.md
- ✅ Add docstrings to all classes/methods
- ✅ Create feature branches and demonstrate merge
- ✅ **Git:** Final commit "docs: add README and documentation"

---

## Sample Code to Get Started

### tenant_registry.json (Copy-Paste Ready)

```json
{
  "tenants": [
    {
      "tenant_id": "pizza-palace-123",
      "restaurant_name": "Pizza Palace",
      "api_key": "pk_pizza_abc123",
      "plan": "premium",
      "features": {
        "sentiment_analysis": true,
        "advanced_insights": true
      },
      "created_at": "2026-01-15T00:00:00Z"
    },
    {
      "tenant_id": "burger-barn-456",
      "restaurant_name": "Burger Barn",
      "api_key": "pk_burger_def456",
      "plan": "basic",
      "features": {
        "sentiment_analysis": false,
        "advanced_insights": false
      },
      "created_at": "2026-01-20T00:00:00Z"
    },
    {
      "tenant_id": "sushi-spot-789",
      "restaurant_name": "Sushi Spot",
      "api_key": "pk_sushi_ghi789",
      "plan": "premium",
      "features": {
        "sentiment_analysis": true,
        "advanced_insights": false
      },
      "created_at": "2026-02-01T00:00:00Z"
    }
  ]
}
```

### Sample Test to Get Started

```python
# tests/test_dynamodb_client.py

import pytest
from src.storage.dynamodb_client import DynamoDBClient


class TestDynamoDBClient:
    def test_save_and_retrieve_feedback(self):
        """Test basic save and retrieve operations."""
        # Arrange
        client = DynamoDBClient()
        tenant_id = "test-tenant"
        feedback_data = {
            "feedback_id": "test-123",
            "tenant_id": tenant_id,
            "rating": 5,
            "comment": "Great!",
            "created_at": "2026-02-22T10:00:00Z"
        }
        
        # Act
        client.save_feedback(tenant_id, feedback_data)
        result = client.get_feedback_by_id(tenant_id, "test-123")
        
        # Assert
        assert result is not None
        assert result["feedback_id"] == "test-123"
        assert result["rating"] == 5
```

---

## Getting Help

### Use AI Assistants Effectively

**Good Prompts:**
- "Write a Python dataclass for a Tenant model with these fields: ..."
- "How do I mock an external API call in pytest?"
- "Explain how to implement tenant isolation in a dictionary"

**Bad Prompts:**
- "Write the entire project for me" (you won't learn anything)
- "Give me the answer" (without understanding it)

### Debugging Checklist

Before asking for help, try:
1. ✅ Read the error message completely
2. ✅ Check file paths (are you in the right directory?)
3. ✅ Verify imports (did you create `__init__.py` files?)
4. ✅ Run a single test to isolate the problem
5. ✅ Add print statements to see intermediate values

---

## Final Checklist Before Submitting

- [ ] All tests pass: `pytest tests/ -v`
- [ ] Coverage >80%: `pytest tests/ --cov=src`
- [ ] No linting errors (if you set up linting)
- [ ] README.md explains the project
- [ ] Docstrings on all public methods
- [ ] Git history shows multiple meaningful commits
- [ ] No sensitive data (API keys, passwords) in code
- [ ] No `venv/` or `__pycache__/` in submission
- [ ] Works on fresh clone: 
  ```bash
  cd ..
  git clone <your-repo>
  cd <your-repo>
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  pytest tests/ -v
  ```

---

## Time-Saving Tips

### Use Copilot/ChatGPT for:
- ✅ Generating boilerplate code (class definitions)
- ✅ Writing test cases
- ✅ Explaining error messages
- ✅ Suggesting better variable names

### Don't Use AI for:
- ❌ Writing your README (use your own words)
- ❌ Designing the architecture (think independently)
- ❌ Blindly copy-pasting without understanding

### Copy-Paste Time Savers

**pytest fixture for fresh client:**
```python
@pytest.fixture
def db_client():
    """Fresh DynamoDB client for each test."""
    return DynamoDBClient()
```

**UUID generation:**
```python
import uuid
feedback_id = str(uuid.uuid4())
```

**Current timestamp:**
```python
from datetime import datetime
created_at = datetime.utcnow().isoformat() + "Z"
```

---

## Good Luck! 🚀

Remember:
- **Quality > Speed** - We'd rather see clean code that's 80% complete than rushed buggy code
- **Tests matter** - They show you write maintainable code
- **Git history matters** - It shows your thought process
- **Documentation matters** - It shows you can communicate

**Time tracking:**  
Start time: _________  
End time: _________  
Total: _________ hours

We're excited to see what you build! 🎉
