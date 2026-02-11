# 整合使用open-webui和cloudflare tunnel

你現在已經有：

- ✅ open-webui
- ✅ cloudflared
- ✅ 自訂 webui-net

我們只要把 mcpo 服務加進來，並且讓它：

- 使用同一個 network
- 透過 service 名稱互相解析
- 不需要再用 host.docker.internal

---

# **✅ 整合後完整 docker-compose.yml**

```other
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    restart: always
    networks:
      - webui-net
    ports:
      - "8080:8080"
    volumes:
      - open-webui:/app/backend/data
    environment:
      OLLAMA_BASE_URL: http://host.docker.internal:11434
      MCP_ENABLE: "true"
    extra_hosts:
      - "host.docker.internal:host-gateway"

  mcpo:
    build: ./mcpo
    container_name: mcpo
    restart: always
    networks:
      - webui-net
    ports:
      - "8000:8000"

  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared
    restart: unless-stopped
    networks:
      - webui-net
    command: tunnel run --token ${CLOUDFLARE_TOKEN}

volumes:
  open-webui:
    external: true

networks:
  webui-net:
    name: webui-net
    driver: bridge
```

---

# **📌 專案結構應該長這樣**

```other
project/
├── docker-compose.yml
└── mcpo/
    └── Dockerfile
```

---

# **🚀 啟動方式**

```other
docker compose up -d --build
```

---

# **🔥 重要觀念（超適合你教學）**

現在整個架構會變成：

```other
Cloudflare Tunnel
        ↓
   open-webui:8080
        ↓
   mcpo:8000
        ↓
   MCP server (time)
```

---

# **🧠 為什麼這樣比較專業？**

因為：

在同一個 network 內

```other
http://mcpo:8000
```

就可以互相存取。

不需要：

```other
host.docker.internal
```

---

# **🎯 Open-WebUI 內該怎麼填 MCP？**

進到：

```other
Settings → MCP
```

填：

```other
http://mcpo:8000
```

因為 service name = hostname

---

# **🔥 進階優化（建議）**

其實 mcpo 不一定要對外開 port。

如果只是給 open-webui 用，可以改成：

```other
mcpo:
    build: ./mcpo
    container_name: mcpo
    restart: always
    networks:
      - webui-net
    expose:
      - "8000"
```

expose 代表：

👉 只給 container 內部使用

👉 不對 host 開 port

這樣更乾淨。

---

# **🧠 你可以在課堂這樣講**

docker-compose 做的事情是：

- 建 network
- build image
- 建 container
- 建立內部 DNS
- 定義服務依賴

這其實已經是：

> 微服務架構雛形

---

# **🎓 如果你願意**

我可以幫你畫一張：

```other
Internet
   ↓
Cloudflare
   ↓
Open-WebUI
   ↓
mcpo
   ↓
MCP Server
```

這張圖放在「MCP 架構總覽」章節，學生會瞬間理解整個技術棧。

