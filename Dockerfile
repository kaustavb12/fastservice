FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-2020-12-19

RUN adduser --disabled-password worker

RUN chown worker:worker /app

COPY ./app/requirements.txt .

RUN pip install -r requirements.txt && rm main.py

RUN mkdir /run/secrets

USER worker

RUN mkdir /app/log/

CMD ["/start-reload.sh"]

COPY ./app /app