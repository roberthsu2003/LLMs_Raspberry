FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY tools.py .

EXPOSE 8000

# 啟動 MCPO，並執行自訂 COVID-19 tools
CMD ["mcpo", "--port", "8000", "--", "python", "tools.py"]
