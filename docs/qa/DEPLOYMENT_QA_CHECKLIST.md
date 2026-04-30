# Deployment QA Checklist

## Backend Deployment

- [ ] Backend deploys successfully on Render or selected hosting provider.
- [ ] `/` endpoint returns status `ok`.
- [ ] `/health` returns status `healthy`.
- [ ] `/chat` returns a complete answer.
- [ ] `/lead` accepts a valid lead.
- [ ] Admin routes reject unauthorised requests.
- [ ] Admin routes accept valid admin token.
- [ ] CORS includes the deployed frontend and MathPath website domain.
- [ ] Environment variables are configured correctly.
- [ ] Logs do not reveal API keys.

## Frontend Deployment

- [ ] Frontend deploys successfully on Vercel or selected hosting provider.
- [ ] Chat launcher appears.
- [ ] MathPath logo appears in launcher/header/avatar.
- [ ] Chat sends requests to the production backend URL.
- [ ] Suggested questions work.
- [ ] Lead form submits correctly.
- [ ] Mobile layout works.
- [ ] Error states are user-friendly.

## Website Integration

- [ ] Embed script is added to MathPath website.
- [ ] Widget appears on homepage.
- [ ] Widget does not hide important website buttons.
- [ ] Widget works on mobile.
- [ ] No JavaScript console errors.
- [ ] No mixed-content errors between HTTPS and HTTP.

## Final User Acceptance

- [ ] Parent can understand what MathPath offers within 2 minutes.
- [ ] Parent can identify the right program or request guidance.
- [ ] Parent can submit a demo/admission enquiry.
- [ ] MathPath team can view/export leads.
