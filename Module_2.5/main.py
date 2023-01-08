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

    async def request_rates_for_date(self):
        if self.dates_str_list:
            async with aiohttp.ClientSession() as session:
                for date_str in self.dates_str_list:
                    url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='+date_str
                    try:
                        async with session.get(url) as response:
                            if response.status == 200:
                                result = await response.text()
                                is_rate_collected = True
                            else:
                                result = f"Error status: {response.status} for {url}"
                                is_rate_collected = False
                    except aiohttp.ClientConnectorError as err:
                        result = f'Connection error: {url}, {str(err)}'
                        is_rate_collected = False
                    self.responses.append(
                        (result, is_rate_collected, date_str))
        else:
            result = 'Requested date is not provided'
            is_rate_collected = False
            self.responses.append((result, is_rate_collected, date_str))

    def form_output(self, currencies: list):
        self.formatted_output = f'Currency rates for {currencies if currencies else "all currencies"}:\n'
        for response in self.responses:
            if response[1]:
                rates_dict = json.loads(response[0])
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


if __name__ == '__main__':
    user_interface = Output_Console()
    rates_request = Currency_Rates_Request()
    try:
        number_of_days = int(sys.argv[1])
    except IndexError:
        number_of_days = 1
    else:
        if number_of_days > 10:
            number_of_days = 10
            user_interface.output_message("Maximum 10 days can be requested.")
    try:
        requested_currencies = sys.argv[2]
    except IndexError:
        requested_currencies = None
    rates_request.form_dates_list(number_of_days)
    asyncio.run(rates_request.request_rates_for_date())
    rates_request.send_output(requested_currencies, user_interface)
