FROM python:3.8

WORKDIR /tg_bot

ENV TELEGRAM_TOKEN="2119124064:AAE3NlfKfaOTgxXYicCBG2CJ4_0C0I69Bc4"

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# RUN pip install -r pip aiogram pytz && apt-get update && apt-get install sqlite3
RUN pip install -U pip -r req.txt
COPY . .

ENTRYPOINT [ "python", "bot.py" ]
