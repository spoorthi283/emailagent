
import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [section, setSection] = useState("compose");

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [history, setHistory] = useState([]);

  async function sendPrompt(event) {
    event.preventDefault();
    setLoading(true);
    setResponse("");
    setMessage("");

    try {
      const res = await fetch(`${API_URL}/api/agent`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Request failed");
      }

      setResponse(JSON.stringify(data, null, 2));
      setPrompt("");
    } catch (error) {
      setResponse(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function saveContact(event) {
    event.preventDefault();
    setMessage("");

    try {
      const res = await fetch(`${API_URL}/api/contacts`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Could not save contact");
      }

      setMessage(data.message || "Contact saved successfully.");
      setName("");
      setEmail("");
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  }

  async function loadHistory() {
    setSection("history");
    setMessage("");

    try {
      const res = await fetch(`${API_URL}/api/history`);
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Could not load history");
      }

      setHistory(Array.isArray(data) ? data : data.history || []);
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-icon">A</span>
          <div>
            <h2>MailPilot</h2>
            <small>AI EMAIL ASSISTANT</small>
          </div>
        </div>

        <p className="nav-label">WORKSPACE</p>

        <button
          className={section === "compose" ? "nav active" : "nav"}
          onClick={() => setSection("compose")}
        >
          <span>✉</span> AI Email Composer
        </button>

        <button
          className={section === "contacts" ? "nav active" : "nav"}
          onClick={() => {
            setSection("contacts");
            setMessage("");
          }}
        >
          <span>♧</span> Contacts
        </button>

        <button
          className={section === "history" ? "nav active" : "nav"}
          onClick={loadHistory}
        >
          <span>◷</span> Email History
        </button>

        <div className="sidebar-footer">
          <span className="status-dot" />
          AI Email Agent
          <small>Local workspace</small>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <p className="eyebrow">YOUR WORKSPACE</p>
            <h1>
              {section === "compose"
                ? "AI Email Composer"
                : section === "contacts"
                ? "Contact Management"
                : "Email History"}
            </h1>
          </div>
          <span className="user-avatar">AI</span>
        </header>

        <div className="content">
          {section === "compose" && (
            <>
              <section className="welcome-card">
                <div>
                  <span className="welcome-tag">✦ AI POWERED</span>
                  <h2>Emails, made effortless.</h2>
                  <p>
                    Describe what you want to communicate. Your AI agent
                    will process your request using your existing backend.
                  </p>
                </div>
                <div className="welcome-art">✉</div>
              </section>

              <section className="panel">
                <div className="panel-heading">
                  <div>
                    <h2>Compose with AI</h2>
                    <p>Write your request in natural language.</p>
                  </div>
                  <span className="step-badge">01 / COMPOSE</span>
                </div>

                <form onSubmit={sendPrompt}>
                  <label htmlFor="prompt">Your instruction</label>
                  <textarea
                    id="prompt"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Example: Send an email to Rinku thanking them for the meeting..."
                    required
                    rows={5}
                  />

                  <div className="form-footer">
                    <span>Be specific about the recipient and purpose.</span>
                    <button className="primary-btn" disabled={loading}>
                      {loading ? "Processing..." : "Run AI Agent →"}
                    </button>
                  </div>
                </form>
              </section>

              {response && (
                <section className="panel result-panel">
                  <div className="panel-heading">
                    <div>
                      <h2>Agent Response</h2>
                      <p>Result returned by your FastAPI backend.</p>
                    </div>
                  </div>
                  <pre>{response}</pre>
                </section>
              )}
            </>
          )}

          {section === "contacts" && (
            <section className="panel">
              <div className="panel-heading">
                <div>
                  <h2>Add a contact</h2>
                  <p>Save a name and email address in SQLite.</p>
                </div>
              </div>

              <form onSubmit={saveContact} className="contact-form">
                <label htmlFor="name">Contact name</label>
                <input
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Enter contact name"
                  required
                />

                <label htmlFor="email">Email address</label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  required
                />

                <button className="primary-btn">Save Contact</button>
              </form>

              {message && <p className="notice">{message}</p>}
            </section>
          )}

          {section === "history" && (
            <section className="panel">
              <div className="panel-heading">
                <div>
                  <h2>Recent email activity</h2>
                  <p>Records retrieved from your backend.</p>
                </div>
                <button className="secondary-btn" onClick={loadHistory}>
                  Refresh
                </button>
              </div>

              {message && <p className="notice">{message}</p>}

              {history.length === 0 ? (
                <p className="empty-state">No email history found yet.</p>
              ) : (
                <div className="history-list">
                  {history.map((item) => (
                    <article className="history-item" key={item.id}>
                      <div className="history-icon">✉</div>
                      <div className="history-details">
                        <strong>{item.subject}</strong>
                        <p>To: {item.recipient}</p>
                        <small>{item.created_at || "Date unavailable"}</small>
                      </div>
                      <span
                        className={
                          item.status === "sent"
                            ? "status-pill sent"
                            : "status-pill"
                        }
                      >
                        {item.status}
                      </span>
                    </article>
                  ))}
                </div>
              )}
            </section>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
