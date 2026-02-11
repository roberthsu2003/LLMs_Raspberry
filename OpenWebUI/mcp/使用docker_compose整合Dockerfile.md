# 使用docker_compose整合Dockerfile

這一步就是把「單一容器」升級成「可管理的服務架構」。

你現在已經有：

- ✅ Dockerfile（mcpo-server）
- ✅ 想要固定 network
- ✅ 未來可能還要加 open-webui

那就改用 docker-compose.yml 管理。

---

# **一、專案結構建議**

建立一個資料夾，例如：

```other
mcpo-project/
├── docker-compose.yml
└── mcpo/
    └── Dockerfile
```

---

# **二、Dockerfile（放在 mcpo/ 內）**

```other
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir mcpo mcp-server-time

EXPOSE 8000

CMD ["mcpo", "--port", "8000", "--", "mcp-server-time", "--local-timezone=Asia/Taipei"]
```

---

# **三、docker-compose.yml**

```other
version: "3.9"

services:
  mcpo:
    build: ./mcpo
    container_name: mcpo
    ports:
      - "8000:8000"
    networks:
      - webui-net

networks:
  webui-net:
    driver: bridge
```

---

# **四、啟動方式**

在專案根目錄執行：

```other
docker compose up -d
```

（新版 Docker 是 docker compose，不是 docker-compose）

---

# **五、執行流程（這段超適合教學）**

當你執行：

```other
docker compose up -d
```

Docker 會做：

---

## **Step 1：建立 network（如果不存在）**

```other
webui-net
```

👉 這就是你剛剛問的「如果有就不建立」

compose 會自動幫你處理。

---

## **Step 2：build image**

等同於：

```other
docker build -t mcpo-project-mcpo .
```

---

## **Step 3：建立 container**

等同於：

```other
docker run ...
```

---

# **六、如果未來加上 Open-WebUI**

你只要改成：

```other
version: "3.9"

services:
  mcpo:
    build: ./mcpo
    container_name: mcpo
    ports:
      - "8000:8000"
    networks:
      - webui-net

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    ports:
      - "3000:8080"
    networks:
      - webui-net

networks:
  webui-net:
    driver: bridge
```

然後在 Open-WebUI 內填：

```other
http://mcpo:8000
```

因為：

> 同一個 network → 可以用 service 名稱當 hostname

---

# **七、為什麼你應該教 compose（對你課程超重要）**

你現在在教 MCP 架構。

docker compose 其實是在教：

```other
Infrastructure as Code
```

而且學生會開始理解：

- service
- network
- container DNS
- multi-service architecture

這會讓 MCP 不再只是工具，而是架構思維。

---

# **八、建議你在課程中這樣拆章節**

1️⃣ 單容器 docker run

2️⃣ 自己寫 Dockerfile

3️⃣ 建立 network

4️⃣ docker compose 管理

5️⃣ 多服務整合

學生會從「會跑」→「會架構」

---

如果你願意，我可以幫你做一個：

🔥「MCP + Open-WebUI + Pipeline Server」完整 docker-compose 架構圖

那張圖會非常有教學震撼力。

