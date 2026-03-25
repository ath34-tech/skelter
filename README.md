<p align="center">
  <img src="logo_2.png" alt="Skelter Logo" width="600">
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

### Option 1: Standalone Binary (One-Click Download)
The easiest way to use Skelter. No Python, Pip, or UV installation is needed.

[![Download Skelter](https://img.shields.io/badge/Download-skelter.exe-blue?style=for-the-badge&logo=windows)](https://github.com/ath34-tech/skelter/releases/download/v1.0.0/skelter.exe)

1. **[Download skelter.exe](https://github.com/ath34-tech/skelter/releases/download/v1.0.0/skelter.exe)**
2. **Move** it to any folder on your computer.
3. **(Optional) Add to PATH**: Move the file to a folder already in your system PATH (like `C:\Windows`) to use `skelter` from any terminal.

### Option 2: For Developers (Python & Pip)
If you already have Python installed and want to run Skelter as a package:

```bash
# Install directly from source
pip install .
```

### Option 3: Modern Tooling (Using [uv](https://github.com/astral-sh/uv))
```bash
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

## 🛠️ For Maintainers

### How to update the one-click download link
To make the "One-Click Download" link work, you must:
1.  **Create a Release**: Go to your GitHub repository → **Releases** → **Create a new release**.
2.  **Tag it**: Give it a version tag (e.g., `v1.0.0`).
3.  **Upload the Binary**: Drag and drop the `dist/skelter.exe` file into the "Attach binaries" area.
4.  **Publish**: Once published, the "latest/download/skelter.exe" link in this README will automatically point to the newest version.
