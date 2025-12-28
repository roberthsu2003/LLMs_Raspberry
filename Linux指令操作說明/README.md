# Linux 指令基礎教學 (新手向)

> **目標**  
> 這份教材專為剛接觸 Linux 的學生設計，透過「老師示範」+「學生練習」的雙向教學模式，讓學員在實作中快速掌握常用指令、概念與除錯技巧。課程內容由淺入深，最後提供進階範例與常見問題排除。

## 📂 教學目錄
- [目錄操作 (01_目錄操作)](01_目錄操作)
- [檔案操作 (02_檔案操作)](02_檔案操作)
- [權限操作 (03_權限操作)](03_權限操作)
- [使用者與群組操作 (04_使用者與群組操作)](04_使用者與群組操作)
- [行程操作 (05_行程操作)](05_行程操作)
- [進階常用指令與小技巧 (06_進階技巧)](06_進階技巧)
- [常見問題排除 (07_FAQ)](07_FAQ)
- [綜合測驗 (08_綜合測驗)](08_綜合測驗)

---

## 📚 學習目標
- 了解 Linux 檔案系統與目錄結構  
- 熟悉檔案、目錄、權限、使用者與行程的基本指令  
- 能在 Raspberry Pi 或任何 Linux 環境下完成日常操作與除錯  

---

## 1️⃣ 目錄操作 (Directory Operations) – 像是在森林中找路

### 說明
| 指令 | 功能 | 常用參數 |
|------|------|----------|
| `pwd` | 顯示目前所在目錄 | 無 |
| `ls` | 列出目錄內容 | `-l` 詳細資訊、`-a` 顯示隱藏檔、`-h` 人類可讀大小 |
| `cd` | 切換目錄 | `..` 上層、`-` 前一次目錄、`~` 使用者家目錄 |
| `mkdir` | 建立新目錄 | `-p` 逐層建立 |
| `rmdir` | 刪除空目錄 | `-p` 逐層刪除 |

### 👨‍🏫 老師示範
```sh
# 1. 查看目前位置
pwd

# 2. 列出家目錄的檔案與目錄 (含隱藏檔)
ls -la

# 3. 建立練習用目錄
mkdir class_demo

# 4. 進入該目錄並確認
cd class_demo
pwd
```

### ✍️ 學生練習
1. 在你的家目錄下建立 `practice_zone` 目錄。  
2. 進入 `practice_zone`，使用 `pwd` 記錄完整路徑。  
3. 回到上一層 (`cd ..`) 並再次確認目前位置。  

---

## 2️⃣ 檔案操作 (File Operations) – 像是在寫筆記

### 說明
| 指令 | 功能 | 常用參數 |
|------|------|----------|
| `touch` | 建立空檔或更新時間戳記 | 無 |
| `cat` | 顯示檔案內容 | `-n` 顯示行號 |
| `cp` | 複製檔案或目錄 | `-r` 複製目錄、`-i` 互動式確認 |
| `mv` | 移動或重新命名 | `-i` 互動式 |
| `rm` | 刪除檔案 | `-r` 刪除目錄、`-i` 互動式、`-f` 強制 |
| `nano` / `vim` | 編輯文字檔 | 無 |

### 👨‍🏫 老師示範
```sh
# 建立空檔案
touch hello.txt

# 查看檔案內容 (目前是空的)
cat hello.txt

# 重新命名檔案
mv hello.txt note.txt

# 複製檔案
cp note.txt backup.txt

# 刪除原始檔案
rm note.txt
```

### ✍️ 學生練習
1. 進入 `practice_zone`。  
2. 建立 `student.txt`，寫入一行文字 (`echo "Hello"` > student.txt)。  
3. 複製為 `student_backup.txt`。  
4. 使用 `rm student.txt` 刪除原檔，確認 `student_backup.txt` 仍在。  

---

## 3️⃣ 權限操作 (Permission Operations) – 誰可以碰我的東西

### 說明
Linux 權限分為 **所有者 (owner)**、**群組 (group)**、**其他人 (others)**，每個類別都有 **讀 (r)**、**寫 (w)**、**執行 (x)** 權限。  
常見指令：

| 指令 | 功能 |
|------|------|
| `ls -l` | 顯示長格式資訊，第一欄即為權限 |
| `chmod` | 變更權限 (符號式或八進位) |
| `chown` | 變更檔案擁有者 |
| `chgrp` | 變更檔案群組 |

#### 符號式範例
- `chmod u+x file` → 為所有者新增執行權限  
- `chmod go-w file` → 移除群組與其他人的寫權限  

#### 八進位範例
- `chmod 755 script.sh` → `rwx r-x r-x`  

### 👨‍🏫 老師示範
```sh
# 查看權限
ls -l student_backup.txt

# 移除寫入權限 (僅保留讀取)
chmod -w student_backup.txt

# 為檔案加上執行權限
chmod +x student_backup.txt

# 改變擁有者 (需 sudo)
sudo chown pi:pi student_backup.txt
```

### ✍️ 學生練習
1. 用 `ls -l` 觀察 `student_backup.txt` 的目前權限。  
2. 執行 `chmod 744 student_backup.txt`，再檢查變化。  
3. 若你有 sudo 權限，使用 `sudo chown root:root student_backup.txt`，觀察權限變化與 `ls -l` 結果。  

---

## 4️⃣ 使用者與群組操作 (User & Group Operations) – 班級管理

### 說明
| 指令 | 功能 |
|------|------|
| `whoami` | 顯示目前使用者名稱 |
| `id` | 顯示 UID、GID 與所屬群組 |
| `groups` | 列出使用者所屬群組 |
| `sudo` | 以管理員身份執行單一指令 |
| `adduser` / `useradd` | 新增使用者 |
| `usermod` | 修改使用者屬性 |
| `groupadd` | 新增群組 |

### 👨‍🏫 老師示範
```sh
whoami          # 例如 pi
id              # 顯示 uid=1000(pi) gid=1000(pi) groups=1000(pi),27(sudo)
groups          # 列出所屬群組

# 更新套件清單（需要 sudo）
sudo apt update
```

### ✍️ 學生練習
1. 執行 `whoami` 並寫下結果。  
2. 使用 `id` 觀察 UID、GID 與所屬群組。  
3. 嘗試 `sudo apt update`（若無 sudo 權限，會顯示錯誤訊息）。  

---

## 5️⃣ 行程操作 (Process Operations) – 電腦在忙什麼

### 說明
| 指令 | 功能 |
|------|------|
| `ps` | 列出目前行程 |
| `top` / `htop` | 即時監控 CPU、記憶體 |
| `pgrep` | 依名稱搜尋行程 PID |
| `kill` | 終止行程 |
| `killall` | 依名稱終止多個行程 |
| `nohup` | 讓程式在退出終端後仍持續執行 |
| `&` | 背景執行指令 |

### 👨‍🏫 老師示範
```sh
# 觀察系統資源使用情況
top

# 列出所有行程，篩選出 bash
ps aux | grep bash

# 假設要終止 PID 為 1234 的程式
kill 1234

# 若要結束所有名為 python 的程式
killall python
```

### ✍️ 學生練習
1. 執行 `top`，觀察 CPU、Memory 使用率，按 `q` 離開。  
2. 用 `ps aux | grep top` 找到 `top` 程式的 PID，然後 `kill` 該 PID (會結束 `top`)。  

---

## 6️⃣ 進階常用指令與小技巧

| 指令 | 小技巧 |
|------|--------|
| `grep` | `grep -i` 忽略大小寫、`grep -R` 遞迴搜尋 |
| `find` | `find . -name "*.py"` 搜尋特定副檔名、`-exec` 執行指令 |
| `history` | `history | grep sudo` 快速找過去使用過的 sudo 指令 |
| `alias` | `alias ll='ls -la'` 建立常用別名 |
| `df -h` | 查看磁碟使用情況（人類可讀） |
| `du -sh *` | 查看當前目錄下各子目錄大小 |
| `wget` / `curl` | 下載檔案或測試 API |
| `nano` vs `vim` | `nano` 友好、`vim` 功能強大（可用 `vimtutor` 練習） |

---

## 7️⃣ 常見問題排除 (FAQ)

1. **指令找不到 (`command not found`)**  
   - 確認是否已安裝該套件 (`sudo apt install <package>`)。  
   - 檢查 `$PATH` 是否包含執行檔目錄 (`echo $PATH`)。

2. **權限不足 (`Permission denied`)**  
   - 使用 `sudo` 提升權限。  
   - 檢查檔案或目錄的權限 (`ls -l`)。  

3. **檔案或目錄不存在 (`No such file or directory`)**  
   - 使用 `ls` 確認路徑拼寫。  
   - 若路徑含空格，請加上引號或使用反斜線跳脫 (`cd "My Folder"` 或 `cd My\ Folder`)。

4. **`apt` 更新失敗**  
   - 確認網路連線。  
   - 嘗試 `sudo apt clean && sudo apt update` 重置快取。  

5. **`top` 顯示奇怪字元**  
   - 可能是 locale 設定不正確，執行 `sudo locale-gen zh_TW.UTF-8 && sudo update-locale LANG=zh_TW.UTF-8`。

---

## 📌 綜合測驗 (大挑戰)

1. 在家目錄下建立 `final_test` 目錄。  
2. 於其中建立 `readme.md`，寫入「Hello Linux」。  
3. 設定權限：所有人皆可讀 (`chmod 644 readme.md`)，只有你可寫 (`chmod u+w readme.md`)。  
4. 使用 `ls -l` 確認權限正確。  
5. (挑戰) 用 `chmod 755` 讓 `readme.md` 變成可執行，觀察 `ls -l` 顯示的 `x` 標記。  

祝你玩得開心，若有任何問題，隨時回報，我會協助除錯！  
