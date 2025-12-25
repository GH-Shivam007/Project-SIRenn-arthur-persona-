# 🚨 SIREN: Autonomous Counter-Espionage Agent

> **"Don't just block the scammers. Break them."**

**SIREN** is an intelligent, autonomous cybersecurity agent designed to execute **Economic Denial of Service (EDoS)** attacks against cybercriminals. Instead of passively filtering phishing emails, SIREN engages attackers using a hyper-realistic AI persona ("Arthur"), wasting their time, draining their resources, and ultimately tracking their location via honeytoken traps.

---

## 💡 The Problem
* **Asymmetry:** Scammers use automation to target millions of victims at near-zero cost.
* **Passive Defense:** Traditional spam filters hide threats but do nothing to stop the attacker's operations.
* **The Gap:** There is no active defense system that imposes a *cost* on the attacker.

## 🛡️ The Solution
SIREN automates the "victim." It deploys **Arthur V5**—an 82-year-old, tech-illiterate, wealthy, and panicked persona—to reply to scams.

1.  **Bait:** Arthur engages with the scammer, asking naive questions.
2.  **Stall:** The AI acts incompetent (typos, "broken" buttons, confusion) to keep the scammer hooked for hours.
3.  **Trap:** When the scammer demands proof of payment, Arthur sends a **Honeytoken Link** (Grabify).
4.  **Report:** Once the link is clicked, the attacker's IP and location are captured and reported to the CyberDesk.

---

## 🚀 Key Features

* **🧠 Adaptive AI Brain:** Powered by **Google Gemini 2.5 Flash**, Arthur adapts his fears based on the threat context (e.g., panic about "Heart Meds" for package scams, or "Life Savings" for bank scams).
* **🕸️ The Honeytoken Trap:** Automatically deploys a tracking link disguised as a "cloud receipt" when the attacker demands proof.
* **🛡️ Economic Denial of Service:** Uses smart rate-limiting and infinite conversation loops to waste human scammer labor.
* **🏢 CyberDesk Integration (SOAR):** Automatically files an incident report with the Security Operations Center (SOC) the moment a trap is deployed.
* **💻 War Room UI:** A "Hollywood-style" CLI dashboard with real-time threat alerts and status updates.
* **⚡ Auto-Recovery:** Built-in handling for API Rate Limits (Error 429) to ensure 24/7 uptime.

---

## 🛠️ Tech Stack

* **Core Logic:** Python 3.9+
* **AI Model:** Google Gemini 2.5 Flash (via REST API)
* **Networking:** `requests`, `imaplib`, `smtplib` (Native Protocol Support)
* **Security:** `python-dotenv` for credential management
* **Interface:** `colorama` for CLI visualization

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/project-siren.git](https://github.com/yourusername/project-siren.git)
cd project-siren
