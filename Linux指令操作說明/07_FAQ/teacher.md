# 常見問題與解答 – 教師示範

本文件針對本教學中最常遇到的問題，提供教師在課堂上可以直接示範的解答與說明。請依序閱讀，並在學生提問時對症下藥，必要時示範指令操作。

---

## 1️⃣ 為什麼會出現 `command not found`？

- **原因**  
  1. 指令未安裝（例如 `curl`、`htop`）。  
  2. 執行檔所在目錄未在 `$PATH` 中。  
- **解決步驟**  
  ```sh
  # 確認是否已安裝（以 curl 為例）
  which curl || echo "curl 未安裝"

  # 若未安裝，使用套件管理員安裝
  sudo apt update
  sudo apt install -y curl

  # 若已安裝但不在 PATH，檢查環境變數
  echo $PATH
  # 臨時加入 /usr/local/bin（視實際安裝路徑而定）
  export PATH=$PATH:/usr/local/bin
  # 永久加入寫入 ~/.bashrc
  echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
  source ~/.bashrc
  ```

---

## 2️⃣ `Permission denied` – 權限不足

- **常見情境**  
  1. 嘗試執行沒有執行權限的腳本。  
  2. 嘗試編輯系統檔案（如 `/etc/hosts`）而未使用 `sudo`。  
  3. 刪除非自己擁有的檔案。  
- **解決方式**  
  ```sh
  # 為腳本加上執行權限
  chmod +x myscript.sh

  # 使用 sudo 編輯系統檔案
  sudo nano /etc/hosts

  # 若是普通檔案需要提升權限
  sudo rm /path/to/protected_file
  ```

---

## 3️⃣ `sudo: command not found` 或 `sudo: not in the sudoers file.  This incident will be reported.`

- **原因**  
  - 系統未安裝 `sudo`（極少見於最小化安裝）。  
  - 使用者未加入 `sudo` 群組。  
- **解決步驟**（需要 root 權限）  
  ```sh
  # 先切換到 root（如果有 root 密碼）
  su -
  # 安裝 sudo
  apt update && apt install -y sudo
  # 把使用者加入 sudo 群組（以 pi 為例）
  usermod -aG sudo pi
  # 退出 root，重新登入以套用群組變更
  exit
  ```

---

## 4️⃣ `No such file or directory` – 檔案或目錄不存在

- **檢查方法**  
  1. 使用 `ls` 確認路徑拼寫是否正確。  
  2. 若路徑含空格或特殊字元，需加上引號或使用反斜線跳脫。  
- **示範**  
  ```sh
  # 正確寫法（含空格的目錄）
  cd "My Documents"
  # 或使用跳脫
  cd My\ Documents
  ```

---

## 5️⃣ `ssh: connect to host <host> port 22: Connection timed out`

- **可能原因**  
  1. 目標主機未開啟 SSH 服務（`sshd`）。  
  2. 防火牆阻擋 22 埠。  
  3. 網路不通（IP 錯誤、VPN 未連線）。  
- **排除步驟**  
  ```sh
  # 確認本機能 ping 通目標
  ping <host>

  # 檢查目標是否開放 22 埠（需要在目標機執行）
  sudo netstat -tlnp | grep :22

  # 若防火牆阻擋，開放 22 埠（以 ufw 為例）
  sudo ufw allow 22/tcp

  # 確認 sshd 正在執行
  sudo systemctl status ssh
  # 若未啟動
  sudo systemctl start ssh
  sudo systemctl enable ssh
  ```

---

## 6️⃣ `apt-get update` 卡在某個鏡像站或顯示 `404 Not Found`

- **原因**  
  - `/etc/apt/sources.list` 中的鏡像站已過期或不支援當前的發行版。  
- **解決方法**  
  ```sh
  # 先備份原始 sources.list
  sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

  # 編輯 sources.list，改成官方或可靠的鏡像（以 Raspberry Pi OS 為例）
  sudo nano /etc/apt/sources.list
  # 內容示例：
  # deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi
  # deb http://archive.raspberrypi.org/debian/ buster main ui

  # 更新套件清單
  sudo apt update
  ```

---

## 7️⃣ 為什麼 `top` 看不到某些行程？

- **說明**  
  1. `top` 預設只顯示屬於當前使用者的行程（除非使用 `sudo`）。  
  2. 行程可能已結束或被其他使用者隱藏。  
- **解決方式**  
  ```sh
  # 以 root 身分查看全部行程
  sudo top

  # 或使用 ps 結合過濾
  ps -ef | grep <process_name>
  ```

---

## 8️⃣ `grep` 找不到字串卻確定檔案中有

- **可能原因**  
  1. 行尾是 Windows 的 `\r\n`，導致搜尋失敗。  
  2. 檔案是二進位或壓縮檔。  
- **排除方法**  
  ```sh
  # 先轉換檔案為 Unix 格式
  dos2unix file.txt

  # 若是壓縮檔，先解壓縮再搜尋
  gzip -d file.txt.gz
  grep "關鍵字" file.txt
  ```

---

## 9️⃣ `chmod` 後仍然無法執行腳本

- **檢查點**  
  1. 確認檔案的 **執行權限** 已設定（`ls -l script.sh`）。  
  2. 檢查第一行是否有正確的 shebang（如 `#!/bin/bash`）。  
  3. 確認檔案所在的目錄沒有 `noexec` 掛載選項。  
- **示範**  
  ```sh
  # 加上 shebang
  echo '#!/bin/bash' | cat - script.sh > temp && mv temp script.sh

  # 設定執行權限
  chmod +x script.sh

  # 若目錄被掛載為 noexec，重新掛載或搬移檔案
  mount | grep noexec   # 檢查
  sudo mount -o remount,exec /path/to/dir
  ```

---

## 10️⃣ 其他常見問題彙總

| 問題 | 簡短解答 | 示範指令 |
|------|----------|----------|
| `ls: cannot access …: No such file or directory` | 路徑錯誤或檔案已被刪除 | `ls -l <path>` |
| `df -h` 顯示磁碟已滿 | 清理不必要的檔案或擴充磁碟 | `sudo apt clean && sudo rm -rf /var/log/*.gz` |
| `du -sh *` 顯示某目錄佔用過大 | 使用 `ncdu` 交互式檢查 | `sudo apt install -y ncdu && ncdu .` |
| `ssh` 提示 `Host key verification failed` | 目標主機的公鑰變更，需要移除舊的條目 | `ssh-keygen -R <host>` |

---

## 小結

- **先確認環境**：`which`, `echo $PATH`, `whoami`。  
- **使用 `sudo`** 前先確定使用者有權限。  
- **權限與執行**：`chmod`, `chown`, `sudo` 是最常見的三把鑰匙。  
- **排錯流程**：觀察錯誤訊息 → 確認指令/檔案是否存在 → 檢查權限 → 使用 `sudo` 或調整環境變數。  

教師可根據學生的實際提問，挑選上述對應的解答示範，並在課堂上即時演練。祝教學順利！