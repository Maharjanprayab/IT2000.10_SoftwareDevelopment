import typer
import json
from pathlib import Path
from rich.table import Table
from rich.console import Console

app = typer.Typer()

BOOKMARK_FILE = Path("bookmark.json")


#This function checks if the file exists and loads the file.
def load_file():
    if BOOKMARK_FILE.exists():
        with open(BOOKMARK_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}


#This function saves a bookmark in the file.
def save_file(bookmark):
    with open(BOOKMARK_FILE, 'w') as file:
        json.dump(bookmark, file, indent=4)



@app.command(help="This command adds the bookmark")
def add(name:str, url:str):
    bookmarks = load_file()
    bookmarks[name] = url
    save_file(bookmarks)
    print(f"Bookmark '{name}' successfully added")


@app.command(help="This command list all the commands")
def list():
    bookmark = load_file()
    table = Table(title = "Bookmarks")
    table.add_column("Name")
    table.add_column("URL")

    for name, url in bookmark.items():
        table.add_row(name, url)

    console = Console()
    console.print(table)

@app.command(help="This command removes bookmark with specific name")
def remove(name: str):
    bookmark = load_file()

    if name in bookmark:
        del bookmark[name]
        save_file(bookmark)
        print(f"Bookmark with name '{name}' has been removed from the list.")

    else:
        print(f"Bookmark with name '{name}' doesnot exists in the list.")


@app.command(help="This command searches for the bookmark in the list")
def search(query:str):
    bookmark = load_file()
    table = Table(title=f"Search for the book mark with name '{query}'")
    table.add_column("Name")
    table.add_column("URL")
    
    result = {name: url for name, url in bookmark.items() if query.lower() in name.lower() or query.lower() in url.lower()}

    for name, url in result.items():
        table.add_row(name, url)
        
    if result:
        console = Console()
        console.print(table)
    else:
        print(f"The bookmark with name '{query}' or url '{query}' doesnot exist.")


@app.command(help="This command lets you to edit any bookmark that has been registered in the list.")
def edit(option: str = typer.Option(..., prompt="Choose an option: ", help = "Enter 'a' if you want to change name. Enter 'b' if you want to change url.")):
    bookmark = load_file()
    option = option.lower()
    if option == "a":
        old = input("Enter the old name: ")
        if old in bookmark:
            val = bookmark.pop(old)
            new = input("Enter the new name: ")
            bookmark[new] = val
            save_file(bookmark)
            print(f"Bookmark with the url '{val}' had it's name changed form '{old}' to '{new}'")
        else:
            print(f"Bookmark with name '{old}' does not exists.")
    elif option =="b":
        name = input("Enter the name of the bookmark that you want to change: ")
        if name in bookmark:
            val = bookmark[name]
            new = input("Enter the new url: ")
            bookmark[name] = new
            save_file(bookmark)
            print(f"The url of the bookmark '{name}' has been changed from'{val}' to '{new}'")
        else:
            print(f"The bookmark with name '{name}' does not exists in the list.")
    else:
        print(f"Choose either 'a' or 'b'.")





if __name__ == "__main__":
    app()
