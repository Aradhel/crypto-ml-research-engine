FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m src.market_research.pipeline --demo
EXPOSE 5000
CMD ["python", "dashboard/app.py"]

