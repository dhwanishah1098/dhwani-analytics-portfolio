# Case Study: Stockout Root-Cause Analysis

## Business Problem
A distribution business was experiencing frequent stockouts across 40+ SKUs
with no clear visibility into which suppliers or products were the primary drivers.

## Approach
1. Joined purchase order, inventory, and sales data in SQL
2. Calculated days-of-stock for each SKU using rolling 30-day sales velocity
3. Identified SKUs breaching reorder threshold before replenishment arrived
4. Ran supplier-level analysis on lead time variance and fill rate

## Findings
- 5 SKUs accounted for 73% of total stockout events
- 2 suppliers had average lead time 40% longer than promised
- Seasonal demand spikes in Q4 not factored into safety stock calculations

## Recommended Actions
1. Increase safety stock multiplier for the 5 high-risk SKUs
2. Renegotiate SLAs with the 2 underperforming suppliers
3. Add seasonal adjustment factor to reorder point formula

## Outcome
Estimated cost savings of **A$45,000/quarter** from reduced emergency procurement
and lost-sale events.
