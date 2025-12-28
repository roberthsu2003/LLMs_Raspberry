# 行程操作練習 – 學生作業

以下題目請在你的 Linux 環境（Raspberry Pi、Docker、或任何 Linux 主機）上依序完成。每完成一步，請使用 `ps`、`top`、`pgrep`、`kill` 或將指令輸出截圖保存，作為作業回報的依據。

---

## 1️⃣ 基本行程查詢

1. 執行 `ps -u $(whoami) -f`，列出目前使用者的所有行程，寫下最上面的 **PID** 與 **COMMAND**。  
2. 執行 `ps -eo pid,%cpu,%mem,cmd --sort=-%cpu | head -n 5`，找出 CPU 使用率最高的 5 個行程，記錄其 **PID** 與 **%CPU**。  
3. 使用 `top` 觀察系統資源，按 `q` 退出。將 `top` 畫面中 **CPU**、**MEM** 使用率的數值記錄下來。  

---

## 2️⃣ 使用 `pgrep` 與 `pkill`

1. 用 `pgrep -l bash` 找出所有 `bash` 相關的行程，列出它們的 **PID** 與名稱。  
2. 若系統中有 `sleep` 行程，使用 `pkill sleep` 終止它們。之後再執行 `pgrep sleep` 確認已無結果。  

---

## 3️⃣ 背景執行與作業控制

1. 在終端機中執行 `sleep 120 &`，使其在背景執行，記錄回傳的 **Job ID**（如 `[1] 12345`）。  
2. 執行 `jobs`，確認背景作業仍在列表中。  
3. 使用 `fg %1`（或相對應的 Job ID）把剛才的 `sleep` 拉回前景，觀察它是否繼續執行。  
4. 按 `Ctrl+Z` 暫停前景作業，使用 `bg %1` 讓它在背景繼續執行。最後使用 `kill %1` 終止該作業。  

---

## 4️⃣ 使用 `nice` 與 `renice`

1. 以較低優先權（nice +10）執行一個 CPU 密集指令，例如：
   ```sh
   nice -n 10 dd if=/dev/zero of=/dev/null bs=1M count=1024
   ```
2. 在另一個終端機中使用 `ps -eo pid,nice,cmd | grep dd`，找出剛才指令的 **PID** 與 **NI**（nice 值），確認其為 10。  
3. 使用 `renice -5 -p <PID>` 把該行程的 nice 值調整為 -5，重新檢查結果。  

---

## 5️⃣ 使用 `kill` 終止行程

1. 執行 `sleep 300 &`，取得其 **PID**（如 5678）。  
2. 使用 `kill 5678` 送出 **SIGTERM**，觀察 `ps` 是否仍顯示該行程。  
3. 若仍在，使用 `kill -9 5678` 送出 **SIGKILL**，確認行程已消失。  

---

## 6️⃣ 監控與自動化（挑戰題）

1. 建立簡易監控腳本 `monitor.sh`，內容如下（使用 `#!/bin/bash` 開頭）：

   ```sh
   #!/bin/bash
   # 每 5 秒檢查 myservice 是否在執行，若未執行則自動啟動
   while true; do
       if ! pgrep -x "myservice" > /dev/null; then
           echo "$(date): myservice not running, restarting..." >> ~/monitor.log
           /usr/local/bin/myservice &
       fi
       sleep 5
   done
   ```

2. 給予腳本執行權限：`chmod +x monitor.sh`。  
3. 使用 `nohup ./monitor.sh &` 在背景執行，並用 `ps -ef | grep monitor.sh` 確認它在執行。  
4. 停止腳本時，先找到其 **PID**，使用 `kill <PID>` 終止，或直接 `pkill -f monitor.sh`。  

---

## 7️⃣ 小挑戰（加分題）

1. 使用 `watch` 每 2 秒顯示一次系統上 CPU 使用率最高的 3 個行程：
   ```sh
   watch -n 2 "ps -eo pid,%cpu,cmd --sort=-%cpu | head -n 4"
   ```
2. 建立一個名為 `project` 的資料夾結構：
   ```sh
   mkdir -p project/src project/docs project/tests
   ```
3. 在 `src` 中建立腳本 `run.sh`，內容：
   ```sh
   #!/bin/bash
   echo "Running project script"
   ```
   設定權限為 `chmod 755 run.sh`，執行 `./project/src/run.sh`，確認輸出。  
4. 把 `src` 目錄的權限改為 `770`，讓同屬 `project` 群組的使用者也能執行腳本，驗證效果。  

---

## 作業提交說明

完成所有練習後，請把以下資訊整理成一份報告（文字檔或 PDF）：

- 每一步的指令與對應輸出（可直接貼上終端機文字或截圖）。  
- 遇到的錯誤訊息與解決方式（特別是第 5 題的 `kill` 操作）。  
- 加分挑戰的完成結果與個人感想。  

祝練習順利，期待看到你的作業！