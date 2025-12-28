# 使用者與群組操作練習 – 學生作業

以下題目請在你的 Linux 環境（Raspberry Pi、Docker、或任何 Linux 主機）上依序完成。每完成一步，請使用 `id`、`groups`、`ls -l` 或將指令輸出截圖保存，作為作業回報的依據。

---

## 1️⃣ 查詢當前身份與群組

1. 執行 `whoami`，寫下顯示的使用者名稱。  
2. 執行 `id`，記錄 UID、GID 與所屬的所有群組。  
3. 執行 `groups`，確認與第 2 步相同的群組列表。  

---

## 2️⃣ 建立新使用者與家目錄

> **提示**：本練習需要 `sudo` 權限。若你沒有管理員權限，請向老師申請或在本機使用 `sudo`。

1. 使用 `sudo adduser alice` 建立使用者 **alice**，依提示設定密碼與資訊。  
2. 確認 `/home/alice` 已被建立，執行 `ls -ld /home/alice`。  
3. 以 `su - alice` 切換至新使用者，執行 `whoami` 確認身分。  
4. 使用 `exit` 返回原使用者。  

---

## 3️⃣ 使用者屬性調整

1. 為 **alice** 加入 `sudo` 群組，使其能使用 `sudo`：  
   ```sh
   sudo usermod -aG sudo alice
   ```  
2. 執行 `id alice`，確認 `sudo` 已列在其群組列表中。  
3. 改變 **alice** 的預設殼程式為 `zsh`（若已安裝）：  
   ```sh
   sudo usermod -s /bin/zsh alice
   ```  
4. 再次以 `su - alice` 登入，執行 `echo $SHELL`，驗證殼程式已變更。  

---

## 4️⃣ 群組管理

1. 建立新群組 `developers`：  
   ```sh
   sudo groupadd developers
   ```  
2. 把 **alice** 加入 `developers`：  
   ```sh
   sudo usermod -aG developers alice
   ```  
3. 使用 `id alice` 或 `groups alice` 確認加入成功。  
4. 刪除群組 `developers`（先確保沒有使用者屬於此群組）：  
   ```sh
   sudo groupdel developers
   ```  

---

## 5️⃣ `sudo` 與 `su` 的實務練習

1. 以 `sudo` 更新套件清單（若系統為 Debian/Ubuntu 系列）：  
   ```sh
   sudo apt update
   ```  
2. 以 `sudo` 編輯系統檔案 `/etc/hosts`（使用 `nano` 或 `vim`），保存後退出。  
3. 使用 `sudo visudo` 開啟 sudoers 檔，搜尋 `#includedir /etc/sudoers.d`，說明此行的作用。  
4. 使用 `su -` 切換至 root，執行 `whoami` 確認身分，之後 `exit` 回到原使用者。  

---

## 6️⃣ 進階挑戰：共享資料夾與 SGID

1. 建立共享目錄 `/opt/shared_project`：  
   ```sh
   sudo mkdir -p /opt/shared_project
   ```  
2. 設定擁有者為 `root`，群組為 `developers`（若已建立）：  
   ```sh
   sudo chown root:developers /opt/shared_project
   ```  
3. 設定權限為 `2775`，使新建立的檔案自動繼承 `developers` 群組：  
   ```sh
   sudo chmod 2775 /opt/shared_project
   ```  
4. 使用 `ls -ld /opt/shared_project` 確認權限顯示為 `drwxrwsr-x`。  
5. 以 **alice**（已在 `developers` 群組）登入，嘗試在此目錄下建立檔案 `test.txt`，檢查檔案的群組是否為 `developers`：  
   ```sh
   su - alice
   echo "test" > /opt/shared_project/test.txt
   ls -l /opt/shared_project/test.txt
   exit
   ```  

---

## 7️⃣ 小挑戰（加分題）

1. 建立一個名為 `project` 的資料夾結構：  
   ```sh
   mkdir -p project/src project/docs project/tests
   ```  
2. 在 `src` 中建立腳本 `run.sh`，內容：  
   ```sh
   #!/bin/bash
   echo "Running project script"
   ```  
3. 設定 `run.sh` 為所有人可讀、所有者可執行（`chmod 744 run.sh`），然後執行 `./project/src/run.sh`。  
4. 把 `src` 目錄的權限改為 `770`，讓群組成員也能執行腳本，驗證效果。  

---

## 作業提交說明

完成所有練習後，請把以下資訊整理成一份報告（文字檔或 PDF）：

- 每一步的指令與對應輸出（可直接貼上終端機文字或截圖）。  
- 遇到的錯誤訊息與解決方式（特別是第 5 題的 `sudo`/`su` 操作）。  
- 加分挑戰的完成結果與個人感想。  

祝練習順利，期待看到你的作業！