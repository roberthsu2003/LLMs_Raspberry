# 進階技巧教學 – 老師示範

本文件為教師在課堂上示範 Linux 常見進階指令與技巧的教案，內容涵蓋文字處理、檔案搜尋、壓縮與傳輸、遠端連線、環境變數與別名、簡易腳本與服務管理等。請依序在終端機執行以下指令，並逐一說明每一步的目的與結果，讓學生能在實務情境中熟練這些工具。

---

## 1️⃣ 文字搜尋與過濾 – `grep`

### 說明
- `grep` 用於在檔案或輸出中搜尋符合模式的行。  
- 常用參數：
  - `-i`：忽略大小寫  
  - `-r`：遞迴搜尋目錄  
  - `-n`：顯示行號  
  - `--color=auto`：高亮顯示匹配文字  

### 示範指令
```sh
# 在當前目錄遞迴搜尋所有 .md 檔中出現「Linux」的行，顯示行號與彩色高亮
grep -rin --color=auto "Linux" *.md

# 同時排除 .git 目錄
grep -rin --exclude-dir=.git "error" .

# 只列出檔名（不顯示匹配內容）
grep -rl "TODO" .
```

---

## 2️⃣ 檔案與目錄搜尋 – `find`

### 說明
- `find` 能根據名稱、大小、時間、權限等條件搜尋檔案。  
- 常用參數：
  - `-name`、`-iname`：依檔名（大小寫不敏感）  
  - `-type f` / `-type d`：限定檔案或目錄  
  - `-size +10M`：大於 10 MiB 的檔案  
  - `-mtime -7`：最近 7 天內修改過的檔案  

### 示範指令
```sh
# 找出當前目錄下所有 .log 檔
find . -type f -name "*.log"

# 找出大小超過 100 MiB 的檔案，並顯示完整路徑
find /var -type f -size +100M

# 同時執行刪除（-exec rm {} \;）前先列出
find . -name "*.tmp" -exec echo "將刪除：" {} \;

# 使用 xargs 結合 rm（更快）
find . -name "*.bak" -print0 | xargs -0 rm -v
```

---

## 3️⃣ 流式文字處理 – `awk` 與 `sed`

### 3.1 `awk` 基礎
- 以欄位為單位處理文字，預設分隔符為空白。  
- 常用語法：`awk '{print $1,$3}' file`  

#### 示範
```sh
# 顯示 /etc/passwd 的使用者名稱與 UID
awk -F: '{print $1 "\t" $3}' /etc/passwd

# 計算當前目錄下所有檔案的總大小（KB）
ls -l | awk '{sum+=$5} END {print "Total size:", sum/1024, "KB"}'

# 只列出狀態為「R」的行程（配合 ps）
ps aux | awk '$8=="R"{print $2, $11}'
```

### 3.2 `sed` 基礎
- 文字取代與行編輯的流編輯器。  
- 常用語法：`sed 's/old/new/g' file`  

#### 示範
```sh
# 把檔案內所有 "foo" 換成 "bar"
sed -i 's/foo/bar/g' example.txt

# 刪除檔案中第 3 行
sed -i '3d' example.txt

# 在每行前面加上行號
sed = example.txt | sed 'N; s/\n/\t/'
```

---

## 4️⃣ 壓縮與解壓 – `tar`、`gzip`、`xz`

### 說明
- `tar` 用於打包，多數情況會搭配壓縮工具（`gzip`、`bzip2`、`xz`）。  
- 常用參數：
  - `-c`：建立檔案  
  - `-x`：解壓縮  
  - `-v`：顯示過程  
  - `-f`：指定檔名  
  - `-z`、`-j`、`-J`：分別使用 gzip、bzip2、xz  

### 示範指令
```sh
# 打包並 gzip 壓縮整個 project 目錄
tar -czvf project.tar.gz project/

# 解壓縮
tar -xzvf project.tar.gz

# 使用 xz（更高壓縮率）
tar -cJvf backup.tar.xz /var/log

# 列出 tar 檔內容而不解壓
tar -tzvf project.tar.gz
```

---

## 5️⃣ 網路下載 – `curl`、`wget`

### 說明
- `curl` 與 `wget` 都能從 HTTP/HTTPS/FTP 下載檔案，`curl` 更適合 API 呼叫與資料管道。  

### 示範
```sh
# 直接下載檔案（wget）
wget https://example.com/file.zip -O downloaded.zip

# 只取得標頭資訊（curl）
curl -I https://api.github.com/repos/octocat/Hello-World

# 使用 POST 送出 JSON（curl）
curl -X POST -H "Content-Type: application/json" \
     -d '{"name":"test","value":123}' \
     https://httpbin.org/post

# 下載後直接解壓（管道結合 tar）
curl -L https://example.com/archive.tar.gz | tar -xzv
```

---

## 6️⃣ 遠端連線與檔案傳輸 – `ssh`、`scp`、`rsync`

### 說明
- `ssh` 提供安全的遠端 shell；`scp` 用於簡易檔案傳輸；`rsync` 支援增量同步與壓縮。  

### 示範
```sh
# 以密鑰登入遠端主機（假設已配置公鑰）
ssh pi@192.168.1.100

# 複製本機檔案到遠端
scp local.txt pi@192.168.1.100:/home/pi/

# 從遠端同步整個資料夾（保留權限與時間）
rsync -avz --progress pi@192.168.1.100:/home/pi/project ./project_backup
```

---

## 7️⃣ 環境變數、別名與 Shell 設定

### 7.1 環境變數
```sh
# 顯示目前所有環境變數
printenv

# 設定臨時變數（只在當前終端有效）
export MY_VAR="HelloWorld"

# 永久設定（寫入 ~/.bashrc 或 ~/.zshrc）
echo 'export PATH=$PATH:/opt/mytools' >> ~/.bashrc
source ~/.bashrc
```

### 7.2 別名
```sh
# 建立常用別名
alias ll='ls -alF --color=auto'
alias gs='git status'

# 永久保存
echo "alias ll='ls -alF --color=auto'" >> ~/.bashrc
source ~/.bashrc
```

---

## 8️⃣ 簡易 Bash 腳本

### 範例腳本 `backup.sh`
```sh
#!/bin/bash
# 備份指定目錄到 /backup，保留 7 天內的備份
SRC_DIR="${1:-$HOME}"
DEST_DIR="/backup/$(date +%Y%m%d_%H%M%S)"

mkdir -p "$DEST_DIR"
rsync -a --delete "$SRC_DIR/" "$DEST_DIR/"

# 移除超過 7 天的備份
find /backup -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \;

echo "Backup of $SRC_DIR completed at $DEST_DIR"
```
- **使用方式**：`chmod +x backup.sh && ./backup.sh /path/to/target`

---

## 9️⃣ 系統服務管理 – `systemd`

### 基本指令
```sh
# 查看服務狀態
systemctl status nginx

# 啟動、停止、重新啟動
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx

# 設定開機自動啟動
sudo systemctl enable nginx
sudo systemctl disable nginx

# 重新載入單元檔（修改後使用）
sudo systemctl daemon-reload
```

### 建立自訂服務範例 `/etc/systemd/system/myjob.service`
```ini
[Unit]
Description=簡易每日任務

[Service]
Type=simple
ExecStart=/usr/local/bin/myjob.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
- 啟用：`sudo systemctl enable myjob.service && sudo systemctl start myjob.service`

---

## 10️⃣ 日誌檢視 – `journalctl`

### 常用指令
```sh
# 查看最近 20 行系統日誌
journalctl -n 20

# 按時間範圍過濾
journalctl --since "2025-12-01" --until "2025-12-28"

# 只顯示特定服務（例如 nginx）
journalctl -u nginx

# 持續追蹤新日誌（類似 tail -f）
journalctl -f
```

---

## 小結

- **文字搜尋**：`grep`、`awk`、`sed`  
- **檔案搜尋**：`find`、`xargs`  
- **壓縮與傳輸**：`tar`、`gzip`/`xz`、`curl`/`wget`、`scp`/`rsync`  
- **遠端操作**：`ssh`、`rsync`  
- **環境與別名**：`export`、`alias`、`~/.bashrc`  
- **腳本與自動化**：Bash 基礎、`systemd`、`journalctl`  

在示範每個指令後，請讓學生自行在終端機練習，並即時檢查結果（例如 `ls -l`、`ps -ef`、`cat /var/log/syslog`），確保概念已內化。祝教學順利！