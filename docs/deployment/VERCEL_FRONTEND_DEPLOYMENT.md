# MathPath AI Chatbot — Vercel Frontend Deployment

This guide deploys the React/Vite chatbot frontend with the MathPath logo, floating widget, suggested questions, and lead form.

## 1. Create a Vercel project

1. Go to Vercel.
2. Click **Add New Project**.
3. Import the GitHub repository.
4. Set the frontend directory as the project root:

```text
frontend
```

## 2. Build settings

Use:

```bash
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

The project includes `vercel.json`.

## 3. Add environment variable

In Vercel → Settings → Environment Variables:

```env
VITE_MATHPATH_API_URL=https://your-render-backend-url.onrender.com
```

Redeploy after adding the variable.

## 4. Verify pages

Preview page:

```text
https://your-vercel-chatbot-url.vercel.app/
```

Embed-only chatbot page:

```text
https://your-vercel-chatbot-url.vercel.app/?embed=1&open=1
```

## 5. Verify public embed script

The file is available at:

```text
https://your-vercel-chatbot-url.vercel.app/mathpath-chatbot-embed.js
```

Use this script URL when integrating into the MathPath website.
