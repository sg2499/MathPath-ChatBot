# MathPath AI Chatbot — Final Launch Checklist

## Backend
- [ ] `.env` created from `.env.example`
- [ ] `OPENAI_API_KEY` added
- [ ] `ADMIN_API_KEY` changed from default
- [ ] `ALLOWED_ORIGINS` includes frontend, admin, and MathPath website domains
- [ ] `/health` returns healthy
- [ ] `/chat` returns MathPath-specific answers
- [ ] `/lead` creates a lead successfully
- [ ] `/admin/leads` works only with admin key

## Frontend chatbot
- [ ] MathPath logo appears on launcher, header, and bot avatar
- [ ] Suggested questions work
- [ ] Parent questions return good answers
- [ ] Lead form opens when user asks for demo/admission/callback
- [ ] Mobile view tested
- [ ] Widget does not block important website buttons

## Admin dashboard
- [ ] Admin dashboard connects to backend
- [ ] Leads visible
- [ ] Filters/search work
- [ ] CSV export works
- [ ] Chat log export works

## Website integration
- [ ] Embed script added to MathPath website
- [ ] Widget loads on homepage
- [ ] Widget loads on mobile
- [ ] Widget calls production backend
- [ ] No CORS errors in browser console

## QA
- [ ] Run parent prompt tests
- [ ] Run lead capture tests
- [ ] Run RAG quality tests
- [ ] Run deployment smoke test
- [ ] Check fallback answers for fees/timings

## Go-live
- [ ] Send 3 test leads
- [ ] Verify contact details are correct
- [ ] Verify Bridge Course answers
- [ ] Verify age-wise recommendation answers
- [ ] Verify no unsupported claims are made
