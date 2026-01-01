# 教案：文字處理與搜尋工具

## 課程核心目標

讓學生透過實作，深刻理解以下三點：
1. **文字搜尋工具 (`grep`)** 如何快速在檔案中尋找特定內容。
2. **檔案搜尋工具 (`find`)** 如何根據條件搜尋檔案和目錄。
3. **管道 (`|`) 與重定向** 如何組合多個指令，提升工作效率。

---

## 1️⃣ grep：文字搜尋的利器

### 核心概念

`grep` (Global Regular Expression Print) 是 Linux 中最常用的文字搜尋工具，可以在檔案或輸入中尋找符合條件的文字。

**基本語法：**
```bash
grep [選項] 搜尋模式 檔案名
```

### 基本使用

| 指令 | 說明 | 範例 |
| :--- | :--- | :--- |
| `grep "關鍵字" 檔案` | 在檔案中搜尋關鍵字 | `grep "error" log.txt` |
| `grep -i "關鍵字" 檔案` | 忽略大小寫搜尋 | `grep -i "ERROR" log.txt` |
| `grep -n "關鍵字" 檔案` | 顯示行號 | `grep -n "error" log.txt` |
| `grep -v "關鍵字" 檔案` | 反向搜尋（顯示不包含的行） | `grep -v "debug" log.txt` |
| `grep -r "關鍵字" 目錄` | 遞迴搜尋目錄下所有檔案 | `grep -r "TODO" ~/projects` |
| `grep -l "關鍵字" 檔案` | 只顯示包含關鍵字的檔案名 | `grep -l "error" *.log` |

### 實務範例

**範例 1：在日誌檔中搜尋錯誤**

```bash
# 建立測試日誌檔
cat > app.log << 'EOF'
2025-01-01 10:00:00 INFO: Application started
2025-01-01 10:05:00 ERROR: Database connection failed
2025-01-01 10:10:00 INFO: User logged in
2025-01-01 10:15:00 ERROR: File not found
2025-01-01 10:20:00 WARNING: Memory usage high
EOF

# 搜尋所有錯誤
grep "ERROR" app.log

# 搜尋錯誤並顯示行號
grep -n "ERROR" app.log

# 搜尋錯誤或警告
grep -E "ERROR|WARNING" app.log
```

**範例 2：在配置檔中搜尋設定**

```bash
# 搜尋所有註解行（以 # 開頭）
grep "^#" /etc/ssh/sshd_config

# 搜尋非註解且非空白的行
grep -v "^#" /etc/ssh/sshd_config | grep -v "^$"
```

---

## 2️⃣ find：檔案搜尋的專家

### 核心概念

`find` 是 Linux 中最強大的檔案搜尋工具，可以根據檔名、大小、時間、權限等多種條件搜尋檔案。

**基本語法：**
```bash
find [搜尋路徑] [搜尋條件] [動作]
```

### 基本使用

| 指令 | 說明 | 範例 |
| :--- | :--- | :--- |
| `find . -name "檔名"` | 根據檔名搜尋 | `find . -name "*.txt"` |
| `find . -type f` | 只搜尋檔案 | `find . -type f` |
| `find . -type d` | 只搜尋目錄 | `find . -type d` |
| `find . -size +100M` | 搜尋大於 100MB 的檔案 | `find . -size +100M` |
| `find . -mtime -7` | 搜尋 7 天內修改的檔案 | `find . -mtime -7` |
| `find . -user 使用者` | 搜尋特定使用者的檔案 | `find . -user pi` |
| `find . -perm 644` | 搜尋特定權限的檔案 | `find . -perm 644` |

### 實務範例

**範例 1：搜尋特定類型的檔案**

```bash
# 搜尋所有 .log 檔案
find ~ -name "*.log"

# 搜尋所有 .txt 和 .md 檔案
find ~ -name "*.txt" -o -name "*.md"

# 搜尋所有 Python 檔案
find ~/projects -name "*.py"
```

**範例 2：搜尋大檔案**

```bash
# 搜尋大於 100MB 的檔案
find /home -size +100M

# 搜尋大於 1GB 的檔案並顯示大小
find /home -size +1G -exec ls -lh {} \;
```

**範例 3：搜尋並執行動作**

```bash
# 搜尋所有 .tmp 檔案並刪除
find ~ -name "*.tmp" -delete

# 搜尋所有 .log 檔案並顯示詳細資訊
find ~ -name "*.log" -exec ls -lh {} \;

# 搜尋所有空檔案
find ~ -type f -empty
```

---

## 3️⃣ 管道 (|)：指令的組合技

### 核心概念

**管道 (`|`)** 可以將一個指令的輸出，作為另一個指令的輸入，讓多個指令串接起來，完成複雜的工作。

**基本語法：**
```bash
指令1 | 指令2 | 指令3
```

### 實務範例

**範例 1：組合 grep 和 find**

```bash
# 搜尋所有 .py 檔案，並在其中找 "import os"
find ~/projects -name "*.py" | xargs grep "import os"

# 或使用更安全的方式
find ~/projects -name "*.py" -exec grep -H "import os" {} \;
```

**範例 2：統計檔案數量**

```bash
# 計算當前目錄下的檔案數量
ls -1 | wc -l

# 計算包含 "error" 的行數
grep -r "error" ~/logs | wc -l
```

**範例 3：過濾和排序**

```bash
# 列出所有程序，過濾出 python，並排序
ps aux | grep python | sort

# 列出檔案，過濾出 .txt，顯示前 10 個
ls -1 | grep "\.txt$" | head -10
```

---

## 4️⃣ head 與 tail：查看檔案頭尾

### 核心概念

- **`head`**：顯示檔案的前幾行（預設 10 行）
- **`tail`**：顯示檔案的最後幾行（預設 10 行）

### 基本使用

| 指令 | 說明 | 範例 |
| :--- | :--- | :--- |
| `head 檔案` | 顯示前 10 行 | `head log.txt` |
| `head -n 20 檔案` | 顯示前 20 行 | `head -n 20 log.txt` |
| `tail 檔案` | 顯示最後 10 行 | `tail log.txt` |
| `tail -n 20 檔案` | 顯示最後 20 行 | `tail -n 20 log.txt` |
| `tail -f 檔案` | 即時監看檔案（常用於日誌） | `tail -f app.log` |

### 實務範例

**範例 1：查看日誌檔**

```bash
# 查看日誌檔的最後 50 行
tail -n 50 /var/log/syslog

# 即時監看日誌檔（非常實用！）
tail -f /var/log/syslog
```

**範例 2：查看配置檔開頭**

```bash
# 查看配置檔的前 20 行
head -n 20 /etc/ssh/sshd_config
```

---

## 5️⃣ wc：統計工具

### 核心概念

`wc` (word count) 可以統計檔案的行數、字數、字元數。

### 基本使用

| 指令 | 說明 | 範例 |
| :--- | :--- | :--- |
| `wc 檔案` | 顯示行數、字數、字元數 | `wc file.txt` |
| `wc -l 檔案` | 只顯示行數 | `wc -l file.txt` |
| `wc -w 檔案` | 只顯示字數 | `wc -w file.txt` |
| `wc -c 檔案` | 只顯示字元數 | `wc -c file.txt` |

### 實務範例

```bash
# 統計檔案的行數
wc -l log.txt

# 統計目錄下所有 .py 檔案的總行數
find ~/projects -name "*.py" -exec wc -l {} + | tail -1

# 統計包含 "error" 的行數
grep -r "error" ~/logs | wc -l
```

---

## 6️⃣ 綜合實務範例

### 範例 1：分析日誌檔

**情境：** 分析應用程式的日誌檔，找出錯誤和警告。

```bash
# 建立測試日誌檔
cat > app.log << 'EOF'
2025-01-01 10:00:00 INFO: Application started
2025-01-01 10:05:00 ERROR: Database connection failed
2025-01-01 10:10:00 INFO: User logged in
2025-01-01 10:15:00 ERROR: File not found
2025-01-01 10:20:00 WARNING: Memory usage high
2025-01-01 10:25:00 INFO: Request processed
2025-01-01 10:30:00 ERROR: Timeout occurred
EOF

# 1. 統計總行數
wc -l app.log

# 2. 找出所有錯誤
grep "ERROR" app.log

# 3. 統計錯誤數量
grep "ERROR" app.log | wc -l

# 4. 找出錯誤並顯示行號
grep -n "ERROR" app.log

# 5. 找出錯誤或警告
grep -E "ERROR|WARNING" app.log

# 6. 查看最後 5 行
tail -n 5 app.log
```

### 範例 2：清理專案檔案

**情境：** 找出並清理專案中的臨時檔案。

```bash
# 1. 找出所有 .tmp 檔案
find ~/projects -name "*.tmp"

# 2. 找出所有空檔案
find ~/projects -type f -empty

# 3. 找出大於 100MB 的檔案
find ~/projects -size +100M

# 4. 找出並刪除所有 .tmp 檔案（謹慎使用！）
find ~/projects -name "*.tmp" -delete
```

### 範例 3：搜尋程式碼

**情境：** 在專案中搜尋特定的函數或變數。

```bash
# 1. 在所有 Python 檔案中搜尋 "def main"
find ~/projects -name "*.py" -exec grep -H "def main" {} \;

# 2. 搜尋並顯示檔案名和行號
find ~/projects -name "*.py" -exec grep -Hn "import os" {} \;

# 3. 只顯示包含關鍵字的檔案名
find ~/projects -name "*.py" -exec grep -l "TODO" {} \;
```

---

## 7️⃣ 進階技巧

### 正則表達式基礎

`grep` 支援正則表達式，可以進行更複雜的搜尋：

```bash
# 搜尋以 "error" 開頭的行
grep "^error" file.txt

# 搜尋以 ".log" 結尾的行
grep "\.log$" file.txt

# 搜尋包含數字 3 次以上的行
grep "[0-9]\{3,\}" file.txt
```

### find 的進階用法

```bash
# 搜尋並複製到另一個目錄
find ~/source -name "*.txt" -exec cp {} ~/backup/ \;

# 搜尋並修改權限
find ~/scripts -name "*.sh" -exec chmod +x {} \;

# 搜尋最近 7 天內修改的檔案
find ~ -type f -mtime -7
```

### 組合多個工具

```bash
# 找出所有 .log 檔案，搜尋 "error"，統計數量
find ~/logs -name "*.log" -exec grep -l "error" {} \; | wc -l

# 列出所有程序，過濾出 python，顯示前 5 個
ps aux | grep python | head -5

# 統計目錄下所有檔案的行數總和
find ~/projects -type f -name "*.py" -exec wc -l {} + | tail -1
```

---

## 8️⃣ 常見問題與除錯

### 問題 1：grep 找不到檔案

**錯誤：**
```bash
grep "error" *.log
# grep: *.log: No such file or directory
```

**解決方法：**
```bash
# 先確認檔案是否存在
ls *.log

# 或使用 find 先找出檔案
find . -name "*.log" -exec grep "error" {} \;
```

### 問題 2：find 搜尋太慢

**原因：** 在大型目錄中搜尋會很慢

**解決方法：**
```bash
# 限制搜尋深度
find ~/projects -maxdepth 3 -name "*.py"

# 排除特定目錄
find ~/projects -path "*/node_modules" -prune -o -name "*.py" -print
```

### 問題 3：管道指令失敗

**錯誤：** 前一個指令失敗導致後續指令也失敗

**解決方法：**
```bash
# 使用 set -o pipefail 或檢查每個指令的返回值
grep "error" file.txt | head -10
# 如果 grep 找不到，head 仍會執行（但沒有輸入）
```

---

## 9️⃣ 總結

### 核心要點

1. **`grep`** 是文字搜尋的利器，可以快速在檔案中找內容
2. **`find`** 是檔案搜尋的專家，可以根據多種條件搜尋檔案
3. **管道 (`|`)** 可以組合多個指令，完成複雜的工作
4. **`head`/`tail`** 用於查看檔案的頭尾
5. **`wc`** 用於統計檔案的行數、字數

### 實務建議

- ✅ **日誌分析**：使用 `grep` + `tail` 快速找出問題
- ✅ **檔案清理**：使用 `find` 找出不需要的檔案
- ✅ **程式碼搜尋**：使用 `find` + `grep` 在專案中搜尋
- ✅ **組合使用**：善用管道串接多個指令

### 下一步

完成 `student.md` 中的練習，親手體驗這些工具的強大功能！

