import xml.etree.ElementTree as ET
import requests

UsedData = ''
DataFile = ''
namespaces = {'ns': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
amount = 0
currency = ''


class Calculator:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency
        global DataFile

    def exchange(self):
        tree = ET.parse(DataFile)
        root = tree.getroot()
        match = root.find('.//ns:Cube[@currency="{}"]'.format(self.currency.upper()), namespaces=namespaces)
        exchanged_amount = round(float(self.amount) * float(match.attrib['rate']), 2)
        print('The exchange of {} EUR to {} would be {}'.format(self.amount, self.currency, exchanged_amount))


def input_reader():
    global currency
    global amount
    tree = ET.parse(DataFile)
    root = tree.getroot()

    while True:
        amount = input('\nHow much money would you like to exchange: ')
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
    global DataFile
    global UsedData
    UsedData = requests.get(URL)

    try:
        open('eurofxref-daily.xml', 'wb').write(UsedData.content)
        DataFile = 'eurofxref-daily.xml'
    except requests.exceptions.RequestException as e:
        print('Could not download current data - using historic data \nerror: ', e, '\n\n')
        DataFile = 'eurofxref-daily-old.xml'


def data_saver():
    global DataFile
    global UsedData

    if DataFile == 'eurofxref-daily.xml':
        open('eurofxref-daily-old.xml', 'wb').write(UsedData.content)


def main():
    rates_downloader()

    while True:
        input_reader()
        action = Calculator(amount, currency)
        action.exchange()
        data_saver()
        print("\n")


main()
