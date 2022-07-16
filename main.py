import xml.etree.ElementTree as ET
import requests
import re


UsedData = ''
DataFolder = ''
namespaces = {'ns': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
amount = 0
currency = ''


class Calculator:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency
        global DataFolder

    def exchange(self):
        # self.amount = input('How much money would you like to exchange: ')
        # self.currency = input('To which currency would you like to exchange to: ')
        tree = ET.parse(DataFolder)
        root = tree.getroot()
        match = root.find('.//ns:Cube[@currency="{}"]'.format(self.currency.upper()), namespaces=namespaces)
        ex_money = round(float(self.amount) * float(match.attrib['rate']), 2)
        print('The exchange of {} EUR to {} would be {}'.format(self.amount, self.currency, ex_money))


def input_reader():
    global currency
    global amount
    tree = ET.parse(DataFolder)
    root = tree.getroot()
    while True:
        amount = input('How much money would you like to exchange: ')
        amount = amount.replace(',', '.')
        try:
            float(amount)
            break
        except ValueError:
            print('\nInput error, please note that input should not include any characters that are not numbers')
            print('It should also only include one decimal separator\n')

    while True:
        currency = input('To which currency would you like to exchange to: ')
        match = root.find('.//ns:Cube[@currency="{}"]'.format(currency.upper()), namespaces=namespaces)
        if match is not None:
            break
        else:
            print('\nInput error, please insert the correct currency code (ex. US dollar = USD)\n')


def rates_downloader():
    try:
        global DataFolder
        global UsedData
        UsedData = requests.get(URL)
        open('eurofxref-daily.xml', 'wb').write(UsedData.content)
        DataFolder = 'eurofxref-daily.xml'
    except requests.exceptions.RequestException as e:
        print('Could not download current data - using historic data \nerror: ', e, '\n\n')
        DataFolder = 'eurofxref-daily-old.xml'


def data_saver():
    global DataFolder
    global UsedData
    if DataFolder == 'eurofxref-daily.xml':
        open('eurofxref-daily-old.xml', 'wb').write(UsedData.content)


rates_downloader()
input_reader()
action = Calculator(amount, currency)
action.exchange()
data_saver()
