# 練習：從前景程序到系統服務

**目標：** 透過親手操作，體驗程序在前景、背景、以及系統服務三種模式的完整生命週期，深刻理解為何正式環境必須使用 systemd。

---

## 1️⃣ 體驗前景程序

**目標：** 理解前景程序如何「占用」終端機。

1. 在終端機輸入 `sleep 300` 並按下 Enter。
2. **思考與觀察：**
   - 你的終端機現在是什麼狀態？還能輸入其他指令嗎？
   - 這就是「前景程序」，它會佔用你的終端機直到執行完畢。
3. 按下 `Ctrl + C`。
4. **思考與觀察：**
   - 發生了什麼事？`sleep` 程序還在嗎？
   - 你如何確認 `sleep` 已經不在執行了？（提示：`ps aux | grep sleep`）

---

## 2️⃣ 將程序送到背景

**目標：** 學會使用 `&` 將程序放到背景執行，釋放終端機。

1. 這次，請輸入 `sleep 300 &` 並按下 Enter。
2. **觀察與記錄：**
   - 畫面上出現了什麼？（`[1] 12345` 的格式）
   - 記下你的「工作編號 (Job ID)」和「程序編號 (PID)」。
   - 終端機現在可以輸入指令了嗎？
3. 執行 `ps aux | grep sleep`，確認 `sleep` 程序仍在背景執行。

---

## 3️⃣ 背景工作控制

**目標：** 學習 `jobs`, `fg`, `bg`, `kill` 來靈活操作背景工作。

現在我們有一個在背景執行的工作，讓我們來操作它。

1. 執行 `jobs -l`。
   - **問題：** 這個指令告訴了你什麼？它顯示的資訊跟上一步記錄的一樣嗎？
2. 執行 `fg %1`（如果你的工作編號不是 1，請替換它）。
   - **觀察：** 終端機發生了什麼變化？`sleep` 程序現在在哪裡？
3. 這次，不要按 `Ctrl + C`，改為按下 `Ctrl + Z`。
   - **觀察與記錄：** 畫面上顯示了什麼狀態？（例如：`Stopped`）
   - 執行 `jobs -l`，看看 `sleep` 現在的狀態是什麼。
4. 執行 `bg %1`。
   - **觀察：** `sleep` 的狀態又變成了什麼？
5. 最後，使用 `kill %1` 來終止這個工作。
   - 執行 `jobs -l` 確認它已被 `Terminated`（終止）。
   - 執行 `ps aux | grep sleep` 確認它已從程序列表中消失。

---

## 4️⃣ 存活問題實驗：關閉終端機的影響

**目標：** 深刻體會 `SIGHUP` 信號的影響，以及 `nohup` 的作用與局限性。

這個練習將讓你深刻體會 `nohup` 的重要性。**你需要開啟兩個終端機視窗來完成。**

### 實驗 A：不使用 nohup

1. 在 **終端機 A** 中，執行 `sleep 300 &`。
2. 執行 `jobs` 確認它在背景執行。
3. 執行 `ps aux | grep sleep` 記錄 PID。
4. 現在，直接關閉 **終端機 A** 的視窗。
5. 在 **終端機 B** 中，執行 `ps aux | grep sleep`。
   - **問題：** 你還能找到 `sleep` 程序嗎？它去哪了？
   - **思考：** 為什麼關閉終端機後，程序會消失？

### 實驗 B：使用 nohup

1. 重新打開一個 **終端機 A**，這次執行 `nohup sleep 300 &`。
2. **觀察：** 你會看到一個關於 `nohup.out` 的訊息。
3. 執行 `ps aux | grep sleep` 記錄 PID。
4. 現在，再次關閉 **終端機 A** 的視窗。
5. 在 **終端機 B** 中，執行 `ps aux | grep sleep`。
   - **問題：** 這次 `sleep` 程序是否還在？
   - **進階思考：** `nohup` 和 `systemd` 服務有什麼本質上的不同？為什麼正式環境不能只用 `nohup`？

---

## 5️⃣ systemd 實作練習：建立第一個系統服務

**目標：** 透過完整的實作流程，理解 systemd 如何管理系統服務，以及它與背景工作、nohup 的根本差異。

### 練習目標

> **建立一個 systemd 服務，每 5 秒在 log 裡印一句話**
> 
> 關掉終端機、重新登入，它都還活著
> 
> 最後把它「乾乾淨淨地刪掉」

---

### Step 1：準備一個簡單的程式

1. 建立 Shell 腳本：
   ```bash
   sudo nano /usr/local/bin/hello-service.sh
   ```

2. **輸入以下內容：**
   ```bash
   #!/bin/bash
   
   while true
   do
     echo "Hello from systemd at $(date)"
     sleep 5
   done
   ```

3. **存檔後給執行權限：**
   ```bash
   sudo chmod +x /usr/local/bin/hello-service.sh
   ```

4. **思考問題：**
   - 這個程式有什麼特點？（提示：它會永遠執行下去）
   - 如果我們用 `./hello-service.sh &` 來執行，它會是「服務」嗎？為什麼？

---

### Step 2：建立 systemd 服務檔（核心）

1. 建立服務檔：
   ```bash
   sudo nano /etc/systemd/system/hello.service
   ```

2. **輸入以下內容：**
   ```ini
   [Unit]
   Description=My First systemd Demo Service
   
   [Service]
   ExecStart=/usr/local/bin/hello-service.sh
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

3. **理解每個區段：**
   - `[Unit]` 區段的作用是什麼？
   - `[Service]` 區段中的 `ExecStart` 指定了什麼？
   - `Restart=always` 這一行為什麼很重要？它和 `nohup` 有什麼不同？
   - `[Install]` 區段的作用是什麼？

---

### Step 3：讓 systemd「認識新服務」

1. 執行：
   ```bash
   sudo systemctl daemon-reload
   ```

2. **思考問題：**
   - 為什麼需要執行這個指令？
   - 如果沒有執行會發生什麼事？

---

### Step 4：啟動服務（關鍵轉折點）

1. 啟動服務：
   ```bash
   sudo systemctl start hello.service
   ```

2. **立刻檢查狀態：**
   ```bash
   systemctl status hello.service
   ```

3. **觀察與記錄：**
   - 服務的狀態是什麼？（應該是 `active (running)`）
   - 記錄下服務的 PID。
   - 注意：服務是否綁定了任何終端機？

4. **思考問題：**
   - 這一刻，服務已經「活在系統裡」了。這和 `&` 或 `nohup` 有什麼不同？

---

### Step 5：觀察服務運行（這一步超重要）

1. **即時查看 log：**
   ```bash
   journalctl -u hello.service -f
   ```

2. **觀察：** 你會看到每 5 秒出現一行：
   ```
   Hello from systemd at ...
   ```

3. **關鍵實驗：關閉終端機測試**
   - 保持 `journalctl -u hello.service -f` 在運行
   - **關掉這個終端機視窗**
   - **重新登入系統**
   - 再執行一次：
     ```bash
     journalctl -u hello.service -n 10
     ```

4. **觀察與思考：**
   - 服務還在運行嗎？
   - log 是否持續在更新？
   - **這一刻，你應該深刻理解：服務真的跟終端機無關！**

---

### Step 6：停止服務（服務 ≠ 殺程序）

1. 停止服務：
   ```bash
   sudo systemctl stop hello.service
   ```

2. **檢查狀態：**
   ```bash
   systemctl status hello.service
   ```

3. **觀察：** 狀態會變成什麼？（應該是 `inactive (dead)`）

4. **思考問題：**
   - systemd 是「請它停止」，不是 `kill` 它。這兩種方式有什麼不同？
   - 如果服務設定了 `Restart=always`，停止後會發生什麼事？

---

### Step 7：完整「消滅」這個服務（收尾很重要）

**按照以下步驟，完整地刪除這個服務：**

1. **取消開機啟動（如果有啟用的話）：**
   ```bash
   sudo systemctl disable hello.service
   ```

2. **刪掉服務檔：**
   ```bash
   sudo rm /etc/systemd/system/hello.service
   ```

3. **刪掉程式本體：**
   ```bash
   sudo rm /usr/local/bin/hello-service.sh
   ```

4. **重新載入 systemd：**
   ```bash
   sudo systemctl daemon-reload
   ```

5. **驗證真的不見了：**
   ```bash
   systemctl status hello.service
   ```

6. **應該會看到：**
   ```
   Unit hello.service could not be found.
   ```

✅ **乾乾淨淨！**

---

## 6️⃣ 觀念問答與對照比較

### 基礎觀念問答

1. 當你按下 `Ctrl + C` 時，系統送出了什麼信號？這個信號的作用是什麼？
2. 當你按下 `Ctrl + Z` 時，系統送出了什麼信號？這個信號和 `Ctrl + C` 有什麼不同？
3. 當你關閉終端機時，系統預設會送出什麼信號？`nohup` 的作用是什麼？
4. 請用你自己的話，簡單描述「前景程序」、「背景工作」和「系統服務」三者最大的區別。

### 對照比較練習

請根據你的實作經驗，完成以下對照表：

| 特性 | `&` (背景工作) | `nohup` | `systemd` |
| :--- | :--- | :--- | :--- |
| 關閉終端機後是否存活？ | | | |
| 程序崩潰後是否自動重啟？ | | | |
| 是否支援開機自動啟動？ | | | |
| 是否由系統統一管理？ | | | |
| 是否可以看到系統日誌？ | | | |
| 適用場景 | | | |

### 進階思考題

1. **為什麼正式環境不能只用 `nohup`？**
   - 如果服務自己掛了，`nohup` 會怎麼處理？
   - 如果系統重開機，`nohup` 啟動的程序會自動恢復嗎？
   - `systemd` 如何解決這些問題？

2. **systemd 服務檔中的 `Restart=always` 有什麼意義？**
   - 如果沒有這一行，服務崩潰後會發生什麼事？
   - 這和 `nohup` 有什麼本質上的不同？

3. **實際應用場景：**
   - 如果你要部署一個 Web 伺服器（例如 FastAPI），你會選擇哪種方式？為什麼？
   - 如果你只是要測試一個腳本，你會選擇哪種方式？為什麼？

---

## 作業提交說明

請將以上每個步驟的：

1. **指令與輸出**：截圖或文字記錄每個指令的執行結果
2. **觀察記錄**：記錄你在每個步驟中觀察到的現象
3. **問題答案**：回答所有「思考問題」和「觀念問答」
4. **對照表**：完成「對照比較練習」的表格
5. **心得反思**：寫下你對「為什麼正式環境一定要用 systemd」的理解

整理成一份完整的文件提交。

---

## 額外挑戰（選做）

如果你已經完成以上所有練習，可以嘗試：

1. **修改服務檔**：將 `hello-service.sh` 改為每 3 秒輸出一次，並重新載入服務
2. **觀察自動重啟**：手動 kill 掉服務的 PID，觀察 systemd 是否自動重啟
3. **設定開機自啟**：使用 `systemctl enable hello.service`，然後重開機驗證服務是否自動啟動
4. **建立自己的服務**：選擇一個你常用的程式（例如 Python 腳本），將它設定為 systemd 服務
