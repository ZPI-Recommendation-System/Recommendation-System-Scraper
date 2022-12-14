# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /scraper

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-um", "src.main"]