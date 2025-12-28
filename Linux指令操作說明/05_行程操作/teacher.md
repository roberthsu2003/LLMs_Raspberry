# 行程操作教學 – 老師示範

本文件提供教師在課堂上示範 Linux 行程（process）管理的完整教案，涵蓋概念說明、常用指令、進階技巧與除錯範例。請依序在終端機執行以下指令，並逐一解說每一步的目的與結果，讓學生能在實作中掌握系統資源的使用與控制。

---

## 1️⃣ 行程概念基礎

| 名稱 | 說明 |
|------|------|
| **PID** (Process ID) | 系統分配給每個行程的唯一編號。 |
| **PPID** (Parent PID) | 產生該行程的父行程 ID。 |
| **TTY** | 行程所屬的終端設備（`?` 表示非終端行程，如 daemon）。 |
| **STAT** | 行程狀態：`R` 執行、`S` 休眠、`Z` 殭屍、`T` 停止等。 |
| **%CPU / %MEM** | 行程使用的 CPU 與記憶體佔比。 |

> **小提醒**：在多使用者系統中，非 root 使用者只能看到自己擁有的行程。

---

## 2️⃣ 常用行程查詢指令

### 2.1 `ps` 系列

```sh
# 顯示當前使用者的所有行程（完整格式）
ps -u $(whoami) -f

# 列出系統上所有行程（需要 sudo 取得完整資訊）
sudo ps aux

# 只顯示 PID、CPU、記憶體與指令欄位
ps -eo pid,%cpu,%mem,cmd --sort=-%cpu | head -n 10
```

*說明*：`aux` 為常見組合，`-eo` 可自訂欄位，`--sort` 讓結果依指定欄位排序。

### 2.2 `top` / `htop`

```sh
# 即時監控系統資源（按 q 退出）
top

# 若已安裝 htop，使用更友好的介面
htop
```

*說明*：`top` 內建於大多數 Linux 發行版；`htop` 支援滑鼠與彩色顯示，適合新手觀察。

### 2.3 `pgrep` / `pkill`

```sh
# 找出所有名稱含 "python" 的行程 PID
pgrep -l python

# 終止所有名稱含 "sleep" 的行程
pkill sleep
```

*說明*：`pgrep` 只回傳 PID，`pkill` 直接發送 `SIGTERM`（可加 `-9` 強制）。

### 2.4 `pidof`（僅限部分發行版）

```sh
# 取得單一程式的 PID（如 sshd）
pidof sshd
```

---

## 3️⃣ 行程控制指令

### 3.1 `kill` 系列

```sh
# 以 PID 終止行程（預設 SIGTERM）
kill 1234

# 強制終止（SIGKILL）
kill -9 1234

# 使用訊號名稱
kill -SIGSTOP 1234   # 暫停
kill -SIGCONT 1234   # 繼續
```

*說明*：`SIGTERM` 給予程式自行清理的機會；`SIGKILL` 直接強制關閉，無法捕獲。

### 3.2 `nice` / `renice`

```sh
# 以較低優先權（nice +5）執行長時間指令
nice -n 5 dd if=/dev/zero of=bigfile bs=1M count=1024

# 調整已在執行的行程優先權（PID 為 5678）
renice +10 -p 5678
```

*說明*：`nice` 數值範圍 -20（最高）到 +19（最低），`renice` 可改變已執行行程的優先權。

### 3.3 背景執行與作業控制

```sh
# 將指令放到背景（&）
sleep 60 &

# 查看目前的工作（jobs）
jobs

# 前景執行（fg）或將背景作業放回前景
fg %1

# 讓已在前景的指令暫停（Ctrl+Z），再送到背景（bg）
Ctrl+Z
bg %1
```

*說明*：`jobs` 顯示由當前 shell 管理的作業；`%N` 為作業編號。

### 3.4 `nohup` 與 `disown`

```sh
# 讓指令即使關閉終端仍持續執行，並把輸出寫入 nohup.out
nohup ./long_running_task.sh &

# 把已在背景的作業從 shell 中解除（不會因關閉終端被終止）
disown %1
```

*說明*：適用於遠端 SSH 後斷線仍希望程式持續執行的情境。

---

## 4️⃣ 進階範例：監控與自動化

### 4.1 使用 `watch` 觀察特定指令

```sh
# 每 2 秒顯示一次 CPU 前 5 名佔用最高的行程
watch -n 2 "ps -eo pid,%cpu,cmd --sort=-%cpu | head -n 6"
```

### 4.2 自動重啟失敗的服務（簡易腳本）

```sh
#!/bin/bash
# monitor.sh：監控 myservice，若死亡則自動重啟

while true; do
    if ! pgrep -x "myservice" > /dev/null; then
        echo "$(date): myservice not running, restarting..." >> /var/log/monitor.log
        /usr/local/bin/myservice &
    fi
    sleep 30
done
```

將此腳本放在 `/opt/monitor.sh`，使用 `nohup /opt/monitor.sh &` 背景執行。

---

## 5️⃣ 常見錯誤與除錯技巧

| 錯誤訊息                     | 可能原因                         | 解決方式                                   |
|----------------------------|--------------------------------|-------------------------------------------|
| `kill: (1234) - No such process` | PID 已不存在或輸入錯誤          | 使用 `ps -ef | grep <name>` 重新確認 PID |
| `ps: permission denied`    | 非 root 嘗試查看其他使用者行程   | 使用 `sudo ps aux` 或只查看自己的行程   |
| `nohup: ignoring input and appending output to 'nohup.out'` | 正常訊息，表示已成功在背景執行 | 確認 `nohup.out` 是否產生預期輸出        |
| `pgrep: unknown option`    | 使用舊版 `pgrep` 不支援 `-l`    | 改用 `pgrep <name>` 再搭配 `ps -p` 查詢   |

---

## 6️⃣ 小結

- `ps`、`top` / `htop`：即時或靜態檢視行程資訊。  
- `kill`、`pkill`、`pgrep`：搜尋與終止特定行程。  
- `nice` / `renice`：調整 CPU 調度優先權。  
- `&`、`jobs`、`fg`、`bg`、`nohup`、`disown`：背景執行與作業控制。  
- `watch`、自動化腳本：提升監控與自動恢復能力。

在示範每個指令後，請讓學生自行在終端機練習，並即時使用 `ps -ef`、`jobs`、`ls -l` 等檢查變化，確保概念已內化。祝教學順利！
