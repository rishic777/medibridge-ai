import { useNavigate } from "react-router-dom";
import Button from "../components/Button";
import Card from "../components/Card";

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="mb-page mb-landing">
      <header className="mb-header">
        <div className="mb-header__logo">MediBridge AI</div>
        <nav className="mb-header__nav">
          <a href="#how-it-works">How it works</a>
          <a href="#trust">Help</a>
          <select aria-label="Language" defaultValue="en">
            <option value="en">English</option>
            <option value="hi">हिन्दी</option>
          </select>
        </nav>
      </header>

      <section className="mb-hero">
        <h1>Your story matters.</h1>
        <p className="mb-hero__subtitle">Tell us what you're feeling.</p>

        <div className="mb-hero__actions">
          <Button onClick={() => navigate("/register")}>🎤 Start speaking</Button>
          <Button variant="secondary" onClick={() => navigate("/register")}>
            Type instead
          </Button>
        </div>

        <p className="mb-hero__trust">Secure • Multilingual • Doctor reviewed</p>
      </section>

      <section id="how-it-works" className="mb-how">
        <h2>How it works</h2>
        <ol className="mb-how__steps">
          <li>Tell your story</li>
          <li>AI organizes information</li>
          <li>Answer relevant questions</li>
          <li>Doctor reviews history</li>
        </ol>
      </section>

      <section id="trust" className="mb-trust">
        <Card>
          <strong>Patient reported</strong> → <strong>Document supported</strong> → <strong>Doctor verified</strong>
          <p>Every piece of information in your history carries a clear source, so nothing is presented as fact until a clinician confirms it.</p>
        </Card>
      </section>
    </div>
  );
}
