#!/usr/bin/env python3

import os
from pathlib import Path

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_symlink():
    home = Path.home()
    desktop = home / "Desktop"
    if not desktop.exists():
        print("Error: Desktop directory not found.")
        return

    file_name = input("filename: ").strip()
    if not file_name:
        print("Error: No filename entered.")
        return

    matches = list(home.rglob(file_name))

    if not matches:
        print("Error: No files found.")
        return

    # Bonus task: multiple matches
    if len(matches) > 1:
        print(f"Which file?")
        for i, path in enumerate(matches, 1):
            print(f"{i} - {path}")
        while True:
            choice = input(f"Please select the file you want (1-{len(matches)}): ").strip()
            if not choice.isdigit() or not (1 <= int(choice) <= len(matches)):
                print("Please enter a valid number.")
            else:
                target = matches[int(choice) - 1]
                break
    else:
        target = matches[0]

    link_path = desktop / target.name
    if link_path.exists():
        print(f"Error: '{target.name}' already exists.")
        return

    try:
        os.symlink(target, link_path)
        print(f"Symlink created: {target}")
    except PermissionError:
        print("Error: Permission denied.")
    except Exception as e:
        print(f"Error: {e}")

def delete_symlink():
    home = Path.home()
    desktop = home / "Desktop"

    links = [f for f in desktop.iterdir() if f.is_symlink()]

    if not links:
        print("No symlinks found.")
        return

    print("Symlinks:")

    for i, link in enumerate(links, 1):
        print(f"{i} - {link.name} -> {os.readlink(link)}")

    while True:
        choice = input(f"\nPlease select the symlink to delete (1-{len(links)}): ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(links)):
            print("Please enter a valid number.")
        else:
            link_to_delete = links[int(choice) - 1]
            try:
                link_to_delete.unlink()
                print(f"Deleted symlink '{link_to_delete.name}'.")
            except Exception as e:
                print(f"Error: {e}")
            break

def generate_report():
    home = Path.home()
    desktop = home / "Desktop"

    links = [f for f in desktop.iterdir() if f.is_symlink()]

    if not links:
        print("No symlinks found.")
        return

    for link in links:
        try:
            target = os.readlink(link)
            print(f"{link.name} → {target}")
        except Exception as e:
            print(f"Error: {e}")

    # Count all symbolic links in home directory
    all_links = [p for p in desktop.rglob('*') if p.is_symlink()]
    print(f"{len(all_links)} symlinks found.")

def main():
    os.system("clear")
    while True:
        print("1 - Create a symbolic link")
        print("2 - Delete a symbolic link")
        print("3 - Generate a symbolic link report")
        print("4 - Quit")

        choice = input("Select an option (1-4): ").strip().lower()

        if choice == '4':
            print("Goodbye.")
            break
        elif choice == '1':
            create_symlink()
        elif choice == '2':
            delete_symlink()
        elif choice == '3':
            generate_report()
        else:
            print("Invalid input.")
        print()

if __name__ == "__main__":
    main()
