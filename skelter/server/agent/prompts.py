ARCH_PROMPT = """
You are a senior full-stack software architect.
A developer wants to generate a clean, scalable project skeleton for a specific usecase.

User requested tech stack:
{stack}

Usecase:
{usecase}

Your task:
Design a modern, practical folder structure tailored to the provided usecase. 
If the stack includes both frontend and backend (e.g., "FastAPI + React"), organize them into distinct subdirectories (e.g., 'backend/', 'frontend/').

Architecture guidelines:
- Use layered architecture principles.
- Include clear separation of concerns.
- For backends: prefer folders like api, services, models, db, core.
- For frontends: prefer folders like src, components, hooks, services, assets.
- Ensure the folders and files reflect the specific needs of the '{usecase}' usecase.
- Include a tests folder for each part.
- List all necessary files with their paths relative to the project root.
- Keep structure realistic and minimal.

IMPORTANT:
Return ONLY valid JSON. No explanations, markdown, or comments.

Output format must be EXACTLY:
{{
  "folders": ["folder/path", "folder/path"],
  "files": ["file/path.ext", "file/path.ext"]
}}
"""

PRD_PROMPT = """
Generate a professional Product Requirements Document (PRD) for the following application:

Tech Stack: {stack}
Usecase: {usecase}

The PRD should include:
1. **Introduction**: Purpose and vision.
2. **Target Audience**: Who is this for?
3. **User Stories**: Key scenarios.
4. **Functional Requirements**: List of what the app MUST do.
5. **Non-Functional Requirements**: Performance, security, etc.
6. **Success Metrics**: How to measure impact.

Return ONLY the markdown content.
"""

WALKTHROUGH_PROMPT = """
Generate a Technical Walkthrough for the following project structure:

Tech Stack: {stack}
Usecase: {usecase}
Folders: {folders}
Files: {files}

The walkthrough should explain:
1. **Project Setup**: How to get it running.
2. **Folder Explanation**: What each folder is for.
3. **Feature Implementation**: Where to start coding the core features.
4. **Next Steps**: Suggestions for the developer.

Return ONLY the markdown content.
"""

HLD_PROMPT = """
Generate a High-Level Design (HLD) document for the following application:

Tech Stack: {stack}
Usecase: {usecase}
Folders: {folders}
Files: {files}

The HLD should include:
1. **System Architecture**: Overall design pattern.
2. **Component Design**: Key frontend and backend modules.
3. **Data Flow**: How data moves through the system.
4. **API Design (Conceptual)**: Main endpoints.
5. **Database Schema**: Key tables and relationships.

Return ONLY the markdown content.
"""

REFINE_PROMPT = """
You are a senior software architect helping a developer refine their project structure.

Current project structure:
Tech Stack: {stack}
Usecase: {usecase}

Current folders:
{folders}

Current files:
{files}

The developer wants to make the following change:
"{instruction}"

Your task:
Apply the requested change to the structure. You may add, remove, or rename folders and files.
Keep the overall architecture consistent and professional.
Do NOT include any explanations — only return the updated structure as valid JSON.

IMPORTANT:
- All file and folder paths must be relative to project root (no leading slashes).
- Preserve paths that are unaffected by the change.
- Return ONLY valid JSON. No markdown, no commentary.

Output format must be EXACTLY:
{{
  "folders": ["folder/path", "folder/path"],
  "files": ["file/path.ext", "file/path.ext"]
}}
"""