import json
import os

# Define the file name where we will save our tasks
# Using a constant makes it easy to change the file name later if needed
FILE_NAME = "tasks.json"

def load_tasks_from_file():
    """Reads tasks from the JSON file. Returns an empty list if file doesn't exist."""
    # Check if the file exists before trying to open it
    if not os.path.exists(FILE_NAME):
        return []
    
    # Try to open and read the file
    try:
        with open(FILE_NAME, "r") as file:
            # json.load turns the file content into a Python list
            tasks = json.load(file)
            return tasks
    except:
        # If there's any error (like a corrupted file), return an empty list
        return []

def save_tasks_to_file(tasks_list):
    """Saves the current list of tasks into the JSON file."""
    try:
        with open(FILE_NAME, "w") as file:
            # json.dump saves the list into the file with nice formatting (indent=4)
            json.dump(tasks_list, file, indent=4)
    except:
        print("Oops! There was an error saving your tasks.")

def show_all_tasks(tasks_list):
    """Displays tasks in a nice table format."""
    if len(tasks_list) == 0:
        print("\nYour to-do list is empty!")
        return

    # Print a nice header for our table
    print("\n" + "=" * 55)
    print("ID    | Task Description               | Status")
    print("-" * 55)
    
    # Loop through each task and print its details
    for task in tasks_list:
        task_id = str(task["id"]).ljust(5)
        
        # Limit description length so it doesn't break the table
        description = task["description"]
        if len(description) > 30:
            description = description[:27] + "..."
        description = description.ljust(30)
        
        status = task["status"].ljust(10)
        
        print(f"{task_id} | {description} | {status}")
    
    print("=" * 55 + "\n")

def add_new_task(tasks_list):
    """Asks the user for a task and adds it to the list."""
    user_input = input("What do you need to do? ").strip()
    
    if user_input == "":
        print("Error: You can't add an empty task!")
        return

    # Find the next ID for the new task
    highest_id = 0
    for task in tasks_list:
        if task["id"] > highest_id:
            highest_id = task["id"]
    
    new_id = highest_id + 1
    
    # Create the task dictionary
    new_task = {
        "id": new_id,
        "description": user_input,
        "status": "Pending"
    }
    
    # Add to our list and save to file
    tasks_list.append(new_task)
    save_tasks_to_file(tasks_list)
    print("Task added successfully!")

def edit_existing_task(tasks_list):
    """Changes the description or status of a task."""
    show_all_tasks(tasks_list)
    
    if len(tasks_list) == 0:
        return

    user_id_input = input("Enter the ID of the task you want to edit: ")
    
    # Try to find the task with that ID
    target_task = None
    for task in tasks_list:
        if str(task["id"]) == user_id_input:
            target_task = task
            break
            
    if target_task == None:
        print("Could not find a task with that ID.")
        return

    # Ask for new description
    print(f"Current description: {target_task['description']}")
    new_desc = input("Enter new description (leave blank to keep current): ").strip()
    if new_desc != "":
        target_task["description"] = new_desc

    # Ask to update status
    status_input = input("Is this task finished? (yes/no): ").lower()
    if status_input == "yes" or status_input == "y":
        target_task["status"] = "Completed"
    else:
        target_task["status"] = "Pending"

    save_tasks_to_file(tasks_list)
    print("Task updated!")

def remove_task_from_list(tasks_list):
    """Deletes a task from the list."""
    show_all_tasks(tasks_list)
    
    if len(tasks_list) == 0:
        return

    user_id_input = input("Enter the ID of the task to remove: ")
    
    # Look for the task and remove it
    found = False
    for i in range(len(tasks_list)):
        if str(tasks_list[i]["id"]) == user_id_input:
            tasks_list.pop(i)
            found = True
            break
            
    if found:
        save_tasks_to_file(tasks_list)
        print("Task removed!")
    else:
        print("Task ID not found.")

def run_to_do_app():
    """The main loop of the application."""
    while True:
        # Always reload tasks to make sure we have the latest data
        tasks = load_tasks_from_file()
        
        print("\n--- SIMPLE TO-DO MENU ---")
        print("1. View My Tasks")
        print("2. Add a Task")
        print("3. Edit a Task")
        print("4. Remove a Task")
        print("5. Exit Program")
        
        choice = input("What would you like to do? (1-5): ")
        
        if choice == "1":
            show_all_tasks(tasks)
        elif choice == "2":
            add_new_task(tasks)
        elif choice == "3":
            edit_existing_task(tasks)
        elif choice == "4":
            remove_task_from_list(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please pick a number between 1 and 5.")

# This line tells Python to start the app when we run this file
if __name__ == "__main__":
    run_to_do_app()
