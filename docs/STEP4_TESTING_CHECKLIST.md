# Step 4 Testing Checklist

## Backend

Run the backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

## Test Lead Submission

Use `/lead` in Swagger or run:

```bash
curl -X POST http://localhost:8000/lead \
  -H "Content-Type: application/json" \
  -d '{
    "parent_name":"Test Parent",
    "child_name":"Test Child",
    "child_age":"8",
    "child_class":"Class 3",
    "phone":"9876543210",
    "email":"parent@example.com",
    "preferred_mode":"offline",
    "main_concern":"My child is slow in calculations and weak in basics",
    "preferred_callback_time":"Evening",
    "session_id":"test-session",
    "source":"manual_test",
    "consent_to_contact":true
  }'
```

Expected result:

- `status` should be `success`
- `lead_id` should start with `MP-`
- `backend/storage/leads.csv` should be created

## Test Admin Export

```bash
curl -H "x-admin-api-key: change_this_admin_key" \
  http://localhost:8000/admin/leads?limit=10
```

## Frontend

Run the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

Submit the chatbot lead form and confirm the record appears in `backend/storage/leads.csv`.
