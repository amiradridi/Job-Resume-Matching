FROM python:3.9.4-slim
WORKDIR /code
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./main.py /code/
ENV PYTHONUNBUFFERED 1
EXPOSE 8080:8000
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]