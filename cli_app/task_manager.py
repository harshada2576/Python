"""Core task management functionality"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class TaskManager:
    """Manages tasks with persistence to JSON file"""
    
    def __init__(self, data_file: str = "tasks.json"):
        """Initialize TaskManager with data file path"""
        self.data_file = data_file
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> List[Dict]:
        """Load tasks from JSON file"""
        if not os.path.exists(self.data_file):
            return []
        
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    def _save_tasks(self) -> None:
        """Save tasks to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self, description: str, priority: str = "medium") -> Dict:
        """Add a new task"""
        task = {
            "id": self._get_next_id(),
            "description": description,
            "priority": priority.lower(),
            "completed": False,
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        self.tasks.append(task)
        self._save_tasks()
        return task
    
    def _get_next_id(self) -> int:
        """Get next available task ID"""
        if not self.tasks:
            return 1
        return max(task["id"] for task in self.tasks) + 1
    
    def list_tasks(self, show_completed: bool = False, priority: Optional[str] = None) -> List[Dict]:
        """List tasks with optional filters"""
        filtered_tasks = self.tasks
        
        if not show_completed:
            filtered_tasks = [t for t in filtered_tasks if not t["completed"]]
        
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t["priority"] == priority.lower()]
        
        return filtered_tasks
    
    def complete_task(self, task_id: int) -> Optional[Dict]:
        """Mark a task as completed"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat()
                self._save_tasks()
                return task
        return None
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID"""
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks.pop(i)
                self._save_tasks()
                return True
        return False
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """Get a specific task by ID"""
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def get_statistics(self) -> Dict:
        """Get task statistics"""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        pending = total - completed
        
        by_priority = {"high": 0, "medium": 0, "low": 0}
        for task in self.tasks:
            if not task["completed"]:
                priority = task.get("priority", "medium")
                if priority in by_priority:
                    by_priority[priority] += 1
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "by_priority": by_priority
        }
