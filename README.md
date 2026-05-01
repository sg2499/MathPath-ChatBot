# 🧮 MathPath AI ChatBot — Agentic RAG Website Assistant

![GitHub repo size](https://img.shields.io/github/repo-size/sg2499/MathPath-ChatBot)
![Last Commit](https://img.shields.io/github/last-commit/sg2499/MathPath-ChatBot)
![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-blue)
![Backend](https://img.shields.io/badge/Backend-FastAPI-green)
![RAG](https://img.shields.io/badge/AI-Agentic%20RAG-purple)
![Deployment](https://img.shields.io/badge/Deployment-Render%20%2B%20Vercel-black)
![Python](https://img.shields.io/badge/Python-3.11.11-yellow)
![License](https://img.shields.io/badge/License-Private%20%2F%20Commercial-lightgrey)

**Repository:** https://github.com/sg2499/MathPath-ChatBot  
**MathPath Website:** https://www.mathpath.in/website/index  
**Public Chatbot App:** https://math-path-chat-bot.vercel.app  
**Backend API:** https://mathpath-chatbot.onrender.com  
**Backend Health Check:** https://mathpath-chatbot.onrender.com/health  
**Backend API Docs:** https://mathpath-chatbot.onrender.com/docs

---

## 📌 What is MathPath AI ChatBot?

**MathPath AI ChatBot** is a commercial-ready AI assistant built for the MathPath website. It helps parents and visitors quickly understand MathPath, its programs, class structure, practice model, centres, contact details, fee guidance, assessment process, competitions, and admission flow.

The chatbot is designed to behave like a professional website assistant, not a generic AI demo. It answers crisply, avoids unnecessary long responses, streams answers like modern AI products, and guides interested parents toward a demo or callback only when relevant.

This project was built for integration into the official MathPath website by the website developer.

---

## 🌐 Important Links

| Purpose | Link |
|---|---|
| GitHub Repository | https://github.com/sg2499/MathPath-ChatBot |
| MathPath Website | https://www.mathpath.in/website/index |
| Public Chatbot Preview | https://math-path-chat-bot.vercel.app |
| Render Backend API | https://mathpath-chatbot.onrender.com |
| Backend Health Check | https://mathpath-chatbot.onrender.com/health |
| Backend API Docs | https://mathpath-chatbot.onrender.com/docs |
| Render Dashboard | https://dashboard.render.com/ |
| Vercel Dashboard | https://vercel.com/dashboard |
| OpenAI Platform | https://platform.openai.com/ |
| OpenAI API Keys | https://platform.openai.com/settings/organization/api-keys |
| OpenAI Billing | https://platform.openai.com/settings/organization/billing |
| OpenAI Models Docs | https://developers.openai.com/api/docs/models |

---

## 🎯 Purpose of This Project

The MathPath website needs a professional AI assistant that can:

- Answer parent questions instantly.
- Explain MathPath programs in simple language.
- Recommend the correct entry program based on class or age.
- Provide centre addresses and contact details.
- Explain weekly class structure, practice model, assessments, certification, competitions, and admission process.
- Avoid fake information about fees, ownership, batch timings, or internal details.
- Collect leads for demo class or callback requests.
- Stream answers in a modern ChatGPT-style interface.
- Be embedded into the existing MathPath website without rewriting the website.

---

## 🧠 High-Level Architecture

```text
MathPath Website Visitor
        ↓
Floating Chat Widget / Public Chat Page
        ↓
React + Vite Frontend on Vercel
        ↓
FastAPI Backend on Render
        ↓
Intent Router + Agentic RAG + Knowledge Base
        ↓
OpenAI LLM Response Generation
        ↓
Streaming Answer + Lead Capture + Logs
```

---

## 🧩 Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite |
| UI Styling | Custom CSS premium chatbot design |
| Backend | FastAPI |
| Server | Uvicorn |
| AI Layer | OpenAI LLM |
| Retrieval | Local knowledge base + Agentic RAG logic |
| Streaming | Server-Sent Events / streaming response endpoint |
| Lead Capture | Local CSV, optional webhook/Supabase-ready structure |
| Admin | Admin dashboard package / admin endpoints |
| Frontend Deployment | Vercel |
| Backend Deployment | Render |
| Python Version | 3.11.11 |

---

## 🤖 AI Model Configuration

The backend uses an OpenAI model configured through environment variables.

Recommended production model options:

```env
OPENAI_MODEL=gpt-5.5
```

or, for a chat-optimized latest snapshot:

```env
OPENAI_MODEL=gpt-5.1-chat-latest
```

If the selected model is unavailable in the OpenAI account, switch to a model available in the account from the OpenAI model list:

https://developers.openai.com/api/docs/models

Do **not** expose the OpenAI API key in frontend code. It must stay only in the Render backend environment variables.

---

## ✨ Core Features

### 1. Agentic RAG Answering

The bot retrieves MathPath-specific knowledge before answering. It uses structured routing and guardrails to avoid hallucination.

### 2. Crisp Commercial-Ready Responses

The chatbot is instructed to respond in short, parent-friendly answers. It avoids long essay-style output unless the user explicitly asks for detailed explanation.

### 3. Streaming Responses

The frontend calls the streaming backend endpoint so answers appear progressively like modern AI products.

Primary endpoint:

```text
POST /chat/stream
```

Fallback endpoint:

```text
POST /chat
```

### 4. Entry Program Flow

For general program questions, the bot shows only the three entry/enrolment programs:

| Entry Program | Suitable For | Duration | Focus | Next Progression |
|---|---|---:|---|---|
| Young Learner | UKG, Class 1, Class 2 | 10 months | Foundational abacus operations | Preparatory Level 2 |
| Preparatory Level 1 | Class 3 and Class 4 | 4 months | Visual and operational fluency | Preparatory Level 2 |
| Bridge Course | Class 5 to Class 8 late joiners | 10-12 months | 4 levels clubbed into one level | Intermediate Level 1 |

The bot should not show Intermediate or Master Module in the basic program answer unless the user asks about full journey, advanced levels, Intermediate, or Master Module specifically.

### 5. Lead Capture

The bot captures parent details only when the user clearly shows interest in demo, callback, admission, joining, or enrolment.

It does **not** force a lead form after every question.

### 6. Professional UI

The chatbot UI has been upgraded to a more premium commercial look with:

- Floating launcher.
- MathPath branding.
- Modern AI-style message bubbles.
- Streaming cursor.
- Quick question chips.
- Controlled demo form.
- Refresh/start-new-chat button.
- Mobile responsive behavior.

### 7. Refresh Chat Option

The chatbot header includes a refresh option so users can start a new conversation without reloading the full website.

### 8. Centre Address Handling

The bot now knows both MathPath centres:

```text
Lake Town Centre:
240, Block A, 1st Floor, Laketown, Kolkata - 700089

Rajarhat Centre:
Laxmi Apartment, 1st Floor, Dashadrone, Checkpost, Rajarhat Main Road,
next to Urban Greens, above Vrindavan Sweets, Kolkata 700136
```

### 9. Guardrails

The bot must never invent:

- Fees.
- Batch timings beyond available guidance.
- Offers.
- Owners or management names.
- Registration details.
- Guarantees of marks or results.
- Teacher names.
- Internal administrative details.

For unknowns, it shares official MathPath contact details.

---

## 📚 MathPath Knowledge Base Summary

The knowledge base contains information about:

- What MathPath is.
- Program structure.
- Age-wise/class-wise entry programs.
- Bridge Course.
- Weekly class model.
- Daily practice sheet submission.
- Automated student portal.
- Batch size.
- Fee contact guidance.
- Admissions open round the year.
- Annual competition eligibility.
- Assessment and certification rules.
- Centre locations.
- Phone and email details.
- Bot guardrails and fallback responses.

### Key FAQ Knowledge Added

| Topic | Bot Knowledge |
|---|---|
| What is MathPath? | A UKG-Class 8 abacus + visualisation + school-syllabus-aligned maths program. |
| Class frequency | Weekly once, 2 hours per class, 4 classes per month. |
| Daily practice | Daily practice sheet submission through automated student portal. |
| Fees | Contact helpline: 7980918759 / 9831684229. |
| Batch size | Maximum 10-12 students. |
| Admission | Round-the-year admission. Learning starts from date of joining. |
| Competition | Annual competition; Level 2 onward students are eligible. |
| Assessment | Level-end assessment; minimum 75% needed for promotion. |
| Certification | Certificate issued after successful level assessment. |

---

## 📁 Recommended Repository Structure

```text
MathPath-ChatBot/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── .python-version
│   ├── .env.example
│   ├── agents/
│   │   ├── rag_answer_agent.py
│   │   ├── router_agent.py
│   │   └── recommendation_agent.py
│   ├── knowledge_base/
│   │   ├── 11_contact_and_location.md
│   │   ├── 12_bot_guardrails.md
│   │   └── 13_faq_program_details_from_latest_doc.md
│   ├── rag/
│   ├── leads/
│   └── data/
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── public/
│   │   └── mathpath-favicon.png
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── components/
│       │   ├── ChatWidget.jsx
│       │   └── api.js
│       └── styles/
│           └── chatbot.css
│
├── admin-dashboard/
├── docs/
├── qa-testing/
├── assets/
├── README.md
└── .gitignore
```

---

## 🚀 Local Developer Setup

### 1. Clone the Repository

```bash
git clone https://github.com/sg2499/MathPath-ChatBot.git
cd MathPath-ChatBot
```

---

## 🖥️ Backend Setup

### 1. Open Backend Folder

```bash
cd backend
```

### 2. Create Virtual Environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env`

**Windows PowerShell**

```powershell
copy .env.example .env
```

**macOS / Linux**

```bash
cp .env.example .env
```

### 5. Configure Backend Environment

Example:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-5.5
ADMIN_API_KEY=change_this_to_a_secure_admin_key
ALLOWED_ORIGINS=http://localhost:5173,https://math-path-chat-bot.vercel.app,https://www.mathpath.in
PYTHON_VERSION=3.11.11
```

### 6. Run Backend Locally

```bash
python -m uvicorn main:app --reload --port 8000
```

Test:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

---

## 💬 Frontend Setup

### 1. Open Frontend Folder

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Create `.env`

**Windows PowerShell**

```powershell
copy .env.example .env
```

**macOS / Linux**

```bash
cp .env.example .env
```

### 4. Configure Frontend Environment

For local testing:

```env
VITE_MATHPATH_API_URL=http://localhost:8000
```

For production Vercel:

```env
VITE_MATHPATH_API_URL=https://mathpath-chatbot.onrender.com
```

The code also supports:

```env
VITE_API_BASE_URL=https://mathpath-chatbot.onrender.com
```

### 5. Run Frontend Locally

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

---

## 🔐 Environment Variables Summary

### Backend on Render

| Variable | Required | Example |
|---|---|---|
| `OPENAI_API_KEY` | Yes | `sk-...` |
| `OPENAI_MODEL` | Recommended | `gpt-5.5` or `gpt-5.1-chat-latest` |
| `ADMIN_API_KEY` | Yes | `mathpath_admin_secure_key` |
| `ALLOWED_ORIGINS` | Yes | `https://math-path-chat-bot.vercel.app,https://www.mathpath.in` |
| `PYTHON_VERSION` | Recommended | `3.11.11` |

### Frontend on Vercel

| Variable | Required | Example |
|---|---|---|
| `VITE_MATHPATH_API_URL` | Yes | `https://mathpath-chatbot.onrender.com` |
| `VITE_API_BASE_URL` | Optional fallback | `https://mathpath-chatbot.onrender.com` |

### Admin Dashboard on Vercel, if deployed

| Variable | Required | Example |
|---|---|---|
| `VITE_API_BASE_URL` | Yes | `https://mathpath-chatbot.onrender.com` |
| `VITE_ADMIN_API_KEY` | Yes | Same value as backend `ADMIN_API_KEY` |

---

## ☁️ Deployment Guide

## Backend Deployment on Render

Create a new **Web Service** on Render.

| Setting | Value |
|---|---|
| Repository | `sg2499/MathPath-ChatBot` |
| Root Directory | `backend` |
| Runtime | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/health` |
| Python Version | `3.11.11` |

Backend URL:

```text
https://mathpath-chatbot.onrender.com
```

Health check:

```text
https://mathpath-chatbot.onrender.com/health
```

API docs:

```text
https://mathpath-chatbot.onrender.com/docs
```

---

## Frontend Deployment on Vercel

Create a new Vercel project from the same GitHub repository.

| Setting | Value |
|---|---|
| Repository | `sg2499/MathPath-ChatBot` |
| Framework | Vite |
| Root Directory | `frontend` |
| Build Command | `npm run build` |
| Output Directory | `dist` |

Add environment variable:

```env
VITE_MATHPATH_API_URL=https://mathpath-chatbot.onrender.com
```

Public frontend URL:

```text
https://math-path-chat-bot.vercel.app
```

---

## 🔁 After Every Backend Change

1. Push code to GitHub.
2. Go to Render.
3. Click **Manual Deploy**.
4. Prefer **Clear build cache & deploy** for dependency or config changes.
5. Verify `/health`.
6. Test public chatbot.

---

## 🔁 After Every Frontend Change

1. Push code to GitHub.
2. Vercel should redeploy automatically.
3. Open deployment logs if the build fails.
4. Hard refresh the browser with `Ctrl + F5`.
5. If favicon does not update, test in an incognito window.

---

# 🌍 Website Integration Guide for MathPath Developer

This section is for the developer who maintains the existing MathPath website source code.

The chatbot can be integrated without rebuilding the website. The safest integration method is to embed the deployed chatbot as a floating iframe widget.

---

## Integration Option A — Floating Iframe Widget, Recommended

Use this when the current website is not React/Vite or when the developer wants the quickest, safest integration.

Add the following code before the closing `</body>` tag of the MathPath website:

```html
<!-- MathPath AI ChatBot Floating Widget -->
<div id="mathpath-chatbot-wrapper">
  <button id="mathpath-chatbot-button" aria-label="Open MathPath ChatBot">
    <span>💬</span>
    <strong>Ask MathPath</strong>
  </button>

  <div id="mathpath-chatbot-frame-container" aria-hidden="true">
    <iframe
      id="mathpath-chatbot-frame"
      src="https://math-path-chat-bot.vercel.app"
      title="MathPath ChatBot"
      loading="lazy"
      allow="clipboard-write"
    ></iframe>
  </div>
</div>

<style>
  #mathpath-chatbot-wrapper {
    position: fixed;
    right: 22px;
    bottom: 22px;
    z-index: 999999;
    font-family: Inter, Arial, sans-serif;
  }

  #mathpath-chatbot-button {
    border: 0;
    border-radius: 999px;
    padding: 13px 18px;
    background: linear-gradient(135deg, #ff3f7f, #05aeea);
    color: #fff;
    font-weight: 800;
    box-shadow: 0 18px 40px rgba(41, 45, 99, 0.25);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  #mathpath-chatbot-frame-container {
    display: none;
    width: min(430px, calc(100vw - 28px));
    height: min(700px, calc(100vh - 34px));
    margin-bottom: 14px;
    border-radius: 26px;
    overflow: hidden;
    box-shadow: 0 24px 70px rgba(41, 45, 99, 0.35);
    background: #fff;
  }

  #mathpath-chatbot-frame-container.open {
    display: block;
  }

  #mathpath-chatbot-frame {
    width: 100%;
    height: 100%;
    border: 0;
  }

  @media (max-width: 520px) {
    #mathpath-chatbot-wrapper {
      right: 12px;
      bottom: 12px;
    }

    #mathpath-chatbot-frame-container {
      width: calc(100vw - 24px);
      height: calc(100vh - 90px);
    }
  }
</style>

<script>
  (function () {
    const button = document.getElementById('mathpath-chatbot-button');
    const frame = document.getElementById('mathpath-chatbot-frame-container');

    button.addEventListener('click', function () {
      const isOpen = frame.classList.toggle('open');
      frame.setAttribute('aria-hidden', String(!isOpen));
      button.querySelector('strong').textContent = isOpen ? 'Close Chat' : 'Ask MathPath';
    });
  })();
</script>
```

### What this does

- Keeps the chatbot hosted independently on Vercel.
- Avoids dependency conflicts with the existing MathPath website.
- Adds a floating chat button to the website.
- Opens the chatbot inside a clean frame.
- Allows future chatbot updates without changing the website code again.

---

## Integration Option B — Simple Link Button

If the developer does not want iframe integration initially, add a button on the website that opens the chatbot in a new tab:

```html
<a
  href="https://math-path-chat-bot.vercel.app"
  target="_blank"
  rel="noopener noreferrer"
  class="mathpath-chatbot-link"
>
  Ask MathPath ChatBot
</a>
```

---

## Integration Option C — Direct React Component Integration

Use this only if the MathPath website is also a React/Vite application and the developer wants to merge the component into the website codebase.

Required files from this repository:

```text
frontend/src/components/ChatWidget.jsx
frontend/src/components/api.js
frontend/src/styles/chatbot.css
frontend/public/mathpath-favicon.png
```

In the website React app:

```jsx
import ChatWidget from './components/ChatWidget';
import './styles/chatbot.css';

function App() {
  return (
    <>
      {/* existing website */}
      <ChatWidget />
    </>
  );
}
```

Set website environment variable:

```env
VITE_MATHPATH_API_URL=https://mathpath-chatbot.onrender.com
```

Important: Direct component integration can create CSS or dependency conflicts. For a third-party website source code, iframe integration is safer.

---

## 🔐 Required CORS Update After Website Integration

After the chatbot is embedded on the official MathPath website, update the Render backend environment variable:

```env
ALLOWED_ORIGINS=https://math-path-chat-bot.vercel.app,https://www.mathpath.in
```

If the website also uses a non-www domain, include both:

```env
ALLOWED_ORIGINS=https://math-path-chat-bot.vercel.app,https://www.mathpath.in,https://mathpath.in
```

Then redeploy the backend on Render.

---

## ✅ Integration Testing Checklist

After adding the chatbot to the website, test the following:

### Visual Checks

- Chat button is visible on desktop.
- Chat button is visible on mobile.
- Chat window does not cover important page buttons.
- Chat window opens and closes smoothly.
- Chat is not clipped by website sections.
- z-index is high enough.

### Functional Checks

Ask:

```text
What is MathPath?
```

Expected: A short explanation of MathPath.

Ask:

```text
Explain the different programs you offer.
```

Expected: Only Young Learner, Preparatory Level 1, and Bridge Course.

Ask:

```text
Where are your centres located?
```

Expected: Both Lake Town Centre and Rajarhat Centre.

Ask:

```text
What is the fee structure?
```

Expected: Bot does not invent fees; it shares helpline numbers.

Ask:

```text
Who are the owners?
```

Expected: Bot does not guess; it says ownership details are not publicly listed and shares official contact details.

Ask:

```text
I want to book a demo class.
```

Expected: Lead form appears.

### Browser Checks

Test in:

- Chrome desktop.
- Chrome mobile view.
- Edge.
- Safari, if available.
- Android phone browser.

---

## 🧪 API Testing Commands

### Health Check

```bash
curl https://mathpath-chatbot.onrender.com/health
```

### Normal Chat

```bash
curl -X POST https://mathpath-chatbot.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What is MathPath?"}'
```

### Streaming Chat

```bash
curl -N -X POST https://mathpath-chatbot.onrender.com/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message":"Where are your centres located?"}'
```

---

## 🛡️ Safety and Brand Rules

The chatbot must:

- Use official MathPath details.
- Keep answers short and professional.
- Avoid placeholders like `[insert contact details here]`.
- Avoid hallucinated owners, fees, batch times, or guarantees.
- Suggest demo only when relevant.
- Provide both centre addresses when asked about location.
- Use helpline numbers for fee and admission-specific questions.
- Never expose OpenAI keys or admin keys.

---

## 💰 Cost Control and API Safety

This bot uses OpenAI through the backend. To control cost:

- Keep API key only in Render backend environment variables.
- Do not expose keys in frontend code.
- Monitor OpenAI usage at: https://platform.openai.com/usage
- Set usage limits in OpenAI billing dashboard if required.
- Avoid enabling unrestricted high-volume public traffic without monitoring.
- Consider rate limiting if the website receives high traffic.

---

## 🧯 Troubleshooting Guide

### 1. Bot says it cannot connect to backend

Cause:

- Vercel is calling `localhost:8000`.
- Backend URL env variable missing.
- Render service is asleep or down.

Fix:

Set in Vercel:

```env
VITE_MATHPATH_API_URL=https://mathpath-chatbot.onrender.com
```

Redeploy Vercel.

---

### 2. Console shows CORS error

Cause:

The website domain is not allowed by backend CORS.

Fix:

Set in Render:

```env
ALLOWED_ORIGINS=https://math-path-chat-bot.vercel.app,https://www.mathpath.in,https://mathpath.in
```

Redeploy Render.

---

### 3. Render build is stuck on scikit-learn or Python dependency build

Cause:

Wrong Python version.

Fix:

Add in Render:

```env
PYTHON_VERSION=3.11.11
```

Make sure `backend/.python-version` contains:

```text
3.11.11
```

---

### 4. Uvicorn cannot import `app`

Correct backend command is:

```bash
python -m uvicorn main:app --reload --port 8000
```

For Render:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

### 5. Favicon does not update

Cause:

Browser favicon cache.

Fix:

- Hard refresh with `Ctrl + F5`.
- Open in incognito.
- Wait after Vercel redeploy.

---

### 6. Lead form appears too often

Expected current behavior:

Lead form should appear only when the user asks to book, join, schedule demo, request callback, or enroll.

If it appears after every answer, check the latest `ChatWidget.jsx` has been deployed.

---

### 7. Bot gives long answers

Check `backend/agents/rag_answer_agent.py` prompt. It should instruct:

```text
Answer crisply in 2-5 short sentences unless the user asks for details.
```

Redeploy backend after prompt changes.

---

### 8. Bot shows `[insert contact details here]`

This should be blocked by guardrails. If it appears:

- Check `rag_answer_agent.py` sanitization.
- Check `12_bot_guardrails.md`.
- Redeploy backend.

---

## ✅ Final Developer Handoff Checklist

Before marking integration complete:

- [ ] Backend `/health` works.
- [ ] Backend `/docs` works.
- [ ] Frontend chatbot page works.
- [ ] Website domain added to Render `ALLOWED_ORIGINS`.
- [ ] Chatbot added to MathPath website.
- [ ] Chat opens on desktop and mobile.
- [ ] Streaming answers work.
- [ ] Location answer shows both centres.
- [ ] Program answer shows only entry programs.
- [ ] Fee answer does not invent prices.
- [ ] Demo form appears only when user asks for demo/callback/admission.
- [ ] Refresh chat button works.
- [ ] No console errors.
- [ ] OpenAI key is not present in frontend or GitHub.

---

## ✍️ Author / Project Owner

Built by **Shailesh Gupta**

- GitHub: https://github.com/sg2499
- LinkedIn: https://www.linkedin.com/in/shailesh-gupta-7b7278188
- Portfolio: https://personal-portfolio-ten-virid-75.vercel.app/
- Blog: https://prismatic-metrics.blogspot.com/
- Email: shaileshgupta841@gmail.com

---

## 🏢 MathPath Contact Details

**Website:** https://www.mathpath.in/website/index  
**Email:** info@mathpath.in  
**Phone:** 7980918759 / 9831684229

**Lake Town Centre:**  
240, Block A, 1st Floor, Laketown, Kolkata - 700089

**Rajarhat Centre:**  
Laxmi Apartment, 1st Floor, Dashadrone, Checkpost, Rajarhat Main Road, next to Urban Greens, above Vrindavan Sweets, Kolkata 700136

---

> Built to make MathPath’s website more interactive, parent-friendly, and commercially ready through an AI-powered, brand-safe, Agentic RAG chatbot.
