import typer
from skelter.cli.renderer import render_tree


def edit_structure(folders,files):
    while True:
        typer.echo("\nChoose action from list:")
        typer.echo("1. Add folder")
        typer.echo("2. Add file")
        typer.echo("3. Remove folder")
        typer.echo("4. Remove file")
        typer.echo("5. Save")
        action=typer.prompt(" ")
        if action=="1":
            typer.echo("\n enter folder path:")
            folder_path=typer.prompt(" ")
            folders.append(folder_path)
        elif action=="2":
            typer.echo("\n enter file path:")
            file_path=typer.prompt(" ")
            files.append(file_path)
        elif action=="3":
            typer.echo("\n enter folder path to remove:")
            folder_path=typer.prompt(" ")
            if folder_path in folders:
                folders.remove(folder_path)
            else:
                typer.echo("\n folder not found")
        elif action=="4":
            typer.echo("\n enter file path to remove:")
            file_path=typer.prompt(" ")
            if file_path in files:
                files.remove(file_path)
            else:
                typer.echo("\n file not found")
        elif action=="5":
            typer.echo("\n saving structure...")
            render_tree(folders,files)
            break
        else:
            typer.echo("\n invalid action")
