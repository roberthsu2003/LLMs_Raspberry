# 綜合測驗 – 學生練習與作業說明

以下題目設計讓你在完整的 Linux 工作流程中，結合已學習的目錄、檔案、權限、使用者、行程、文字處理、服務與日誌等概念。請依序在你的 Raspberry Pi（或任意 Linux 主機）上完成每一步，將指令、執行結果與任何錯誤訊息記錄下來（可直接貼在筆記或截圖），最後彙整成一份報告（文字檔或 PDF）提交。

---

## 📋 作業流程概覽

| 步驟 | 目標說明 | 需要的指令/概念 |
|------|----------|----------------|
| 1️⃣   | 建立測驗專案目錄結構 | `mkdir -p`、`cd` |
| 2️⃣   | 檔案建立與權限設定 | `touch`、`echo`、`chmod`、`chown`、`chgrp` |
| 3️⃣   | 使用者與群組管理 | `sudo groupadd`、`sudo usermod -aG` |
| 4️⃣   | 行程控制與監控 | `sleep &`、`ps`、`kill`、`SIGSTOP`/`SIGCONT` |
| 5️⃣   | 文字搜尋與取代 | `grep`、`awk`、`sed` |
| 6️⃣   | 壓縮、傳輸與遠端驗證 | `tar`、`scp`、`ssh`、`rsync` |
| 7️⃣   | Systemd 服務建立與日誌檢視 | `systemctl`、`journalctl` |
| 8️⃣   | 加分挑戰（可選） | `find`、`xargs`、`rsync` 增量同步 |
| 📦   | 作業提交 | 整理指令、輸出、錯誤與心得 |

---

## 1️⃣ 建立測驗專案目錄結構

1. 在家目錄下建立根目錄 **final_test**，並在其中建立子目錄 **project/src、project/docs、project/tests**。  
   ```sh
   mkdir -p ~/final_test/project/{src,docs,tests}
   ```
2. 使用 `tree -L 2 ~/final_test`（若未安裝 `tree`，先 `sudo apt install -y tree`）確認目錄結構正確。

---

## 2️⃣ 檔案建立與權限設定

1. 在 **src** 目錄建立 `main.py`，內容為簡單的 Python 輸出：  
   ```sh
   cat > ~/final_test/project/src/main.py <<'EOF'
   #!/usr/bin/env python3
   print("Hello, Linux!")
   EOF
   ```
2. 為 `main.py` 設定 **744** 權限（所有人可讀，擁有者可讀寫執行）：  
   ```sh
   chmod 744 ~/final_test/project/src/main.py
   ```
3. 確認權限與擁有者：  
   ```sh
   ls -l ~/final_test/project/src/main.py
   ```
   預期顯示 `-rwxr--r--`。

4. 在 **docs** 目錄建立說明檔 `README.md`，寫入任意說明文字，設定權限為 **664**（所有人可讀，擁有者可寫）：  
   ```sh
   echo "# Project Documentation" > ~/final_test/project/docs/README.md
   chmod 664 ~/final_test/project/docs/README.md
   ```

---

## 3️⃣ 使用者與群組管理

> **注意**：以下操作需要 `sudo` 權限。

1. 建立新群組 **developers**：  
   ```sh
   sudo groupadd developers
   ```
2. 把目前使用者（假設為 `pi`）加入 `developers` 群組：  
   ```sh
   sudo usermod -aG developers $USER
   ```
3. 把 `README.md` 的群組改為 `developers`，確認權限仍為 **664**：  
   ```sh
   sudo chgrp developers ~/final_test/project/docs/README.md
   ls -l ~/final_test/project/docs/README.md
   ```

---

## 4️⃣ 行程控制與監控

1. 在背景執行 `sleep 300`，取得 PID：  
   ```sh
   sleep 300 &
   PID=$!
   echo "PID: $PID"
   ```
2. 使用 `ps -p $PID -o pid,stat,cmd` 確認狀態為 **S**（睡眠）。  
3. 暫停行程（`SIGSTOP`）並再次檢查：  
   ```sh
   kill -SIGSTOP $PID
   ps -p $PID -o pid,stat,cmd
   ```
4. 恢復行程（`SIGCONT`）並最後強制結束（`SIGKILL`）：  
   ```sh
   kill -SIGCONT $PID
   kill -9 $PID
   ps -p $PID   # 應無輸出，表示已結束
   ```

---

## 5️⃣ 文字搜尋與取代

1. 在 **tests** 目錄建立測試檔 `log.txt`，內容包含多行文字，至少兩行包含關鍵字 **ERROR**（大小寫隨意）：  
   ```sh
   cat > ~/final_test/project/tests/log.txt <<'EOF'
   Initialization complete.
   ERROR: Failed to load config.
   Running routine.
   error: unable to connect.
   Shutdown.
   EOF
   ```
2. 使用 `grep -i "error" log.txt` 列出所有錯誤行，記錄輸出。  
3. 使用 `awk '{print NR, $0}' log.txt` 為每行加上行號，保存結果至 `log_numbered.txt`：  
   ```sh
   awk '{print NR, $0}' ~/final_test/project/tests/log.txt > ~/final_test/project/tests/log_numbered.txt
   ```
4. 使用 `sed` 把所有 **ERROR** 替換成 **WARN**（保留大小寫）：  
   ```sh
   sed -i 's/ERROR/WARN/g; s/error/warn/g' ~/final_test/project/tests/log.txt
   cat ~/final_test/project/tests/log.txt
   ```

---

## 6️⃣ 壓縮、傳輸與遠端驗證

> **前置作業**：若尚未產生 SSH 金鑰，先 `ssh-keygen -t rsa -b 4096`，再 `ssh-copy-id user@remote-host`。

1. 把整個 `final_test` 目錄打包為 gzip 壓縮檔：  
   ```sh
   tar -czvf ~/final_test.tar.gz -C ~ final_test
   ```
2. 使用 `scp` 把壓縮檔傳到遠端主機（假設 `user@remote-host`）：  
   ```sh
   scp ~/final_test.tar.gz user@remote-host:/tmp/
   ```
3. 在遠端解壓並確認目錄結構：  
   ```sh
   ssh user@remote-host 'tar -tzvf /tmp/final_test.tar.gz'
   ```
4. 若想同步檔案（增量備份），使用 `rsync`：  
   ```sh
   rsync -avz --progress ~/final_test/ user@remote-host:/home/user/remote_final_test/
   ```

---

## 7️⃣ Systemd 服務建立與日誌檢視

1. 在本機建立簡易服務檔案 `hello.service`（路徑 `/etc/systemd/system/hello.service`），內容如下（需要 `sudo`）：  
   ```sh
   sudo tee /etc/systemd/system/hello.service > /dev/null <<'EOF'
   [Unit]
   Description=Hello World Service

   [Service]
   ExecStart=/usr/bin/bash -c 'while true; do echo "Hello at $(date)"; sleep 60; done'
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   EOF
   ```
2. 重新載入 systemd、啟用並立即啟動服務：  
   ```sh
   sudo systemctl daemon-reload
   sudo systemctl enable --now hello.service
   ```
3. 檢查服務狀態：  
   ```sh
   systemctl status hello.service
   ```
4. 用 `journalctl` 查看最近三條日誌，確保有 `Hello at …` 訊息：  
   ```sh
   journalctl -u hello.service -n 3
   ```
5. **加分題**：停止並禁用服務，確認狀態變為 `inactive (dead)`：  
   ```sh
   sudo systemctl stop hello.service
   sudo systemctl disable hello.service
   systemctl status hello.service
   ```

---

## 8️⃣ 加分挑戰（可選）

### 8.1 使用 `find` 找出大型檔案
1. 在家目錄下搜尋所有大於 **10 MiB** 的檔案，結果寫入 `big_files.txt`：  
   ```sh
   find $HOME -type f -size +10M > ~/final_test/big_files.txt
   ```
2. 用 `tar` 把這些檔案一次打包為 `big_files.tar.gz`：  
   ```sh
   tar -czvf ~/final_test/big_files.tar.gz -T ~/final_test/big_files.txt
   ```

### 8.2 遠端驗證大型檔案
1. 把 `big_files.tar.gz` 上傳至遠端（同第 6 步的方式），在遠端使用 `tar -tzvf` 列出檔案清單，確認完整性。

---

## 📄 作業提交說明

完成上述所有步驟後，請將以下資訊彙整成一份報告（文字檔或 PDF）提交：

1. **每一步的指令**（完整貼上）與 **執行結果**（`ls -l`、`ps`、`journalctl` 等輸出）。  
2. **遇到的錯誤訊息** 與 **解決過程**（如需 `sudo`、權限調整、路徑修正等）。  
3. **加分挑戰** 的完成情況與心得（若未完成可寫說明）。  
4. **自我反思**：哪個步驟最具挑戰性？學到了哪些新技巧？

> **提交格式**：  
> - 檔名 `final_test_report.md`（或 `final_test_report.pdf`）  
> - 目錄結構與檔案權限的截圖（可使用 `tree -L 3` 輸出）  
> - 若有遠端作業，請附上遠端 `ssh`、`scp`、`rsync` 的執行紀錄。

祝你完成測驗順利，期待看到你的完整作品！