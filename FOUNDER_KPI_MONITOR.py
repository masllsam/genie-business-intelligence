#!/usr/bin/env python3
"""
===============================================================================
GENIE BUSINESS INTELLIGENCE — FOUNDER KPI MONITOR & EXECUTIVE CONTROL PLANE
===============================================================================
Author: Genie Autonomous Systems / Founder Business Intelligence
Target: Oracle Cloud Infrastructure ARM64 / Multi-Tenant Agent Ecosystem
Jurisdiction: Vienna / Lower Austria (EU)

Description:
  Real-time executive monitoring suite that interfaces with:
    1. Local PostgreSQL Database (ironclaw_tenant / dare_game_db)
    2. OpenRouter LLM API Gateway (Live token consumption, limits & balance)
    3. Host Operating System Metrics (CPU, RAM, NVMe Disk, Uptime, PM2, Docker)
    4. Financial Engine (MRR, ARR, ARPU, Gross Margins 76%-92%, Daily Profit Run-Rate)

Usage:
  python3 FOUNDER_KPI_MONITOR.py          # Full interactive terminal dashboard
  python3 FOUNDER_KPI_MONITOR.py --json   # Machine-readable JSON output for webhooks/cron
  python3 FOUNDER_KPI_MONITOR.py --check  # Health check mode (Exit code 0=Healthy, 1=Degraded)
===============================================================================
"""

import sys
import os
import json
import time
import shutil
import subprocess
import datetime
import urllib.request
import urllib.error

# -----------------------------------------------------------------------------
# CONSTANTS & CONFIGURATION
# -----------------------------------------------------------------------------
DB_NAME = "ironclaw_tenant"
FIXED_INFRA_COST_MONTHLY_USD = 45.00  # Base infrastructure, domain, SSL & backup storage
EUR_USD_EXCHANGE_RATE = 1.085         # Reference rate: 1 EUR = ~1.085 USD

# ANSI Color Codes
CLR_RESET = "\033[0m"
CLR_BOLD = "\033[1m"
CLR_DIM = "\033[2m"
CLR_CYAN = "\033[36m"
CLR_GREEN = "\033[32m"
CLR_YELLOW = "\033[33m"
CLR_RED = "\033[31m"
CLR_MAGENTA = "\033[35m"
CLR_BLUE = "\033[34m"
CLR_BG_DARK = "\033[40m"
CLR_WHITE_BOLD = "\033[1;37m"

def load_openrouter_key():
    """Extracts OpenRouter key from environment or system .env paths."""
    key = os.environ.get("OPENROUTER_API_KEY")
    if key and key.startswith("sk-or-v1-"):
        return key

    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_paths = [
        os.path.join(script_dir, ".env"),
        "/home/opc/genie-business-intelligence/.env",
        "/home/opc/ironclaw/.env",
        "/home/opc/ironclaw/control_plane/.env",
        "/home/opc/dorotheum-web/.env"
    ]
    for path in env_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("OPENROUTER_API_KEY=") and not line.startswith("#"):
                            val = line.split("=", 1)[1].strip().strip('"').strip("'")
                            if val.startswith("sk-or-v1-"):
                                return val
            except Exception:
                pass
    return None

def execute_psql_query(query, database=DB_NAME):
    """Executes a PostgreSQL query via psql subprocess returning stdout."""
    cmds = [
        ["psql", "-d", database, "-t", "-A", "-c", query],
        ["sudo", "-u", "postgres", "psql", "-d", database, "-t", "-A", "-c", query]
    ]
    for cmd in cmds:
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=4, universal_newlines=True)
            if res.returncode == 0:
                return res.stdout.strip()
        except Exception:
            continue
    return None

def fetch_openrouter_metrics(api_key):
    """Queries OpenRouter API for live usage, credits, and rate limits."""
    if not api_key:
        return {"error": "OPENROUTER_API_KEY not configured"}

    url = "https://openrouter.ai/api/v1/auth/key"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": "Bearer {}".format(api_key),
            "User-Agent": "Genie-Founder-BI/1.0",
            "Accept": "application/json"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.getcode() == 200:
                data = json.loads(response.read().decode("utf-8"))
                return data.get("data", {})
    except Exception as e:
        return {"error": str(e)}
    return {}

def fetch_system_metrics():
    """Collects host server operating system metrics."""
    metrics = {
        "uptime": "Unknown",
        "load_1m": 0.0,
        "load_5m": 0.0,
        "load_15m": 0.0,
        "ram_total_mb": 0,
        "ram_used_mb": 0,
        "ram_pct": 0.0,
        "disk_total_gb": 0.0,
        "disk_used_gb": 0.0,
        "disk_free_gb": 0.0,
        "disk_pct": 0.0,
        "services": {}
    }

    # Uptime & Load
    try:
        res = subprocess.run(["uptime", "-p"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if res.returncode == 0:
            metrics["uptime"] = res.stdout.strip()
    except Exception:
        pass

    try:
        load = os.getloadavg()
        metrics["load_1m"] = round(load[0], 2)
        metrics["load_5m"] = round(load[1], 2)
        metrics["load_15m"] = round(load[2], 2)
    except Exception:
        pass

    # RAM
    try:
        with open("/proc/meminfo", "r") as f:
            mem = {}
            for line in f:
                parts = line.split(":")
                if len(parts) == 2:
                    mem[parts[0].strip()] = int(parts[1].strip().split()[0])
            total_kb = mem.get("MemTotal", 0)
            avail_kb = mem.get("MemAvailable", 0)
            used_kb = total_kb - avail_kb
            if total_kb > 0:
                metrics["ram_total_mb"] = round(total_kb / 1024, 1)
                metrics["ram_used_mb"] = round(used_kb / 1024, 1)
                metrics["ram_pct"] = round((used_kb / total_kb) * 100.0, 1)
    except Exception:
        pass

    # Disk
    try:
        disk = shutil.disk_usage("/")
        metrics["disk_total_gb"] = round(disk.total / (1024**3), 1)
        metrics["disk_used_gb"] = round(disk.used / (1024**3), 1)
        metrics["disk_free_gb"] = round(disk.free / (1024**3), 1)
        metrics["disk_pct"] = round((disk.used / disk.total) * 100.0, 1)
    except Exception:
        pass

    # Services Health Check
    for svc in ["postgresql", "docker", "nginx"]:
        try:
            res = subprocess.run(["systemctl", "is-active", svc], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            metrics["services"][svc] = (res.stdout.strip() == "active")
        except Exception:
            metrics["services"][svc] = False

    # PM2 Process Check
    try:
        res_pm2 = subprocess.run(["pm2", "ping"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        pm2_active = "pong" in res_pm2.stdout.lower() or res_pm2.returncode == 0
        if not pm2_active:
            res_pgrep = subprocess.run(["pgrep", "-f", "PM2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pm2_active = (res_pgrep.returncode == 0)
        metrics["services"]["pm2"] = pm2_active
    except Exception:
        metrics["services"]["pm2"] = False

    return metrics

def fetch_database_kpis():
    """Queries PostgreSQL database for tenant subscriptions, plans, and usage logs."""
    kpis = {
        "db_connected": False,
        "total_tenants": 0,
        "total_subscribers": 0,
        "active_subscribers": 0,
        "tier_counts": {"free": 0, "starter": 0, "pro": 0, "enterprise": 0, "other": 0},
        "mrr_usd": 0.0,
        "arr_usd": 0.0,
        "total_tokens_in": 0,
        "total_tokens_out": 0,
        "total_usage_cost_usd": 0.0,
        "plans": []
    }

    # Verify connection & fetch plans
    plans_raw = execute_psql_query("SELECT id, name, price_cents, daily_quota, max_agents FROM plans ORDER BY price_cents ASC;")
    if plans_raw is not None:
        kpis["db_connected"] = True
        plan_prices = {}
        for line in plans_raw.splitlines():
            if line and "|" in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 3:
                    p_id = parts[0]
                    p_name = parts[1]
                    try:
                        p_price = int(parts[2]) / 100.0
                    except ValueError:
                        p_price = 0.0
                    p_quota = parts[3] if len(parts) > 3 else "N/A"
                    p_agents = parts[4] if len(parts) > 4 else "N/A"
                    plan_prices[p_id] = p_price
                    kpis["plans"].append({
                        "id": p_id,
                        "name": p_name,
                        "price_usd": p_price,
                        "daily_quota": p_quota,
                        "max_agents": p_agents
                    })

        # Count tenants
        tenants_raw = execute_psql_query("SELECT count(*) FROM tenants;")
        if tenants_raw and tenants_raw.isdigit():
            kpis["total_tenants"] = int(tenants_raw)

        # Count subscriptions by plan and status
        subs_raw = execute_psql_query("SELECT plan_id, status, count(*) FROM subscriptions GROUP BY plan_id, status;")
        if subs_raw:
            for line in subs_raw.splitlines():
                if line and "|" in line:
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) == 3:
                        p_id, status, cnt_str = parts[0], parts[1], parts[2]
                        cnt = int(cnt_str) if cnt_str.isdigit() else 0
                        kpis["total_subscribers"] += cnt
                        if status in ["active", "trialing"]:
                            kpis["active_subscribers"] += cnt
                            if p_id in kpis["tier_counts"]:
                                kpis["tier_counts"][p_id] += cnt
                            else:
                                kpis["tier_counts"]["other"] += cnt
                            # Add to MRR
                            price = plan_prices.get(p_id, 0.0)
                            kpis["mrr_usd"] += price * cnt

        kpis["arr_usd"] = kpis["mrr_usd"] * 12.0

        # Token Usage Logs
        usage_raw = execute_psql_query("SELECT COALESCE(SUM(tokens_in),0), COALESCE(SUM(tokens_out),0), COALESCE(SUM(cost_usd),0) FROM usage_log;")
        if usage_raw and "|" in usage_raw:
            parts = [p.strip() for p in usage_raw.split("|")]
            if len(parts) == 3:
                try:
                    kpis["total_tokens_in"] = int(parts[0])
                    kpis["total_tokens_out"] = int(parts[1])
                    kpis["total_usage_cost_usd"] = float(parts[2])
                except (ValueError, TypeError):
                    pass

    return kpis

def format_progress_bar(pct, width=20):
    """Renders a simple ASCII progress bar."""
    pct = max(0.0, min(100.0, pct))
    filled = int(round((pct / 100.0) * width))
    bar = "█" * filled + "░" * (width - filled)
    return bar

def compute_executive_financials(db_kpis, or_metrics):
    """Synthesizes high-level unit economics and profit margins."""
    mrr = db_kpis.get("mrr_usd", 0.0)
    arr = db_kpis.get("arr_usd", 0.0)
    active_subs = db_kpis.get("active_subscribers", 0)

    # OpenRouter actual monthly cost
    or_monthly_cost = or_metrics.get("usage_monthly", 0.0) or 0.0
    or_daily_cost = or_metrics.get("usage_daily", 0.0) or 0.0

    # Blended Monthly COGS = OpenRouter monthly usage + Payment Processing (~3.2%) + Fixed Infra
    payment_fees = mrr * 0.032
    total_cogs = or_monthly_cost + payment_fees + FIXED_INFRA_COST_MONTHLY_USD
    gross_profit_usd = max(0.0, mrr - (or_monthly_cost + payment_fees))
    net_profit_usd = mrr - total_cogs

    gross_margin_pct = (gross_profit_usd / mrr * 100.0) if mrr > 0 else 84.5  # Model baseline if fresh DB
    arpu = (mrr / active_subs) if active_subs > 0 else 0.0
    daily_profit_run_rate = (mrr / 30.0) - (or_daily_cost + (FIXED_INFRA_COST_MONTHLY_USD / 30.0))

    return {
        "mrr_usd": round(mrr, 2),
        "mrr_eur": round(mrr / EUR_USD_EXCHANGE_RATE, 2),
        "arr_usd": round(arr, 2),
        "arr_eur": round(arr / EUR_USD_EXCHANGE_RATE, 2),
        "arpu_usd": round(arpu, 2),
        "or_monthly_cost_usd": round(or_monthly_cost, 4),
        "or_daily_cost_usd": round(or_daily_cost, 4),
        "fixed_infra_monthly_usd": FIXED_INFRA_COST_MONTHLY_USD,
        "total_cogs_usd": round(total_cogs, 2),
        "gross_profit_usd": round(gross_profit_usd, 2),
        "net_profit_usd": round(net_profit_usd, 2),
        "gross_margin_pct": round(gross_margin_pct, 1),
        "daily_profit_run_rate_usd": round(daily_profit_run_rate, 2),
        "break_even_subscribers_needed": max(1, int(round(FIXED_INFRA_COST_MONTHLY_USD / 29.99)))
    }

def print_dashboard(db_kpis, or_metrics, sys_metrics, financials):
    """Renders the executive terminal control dashboard."""
    now_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    print("\n" + CLR_WHITE_BOLD + "╔" + "═"*76 + "╗" + CLR_RESET)
    print(CLR_WHITE_BOLD + "║" + CLR_CYAN + "   GENIE AUTONOMOUS PLATFORM — FOUNDER BUSINESS INTELLIGENCE DASHBOARD   " + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "║" + CLR_DIM + f"   System Timestamp: {now_str:<32} Oracle ARM64 (Vienna)   " + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "╠" + "═"*76 + "╣" + CLR_RESET)

    # 1. REVENUE & SUBSCRIBER KPIs
    print(CLR_WHITE_BOLD + "║" + CLR_YELLOW + " ▌ FINANCIAL REVENUE & ACTIVE SUBSCRIBER METRICS (MRR / ARR)" + " "*17 + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "╟" + "─"*76 + "╢" + CLR_RESET)
    
    mrr_usd = financials["mrr_usd"]
    mrr_eur = financials["mrr_eur"]
    arr_usd = financials["arr_usd"]
    arpu = financials["arpu_usd"]
    active = db_kpis["active_subscribers"]
    total_tenants = db_kpis["total_tenants"]

    print(CLR_WHITE_BOLD + "║" + f"   Monthly Recurring Rev (MRR):  " + CLR_GREEN + f"${mrr_usd:>8.2f} USD" + CLR_RESET + f"  ({mrr_eur:>8.2f} EUR)" + " "*18 + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "║" + f"   Annual Recurring Rev (ARR):   " + CLR_GREEN + f"${arr_usd:>8.2f} USD" + CLR_RESET + f"  ({financials['arr_eur']:>8.2f} EUR)" + " "*18 + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "║" + f"   Average Revenue / User (ARPU):" + CLR_CYAN + f"${arpu:>8.2f} USD" + CLR_RESET + f"  (Active Subs: {active:>3} / Tenants: {total_tenants:<3})" + " "*11 + CLR_WHITE_BOLD + "║" + CLR_RESET)

    # Tier breakdown
    tc = db_kpis["tier_counts"]
    tiers_str = f"Starter: {tc['starter']} | Pro: {tc['pro']} | Enterprise: {tc['enterprise']} | Free: {tc['free']}"
    print(CLR_WHITE_BOLD + "║" + f"   Tier Distribution:            " + CLR_MAGENTA + f"{tiers_str:<45}" + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "╠" + "═"*76 + "╣" + CLR_RESET)

    # 2. UNIT ECONOMICS & PROFIT MARGINS
    print(CLR_WHITE_BOLD + "║" + CLR_YELLOW + " ▌ UNIT TOKEN ECONOMICS & MARGIN CONTROL PLANE" + " "*31 + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "╟" + "─"*76 + "╢" + CLR_RESET)

    gm_pct = financials["gross_margin_pct"]
    gm_color = CLR_GREEN if gm_pct >= 76.0 else (CLR_YELLOW if gm_pct >= 50.0 else CLR_RED)
    gm_bar = format_progress_bar(gm_pct, width=15)
    
    print(CLR_WHITE_BOLD + "║" + f"   Target SaaS Gross Margin:     " + CLR_CYAN + "76.0% - 92.4%" + CLR_RESET + f" (Smart routing + Gemini Flash)" + " "*6 + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "║" + f"   Live Realized Gross Margin:   " + gm_color + f"{gm_pct:>5.1f}% [{gm_bar}]" + CLR_RESET + " "*28 + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "║" + f"   Daily Profit Run-Rate:        " + CLR_GREEN + f"${financials['daily_profit_run_rate_usd']:>8.2f} / day" + CLR_RESET + " "*35 + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "║" + f"   Fixed Overhead (Oracle+Infra):" + CLR_DIM + f"${financials['fixed_infra_monthly_usd']:>8.2f} / mo" + CLR_RESET + f"  (Break-even: {financials['break_even_subscribers_needed']} Pro subs)" + " "*11 + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "╠" + "═"*76 + "╣" + CLR_RESET)

    # 3. OPENROUTER LLM GATEWAY METRICS
    print(CLR_WHITE_BOLD + "║" + CLR_YELLOW + " ▌ OPENROUTER API GATEWAY & TOKEN INGESTION" + " "*34 + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "╟" + "─"*76 + "╢" + CLR_RESET)

    or_limit = or_metrics.get("limit", 0) or 0
    or_rem = or_metrics.get("limit_remaining", 0) or 0
    or_use_mo = or_metrics.get("usage_monthly", 0) or 0
    or_use_day = or_metrics.get("usage_daily", 0) or 0
    key_label = or_metrics.get("label", "Configured via .env")

    print(CLR_WHITE_BOLD + "║" + f"   Key / Account Profile:        " + CLR_CYAN + f"{key_label:<45}" + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "║" + f"   Credit Balance / Limit:       " + CLR_GREEN + f"${or_rem:>6.2f} remaining" + CLR_RESET + f" of ${or_limit:.2f} limit" + " "*21 + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "║" + f"   Token Spend Today / Month:    " + CLR_YELLOW + f"${or_use_day:>6.4f} (Today)" + CLR_RESET + f" | ${or_use_mo:.4f} (30d)" + " "*17 + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "║" + f"   Database Token Logs:          " + CLR_DIM + f"{db_kpis['total_tokens_in']:,} In | {db_kpis['total_tokens_out']:,} Out" + CLR_RESET + " "*21 + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "╠" + "═"*76 + "╣" + CLR_RESET)

    # 4. INFRASTRUCTURE HEALTH & UPTIME SLA
    print(CLR_WHITE_BOLD + "║" + CLR_YELLOW + " ▌ HOST HARDWARE & SLA AVAILABILITY MONITOR (99.9% TARGET)" + " "*18 + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "╟" + "─"*76 + "╢" + CLR_RESET)

    uptime_str = sys_metrics["uptime"]
    load_str = f"{sys_metrics['load_1m']}, {sys_metrics['load_5m']}, {sys_metrics['load_15m']}"
    ram_str = f"{sys_metrics['ram_used_mb']} MB / {sys_metrics['ram_total_mb']} MB ({sys_metrics['ram_pct']}%)"
    disk_str = f"{sys_metrics['disk_used_gb']} GB / {sys_metrics['disk_total_gb']} GB ({sys_metrics['disk_pct']}%)"

    print(CLR_WHITE_BOLD + "║" + f"   Host Node Uptime:             " + CLR_GREEN + f"{uptime_str:<45}" + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "║" + f"   CPU Load Avg (1m, 5m, 15m):   " + CLR_CYAN + f"{load_str:<45}" + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "║" + f"   RAM Utilization:              " + CLR_CYAN + f"{ram_str:<45}" + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "║" + f"   NVMe Disk Storage:            " + CLR_CYAN + f"{disk_str:<45}" + CLR_WHITE_BOLD + "║" + CLR_RESET)

    svcs = sys_metrics["services"]
    svc_status_line = " ".join([
        (CLR_GREEN + f"[{s.upper()}: OK]" if active else CLR_RED + f"[{s.upper()}: OFF]") + CLR_RESET
        for s, active in svcs.items()
    ])
    print(CLR_WHITE_BOLD + "║" + f"   Core Daemon Probes:           " + f"{svc_status_line:<54}" + CLR_WHITE_BOLD + "║" + CLR_RESET)
    print(CLR_WHITE_BOLD + "╚" + "═"*76 + "╝\n" + CLR_RESET)

def main():
    json_mode = "--json" in sys.argv
    check_mode = "--check" in sys.argv or "--alert" in sys.argv

    # Gather data
    or_key = load_openrouter_key()
    or_metrics = fetch_openrouter_metrics(or_key)
    sys_metrics = fetch_system_metrics()
    db_kpis = fetch_database_kpis()
    financials = compute_executive_financials(db_kpis, or_metrics)

    payload = {
        "timestamp_utc": datetime.datetime.utcnow().isoformat() + "Z",
        "financials": financials,
        "database_kpis": db_kpis,
        "openrouter_gateway": or_metrics,
        "system_metrics": sys_metrics,
        "status": "HEALTHY" if sys_metrics["services"].get("postgresql", False) else "DEGRADED"
    }

    if json_mode:
        print(json.dumps(payload, indent=2))
        return 0

    if check_mode:
        healthy = (
            sys_metrics["services"].get("postgresql", False) and
            db_kpis["db_connected"] and
            "error" not in or_metrics
        )
        if healthy:
            print("[HEALTH CHECK PASSED] All Genie BI subsystems operational.")
            return 0
        else:
            print("[HEALTH CHECK FAILED] One or more core subsystems degraded.")
            return 1

    # Default: Interactive Dashboard
    print_dashboard(db_kpis, or_metrics, sys_metrics, financials)
    return 0

if __name__ == "__main__":
    sys.exit(main())
