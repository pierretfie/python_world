import json
from json.decoder import JSONDecodeError
from datetime import datetime
from plyer import notification
import platform
import os
import sys
import signal
import atexit
from time import sleep


reminder_path = os.path.expanduser('~/')
def save_reminders(reminders):
    """safely save reminders to file using a temporary file"""
    try:
        #write to a temporary file first
        temp_file = 'reminders.temp.json'
        with open(os.path.join(reminder_path, temp_file), 'w') as f:
            json.dump(reminders, f, indent=4)
            #automatically rename the file
        os.replace(os.path.join(reminder_path, temp_file), 
                  os.path.join(reminder_path, 'reminders.json'))
    except Exception as e:
        #change this line to use notify
        print(f"Error saving reminders: {e}")
def cleanup_handler():
    """cleanup funcction to be called on exit"""
    if 'reminders' in globals() and modified:
        save_reminders(reminders)
    #change this line
    print("\nReminder checker shutting down...")

def signal_handler(signum, frame):
    """Handle various termination signals"""
    #change this line
    print(f'\n Received signal{signum}')
    sys.exit(0)

def check_current_reminders():
    while True:
        try:
            # Get the current time once at the start
            now = datetime.now()
            date_today = now.strftime('%Y-%m-%d')
            day_today = now.strftime('%A')
            time_now = now.strftime('%H:%M')

            # Read reminders
            with open(os.path.join(reminder_path, 'reminders.json'), 'r') as f:
                reminders = json.load(f)

            for reminder in reminders:
                if (not reminder.get('completed', False) and
                    reminder.get('day') == day_today and
                    reminder.get('time', '').replace(' hrs', '') == time_now):

                    notification.notify(
                        title=f"Reminder for {reminder['time']}",
                        message=reminder['task'],
                        timeout=10  # 10 seconds instead of 10 hours
                    )

                    # Play sound 3 times
                    for _ in range(3):
                        if platform.system() == 'Linux':
                            os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga')
                        elif platform.system() == 'Windows':
                            try:
                                import winsound
                                winsound.MessageBeep()
                            except Exception:
                                pass

                    # Mark as completed and save
                    reminder['completed'] = True
                    try:
                        save_reminders(reminders)
                    except Exception as e:
                        print(f"Error saving reminders: {e}")

            sleep(20)  # Wait before checking again

        except (FileNotFoundError, json.JSONDecodeError, EOFError) as e:
            #print(f"Warning: {e}")  # Log the error instead of silent `continue`
            sleep(5)  # Prevent CPU overuse in case of repeated errors
    
def check_reminders():
    global reminders, modified # Make these global so cleanup handler can access them

    #regidter cleanup handlers
    atexit.register(cleanup_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        try:
            #sleep(15)
            
            with open(os.path.join(reminder_path, 'reminders.json'), 'r') as f:
                reminders = json.load(f)
            daily_reminder_tasks = []
            upcoming_tasks = []
            modified = False
            date_today = datetime.now().strftime('%Y-%m-%d')
            day_today = datetime.now().strftime('%A')
            time_now = datetime.now().strftime('%H:%M')
            alert = False
            up_alert = False
            for reminder in reminders:
                #today reminders
                missed_today_time = int(time_now[:2]) > int(reminder['time'][:2]) and day_today == reminder['day']
                missed_now = int(time_now[:2]) == int(reminder['time'].strip(' hrs')[:2]) and int(time_now[-2:]) > int(reminder['time'].strip(' hrs')[-2:])

                if reminder['completed'] == False and reminder['day'] == datetime.now().strftime('%A'):
                    if not missed_today_time and not missed_now:
                        daily_reminder_tasks.append(f'{reminder['task']} at {reminder['time']} hrs')
                        alert = True
                #upcoming reminders
                if reminder['completed'] == False and datetime.strptime(date_today, '%Y-%m-%d') < datetime.strptime(reminder['date'], '%Y-%m-%d'):
                    upcoming_tasks.append(f'{reminder['task']} at {reminder['time']}hrs on {reminder['day']} {reminder['date']}')
                    up_alert = True
            daily_reminder_tasks = '\n'.join(str(x) for x in daily_reminder_tasks)
            upcoming_tasks = '\n'.join(str(x) for x in upcoming_tasks)

            # Notify about today's tasks if any exist
            if alert :
                notification.notify(
                    title = "Today's Reminders",
                    message = daily_reminder_tasks,
                    timeout = 300
                )
                if platform.system() == 'Linux':
                    try:
                        os.system('paplay /usr/share/sounds/freedesktop/stereo/service-logout.oga ')
                    except Exception as e:
                        pass
                elif platform.system() == 'Windows':
                    try:
                        # Windows fallback using winsound (built-in)
                        import winsound
                        winsound.MessageBeep()
                    except Exception as e:
                        pass   
            if up_alert:
            # Notify about upcoming tasks if any exist
                notification.notify(
                    title = "Upcoming Reminders",
                    message = upcoming_tasks,
                    timeout = 300
                )
                if platform.system() == 'Linux':
                    try:
                        os.system('paplay /usr/share/sounds/freedesktop/stereo/service-logout.oga ')
                    except Exception as e:
                        pass
                elif platform.system() == 'Windows':
                    try:
                        # Windows fallback using winsound (built-in)
                        import winsound
                        winsound.MessageBeep()
                    except Exception as e:
                        pass    

            # First check for missed reminders
            missed_today = False
            missed_otherday = False
            missed_reminders = []
            other_day_missed = []
            
            for reminder in reminders:
                if reminder['completed'] == False:
                    if int(time_now[:2]) > int(reminder['time'][:2]) and day_today == reminder['day']:
                        missed_reminders.append(f'{reminder["task"]} at {reminder["time"]}')
                        missed_today = True
                    elif int(time_now[:2]) == int(reminder['time'].strip(' hrs')[:2]) and int(time_now[-2:]) > int(reminder['time'].strip(' hrs')[-2:]):
                        missed_reminders.append(f'{reminder["task"]} at {reminder["time"]}')
                        missed_today = True
                    if day_today != reminder['day'] and datetime.strptime(date_today, '%Y-%m-%d') > datetime.strptime(reminder['date'], '%Y-%m-%d'):
                        other_day_missed.append(f'{reminder["task"]} at {reminder["time"]} on {reminder["day"]} {reminder["date"]}')
                        missed_otherday = True
            
            other_day_missed = '\n'.join(str(x) for x in other_day_missed)
            missed_reminders = '\n'.join(str(x) for x in missed_reminders)

            # Then notify and mark as completed
            if missed_today:
                notification.notify(
                        title = f"looks like you misssed something Today",
                        message = missed_reminders,
                        timeout = 400
                    )
                # Mark today's missed reminders as completed
                for reminder in reminders:
                    if reminder['completed'] == False and day_today == reminder['day']:
                        if (int(time_now[:2]) > int(reminder['time'][:2]) or 
                            (int(time_now[:2]) == int(reminder['time'].strip(' hrs')[:2]) and 
                             int(time_now[-2:]) > int(reminder['time'].strip(' hrs')[-2:]))):
                            reminder['completed'] = True
                            modified = True
                if modified:
                    save_reminders(reminders)
                
            if missed_otherday:
                notification.notify(
                        title = "Previously Missed Reminders",
                        message = other_day_missed,
                        timeout = 400
                    )
                # Mark previous days' missed reminders as completed
                for reminder in reminders:
                    if (reminder['completed'] == False and 
                        day_today != reminder['day'] and 
                        datetime.strptime(date_today, '%Y-%m-%d') > datetime.strptime(reminder['date'], '%Y-%m-%d')):
                        reminder['completed'] = True
                        modified = True
                if modified:
                    save_reminders(reminders)
            if missed_otherday == True or missed_today == True:

                if platform.system() == 'Linux':
                    try:
                        os.system('paplay /usr/share/sounds/freedesktop/stereo/service-logout.oga ')
                    except Exception as e:
                        pass
                elif platform.system() == 'Windows':
                    try:
                        # Windows fallback using winsound (built-in)
                        import winsound
                        winsound.MessageBeep()
                    except Exception as e:
                        pass
            check_current_reminders()

        except (FileNotFoundError, JSONDecodeError, EOFError):
            notification.notify(
                title = 'Reminders',
                message = 'No reminders found for Today',
                timeout = 300
            )
            if platform.system() == 'Linux':
                try:
                    os.system('paplay /usr/share/sounds/freedesktop/stereo/service-logout.oga')
                except Exception as e:
                    pass
            elif platform.system() == 'Windows':
                try:
                    # Windows fallback using winsound (built-in)
                    import winsound
                    winsound.MessageBeep()
                except Exception as e:
                    pass
            check_current_reminders()
            sleep(30)
    except Exception as e:
        print(f"Unexpected error: {e}")
        if 'reminders' in locals() and modified:
            save_reminders(reminders)
        raise
if __name__ == '__main__' :
    check_reminders()