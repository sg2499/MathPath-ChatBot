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
        <h1>MathPath ChatBot</h1>
        <p>
          MathPath helps children build strong maths fundamentals through abacus, visualisation, and
          school-syllabus-aligned learning. Our programs are designed to improve speed, accuracy,
          focus, and confidence in mathematics for different age groups.
        </p>
      </section>
      <ChatWidget />
    </main>
  );
}
