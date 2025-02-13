# importing modules
from time import sleep
from datetime import date,datetime
from os import mkdir, chdir, path
# function that creates the AI working dir
dir = 'my_AI'

def folder():
    chdir('/home')
    #  path.exist checks for dir with no error
    if path.exists(dir):
        pass
    else:
        # we try creating dir

        try:
            mkdir(dir)       
            print('initiating my_AI system environment.........')
            sleep(3)

    
        # catch any other error thrown while creating dir
        except FileNotFoundError:
            print('system ran into an unknown error')
            
        finally:
        #the code finally moves into the working dir        
            chdir(dir)
    # chdir(dir)

folder()
# now lets work in the  AI's dir
# a function to read the last date recorded
# and also record the new date
# we will add time later
chdir(f'/home/{dir}')
def recall_last_meeting():
    today = date.today()
    # creates a log file , if no log file was present a new one will be created
    with open('log.txt','a') as file:
        pass
    # reads the log file
    with open('log.txt','r') as file:
        for lines in file:
                lines = file.readlines()
            # print(lines[-1].strip())
            # obtains the last line in the log file
                
                
                pass
           # a function that converts str date of format yy-mm-dd
      # to a datetime type that can be subtracted from another date
        def last_date():
            
           try:
               last_date1 = lines[-1].strip()
               year = last_date1[0]+last_date1[1]+last_date1[2]+last_date1[3]
           except Exception:
            last_date1 = str(today)
            year = last_date1[0]+last_date1[1]+last_date1[2]+last_date1[3]
           finally:
            if last_date1[5] == '0':
                month = last_date1[6]
            else:
                month = last_date1[5]+last_date1[6]
            day = last_date1[8]+last_date1[9]
            recall_date = date(int(year),int(month),int(day))
            
            return recall_date
        recall_date = last_date()
        days_since = (today - recall_date).days
            
        def time_passed():
    # know current time
            now = str(datetime.now().time())
            
    # i'll need to access the last time from a file
    # create an empty time file
            with open ('time.txt', 'a')as time_file:
                pass
    # read the time file
            with open ('time.txt','r')as time_file:
                for lines in time_file:
                    lines = time_file.readlines()
                try:
                    last_time = lines[-1].strip()
                
                except Exception:
                    last_time = str(now)

                finally:

                    pass
                def calc():
                    current_hour = int(now[0]+now[1])
                    current_minute = int(now[3]+now[4])
                    current_second = int(now[6]+now[7])

        # obtain the hour and minutes
                    last_hour = last_time[0]+last_time[1]
                    last_minute = last_time[3]+last_time[4]
                    last_second = int(last_time[6]+last_time[7])
                    last_hour = int(last_hour)
                    last_minute = int(last_minute)
        # now we calculate the time passed
                    if current_hour < last_hour:
                        current_hour = current_hour+12
                        pass
                    else:
                        pass
                    hour_passed = current_hour - last_hour
                    if current_minute < last_minute:
                        current_minute = current_minute+60
                        pass
                    else:
                        pass
                    minutes_passed = current_minute - last_minute
                    if current_second < last_second:
                        current_second = current_second+60
                        pass
                    else:
                        pass
                    seconds_passed = current_second - last_second
                    print(f'hello user it has been {days_since} day(s) '
                           f'{hour_passed} hour(s), '
                        f'{minutes_passed} minute(s) and {seconds_passed} second(s) since we met 😊')
                calc()
    # record new time
                with open('time.txt','a')as time_file:
                    time_file.write(f'{now}\n')    
        time_passed()
    with open('log.txt','a') as file:
        #     # records new date
        file.write(f'{str(today)}\n')
recall_last_meeting()
# birthday reminder function
print('checking for any reminders..................')
sleep(3)
def birthday():
    today = date.today()
    # open a database file with personal info
    with open('peter_db.txt', 'a')as file:
        pass
    # read the lines
    with open('peter_db.txt', 'r')as file:
        for lines in file:
            lines=file.readlines()
            lines = lines[0].strip()
        # find a line with the birthday info
            try:
                key_word = 'birthday'
                if key_word in lines:
            # print(lines.replace('birthday ',''))
            # extract the birthday date in strings
                    bd_year = lines[9]+lines[10]+lines[11]+lines[12]
                    bd_month = lines[14]+lines[15]
                    bd_day = lines[17]+lines[18]
                else:
                    print('no birthday reminders today, i hope your database is up to date')
            # birthday = date(int(bd_year),int(bd_month),int(bd_day))
            # days_to_bd = (today - birthday).days
            # know if the birthday is soon
            except Exception:
                print('failed to access any data,database might be empty')
            else:
                pass  
            if int(bd_month) == datetime.now().month and int(bd_day) == datetime.now().day:
                print('today is your birthday!!🎂\nenjoy your day')
                age = datetime.now().year - int(bd_year)
                print(f'HAPPY {age} 🥳')
            elif int(bd_month) == datetime.now().month and int(bd_day) > datetime.now().day:
                days_to_bd = int(bd_day) - datetime.now().day
                print(f'just a reminder, your birthday is in {days_to_bd} day(s)')
            else:
                pass
        
    sleep(2)
    print('no new reminders')
                
birthday()          

    