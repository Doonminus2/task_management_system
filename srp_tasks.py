# oop_tasks.py (ต่อจาก Class Task)
from abc import ABC, abstractmethod

class TaskStorage(ABC):
    @abstractmethod
    def load_tasks(self):
        pass
    @abstractmethod
    def save_tasks(self, tasks):
        pass

class FileTaskStorage(TaskStorage):
    def __init__(self, filename = "tasks.txt"):
        self.filename = filename
    
    def load_tasks(self):
        loaded_tasks = []
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 5:
                        task_id = int(parts[0])
                        description = parts[1]
                        due_date = parts[2]
                        completed = parts[3] == "True"
                        priority = parts[4]
                        loaded_tasks.append(Task(task_id, description, due_date, completed, priority))
                    elif len(parts) == 4:
                        task_id = int(parts[0])
                        description = parts[1]
                        due_date = parts[2]
                        completed = parts[3] == "True"
                        loaded_tasks.append(Task(task_id, description, due_date, completed))
        except FileNotFoundError:
            print(f"NO existing task file {self.filename} found. Starting fresh.")
        return loaded_tasks
    def save_tasks(self, tasks):
        with open(self.filename, "w") as f:
            for task in tasks:
                f.write(f"{task.id},{task.description},{task.due_date},{task.completed},{task.priority}\n")
            print(f"Tasks saved to {self.filename}")



class Task:
    VALID_PRIORITIES = ("low", "medium", "high")

    def __init__(self, task_id, description, due_date=None, completed=False, priority="medium"):
        self.id = task_id
        self.description = description
        self.due_date = due_date
        self.completed = completed
        if priority.lower() not in self.VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of {self.VALID_PRIORITIES}, got '{priority}'")
        self.priority = priority.lower()
        
        
    def mark_completed(self):
        self.completed = True
        print(f"Task {self.id} '{self.description}' marked as completed.")

    def __str__(self):
        status = "✓" if self.completed else " "
        due = f" (Due: {self.due_date})" if self.due_date else ""
        priority_icon = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(self.priority, "⚪")
        return f"[{status}] {self.id}. {self.description}{due} | Priority: {priority_icon} {self.priority}"

class TaskManager:
    def __init__(self, storage: TaskStorage):
        self.storage = storage
        self.tasks = self.storage.load_tasks()
        self.next_id = max([t.id for t in self.tasks]) + 1 if self.tasks else 1
        print(f"Loaded {len(self.tasks)} tasks.Next ID: {self.next_id}")


    def add_task(self, description, due_date=None, priority="medium"):
        task = Task(self.next_id, description, due_date, priority=priority)
        self.tasks.append(task)
        self.next_id += 1
        print(f"Task '{description}' added.")
        return task

    def list_tasks(self):
        print("\n--- Current Tasks ---")
        if not self.tasks:
            print("No tasks available.")
            return
        for task in self.tasks:
            print(task)
        print("---------------------")

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def mark_task_completed(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_completed()
            self.storage.save_tasks(self.tasks)
            return True
        print(f"Task {task_id} not found.")
        return False


if __name__ == "__main__":
    file_storage = FileTaskStorage("My_tasks.txt")
    manager = TaskManager(file_storage)
    manager.list_tasks()
    manager.add_task("Review SOLID Principles", "2026-08-28", priority="high")
    manager.add_task("Practice OOP", "2026-08-30", priority="low")
    manager.list_tasks()
    manager.mark_task_completed(1)
    manager.list_tasks()
