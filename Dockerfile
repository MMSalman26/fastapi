FROM python:3.11
COPY main.py /app/
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
WORKDIR /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]