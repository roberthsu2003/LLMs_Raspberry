"""
測試 tools.py 的 COVID-19 MCP 工具是否正常執行。

執行方式（擇一）：
  1. Docker 內（推薦）：docker compose up -d postgres && docker compose run --rm postgres-mcp python tools_test.py
  2. 本機測試：PostgreSQL 在樹莓派 Docker 內，需設定 DATABASE_URI=postgresql://pi:raspberry@<樹莓派IP>:5432/mydb

僅檢查欄位：python tools_test.py --schema-only
"""

import sys

# 僅檢查 schema 模式
if len(sys.argv) > 1 and sys.argv[1] == "--schema-only":
    from tools import list_table_columns
    print("world 資料表欄位清單（請依此更新 tools.py 的 SCHEMA）：\n")
    print(list_table_columns())
    sys.exit(0)

# 測試 1：匯入模組
print("=" * 50)
print("測試 1：匯入 tools 模組")
print("=" * 50)
try:
    from tools import (
        _q,
        get_covid_by_country,
        get_covid_by_date,
        get_top_countries,
        get_covid_summary,
        list_table_columns,
        SCHEMA,
    )
    print("✓ 匯入成功\n")
except ImportError as e:
    print(f"✗ 匯入失敗: {e}")
    sys.exit(1)

# 測試 2：_q() 輔助函數（不需資料庫）
print("=" * 50)
print("測試 2：_q() 識別符加引號")
print("=" * 50)
assert _q("國家") == '"國家"', f"預期 '\"國家\"'，得到 {_q('國家')!r}"
assert _q("world") == '"world"', f"預期 '\"world\"'，得到 {_q('world')!r}"
print("✓ _q() 正常\n")

# 測試 3～7：呼叫各工具（需資料庫連線）
print("=" * 50)
print("測試 3～7：呼叫 MCP 工具（需 PostgreSQL）")
print("=" * 50)

tests = [
    ("list_table_columns", lambda: list_table_columns(), "列出資料表欄位"),
    ("get_covid_summary", lambda: get_covid_summary(), "取得資料摘要"),
    ("get_covid_by_country", lambda: get_covid_by_country("台灣", limit=3), "查詢台灣疫情"),
    ("get_covid_by_date", lambda: get_covid_by_date("2024-01-15"), "查詢指定日期"),
    ("get_top_countries", lambda: get_top_countries("confirmed", limit=5), "查詢確診前 5 名"),
]

all_ok = True
for name, fn, desc in tests:
    try:
        result = fn()
        # 若回傳「查詢失敗」表示資料庫連線或查詢有問題
        if "查詢失敗" in str(result):
            print(f"✗ {name}: {desc}")
            print(f"  資料庫錯誤: {result[:150]}...")
            all_ok = False
            # 若為 schema 錯誤，提示檢查 list_table_columns 的完整輸出
            if "does not exist" in result and name != "list_table_columns":
                print(f"\n  >>> 欄位不符，請查看上方 list_table_columns 的完整欄位清單，並更新 tools.py 的 SCHEMA <<<\n")
        else:
            print(f"✓ {name}: {desc}")
            # list_table_columns 成功時顯示完整欄位（供對照 SCHEMA）
            if name == "list_table_columns":
                print(result)
            else:
                preview = str(result)[:100].replace("\n", " ")
                print(f"  結果預覽: {preview}...")
    except Exception as e:
        print(f"✗ {name}: {desc}")
        print(f"  錯誤: {e}")
        all_ok = False
    print()

# 測試 8：get_top_countries 參數驗證
print("=" * 50)
print("測試 8：get_top_countries 無效參數")
print("=" * 50)
try:
    result = get_top_countries(metric="invalid")
    assert "metric 請填" in result, f"預期錯誤訊息，得到: {result}"
    print("✓ 無效 metric 正確回傳錯誤訊息\n")
except Exception as e:
    print(f"✗ 未預期錯誤: {e}\n")
    all_ok = False

# 總結
print("=" * 50)
if all_ok:
    print("✓ 所有測試通過")
else:
    print("✗ 部分測試失敗（可能是資料庫未連線或 world 表不存在）")
    print("  請確認：")
    print("  1. 推薦在 Docker 內測試：docker compose run --rm postgres-mcp python tools_test.py")
    print("  2. 本機測試（PostgreSQL 在樹莓派）：DATABASE_URI=postgresql://pi:raspberry@<樹莓派IP>:5432/mydb python tools_test.py")
    print("  3. 已建立 world 資料表並匯入 COVID-19 資料")
    sys.exit(1)
