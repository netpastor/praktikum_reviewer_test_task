
import datetime as dt

# Codereview comments
#   1. Отсутствует докстринг с описанием класса
class Record:

    # Codereview comments
    #   1. Добавить аннотирование типов для переменных
    def __init__(self, amount, comment, date=''):
        self.amount = amount

        # Codereview comments
        # 1. При неправильном значении переменной date при вызове метода strptime
        # будет вызвано исключение ValueError. Продумать или проверку этого значения
        # с выводом текста ошибки, или инициализацию переменной класса значением
        # по умолчанию - текущей датой.
        # 2. Код не отформатирован по PEP8
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())

        self.comment = comment


# Codereview comments
#   1. Отсутствует докстринг с описанием класса
class Calculator:

    # Codereview comments
    #   1. Добавить аннотирование типов для переменных
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    # Codereview comments
    #   1. Отсутствует докстринг с описанием метода
    #   2. Добавить аннотирование типов для переменных
    def add_record(self, record):
        self.records.append(record)

    # Codereview comments
    #   1. Отсутствует докстринг с описанием метода
    def get_today_stats(self):
        today_stats = 0

        # Codereview comments
        #   1. Имя переменной в цикле не должно начинаться с заглавной буквы
        #      - переименовать в record
        #   2. Для вынесения условия из цикла лучше использовать функцию filter:
        #      today = dt.datetime.now().date()
        #      for record in filter(lambda r: r.date == today, self.records):
        #          today_stats += record.amount
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    # Codereview comments
    #   1. Отсутствует докстринг с описанием метода
    #   2. Для вынесения условия из цикла лучше использовать функцию filter:
    #      today = dt.datetime.now().date()
    #      for record in filter(
    #          lambda r: (today - r.date).days in range(0, 7),
    #          self.records
    #          ):
    #          week_stats += record.amount
    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats

# Codereview comments
#   1. Отсутствует докстринг с описанием класса
class CaloriesCalculator(Calculator):
    # Codereview comments
    #   1. Комментарий вынести в докстринг с описанием метода
    def get_calories_remained(self):  # Получает остаток калорий на сегодня

        # Codereview comments
        #   1. Переименовать переменную x  для читаемости -
        #   к примеру в calory_balance
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь ' \
                   f'ещё, но с общей калорийностью не более {x} кКал'

        # Codereview comments
        #   1. В этом else нет необходимости, можно просто оставить один
        #   return
        else:
            return('Хватит есть!')


# Codereview comments
#   1. Отсутствует докстринг с описанием класса
class CashCalculator(Calculator):

    # Codereview comments
    #   1. Для операций с денежными величинами float тип не самый лучший вариант,
    #   лучше использовать тип Decimal из модуля decimal
    #   https://docs.python.org/3/library/decimal.html
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Codereview comments
    #   1. Отсутствует докстринг с описанием метода
    #   2. Добавить аннотирование типов для переменных

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):

        # Codereview comments
        #   1. Необходимо проверить что переменная currency содержит
        #   необходимое значение. Начиная с версии 3.10 появилась конструкция
        #   языка match case - https://peps.python.org/pep-0636/.
        #   Для универсальности можно использовать решение на словарях
        #   Пример:
        #   cash_remained = self.limit - self.get_today_stats()
        #   currency_dict = {
        #       'usd': {
        #           'value': cash_remained / USD_RATE,
        #           'currency_type': 'USD'
        #       },
        #       'eur': {
        #           'value': cash_remained / EURO_RATE,
        #           'currency_type': 'Euro'
        #       },
        #       'rub': {
        #           'value': 1.00,
        #           'currency_type': 'руб'
        #       },
        #   }
        #   _currency = currency_dict.get(currency)
        #   if not _currency:
        #       raise ValueError('Неподдерживаемый тип валюты.')
        #
        #   cash_remained, currency_type = _currency.values()
        #
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'

        # Codereview comments
        #   1. В этом else нет необходимости, можно просто оставить один
        #   return
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Codereview comments
    #   1. Отсутствует докстринг с описанием метода
    #   2. Объявлять метод просто с вызовом метода из класса родителя нет смысла,
    #   он и так будет вызван в процессе MRO, лучше убрать этот метод.
    def get_week_stats(self):
        super().get_week_stats()
