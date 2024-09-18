import os
import discord
from dotenv import load_dotenv
import csv
from datetime import datetime as dt
from discord.ext import commands

pay_rate = 13

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='?', case_insensitive=True, intents=intents)

def sumOfList(lst): #GET THE SUM OF A LIST
    total = 0
    for i in lst:
        total = total + int(i)
    return total

@client.event
async def on_ready():
    for server in client.guilds:
        print(f'Connected successfully to: {server.name} ---- id: {server.id}')


@client.command()
async def add_shift(ctx):
    await ctx.send('How many hours did you work?')
    hours = await client.wait_for('message')
    data = []
    if hours.content.isnumeric():  # CHECKS INPUT VALIDITY
        date = dt.today().strftime('%Y-%m-%d')
        data.append(date)
        data.append(hours.content)
        pay = int(hours.content) * pay_rate
        data.append(pay)
        with open('shifts.csv', 'a', newline='') as read_obj:
            csv_writer = csv.writer(read_obj)
            csv_writer.writerow(data)
        await ctx.send('Shift added!')
    else:
        await ctx.send('You didnt enter a number!!!!')


@client.command()
async def invoice(ctx):
    hours_worked = ""
    total_pay = ""
    double_shifts_str = ""
    os.system('clear')
    current_month = dt.today().strftime('%m')
    temp = int(current_month) - 1
    prev_month = '0' + str(temp)
    date_lower = dt.today().strftime('%Y-' + prev_month + '-27')
    date_upper = dt.today().strftime('%Y-%m-27')
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
        for row in csv_list:  # MAKES SURE DATA IS WITHIN THE 27TH-26TH RANGE
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
    hours_worked = sumOfList(hours)

    for row in tf_list:
        total.append(row[2])
    total_pay = sumOfList(total)

    temp_count = 0
    for row in tf_list:  # ADDS ANY DOUBLE SHIFTS TO A SEPARATE LIST TO ALLOW USER TO ADD THESE TO INVOICE TO MAKE EASIER FOR PAYMENTS
        date = row[0]
        if date not in temp_shifts:
            temp_shifts[date] = 1
        else:
            temp_shifts[date] = temp_shifts[date] + 1
            double_shift_hours_temp.append(temp_count)
        temp_count = temp_count + 1

    for item in double_shift_hours_temp:  # CALCULATES HOW MANY HOURS IN TOTAL WERE WORKED THAT DAY
        hours_sum = int(hours[item - 1]) + int(hours[item])
        double_shift_hours.append(hours_sum)

    shift_count = 0
    double_shifts = {}
    for key, value in temp_shifts.items():  # DICTIONARY TO COUNT IF TWO SHIFTS HAVE BEEN WORKED ON THE SAME DAY
        if 1 != value:
            double_shifts.update({key: value})
            shift_count = shift_count + 1
    shift_count = 0

    for key in double_shifts.items():
        double_shifts_str = double_shifts_str + str(key) + '   Total hours worked: ' + str(double_shift_hours[shift_count]) + "\n"  # PRINTS THE DATE THE DOUBLE SHIFT WAS WORKED ALONG WITH OHW MANY HOURS TOTAL WERE WORKED THAT DAY
        shift_count = shift_count + 1

    await ctx.send('Hours worked this month: ' + str(hours_worked))
    await ctx.send('Total pay : £' + str(total_pay))
    await ctx.send('Double shifts worked: ' + '\n' + str(double_shifts_str))

client.run(TOKEN)
