# SSH Tunnel

## 為什麼要SSH Tunnel

## [區域網路](./local_network.md)

## SSH連線和SSH Tunnel有什麼不同

SSH連線是基本遠端登入功能，而SSH Tunnel則在SSH連線基礎上建立埠轉發通道，實現流量加密轉送與突破限制。

### 主要差別
SSH連線僅提供終端機存取（如`ssh pi@raspberry-ip`執行指令），不改變其他流量路徑；SSH Tunnel額外轉發指定埠流量，例如`ssh -L 8080:localhost:80 pi@raspberry-ip`讓本地8080埠連到Raspberry Pi的80埠服務。

### 功能比較

| 方面       | SSH連線                          | SSH Tunnel                          |
|------------|----------------------------------|-------------------------------------|
| **目的**  | 遠端Shell操作與檔案傳輸         | 加密轉發任意TCP流量（如Web、DB）   |
| **指令範例** | `ssh user@host`                 | `ssh -L localport:remotehost:port user@host` |
| **流量範圍** | 僅SSH埠22                       | 多埠轉發，偽裝成SSH流量            |
| **應用**  | 管理伺服器指令                  | 突破防火牆存取內網服務             |[1][6]

### 教學情境應用
在Windows Warp終端，SSH連線用於登入Raspberry Pi管理；Tunnel則用於安全存取受限服務，如MQTT埠1883，避免公網暴露。
