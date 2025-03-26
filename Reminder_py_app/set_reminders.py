import json
import os
from datetime import datetime

# Get the actual home directory path
HOME = os.path.expanduser("~")
reminder_path = os.path.join(HOME, "reminders.json")
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_reminder(task, reminder_time, reminder_date):
    try:
        # Validate task is not empty
        if not task.strip():
            print("Task cannot be empty")
            return False

        # Validate and set default date if empty
        if reminder_date.strip() == '':
            reminder_date = datetime.now().strftime('%Y-%m-%d')
        else:
            try:
                # Validate date format
                datetime.strptime(reminder_date, '%Y-%m-%d')
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD")
                return False

        # Validate time format
        if ':' in reminder_time:
            try:
                hr, min = reminder_time.split(':')
                hr = int(hr)
                min = int(min)
                
                if hr > 23:
                    print('Invalid hour format - must be between 0-23')
                    return False
                if min > 59:
                    print('Invalid minute format - must be between 0-59')
                    return False
                
            except ValueError:
                print("Use digits only for time format")
                return False
        else:
            print('Invalid time format - use HH:MM')
            return False

        # Format time with leading zeros
        reminder_time = f'{hr:02d}:{min:02d}'
                # Parse the reminder_date to get the day of the week
        reminder_day = datetime.strptime(reminder_date, '%Y-%m-%d').strftime('%A')

        # Load existing reminders or create new list
        try:
            with open(reminder_path, 'r') as f:
                reminders = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            reminders = []

        # Add new reminder
        reminder = {
            'task': task,
            'time': reminder_time,
            'date': reminder_date,
            'day' : reminder_day,
            'completed' : False
        }
        reminders.append(reminder)

        # Save updated reminders
        with open(reminder_path, 'w') as f:
            json.dump(reminders, f, indent=2)
            
        print(f"\nReminder set for {reminder_date} at {reminder_time} on {reminder_day}")
        return True

    except KeyboardInterrupt:
        print('\nExiting')
        return False

def view_reminders():
    try:
        with open(reminder_path, 'r') as f:
            reminders = json.load(f)
            if not reminders:
                print("\nNo reminders set!")
                return
            
            print("\nYour Reminders:")
            for i, rem in enumerate(reminders, 1):
                print(f"{i}. Task: {rem['task']}")
                print(f'   Day: {rem['day']}')
                print(f"   Date: {rem['date']} at {rem['time']}\n")
    except (FileNotFoundError, json.JSONDecodeError):
        print("\nNo reminders found!")
    
    input("\nPress Enter to continue...")

def delete_reminder():
    try:
        with open(reminder_path, 'r') as f:
            reminders = json.load(f)
            if not reminders:
                print("\nNo reminders to delete!")
                return
            
        print("\nSelect reminder to delete:")
        for i, rem in enumerate(reminders, 1):
            print(f"{i}. {rem['task']} - {rem['date']} at {rem['time']}")
            
        choice = input("\nEnter number to delete (or 0 to cancel): ")
        if choice.isdigit():
            choice = int(choice)
            if 0 < choice <= len(reminders):
                deleted = reminders.pop(choice-1)
                with open(reminder_path, 'w') as f:
                    json.dump(reminders, f, indent=2)
                print(f"\nDeleted: {deleted['task']}")
            elif choice != 0:
                print("Invalid choice!")
        else:
            print('Invalid choice!')
                
    except (FileNotFoundError, json.JSONDecodeError):
        print("\nNo reminders found!")
    
    input("\nPress Enter to continue...")

def main():
    try:
        while True:
            clear_screen()
            print("=== Reminder App ===")
            print("1. Add Reminder")
            print("2. View Reminders")
            print("3. Delete Reminder")
            print("4. Exit")
            choice = input("\nChoose an option (1-4): ")
            
            if choice == '1':
                clear_screen()
                print("=== Add New Reminder ===")
                set_reminder(
                    task=input('\nAdd task: ').strip(),
                    reminder_time=input('Add time in HH:MM (24hr)format: ').strip(),
                    reminder_date=input('Add reminder date(yyyy-mm-dd) or press ENTER for Today: ').strip()
                )
                
                input("\nPress Enter to continue...")
            
            elif choice == '2':
                clear_screen()
                print("=== View Reminders ===")
                view_reminders()
                
            elif choice == '3':
                clear_screen()
                print("=== Delete Reminder ===")
                delete_reminder()
                
            elif choice == '4':
                print("\nGoodbye!")
                break
            
            else:
                print("\nInvalid choice!")
                input("Press Enter to continue...")
    except KeyboardInterrupt:
        print('\nProgram closed by user Interaction\n')
if __name__ == '__main__':
    main()
    # Keep window open on Windows
    if os.name == 'nt':
        input("\nPress Enter to exit...")