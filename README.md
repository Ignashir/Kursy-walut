This app provides functionalities to pull data from [nbp.api](https://nbp.pl/statystyka-i-sprawozdawczosc/kursy/)
Project written using hexagonal architecture

## Installation

In order to use the app, go into projects directory and write

```bash
pipenv shell
```
Then
```bash
docker-compose up -d --build
```
For additional information about apps working process such as listeners type
```bash
docker-compose logs -f
```

## Usage
To pull data about single currency use:  
localhost:8000/currency/<code>?  
To pull data about many currencies use:  
localhost:8000/currency?  
To pull data about gold use:  
localhost:8000/gold?  

options (separated by &):  
limit=0  
req_date=year-month-day  
date_begin=year-month-day  
date_end=year-month-day  
graph=True  
pdf=True

Use limit / req_date / (date_begin and date_end) separately.  
The same applies to graph and pdf.

To predict data about gold from a certain date use:  
localhost:8000/gold/predict/year-month-day

## License

[MIT](https://choosealicense.com/licenses/mit/)