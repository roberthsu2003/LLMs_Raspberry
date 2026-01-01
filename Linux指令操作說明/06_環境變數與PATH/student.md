# 練習：環境變數與 PATH

**目標：** 透過親手操作，理解環境變數的作用機制，以及在不同階段（終端機、開機、服務）如何正確設定環境變數。

---

## 1️⃣ 認識環境變數

**目標：** 學會查看和使用環境變數。

### 練習 1：查看環境變數

1. 執行 `env` 指令，查看所有環境變數。
   - **觀察：** 記錄下你看到的環境變數名稱和值。
   - **問題：** 你看到了哪些常見的環境變數？（例如：`HOME`, `USER`, `PATH`）

2. 使用 `echo` 查看特定環境變數：
   ```bash
   echo $HOME
   echo $USER
   echo $PATH
   echo $SHELL
   ```

3. **記錄與思考：**
   - `HOME` 的值是什麼？它代表什麼意思？
   - `PATH` 的值是什麼？它包含哪些路徑？
   - `PATH` 中的路徑是用什麼符號分隔的？

---

## 2️⃣ 理解 PATH 的作用

**目標：** 理解系統如何透過 PATH 找到指令。

### 練習 2：追蹤指令的位置

1. 使用 `which` 指令找出常用指令的位置：
   ```bash
   which ls
   which python3
   which nano
   ```

2. **觀察與記錄：**
   - `ls` 指令位於哪個路徑？
   - 這個路徑是否在你的 `PATH` 中？

3. 使用 `whereis` 查看指令的完整資訊：
   ```bash
   whereis ls
   whereis python3
   ```

4. **思考問題：**
   - `which` 和 `whereis` 的輸出有什麼不同？
   - 為什麼系統能找到 `ls` 指令？

---

### 練習 3：PATH 的搜尋順序

1. 查看你的 PATH：
   ```bash
   echo $PATH
   ```

2. **記錄：** 將 PATH 中的路徑依序寫下來。

3. **實驗：** 建立一個測試腳本，觀察系統的搜尋順序：
   ```bash
   # 在 /tmp 建立一個名為 ls 的腳本
   cat > /tmp/ls << 'EOF'
   #!/bin/bash
   echo "This is a fake ls command!"
   EOF
   chmod +x /tmp/ls
   ```

4. 測試：
   ```bash
   /tmp/ls
   ls
   ```

5. **思考問題：**
   - 為什麼執行 `ls` 時，系統沒有執行 `/tmp/ls`？
   - 如果 `/tmp` 在 PATH 的最前面，會發生什麼事？

---

## 3️⃣ 臨時設定環境變數

**目標：** 學會臨時設定環境變數，理解其作用範圍。

### 練習 4：設定臨時環境變數

1. 設定一個臨時環境變數：
   ```bash
   export MY_NAME="Student"
   export MY_NUMBER=123
   ```

2. 查看設定的環境變數：
   ```bash
   echo $MY_NAME
   echo $MY_NUMBER
   ```

3. **實驗：** 在腳本中使用環境變數：
   ```bash
   cat > /tmp/test-env.sh << 'EOF'
   #!/bin/bash
   echo "My name is: $MY_NAME"
   echo "My number is: $MY_NUMBER"
   EOF
   chmod +x /tmp/test-env.sh
   /tmp/test-env.sh
   ```

4. **觀察：** 腳本是否能讀取到環境變數？

5. **關鍵實驗：**
   - 開啟**另一個終端機視窗**
   - 在新視窗中執行 `echo $MY_NAME`
   - **問題：** 新視窗能看到這個環境變數嗎？為什麼？

---

## 4️⃣ 永久設定環境變數（使用者層級）

**目標：** 學會在 `~/.bashrc` 中設定永久環境變數。

### 練習 5：建立自訂工具並加入 PATH

**完整流程：從建立工具到讓系統能找到它**

#### Step 1：建立自訂工具

1. 建立工具目錄：
   ```bash
   mkdir -p ~/my-tools
   ```

2. 建立一個簡單的工具腳本：
   ```bash
   nano ~/my-tools/hello-world
   ```

3. **輸入以下內容：**
   ```bash
   #!/bin/bash
   echo "=================================="
   echo "Hello from my custom tool!"
   echo "Current time: $(date)"
   echo "Current user: $USER"
   echo "Current directory: $PWD"
   echo "=================================="
   ```

4. 給執行權限：
   ```bash
   chmod +x ~/my-tools/hello-world
   ```

5. **測試（使用完整路徑）：**
   ```bash
   ~/my-tools/hello-world
   ```
   - **確認：** 應該可以正常執行

#### Step 2：嘗試直接執行（應該會失敗）

1. 嘗試直接執行：
   ```bash
   hello-world
   ```

2. **觀察：** 會發生什麼錯誤？
   - **錯誤訊息：** `command not found`
   - **原因：** `~/my-tools` 不在 PATH 中

#### Step 3：將路徑加入 PATH

1. 編輯 `~/.bashrc`：
   ```bash
   nano ~/.bashrc
   ```

2. **在檔案末尾加入：**
   ```bash
   # 自訂工具路徑
   export PATH=$PATH:$HOME/my-tools
   ```

3. **重新載入設定檔：**
   ```bash
   source ~/.bashrc
   ```

4. **驗證 PATH 是否已更新：**
   ```bash
   echo $PATH
   ```
   - **確認：** 應該能看到 `~/my-tools` 在 PATH 中

#### Step 4：測試直接執行

1. 現在嘗試直接執行：
   ```bash
   hello-world
   ```

2. **觀察：** 應該可以正常執行了！

3. **驗證：**
   ```bash
   which hello-world
   ```
   - **應該顯示：** `/home/pi/my-tools/hello-world`（或你的家目錄路徑）

#### Step 5：測試新終端機

1. **開啟一個新的終端機視窗**
2. 在新視窗中執行：
   ```bash
   hello-world
   ```

3. **觀察與思考：**
   - 新終端機也能執行 `hello-world` 嗎？
   - 為什麼？`~/.bashrc` 什麼時候會被載入？

---

### 練習 6：設定自訂環境變數

1. 編輯 `~/.bashrc`：
   ```bash
   nano ~/.bashrc
   ```

2. **加入以下環境變數：**
   ```bash
   # 自訂環境變數
   export MY_PROJECT_DIR="$HOME/projects"
   export MY_EDITOR="nano"
   export MY_FAVORITE_COLOR="blue"
   ```

3. 重新載入：
   ```bash
   source ~/.bashrc
   ```

4. **測試：**
   ```bash
   echo $MY_PROJECT_DIR
   echo $MY_EDITOR
   echo $MY_FAVORITE_COLOR
   ```

5. **建立測試腳本：**
   ```bash
   cat > /tmp/test-my-env.sh << 'EOF'
   #!/bin/bash
   echo "Project directory: $MY_PROJECT_DIR"
   echo "Editor: $MY_EDITOR"
   echo "Favorite color: $MY_FAVORITE_COLOR"
   EOF
   chmod +x /tmp/test-my-env.sh
   /tmp/test-my-env.sh
   ```

6. **觀察：** 腳本是否能讀取到這些環境變數？

---

## 5️⃣ 系統層級的環境變數（進階）

**目標：** 理解系統層級環境變數的設定（需要 root 權限）。

### 練習 7：查看系統層級的環境變數

1. 查看系統環境變數檔案：
   ```bash
   cat /etc/environment
   ```

2. **觀察：** 記錄下你看到的內容。

3. **思考問題：**
   - 這個檔案和 `~/.bashrc` 有什麼不同？
   - 誰可以修改這個檔案？

---

## 6️⃣ 服務層級的環境變數（systemd）

**目標：** 理解 systemd 服務如何設定環境變數，以及為什麼服務看不到終端機的環境變數。

### 練習 8：驗證服務不會繼承終端機的環境變數

#### Step 1：在終端機設定環境變數

1. 在終端機設定一個環境變數：
   ```bash
   export TEST_VAR="This is from terminal"
   echo $TEST_VAR
   ```

2. **確認：** 終端機可以讀取到這個變數

#### Step 2：建立測試服務

1. 建立服務腳本：
   ```bash
   sudo nano /usr/local/bin/test-env-service.sh
   ```

2. **輸入以下內容：**
   ```bash
   #!/bin/bash
   
   echo "=== Environment Variables in Service ==="
   echo "TEST_VAR = $TEST_VAR"
   echo "HOME = $HOME"
   echo "USER = $USER"
   echo "PATH = $PATH"
   echo "========================================"
   
   while true
   do
     echo "Service is running... TEST_VAR = $TEST_VAR"
     sleep 10
   done
   ```

3. 給執行權限：
   ```bash
   sudo chmod +x /usr/local/bin/test-env-service.sh
   ```

#### Step 3：建立服務檔（不設定環境變數）

1. 建立服務檔：
   ```bash
   sudo nano /etc/systemd/system/test-env.service
   ```

2. **輸入以下內容：**
   ```ini
   [Unit]
   Description=Test Environment Variables Service

   [Service]
   ExecStart=/usr/local/bin/test-env-service.sh
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. 啟動服務：
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start test-env.service
   ```

4. **查看服務日誌：**
   ```bash
   journalctl -u test-env.service -n 20
   ```

5. **觀察與思考：**
   - `TEST_VAR` 的值是什麼？
   - 服務能看到終端機設定的 `TEST_VAR` 嗎？
   - **為什麼？**

#### Step 4：在服務檔中設定環境變數

1. 修改服務檔：
   ```bash
   sudo nano /etc/systemd/system/test-env.service
   ```

2. **修改為：**
   ```ini
   [Unit]
   Description=Test Environment Variables Service

   [Service]
   Environment="TEST_VAR=This is from service file"
   Environment="MY_SERVICE_NAME=TestService"
   ExecStart=/usr/local/bin/test-env-service.sh
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. 重新載入並重啟：
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart test-env.service
   ```

4. **查看服務日誌：**
   ```bash
   journalctl -u test-env.service -n 20 -f
   ```

5. **觀察：**
   - 現在 `TEST_VAR` 的值是什麼？
   - 服務是否能讀取到環境變數了？

6. **停止服務：**
   ```bash
   sudo systemctl stop test-env.service
   ```

---

### 練習 9：使用環境變數檔案管理服務環境變數

**目標：** 學會使用 `EnvironmentFile` 來管理服務的環境變數。

#### Step 1：建立環境變數檔案

1. 建立目錄和檔案：
   ```bash
   sudo mkdir -p /etc/my-service
   sudo nano /etc/my-service/env.conf
   ```

2. **輸入以下內容：**
   ```bash
   # 資料庫設定
   DATABASE_URL=postgresql://localhost/mydb
   DATABASE_USER=admin
   DATABASE_PASSWORD=secret123

   # 服務設定
   SERVICE_NAME=MyDemoService
   SERVICE_PORT=8080
   DEBUG_MODE=true
   ```

3. **設定檔案權限（保護敏感資訊）：**
   ```bash
   sudo chmod 600 /etc/my-service/env.conf
   ```

#### Step 2：建立服務腳本

1. 建立服務腳本：
   ```bash
   sudo nano /usr/local/bin/env-demo-service.sh
   ```

2. **輸入以下內容：**
   ```bash
   #!/bin/bash
   
   echo "=== Service Environment Variables ==="
   echo "SERVICE_NAME: $SERVICE_NAME"
   echo "SERVICE_PORT: $SERVICE_PORT"
   echo "DATABASE_URL: $DATABASE_URL"
   echo "DATABASE_USER: $DATABASE_USER"
   echo "DEBUG_MODE: $DEBUG_MODE"
   echo "======================================"
   
   while true
   do
     echo "[$(date)] Service $SERVICE_NAME is running on port $SERVICE_PORT"
     echo "  Database: $DATABASE_URL"
     echo "  Debug mode: $DEBUG_MODE"
     sleep 15
   done
   ```

3. 給執行權限：
   ```bash
   sudo chmod +x /usr/local/bin/env-demo-service.sh
   ```

#### Step 3：建立服務檔

1. 建立服務檔：
   ```bash
   sudo nano /etc/systemd/system/env-demo.service
   ```

2. **輸入以下內容：**
   ```ini
   [Unit]
   Description=Environment Variables Demo Service

   [Service]
   EnvironmentFile=/etc/my-service/env.conf
   ExecStart=/usr/local/bin/env-demo-service.sh
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

#### Step 4：啟動並測試

1. 啟動服務：
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start env-demo.service
   sudo systemctl status env-demo.service
   ```

2. **查看服務日誌：**
   ```bash
   journalctl -u env-demo.service -f
   ```

3. **觀察：**
   - 服務是否能正確讀取所有環境變數？
   - 每個環境變數的值是什麼？

#### Step 5：修改環境變數（不需要改服務檔）

1. 修改環境變數檔案：
   ```bash
   sudo nano /etc/my-service/env.conf
   ```

2. **修改 `SERVICE_PORT` 為 `9090`**

3. 重啟服務：
   ```bash
   sudo systemctl restart env-demo.service
   ```

4. **查看日誌：**
   ```bash
   journalctl -u env-demo.service -n 10
   ```

5. **觀察：** `SERVICE_PORT` 是否已更新？

6. **清理：**
   ```bash
   sudo systemctl stop env-demo.service
   sudo systemctl disable env-demo.service
   ```

---

## 7️⃣ 綜合練習：完整的環境變數設定流程

**目標：** 整合所有學習內容，完成一個完整的實務案例。

### 練習 10：建立一個完整的工具和服務

**情境：** 建立一個自訂的監控工具，並讓它在終端機和服務中都能正確使用環境變數。

#### 任務 1：建立工具腳本

1. 建立工具目錄和腳本：
   ```bash
   mkdir -p ~/my-tools
   nano ~/my-tools/system-monitor
   ```

2. **輸入以下內容：**
   ```bash
   #!/bin/bash
   
   # 使用環境變數設定監控間隔
   INTERVAL=${MONITOR_INTERVAL:-5}  # 預設 5 秒
   
   echo "=== System Monitor ==="
   echo "Monitor interval: ${INTERVAL} seconds"
   echo "User: $USER"
   echo "Home: $HOME"
   echo "======================"
   
   while true
   do
     echo "[$(date)] CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}') | Memory: $(free -h | grep Mem | awk '{print $3}')"
     sleep $INTERVAL
   done
   ```

3. 給執行權限：
   ```bash
   chmod +x ~/my-tools/system-monitor
   ```

#### 任務 2：在終端機中使用

1. 將工具加入 PATH（如果還沒加入）：
   ```bash
   echo 'export PATH=$PATH:$HOME/my-tools' >> ~/.bashrc
   source ~/.bashrc
   ```

2. 設定環境變數並執行：
   ```bash
   export MONITOR_INTERVAL=3
   system-monitor
   ```

3. **觀察：** 監控間隔是否為 3 秒？

4. 按 `Ctrl + C` 停止

#### 任務 3：建立 systemd 服務版本

1. 建立服務腳本：
   ```bash
   sudo nano /usr/local/bin/system-monitor-service.sh
   ```

2. **輸入以下內容：**
   ```bash
   #!/bin/bash
   
   # 從環境變數讀取設定
   INTERVAL=${MONITOR_INTERVAL:-10}  # 預設 10 秒
   LOG_FILE=${MONITOR_LOG_FILE:-/var/log/system-monitor.log}
   
   echo "=== System Monitor Service ==="
   echo "Interval: ${INTERVAL} seconds"
   echo "Log file: $LOG_FILE"
   echo "=============================="
   
   while true
   do
     TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
     CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}')
     MEM=$(free -h | grep Mem | awk '{print $3}')
     echo "[$TIMESTAMP] CPU: $CPU | Memory: $MEM" | tee -a $LOG_FILE
     sleep $INTERVAL
   done
   ```

3. 給執行權限：
   ```bash
   sudo chmod +x /usr/local/bin/system-monitor-service.sh
   ```

4. 建立環境變數檔案：
   ```bash
   sudo mkdir -p /etc/system-monitor
   sudo nano /etc/system-monitor/env.conf
   ```

5. **輸入以下內容：**
   ```bash
   MONITOR_INTERVAL=15
   MONITOR_LOG_FILE=/var/log/system-monitor.log
   ```

6. 建立服務檔：
   ```bash
   sudo nano /etc/systemd/system/system-monitor.service
   ```

7. **輸入以下內容：**
   ```ini
   [Unit]
   Description=System Monitor Service

   [Service]
   EnvironmentFile=/etc/system-monitor/env.conf
   ExecStart=/usr/local/bin/system-monitor-service.sh
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

8. 啟動服務：
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start system-monitor.service
   sudo systemctl status system-monitor.service
   ```

9. **查看日誌：**
   ```bash
   journalctl -u system-monitor.service -f
   ```

10. **查看日誌檔案：**
    ```bash
    sudo tail -f /var/log/system-monitor.log
    ```

11. **觀察與驗證：**
    - 服務是否正確讀取了 `MONITOR_INTERVAL`？
    - 監控間隔是否為 15 秒？
    - 日誌是否正確寫入檔案？

---

## 8️⃣ 觀念問答與對照比較

### 基礎觀念問答

1. **環境變數是什麼？** 請用你自己的話解釋。

2. **PATH 的作用是什麼？** 當你輸入 `ls` 時，系統是如何找到這個指令的？

3. **臨時設定和永久設定環境變數有什麼不同？**
   - 什麼時候用 `export`？
   - 什麼時候需要修改 `~/.bashrc`？

4. **為什麼服務看不到終端機設定的環境變數？**

5. **`~/.bashrc` 和 `/etc/environment` 有什麼不同？**

### 對照比較練習

請根據你的實作經驗，完成以下對照表：

| 特性 | 終端機階段 (`~/.bashrc`) | 系統層級 (`/etc/environment`) | 服務階段 (systemd) |
| :--- | :--- | :--- | :--- |
| 設定檔案位置 | | | |
| 影響範圍 | | | |
| 何時載入 | | | |
| 是否需要 root 權限 | | | |
| 是否影響其他使用者 | | | |
| 是否影響系統服務 | | | |
| 適用場景 | | | |

### 進階思考題

1. **為什麼 systemd 服務不會繼承終端機的環境變數？**
   - 這樣設計有什麼好處？
   - 有什麼潛在問題？

2. **環境變數的安全性考量：**
   - 如果環境變數包含密碼，應該如何保護？
   - 檔案權限應該設定為什麼？

3. **實際應用場景：**
   - 如果你要部署一個需要資料庫連線的 Python 應用，應該在哪裡設定資料庫 URL？
   - 如果你要讓所有使用者都能使用某個工具，應該在哪裡設定 PATH？

---

## 作業提交說明

請將以上每個步驟的：

1. **指令與輸出**：截圖或文字記錄每個指令的執行結果
2. **觀察記錄**：記錄你在每個步驟中觀察到的現象
3. **問題答案**：回答所有「思考問題」和「觀念問答」
4. **對照表**：完成「對照比較練習」的表格
5. **心得反思**：
   - 寫下你對「為什麼不同階段需要不同的環境變數設定方式」的理解
   - 說明在什麼情況下應該使用哪種設定方式

整理成一份完整的文件提交。

---

## 額外挑戰（選做）

如果你已經完成以上所有練習，可以嘗試：

1. **建立多個自訂工具**：建立 3-5 個不同的工具腳本，都放在 `~/my-tools`，並測試它們是否都能正常執行

2. **建立複雜的服務環境變數**：
   - 建立一個需要多個環境變數的服務（例如：資料庫連線、API 金鑰、設定檔路徑）
   - 使用 `EnvironmentFile` 管理這些變數
   - 測試修改環境變數後，服務是否能正確讀取

3. **環境變數的條件判斷**：
   - 在腳本中使用環境變數進行條件判斷
   - 例如：如果 `DEBUG_MODE=true`，輸出詳細資訊；否則只輸出基本資訊

4. **PATH 的優先順序實驗**：
   - 建立多個同名但不同功能的腳本
   - 將它們放在 PATH 的不同位置
   - 觀察系統會執行哪一個

