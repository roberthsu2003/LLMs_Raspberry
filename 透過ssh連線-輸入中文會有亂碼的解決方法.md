# 透過ssh連線,輸入中文會有亂碼的解決方法

1. 編輯 locale 設定檔：

```bash
sudo nano /etc/default/locale
```

2. 將內容改為：

```bash
LANG=zh_TW.UTF-8
LC_ALL=zh_TW.UTF-8
LC_CTYPE=zh_TW.UTF-8
```
