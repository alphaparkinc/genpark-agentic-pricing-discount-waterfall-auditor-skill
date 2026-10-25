from client import AgenticPricingDiscountWaterfallAuditorClient
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    auditor = AgenticPricingDiscountWaterfallAuditorClient(min_acceptable_margin=0.40, max_cumulative_discount=0.40)
    print("=== AGENTIC PRICING DISCOUNT WATERFALL AUDITOR ===")
    
    # $50,000 Enterprise License Deal with COGS of $18,000
    discounts = [
        {"name": "Tier-3 Volume Rebate", "pct": 0.15},
        {"name": "Gold Partner Margin", "pct": 0.10},
        {"name": "End-of-Quarter Promo", "pct": 0.10},
        {"name": "Net-10 Early Payment", "pct": 0.03}
    ]
    
    res = auditor.audit_pricing_waterfall(50000.00, 18000.00, discounts)
    print()
    print(f"List: ${res['list_price']:,.2f} -> Pocket: ${res['pocket_price']:,.2f} (Total Cut: -${res['total_discount_amount']:,.2f})")
    print(f"Cumulative Discount: {res['cumulative_discount_pct']}% | Pocket Margin: {res['pocket_margin_pct']}%")
    print(f"Approval Tier: {res['required_approval_authority']}")
    print("Waterfall Stages:")
    for step in res['waterfall_breakdown']:
        print(f"  - {step['stage']:<24}: -{step['discount_percentage']}% (-${step['discount_deduction']:,.2f}) => ${step['subtotal_price']:,.2f}")

if __name__ == "__main__":
    main()
