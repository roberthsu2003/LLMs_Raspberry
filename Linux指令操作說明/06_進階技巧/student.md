# 進階技巧練習 – 學生作業

以下題目請在你的 Linux 環境（Raspberry Pi、Docker、或任意 Linux 主機）上依序完成。每完成一步，請使用指令列印輸出（`echo`、`cat`、`ls -l`、`journalctl` 等）或截圖保存，作為作業回報的依據。

---

## 1️⃣ 文字搜尋與過濾 – `grep`

1. 在當前目錄下建立兩個測試檔 `file1.txt`、`file2.md`，內容分別包含多行文字，其中至少有兩行包含單字 **Linux**（大小寫隨意）。  
2. 使用 `grep -rin --color=auto "linux" *.txt *.md` 搜尋所有檔案，記錄顯示的 **檔名、行號** 與匹配行。  
3. 再次搜尋，加入 `-i` 參數忽略大小寫，確認結果與上一步相同。  
4. 使用 `grep -rl "TODO" .`（若無 `TODO`，自行在任意檔案加入一行 `# TODO: ...`），列出所有包含 `TODO` 的檔案路徑。

---

## 2️⃣ 檔案與目錄搜尋 – `find`

1. 在家目錄下建立一個測試目錄 `find_demo`，其中放入以下檔案：
   - `large.log`（使用 `dd if=/dev/zero of=large.log bs=1M count=20` 產生約 20 MiB）  
   - `old.txt`（使用 `touch -t 202001010000 old.txt` 設定為 2020‑01‑01）  
   - `script.sh`（任意小腳本）  
2. 執行 `find . -type f -name "*.log"`，確認只找到 `large.log`。  
3. 執行 `find . -size +10M`，找出大於 10 MiB 的檔案，記錄其完整路徑。  
4. 執行 `find . -mtime -30`，列出最近 30 天內修改過的檔案，確認 `old.txt` 不在結果中。  
5. 使用 `-exec` 參數刪除所有 `.txt` 檔案（先 `echo` 確認會刪除哪些檔案），指令形式：`find . -name "*.txt" -exec echo "刪除：" {} \;`，之後改為 `-exec rm {} \;` 完成刪除。

---

## 3️⃣ 流式文字處理 – `awk` 與 `sed`

### 3.1 `awk`

1. 以 `awk -F: '{print $1 "\t" $3}' /etc/passwd` 列出所有系統使用者與 UID，將結果存入 `users_uid.txt`。  
2. 使用 `awk '{sum+=$5} END {print "總大小 (KB):", sum/1024}' *` 計算當前目錄所有檔案的總大小（以 KB 為單位），將結果寫入 `size_report.txt`。  
3. 以 `ps aux | awk '$8=="R"{print $2, $11}'` 找出所有正執行（R）狀態的行程，將 PID 與指令列印出來。

### 3.2 `sed`

1. 在 `script.sh`（前一步建立的腳本）中，使用 `sed -i 's/echo/printf/g' script.sh` 把所有 `echo` 改成 `printf`，確認檔案內容已變更。  
2. 刪除 `script.sh` 中的第 3 行（若不存在自行插入三行測試文字），使用 `sed -i '3d' script.sh`。  
3. 使用 `sed = script.sh | sed 'N; s/\n/\t/'` 為每行加上行號並顯示在終端。

---

## 4️⃣ 壓縮與解壓 – `tar`、`gzip`、`xz`

1. 把剛才的 `find_demo` 目錄打包並使用 gzip 壓縮：`tar -czvf find_demo.tar.gz find_demo/`。  
2. 列出壓縮檔內容而不解壓：`tar -tzvf find_demo.tar.gz`，確認所有檔案均在清單中。  
3. 解壓縮到新目錄 `find_demo_extracted`：`mkdir find_demo_extracted && tar -xzvf find_demo.tar.gz -C find_demo_extracted`。  
4. 使用 xz 重新壓縮：`tar -cJvf find_demo.tar.xz find_demo/`，同樣列出與解壓縮驗證。

---

## 5️⃣ 網路下載 – `curl`、`wget`

1. 使用 `wget https://raw.githubusercontent.com/git/git/master/README.md -O git_readme.md` 下載 Git 官方 README。  
2. 用 `curl -I https://api.github.com` 取得 HTTP 標頭，將結果寫入 `github_header.txt`。  
3. 以 `curl` 下載並直接解壓縮遠端的 tar.gz 檔（示例）：`curl -L https://github.com/vim/vim/archive/refs/heads/master.tar.gz | tar -xzv`，確認 `vim-master` 目錄出現在當前路徑。  

---

## 6️⃣ 遠端連線與檔案傳輸 – `ssh`、`scp`、`rsync`

> **前置作業**：請先在本機產生 SSH 金鑰（`ssh-keygen -t rsa -b 4096`），並將公鑰上傳至遠端測試機（`ssh-copy-id user@remote-host`），確保免密碼登入。

1. 使用 `ssh user@remote-host 'hostname && uptime'` 取得遠端主機名稱與負載資訊。  
2. 使用 `scp ./git_readme.md user@remote-host:/tmp/` 把剛才下載的檔案傳到遠端 `/tmp` 目錄，然後在遠端執行 `ssh user@remote-host 'ls -l /tmp/git_readme.md'` 確認檔案存在。  
3. 使用 `rsync -avz --progress ./find_demo/ user@remote-host:/home/user/remote_demo/` 同步整個目錄，並在遠端確認目錄結構與檔案完整性。  

---

## 7️⃣ 環境變數、別名與 Shell 設定

1. 在當前終端機設定臨時環境變數：`export MY_PROJECT="AdvancedLinux"`，使用 `echo $MY_PROJECT` 確認。  
2. 把上述變數寫入 `~/.bashrc`（或 `~/.zshrc`），指令：`echo 'export MY_PROJECT="AdvancedLinux"' >> ~/.bashrc && source ~/.bashrc`，重新開啟一個終端驗證變數仍在。  
3. 建立別名 `ll='ls -alF --color=auto'`，先在當前終端 `alias ll='ls -alF --color=auto'` 測試，然後永久寫入 `~/.bashrc`：`echo "alias ll='ls -alF --color=auto'" >> ~/.bashrc && source ~/.bashrc`，測試 `ll` 是否生效。  

---

## 8️⃣ 簡易 Bash 腳本

1. 在當前目錄建立腳本 `backup.sh`，內容如下（使用 `#!/bin/bash` 開頭）：

   ```bash
   #!/bin/bash
   # 備份指定目錄到 $HOME/backups，保留最近 5 次備份
   SRC="${1:-$HOME}"
   TIMESTAMP=$(date +%Y%m%d_%H%M%S)
   DEST="$HOME/backups/$TIMESTAMP"

   mkdir -p "$DEST"
   rsync -a --delete "$SRC/" "$DEST/"

   # 移除超過 5 次的備份
   ls -1dt $HOME/backups/* | tail -n +6 | xargs -d '\n' rm -rf

   echo "Backup of $SRC completed at $DEST"
   ```

2. 給予執行權限：`chmod +x backup.sh`。  
3. 執行腳本備份家目錄：`./backup.sh $HOME`，確認 `$HOME/backups` 內產生新目錄，且 `ls -l $HOME/backups` 顯示最近的備份。  
4. 重複執行三次，驗證只保留最近 5 次（使用 `ls -1 $HOME/backups` 檢查目錄數量）。  

---

## 9️⃣ 系統服務管理 – `systemd`

1. 建立簡易服務檔案 `/etc/systemd/system/hello.service`（需要 sudo）：

   ```ini
   [Unit]
   Description=Hello World Service

   [Service]
   ExecStart=/usr/bin/bash -c 'while true; do echo "Hello at $(date)"; sleep 60; done'
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```

2. 重新載入 daemon：`sudo systemctl daemon-reload`。  
3. 啟用並啟動服務：`sudo systemctl enable hello.service && sudo systemctl start hello.service`。  
4. 使用 `systemctl status hello.service` 確認服務正在執行，並觀察輸出（`journalctl -u hello.service -n 5`）顯示最近的 `Hello` 訊息。  
5. 停止與禁用服務：`sudo systemctl stop hello.service && sudo systemctl disable hello.service`，再次確認狀態為 `inactive (dead)`。  

---

## 🔟 日誌檢視 – `journalctl`

1. 查看最近 20 行系統日誌：`journalctl -n 20`，將輸出保存至 `syslog_recent.txt`。  
2. 只顯示 `hello.service` 產生的日誌：`journalctl -u hello.service`（若已停用可先啟動服務），確認其中包含 `Hello at …` 訊息。  
3. 以時間範圍過濾日誌，例如顯示今天的所有日誌：`journalctl --since "today"`，把結果寫入 `today_log.txt`。  
4. 使用 `-f` 持續追蹤新日誌（類似 `tail -f`），在另一個終端執行 `journalctl -f`，同時在第一個終端觸發一些系統事件（如 `sudo apt update`），觀察即時輸出。  

---

## 📂 作業提交說明

完成所有練習後，請把以下資訊整理成一份報告（文字檔或 PDF）：

- 每一步的指令與對應輸出（可直接貼上終端文字或截圖）。  
- 遇到的錯誤訊息與解決方式（特別是 `systemd`、`rsync`、`chmod` 等需要 sudo 的操作）。  
- 加分挑戰的完成結果與個人感想。  

祝練習順利，期待看到你的作業！