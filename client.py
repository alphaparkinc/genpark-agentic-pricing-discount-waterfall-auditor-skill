import sys
sys.stdout.reconfigure(encoding='utf-8')

class AgenticPricingDiscountWaterfallAuditorClient:
    """
    B2B CPQ discount waterfall auditor. Computes sequential discount deductions
    (Volume, Partner Channel, Promotional, Prompt Payment) and verifies against
    Minimum Acceptable Margin (MAM) governance limits.
    """
    def __init__(self, min_acceptable_margin=0.35, max_cumulative_discount=0.45):
        self.mam = min_acceptable_margin
        self.max_discount = max_cumulative_discount

    def audit_pricing_waterfall(self, list_price, unit_cogs, discount_schedule):
        # discount_schedule: list of {"name": str, "pct": float (0-1)}
        current_price = list_price
        waterfall_steps = []
        total_discount_dollars = 0.0

        for step in discount_schedule:
            name = step["name"]
            pct = step["pct"]
            discount_amount = current_price * pct
            new_price = current_price - discount_amount
            total_discount_dollars += discount_amount

            waterfall_steps.append({
                "stage": name,
                "discount_percentage": round(pct * 100.0, 1),
                "discount_deduction": round(discount_amount, 2),
                "subtotal_price": round(new_price, 2)
            })
            current_price = new_price

        pocket_price = current_price
        cumulative_discount_pct = (list_price - pocket_price) / max(1e-4, list_price)
        pocket_margin = (pocket_price - unit_cogs) / max(1e-4, pocket_price)

        # Compliance and Governance Checks
        violations = []
        if pocket_margin < self.mam:
            violations.append(f"Pocket margin {pocket_margin*100:.1f}% violates Minimum Acceptable Margin threshold ({self.mam*100:.1f}%)")
        if cumulative_discount_pct > self.max_discount:
            violations.append(f"Cumulative discount {cumulative_discount_pct*100:.1f}% exceeds maximum allowed cap ({self.max_discount*100:.1f}%)")

        if not violations:
            approval_level = "AUTOMATIC_PRE_APPROVED"
        elif pocket_margin >= (self.mam - 0.05):
            approval_level = "REQUIRES_VP_SALES_OVERRIDE"
        else:
            approval_level = "REQUIRES_CFO_AND_DEAL_DESK_ESCALATION"

        return {
            "status": "success",
            "list_price": round(list_price, 2),
            "unit_cogs": round(unit_cogs, 2),
            "pocket_price": round(pocket_price, 2),
            "total_discount_amount": round(total_discount_dollars, 2),
            "cumulative_discount_pct": round(cumulative_discount_pct * 100.0, 2),
            "pocket_margin_pct": round(pocket_margin * 100.0, 2),
            "waterfall_breakdown": waterfall_steps,
            "governance_violations": violations,
            "required_approval_authority": approval_level
        }
