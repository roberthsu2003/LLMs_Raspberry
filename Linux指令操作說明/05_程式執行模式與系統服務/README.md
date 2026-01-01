# 教案：前景程序、背景工作與系統服務

## 課程核心目標

讓學生透過實作，深刻理解以下三點：
1.  **前景程序 (Foreground Process)** 如何綁定終端機，以及為何關閉視窗會導致程序終止。
2.  **背景工作 (Background Job)** 的概念，以及如何使用 `&`, `jobs`, `fg`, `bg`, `kill` 進行工作控制。
3.  **系統服務 (Service)** 與背景工作的本質區別，以及為何正式環境必須使用 `systemd` 這類的服務管理器。

---

![linux的程式執行模式與系統服務](./images/linux的程式執行模式與系統服務.png)

## 1️⃣ 前景程序：一切的起點

**目標**：展示前景程序會「占用」終端機，直到它執行完畢或被中斷。

| 老師操作 (Teacher's Action) | 預期結果 (Expected Outcome) | 解說重點 (Explanation Points) |
| :--- | :--- | :--- |
| `sleep 300` | 終端機沒有反應，無法輸入新指令。 | 1. `sleep 300` 是一個前景程序，它會持續執行 300 秒。 <br> 2. 在它結束前，這個終端機被「卡住」了，無法做其他事。 |
| 按下 `Ctrl + C` | `sleep` 命令被中斷，終端機恢復正常，可以輸入指令。 | 1. `Ctrl + C` 會送出一個 `SIGINT` 信號，意思是「請中斷」。<br> 2. 這是終止前景程序的標準方法。 |

---

## 2️⃣ 背景工作：讓程序在背景執行

**目標**：學會使用 `&` 將程序放到背景執行，釋放終端機。

| 老師操作 (Teacher's Action) | 預期結果 (Expected Outcome) | 解說重點 (Explanation Points) |
| :--- | :--- | :--- |
| `sleep 300 &` | 畫面上出現 `[1] 12345` 這樣的字樣，然後可以立刻輸入新指令。 | 1. `&` 的意思是「在背景執行」。<br> 2. `[1]` 是「工作編號 (Job ID)」，`12345` 是「程序編號 (PID)」。<br> 3. 終端機立刻被釋放了，我們可以做其他事。 |
| ps aux \| grep sleep | 可以看到剛剛執行的 `sleep 300` 程序仍在列表中。 | `ps` 指令可證明程序確實還「活著」，<br>只是它已不在前景與我們互動。 |

## 3️⃣ 工作控制：管理背景工作

**目標**：學習 `jobs`, `fg`, `bg`, `kill` 來靈活操作背景工作。

| 老師操作 (Teacher's Action) | 預期結果 (Expected Outcome) | 解說重點 (Explanation Points) |
| :--- | :--- | :--- |
| `jobs -l` | 顯示 `[1]+  Running   sleep 300 &` 以及其 PID。 | 1. `jobs` 指令可以列出目前這個終端機的所有「背景工作」。<br> 2. `-l` 參數可以同時顯示 PID。 |
| `fg %1` | `sleep 300` 回到前景，終端機再次被卡住。 | 1. `fg` (foreground) 可以將背景工作拉回前景。<br> 2. `%1` 代表要操作「工作編號」為 1 的工作。 |
| 按下 `Ctrl + Z` | `sleep` 命令被「暫停」，終端機恢復。畫面上顯示 `[1]+  Stopped   sleep 300`。 | 1. `Ctrl + Z` 送出 `SIGTSTP` 信號，意思是「暫停」。<br> 2. 程序還活著，但被凍結了。 |
| `bg %1` | 畫面上顯示 `[1]+ sleep 300 &`，`jobs` 顯示其狀態為 `Running`。 | 1. `bg` (background) 可以讓一個「已暫停」的工作在背景「繼續執行」。 |
| `kill %1` | 畫面上顯示 `[1]+  Terminated   sleep 300`。 | 1. `kill` 不僅能用 PID，也能用 `%` 加上工作編號來終止程序。<br> 2. `jobs` 列表會顯示工作已被 `Terminated` (終止)。 |

---



## 4️⃣ 存活問題：為何關閉終端機後，程序會消失？



這個問題是從背景工作 (`&`) 轉向系統服務 (`systemd`) 的關鍵。



**簡短答案**：**因為系統會發送 `SIGHUP` (Hang Up) 信號，而程序的預設行為是收到此信號後就終止。**



#### 發生了什麼事？



當你執行 `sleep 300 &`，該程序只是成為一個「背景工作」，但它**仍然隸屬於目前的終端機**。



當你關閉終端機視窗時：

1.  系統會向該終端機下的所有子程序發送 `SIGHUP` 信號。

2.  `sleep 300` 收到了 `SIGHUP`。

3.  `sleep 300` 執行預設行為，即刻終止。



| 關鍵觀念 | 說明 |
| :--- | :--- |
| **背景工作 (`&`)** | 只解決了「不佔用終端機」的問題。 |
| **`SIGHUP` 信號** | 才是程序在終端機關閉時被終止的根本原因。 |



👉 `&` **只解決「佔用」，不解決「存活」**。為了解決存活問題，我們需要 `nohup` 或 `systemd`。



---



## 5️⃣ `nohup`：一個簡單的存活方案



**目標**：理解 `&` 的局限性，並引入 `nohup` 來解決「關閉終端機，程序就終止」的問題。



`nohup` 的全名是 **no hang up**，它的作用只有一個：**讓程序忽略 `SIGHUP` 信號**。



| 老師操作 (Teacher's Action) | 預期結果 (Expected Outcome) | 解說重點 (Explanation Points) |
| :--- | :--- | :--- |
| **(開啟新終端機)** <br> 1. `sleep 300 &` <br> 2. 關閉此終端機視窗。 <br> 3. **(回到原終端機)** <br> `ps aux \| grep sleep` | 找不到 `sleep` 程序。 | 驗證了我們剛才學到的：單純用 `&`，程序會因為 `SIGHUP` 而終止。 |
| **(開啟新終端機)** <br> 1. `nohup sleep 300 &` <br> 2. 畫面上顯示 `nohup: ignoring input and appending output to 'nohup.out'` <br> 3. 關閉此終端機視窗。 <br> 4. **(回到原終端機)** <br> `ps aux \| grep sleep` | 依然可以找到 `sleep 300` 程序。 | 1. `nohup` 讓 `sleep` 程序忽略了 `SIGHUP` 信號，因此得以存活。<br> 2. 所有輸出會被自動導向到 `nohup.out` 檔案中。<br> 3. **重點：** `nohup` 依然不是「服務」，它不會開機自啟，如果程序自己掛了也沒人管。它只是一個臨時的、不可靠的方案。 |



---



## 6️⃣ `systemd`：真正的系統服務

**目標**：透過實作，讓學生理解 `systemd` 作為現代 Linux 服務管理員的核心地位與優勢。

### 6.1 `systemd` 的核心概念

| 核心概念 | `systemd` 的職責 | 關鍵指令 |
| :--- | :--- | :--- |
| **Daemon (守護程序)**：一個在背景執行、獨立於任何終端機、由系統管理的程序。 | 1. **開機自動啟動**：根據設定，在開機時自動運行服務。<br> 2. **狀態監控**：隨時可以查詢服務的運行狀態、讀取日誌。<br> 3. **自動重啟**：如果服務崩潰，`systemd` 可以自動將其重啟。<br> 4. **資源管理**：可以限制服務的 CPU 和記憶體用量。 | `systemctl status <服務名>` (看狀態)<br> `systemctl start <服務名>` (啟動)<br> `systemctl stop <服務名>` (停止)<br> `systemctl enable <服務名>` (設為開機啟動)<br> `systemctl disable <服務名>` (取消開機啟動)<br> `journalctl -u <服務名>` (看日誌) |

---

### 6.2 實作範例：建立第一個 systemd 服務

這個範例的設計理念是：**最小可理解、可觀察、可完整刪除**。

#### 範例目標

> **建立一個 systemd 服務，每 5 秒在 log 裡印一句話**
> 
> 關掉終端機、重新登入，它都還活著
> 
> 最後把它「乾乾淨淨地刪掉」

#### Step 1：準備一個簡單的程式

我們使用 Shell 腳本來建立一個「永遠不會結束的程式」：

```bash
sudo nano /usr/local/bin/hello-service.sh
```

**內容：**

```bash
#!/bin/bash

while true
do
  echo "Hello from systemd at $(date)"
  sleep 5
done
```

**存檔後給執行權限：**

```bash
sudo chmod +x /usr/local/bin/hello-service.sh
```

**教學重點：**

- 這就是一個「永遠不會結束的程式」
- 如果用 `./hello-service.sh &` → **不是服務**
- 接下來要交給 systemd 管

---

#### Step 2：建立 systemd 服務檔（核心）

```bash
sudo nano /etc/systemd/system/hello.service
```

**內容（極簡版）：**

```ini
[Unit]
Description=My First systemd Demo Service

[Service]
ExecStart=/usr/local/bin/hello-service.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

**教學時可以這樣講（一句一句）：**

| 區段 | 說明 |
| :--- | :--- |
| `[Unit]` | 這是什麼服務（人看的） |
| `[Service]` | 真正跑的程式是誰 |
| `Restart=always` | 👉 **這一行就是 systemd 跟 nohup 最大的差別** |
| `[Install]` | 什麼時候自動啟動 |

---

#### Step 3：讓 systemd「認識新服務」

```bash
sudo systemctl daemon-reload
```

**📌 教學比喻**

> 「我新增了一張規格書，要跟 systemd 說一聲」

---

#### Step 4：啟動服務（關鍵轉折點）

```bash
sudo systemctl start hello.service
```

**立刻檢查狀態：**

```bash
systemctl status hello.service
```

**你會看到：**

- `Active: active (running)`
- PID
- 沒有綁定任何終端機

👉 **這一刻就是「它已經活在系統裡了」**

---

#### Step 5：看 log（這一步超有教學效果）

```bash
journalctl -u hello.service -f
```

**你會看到每 5 秒：**

```
Hello from systemd at ...
```

**這時你可以做一件很重要的事：**

👉 **關掉終端機**  
👉 重新登入  
👉 再跑一次：

```bash
journalctl -u hello.service -n 5
```

**學生會瞬間懂一件事：**

> 「原來服務真的跟終端機無關」

---

#### Step 6：停止服務（服務 ≠ 殺程序）

```bash
sudo systemctl stop hello.service
```

**再看：**

```bash
systemctl status hello.service
```

**狀態會變成：**

```
inactive (dead)
```

**📌 教學重點**

> systemd 是「請它停止」，不是 kill 它

---

#### Step 7：完整「消滅」這個服務（收尾很重要）

**1️⃣ 取消開機啟動（如果有）**

```bash
sudo systemctl disable hello.service
```

**2️⃣ 刪掉服務檔**

```bash
sudo rm /etc/systemd/system/hello.service
```

**3️⃣ 刪掉程式本體**

```bash
sudo rm /usr/local/bin/hello-service.sh
```

**4️⃣ 重新載入 systemd**

```bash
sudo systemctl daemon-reload
```

**5️⃣ 驗證真的不見了**

```bash
systemctl status hello.service
```

**會看到：**

```
Unit hello.service could not be found.
```

✅ **乾乾淨淨**

---

### 6.3 三種方法的對照比較

這個範例讓我們可以很自然地對照三種方法的差異：

| 方法 | 關終端機 | 自動重啟 | 系統管理 | 開機自啟 |
| :--- | :--- | :--- | :--- | :--- |
| `&` (背景工作) | ❌ | ❌ | ❌ | ❌ |
| `nohup` | ✅ | ❌ | ❌ | ❌ |
| `systemd` | ✅ | ✅ | ✅ | ✅ |

**學生會真的看到：**

- service 檔案在哪
- systemd 怎麼管它
- 刪掉就真的消失
- 關掉終端機、重新登入，服務依然運行



---



## 7️⃣ 總結：為什麼正式環境一定要用服務

**一句話總結**

> **前景執行**是臨時測試，**背景工作**是暫時方便，**系統服務**才是讓你的程式「真正活在系統裡」的唯一方法。

---

### 實際應用場景對照

**以 `cloudflared` 或任何需要長期運行的服務為例：**

| 執行方式 | 適用場景 | 優點 | 缺點 |
| :--- | :--- | :--- | :--- |
| **手動執行 (`foreground`)** | 本機開發、除錯 | 能即時看到 log，方便除錯 | 關閉終端機就停止，無法長期運行 |
| **`nohup` 執行** | 臨時測試 | 簡單快速，關閉終端機不會停止 | 不會自動重啟，不會開機自啟，無法系統管理 |
| **`systemd` 服務** | 正式環境、生產環境 | 自動重啟、開機自啟、系統管理、狀態監控 | 需要學習服務檔設定 |

**結論：**

- **開發階段**：使用前景執行，方便除錯
- **測試階段**：可以使用 `nohup` 快速測試
- **正式環境**：**必須使用 `systemd`**！確保了服務在重開機後能自動啟動，並且在意外中斷時能被系統監控和重啟
