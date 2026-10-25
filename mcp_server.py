import sys, json
from client import AgenticPricingDiscountWaterfallAuditorClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    auditor = AgenticPricingDiscountWaterfallAuditorClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "genpark-agentic-pricing-discount-waterfall-auditor-skill"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    list_p = float(req.get("list_price", 1000.0))
    cogs = float(req.get("cogs", 400.0))
    sched = req.get("discount_schedule", [])
    res = auditor.audit_pricing_waterfall(list_p, cogs, sched)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
