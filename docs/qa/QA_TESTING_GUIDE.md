# MathPath AI Chatbot QA Testing Guide

## 1. Testing Goal

The goal is to confirm that the MathPath chatbot is accurate, parent-friendly, safe, and ready for deployment.

The chatbot must be able to answer MathPath-specific questions about:

- Organisation identity and purpose
- Age-wise program structure
- Young Learner Program
- Preparatory Level
- Intermediate Level
- Master Module
- Bridge Course
- Hybrid learning model
- Daily app practice
- Parent concerns
- Contact details
- Demo/admission interest

It must not invent unsupported information such as exact fees, exact batches, admission deadlines, or guaranteed school marks.

## 2. Automated Test Types

### API Smoke Tests

Located in:

```text
qa_tests/api/test_api_smoke.py
```

These confirm that `/`, `/health`, and `/chat` are working.

### Lead Capture Tests

Located in:

```text
qa_tests/api/test_lead_capture.py
```

These confirm that valid leads are accepted and invalid phone numbers are rejected.

### RAG Quality Tests

Located in:

```text
qa_tests/rag/test_rag_quality.py
```

These test real parent-style prompts and check expected keywords, forbidden phrases, lead-capture triggers, and program recommendation outputs.

### Admin Endpoint Tests

Located in:

```text
qa_tests/api/test_admin_endpoints.py
```

These validate that admin routes are protected and work when the admin token is provided.

## 3. How to Run

```bash
pip install -r requirements-test.txt
export MATHPATH_API_BASE_URL="http://localhost:8000"
python scripts/run_all_tests.py
```

On Windows PowerShell:

```powershell
$env:MATHPATH_API_BASE_URL="http://localhost:8000"
python scripts/run_all_tests.py
```

## 4. How to Interpret Failures

### Missing Expected Keyword

The answer may be too generic or retrieval may not be finding the right knowledge-base chunk.

Fix:

- Improve the relevant knowledge-base file.
- Improve retrieval query expansion.
- Adjust the fallback response template.

### Forbidden Phrase Found

The bot may be making unsupported claims.

Fix:

- Strengthen guardrails.
- Add a direct instruction in the system prompt.
- Add the exact forbidden topic to the FAQ/guardrails.

### Wrong Program Recommendation

The recommendation agent needs adjustment.

Fix:

- Update `recommendation_agent.py` rules.
- Add more age/class parsing cases.

### Lead Capture Not Triggered

The intent router may not be detecting admission/demo/callback intent.

Fix:

- Add trigger words such as admission, demo, fees, call, join, enroll, callback.

## 5. Final QA Sign-Off Criteria

Move to final consolidation only when:

- All automated tests pass or all failures are reviewed and accepted.
- Manual frontend checklist is complete.
- Deployed backend smoke test passes.
- Bot correctly handles fees and batch-timing questions without inventing values.
- Contact details are correct.
- Logo appears in the launcher, header, and bot avatar.
