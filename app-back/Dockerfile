FROM python:3.8
WORKDIR /app-back
RUN pip install fastapi uvicorn mysql-connector-python sqlalchemy pydantic
COPY . .
EXPOSE 8000
CMD uvicorn backend-service:app --host 0.0.0.0 --port 8000