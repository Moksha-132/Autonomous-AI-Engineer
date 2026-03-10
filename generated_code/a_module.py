class TaskManager:
    def __init__(self):
        self.tasks = {}

    def add_task(self, name, description):
        if name in self.tasks:
            print(f"Task '{name}' already exists.")
            return
        new_task = {
            'name': name,
            'description': description,
            'complete': False
        }
        self.tasks[name] = new_task

    def delete_task(self, name):
        if name not in self.tasks:
            print(f"No task found with the name '{name}'.")
            return
        del self.tasks[name]

    def complete_task(self, name):
        if name not in self.tasks:
            print(f"No task found with the name '{name}'.")
            return
        if self.tasks[name]['complete']:
            print(f"Task '{name}' is already marked as complete.")
            return
        self.tasks[name]['complete'] = True

    def list_tasks(self):
        for name, task in self.tasks.items():
            status = "Complete" if task['complete'] else "Not Complete"
            print(f"{name}: {status} - {task['description']}")

def main():
    manager = TaskManager()

    while True:
        print("\n1. Add Task")
        print("2. Delete Task")
        print("3. Complete Task")
        print("4. List Tasks")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter task name: ")
            description = input("Enter task description: ")
            manager.add_task(name, description)
        elif choice == "2":
            name = input("Enter task name to delete: ")
            manager.delete_task(name)
        elif choice == "3":
            name = input("Enter task name to complete: ")
            manager.complete_task(name)
        elif choice == "4":
            manager.list_tasks()
        elif choice == "5":
            print("Exiting task manager.")
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()
