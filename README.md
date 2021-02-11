# API USD-RUB exchange converter

Этой простое HTTP API для двусторонней конвертации валют RUB-USD по внешнему актуальному курсу.
Курс забирается из "https://moskva.vbr.ru/banki/kurs-valut/prodaja-usd/" посредством парсинга.
Есть логировние в STDOUT.

## Конвертировать 100 USD в RUB
**Request: 
```json
PUT /usd-rub
Accept: application/json
Content-Type: application/json

{
    "initial_currency":"USD",
    "initial_amount": "100"
}
```
**Response **
```
{
    "initial_currency": "USD",
    "init_amount": 100,
    "exchange_rate": 73.4,
    "final_currency": "RUB",
    "final_amount": 7340.000000000001
}
```

## Попытка конвертировать не поддерживаемую валюту
**Request: 
```json
PUT /usd-rub
Accept: application/json
Content-Type: application/json

{
    "initial_currency":"EUR",
    "initial_amount": "100"
}
```
**Response **
```
{
    "error": "Incorrect initial currency. Allowed are USD, RUB"
}
```

## Попытка конвертации, указав исходную сумму не как целое число
**Request: 
```json
PUT /usd-rub
Accept: application/json
Content-Type: application/json

{
    "initial_currency":"RUB",
    "initial_amount": "hundred"
}
```
**Response **
```
{
    "error": "Please provide initial amount as integer"
}
```



