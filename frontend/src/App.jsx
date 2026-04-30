import ChatWidget from "./components/ChatWidget.jsx";

export default function App() {
  const params = new URLSearchParams(window.location.search);
  const embedMode = params.get("embed") === "1" || params.get("embed") === "true";

  if (embedMode) {
    return <ChatWidget />;
  }

  return (
    <main className="mathpath-demo-page">
      <section className="mathpath-demo-hero">
        <img src="/MathPath-Logo.png" alt="MathPath Ace with Abacus" className="mathpath-demo-logo" />
        <h1>MathPath AI Chatbot Preview</h1>
        <p>
          This page previews the production-ready floating chatbot widget before it is integrated into the MathPath website.
          The bot connects to the deployed FastAPI backend and answers parent enquiries using the MathPath knowledge base.
        </p>
      </section>
      <ChatWidget />
    </main>
  );
}
