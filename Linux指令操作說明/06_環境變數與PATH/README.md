# 教案：環境變數與 PATH

## 課程核心目標

讓學生透過實作，深刻理解以下三點：
1. **環境變數 (Environment Variables)** 是什麼，以及它們如何影響程式的執行。
2. **PATH** 的作用機制，以及為何系統能找到我們輸入的指令。
3. **不同階段的環境變數**（終端機階段、開機階段、服務階段）的差異，以及如何正確設定。

---

## 1️⃣ 環境變數是什麼？

### 核心概念

**環境變數**是系統或程式用來儲存設定資訊的「變數」，它們會影響程式的行為。

想像一下：
- 環境變數就像程式的「設定檔」
- 不同的程式可以讀取這些變數來調整自己的行為
- 就像你告訴程式「我的家目錄在哪裡」、「我喜歡的編輯器是什麼」

### 查看環境變數

| 指令 | 說明 | 範例輸出 |
| :--- | :--- | :--- |
| `env` | 列出所有環境變數 | `USER=pi`<br>`HOME=/home/pi`<br>`PATH=/usr/bin:/bin` |
| `echo $變數名` | 查看特定環境變數 | `echo $HOME` → `/home/pi` |
| `printenv 變數名` | 查看特定環境變數 | `printenv USER` → `pi` |

### 常見的環境變數

| 環境變數 | 作用 | 範例值 |
| :--- | :--- | :--- |
| `HOME` | 使用者的家目錄 | `/home/pi` |
| `USER` | 目前登入的使用者名稱 | `pi` |
| `PATH` | 系統搜尋可執行檔的路徑 | `/usr/bin:/bin:/usr/local/bin` |
| `SHELL` | 預設的 Shell | `/bin/bash` |
| `PWD` | 目前工作目錄 | `/home/pi/Documents` |
| `LANG` | 系統語言設定 | `zh_TW.UTF-8` |

---

## 2️⃣ PATH：系統如何找到指令？

### PATH 的作用機制

當你在終端機輸入 `ls` 時，系統是怎麼找到這個指令的？

**答案：透過 PATH 環境變數！**

### PATH 的工作原理

1. **PATH 是一個路徑列表**，用冒號 (`:`) 分隔
2. **系統會依序在這些路徑中搜尋**你要執行的指令
3. **找到第一個符合的就執行**，找不到就報錯

**範例：**

```bash
echo $PATH
# 輸出：/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

當你輸入 `ls` 時，系統會依序檢查：
1. `/usr/local/sbin/ls` ❌ 不存在
2. `/usr/local/bin/ls` ❌ 不存在
3. `/usr/sbin/ls` ❌ 不存在
4. `/usr/bin/ls` ✅ 找到了！執行它

### 為什麼有些指令找不到？

如果你寫了一個自訂腳本 `my-script.sh`，放在 `/home/pi/my-tools/`，然後直接輸入：

```bash
my-script.sh
```

**會發生什麼？**

```
bash: my-script.sh: command not found
```

**為什麼？**

因為 `/home/pi/my-tools/` 不在 PATH 中，系統找不到這個指令！

**解決方法：**

1. **使用完整路徑：**
   ```bash
   /home/pi/my-tools/my-script.sh
   ```

2. **將路徑加入 PATH（臨時）：**
   ```bash
   export PATH=$PATH:/home/pi/my-tools
   ```

3. **將路徑加入 PATH（永久）**：需要修改設定檔（後面會教）

---

## 3️⃣ 設定環境變數的方法

### 方法 1：臨時設定（只對目前終端機有效）

```bash
# 設定環境變數
export MY_VAR="hello world"

# 查看
echo $MY_VAR
# 輸出：hello world
```

**特點：**
- ✅ 立即生效
- ❌ 關閉終端機後就消失
- ❌ 只對這個終端機視窗有效

### 方法 2：永久設定（對所有終端機有效）

需要修改 Shell 的設定檔。根據不同的 Shell，設定檔也不同：

| Shell | 設定檔 | 何時載入 |
| :--- | :--- | :--- |
| **bash** | `~/.bashrc` | 每次開啟新的終端機時 |
| **bash** | `~/.bash_profile` | 登入時（只載入一次） |
| **zsh** | `~/.zshrc` | 每次開啟新的終端機時 |

**設定步驟：**

1. 編輯設定檔：
   ```bash
   nano ~/.bashrc
   ```

2. 在檔案末尾加入：
   ```bash
   export MY_VAR="hello world"
   export PATH=$PATH:/home/pi/my-tools
   ```

3. 重新載入設定檔：
   ```bash
   source ~/.bashrc
   # 或
   . ~/.bashrc
   ```

**特點：**
- ✅ 永久有效
- ✅ 每次開啟新終端機都會載入
- ❌ 需要重新載入或重開終端機才會生效

---

## 4️⃣ 不同階段的環境變數

這是本課程的核心重點！環境變數在不同的「階段」有不同的來源和影響範圍。

### 階段 1：系統層級（開機階段）

**設定檔位置：** `/etc/environment` 或 `/etc/profile`

**影響範圍：**
- ✅ 所有使用者
- ✅ 所有終端機
- ✅ 系統服務（部分）

**設定方法：**

```bash
sudo nano /etc/environment
```

**內容範例：**

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
JAVA_HOME="/usr/lib/jvm/java-11-openjdk"
```

**特點：**
- 系統開機時載入
- 影響整個系統
- 需要 root 權限修改

---

### 階段 2：使用者層級（終端機階段）

**設定檔位置：** `~/.bashrc` 或 `~/.bash_profile`

**影響範圍：**
- ✅ 該使用者的所有終端機
- ❌ 不影響系統服務
- ❌ 不影響其他使用者

**設定方法：**

```bash
nano ~/.bashrc
```

**內容範例：**

```bash
# 自訂環境變數
export MY_TOOLS="/home/pi/my-tools"
export PATH=$PATH:$MY_TOOLS

# 自訂別名
alias ll='ls -alF'
```

**特點：**
- 使用者登入或開啟終端機時載入
- 只影響該使用者
- 不需要 root 權限

---

### 階段 3：服務層級（systemd 服務）

**設定檔位置：** systemd 服務檔（`.service`）

**影響範圍：**
- ✅ 該服務本身
- ❌ 不影響終端機
- ❌ 不影響其他服務

**設定方法：**

在服務檔中設定：

```ini
[Service]
Environment="MY_VAR=hello"
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/local/bin/my-service.sh
```

**或使用環境變數檔案：**

```ini
[Service]
EnvironmentFile=/etc/my-service/env.conf
ExecStart=/usr/local/bin/my-service.sh
```

**特點：**
- 只影響該服務
- 服務啟動時載入
- 不會繼承終端機的環境變數

---

## 5️⃣ 為什麼要分不同階段？

### 核心原因

**不同的程式在不同的「環境」中運行，需要不同的設定！**

| 階段 | 使用場景 | 為什麼需要獨立設定？ |
| :--- | :--- | :--- |
| **系統層級** | 所有使用者都需要相同的設定 | 例如：系統預設的 PATH，應該所有使用者都一樣 |
| **使用者層級** | 個人化的設定 | 例如：你喜歡的編輯器、個人工具路徑 |
| **服務層級** | systemd 服務需要特定環境 | 例如：服務可能需要特定的資料庫連線資訊，但終端機不需要 |

### 實際案例：為什麼服務看不到終端機的環境變數？

**情境：**

1. 你在終端機設定了：
   ```bash
   export DATABASE_URL="postgresql://localhost/mydb"
   ```

2. 你寫了一個 Python 腳本，它會讀取 `DATABASE_URL`：
   ```python
   import os
   db_url = os.environ.get('DATABASE_URL')
   ```

3. 在終端機執行：✅ 可以正常讀取
   ```bash
   python my-script.py
   ```

4. 設定為 systemd 服務執行：❌ 讀不到！
   ```ini
   [Service]
   ExecStart=/usr/bin/python3 /home/pi/my-script.py
   ```

**為什麼？**

因為 systemd 服務**不會繼承終端機的環境變數**！服務是在「乾淨的環境」中啟動的。

**解決方法：**

在服務檔中明確設定：

```ini
[Service]
Environment="DATABASE_URL=postgresql://localhost/mydb"
ExecStart=/usr/bin/python3 /home/pi/my-script.py
```

---

## 6️⃣ 實務範例：完整的環境變數設定流程

### 範例目標

建立一個自訂工具，並讓它在三個階段都能正確使用。

---

### 範例 1：建立自訂工具並加入 PATH

**步驟 1：建立工具腳本**

```bash
mkdir -p ~/my-tools
nano ~/my-tools/hello-world
```

**內容：**

```bash
#!/bin/bash
echo "Hello from my custom tool!"
echo "Current time: $(date)"
```

**給執行權限：**

```bash
chmod +x ~/my-tools/hello-world
```

**步驟 2：測試（使用完整路徑）**

```bash
~/my-tools/hello-world
# 應該可以執行
```

**步驟 3：加入 PATH（使用者層級）**

```bash
nano ~/.bashrc
```

**在檔案末尾加入：**

```bash
# 自訂工具路徑
export PATH=$PATH:$HOME/my-tools
```

**重新載入：**

```bash
source ~/.bashrc
```

**步驟 4：測試（直接使用指令名）**

```bash
hello-world
# 現在應該可以直接執行了！
```

---

### 範例 2：為 systemd 服務設定環境變數

**情境：** 建立一個服務，需要讀取自訂的環境變數。

**步驟 1：建立服務腳本**

```bash
sudo nano /usr/local/bin/env-demo.sh
```

**內容：**

```bash
#!/bin/bash

while true
do
  echo "Service Name: $SERVICE_NAME"
  echo "Database URL: $DATABASE_URL"
  echo "Current time: $(date)"
  sleep 10
done
```

**給執行權限：**

```bash
sudo chmod +x /usr/local/bin/env-demo.sh
```

**步驟 2：建立服務檔**

```bash
sudo nano /etc/systemd/system/env-demo.service
```

**內容：**

```ini
[Unit]
Description=Environment Variables Demo Service

[Service]
# 方法 1：直接在服務檔中設定
Environment="SERVICE_NAME=MyDemoService"
Environment="DATABASE_URL=postgresql://localhost/demo"

# 方法 2：使用環境變數檔案（推薦，方便管理）
# EnvironmentFile=/etc/env-demo/env.conf

ExecStart=/usr/local/bin/env-demo.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

**步驟 3：啟動服務**

```bash
sudo systemctl daemon-reload
sudo systemctl start env-demo.service
sudo systemctl status env-demo.service
```

**步驟 4：查看服務日誌**

```bash
journalctl -u env-demo.service -f
```

**你會看到服務正確讀取了環境變數！**

---

### 範例 3：使用環境變數檔案（進階）

**當環境變數很多時，建議使用獨立的檔案管理。**

**步驟 1：建立環境變數檔案**

```bash
sudo mkdir -p /etc/env-demo
sudo nano /etc/env-demo/env.conf
```

**內容：**

```bash
# 資料庫設定
DATABASE_URL=postgresql://localhost/demo
DATABASE_USER=admin
DATABASE_PASSWORD=secret123

# 服務設定
SERVICE_NAME=MyDemoService
SERVICE_PORT=8080

# API 金鑰
API_KEY=your-api-key-here
```

**步驟 2：修改服務檔**

```bash
sudo nano /etc/systemd/system/env-demo.service
```

**修改為：**

```ini
[Unit]
Description=Environment Variables Demo Service

[Service]
# 使用環境變數檔案
EnvironmentFile=/etc/env-demo/env.conf
ExecStart=/usr/local/bin/env-demo.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

**步驟 3：重新載入並啟動**

```bash
sudo systemctl daemon-reload
sudo systemctl restart env-demo.service
```

**優點：**
- ✅ 環境變數集中管理
- ✅ 方便修改（不需要改服務檔）
- ✅ 可以設定權限保護敏感資訊

---

## 7️⃣ 環境變數的影響範圍總結

| 設定位置 | 影響範圍 | 何時載入 | 適用場景 |
| :--- | :--- | :--- | :--- |
| `/etc/environment` | 所有使用者、所有終端機 | 系統開機時 | 系統層級的預設設定 |
| `~/.bashrc` | 該使用者的所有終端機 | 開啟終端機時 | 個人化的工具路徑、別名 |
| systemd 服務檔 | 該服務本身 | 服務啟動時 | 服務需要的特定環境變數 |

### 重要觀念

1. **終端機的環境變數 ≠ 服務的環境變數**
   - 在終端機設定的環境變數，服務**看不到**
   - 服務需要在自己的服務檔中設定

2. **PATH 的繼承**
   - 終端機會繼承系統層級的 PATH
   - 服務**不會**繼承終端機的 PATH
   - 服務需要明確設定 PATH

3. **安全性考量**
   - 敏感資訊（如密碼、API 金鑰）應該放在服務的環境變數檔案中
   - 設定適當的檔案權限（`chmod 600`）

---

## 8️⃣ 常見問題與除錯技巧

### 問題 1：為什麼我的指令找不到？

**檢查步驟：**

1. 確認指令是否存在：
   ```bash
   which my-command
   # 或
   ls -l /path/to/my-command
   ```

2. 檢查 PATH：
   ```bash
   echo $PATH
   # 確認你的指令路徑是否在 PATH 中
   ```

3. 檢查執行權限：
   ```bash
   ls -l /path/to/my-command
   # 應該要有 x (執行) 權限
   ```

### 問題 2：為什麼服務讀不到環境變數？

**檢查步驟：**

1. 確認服務檔中是否有設定：
   ```bash
   sudo systemctl show env-demo.service | grep Environment
   ```

2. 檢查服務的實際環境變數：
   ```bash
   sudo systemctl show env-demo.service -p Environment
   ```

3. 查看服務日誌：
   ```bash
   journalctl -u env-demo.service -n 50
   ```

### 問題 3：如何確認環境變數是否正確載入？

**在終端機：**

```bash
# 查看所有環境變數
env

# 查看特定環境變數
echo $MY_VAR

# 在腳本中測試
cat > test-env.sh << 'EOF'
#!/bin/bash
echo "MY_VAR = $MY_VAR"
EOF
chmod +x test-env.sh
./test-env.sh
```

**在服務中：**

修改服務腳本，加入環境變數輸出：

```bash
#!/bin/bash
echo "All environment variables:"
env
echo "MY_VAR = $MY_VAR"
```

然後查看日誌：

```bash
journalctl -u your-service -f
```

---

## 9️⃣ 總結

### 核心要點

1. **環境變數是程式的設定檔**，影響程式的行為
2. **PATH 決定系統在哪裡找指令**
3. **不同階段需要不同的設定方式**：
   - 終端機階段 → `~/.bashrc`
   - 系統層級 → `/etc/environment`
   - 服務階段 → systemd 服務檔
4. **服務不會繼承終端機的環境變數**，必須明確設定

### 實務建議

- ✅ **個人工具**：放在 `~/my-tools`，在 `~/.bashrc` 加入 PATH
- ✅ **系統工具**：放在 `/usr/local/bin`（通常已在 PATH 中）
- ✅ **服務環境變數**：使用服務檔的 `Environment` 或 `EnvironmentFile`
- ✅ **敏感資訊**：使用環境變數檔案，設定適當權限

### 下一步

完成 `student.md` 中的練習，親手體驗環境變數的設定與應用！

