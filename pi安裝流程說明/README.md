# Raspberry Pi 安裝流程說明

本指南將帶你完成 Raspberry Pi 從硬體準備到系統設定的完整流程。

---

## 📋 目錄

1. [硬體準備](#硬體準備)
2. [下載作業系統映像檔](#下載作業系統映像檔)
3. [燒錄映像檔到 SD 卡](#燒錄映像檔到-sd-卡)
4. [首次開機設定](#首次開機設定)
5. [基本系統配置](#基本系統配置)
6. [網路設定](#網路設定)
7. [SSH 設定](#ssh-設定)
8. [系統更新](#系統更新)
9. [常用軟體安裝](#常用軟體安裝)
10. [故障排除](#故障排除)

---

## 硬體準備

### 必要設備

1. **Raspberry Pi 主機板**
   - 建議使用 Raspberry Pi 4 Model B（4GB 或 8GB RAM）或更新型號
   - 較舊的型號（如 Pi 3B+）也可使用，但效能較低

2. **microSD 卡**
   - 容量：至少 16GB（建議 32GB 或以上）
   - 速度：Class 10 或 UHS-I（建議使用 U3 規格，寫入速度較快）
   - 品牌推薦：SanDisk、Samsung、Kingston

3. **電源供應器**
   - Raspberry Pi 4：使用 USB-C 電源（5V/3A，15W）
   - Raspberry Pi 3 或更早：使用 micro USB 電源（5V/2.5A）
   - **重要**：請使用官方電源或品質良好的電源，電壓不穩定可能導致系統不穩定

4. **散熱裝置**（建議）
   - 散熱片或散熱風扇
   - Raspberry Pi 4 在高負載下容易過熱，強烈建議加裝散熱裝置

5. **外殼**（建議）
   - 保護主機板，防止靜電和物理損壞

### 可選設備

- 鍵盤和滑鼠（用於首次設定）
- HDMI 線和顯示器（用於首次設定）
- 有線網路線（或使用 Wi-Fi）

---

## 下載作業系統映像檔

Raspberry Pi 官方推薦使用 **Raspberry Pi OS**（基於 Debian）。

### 方法一：使用 Raspberry Pi Imager（推薦）

**Raspberry Pi Imager** 是最簡單的方式，它會自動下載並燒錄映像檔。

1. **下載 Raspberry Pi Imager**：
   - 前往 [Raspberry Pi 官網](https://www.raspberrypi.com/software/)
   - 選擇適合你作業系統的版本（Windows、macOS、Linux）
   - 下載並安裝

2. **使用 Imager 的優點**：
   - 自動下載最新版本的 Raspberry Pi OS
   - 可以在燒錄前預先設定 Wi-Fi、SSH、使用者帳號等
   - 支援多種作業系統（Raspberry Pi OS、Ubuntu、其他第三方系統）

### 方法二：手動下載映像檔

如果需要手動下載：

1. **前往下載頁面**：
   - [Raspberry Pi OS 官方下載頁](https://www.raspberrypi.com/software/operating-systems/)
   
2. **選擇版本**：
   - **Raspberry Pi OS with desktop**：包含圖形介面（適合有顯示器的使用）
   - **Raspberry Pi OS Lite**：僅命令列版本（輕量，適合伺服器用途）
   - **Raspberry Pi OS with desktop and recommended software**：完整版（包含各種預裝軟體）

3. **下載檔案**：
   - 檔案格式為 `.img.xz`（壓縮的映像檔）
   - 下載後需要解壓縮為 `.img` 檔案

---

## 燒錄映像檔到 SD 卡

### 使用 Raspberry Pi Imager（推薦）

1. **開啟 Raspberry Pi Imager**

2. **選擇作業系統**：
   - 點擊 "CHOOSE OS"
   - 選擇 "Raspberry Pi OS (recommended)" 或其他版本

3. **選擇 SD 卡**：
   - 插入 SD 卡（使用讀卡機）
   - 點擊 "CHOOSE STORAGE"
   - 選擇你的 SD 卡（**注意：選擇錯誤會格式化其他磁碟**）

4. **進階設定**（點擊左下角的齒輪圖示）：
   
   **在這個階段可以預先設定：**
   - **啟用 SSH**：勾選 "Enable SSH"，設定密碼或使用 SSH 金鑰
   - **設定 Wi-Fi**：輸入 SSID 和密碼
   - **設定主機名稱**：自訂樹莓派的名稱
   - **設定使用者名稱和密碼**：預設使用者為 `pi`，可以改為其他名稱

5. **開始燒錄**：
   - 點擊 "WRITE"
   - 確認警告訊息
   - 等待燒錄完成（通常需要 5-10 分鐘）
---

## 首次開機設定

### 如果使用 Raspberry Pi Imager 預先設定

如果你在燒錄時已經設定了 Wi-Fi、SSH、使用者帳號等，可以直接跳過此步驟，直接開機。

### 如果沒有預先設定（需要顯示器和鍵盤）

1. **插入 SD 卡**到 Raspberry Pi

2. **連接必要設備**：
   - 連接鍵盤和滑鼠
   - 連接 HDMI 顯示器
   - 連接網路線（或有 Wi-Fi）

3. **開機**：
   - 插入電源線
   - Raspberry Pi 會自動開機（電源 LED 燈會亮起）

4. **首次開機設定精靈**：
   - 系統會自動啟動設定精靈（Raspberry Pi OS Imager）
   - 依序設定：
     - **語言和地區設定**：選擇語言、時區、鍵盤配置
     - **建立使用者帳號**：設定使用者名稱和密碼（新版本不再預設 `pi` 使用者）
     - **Wi-Fi 設定**：如果使用 Wi-Fi，輸入網路 SSID 和密碼
     - **系統更新**：選擇是否立即更新系統（建議選擇「是」）
     - **啟用 SSH**：如果要用 SSH 遠端連線，建議啟用
     - **完成設定**：點擊「重新開機」

---

## 基本系統配置

### 連線到 Raspberry Pi

#### 方法一：使用 SSH（推薦，無需顯示器）

1. **確認 Raspberry Pi 的 IP 位址**：

**在樹莓派上**（如果有顯示器）：
```bash
hostname -I
```

**在路由器管理介面**：
- 登入路由器管理頁面（通常是 `192.168.1.1`）
- 查看已連接裝置列表

**使用網路ping工具**：
```bash
# macOS/Linux/Windows
ping 你的ip或hostname

```

2. **SSH 連線**：
```bash
ssh 使用者名稱@樹莓派IP位址
# 例如：ssh pi@192.168.1.100
```

3. **輸入密碼**：首次連線會詢問是否信任主機，輸入 `yes`，然後輸入密碼

#### 方法二：使用 VNC（圖形界面遠端桌面）

1. **在樹莓派上啟用 VNC**：
```bash
sudo raspi-config
# 選擇 Interfacing Options → VNC → Enable
```

2. **安裝 VNC Viewer**（在本機電腦）：
   - 下載 [RealVNC Viewer](https://www.realvnc.com/en/connect/download/viewer/)

3. **連線**：
   - 開啟 VNC Viewer
   - 輸入樹莓派的 IP 位址
   - 輸入使用者名稱和密碼

### 使用 raspi-config 進行系統設定

`raspi-config` 是 Raspberry Pi 官方提供的系統設定工具。

```bash
sudo raspi-config
```

**常用設定選項**：

1. **System Options**：
   - **Change Password**：修改使用者密碼
   - **Network at Boot**：設定開機時的網路行為
   - **Boot / Auto Login**：設定開機行為（命令列或圖形界面）

2. **Interface Options**：
   - **SSH**：啟用/停用 SSH
   - **VNC**：啟用/停用 VNC（圖形界面遠端桌面）
   - **RPi Connect** 啟用/停用 Raspberry Pi Connect(外網控制)

3. **Localisation Options**：
   - **Change Locale**：設定語言和地區
   - **Change Timezone**：設定時區
   - **Change Keyboard Layout**：設定鍵盤配置
   - **Change WiFi Country**：設定 Wi-Fi 國家代碼

4. **Advanced Options**：
   - **Expand Filesystem**：擴展檔案系統以使用整個 SD 卡（舊版本需要，新版本通常自動處理）
   - **Memory Split**：分配記憶體給 GPU（預設是 64MB，通常不需調整）

5. **完成設定後**：
   - 選擇 "Finish"
   - 系統會詢問是否重新開機，選擇 "Yes"

---

## 網路設定

**上課用途**

- 新增手機熱點
- 新增Dongle wifi熱點
- 新增家中wifi熱點
---

## SSH 設定

### 啟用 SSH

**方法一：使用 raspi-config**：
```bash
sudo raspi-config
# Interfacing Options → SSH → Enable
```

---

## 系統更新

安裝完成後，建議立即更新系統：

1. **更新套件列表**：
```bash
sudo apt update
```

2. **升級已安裝的套件**：
```bash
sudo apt upgrade -y
```

3. **清理不需要的套件**（可選）：
```bash
sudo apt autoremove -y
sudo apt autoclean
```

4. **更新韌體**（可選）：
```bash
sudo rpi-update
```

---

## 常用軟體安裝

### 基本工具

```bash
# Git（版本控制）
sudo apt install git -y

# Vim（文字編輯器）
sudo apt install vim -y

# htop（進程監控工具）
sudo apt install htop -y

# curl 和 wget（下載工具，通常已預裝）
sudo apt install curl wget -y
```

### 開發環境

```bash
# Python 3（通常已預裝）
sudo apt install python3 python3-pip -y

# Node.js 和 npm（使用 NodeSource 安裝最新版本）
# NodeSource 的通用 'lts' 腳本已停用，請指定主版本號。
# 例如，使用 20.x (目前的 LTS 版本)。您可以將 "20.x" 替換為其他版本，例如 "18.x"。
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 或使用預設版本
sudo apt install nodejs npm -y
```

### 網頁伺服器

```bash
# Nginx（網頁伺服器）
sudo apt install nginx -y

# Apache（替代選項）
sudo apt install apache2 -y
```

### 資料庫

```bash
# MySQL
sudo apt install mysql-server -y

# PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# SQLite（通常已預裝）
```

---

## 故障排除

### 無法開機

1. **檢查電源**：
   - 確認電源供應器規格正確（5V，足夠的電流）
   - 檢查電源 LED 燈是否亮起
   - 嘗試更換電源線

2. **檢查 SD 卡**：
   - 確認 SD 卡已正確插入
   - 確認映像檔燒錄成功
   - 嘗試使用不同的 SD 卡

3. **檢查顯示器**：
   - 確認 HDMI 線連接正確
   - 嘗試不同的 HDMI 端口（Raspberry Pi 4 有兩個）
   - 確認顯示器已開機

### 無法連線網路

1. **檢查網路線**（有線網路）：
   - 確認網路線連接正確
   - 確認路由器端口正常

2. **檢查 Wi-Fi 設定**：
   - 確認 SSID 和密碼正確
   - 檢查 Wi-Fi 國家代碼設定：`sudo raspi-config` → Localisation Options → Change WiFi Country

3. **查看網路介面狀態**：
```bash
ifconfig
# 或
ip addr show
```

4. **重新啟動網路服務**：
```bash
sudo systemctl restart networking
```

### 無法 SSH 連線

1. **確認 SSH 已啟用**：
```bash
sudo systemctl status ssh
```

2. **檢查防火牆**（如果有設定）：
```bash
sudo ufw status
```

3. **確認 IP 位址正確**：
```bash
hostname -I
```

4. **檢查 SSH 服務是否監聽**：
```bash
sudo netstat -tlnp | grep ssh
```

### SD 卡空間不足

1. **清理套件快取**：
```bash
sudo apt clean
sudo apt autoremove -y
```

2. **擴展檔案系統**（如果沒有自動擴展）：
```bash
sudo raspi-config
# Advanced Options → Expand Filesystem
```

3. **檢查磁碟使用情況**：
```bash
df -h
```

### 系統過熱

1. **檢查溫度**：
```bash
vcgencmd measure_temp
```

2. **降溫措施**：
   - 加裝散熱片或散熱風扇
   - 改善通風環境
   - 降低 CPU 頻率（臨時措施）：
```bash
sudo nano /boot/config.txt
# 加入：arm_freq=1200（降低頻率）
```

---
