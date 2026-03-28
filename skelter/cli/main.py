import typer
import os
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.rule import Rule
from rich import box
from rich.text import Text

from skelter.cli.renderer import render_tree
from skelter.cli.prompts import edit_structure
from skelter.server.agent.planner import plan_architecture, generate_prd, generate_hld, generate_walkthrough
from skelter.server.core.utils import clean_json_response
from dotenv import load_dotenv

console = Console()
app = typer.Typer(
    help="🦴 Skelter — AI-powered project architect",
    add_completion=False,
    rich_markup_mode="rich",
)

BANNER = """[bold yellow]
  ██████  ██ ▄█▀▓█████  ██▓  ▄▄▄█████▓▓█████  ██▀███  
▒██    ▒  ██▄█▒ ▓█   ▀ ▓██▒  ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒
░ ▓██▄   ▓███▄░ ▒███   ▒██░  ▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒
  ▒   ██▒▓██ █▄ ▒▓█  ▄ ▒██░  ░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄  
▒██████▒▒▒██▒ █▄░▒████▒░██████▒▒██▒ ░ ░▒████▒░██▓ ▒██▒
▒ ▒▓▒ ▒ ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒░▓  ░▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░▒  ░ ░░ ░▒ ▒░ ░ ░  ░░ ░ ▒  ░  ░     ░ ░  ░  ░▒ ░ ▒░
░  ░  ░  ░ ░░ ░    ░     ░ ░   ░         ░     ░░   ░ 
      ░  ░  ░      ░  ░    ░  ░          ░  ░   ░     
[/bold yellow]"""


def _print_banner():
    console.print(BANNER)
    console.print(
        Panel(
            "[dim]AI-powered project architect · Plan · Scaffold · Document[/dim]",
            border_style="yellow",
            padding=(0, 4),
        )
    )
    console.print()


def load_env():
    env_path = Path(".env")
    if not env_path.exists():
        parent_env = Path("skelter/.env")
        if parent_env.exists():
            env_path = parent_env
    load_dotenv(env_path)


@app.command()
def init(
    stack: str = typer.Option(..., "--stack", "-s", help="Tech stack (e.g. 'FastAPI + React')"),
    name: str = typer.Option(None, "--name", "-n", help="Project name"),
    usecase: str = typer.Option(None, "--usecase", "-u", help="What are you building?"),
):
    """
    🚀 Initialize a new project with AI-designed architecture & full documentation.
    """
    _print_banner()
    load_env()

    if not os.getenv("GROQ_API_KEY"):
        console.print(
            Panel(
                "[bold red]GROQ_API_KEY not found.[/bold red]\n"
                "Run [bold cyan]skelter config --key YOUR_KEY[/bold cyan] first.",
                title="[red]❌ Configuration Error[/red]",
                border_style="red",
            )
        )
        raise typer.Exit()

    # ── Gather project info ─────────────────────────────────────────────────
    if not name:
        name = Prompt.ask(
            "  [bold cyan]Project name[/bold cyan]",
            default="my-skelter-project",
        )
    if not usecase:
        usecase = Prompt.ask(
            "  [bold cyan]What are you building?[/bold cyan]",
            default="general purpose app",
        )

    safe_name = name.lower().replace(" ", "-")
    output_dir = Path("generated") / safe_name

    # ── Summary panel ───────────────────────────────────────────────────────
    summary = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    summary.add_row("[bold]Project[/bold]", f"[cyan]{name}[/cyan]")
    summary.add_row("[bold]Stack[/bold]",   f"[magenta]{stack}[/magenta]")
    summary.add_row("[bold]Use-case[/bold]", f"[white]{usecase}[/white]")
    summary.add_row("[bold]Output[/bold]",  f"[green]{output_dir}[/green]")
    console.print(Panel(summary, title="[bold yellow]📋 Project Details[/bold yellow]", border_style="bright_blue"))
    console.print()

    try:
        # ── Phase 1: Architecture planning ───────────────────────────────────
        with Progress(
            SpinnerColumn(spinner_name="dots", style="bold yellow"),
            TextColumn("[bold yellow]{task.description}"),
            TimeElapsedColumn(),
            transient=True,
            console=console,
        ) as progress:
            task = progress.add_task("🤖  Planning architecture with AI...", total=None)
            response = plan_architecture(stack, usecase)
            arch = clean_json_response(response.content)
            progress.update(task, description="✅  Architecture ready!")

        console.print(Rule("[bold yellow]Suggested Structure[/bold yellow]"))
        render_tree(arch["folders"], arch["files"])
        console.print()

        # ── Edit prompt ──────────────────────────────────────────────────────
        want_edit = Confirm.ask("  [bold]Do you want to edit this structure?[/bold]", default=False)
        if want_edit:
            edit_structure(arch["folders"], arch["files"], stack=stack, usecase=usecase)
            console.print(Rule("[bold yellow]Updated Structure[/bold yellow]"))
            render_tree(arch["folders"], arch["files"])
            console.print()

        if not Confirm.ask("  [bold green]Proceed with this structure?[/bold green]", default=True):
            console.print(Panel("[bold red]Aborted.[/bold red]", border_style="red"))
            raise typer.Exit()

        # ── Phase 2: Create directories/files ────────────────────────────────
        output_dir.mkdir(parents=True, exist_ok=True)

        all_paths = arch["folders"] + arch["files"]
        with Progress(
            SpinnerColumn(spinner_name="dots2", style="cyan"),
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(bar_width=30, style="cyan", complete_style="green"),
            TextColumn("[green]{task.completed}/{task.total}[/green]"),
            console=console,
        ) as progress:
            task = progress.add_task("📁  Creating project structure...", total=len(all_paths))
            for folder in arch["folders"]:
                (output_dir / folder).mkdir(parents=True, exist_ok=True)
                progress.advance(task)
            for file in arch["files"]:
                fp = output_dir / file
                fp.parent.mkdir(parents=True, exist_ok=True)
                if not fp.exists():
                    fp.touch()
                progress.advance(task)

        # ── Phase 3: Documentation generation ───────────────────────────────
        docs = [
            ("📝  Generating PRD...",        lambda: generate_prd(stack, usecase)),
            ("🏗  Generating HLD...",         lambda: generate_hld(stack, usecase, arch["folders"], arch["files"])),
            ("📖  Generating Walkthrough...", lambda: generate_walkthrough(stack, usecase, arch["folders"], arch["files"])),
        ]
        doc_results = {}

        with Progress(
            SpinnerColumn(spinner_name="moon", style="magenta"),
            TextColumn("[bold magenta]{task.description}"),
            TimeElapsedColumn(),
            transient=True,
            console=console,
        ) as progress:
            for label, fn in docs:
                t = progress.add_task(label, total=None)
                doc_results[label] = fn()
                progress.update(t, description=label.replace("Generating", "✅ Done:"))

        # Write docs
        (output_dir / "PRD.md").write_text(list(doc_results.values())[0].content, encoding="utf-8")
        (output_dir / "HLD.md").write_text(list(doc_results.values())[1].content, encoding="utf-8")
        (output_dir / "walkthrough.md").write_text(list(doc_results.values())[2].content, encoding="utf-8")

        # ── Success ──────────────────────────────────────────────────────────
        success_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
        success_table.add_row("📁", f"[cyan]{output_dir}[/cyan]")
        success_table.add_row("📄", "[green]PRD.md[/green]")
        success_table.add_row("📐", "[green]HLD.md[/green]")
        success_table.add_row("📖", "[green]walkthrough.md[/green]")

        console.print()
        console.print(
            Panel(
                success_table,
                title=f"[bold green]✨ '{name}' initialized successfully![/bold green]",
                border_style="green",
                padding=(1, 2),
            )
        )

    except typer.Exit:
        raise
    except Exception as e:
        console.print(
            Panel(
                f"[bold red]{e}[/bold red]",
                title="[red]❌ Error[/red]",
                border_style="red",
            )
        )


@app.command()
def config(
    key: str = typer.Option(..., "--key", "-k", help="Your Groq API key"),
):
    """
    🔑 Save your Groq API key to .env.
    """
    env_path = Path(".env")
    if not env_path.exists():
        parent_env = Path("skelter/.env")
        if parent_env.exists():
            env_path = parent_env

    with open(env_path, "w") as f:
        f.write(f"GROQ_API_KEY={key}\n")

    console.print(
        Panel(
            f"[green]API key saved to[/green] [bold cyan]{env_path}[/bold cyan]",
            title="[green]✅ Config Saved[/green]",
            border_style="green",
        )
    )


@app.command()
def version():
    """
    🦴 Show current Skelter version.
    """
    console.print(
        Panel(
            "[bold yellow]🦴 Skelter[/bold yellow]  [dim]v0.1.0[/dim]\n"
            "[dim]Built with ❤️  for developers, by developers[/dim]",
            border_style="yellow",
            padding=(0, 2),
        )
    )


def run():
    app()


if __name__ == "__main__":
    run()