# Task Manager CLI

A practical command-line task management tool built with Python. Manage your tasks efficiently from the terminal with features for adding, listing, completing, and deleting tasks.

## Features

- ✅ **Add tasks** with priority levels (high, medium, low)
- 📋 **List tasks** with filters (all, pending, by priority)
- ✓ **Complete tasks** to mark them as done
- 🗑️ **Delete tasks** to remove them permanently
- 📊 **View statistics** about your tasks
- 💾 **Persistent storage** using JSON
- 🎨 **Color-coded output** for better visibility

## Installation

No external dependencies required! Just Python 3.6+

```bash
cd cli_app
```

## Usage

### Add a Task

```bash
python task.py add "Buy groceries"
python task.py add "Finish report" -p high
python task.py add "Call dentist" --priority low
```

### List Tasks

```bash
# List pending tasks only
python task.py list

# List all tasks (including completed)
python task.py list --all
python task.py list -a

# Filter by priority
python task.py list -p high
python task.py list --priority medium
```

### Complete a Task

```bash
python task.py complete 1
```

### Delete a Task

```bash
python task.py delete 2
```

### View Statistics

```bash
python task.py stats
```

### Help

```bash
python task.py --help
python task.py add --help
```

## Examples

```bash
# Add some tasks
python task.py add "Complete project documentation" -p high
python task.py add "Review pull requests" -p medium
python task.py add "Update dependencies" -p low

# List all pending tasks
python task.py list

# Complete task #1
python task.py complete 1

# View statistics
python task.py stats

# List all tasks including completed
python task.py list --all

# Delete a task
python task.py delete 3
```

## Data Storage

Tasks are stored in `tasks.json` in the same directory as the script. This file is automatically created when you add your first task.

## Features Explained

### Priority Levels

- **High** (red): Urgent tasks that need immediate attention
- **Medium** (yellow): Regular priority tasks
- **Low** (blue): Tasks that can be done later

### Color Coding

- ✓ Green checkmark: Completed tasks
- ○ Circle: Pending tasks
- Different colors for priority levels

### Task Information

Each task stores:

- Unique ID
- Description
- Priority level
- Completion status
- Creation timestamp
- Completion timestamp (if completed)

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## License

Open source - feel free to use and modify!
