FROM python:3-bookworm

RUN pip install psycopg2

WORKDIR /myeco_api

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["fastapi", "run", "main.py"]