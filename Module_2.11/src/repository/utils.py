from calendar import isleap
from datetime import datetime


def days_to_birthday(birthday: datetime) -> int:
    next_birthday = None
    Feb29_birthdate = False
    if birthday.month == 2 and birthday.day == 29 \
            and not isleap(datetime.now().year):
        Feb29_birthdate = True
        birthday_this_year = datetime.date(datetime.now().year, 2, 28)
    else:
        birthday_this_year = datetime.date(
            datetime.now().year,
            birthday.month,
            birthday.day
        )
    # if the birthday this year already occurred take the next year
    if birthday_this_year < datetime.date(datetime.now()):
        next_birthday = birthday_this_year.replace(
            year=birthday_this_year.year+1)
        if Feb29_birthdate and isleap(next_birthday.year):
            next_birthday = birthday_this_year.replace(
                day=birthday_this_year.day+1)
    else:
        next_birthday = birthday_this_year
    return (next_birthday - datetime.date(datetime.now())).days
