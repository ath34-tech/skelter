from rich.tree import Tree
from rich.console import Console
from rich import print as rprint

console = Console()


def render_tree(folders, files, title="📁 Project Structure"):
    """Render a beautiful tree of folders and files using Rich."""
    tree_data: dict = {}

    # Build nested dict from folder paths
    for folder in sorted(folders):
        parts = folder.split("/")
        cur = tree_data
        for p in parts:
            cur = cur.setdefault(p, {})

    # Attach files to their parent folder nodes
    loose_files = []
    for f in sorted(files):
        if "/" in f:
            parts = f.split("/")
            cur = tree_data
            # navigate to parent dir
            for p in parts[:-1]:
                cur = cur.setdefault(p, {})
            # store file under sentinel key
            cur.setdefault("__files__", []).append(parts[-1])
        else:
            loose_files.append(f)

    def _build(rich_node: Tree, d: dict):
        for k, v in sorted(d.items()):
            if k == "__files__":
                for fname in v:
                    rich_node.add(f"[dim white]📄 {fname}[/dim white]")
            else:
                sub = rich_node.add(f"[bold cyan]📂 {k}/[/bold cyan]")
                _build(sub, v)

    root = Tree(f"[bold yellow]{title}[/bold yellow]")
    _build(root, tree_data)

    for lf in loose_files:
        root.add(f"[dim white]📄 {lf}[/dim white]")

    console.print(root)