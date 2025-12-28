# 綜合測驗教學 – 老師示範與說明
> **教學目標**  
> 本章節提供教師在課堂上引導學生完成「綜合測驗」的完整流程，涵蓋題目說明、示範解題步驟、常見錯誤與提示，以及完整的解答指引。教師可依需求挑選題目深度，亦可在課堂上即時演練。

---

## 1️⃣ 測驗概述

- **測驗範圍**：結合前七章的核心指令與概念，包括目錄與檔案操作、權限管理、使用者與群組、行程控制、進階文字處理、系統服務與日誌檢視。  
- **題型**：實作題（必做）+ 進階挑戰（加分），每題皆提供「步驟說明」與「期望結果」兩欄。  
- **時間建議**：45 ~ 60 分鐘（依學生熟練度可調整）。

---

## 2️⃣ 教師示範流程

### 2.1 先行說明
1. **說明測驗目的**：驗證學生是否能在真實環境中獨立完成常見系統管理任務。  
2. **提醒注意**：所有指令均可在普通使用者帳號下執行，除非特別標註需要 `sudo`。  
3. **提供範例**：先示範第 1 題（目錄操作），讓學生了解作答格式與驗證方式。

### 2.2 示範題目（以「目錄與檔案」為例）

```sh
# 1. 建立測試目錄
mkdir -p ~/final_test/project/src

# 2. 進入目錄並建立檔案
cd ~/final_test/project/src
touch main.py
echo 'print("Hello, Linux!")' > main.py

# 3. 設定權限：所有人可讀、所有者可寫、執行權限給所有者
chmod 744 main.py

# 4. 檢查結果
ls -l main.py
# 預期輸出：-rwxr--r-- 1 <user> <group> <size> <date> main.py
```

- **教師重點**：  
  - `mkdir -p` 逐層建立。  
  - `chmod 744` 簡潔的八進位表示。  
  - 使用 `ls -l` 驗證權限欄位。

### 2.3 常見錯誤示範與排除

| 錯誤訊息 | 可能原因 | 解決方式 |
|----------|----------|----------|
| `permission denied` (執行 `./main.py`) | 缺少執行權限或 shebang 錯誤 | `chmod +x main.py` 或在首行加入 `#!/usr/bin/env python3` |
| `No such file or directory` (`cd ~/final_test/project/src`) | 目錄尚未建立或路徑拼寫錯誤 | 確認 `mkdir -p` 已成功，使用 `pwd` 核對路徑 |
| `command not found` (`systemctl`) | 非 root 使用者未加 `sudo` | `sudo systemctl status <service>` |

---

## 3️⃣ 測驗題目與解答指引

> **教師提示**：在投放題目前，先把每題的「步驟說明」與「期望結果」投影或印出，讓學生清楚知道要完成什麼。解答指引僅供教師參考，請勿直接給予完整指令，鼓勵學生自行思考。

### 3.1 題目 1 – 目錄與檔案操作
| 步驟 | 說明 |
|------|------|
| 1 | 在家目錄下建立 `final_test` 目錄，並在其中建立子目錄 `project/src`、`project/docs`、`project/tests`。 |
| 2 | 在 `src` 中建立 `main.py`，內容為 `print("Hello, Linux!")`。 |
| 3 | 設定 `main.py` 權限為 **744**（所有人皆可讀，只有擁有者可寫與執行）。 |
| 4 | 使用 `ls -l` 確認權限正確。 |
| **期望結果** | `-rwxr--r--` 權限顯示於 `main.py`。 |

### 3.2 題目 2 – 權限與群組
| 步驟 | 說明 |
|------|------|
| 1 | 在 `final_test` 內建立檔案 `shared.txt`，內容任意。 |
| 2 | 建立新群組 `developers`（`sudo groupadd developers`），將目前使用者加入此群組（`sudo usermod -aG developers $USER`）。 |
| 3 | 把 `shared.txt` 的群組改為 `developers`，權限設為 **664**（所有者讀寫，群組讀寫，其他人只讀）。 |
| 4 | 使用 `ls -l` 檢查 `shared.txt` 權限與群組。 |
| **期望結果** | 權限顯示 `-rw-rw-r--`，群組欄位為 `developers`。 |

### 3.3 題目 3 – 行程管理
| 步驟 | 說明 |
|------|------|
| 1 | 在背景執行長時間指令 `sleep 300 &`，取得其 **PID**。 |
| 2 | 使用 `ps -p <PID> -o pid,stat,cmd` 確認行程狀態為 `S`（睡眠）。 |
| 3 | 使用 `kill -SIGSTOP <PID>` 暫停行程，確認狀態變為 `T`（停止）。 |
| 4 | 使用 `kill -CONT <PID>` 繼續行程，最後使用 `kill -9 <PID>` 終止。 |
| **期望結果** | `ps` 輸出分別顯示 `S`、`T`、`S`（結束前），最終行程不再存在。 |

### 3.4 題目 4 – 文字處理與搜尋
| 步驟 | 說明 |
|------|------|
| 1 | 在 `final_test` 目錄下建立檔案 `log.txt`，內容包含多行文字，其中至少兩行含關鍵字 **ERROR**。 |
| 2 | 使用 `grep -i "error" log.txt` 列出所有包含 **ERROR**（不區分大小寫）的行。 |
| 3 | 使用 `awk '{print NR, $0}' log.txt` 為每行加上行號並輸出。 |
| 4 | 使用 `sed -i 's/ERROR/WARN/g' log.txt` 把所有 **ERROR** 替換為 **WARN**，再用 `cat` 確認變更。 |
| **期望結果** | `grep` 輸出原始 **ERROR** 行，`awk` 輸出行號，`sed` 後檔案不再出現 **ERROR**。 |

### 3.5 題目 5 – 系統服務與日誌
| 步驟 | 說明 |
|------|------|
| 1 | 建立簡易 systemd 服務 `hello.service`（參照第 06 章範例），內容為每分鐘輸出一次 `Hello at $(date)`。 |
| 2 | 重新載入 daemon、啟用並啟動服務：`sudo systemctl daemon-reload && sudo systemctl enable --now hello.service`。 |
| 3 | 使用 `systemctl status hello.service` 確認服務為 **active (running)**。 |
| 4 | 用 `journalctl -u hello.service -n 3` 查看最近三條日誌，確認有 `Hello at …` 訊息。 |
| 5 (加分) | 停止服務並禁用：`sudo systemctl stop hello.service && sudo systemctl disable hello.service`，再次確認狀態為 **inactive (dead)**。 |
| **期望結果** | 服務正常啟動、日誌顯示、停止後狀態為 inactive。 |

### 3.6 題目 6 – 進階挑戰（加分題）
| 步驟 | 說明 |
|------|------|
| 1 | 使用 `find` 找出家目錄下所有超過 **10 MiB** 的檔案，並把結果寫入 `big_files.txt`。 |
| 2 | 使用 `tar` 把這些大檔案一次打包為 `big_files.tar.gz`。 |
| 3 | 把打包檔上傳至遠端主機（假設已設定 SSH 金鑰）使用 `scp`，路徑為 `/tmp/`。 |
| 4 | 在遠端使用 `ssh` 執行 `tar -tzvf /tmp/big_files.tar.gz` 確認檔案清單。 |
| **期望結果** | `big_files.txt` 包含正確路徑，`big_files.tar.gz` 成功傳輸並能在遠端正確解壓列出內容。 |

---

## 4️⃣ 評分指標

| 項目 | 配分 | 評分要點 |
|------|------|----------|
| 正確建立目錄與檔案 | 10 | 路徑、檔名正確、使用 `mkdir -p`、`touch` |
| 權限設定 | 15 | 使用正確的 `chmod`/`chown`，權限欄位符合預期 |
| 行程管理 | 15 | 正確取得 PID、使用 `kill`/`SIGSTOP`/`SIGCONT`，最終行程消失 |
| 文字處理 | 10 | `grep`/`awk`/`sed` 正確運作，結果符合要求 |
| 服務與日誌 | 15 | `systemd` 服務建立、啟動、日誌顯示、停用 |
| 進階挑戰 | 20 | `find`、`tar`、`scp`、遠端驗證完整 |
| 文件說明與排版 | 5 | 作業報告文字清晰、指令與輸出完整 |
| 加分題完成度 | 10 | 任何加分題完整執行並提供說明 |

> **總分 100 分**，加分題最高可獲 10 分額外加分。

---

## 5️⃣ 教師評分與回饋

1. **即時檢查**：在學生提交作業前，可使用 `diff` 與範例答案比對。  
2. **口頭提問**：針對每題的「為什麼要這樣做」進行簡短問答，確認概念是否內化。  
3. **回饋表**：在作業結束後給予每位學生書面回饋，指出做得好的地方與可改進的項目（如指令使用的最佳參數、錯誤排除流程）。  

---

## 6️⃣ 參考答案（教師備註）

> 以下僅供教師在需要時快速核對，請勿直接交給學生。

```sh
# 題目 1
mkdir -p ~/final_test/project/{src,docs,tests}
echo 'print("Hello, Linux!")' > ~/final_test/project/src/main.py
chmod 744 ~/final_test/project/src/main.py
ls -l ~/final_test/project/src/main.py

# 題目 2
touch ~/final_test/shared.txt
sudo groupadd developers
sudo usermod -aG developers $USER
sudo chgrp developers ~/final_test/shared.txt
chmod 664 ~/final_test/shared.txt
ls -l ~/final_test/shared.txt

# 題目 3
sleep 300 &
PID=$!
ps -p $PID -o pid,stat,cmd
kill -SIGSTOP $PID
ps -p $PID -o pid,stat,cmd
kill -CONT $PID
ps -p $PID -o pid,stat,cmd
kill -9 $PID
ps -p $PID

# 題目 4
cat > ~/final_test/log.txt <<'EOF'
Line one
Error occurred here
All good
Another ERROR found
EOF
grep -i "error" ~/final_test/log.txt
awk '{print NR, $0}' ~/final_test/log.txt
sed -i 's/ERROR/WARN/g' ~/final_test/log.txt
cat ~/final_test/log.txt

# 題目 5
cat <<'EOF' | sudo tee /etc/systemd/system/hello.service > /dev/null
[Unit]
Description=Hello World Service

[Service]
ExecStart=/usr/bin/bash -c 'while true; do echo "Hello at $(date)"; sleep 60; done'
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now hello.service
systemctl status hello.service
journalctl -u hello.service -n 3
# 加分
sudo systemctl stop hello.service
sudo systemctl disable hello.service
systemctl status hello.service

# 題目 6（加分）
find $HOME -type f -size +10M > ~/final_test/big_files.txt
tar -czvf ~/final_test/big_files.tar.gz -T ~/final_test/big_files.txt
scp ~/final_test/big_files.tar.gz user@remote:/tmp/
ssh user@remote 'tar -tzvf /tmp/big_files.tar.gz'
```

---

## 7️⃣ 小結

- 透過 **實作** 讓學生將指令從記憶搬到手中，鞏固概念。  
- **即時回饋** 能快速修正錯誤思維，提升學習成效。  
- 本測驗涵蓋了前面所有章節的核心內容，完成後學生將具備在 Linux 系統上自行完成日常管理任務的能力。

祝教學順利，期待看到學生的精彩作品！