from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import os
import re
import shutil
from pathlib import Path


# Instantiate a console object
console = Console()


def list_files(directory):
    """List all files in the given directory."""
    try:
        files = os.listdir(directory)
        table = Table(title=f"Files in [bold green]{directory}[/bold green]")
        table.add_column("File Name", style="dim")
        for file in files:
            table.add_row(file)
        console.print(table)
    except FileNotFoundError:
        console.print("[bold red]Directory not found.[/bold red]")



def move_file(directory, file, target_directory):
    """Move the given file from the current directory to the target directory."""
    try:
        shutil.move(os.path.join(directory, file), os.path.join(target_directory, file))
        console.print(f"[bold green]{file}[/bold green] has been moved from [bold blue]{directory}[/bold blue] to [bold yellow]{target_directory}[/bold yellow]")
    except FileNotFoundError:
        console.print("[bold red]Directory or file not found.[/bold red]")


def search_files(directory, pattern):
    """Search files in the given directory that match the given regex pattern."""
    try:
        files = os.listdir(directory)
        matches = [file for file in files if re.search(pattern, file)]
        table = Table(title=f"Files in [bold green]{directory}[/bold green] matching [bold blue]{pattern}[/bold blue]")
        table.add_column("Matching File Name", style="dim")
        for match in matches:
            table.add_row(match)
        console.print(table)
    except FileNotFoundError:
        console.print("[bold red]Directory not found.[/bold red]")

def search_and_move(directory, pattern):
    """Search files in the given directory that match the given regex pattern."""
    try:
        files = os.listdir(directory)
        matches = [file for file in files if re.search(pattern, file)]
        for match in matches:
            if "log" in match:

                if os.path.exists("./logs"):
                    move_file(directory, match,"./logs")
                else:
                    os.makedirs("./logs")
                    move_file(directory, match, "./logs")
            if "email" in match:
    
                if os.path.exists("./emails"):
                    move_file(directory, match,"./emails")
                else:
                    os.makedirs("./emails")
                    move_file(directory, match, "./emails")
            if "document" in match:
                
                if os.path.exists("./documents"):
                    move_file(directory, match,"./documents")
                else:
                    os.makedirs("./documents")
                    move_file(directory, match, "./documents")

            
    except FileNotFoundError:
        console.print("[bold red]Directory not found.[/bold red]")

def check_for_errors_and_warnings(file):
    open_file = open(file)
    read_file = open_file.read()
    split_file = read_file.split("\n")
    return_warning_string = ""
    retrun_error_string = ""
    for line in split_file:
        if "WARNING" in line:
            return_warning_string += f"{line}\n"

        if "ERROR" in line:
            retrun_error_string += f"{line}\n"

    if retrun_error_string:
        if os.path.exists("./error_collection"):
            with open("./error_collection/errors.txt", "w") as open_file:
                open_file.write(f'{retrun_error_string}\n')

        else:
            os.makedirs("./error_collection")
            Path('./error_collection/errors.txt').touch()
            with open("./error_collection/errors.txt", "w") as open_file:
                open_file.write(f'{retrun_error_string}\n')

            

    if return_warning_string:
        if os.path.exists("./warning_collection"):
             with open("./warning_collection/warnings.txt", "w") as open_file:
                open_file.write(f'{return_warning_string}\n')

        else:
            os.makedirs("./warning_collection")
            Path('./warning_collection/warnings.txt').touch()
            with open("./warning_collection/warnings.txt", "w") as open_file:
                open_file.write(f'{return_warning_string}\n')


def main():
    """Main function to run the CLI app."""
    while True:
        console.print("\n1. List files\n2. Move file\n3. Search files\n4. Create a folder\n5. Sort folder\n6. Parse a file for errors and warnings\n7. Delete\n8. Exit")
        choice = Prompt.ask("Choose a task (Enter the number)", choices=['1', '2', '3', '4','5','6','7'], default='4')

        if choice == '1':
            directory = Prompt.ask("Enter the directory to list files")
            list_files(directory)


        elif choice == '2':
            directory = Prompt.ask("Enter the current directory of the file")
            file = Prompt.ask("Enter the file to move")
            target_directory = Prompt.ask("Enter the target directory to move the file to")
            move_file(directory, file, target_directory)


        elif choice == '3':
            directory = Prompt.ask("Enter the directory to search files")
            pattern = Prompt.ask("Enter the regex pattern to search for")
            search_files(directory, pattern)


        elif choice == "4":
            directory = Prompt.ask("Enter the name of the folder you want to create.")
            if os.path.exists(f"./{directory}"):
                Prompt.ask("Folder has already been created, enter 1 to return")
            else:
                target_directory = os.makedirs(f"./{directory}")


        elif choice == "5":
            directory = Prompt.ask("Enter the directory to search")
            file = Prompt.ask("Enter the file to sort")
            if os.path.exists(f"./{directory}"):
                search_and_move(directory, file)
            else:
                console.print("[bold red]Directory or file not found.[/bold red]")

        
        elif choice == "6":
            directory = Prompt.ask("Enter the directory to search for a file to parse")
            file = Prompt.ask("Enter the file to parse")
            check_for_errors_and_warnings(f'{directory}/{file}') 


        elif choice == "7":
            directory = Prompt.ask("Enter the directory to search for a file to delete")
            file = Prompt.ask("Enter the file to delete")
            if os.path.exists(f"./{directory}"):
                move_file(directory, file, "./deleted_files")
            else:
                target_directory = os.makedirs("./deleted_files")
                move_file(directory, file, target_directory)


        else:
            break


if __name__ == "__main__":
    main()