"""
COVID-19 世界資料 MCP Server

連接 PostgreSQL 的 world 資料表，提供疫情查詢功能。
欄位為繁體中文（國家、日期、總確診數、總死亡數、解除隔離數等）。
"""

import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Postgres 的 COVID-19 world 資料")

# ========== 資料表結構設定（依 list_table_columns 實際欄位）==========
SCHEMA = {
    "table": "world",
    "country": "國家",
    "date": "日期",
    "confirmed": "總確診數",
    "deaths": "總死亡數",
    "recovered": "解除隔離數",
}


def _q(name: str) -> str:
    """PostgreSQL 識別符加雙引號（繁體中文欄位必須）"""
    return f'"{name}"'


def get_connection():
    """
    取得 PostgreSQL 連線。使用環境變數 DATABASE_URI。
    - Docker 內：compose 設定 postgres:5432（同一網路）
    - 本機測試：需設定 DATABASE_URI，例如 postgresql://pi:raspberry@<樹莓派IP>:5432/mydb
    """
    uri = os.environ.get(
        "DATABASE_URI",
        "postgresql://pi:raspberry@10.170.1.218:5432/mydb",
    )
    return psycopg2.connect(uri)


@contextmanager
def get_cursor():
    """取得資料庫游標的 context manager。"""
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            yield cur
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@mcp.tool()
def get_covid_by_country(country_name: str, limit: int = 10) -> str:
    """
    查詢指定國家或地區的 COVID-19 疫情數據，依日期由新到舊排序。
    參數 country_name: 國家/地區名稱（如 台灣、美國、日本、歐洲）
    參數 limit: 回傳筆數，預設 10
    """
    tq = _q(SCHEMA["table"])
    col_country = SCHEMA["country"]
    col_date = SCHEMA["date"]
    col_confirmed = SCHEMA["confirmed"]
    col_deaths = SCHEMA["deaths"]
    col_recovered = SCHEMA.get("recovered")

    cols = f"{_q(col_country)}, {_q(col_date)}, {_q(col_confirmed)}, {_q(col_deaths)}"
    if col_recovered:
        cols += f", {_q(col_recovered)}"

    try:
        with get_cursor() as cur:
            cur.execute(
                f"""
                SELECT {cols}
                FROM {tq}
                WHERE {_q(col_country)} ILIKE %s
                ORDER BY {_q(col_date)} DESC
                LIMIT %s
                """,
                (f"%{country_name}%", limit),
            )
            rows = cur.fetchall()
    except Exception as e:
        return f"查詢失敗: {e}"

    if not rows:
        return f"找不到國家「{country_name}」的資料"

    lines = [f"國家: {country_name} | 共 {len(rows)} 筆\n"]
    for r in rows:
        line = f"  日期: {r[col_date]} | 確診: {r[col_confirmed]} | 死亡: {r[col_deaths]}"
        if col_recovered and r.get(col_recovered) is not None:
            line += f" | 康復: {r[col_recovered]}"
        lines.append(line)
    return "\n".join(lines)


@mcp.tool()
def get_covid_by_date(date_str: str) -> str:
    """
    查詢指定日期的全球 COVID-19 疫情摘要（前 20 國依確診數排序）。
    參數 date_str: 日期，格式 YYYY-MM-DD（如 2022-04-18）
    """
    tq = _q(SCHEMA["table"])
    col_country = SCHEMA["country"]
    col_date = SCHEMA["date"]
    col_confirmed = SCHEMA["confirmed"]
    col_deaths = SCHEMA["deaths"]

    try:
        with get_cursor() as cur:
            cur.execute(
                f"""
                SELECT {_q(col_country)}, {_q(col_confirmed)}, {_q(col_deaths)}
                FROM {tq}
                WHERE {_q(col_date)}::text = %s
                ORDER BY {_q(col_confirmed)} DESC
                LIMIT 20
                """,
                (date_str,),
            )
            rows = cur.fetchall()
    except Exception as e:
        return f"查詢失敗: {e}"

    if not rows:
        return f"找不到日期 {date_str} 的資料"

    total_confirmed = sum(r[col_confirmed] or 0 for r in rows)
    total_deaths = sum(r[col_deaths] or 0 for r in rows)

    lines = [f"日期: {date_str} | 前 20 國確診總和: {total_confirmed} | 死亡總和: {total_deaths}\n"]
    for r in rows:
        lines.append(f"  {r[col_country]}: 確診 {r[col_confirmed]} | 死亡 {r[col_deaths]}")
    return "\n".join(lines)


@mcp.tool()
def get_top_countries(metric: str = "confirmed", limit: int = 10) -> str:
    """
    查詢確診或死亡數最高的國家/地區（取最新日期的資料，含全球、洲別）。
    參數 metric: 排序依據，'confirmed'（總確診數）或 'deaths'（總死亡數）
    參數 limit: 回傳筆數，預設 10
    """
    if metric not in ("confirmed", "deaths"):
        return "metric 請填 'confirmed' 或 'deaths'"

    tq = _q(SCHEMA["table"])
    col_country = SCHEMA["country"]
    col_date = SCHEMA["date"]
    col_confirmed = SCHEMA["confirmed"]
    col_deaths = SCHEMA["deaths"]
    order_col = col_confirmed if metric == "confirmed" else col_deaths

    try:
        with get_cursor() as cur:
            cur.execute(
                f"""
                WITH latest AS (
                    SELECT MAX({_q(col_date)}) as max_date FROM {tq}
                )
                SELECT {_q(col_country)}, {_q(col_confirmed)}, {_q(col_deaths)}
                FROM {tq}, latest
                WHERE {tq}.{_q(col_date)} = latest.max_date
                ORDER BY {_q(order_col)} DESC NULLS LAST
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()
    except Exception as e:
        return f"查詢失敗: {e}"

    if not rows:
        return "查無資料"

    label = "確診數" if metric == "confirmed" else "死亡數"
    lines = [f"全球 {label} 前 {limit} 名國家:\n"]
    for i, r in enumerate(rows, 1):
        val = r[order_col] or 0
        lines.append(f"  {i}. {r[col_country]}: {val:,}")
    return "\n".join(lines)


@mcp.tool()
def get_covid_summary() -> str:
    """
    取得 COVID-19 world 資料庫的整體摘要：總筆數、國家/地區數、日期範圍、最新日期的全球確診與死亡總和。
    """
    tq = _q(SCHEMA["table"])
    col_country = SCHEMA["country"]
    col_date = SCHEMA["date"]
    col_confirmed = SCHEMA["confirmed"]
    col_deaths = SCHEMA["deaths"]

    try:
        with get_cursor() as cur:
            cur.execute(f"SELECT COUNT(*) as cnt FROM {tq}")
            total = cur.fetchone()["cnt"]

            cur.execute(f"SELECT COUNT(DISTINCT {_q(col_country)}) as cnt FROM {tq}")
            countries = cur.fetchone()["cnt"]

            cur.execute(f"SELECT MIN({_q(col_date)}) as min_d, MAX({_q(col_date)}) as max_d FROM {tq}")
            row = cur.fetchone()
            min_date = row["min_d"]
            max_date = row["max_d"]

            # 最新日期的全球確診與死亡總和
            cur.execute(
                f"""
                SELECT COALESCE(SUM({_q(col_confirmed)}), 0) as tc, COALESCE(SUM({_q(col_deaths)}), 0) as td
                FROM {tq}
                WHERE {_q(col_date)} = (SELECT MAX({_q(col_date)}) FROM {tq})
                """
            )
            agg = cur.fetchone()
            total_confirmed = agg["tc"] or 0
            total_deaths = agg["td"] or 0
    except Exception as e:
        return f"查詢失敗: {e}"

    return (
        f"COVID-19 world 資料摘要:\n"
        f"  總筆數: {total:,}\n"
        f"  國家數: {countries}\n"
        f"  日期範圍: {min_date} ~ {max_date}\n"
        f"  最新日期全球確診總和: {total_confirmed:,}\n"
        f"  最新日期全球死亡總和: {total_deaths:,}"
    )


@mcp.tool()
def list_table_columns() -> str:
    """
    列出 world 資料表的所有欄位名稱與型別，供確認 schema 或除錯用。
    """
    try:
        with get_cursor() as cur:
            cur.execute(
                """
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position
                """,
                (SCHEMA["table"],),
            )
            rows = cur.fetchall()
    except Exception as e:
        return f"查詢失敗: {e}"

    if not rows:
        return f"找不到資料表「{SCHEMA['table']}」，請檢查 SCHEMA 設定"

    lines = [f"資料表 {SCHEMA['table']} 的欄位:\n"]
    for r in rows:
        lines.append(f"  - {r['column_name']}: {r['data_type']}")
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
