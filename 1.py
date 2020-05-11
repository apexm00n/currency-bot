import discord
from pycbrf.toolbox import ExchangeRates
import datetime
from datetime import timedelta
from discord.ext import commands

client = discord.Client()

currency = ['EUR', 'USD', 'BYN', 'GBP', 'DKK', 'CAD', 'CNY', 'CHF', 'AUD', 'PLN']

bot = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!help'):
        print('[command]: help')
        await message.channel.send('Я создан для того, чтобы вы могли узнать курс'
                                   ' валют на любое время из предложенного списка')
        await message.channel.send("['EUR'-'Евро', 'USD'-'Доллар(доллар США), "
                                   "'BYN'-'Рубль(белорусский рубль)', 'GBP'-'Фунт(фунт стерлингов)', "
                                   "'DKK'-'Крона(датская крона)', 'CAD'-'Доллар(канадский доллар)', "
                                   "'CNY'-'Юань', 'CHF'-'Франк(швейцарский франк)', "
                                   "'AUD'-'Доллар(австралийский доллар)', 'PLN'-'Злотый']")
        await message.channel.send("Чтобы узнать текущий курс валют, "
                                   "достаточно ввести команду '!getprice {код валюты}'."
                                   "Чтобы узнать курс валют в определенный день, необходимо ввести команду "
                                   "'!getprice {код валюты} {дата}'. Чтобы узнать курс валют в течение нескольких дней "
                                   "нужно ввести команду '!getprice {код валюты} {начальная дата} {конечная дата}'")
        await message.channel.send('примеры:'
                                   '     !getprice usd'
                                   '     !get price usd 2020-01-02'
                                   '     !get price usd 2020-01-02 2020-01-12')
    if message.content.startswith('!getprice'):
        print('[command]: getprice')
        try:
            if len(message.content.split()) < 2 or len(message.content.split()) > 4:
                await message.channel.send('Неверно введены данные')
            elif message.content.split()[1].upper() in currency and len(message.content.split()) == 4:
                sp = get_range_price(message.content.split()[1].upper(),
                                     message.content.split()[2],
                                     message.content.split()[3])
                for i in sp:
                    await message.channel.send(i)
            elif message.content.split()[1].upper() in currency and len(message.content.split()) == 3:
                result = get_definite_price(message.content.split()[1].upper(), message.content.split()[2])
                await message.channel.send(f'{message.content.split()[1].upper()}: {result}')
            elif message.content.split()[1].upper() in currency and len(message.content.split()) == 2:
                result = get_current_price(message.content.split()[1].upper())
                difference = get_difference(message.content.split()[1].upper())
                await message.channel.send(f'{message.content.split()[1].upper()}: {result}({difference})')
            else:
                await message.channel.send('Неверно введены данные')
        except ValueError or KeyError or IndexError:
            await message.channel.send('Неверно введены данные')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Привет, {member.name}, чтобы ознакомиться с моими возможностями введите команду "help!"'
    )


def get_range_price(currency, date, dattee):
    sp = []
    start_date = datetime.date(int(date.split('-')[0]),
                               int(date.split('-')[1]), int(date.split('-')[2]))
    end_date = datetime.date(int(dattee.split('-')[0]),
                             int(dattee.split('-')[1]), int(dattee.split('-')[2]))
    for _ in range(0, (end_date - start_date).days + 1):
        rates = ExchangeRates(start_date)
        ratess = ExchangeRates(start_date - timedelta(days=1))
        pricee = ratess[f'{currency}'][4]
        price = rates[f'{currency}'][4]
        delta = price - pricee
        if delta >= 0:
            sp.append(f'{start_date}: {price}(+{delta})')
        else:
            sp.append(f'{start_date}: {price}({delta})')
        start_date += timedelta(days=1)
    return sp


def get_current_price(currency):
        rates = ExchangeRates(f'{datetime.datetime.now().year}-{datetime.datetime.now().month}-'
                              f'{datetime.datetime.now().day}')
        price = rates[f'{currency}'][4]
        return price


def get_definite_price(currency, date):
    rates = ExchangeRates(date)
    price = rates[f'{currency}'][4]
    return price


def get_difference(currency):
    rates = ExchangeRates(f'{datetime.datetime.now().year}-{datetime.datetime.now().month}-'
                          f'{datetime.datetime.now().day - 1}')
    difference = rates[f'{currency}'][4] - get_current_price(currency)
    if difference >= 0:
        return f'+{difference}'
    else:
        return str(difference)


client.run('NzA1NzI0NTgwOTA3NDUwNDA4.Xq1cYg.3SG49CHvnafNMXCUROIYOQA62SY')

bot.run('NzA1NzI0NTgwOTA3NDUwNDA4.Xq1cYg.3SG49CHvnafNMXCUROIYOQA62SY')
