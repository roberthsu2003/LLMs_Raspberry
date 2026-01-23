# 使用者與群組操作教學 – 老師示範

「使用者與群組」管理的完整教學，涵蓋概念說明、常用指令、實務範例與常見錯誤排除。請依序在終端機執行以下指令，並逐一解說每一步的目的與結果，讓學生能在實作中理解背後的機制。

---

## 1️⃣ 基本概念說明

| 概念      | 說明                                                         |
|-----------|--------------------------------------------------------------|
| 使用者    | 系統上每個帳號，擁有唯一的 UID（User ID）。                     |
| 群組      | 多個使用者的集合，透過 GID（Group ID）管理權限。                |
| `sudo`    | 以超級使用者（root）身分執行單一指令，授予暫時的管理權限。      |
| `su`      | 切換至另一使用者（常用於切換至 root），會啟動新登入環境。       |

> **小提醒**：在 Raspberry Pi 預設使用者為 `pi`（UID 1000），已加入 `sudo` 群組，可直接使用 `sudo`。

---

## 2️⃣ 查詢目前身份與群組

```sh
# 顯示當前使用者名稱
whoami

# 顯示 UID、GID 與所屬群組
id

# 列出使用者所屬的所有群組
groups
```

*說明*：`id` 會同時顯示 UID、GID 以及補充的群組列表，便於快速檢查權限屬性。

---

## 3️⃣ 新增與管理使用者

### 3.1 建立新使用者

```sh
# 建立使用者 alice，會自動產生家目錄 /home/alice
sudo adduser alice

# 若僅想建立帳號不建立家目錄（較少使用）
sudo useradd -M bob
```

> **教學重點**：`adduser` 為 Debian 系列的友好腳本，會引導設定密碼與基本資訊；`useradd` 為底層指令，參數較多且不會自動建立家目錄。

### 3.2 刪除使用者

```sh
# 刪除使用者 alice，保留其家目錄
sudo deluser alice

# 同時刪除家目錄與郵件 spool
sudo deluser --remove-home alice
```

### 3.3 修改使用者屬性

```sh
# 將使用者 bob 加入 sudo 群組（授予管理權限）
sudo usermod -aG sudo bob

# 改變使用者的預設登入殼（shell）
sudo usermod -s /bin/zsh alice
```

---

## 4️⃣ 群組的建立與管理

### 4.1 建立新群組

```sh
sudo groupadd developers
```

### 4.2 將使用者加入群組

```sh
# 將 alice 加入 developers 群組
sudo usermod -aG developers alice

# 確認 alice 已屬於該群組
id alice
```

> **提示**：`-aG` 必須同時使用，否則會覆蓋使用者原本的所有輔助群組。

### 4.3 刪除群組

```sh
sudo groupdel developers
```

---

## 5️⃣ `sudo` 與 `su` 的實務使用

### 5.1 `sudo` 執行單一指令

```sh
# 更新套件清單（需要管理權限）
sudo apt update

# 以 root 身分編輯系統檔案
sudo nano /etc/hosts
```

### 5.2 `sudo` 的設定（/etc/sudoers）

```sh
# 使用 visudo 安全編輯 sudoers 檔
sudo visudo

# 允許使用者 bob 無密碼執行所有指令（示範用途，請謹慎使用）
bob ALL=(ALL) NOPASSWD: ALL
```

> **安全建議**：僅在必要時授予 NOPASSWD，避免造成安全風險。

### 5.3 `su` 切換使用者

```sh
# 以 root 身分切換（需要 root 密碼）
su -

# 切換至其他使用者 alice（需要 alice 密碼）
su - alice
```

---

## 6️⃣ 進階範例：結合使用者、群組與權限

假設我們要建立一個共享資料夾，讓 `developers` 群組的所有成員都能讀寫，其他人只能讀取。

```sh
# 1. 建立共享目錄
sudo mkdir /opt/shared_project

# 2. 設定擁有者為 root，群組為 developers
sudo chown root:developers /opt/shared_project

# 3. 設定權限為 2775（設定 SGID，使新檔案繼承群組）
sudo chmod 2775 /opt/shared_project

# 4. 檢查設定
ls -ld /opt/shared_project
```

*說明*：`2` 開頭的 `2` 代表 SGID 位元，讓在此目錄下新建立的檔案自動繼承 `developers` 群組。

---

## 7️⃣ 常見錯誤與排除

| 錯誤訊息                              | 可能原因                     | 解決方式                                        |
|---------------------------------------|------------------------------|------------------------------------------------|
| `useradd: user 'alice' already exists` | 使用者已存在                 | 使用 `usermod` 修改屬性，或先 `deluser alice`   |
| `sudo: command not found`              | 使用者未在 sudo 群組          | `sudo usermod -aG sudo <user>` 並重新登入       |
| `su: Authentication failure`           | 密碼錯誤或帳號被鎖定         | 確認密碼正確，或檢查 `/etc/shadow` 中的狀態   |
| `chmod: operation not permitted`       | 非 root 嘗試改變他人檔案權限   | 使用 `sudo chmod …` 或取得相應權限             |

---

## 8️⃣ 小結

- **`whoami`、`id`、`groups`**：快速查詢身份與群組。  
- **`adduser` / `useradd`**：建立新使用者。  
- **`groupadd`、`usermod -aG`**：管理群組與使用者關係。  
- **`sudo`、`su`**：取得臨時或永久的管理權限。  
- **`chown`、`chmod`**：配合使用者與群組設定檔案/目錄權限。

在示範每個指令後，請讓學生自行練習，並即時檢查 `id`、`groups`、`ls -l` 的變化，確保概念已內化。
