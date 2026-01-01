# 練習：文字處理與搜尋工具

**目標：** 透過親手操作，掌握 `grep`、`find`、管道等工具的使用方法，提升日常工作效率。

---

## 1️⃣ grep 基礎練習

**目標：** 學會使用 `grep` 在檔案中搜尋文字。

### 練習 1：建立測試檔案並搜尋

1. 建立測試檔案：
   ```bash
   cat > test.txt << 'EOF'
   Linux is a great operating system.
   I love Linux programming.
   Linux commands are powerful.
   This is not about Linux.
   EOF
   ```

2. **基本搜尋：**
   ```bash
   grep "Linux" test.txt
   ```

3. **觀察與記錄：**
   - 輸出了哪些行？
   - 總共有幾行包含 "Linux"？

4. **顯示行號：**
   ```bash
   grep -n "Linux" test.txt
   ```

5. **忽略大小寫：**
   ```bash
   grep -i "linux" test.txt
   ```

6. **反向搜尋（顯示不包含的行）：**
   ```bash
   grep -v "Linux" test.txt
   ```

### 練習 2：在日誌檔中搜尋

1. 建立模擬日誌檔：
   ```bash
   cat > app.log << 'EOF'
   2025-01-01 10:00:00 INFO: Application started
   2025-01-01 10:05:00 ERROR: Database connection failed
   2025-01-01 10:10:00 INFO: User logged in
   2025-01-01 10:15:00 ERROR: File not found
   2025-01-01 10:20:00 WARNING: Memory usage high
   2025-01-01 10:25:00 INFO: Request processed
   2025-01-01 10:30:00 ERROR: Timeout occurred
   EOF
   ```

2. **搜尋所有錯誤：**
   ```bash
   grep "ERROR" app.log
   ```

3. **搜尋錯誤並顯示行號：**
   ```bash
   grep -n "ERROR" app.log
   ```

4. **統計錯誤數量：**
   ```bash
   grep "ERROR" app.log | wc -l
   ```

5. **搜尋錯誤或警告：**
   ```bash
   grep -E "ERROR|WARNING" app.log
   ```

6. **思考問題：**
   - 如何只顯示包含錯誤的日期和時間？
   - 如何統計不同類型的日誌數量？

---

## 2️⃣ find 基礎練習

**目標：** 學會使用 `find` 搜尋檔案和目錄。

### 練習 3：根據檔名搜尋

1. **建立測試環境：**
   ```bash
   mkdir -p ~/test-find/{docs,scripts,logs}
   touch ~/test-find/docs/file1.txt
   touch ~/test-find/docs/file2.txt
   touch ~/test-find/scripts/script.sh
   touch ~/test-find/logs/app.log
   ```

2. **搜尋所有 .txt 檔案：**
   ```bash
   find ~/test-find -name "*.txt"
   ```

3. **搜尋所有 .sh 檔案：**
   ```bash
   find ~/test-find -name "*.sh"
   ```

4. **搜尋所有 .log 檔案：**
   ```bash
   find ~/test-find -name "*.log"
   ```

5. **觀察與記錄：**
   - 每個指令找到了哪些檔案？
   - 路徑是什麼？

### 練習 4：根據類型搜尋

1. **只搜尋檔案：**
   ```bash
   find ~/test-find -type f
   ```

2. **只搜尋目錄：**
   ```bash
   find ~/test-find -type d
   ```

3. **觀察與思考：**
   - `-type f` 和 `-type d` 的輸出有什麼不同？

### 練習 5：根據大小搜尋

1. **建立不同大小的測試檔案：**
   ```bash
   # 建立一個大檔案（約 1MB）
   dd if=/dev/zero of=~/test-find/large.txt bs=1M count=1 2>/dev/null
   
   # 建立一個小檔案
   echo "small" > ~/test-find/small.txt
   ```

2. **搜尋大於 100KB 的檔案：**
   ```bash
   find ~/test-find -size +100k
   ```

3. **搜尋小於 1KB 的檔案：**
   ```bash
   find ~/test-find -size -1k
   ```

4. **觀察與記錄：**
   - 哪些檔案符合條件？

---

## 3️⃣ 管道 (|) 練習

**目標：** 學會使用管道組合多個指令。

### 練習 6：組合 grep 和 find

1. **在專案中搜尋特定內容：**
   ```bash
   # 先建立測試環境
   mkdir -p ~/test-pipe
   echo "import os" > ~/test-pipe/file1.py
   echo "import sys" > ~/test-pipe/file2.py
   echo "import os" > ~/test-pipe/file3.py
   ```

2. **找出所有 .py 檔案，並搜尋 "import os"：**
   ```bash
   find ~/test-pipe -name "*.py" -exec grep -H "import os" {} \;
   ```

3. **只顯示檔案名：**
   ```bash
   find ~/test-pipe -name "*.py" -exec grep -l "import os" {} \;
   ```

### 練習 7：統計和過濾

1. **統計當前目錄的檔案數量：**
   ```bash
   ls -1 | wc -l
   ```

2. **統計包含 "error" 的行數：**
   ```bash
   grep -r "error" ~/test-find 2>/dev/null | wc -l
   ```

3. **列出所有程序，過濾出包含 "python" 的：**
   ```bash
   ps aux | grep python
   ```

4. **顯示前 5 個結果：**
   ```bash
   ps aux | grep python | head -5
   ```

---

## 4️⃣ head 與 tail 練習

**目標：** 學會查看檔案的頭尾。

### 練習 8：查看檔案頭尾

1. **建立一個較長的測試檔案：**
   ```bash
   seq 1 100 > numbers.txt
   ```

2. **查看前 10 行：**
   ```bash
   head numbers.txt
   ```

3. **查看前 20 行：**
   ```bash
   head -n 20 numbers.txt
   ```

4. **查看最後 10 行：**
   ```bash
   tail numbers.txt
   ```

5. **查看最後 20 行：**
   ```bash
   tail -n 20 numbers.txt
   ```

### 練習 9：即時監看日誌（進階）

1. **建立一個會持續寫入的日誌檔：**
   ```bash
   # 在一個終端機執行（讓它持續運行）
   while true; do echo "$(date): Log entry" >> ~/test.log; sleep 2; done
   ```

2. **在另一個終端機監看：**
   ```bash
   tail -f ~/test.log
   ```

3. **觀察：** 應該會看到日誌即時更新

4. **按 `Ctrl + C` 停止監看**

---

## 5️⃣ wc 統計練習

**目標：** 學會使用 `wc` 統計檔案資訊。

### 練習 10：統計檔案資訊

1. **建立測試檔案：**
   ```bash
   cat > test-wc.txt << 'EOF'
   This is line one.
   This is line two.
   This is line three.
   EOF
   ```

2. **統計完整資訊：**
   ```bash
   wc test-wc.txt
   ```

3. **只統計行數：**
   ```bash
   wc -l test-wc.txt
   ```

4. **只統計字數：**
   ```bash
   wc -w test-wc.txt
   ```

5. **只統計字元數：**
   ```bash
   wc -c test-wc.txt
   ```

6. **觀察與記錄：**
   - 行數、字數、字元數各是多少？

---

## 6️⃣ 綜合實務練習

### 練習 11：分析日誌檔

**任務：** 分析應用程式日誌，找出問題。

1. **建立複雜的日誌檔：**
   ```bash
   cat > complex.log << 'EOF'
   2025-01-01 10:00:00 INFO: Application started
   2025-01-01 10:05:00 ERROR: Database connection failed
   2025-01-01 10:10:00 INFO: User logged in
   2025-01-01 10:15:00 ERROR: File not found
   2025-01-01 10:20:00 WARNING: Memory usage high
   2025-01-01 10:25:00 INFO: Request processed
   2025-01-01 10:30:00 ERROR: Timeout occurred
   2025-01-01 10:35:00 INFO: Cache cleared
   2025-01-01 10:40:00 WARNING: Disk space low
   EOF
   ```

2. **完成以下任務：**
   - 統計總行數
   - 找出所有錯誤（ERROR）
   - 統計錯誤數量
   - 找出所有警告（WARNING）
   - 統計警告數量
   - 查看最後 5 行
   - 找出包含 "failed" 或 "not found" 的行

3. **記錄每個指令的輸出結果**

### 練習 12：清理專案檔案

**任務：** 找出並清理不需要的檔案。

1. **建立測試環境：**
   ```bash
   mkdir -p ~/test-cleanup
   touch ~/test-cleanup/file1.tmp
   touch ~/test-cleanup/file2.tmp
   touch ~/test-cleanup/important.txt
   touch ~/test-cleanup/empty.log
   echo "content" > ~/test-cleanup/normal.log
   ```

2. **完成以下任務：**
   - 找出所有 .tmp 檔案
   - 找出所有空檔案
   - 找出所有 .log 檔案
   - （可選）刪除所有 .tmp 檔案

3. **思考問題：**
   - 在刪除檔案前，應該做什麼檢查？
   - 如何確認要刪除的檔案是正確的？

### 練習 13：搜尋程式碼

**任務：** 在專案中搜尋特定的程式碼模式。

1. **建立測試專案：**
   ```bash
   mkdir -p ~/test-project/{src,tests}
   echo "def main():" > ~/test-project/src/app.py
   echo "    print('Hello')" >> ~/test-project/src/app.py
   echo "import os" > ~/test-project/src/utils.py
   echo "def test_main():" > ~/test-project/tests/test_app.py
   ```

2. **完成以下任務：**
   - 找出所有包含 "def main" 的檔案
   - 找出所有包含 "import os" 的檔案
   - 找出所有包含 "TODO" 的檔案（如果有的話）
   - 統計專案中 Python 檔案的總數

---

## 7️⃣ 進階挑戰（選做）

### 挑戰 1：正則表達式搜尋

1. **建立測試檔案：**
   ```bash
   cat > regex-test.txt << 'EOF'
   error123
   error456
   warning789
   info001
   EOF
   ```

2. **嘗試以下搜尋：**
   ```bash
   # 搜尋以 "error" 開頭的行
   grep "^error" regex-test.txt
   
   # 搜尋包含數字的行
   grep "[0-9]" regex-test.txt
   
   # 搜尋以數字結尾的行
   grep "[0-9]$" regex-test.txt
   ```

### 挑戰 2：複雜的 find 搜尋

1. **找出最近 7 天內修改的檔案：**
   ```bash
   find ~ -type f -mtime -7
   ```

2. **找出特定使用者的檔案：**
   ```bash
   find ~ -user $USER
   ```

3. **找出並修改權限：**
   ```bash
   # 找出所有 .sh 檔案並加上執行權限
   find ~/test-project -name "*.sh" -exec chmod +x {} \;
   ```

---

## 8️⃣ 觀念問答

1. **`grep` 和 `find` 有什麼不同？**
   - 它們分別用於什麼場景？

2. **管道的優點是什麼？**
   - 為什麼要使用管道而不是單一指令？

3. **`head` 和 `tail` 在什麼情況下特別有用？**
   - 實際工作中什麼時候會用到 `tail -f`？

4. **如何安全地使用 `find -delete`？**
   - 在刪除檔案前應該做什麼檢查？

5. **請解釋以下指令的作用：**
   ```bash
   find ~/projects -name "*.py" -exec grep -l "TODO" {} \;
   ```

---

## 作業提交說明

請將以上每個步驟的：

1. **指令與輸出**：截圖或文字記錄每個指令的執行結果
2. **觀察記錄**：記錄你在每個步驟中觀察到的現象
3. **問題答案**：回答所有「思考問題」和「觀念問答」
4. **心得反思**：
   - 寫下你對這些工具的理解
   - 說明在什麼情況下應該使用哪個工具
   - 記錄你覺得最實用的技巧

整理成一份完整的文件提交。

