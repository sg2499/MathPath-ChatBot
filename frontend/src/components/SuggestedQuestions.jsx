const questions = [
  "Which MathPath program is right for my child?",
  "My child is weak in maths. Can MathPath help?",
  "What is the Bridge Course?",
  "How does daily practice work?",
  "Do you have online or hybrid classes?",
  "How can I book a free demo?"
];

export default function SuggestedQuestions({ onSelect, disabled }) {
  return (
    <div className="mp-suggestions" aria-label="Suggested questions">
      {questions.map((question) => (
        <button
          key={question}
          type="button"
          className="mp-suggestion-chip"
          onClick={() => onSelect(question)}
          disabled={disabled}
        >
          {question}
        </button>
      ))}
    </div>
  );
}
