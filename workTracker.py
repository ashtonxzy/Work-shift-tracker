import csv
from datetime import datetime as dt
import re
import os
from pynput import keyboard
from pynput.keyboard import Key

pay_rate = 13

def sumOfList(lst): #GET THE SUM OF A LIST
    total = 0
    for i in lst:
        total = total + int(i)
    return total

def add_shift(): #ADDS SHIFT TO CSV [DATE, HOURS WORKED, PAY FOR THE DAY]
    data = []
    print('\n')
    print('How many hours did you work?')
    while True:
        ans = input('>>')
        if ans.isnumeric(): #CHECKS INPUT VALIDITY
            date = dt.today().strftime('%Y-%m-%d')
            data.append(date)
            data.append(ans)
            pay = int(ans) * pay_rate
            data.append(pay)
            with open('shifts.csv', 'a', newline='') as read_obj:
                csv_writer = csv.writer(read_obj)
                csv_writer.writerow(data)
                break
        else:
            continue
    print('Shift added!')
    ans = input('Press any key to continue...')

def totalHoursWorked(): #CALCULATES HOW MANY HOURS WORKED OVER ALL
    with open('shifts.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        csv_list = list(csv_reader)
        csv_list.pop(0) #removes headers
        hours = []
        for row in csv_list:
            hours.append(row[1])
    return str(sumOfList(hours))

def total_pay(): #CALCULATES TOTAL PAY OF THE WHOLE JOB
    with open('shifts.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        csv_list = list(csv_reader)
        csv_list.pop(0)
        pay = []
        for row in csv_list:
            pay.append(row[2])
    print('Your total pay for this job is: £' + str(sumOfList(pay)))
    ans = input('Press any key to continue...')

def pay_for_the_month(): #CALCULATES PAY FOR THE INVOICING MONTH 26TH-26TH
    current_month = dt.today().strftime('%m')
    temp = int(current_month) - 1
    prev_month = '0' + str(temp) #GETS PREVIOUS MONTH IN FORMAT
    date_lower = dt.today().strftime('%Y-' + prev_month +'-26')
    date_upper = dt.today().strftime('%Y-%m-26')
    total = []
    with open('shifts.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        csv_list = list(csv_reader)
        check = False
        flag = False
        tf_list = []
        total = []
        for row in csv_list:
            if row[0] != date_lower and check == False: #IF DATE IS BELOW THE 26TH OF PREVIOUS MONTH DO NOT ADD TO NEW LIST
                continue
            elif row[0] == date_lower and check == False: #IF DATE IS 26TH THEN ADD
                tf_list.append(row)
                check = True
            elif row[0] == date_upper: #IF DATE IS 26TH OF NEXT MONTH THEN CHECK FLAG TO STOP APPENDING
                tf_list.append(row)
                flag = True
            elif not flag:
                tf_list.append(row)
    for row in tf_list:
        total.append(row[2]) #ADD JUST PAY TO A NEW LIST
    print('This months pay totals at: £' + str(sumOfList(total)))
    ans = input('Press any key to continue...')

def search_shift(): #ALLOWS SEARCHING THROUGH EVERY SHIFT DONE BY DATE
    print('\n')
    while True:
        print('Please enter the date to search for in format [yyyy-mm-dd]')
        ans = input('>>')
        pattern = r'\d{4}-\d{2}-\d{2}$'
        if re.match(pattern, ans): #CHECKS THAT DATE IS IN FORMAT
            try:
                with open('shifts.csv', 'r') as read_obj:
                    csv_r = csv.reader(read_obj)
                    csl_l = list(csv_r)
                    for row in csl_l:
                        if row[0] == ans:
                            print('Shift date: ' + row[0])
                            print('Hours worked: ' + row[1])
                            print('Total pay: ' + row[2])
                            break
            except IOError: #RETURN ERROR IF FILE IS UNABLE TO BE OPENED
                print('Error opening file')
            except:
                print('Unkown error occured')
            break
        else:
            continue
    print('')
    ans = input('Press any key to continue...')

def on_press(key): # CHECKS IF KEY HAS BEEN PRESSED THORUGH THE LISTENER
    global globCount
    if key == Key.up:
        os.system('clear')
        print('Key (esc) to exit.')
        print('\n')
        if globCount < len(globList) -1: #STOPS FROM CHECKING BELOW SHIFT DATE RANGE
            globCount = globCount + 1
            view_shifts_list_up()
        else:
            print('End of shifts.')
    elif key == Key.down:
        os.system('clear')
        print('Key (esc) to exit.')
        print('\n')
        if globCount != 0: #STOPS FROM CHECKING OUT OF DATE RANGE
            globCount = globCount - 1
            view_shifts_list_down()
        else:
            print('End of shifts.')
    elif key == Key.esc:
        listener.stop()
        main()

listener = keyboard.Listener(on_press=on_press) #LISTENS FOR KEYBOARD INPUT TO ALLOW FOR UP AND DOWN KEYS TO BE USED FOR SEARCHING

def view_shifts(): #ALLOWS USER TO SEARCH THROUGH ALL SHIFTS USING UP AND DOWN KEYS
    global globCount
    os.system('clear')
    print('Use [up] key and [down] key')
    listener.start()
    listener.join()

def view_shifts_list_up(): #GOES UP IN DATES FOR SHIFTS
    global globCount
    global globList
    print('Date: ' + str(globList[globCount][0]))
    print('Hours worked: ' + str(globList[globCount][1]))
    print('Pay: ' + str(globList[globCount][2]))

def view_shifts_list_down(): #GOES DOWN IN DATES FOR SHIFTS
    global globCount
    global globList
    print('Date: ' + str(globList[globCount][0]))
    print('Hours worked: ' + str(globList[globCount][1]))
    print('Pay: ' + str(globList[globCount][2]))


def invoice(): #GETS ALL USEFUL DATA FOR CREATING AN INVOICE
    current_month = dt.today().strftime('%m')
    temp = int(current_month) - 1
    prev_month = '0' + str(temp)
    date_lower = dt.today().strftime('%Y-' + prev_month + '-26')
    date_upper = dt.today().strftime('%Y-%m-26')
    with open('shifts.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        csv_list = list(csv_reader)
        check = False
        flag = False
        tf_list = []
        hours = []
        total = []
        temp_shifts = {}
        double_shift_hours = []
        double_shift_hours_temp = []
        for row in csv_list: #MAKES SURE DATA IS WITHIN THE 26TH-26TH RANGE
            if row[0] != date_lower and check == False:
                continue
            elif row[0] == date_lower and check == False:
                tf_list.append(row)
                check = True
            elif row[0] == date_upper:
                tf_list.append(row)
                flag = True
            elif not flag:
                tf_list.append(row)

    for row in tf_list:
        hours.append(row[1])
    print('Total hours worked this invoice month: ' + str(sumOfList(hours)))
    for row in tf_list:
        total.append(row[2])
    print('Total pay this month: £' + str(sumOfList(total)))

    temp_count = 0
    for row in tf_list: #ADDS ANY DOUBLE SHIFTS TO A SEPERATE LIST TO ALLOW USER TO ADD THESE TO INVOICE TO MAKE EASIER FOR PAYMENTS
        date = row[0]
        if date not in temp_shifts:
            temp_shifts[date] =1
        else:
            temp_shifts[date] = temp_shifts[date] + 1
            double_shift_hours_temp.append(temp_count)
        temp_count = temp_count + 1

    for item in double_shift_hours_temp: # CALCULATES HOW MANY HOURS IN TOTAL WERE WORKED THAT DAY
        hours_sum = int(hours[item - 1]) + int(hours[item])
        double_shift_hours.append(hours_sum)

    shift_count = 0
    double_shifts = {}
    for key, value in temp_shifts.items(): #DICTIONARY TO COUNT IF TWO SHIFTS HAVE BEEN WORKED ON THE SAME DAY
        if 1 != value:
            double_shifts.update({key: value})
            shift_count = shift_count + 1
    shift_count = 0
    print('Double shifts worked: ')
    for key, value in double_shifts.items():
        print(key + ' - ' +str(double_shift_hours[shift_count]) + ' Hours') #PRINTS THE DATE THE DOUBLE SHIFT WAS WORKED ALONG WITH OHW MANY HOURS TOTAL WERE WORKED THAT DAY
        shift_count = shift_count + 1
    input('')

def main():
    os.system('clear')
    print('\n')
    print('Total hours worked: ' + str(hours_worked) + '                       Date: ' + dt.today().strftime('%Y-%m-%d'))
    print('\n')
    print('1.) Add shift')
    print('2.) Search shift by date')
    print('3.) View all shifts')
    print('4.) Pay for the month')
    print('5.) Invoice')
    print('6.) Total pay')
    print('99.) Exit')
    ans = input('>>')
    if ans == '1':
        print('Are you sure? (y) for yes')
        ans = input('>>')
        if ans != 'y':
            print('Cancelling...')
        else:
            add_shift()
    elif ans == '2':
        search_shift()
    elif ans == '3':
        global globCount
        global globList
        try:
            with open('shifts.csv', 'r') as read_obj:
                csv_read = csv.reader(read_obj)
                globList = list(csv_read) #USING GLOBAL VARIABLES TO ACCESS IN LISTENER
                globList.pop(0)
            view_shifts()
        except IOError:
            print('An error occured.')
    elif ans == '4':
        pay_for_the_month()
    elif ans == '5':
        invoice()
    elif ans == '6':
        total_pay()
    elif ans == '99':
        os.system('clear')
        exit()

while True:
    globCount = 0
    globList = []
    hours_worked = totalHoursWorked()
    main()
