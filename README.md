# 從Linux操作系統到人工智能生成式模型應用的實踐開發
**本地端LLMs在Raspberry上的應用**

## 硬體需求
- Raspberry PI 5
- 記憶體4GB,8GB,16GB 建議**8GB**(一般操作),16GB(LLM生成式應用)

## 作業系統需求
- PiOS **No Desktop**

## 待完成事項
- 安裝流程說明
- 教室區網連線
  - 使用教室無線網路AP(Wireless Access Point)連線
  - 使用dongle wifi連線
  - 使用手機熱點連線
- 使用ssh連線,使用filezilla連線(sftp)
- 使用vnc viewer連線
- 使用pi connection遠端連線
- 基本的Linux操作指令
- 了解user,group,資料夾和檔案權限rwx的管理
- tunnel連線[待整理資料](./tunnel連線待整理資料.md)
  - 使用ssh tunnel連線
  - 使用ngrok tunnel連線(建立遠端連線通道,開發階段使用)
  - 使用Tailscale tunnel連線(建立虛擬區網)
  - 使用cloudflare tunnel連線(遠端連線使用,正式上線使用)
- 本機安裝應用程式(npm,pip)
  - nodejs 安裝
  - uv安裝
  - miniconda安裝


- 使用openWebUI API
- 使用Ollama 和 OpenWebUI應用
- 使用openWebUI API

## [raspberry pi安裝流程說明](./pi安裝流程說明/README.md)
## [透過ssh連線,輸入中文會有亂碼的解決方法](./透過ssh連線-輸入中文會有亂碼的解決方法.md)
## [Linux指令操作說明](./Linux指令操作說明)
  
## ollama安裝流程說明
## openwebui安裝流程說明
## ngrok tunnel連線說明
## cloudflare tunnel連線說明
## [file_server安裝流程說明](./file_server安裝流程說明/README.md)
## [前端開發環境配置](./前端開發環境配置/README.md)
