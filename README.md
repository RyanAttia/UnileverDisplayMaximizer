# Unilever Display Maximizer

## Overview

This program recommends the best Unilever products to display in a retail store based on expected profitability. It considers factors such as store location, seasonal demand, discounts, special events, and display type to estimate profit per product and recommend the most lucrative option.

The program reads sales data from a CSV file and calculates expected profits by adjusting unit profits for discounts and seasonal multipliers, then scaling by display capacity.

---

## Features

- Adjusts profit by seasonal demand and special event multipliers.
- Supports multiple display types (side display, endcaps, pallets) with different unit capacities.
- Excludes certain product-display combinations (e.g., ice cream on certain displays).
- Interactive command-line input for store, season, discount, special event, and display type.
- Outputs recommended product with expected profit and units to display.

---

## Input

- **Store ID:** The store location identifier (e.g., "Store 1").
- **Season:** One of "summer", "winter", "spring", or "fall". Affects seasonal profit multipliers.
- **Discount per Unit:** Numeric value to subtract from the base profit per unit.
- **Special Event:** Whether a special promotional event is happening (yes/no).
- **Display Type:** Type of product display (e.g., "side_display", "split_endcap", "quarter_pallet", "half_pallet", "full_endcap", "full_pallet").

---

## Output

The program returns the recommended product to display, along with:

- Adjusted profit per unit (after discount and seasonal/special event adjustments).
- Number of units to place on the chosen display type.
- Expected total profit from the displayed units.

---

## How it Works

1. **Display Capacity Scaling:** Each display type has a multiplier representing relative capacity compared to a baseline "split_endcap".

2. **Product Unit Capacity:** The system makes a accurate prediction of the amount of units that could fit based on the size of the product and the type of display mentioned.

3. **Profit Adjustment:** The profit per unit is adjusted by discount, season multiplier (which can increase profitability for some products in certain seasons), and special event multiplier (25% increase if true).

4. **Filtering:** Some product-display combinations are restricted (e.g., ice cream products are only recommended for half or full endcaps).

5. **Recommendation:** Products are ranked by expected total profit (`adjusted_profit * units_on_display`), and the top product is recommended.
