# MathPath AI Chatbot — Step 4 Lead Capture & Storage Guide

This step upgrades the chatbot from a simple enquiry form to a proper admissions lead system.

## What Step 4 Adds

- Structured lead capture from the React chatbot widget
- Parent consent checkbox
- Lead reference ID for every submission
- Local CSV lead storage
- Optional Supabase lead storage
- Optional webhook forwarding to Make, Zapier, Pabbly, or Google Apps Script
- Basic lead scoring: `new`, `warm`, or `hot`
- Recommended program attached to each lead where possible
- Admin-protected lead listing and CSV export endpoints
- Admin-protected chat log export endpoint

## Local Storage

By default, leads are saved here:

```text
backend/storage/leads.csv
```

Chat logs are saved here:

```text
backend/storage/chat_logs.csv
```

These files are created automatically after the first lead or chat.

## Admin API Key

Set this in your backend `.env` file:

```env
ADMIN_API_KEY=replace_with_a_strong_private_key
```

Use this key in the request header:

```text
x-admin-api-key: replace_with_a_strong_private_key
```

## Admin Endpoints

### List Recent Leads

```bash
curl -H "x-admin-api-key: replace_with_a_strong_private_key" \
  http://localhost:8000/admin/leads?limit=50
```

### Export Leads CSV

```bash
curl -H "x-admin-api-key: replace_with_a_strong_private_key" \
  -o mathpath_leads.csv \
  http://localhost:8000/admin/leads/export
```

### Export Chat Logs CSV

```bash
curl -H "x-admin-api-key: replace_with_a_strong_private_key" \
  -o mathpath_chat_logs.csv \
  http://localhost:8000/admin/chat-logs/export
```

## Optional Supabase Setup

1. Create a Supabase project.
2. Open the Supabase SQL Editor.
3. Run `backend/supabase_schema.sql`.
4. Add these values to `.env`:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_LEADS_TABLE=mathpath_leads
```

The backend always saves to local CSV first. If Supabase is configured, it also attempts to save there.

## Optional Google Sheets / CRM Forwarding

Use `LEAD_WEBHOOK_URL` if you want every lead pushed to:

- Google Sheets through Google Apps Script
- Make.com scenario
- Zapier zap
- Pabbly workflow
- CRM webhook

Example:

```env
LEAD_WEBHOOK_URL=https://hook.eu2.make.com/your-webhook-id
```

Webhook failures do not block lead capture. The CSV remains the backup source of truth.

## Lead Score Logic

The chatbot assigns each lead a score from 0 to 100 using deterministic rules.

Higher score means the parent has shown stronger admission/demo intent.

| Priority | Score Range | Meaning |
|---|---:|---|
| hot | 80–100 | Strong admission/demo intent |
| warm | 60–79 | Good enquiry with useful details |
| new | below 60 | Basic enquiry |

## Important Production Notes

- Change `ADMIN_API_KEY` before deployment.
- Do not expose the Supabase service role key in the frontend.
- Keep lead export endpoints private.
- Add the deployed frontend domain to `ALLOWED_ORIGINS`.
- Review local data/privacy compliance before collecting parent/child details.
