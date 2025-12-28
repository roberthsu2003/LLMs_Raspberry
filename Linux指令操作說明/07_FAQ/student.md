# FAQ 練習 – 學生作業

以下題目設計讓你自行排除常見問題，請依序完成，每一步都要在終端機執行指令並記錄輸出（可直接貼在筆記或截圖），最後將所有結果彙整成一份報告（文字檔或 PDF）提交。

---

## 1️⃣ `command not found` 問題

1. 嘗試執行 `curl --version`，記錄系統回傳的錯誤訊息。  
2. 使用 `which curl` 或 `type curl` 確認是否已安裝。  
3. 若未安裝，使用套件管理員安裝：  
   ```sh
   sudo apt update
   sudo apt install -y curl
   ```  
4. 再次執行 `curl --version`，確認安裝成功。  
5. 若 `curl` 已安裝但仍顯示錯誤，檢查 `$PATH`：  
   ```sh
   echo $PATH
   ```  
   若缺少 `/usr/local/bin`（或 `curl` 所在路徑），使用以下指令暫時加入，並寫入 `~/.bashrc` 永久生效：  
   ```sh
   export PATH=$PATH:/usr/local/bin
   echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
   source ~/.bashrc
   ```

---

## 2️⃣ `Permission denied` 問題

1. 建立一個腳本 `runme.sh`（內容僅 `#!/bin/bash` 與 `echo "Hello"`），然後嘗試直接執行 `./runme.sh`。記錄錯誤訊息。  
2. 為腳本加上執行權限：`chmod +x runme.sh`，再次執行，確認可以正常輸出 `Hello`。  
3. 嘗試編輯系統檔案 `/etc/hosts`（不使用 `sudo`），記錄錯誤訊息。  
4. 使用 `sudo nano /etc/hosts` 編輯，加入一行測試條目（如 `127.0.0.1 test.local`），保存後退出。  
5. 使用 `cat /etc/hosts | grep test.local` 確認剛才的變更已生效。

---

## 3️⃣ `sudo: command not found` 或 `not in the sudoers file` 問題

1. 在終端機執行 `sudo ls /root`，記錄錯誤訊息。  
2. 先切換到 `root`（如果你知道 `root` 密碼）`su -`，然後檢查系統是否已安裝 `sudo`：`which sudo`。  
3. 若未安裝，使用 `apt install sudo` 安裝。  
4. 把自己的使用者（假設為 `pi`）加入 `sudo` 群組：`usermod -aG sudo pi`（需要 `root` 權限）。  
5. 退出 `root`（`exit`），重新登入或執行 `newgrp sudo`，再次執行 `sudo ls /root`，確認可以取得 `root` 目錄列表。

---

## 4️⃣ `No such file or directory` 問題

1. 嘗試 `cat /etc/passwd`，確認正常。  
2. 嘗試 `cat "/etc/ passwd"`（在路徑中加入空格），觀察錯誤訊息。  
3. 正確使用引號或跳脫空格：`cat "/etc/ passwd"` → 錯誤；`cat "/etc/passwd"` → 正確。  
4. 建立一個檔名含空格的檔案：`touch "my file.txt"`。使用以下兩種方式讀取內容：  
   ```sh
   cat "my file.txt"
   cat my\ file.txt
   ```  
   確認兩者皆可成功。

---

## 5️⃣ SSH 連線失敗（Connection timed out）

1. 嘗試連線到一個已知不可達的 IP（如 `ssh pi@192.0.2.1`），記錄錯誤訊息。  
2. 使用 `ping <IP>` 確認網路是否通。  
3. 若 `ping` 失敗，檢查本機網路設定（`ip a`、`ip route`）並修正。  
4. 若 `ping` 正常，檢查遠端主機的 SSH 服務是否啟動：  
   ```sh
   ssh pi@<遠端IP> "systemctl status ssh"
   ```  
   若回傳 `inactive`，在遠端執行 `sudo systemctl start ssh && sudo systemctl enable ssh`。  
5. 檢查防火牆（以 `ufw` 為例）：`sudo ufw status`。若未允許 22 埠，執行 `sudo ufw allow 22/tcp`。  
6. 再次嘗試 `ssh pi@<遠端IP>`，確認可以成功登入。

---

## 6️⃣ `apt update` 失敗或 404 Not Found

1. 執行 `sudo apt update`，記錄出現的錯誤（如鏡像站 404）。  
2. 備份原始來源檔案：`sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak`。  
3. 使用 `nano /etc/apt/sources.list`，將鏡像站改為官方或可靠的鏡像（例如 Raspberry Pi OS 的官方源）。範例內容：  
   ```
   deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi
   deb http://archive.raspberrypi.org/debian/ buster main ui
   ```  
4. 保存後再次執行 `sudo apt update`，確認更新成功。  
5. 若仍有問題，嘗試 `sudo apt clean && sudo apt update`。

---

## 7️⃣ `top` 看不到其他使用者的行程

1. 執行 `top`，觀察只顯示自己的行程。  
2. 使用 `sudo top`，確認可以看到系統上所有使用者的行程。  
3. 使用 `ps -ef | grep <已知的系統服務>`（如 `sshd`）比對結果，確保 `top` 與 `ps` 顯示一致。  

---

## 8️⃣ `grep` 找不到明顯存在的字串

1. 在當前目錄建立檔案 `win.txt`，內容使用 Windows 捲行（`\r\n`），例如：  
   ```sh
   echo -e "Hello\r\nWorld\r\nLinux\r\n" > win.txt
   ```  
2. 使用 `grep "Linux" win.txt`，記錄找不到的結果。  
3. 轉換檔案為 Unix 格式：`dos2unix win.txt`（若未安裝 `dos2unix`，先安裝）。  
4. 再次執行 `grep "Linux" win.txt`，確認可以正確找到字串。  

---

## 9️⃣ `chmod` 後仍無法執行腳本

1. 建立腳本 `run.sh`，內容：  
   ```sh
   #!/bin/bash
   echo "Running..."
   ```  
2. 只給予執行權限給所有者：`chmod u+x run.sh`。執行 `./run.sh`，確認成功。  
3. 移除執行權限：`chmod -x run.sh`，再次執行，記錄 `Permission denied`。  
4. 加上執行權限給所有人：`chmod a+x run.sh`，再次執行，確認成功。  
5. 若仍失敗，檢查腳本第一行的 shebang 是否正確（`#!/bin/bash`），以及所在目錄是否被掛載為 `noexec`（`mount | grep noexec`）。若是 `noexec`，示範重新掛載或搬移檔案至可執行的目錄。  

---

## 10️⃣ 其他自選問題

選擇以下任意一個常見錯誤自行排除，並寫下排錯過程：

- `df -h` 顯示磁碟已滿，清理不必要的檔案或擴充磁碟。  
- `ssh` 提示 `Host key verification failed`，使用 `ssh-keygen -R <host>` 移除舊金鑰。  
- `ls: cannot access …: No such file or directory`，檢查路徑是否正確或檔案是否被刪除。  

---

## 📄 作業提交說明

完成上述所有練習後，請將以下資訊彙整成一份報告（文字檔或 PDF）：

1. 每一步的指令與完整輸出（貼上終端機文字或截圖）。  
2. 遇到的錯誤訊息與你採取的解決方式。  
3. 任何額外的學習筆記或感想。  

祝排錯順利，期待看到你的解題過程！