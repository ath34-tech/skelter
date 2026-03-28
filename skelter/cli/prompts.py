from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich import box
from skelter.cli.renderer import render_tree

console = Console()


def _show_menu():
    table = Table(box=box.ROUNDED, show_header=False, border_style="bright_blue", padding=(0, 2))
    table.add_row("[bold cyan]1[/bold cyan]", "➕  Add folder")
    table.add_row("[bold cyan]2[/bold cyan]", "📄  Add file")
    table.add_row("[bold cyan]3[/bold cyan]", "🗑  Remove folder")
    table.add_row("[bold cyan]4[/bold cyan]", "🗑  Remove file")
    table.add_row("[bold magenta]6[/bold magenta]", "🤖  AI Edit  [dim](describe a change in plain English)[/dim]")
    table.add_row("[bold green]5[/bold green]", "💾  Save & continue")
    console.print(
        Panel(table, title="[bold yellow]✏️  Edit Structure[/bold yellow]", border_style="bright_blue")
    )


def edit_structure(folders, files, stack: str = "", usecase: str = ""):
    """
    Interactive edit loop.
    `stack` and `usecase` are forwarded to the AI-edit option so the LLM
    has the full context when refining the structure.
    """
    while True:
        _show_menu()
        action = Prompt.ask(
            "[bold white]Choose action[/bold white]",
            choices=["1", "2", "3", "4", "5", "6"],
        )

        if action == "1":
            folder_path = Prompt.ask("  [cyan]New folder path[/cyan]")
            folders.append(folder_path)
            console.print(f"  [green]✔ Added folder:[/green] [bold]{folder_path}[/bold]")

        elif action == "2":
            file_path = Prompt.ask("  [cyan]New file path[/cyan]")
            files.append(file_path)
            console.print(f"  [green]✔ Added file:[/green] [bold]{file_path}[/bold]")

        elif action == "3":
            folder_path = Prompt.ask("  [red]Folder path to remove[/red]")
            if folder_path in folders:
                folders.remove(folder_path)
                console.print(f"  [green]✔ Removed folder:[/green] [bold]{folder_path}[/bold]")
            else:
                console.print(f"  [red]✘ Folder not found:[/red] [bold]{folder_path}[/bold]")

        elif action == "4":
            file_path = Prompt.ask("  [red]File path to remove[/red]")
            if file_path in files:
                files.remove(file_path)
                console.print(f"  [green]✔ Removed file:[/green] [bold]{file_path}[/bold]")
            else:
                console.print(f"  [red]✘ File not found:[/red] [bold]{file_path}[/bold]")

        elif action == "6":
            _ai_edit(folders, files, stack, usecase)

        elif action == "5":
            console.print("\n  [bold green]💾 Saving structure...[/bold green]")
            render_tree(folders, files)
            break


def _ai_edit(folders: list, files: list, stack: str, usecase: str):
    """Send a natural-language instruction to the LLM and apply its updated structure in-place."""
    # Import here to avoid circular deps at module load
    from skelter.server.agent.planner import refine_structure
    from skelter.server.core.utils import clean_json_response

    console.print(
        Panel(
            "[dim]Describe what you want to change in plain English.\n"
            'Example: [italic cyan]"add a Redis caching layer to the backend"[/italic cyan]\n'
            'Example: [italic cyan]"remove the tests folder from frontend"[/italic cyan]\n'
            'Example: [italic cyan]"add a notifications microservice alongside backend"[/italic cyan][/dim]',
            title="[bold magenta]🤖 AI Edit[/bold magenta]",
            border_style="magenta",
        )
    )

    instruction = Prompt.ask("  [bold magenta]Your instruction[/bold magenta]")
    if not instruction.strip():
        console.print("  [yellow]⚠ No instruction entered — skipping.[/yellow]")
        return

    with Progress(
        SpinnerColumn(spinner_name="dots", style="bold magenta"),
        TextColumn("[bold magenta]{task.description}"),
        TimeElapsedColumn(),
        transient=True,
        console=console,
    ) as progress:
        task = progress.add_task("🤖  AI is refining the structure...", total=None)
        try:
            response = refine_structure(stack, usecase, list(folders), list(files), instruction)
            updated = clean_json_response(response.content)
            progress.update(task, description="✅  Done!")
        except Exception as e:
            progress.stop()
            console.print(
                Panel(
                    f"[bold red]{e}[/bold red]",
                    title="[red]❌ AI Edit Failed[/red]",
                    border_style="red",
                )
            )
            return

    # Apply changes in-place so the caller's lists are mutated
    folders.clear()
    folders.extend(updated.get("folders", []))
    files.clear()
    files.extend(updated.get("files", []))

    console.print(
        Panel(
            f'[green]Applied:[/green] [italic]"{instruction}"[/italic]',
            title="[bold green]✅ AI Edit Applied[/bold green]",
            border_style="green",
        )
    )
    console.print()
    render_tree(folders, files, title="🤖 AI-Updated Structure")
