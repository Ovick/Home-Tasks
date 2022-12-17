FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /Assistant_Bot

RUN pip install pipenv

COPY ["Pipfile", "Pipfile.lock","requirements.txt", "/Assistant_Bot/"] 

RUN pipenv install --system --deploy 

COPY . /Assistant_Bot/

CMD ["python","Assistant_Bot.py"]