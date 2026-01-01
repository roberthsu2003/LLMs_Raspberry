# 練習：系統監控與軟體管理

**目標：** 透過親手操作，掌握系統監控工具和軟體管理的基本技能，能夠監控系統資源並管理軟體套件。

---

## 1️⃣ ps 程序監控練習

**目標：** 學會使用 `ps` 查看運行中的程序。

### 練習 1：基本程序查看

1. **查看當前終端機的程序：**
   ```bash
   ps
   ```

2. **查看所有程序：**
   ```bash
   ps aux
   ```

3. **觀察與記錄：**
   - 輸出了哪些欄位？
   - 記錄下幾個程序的 PID、CPU 使用率、記憶體使用率

4. **查看特定程序：**
   ```bash
   ps aux | grep python
   ```

5. **查看自己的程序：**
   ```bash
   ps aux | grep $USER
   ```

### 練習 2：程序資訊分析

1. **啟動一個背景程序：**
   ```bash
   sleep 300 &
   ```

2. **記錄這個程序的 PID：**
   ```bash
   ps aux | grep sleep
   ```

3. **查看這個程序的詳細資訊：**
   ```bash
   ps -p <PID>
   # 將 <PID> 替換為實際的 PID
   ```

4. **按 CPU 使用率排序：**
   ```bash
   ps aux --sort=-%cpu | head -10
   ```

5. **按記憶體使用率排序：**
   ```bash
   ps aux --sort=-%mem | head -10
   ```

6. **思考問題：**
   - 哪些程序佔用最多的 CPU？
   - 哪些程序佔用最多的記憶體？

---

## 2️⃣ top 即時監控練習

**目標：** 學會使用 `top` 即時監控系統。

### 練習 3：使用 top 監控系統

1. **啟動 top：**
   ```bash
   top
   ```

2. **觀察 top 介面：**
   - 記錄系統負載（load average）
   - 記錄 CPU 使用率
   - 記錄記憶體使用情況

3. **操作練習：**
   - 按 `P`：按 CPU 使用率排序
   - 按 `M`：按記憶體使用率排序
   - 按 `1`：顯示所有 CPU 核心
   - 按 `h`：查看幫助

4. **終止一個程序（練習）：**
   - 按 `k`
   - 輸入要終止的 PID（可以選擇一個不重要的程序）
   - 輸入信號（直接按 Enter 使用預設）

5. **離開 top：**
   - 按 `q`

### 練習 4：建立 CPU 負載（可選）

1. **建立一個會消耗 CPU 的腳本：**
   ```bash
   cat > cpu-test.sh << 'EOF'
   #!/bin/bash
   while true; do
     echo "test" > /dev/null
   done
   EOF
   chmod +x cpu-test.sh
   ```

2. **在背景執行：**
   ```bash
   ./cpu-test.sh &
   ```

3. **使用 top 觀察：**
   ```bash
   top
   ```
   - 觀察 CPU 使用率的變化
   - 找出剛才啟動的程序

4. **停止測試程序：**
   ```bash
   pkill -f cpu-test.sh
   ```

---

## 3️⃣ df 磁碟空間練習

**目標：** 學會使用 `df` 查看磁碟空間。

### 練習 5：查看磁碟空間

1. **查看所有檔案系統：**
   ```bash
   df
   ```

2. **以人類可讀格式查看：**
   ```bash
   df -h
   ```

3. **觀察與記錄：**
   - 記錄各個檔案系統的總容量、已使用、可用空間
   - 哪個分割區使用率最高？

4. **查看根目錄的空間：**
   ```bash
   df -h /
   ```

5. **查看家目錄的空間：**
   ```bash
   df -h ~
   ```

6. **查看 inode 使用情況：**
   ```bash
   df -i
   ```

### 練習 6：分析磁碟使用

1. **找出使用率超過 80% 的分割區：**
   ```bash
   df -h | awk '$5+0 > 80 {print}'
   ```

2. **思考問題：**
   - 如果某個分割區使用率很高，應該如何處理？
   - 如何找出佔用空間的檔案？

---

## 4️⃣ du 目錄大小練習

**目標：** 學會使用 `du` 查看目錄大小。

### 練習 7：查看目錄大小

1. **查看當前目錄的大小：**
   ```bash
   du
   ```

2. **以人類可讀格式查看：**
   ```bash
   du -h
   ```

3. **查看家目錄的總大小：**
   ```bash
   du -sh ~
   ```

4. **查看家目錄下各子目錄的大小：**
   ```bash
   du -h --max-depth=1 ~
   ```

5. **按大小排序：**
   ```bash
   du -h --max-depth=1 ~ | sort -h
   ```

6. **找出最大的 5 個目錄：**
   ```bash
   du -h --max-depth=1 ~ | sort -h | tail -5
   ```

### 練習 8：找出大檔案

1. **找出當前目錄下大於 1MB 的檔案：**
   ```bash
   find . -type f -size +1M -exec du -h {} \;
   ```

2. **找出家目錄下大於 10MB 的檔案：**
   ```bash
   find ~ -type f -size +10M -exec du -h {} \; 2>/dev/null
   ```

3. **找出最大的 10 個檔案：**
   ```bash
   find ~ -type f -exec du -h {} \; 2>/dev/null | sort -h | tail -10
   ```

---

## 5️⃣ apt 軟體管理練習

**目標：** 學會使用 `apt` 管理軟體套件。

### 練習 9：更新套件列表

1. **更新套件列表：**
   ```bash
   sudo apt update
   ```

2. **觀察輸出：**
   - 記錄更新了多少個套件
   - 是否有錯誤訊息？

### 練習 10：搜尋和安裝軟體

1. **搜尋一個軟體（例如：htop）：**
   ```bash
   apt search htop
   ```

2. **查看軟體詳細資訊：**
   ```bash
   apt show htop
   ```

3. **安裝軟體（如果還沒安裝）：**
   ```bash
   sudo apt install htop
   ```

4. **驗證安裝：**
   ```bash
   which htop
   htop --version
   ```

5. **思考問題：**
   - 安裝軟體需要什麼權限？為什麼？

### 練習 11：查看已安裝的套件

1. **列出已安裝的套件：**
   ```bash
   apt list --installed | head -20
   ```

2. **統計已安裝的套件數量：**
   ```bash
   apt list --installed | wc -l
   ```

3. **搜尋已安裝的 Python 相關套件：**
   ```bash
   apt list --installed | grep python
   ```

### 練習 12：更新系統（謹慎操作）

1. **查看可更新的套件：**
   ```bash
   apt list --upgradable
   ```

2. **升級所有套件（可選，需要時間）：**
   ```bash
   sudo apt upgrade
   ```
   - **注意：** 這可能需要一些時間，請耐心等待
   - 如果系統提示，輸入 `y` 確認

3. **思考問題：**
   - 為什麼要定期更新系統？
   - 更新前應該做什麼準備？

### 練習 13：移除軟體（可選）

1. **移除剛才安裝的軟體（如果不需要）：**
   ```bash
   sudo apt remove htop
   ```

2. **驗證是否已移除：**
   ```bash
   which htop
   ```

3. **完全移除（包含設定檔）：**
   ```bash
   sudo apt purge htop
   ```

4. **思考問題：**
   - `remove` 和 `purge` 有什麼不同？
   - 什麼時候應該使用 `purge`？

### 練習 14：清理系統

1. **移除不再需要的套件：**
   ```bash
   sudo apt autoremove
   ```

2. **清理下載的套件快取：**
   ```bash
   sudo apt autoclean
   ```

3. **查看清理前後的磁碟空間：**
   ```bash
   df -h /
   ```

---

## 6️⃣ 綜合實務練習

### 練習 15：系統健康檢查

**任務：** 建立一個系統健康檢查腳本。

1. **建立檢查腳本：**
   ```bash
   cat > ~/system-check.sh << 'EOF'
   #!/bin/bash
   echo "=== System Health Check ==="
   echo "Date: $(date)"
   echo ""
   echo "=== Disk Usage ==="
   df -h
   echo ""
   echo "=== Memory Usage ==="
   free -h
   echo ""
   echo "=== System Load ==="
   uptime
   echo ""
   echo "=== Top 5 CPU Processes ==="
   ps aux --sort=-%cpu | head -6
   echo ""
   echo "=== Top 5 Memory Processes ==="
   ps aux --sort=-%mem | head -6
   EOF
   chmod +x ~/system-check.sh
   ```

2. **執行檢查：**
   ```bash
   ~/system-check.sh
   ```

3. **分析結果：**
   - 磁碟使用率是否正常？
   - 記憶體使用率是否正常？
   - 系統負載是否正常？
   - 哪些程序佔用最多資源？

### 練習 16：找出佔用空間的檔案

**任務：** 找出系統中佔用空間的檔案和目錄。

1. **查看各目錄大小：**
   ```bash
   du -h --max-depth=1 /home 2>/dev/null | sort -h
   ```

2. **找出大檔案（大於 50MB）：**
   ```bash
   find ~ -type f -size +50M -exec ls -lh {} \; 2>/dev/null
   ```

3. **找出最大的 10 個檔案：**
   ```bash
   find ~ -type f -exec du -h {} \; 2>/dev/null | sort -h | tail -10
   ```

4. **記錄結果：**
   - 哪些檔案或目錄佔用最多空間？
   - 這些檔案是否可以清理？

### 練習 17：監控特定程序

**任務：** 監控一個特定程序的資源使用。

1. **啟動一個程序（例如：Python）：**
   ```bash
   python3 -c "import time; time.sleep(60)" &
   ```

2. **記錄 PID：**
   ```bash
   ps aux | grep python3
   ```

3. **持續監控這個程序：**
   ```bash
   watch -n 2 "ps aux | grep python3 | grep -v grep"
   ```
   - 按 `Ctrl + C` 停止監控

4. **使用 top 監控：**
   ```bash
   top -p <PID>
   # 將 <PID> 替換為實際的 PID
   ```

---

## 7️⃣ 進階挑戰（選做）

### 挑戰 1：建立自動監控腳本

建立一個腳本，每 5 分鐘檢查一次系統資源，如果使用率過高就發出警告。

### 挑戰 2：清理腳本

建立一個腳本，自動：
- 清理 apt 快取
- 找出並列出大檔案
- 清理臨時檔案

### 挑戰 3：系統報告

建立一個腳本，生成系統健康報告，包含：
- 系統資訊
- 資源使用情況
- 已安裝的套件數量
- 磁碟使用情況

---

## 8️⃣ 觀念問答

1. **`ps` 和 `top` 有什麼不同？**
   - 什麼時候應該用 `ps`，什麼時候應該用 `top`？

2. **為什麼要定期更新系統？**
   - 更新系統有什麼好處和風險？

3. **如何判斷系統是否需要清理？**
   - 哪些指標可以幫助判斷？

4. **`df` 和 `du` 有什麼不同？**
   - 它們分別用於什麼場景？

5. **如何安全地移除軟體？**
   - `remove` 和 `purge` 應該如何選擇？

6. **請解釋以下指令的作用：**
   ```bash
   ps aux --sort=-%cpu | head -10
   ```

---

## 作業提交說明

請將以上每個步驟的：

1. **指令與輸出**：截圖或文字記錄每個指令的執行結果
2. **觀察記錄**：記錄你在每個步驟中觀察到的現象
3. **問題答案**：回答所有「思考問題」和「觀念問答」
4. **系統分析報告**：
   - 你的系統目前的資源使用情況
   - 磁碟空間使用情況
   - 已安裝的套件數量
5. **心得反思**：
   - 寫下你對系統監控的理解
   - 說明如何判斷系統是否需要維護
   - 記錄你覺得最實用的監控技巧

整理成一份完整的文件提交。

