import typer
import os
import subprocess
from pathlib import Path
from skelter.cli.renderer import render_tree
from skelter.cli.prompts import edit_structure
from skelter.server.agent.planner import plan_architecture, generate_prd, generate_hld, generate_walkthrough
from skelter.server.core.utils import clean_json_response
from dotenv import load_dotenv

app = typer.Typer(help="🦴 Skelter AI Boilerplate Generator")

def load_env():
    env_path = Path(".env")
    if not env_path.exists():
        parent_env = Path("skelter/.env")
        if parent_env.exists():
            env_path = parent_env
    load_dotenv(env_path)

@app.command()
def init(
    stack: str = typer.Option(..., "--stack", "-s", help="Describe tech stack (e.g., 'FastAPI + React')"),
    name: str = typer.Option(None, "--name", "-n", help="Project name (e.g., 'my-cool-app')"),
    usecase: str = typer.Option(None, "--usecase", "-u", help="Describe usecase (e.g., 'travel app')")
):
    """
    Initialize a new project with architecture planning and walkthrough.
    """
    load_env()
    if not os.getenv("GROQ_API_KEY"):
        typer.echo("❌ GROQ_API_KEY not found. Please run 'skelter config --key YOUR_KEY' first.")
        raise typer.Exit()

    if not name:
        name = typer.prompt("🚀 Enter project name", default="my-skelter-project")
    
    if not usecase:
        usecase = typer.prompt("🎯 What kind of app are we making? (usecase)", default="general purpose app")

    safe_name = name.lower().replace(" ", "-")
    output_dir = Path("generated") / safe_name

    typer.echo(f"🚀 Initializing project '{name}' for stack: {stack}")
    typer.echo(f"🎯 Usecase: {usecase}")
    typer.echo(f"📂 Output directory: {output_dir}")

    try:
        typer.echo("🤖 Planning architecture...")
        response = plan_architecture(stack, usecase)
        arch = clean_json_response(response.content)
        
        typer.echo("\n📁 Suggested Structure:")
        render_tree(arch["folders"], arch["files"])

        typer.echo("\nDo you want to edit this structure? (Y/N):")
        edit = typer.prompt(" ", default="N")
        if edit.lower() == "y":
            edit_structure(arch["folders"], arch["files"])
            typer.echo("\n📁 Updated Structure:")
            render_tree(arch["folders"], arch["files"])

        if not typer.confirm("\nProceed with this structure?", default=True):
            typer.echo("❌ Aborted.")
            raise typer.Exit()

        output_dir.mkdir(parents=True, exist_ok=True)
        
        typer.echo(f"📁 Creating structure in {output_dir}...")
        for folder in arch["folders"]:
            (output_dir / folder).mkdir(parents=True, exist_ok=True)
        
        for file in arch["files"]:
            file_path = output_dir / file
            file_path.parent.mkdir(parents=True, exist_ok=True)
            if not file_path.exists():
                file_path.touch()

        typer.echo("📝 Generating project documentation (PRD, HLD, Walkthrough)...")
        
        prd_resp = generate_prd(stack, usecase)
        walk_resp = generate_walkthrough(stack, usecase, arch["folders"], arch["files"])
        hld_resp = generate_hld(stack, usecase, arch["folders"], arch["files"])
        
        with open(output_dir / "PRD.md", "w", encoding="utf-8") as f:
            f.write(prd_resp.content)
        
        with open(output_dir / "HLD.md", "w", encoding="utf-8") as f:
            f.write(hld_resp.content)
            
        with open(output_dir / "walkthrough.md", "w", encoding="utf-8") as f:
            f.write(walk_resp.content)

        typer.echo(f"\n✨ Project '{name}' initialized successfully in ./{output_dir}!")
        typer.echo("📚 Documentation generated: PRD.md, HLD.md, walkthrough.md")

    except Exception as e:
        typer.echo(f"❌ Error: {e}")


@app.command()
def config(
    key: str = typer.Option(..., "--key", "-k", help="Groq API Key")
):
    """
    Configure your Groq API Key
    """
    env_path = Path(".env")
    
    # Also check if we are in a subfolder and .env is in parent
    if not env_path.exists():
        parent_env = Path("skelter/.env")
        if parent_env.exists():
            env_path = parent_env

    with open(env_path, "w") as f:
        f.write(f"GROQ_API_KEY={key}\n")
    
    typer.echo("✅ Groq API Key saved to .env!")


@app.command()
def version():
    """
    Show current version
    """
    typer.echo("🦴 Skelter v0.1.0")


def run():
    app()


if __name__ == "__main__":
    run()