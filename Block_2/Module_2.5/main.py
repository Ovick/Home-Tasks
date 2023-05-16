import aiohttp
import asyncio
import json
import sys
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


class Output_Device(ABC):
    def __init__(self) -> None:
        self.message = None

    @abstractmethod
    def output_message(self, message: str = None) -> None:
        pass


class Output_Console(Output_Device):
    def output_message(self, message: str = None):
        self.message = message
        if self.message:
            print(message)
            self.message = None


class Currency_Rates_Request():

    def __init__(self) -> None:
        self.dates_str_list = []
        self.responses = []
        self.formatted_output = ''

    def form_dates_list(self, number_of_days: int):
        result = []
        today = datetime.now()
        for i in range(number_of_days):
            date = (today-timedelta(days=i)).date()
            date_str = datetime.strftime(date, '%d.%m.%Y')
            result.append(date_str)
        self.dates_str_list = result

    async def request(self):
        async with aiohttp.ClientSession() as session:
            for date_str in self.dates_str_list:
                url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='+date_str
                try:
                    async with session.get(url) as response:
                        if response.status == 200:
                            result = await response.json()
                            is_rate_collected = True
                        else:
                            result = f"Error status: {response.status} for {url}"
                            is_rate_collected = False
                except aiohttp.ClientConnectorError as err:
                    result = f'Connection error: {url}, {str(err)}'
                    is_rate_collected = False
                self.responses.append(
                    (result, is_rate_collected, date_str))

    def form_output(self, currencies: list):
        self.formatted_output = f'Currency rates for {currencies if currencies else "all currencies"}:\n'
        for response in self.responses:
            if response[1]:
                rates_dict = response[0]
                self.formatted_output += f'Base currency {rates_dict["baseCurrencyLit"]}, {response[2]}\n'
                for rate in rates_dict['exchangeRate']:
                    rate_line = f"{rate['currency']}: sale {rate['saleRateNB']}, purchase {rate['purchaseRateNB']}\n"
                    if currencies:
                        if rate['currency'] in currencies:
                            self.formatted_output += rate_line
                    else:
                        self.formatted_output += rate_line
            else:  # collection error
                self.formatted_output += f'Collection error for date {response[2]}: {response[0]}\n'

    def send_output(self, currencies: list, device: Output_Device):
        self.form_output(currencies)
        device.output_message(self.formatted_output)


class Session():
    def __init__(self, args: list, device: Output_Device) -> None:
        self.device = device
        self.currencies = []
        self.number_of_days = 1
        try:
            self.number_of_days = int(args[1])
        except IndexError:
            self.device.output_message(
                "Rates for 1 day will be requested.")
        except ValueError:
            self.device.output_message(
                "Request parameters should be <number of days> [currency1, currency2, ...].")
        else:
            if self.number_of_days > 10:
                self.number_of_days = 10
                self.device.output_message(
                    "Maximum 10 days can be requested.")
        try:
            self.currencies = args[2]
        except IndexError:
            self.currencies = None


if __name__ == '__main__':
    user_interface = Output_Console()
    user_session = Session(sys.argv, user_interface)
    rates_request = Currency_Rates_Request()
    rates_request.form_dates_list(user_session.number_of_days)
    asyncio.run(rates_request.request())
    rates_request.send_output(user_session.currencies, user_session.device)
