# 使用者與群組操作練習 – 學生實作手冊

歡迎來到使用者與群組操作實作練習！使用者與群組管理是 Linux 系統管理的基礎，掌握這些技能對於系統管理非常重要。請在您的 Raspberry Pi（或任何 Linux 終端）上逐一完成以下任務。

---

## 📋 練習前準備

在開始之前，請先確認您的環境：

```sh
# 檢查目前使用者
whoami

# 檢查使用者資訊
id

# 檢查所屬群組
groups
```

> **重要提示**：本練習的許多操作需要 `sudo` 權限。若您沒有管理員權限，請向老師申請或在本機使用 `sudo`。

---

## 1️⃣ 查詢當前身份與群組

### 任務目標
學會查看當前使用者的身份資訊和群組成員資格。

### 操作步驟
1. 執行 `whoami`，查看當前使用者名稱：
   ```sh
   whoami
   ```
   - **記錄：** 寫下顯示的使用者名稱

2. 執行 `id`，查看詳細的使用者資訊：
   ```sh
   id
   ```
   - **記錄：** 記錄 UID、GID 與所屬的所有群組
   - **觀察：** UID 和 GID 是什麼數字？

3. 執行 `groups`，查看所屬群組列表：
   ```sh
   groups
   ```
   - **確認：** 與第 2 步的群組列表是否相同？

4. **進階查看：** 查看其他使用者的資訊（如果系統有其他使用者）：
   ```sh
   id root
   groups root
   ```

### 預期結果
- 能夠查看當前使用者的身份資訊
- 理解 UID、GID 的意義
- 知道如何查看使用者所屬的群組

### 自我檢查
- [ ] 我能說出當前使用者的 UID 和 GID
- [ ] 我知道如何查看使用者所屬的所有群組
- [ ] 我了解 `id` 和 `groups` 的輸出有什麼不同

---

## 2️⃣ 建立新使用者與家目錄

### 任務目標
學會建立新使用者，理解使用者建立的過程。

> **提示**：本練習需要 `sudo` 權限。若您沒有管理員權限，請向老師申請或在本機使用 `sudo`。

### 操作步驟
1. 使用 `adduser` 建立使用者 **alice**：
   ```sh
   sudo adduser alice
   ```
   - **依提示操作：** 設定密碼與基本資訊（可以按 Enter 跳過非必要資訊）

2. 確認 `/home/alice` 已被建立：
   ```sh
   ls -ld /home/alice
   ```
   - **觀察：** 家目錄的權限是什麼？

3. 查看新使用者的資訊：
   ```sh
   id alice
   groups alice
   ```

4. 以 `su` 切換至新使用者：
   ```sh
   su - alice
   ```

5. 確認身分：
   ```sh
   whoami
   pwd
   ```

6. 返回原使用者：
   ```sh
   exit
   ```

### 預期結果
- 能夠建立新使用者
- 理解 `adduser` 會自動建立家目錄
- 能夠使用 `su` 切換使用者

### 自我檢查
- [ ] 我了解 `adduser` 和 `useradd` 的差異
- [ ] 我知道新使用者的家目錄在哪裡
- [ ] 我能使用 `su` 切換使用者並返回

---

## 3️⃣ 使用者屬性調整

### 任務目標
學會修改使用者的屬性，包括群組成員資格和預設 shell。

### 操作步驟
1. 為 **alice** 加入 `sudo` 群組，使其能使用 `sudo`：
   ```sh
   sudo usermod -aG sudo alice
   ```
   - **注意：** `-aG` 必須同時使用，否則會覆蓋原有的群組

2. 確認 `sudo` 已列在其群組列表中：
   ```sh
   id alice
   ```
   - **觀察：** `sudo` 群組是否出現在列表中？

3. **測試 sudo 權限：**
   ```sh
   su - alice
   sudo whoami  # 應該顯示 root
   exit
   ```

4. 改變 **alice** 的預設殼程式（如果系統有安裝 zsh）：
   ```sh
   # 先檢查 zsh 是否存在
   which zsh
   
   # 如果存在，改變預設 shell
   sudo usermod -s /bin/zsh alice
   ```

5. 再次以 `su - alice` 登入，驗證殼程式：
   ```sh
   su - alice
   echo $SHELL
   exit
   ```

### 預期結果
- 能夠將使用者加入群組
- 能夠修改使用者的預設 shell
- 理解 `-aG` 參數的重要性

### 自我檢查
- [ ] 我了解 `usermod -aG` 的作用
- [ ] 我知道為什麼要使用 `-aG` 而不是 `-G`
- [ ] 我能修改使用者的預設 shell

---

## 4️⃣ 群組管理

### 任務目標
學會建立、管理群組，並將使用者加入群組。

### 操作步驟
1. 建立新群組 `developers`：
   ```sh
   sudo groupadd developers
   ```

2. 確認群組已建立：
   ```sh
   getent group developers
   ```

3. 把 **alice** 加入 `developers` 群組：
   ```sh
   sudo usermod -aG developers alice
   ```

4. 確認加入成功：
   ```sh
   id alice
   groups alice
   ```
   - **觀察：** `developers` 群組是否出現在列表中？

5. **測試群組權限：**
   ```sh
   # 建立一個屬於 developers 群組的目錄
   sudo mkdir -p /opt/dev_workspace
   sudo chown root:developers /opt/dev_workspace
   sudo chmod 775 /opt/dev_workspace
   
   # 以 alice 身份測試
   su - alice
   touch /opt/dev_workspace/test.txt
   ls -l /opt/dev_workspace/
   exit
   ```

6. **清理：** 刪除群組（先確保沒有使用者屬於此群組）：
   ```sh
   sudo groupdel developers
   ```

### 預期結果
- 能夠建立和刪除群組
- 能夠將使用者加入群組
- 理解群組在權限管理中的作用

### 自我檢查
- [ ] 我能建立新群組
- [ ] 我能將使用者加入群組
- [ ] 我理解群組在權限管理中的重要性

---

## 5️⃣ `sudo` 與 `su` 的實務練習

### 任務目標
理解 `sudo` 和 `su` 的差異，學會安全地使用管理員權限。

### 操作步驟
1. **使用 `sudo` 執行單一指令：**
   ```sh
   sudo whoami
   ```
   - **觀察：** 輸出是什麼？為什麼？

2. 以 `sudo` 更新套件清單（若系統為 Debian/Ubuntu 系列）：
   ```sh
   sudo apt update
   ```
   - **觀察：** 需要輸入密碼嗎？是誰的密碼？

3. **使用 `sudo` 編輯系統檔案：**
   ```sh
   sudo nano /etc/hosts
   ```
   - **操作：** 查看檔案內容，不要修改，直接退出（Ctrl+X）
   - **思考：** 為什麼需要 `sudo` 才能編輯這個檔案？

4. **查看 sudo 設定：**
   ```sh
   sudo visudo -c  # 檢查語法
   ```
   - **注意：** 不要直接編輯 `/etc/sudoers`，使用 `visudo` 更安全

5. **使用 `su` 切換至 root：**
   ```sh
   su -
   ```
   - **輸入 root 密碼**（如果有的話）
   - 執行 `whoami` 確認身分
   - 執行 `pwd` 查看當前目錄
   - 使用 `exit` 回到原使用者

6. **比較 `su` 和 `su -`：**
   ```sh
   su root  # 不切換環境
   pwd
   exit
   
   su - root  # 切換環境（推薦）
   pwd
   exit
   ```

### 預期結果
- 理解 `sudo` 和 `su` 的差異
- 知道何時使用 `sudo`，何時使用 `su`
- 能夠安全地使用管理員權限

### 自我檢查
- [ ] 我了解 `sudo` 和 `su` 的差異
- [ ] 我知道 `su` 和 `su -` 的差異
- [ ] 我能安全地使用管理員權限執行操作

---

## 6️⃣ 進階挑戰：共享資料夾與 SGID

### 任務目標
學會設定共享目錄，讓群組成員可以協作。

### 操作步驟
1. **重新建立 developers 群組（如果之前刪除了）：**
   ```sh
   sudo groupadd developers
   sudo usermod -aG developers alice
   ```

2. 建立共享目錄：
   ```sh
   sudo mkdir -p /opt/shared_project
   ```

3. 設定擁有者為 `root`，群組為 `developers`：
   ```sh
   sudo chown root:developers /opt/shared_project
   ls -ld /opt/shared_project
   ```

4. 設定權限為 `2775`（SGID 位元）：
   ```sh
   sudo chmod 2775 /opt/shared_project
   ls -ld /opt/shared_project
   ```
   - **觀察：** 權限顯示為 `drwxrwsr-x`，注意 `s` 的位置
   - **說明：** `s` 代表 SGID，新建立的檔案會自動繼承群組

5. **測試 SGID 效果：**
   ```sh
   # 以 alice 身份建立檔案
   su - alice
   echo "test content" > /opt/shared_project/test.txt
   ls -l /opt/shared_project/test.txt
   ```
   - **觀察：** 檔案的群組是否為 `developers`？
   - **思考：** 為什麼新建立的檔案自動屬於 `developers` 群組？

6. 返回原使用者：
   ```sh
   exit
   ```

### 預期結果
- 理解 SGID 位元的作用
- 能夠設定共享目錄讓群組成員協作
- 知道如何讓新檔案自動繼承群組

### 自我檢查
- [ ] 我理解 SGID 位元的作用
- [ ] 我知道如何設定共享目錄
- [ ] 我能解釋為什麼新檔案會自動繼承群組

---

## 7️⃣ 綜合挑戰：建立專案協作環境

### 任務目標
綜合運用所學，建立一個適合團隊協作的專案環境。

### 操作步驟
1. **建立專案結構：**
   ```sh
   sudo mkdir -p /opt/project/{src,docs,tests}
   ```

2. **建立專案群組：**
   ```sh
   sudo groupadd project_team
   sudo usermod -aG project_team alice
   sudo usermod -aG project_team $(whoami)  # 將自己加入
   ```

3. **設定專案目錄的擁有者和群組：**
   ```sh
   sudo chown -R root:project_team /opt/project
   ```

4. **設定適當的權限：**
   ```sh
   # src 目錄：群組成員可讀寫執行
   sudo chmod 2775 /opt/project/src
   
   # docs 目錄：所有人可讀，群組可寫
   sudo chmod 2774 /opt/project/docs
   
   # tests 目錄：群組成員可讀寫執行
   sudo chmod 2775 /opt/project/tests
   ```

5. **測試協作功能：**
   ```sh
   # 以 alice 身份建立檔案
   su - alice
   echo "#!/bin/bash" > /opt/project/src/script.sh
   echo "echo 'Hello from team'" >> /opt/project/src/script.sh
   chmod +x /opt/project/src/script.sh
   ls -l /opt/project/src/
   exit
   
   # 以自己的身份查看
   ls -l /opt/project/src/
   ```

6. **檢視整個專案結構：**
   ```sh
   tree /opt/project
   ls -lR /opt/project
   ```

### 預期結果
- 能夠建立適合團隊協作的專案環境
- 理解不同目錄需要不同的權限設定
- 能夠運用 SGID 實現群組協作

### 自我檢查
- [ ] 我能建立適合團隊協作的專案環境
- [ ] 我理解不同目錄的權限需求
- [ ] 我能運用 SGID 實現群組協作

---

## 📝 作業提交要求

完成所有練習後，請整理一份學習報告，包含以下內容：

### 1. 操作記錄
- 每個任務的主要指令和輸出結果
- 可以使用終端機的「複製」功能或截圖
- 特別記錄第 6 題的 SGID 實驗結果

### 2. 問題與解決
- 遇到的任何錯誤訊息
- 你是如何解決這些問題的
- 特別是在 `sudo`/`su` 操作中遇到的問題

### 3. 學習心得
- 哪個部分最困難？為什麼？
- `sudo` 和 `su` 有什麼不同？什麼時候用哪個？
- 群組管理在實際工作中有什麼應用？

### 4. 挑戰任務成果
- 綜合挑戰的完成結果
- 專案協作環境的權限設定
- 你對團隊協作權限設計的思考

---

## 💡 學習提示

1. **安全第一**：使用 `sudo` 時要謹慎，確認指令正確再執行
2. **理解概念**：`sudo` 和 `su` 的差異要清楚理解
3. **群組管理**：理解群組在權限管理中的重要性
4. **SGID 應用**：SGID 在團隊協作中非常有用
5. **記錄筆記**：記錄常用的使用者管理指令

---

## 🎯 學習目標檢核

完成所有練習後，您應該能夠：

- [ ] 使用 `whoami`、`id`、`groups` 查看使用者資訊
- [ ] 使用 `adduser` 建立新使用者
- [ ] 使用 `usermod` 修改使用者屬性
- [ ] 使用 `groupadd` 建立群組
- [ ] 使用 `sudo` 執行管理員指令
- [ ] 使用 `su` 切換使用者
- [ ] 理解 `sudo` 和 `su` 的差異
- [ ] 設定 SGID 實現群組協作
- [ ] 建立適合團隊協作的專案環境

祝您練習順利！期待看到您的學習成果！
