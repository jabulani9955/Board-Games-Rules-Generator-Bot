FROM python:3.8

COPY /req.txt /app/req.txt

WORKDIR /app

ENV TELEGRAM_TOKEN=""

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN python3.8 -m pip install -U pip
RUN python3.8 -m pip install -r /app/req.txt

COPY . /app

RUN python3.8 -m pip install /app/torch-1.10.0-cp38-cp38-manylinux1_x86_64.whl

ENTRYPOINT [ "python3.8", "bot.py" ]
