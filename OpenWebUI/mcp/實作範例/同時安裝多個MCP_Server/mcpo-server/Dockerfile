FROM python:3.11-slim

WORKDIR /app

COPY config.json /app/config.json

# 安裝 mcpo 與 mcp-server-time
RUN pip install --no-cache-dir mcpo mcp-server-time mcp_weather_server


EXPOSE 8000

CMD ["mcpo", "--port", "8000", "--config", "/app/config.json"]
