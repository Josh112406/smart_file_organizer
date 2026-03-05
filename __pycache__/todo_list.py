import json
import os
from colorama import init, Fore, Style
from tabulate import tabulate


class TodoList:
    PRIORITY_LEVELS = ("low", "medium", "high")

    def __init__(self, file: str = "todo.json", create: bool = False):
        self.cur_dir = os.getcwd()
        self.file_name = file if file.endswith(".json") else f"{file}.json"
        self.file_path = os.path.join(self.cur_dir, self.file_name)
        self.exists = os.path.exists(self.file_path)

        if not self.exists and create:
            with open(self.file_path, "w") as f:
                json.dump([], f)
            self.exists = True
        self.data: list[dict] = self._load_tasks()

    def clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def _load_tasks(self) -> list[dict]:
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r") as f:
                content = json.load(f)
                return content if isinstance(content, list) else []
        except (json.JSONDecodeError, IOError):
            return []

    def _save_tasks(self) -> None:
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def display_tasks(self) -> None:
        if not self.data:
            print("File has no content")
            return

        display_data = []
        status_colors = {
            "pending": Fore.RED,
            "in progress": Fore.YELLOW,
            "done": Fore.GREEN,
        }
        priority_level_colors = {
            "high": Fore.RED,
            "medium": Fore.YELLOW,
            "low": Fore.GREEN,
        }

        for index, task in enumerate(self.data, start=1):
            status = task["status"]
            status_colored = (
                status_colors.get(status, Fore.WHITE) + status + Style.RESET_ALL
            )
            priority_level = task["priority_level"]
            priority_level_colored = (
                priority_level_colors.get(priority_level, Fore.WHITE)
                + priority_level
                + Style.RESET_ALL
            )
            display_data.append(
                [
                    str(index),
                    task["name"],
                    task["description"],
                    priority_level_colored,
                    status_colored,
                ]
            )

        headers = ["No.", "Name", "Description", "Priority", "Status"]
        print(tabulate(display_data, headers=headers, tablefmt="fancy_grid"))

    def add_tasks(self) -> None:
        self.data = self._load_tasks()
        while True:
            try:
                task_name = input("Name of the task: ")
                if not task_name.strip():
                    print("Please enter a task name.")
                    continue

                description = input("Task description: ")
                if not description.strip():
                    print("Please enter a description.")
                    continue
                priority_level = input("Priority level (Low/Medium/High): ").lower()

                print()
                if priority_level in self.PRIORITY_LEVELS:
                    new_task = {
                        "name": task_name,
                        "description": description,
                        "status": "pending",
                        "priority_level": priority_level,
                    }
                    self.data.append(new_task)
                else:
                    print("\nPlease enter a valid choice!\n")
                    continue

                again = input("Add another task? (y/n): ").lower()
                if again == "y":
                    print()
                    continue

                self._save_tasks()
                self.display_tasks()
                break
            except ValueError:
                print("Enter a valid value.")
            except KeyboardInterrupt:
                print("\nClosing...")
                break

    def delete_tasks(self) -> None:
        self.display_tasks()
        while True:
            try:
                index = int(input("What task do you want to remove? (No.): "))
                if 1 <= index <= len(self.data):
                    self.data.pop(index - 1)
                    self.clear_screen()
                    self._save_tasks()
                    self.display_tasks()

                    if not self.data:
                        break

                    resume = input("Do you want to remove more? (y/n): ").lower()
                    if resume == "y":
                        self.clear_screen()
                        continue
                    break
                else:
                    print("Enter a valid number! ")
                    continue
            except ValueError:
                print("Enter a number!")
                continue

    def mark_tasks(self) -> None:
        self.display_tasks()
        statuses = {1: "done", 2: "in progress", 3: "pending"}
        while True:
            try:
                to_mark = int(input("Please select task to mark: "))
                if not (1 <= to_mark <= len(self.data)):
                    print("Select a valid task! ")
                    continue

                print("\nMark as: \n[1] Done \n[2] In progress \n[3] Pending \n")
                status_option = int(input("-> "))
                if status_option not in statuses:
                    print("Select a valid status option!")
                    continue

                new_status = statuses[status_option]
                task_index = to_mark - 1

                if self.data[task_index]["status"] == new_status:
                    self.clear_screen()
                    print(f"Current task is already {new_status}")
                    self.display_tasks()
                    continue

                self.data[task_index]["status"] = new_status
                self._save_tasks()
                self.display_tasks()
                resume = input("\nDo you want to update more tasks? (y/n): ")
                if resume.lower() == "y":
                    continue
                break

            except (KeyboardInterrupt, ValueError):
                print()
                break

    def edit_tasks(self) -> None:
        self.display_tasks()
        option_list = {1: "name", 2: "description", 3: "priority_level"}
        while True:
            try:
                to_edit = int(input("Please select task to edit: "))
                if not (1 <= to_edit <= len(self.data)):
                    print("Select a valid task! ")
                    continue

                task_index = to_edit - 1
                print("\n[1] Name \n[2] Description \n[3] Priority Level\n")
                option = int(input("-> "))

                if option not in option_list:
                    print("Select a valid option!")
                    continue

                field = option_list[option]
                prompt_text = (
                    f"Enter new {field.replace('_', ' ')} for task #{to_edit}: "
                )

                if option == 3:
                    prompt_text = f"Enter new priority level for task #{to_edit} ({'/'.join(self.PRIORITY_LEVELS)}): "

                new_value = input(prompt_text)

                if option == 3:
                    new_value = new_value.lower()
                    if new_value not in self.PRIORITY_LEVELS:
                        print("Please enter a valid priority level!\n")
                        continue

                if self.data[task_index][field] == new_value:
                    print(f"Please enter different {field.replace('_', ' ')}! ")
                    continue

                self.data[task_index][field] = new_value
                self._save_tasks()
                self.display_tasks()

                edit_more = input("Do you want to edit more? (y/n): ")
                if edit_more.lower() != "y":
                    break

            except (KeyboardInterrupt, ValueError):
                print()
                break

    def sort_tasks(self) -> None:
        self.display_tasks()
        level_map = {"high": 1, "medium": 2, "low": 3}
        status_map = {"done": 1, "in progress": 2, "pending": 3}
        option_list = {1: "priority_level", 2: "status"}

        try:
            print("\nSort by:\n[1] Priority level \n[2] Status")
            option = int(input("\n->"))

            if option not in option_list:
                print("Select a valid option!")
                return

            print("\nSort:\n[1] Ascending\n[2] Descending\n- Leave blank for default")
            reverse_input = input("\n->")
            reverse = reverse_input == "2"

            if option == 1:
                self.data.sort(
                    key=lambda x: level_map.get(x["priority_level"], 99),
                    reverse=reverse,
                )
            elif option == 2:
                self.data.sort(
                    key=lambda x: status_map.get(x["status"], 99), reverse=reverse
                )

            self._save_tasks()
            self.display_tasks()

        except (KeyboardInterrupt, ValueError):
            print()
            return


def main():
    init(autoreset=True)
    tabulate.WIDE_CHARS_MODE = False
    print()
    choices = """
Simple python Todo List program
Options:
[1] Create new Todo list
[2] Add new tasks
[3] Load Todo list (default: todo.json)
[4] Update Todo list
[5] Mark task as complete
"""
    print(choices, end="\n")

    while True:
        try:
            choice = int(input("-> "))
            if 1 <= choice <= 5:
                if choice == 1:
                    file_name = input("Save file as: ")
                    todo = TodoList(file_name, create=True)
                    if todo.exists and todo.data:
                        print(f"File {todo.file_name} already exists.")
                        break
                    todo.add_tasks()
                    break
                elif choice == 2:
                    file_name = input("File to open: ")
                    todo = TodoList(file_name)
                    if todo.exists:
                        todo.add_tasks()
                        break
                    else:
                        print(f"The file {file_name} does not exist.")
                        break
                elif choice == 3:
                    file_name = input("File name: ")
                    todo = TodoList(file_name)
                    if todo.exists:
                        todo.display_tasks()
                        print(
                            """
Loaded actions:
[1] Add task
[2] Delete task
[3] Update task
[4] Mark task
[5] Sort task
"""
                        )
                        option = int(input("-> "))
                        if not (1 <= option <= 5):
                            print("Please enter a valid choice.")
                            break
                        if option == 1:
                            todo.add_tasks()
                        elif option == 2:
                            todo.delete_tasks()
                        elif option == 3:
                            todo.edit_tasks()
                        elif option == 4:
                            todo.mark_tasks()
                        elif option == 5:
                            todo.sort_tasks()
                        break
                    else:
                        print(f"The file {file_name} does not exist.")
                        break
                elif choice == 4:
                    file_name = input("File name: ")
                    todo = TodoList(file_name)
                    if not todo.exists:
                        answer = input(
                            "The file does not exist. Do you want to create a new one? (y/n): \n-> "
                        )
                        if answer.lower() == "y":
                            TodoList(file_name, True)
                            print(choices)
                        else:
                            break
                    else:
                        todo.edit_tasks()
                        break
                elif choice == 5:
                    file_name = input("File name: ")
                    todo = TodoList(file_name)
                    if todo.exists:
                        todo.mark_tasks()
                        break
                    else:
                        print(f"File {file_name} does not exist.")
                        break
        except ValueError:
            print("Select a valid choice.")
            break
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
