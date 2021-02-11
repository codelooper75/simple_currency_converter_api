FROM python:3.7
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
COPY . /usr/src/app/
CMD ["python", "http_api_currency_exchange.py"]
