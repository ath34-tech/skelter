<p align="center">
  <img src="https://file.trae.ai/67e2310114972f0932c02450/1742880155013/d46d7904-7a0e-4361-b4f3-c5f7823e2003.png" alt="Skelter Logo" width="600">
</p>

<h1 align="center">🦴 Skelter</h1>

<p align="center">
  <strong>The AI Architect for Modern Developers</strong>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-how-it-works">How it Works</a>
</p>

---

**Skelter** is not just another boilerplate generator. It's a professional-grade AI architect that understands your **usecase** and handles the most boring parts of starting a project: planning the architecture, creating the folder structure, and writing the documentation.

In seconds, Skelter delivers a production-ready skeleton complete with a **PRD**, **HLD**, and a **Technical Walkthrough**.

## ✨ Features

- 🧠 **Usecase-Aware**: Tell Skelter what you're building (e.g., "A travel app with map integration"), and it designs the architecture specifically for that.
- 📚 **Triple-Doc Generation**: Automatically generates three essential documents:
  - `PRD.md` (Product Requirements)
  - `HLD.md` (High-Level Design)
  - `walkthrough.md` (Developer Guide)
- �️ **Full-Stack Orchestration**: Seamlessly handles frontend and backend separation (e.g., FastAPI + React).
- 🧹 **Clean Codebase**: Generates only what you need. No scaffolding bloat, no unnecessary comments.
- 🚀 **Professional CLI**: Built with `uv` and `typer` for a lightning-fast, modern developer experience.

## 🚀 Installation

The most professional way to install Skelter is as a global tool using [uv](https://github.com/astral-sh/uv):

```bash
# Clone the repo
git clone https://github.com/your-username/skelter.git
cd skelter

# Install globally
uv tool install .
```

## 🎯 Quick Start

### 1. Configure your API Key
Skelter uses Groq's Llama 3.3 for lightning-fast architectural planning.

```bash
skelter config --key "YOUR_GROQ_API_KEY"
```

### 2. Initialize a Project
Describe your stack and your vision. Skelter handles the rest.

```bash
skelter init --stack "FastAPI + React" --name "trip-planner" --usecase "A travel booking app with map integration"
```

## 🏗️ How it Works

1. **Planning Phase**: Skelter's AI analyzes your usecase and stack to design a custom folder structure.
2. **Review**: You get to review the suggested tree and make manual edits if needed.
3. **Generation**: Skelter creates every directory and file locally on your machine.
4. **Documentation**: The AI writes your PRD, HLD, and Walkthrough based on the final structure.

---

<p align="center">
  Built with 🦴 by developers, for developers.
</p>
