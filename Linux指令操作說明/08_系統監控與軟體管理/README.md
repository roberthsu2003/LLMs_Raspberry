# 教案：系統監控與軟體管理

## 課程核心目標

讓學生透過實作，深刻理解以下三點：
1. **程序監控 (`ps`, `top`)** 如何查看系統中運行的程序與資源使用情況。
2. **磁碟空間管理 (`df`, `du`)** 如何監控和管理磁碟使用空間。
3. **軟體管理 (`apt`)** 如何安裝、更新和管理系統軟體套件。

---

## 1️⃣ ps：查看運行中的程序

### 核心概念

`ps` (process status) 用於顯示當前系統中運行的程序資訊。

**基本語法：**
```bash
ps [選項]
```

### 基本使用

| 指令 | 說明 | 範例 |
| :--- | :--- | :--- |
| `ps` | 顯示當前終端機的程序 | `ps` |
| `ps aux` | 顯示所有使用者的所有程序 | `ps aux` |
| `ps -ef` | 顯示所有程序的完整資訊 | `ps -ef` |
| `ps aux \| grep 關鍵字` | 搜尋特定程序 | `ps aux \| grep python` |

### ps 輸出欄位說明

執行 `ps aux` 時，會看到以下欄位：

| 欄位 | 說明 |
| :--- | :--- |
| `USER` | 執行程序的使用者 |
| `PID` | 程序 ID（Process ID） |
| `%CPU` | CPU 使用率 |
| `%MEM` | 記憶體使用率 |
| `VSZ` | 虛擬記憶體大小 |
| `RSS` | 實體記憶體大小 |
| `TTY` | 終端機編號 |
| `STAT` | 程序狀態 |
| `START` | 啟動時間 |
| `TIME` | CPU 累計使用時間 |
| `COMMAND` | 執行的指令 |

### 實務範例

**範例 1：查看所有 Python 程序**

```bash
ps aux | grep python
```

**範例 2：查看特定使用者的程序**

```bash
ps aux | grep $USER
```

**範例 3：查看程序的詳細資訊**

```bash
# 查看特定 PID 的程序
ps -p 1234

# 查看程序的樹狀結構
ps auxf
```

---

## 2️⃣ top 與 htop：即時系統監控

### 核心概念

- **`top`**：即時顯示系統資源使用情況和運行中的程序
- **`htop`**：`top` 的增強版，提供更友好的介面（需要安裝）

### top 基本使用

**啟動 top：**
```bash
top
```

**top 介面說明：**

```
top - 10:30:00 up 5 days,  2:15,  3 users,  load average: 0.50, 0.45, 0.40
Tasks: 150 total,   1 running, 149 sleeping,   0 stopped,   0 zombie
%Cpu(s):  5.0 us,  2.0 sy,  0.0 ni, 93.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   2048.0 total,    512.0 free,    768.0 used,    768.0 buff/cache
MiB Swap:   1024.0 total,   1024.0 free,      0.0 used

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 1234 pi        20   0   12345   5678   1234 S   5.0   0.3   0:10.50 python
```

**top 常用操作：**

| 按鍵 | 功能 |
| :--- | :--- |
| `q` | 離開 top |
| `k` | 終止程序（輸入 PID） |
| `M` | 按記憶體使用率排序 |
| `P` | 按 CPU 使用率排序 |
| `1` | 顯示所有 CPU 核心 |
| `h` | 顯示幫助 |

### htop（進階）

如果系統有安裝 `htop`，它提供更友好的介面：

```bash
# 安裝 htop（Debian/Ubuntu）
sudo apt install htop

# 使用
htop
```

**htop 的優點：**
- 彩色顯示，更易讀
- 可以用滑鼠操作
- 更直觀的圖表顯示

---

## 3️⃣ df：查看磁碟空間

### 核心概念

`df` (disk free) 用於顯示檔案系統的磁碟空間使用情況。

**基本語法：**
```bash
df [選項] [檔案系統]
```

### 基本使用

| 指令 | 說明 | 範例 |
| :--- | :--- | :--- |
| `df` | 顯示所有檔案系統的空間使用 | `df` |
| `df -h` | 以人類可讀的格式顯示（推薦） | `df -h` |
| `df -h /` | 顯示根目錄的空間使用 | `df -h /` |
| `df -i` | 顯示 inode 使用情況 | `df -i` |

### df 輸出欄位說明

執行 `df -h` 時，會看到：

| 欄位 | 說明 |
| :--- | :--- |
| `Filesystem` | 檔案系統名稱 |
| `Size` | 總容量 |
| `Used` | 已使用空間 |
| `Avail` | 可用空間 |
| `Use%` | 使用百分比 |
| `Mounted on` | 掛載點 |

### 實務範例

```bash
# 查看所有磁碟空間（人類可讀格式）
df -h

# 查看根目錄空間
df -h /

# 查看特定目錄所在的分割區
df -h /home
```

---

## 4️⃣ du：查看目錄大小

### 核心概念

`du` (disk usage) 用於顯示目錄或檔案佔用的磁碟空間。

**基本語法：**
```bash
du [選項] [目錄或檔案]
```

### 基本使用

| 指令 | 說明 | 範例 |
| :--- | :--- | :--- |
| `du` | 顯示當前目錄的大小 | `du` |
| `du -h` | 以人類可讀的格式顯示 | `du -h` |
| `du -sh 目錄` | 顯示目錄總大小（摘要） | `du -sh ~/Documents` |
| `du -h --max-depth=1` | 顯示第一層子目錄的大小 | `du -h --max-depth=1` |
| `du -h \| sort -h` | 按大小排序 | `du -h \| sort -h` |

### 實務範例

**範例 1：找出佔用空間最大的目錄**

```bash
# 查看家目錄下各目錄的大小
du -h --max-depth=1 ~ | sort -h

# 找出最大的 5 個目錄
du -h --max-depth=1 ~ | sort -h | tail -5
```

**範例 2：找出大檔案**

```bash
# 找出當前目錄下大於 100MB 的檔案
find . -type f -size +100M -exec du -h {} \;
```

---

## 5️⃣ apt：軟體套件管理（Debian/Ubuntu）

### 核心概念

`apt` (Advanced Package Tool) 是 Debian/Ubuntu 系統的套件管理工具，用於安裝、更新、移除軟體。

**重要：** 大部分操作需要 `sudo` 權限。

### 基本使用

| 指令 | 說明 | 範例 |
| :--- | :--- | :--- |
| `sudo apt update` | 更新套件列表 | `sudo apt update` |
| `sudo apt upgrade` | 升級所有已安裝的套件 | `sudo apt upgrade` |
| `sudo apt install 套件名` | 安裝套件 | `sudo apt install htop` |
| `sudo apt remove 套件名` | 移除套件（保留設定檔） | `sudo apt remove htop` |
| `sudo apt purge 套件名` | 移除套件（包含設定檔） | `sudo apt purge htop` |
| `apt search 關鍵字` | 搜尋套件 | `apt search python` |
| `apt show 套件名` | 顯示套件資訊 | `apt show htop` |
| `apt list --installed` | 列出已安裝的套件 | `apt list --installed` |

### 實務範例

**範例 1：安裝新軟體**

```bash
# 1. 更新套件列表
sudo apt update

# 2. 搜尋要安裝的軟體
apt search htop

# 3. 查看軟體資訊
apt show htop

# 4. 安裝軟體
sudo apt install htop
```

**範例 2：更新系統**

```bash
# 1. 更新套件列表
sudo apt update

# 2. 升級所有套件
sudo apt upgrade

# 3. 升級系統（包含核心）
sudo apt full-upgrade
```

**範例 3：清理系統**

```bash
# 移除不再需要的套件
sudo apt autoremove

# 清理下載的套件快取
sudo apt autoclean
```

---

## 6️⃣ 系統監控實務範例

### 範例 1：監控系統資源

**情境：** 檢查系統的 CPU、記憶體和磁碟使用情況。

```bash
# 1. 查看 CPU 和記憶體使用
top -bn1 | head -5

# 2. 查看磁碟空間
df -h

# 3. 查看記憶體使用詳情
free -h

# 4. 查看系統負載
uptime
```

### 範例 2：找出佔用資源的程序

**情境：** 找出佔用 CPU 或記憶體最多的程序。

```bash
# 1. 按 CPU 使用率排序
ps aux --sort=-%cpu | head -10

# 2. 按記憶體使用率排序
ps aux --sort=-%mem | head -10

# 3. 使用 top 即時監控
top
# 然後按 'P' 按 CPU 排序，按 'M' 按記憶體排序
```

### 範例 3：清理磁碟空間

**情境：** 找出佔用空間的檔案和目錄。

```bash
# 1. 查看各目錄大小
du -h --max-depth=1 ~ | sort -h

# 2. 找出大檔案（大於 100MB）
find ~ -type f -size +100M -exec ls -lh {} \;

# 3. 清理 apt 快取
sudo apt clean
```

---

## 7️⃣ 常見問題與除錯

### 問題 1：系統變慢

**檢查步驟：**

1. 查看系統負載：
   ```bash
   uptime
   ```

2. 查看 CPU 使用率：
   ```bash
   top
   # 按 'P' 按 CPU 排序
   ```

3. 查看記憶體使用：
   ```bash
   free -h
   ```

4. 找出佔用資源的程序：
   ```bash
   ps aux --sort=-%cpu | head -10
   ```

### 問題 2：磁碟空間不足

**檢查步驟：**

1. 查看磁碟使用情況：
   ```bash
   df -h
   ```

2. 找出佔用空間的目錄：
   ```bash
   du -h --max-depth=1 / | sort -h
   ```

3. 找出大檔案：
   ```bash
   find / -type f -size +100M 2>/dev/null
   ```

### 問題 3：無法安裝軟體

**可能原因與解決方法：**

1. **套件列表過舊：**
   ```bash
   sudo apt update
   ```

2. **網路連線問題：**
   ```bash
   ping 8.8.8.8
   ```

3. **權限不足：**
   - 確認使用 `sudo`

4. **套件名稱錯誤：**
   ```bash
   apt search 關鍵字
   ```

---

## 8️⃣ 進階技巧

### 監控腳本範例

**建立系統監控腳本：**

```bash
cat > ~/monitor.sh << 'EOF'
#!/bin/bash
echo "=== System Monitor ==="
echo "Date: $(date)"
echo ""
echo "=== Disk Usage ==="
df -h
echo ""
echo "=== Memory Usage ==="
free -h
echo ""
echo "=== Top 5 CPU Processes ==="
ps aux --sort=-%cpu | head -6
echo ""
echo "=== Top 5 Memory Processes ==="
ps aux --sort=-%mem | head -6
EOF

chmod +x ~/monitor.sh
```

**執行：**
```bash
~/monitor.sh
```

### 自動清理腳本

**建立清理腳本：**

```bash
cat > ~/cleanup.sh << 'EOF'
#!/bin/bash
echo "Cleaning apt cache..."
sudo apt clean

echo "Removing unused packages..."
sudo apt autoremove -y

echo "Finding large files..."
find ~ -type f -size +100M 2>/dev/null | head -10
EOF

chmod +x ~/cleanup.sh
```

---

## 9️⃣ 總結

### 核心要點

1. **`ps`** 用於查看運行中的程序
2. **`top`/`htop`** 用於即時監控系統資源
3. **`df`** 用於查看檔案系統的磁碟空間
4. **`du`** 用於查看目錄或檔案的大小
5. **`apt`** 用於管理軟體套件（Debian/Ubuntu）

### 實務建議

- ✅ **定期監控**：使用 `top` 或 `htop` 定期檢查系統資源
- ✅ **空間管理**：使用 `df` 和 `du` 監控磁碟使用情況
- ✅ **系統更新**：定期執行 `apt update && apt upgrade`
- ✅ **清理維護**：定期清理不需要的檔案和套件

### 下一步

完成 `student.md` 中的練習，親手體驗系統監控與軟體管理的操作！

