# Future Admin Dashboard Enhancements

These are optional upgrades for the final production version.

## Recommended Phase 2 dashboard features

1. Admin login with email/password using Supabase Auth.
2. Lead status update directly inside dashboard.
3. Notes column for counsellor comments.
4. Assign lead to counsellor.
5. WhatsApp click-to-message templates.
6. Demo booking calendar integration.
7. Conversion tracking: enquiry → demo → admission.
8. Bot analytics: most asked questions, unanswered queries, low-confidence answers.
9. Knowledge base editor for non-technical admin users.
10. Automatic daily email report of new leads.

## Recommended database upgrade

Move from CSV storage to Supabase/Postgres for production.

Suggested tables:

- `leads`
- `chat_logs`
- `admin_users`
- `lead_notes`
- `demo_bookings`
- `bot_feedback`

## Suggested dashboard KPIs

- Total enquiries
- Hot leads
- Demo requests
- Demo booked
- Admissions converted
- Most common parent concern
- Top age/class group enquiring
- Lead source
- Bot handoff rate
