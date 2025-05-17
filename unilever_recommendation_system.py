import pandas as pd

display_types = {
    "side_display": 0.5,
    "split_endcap": 1,
    "quarter_pallet": 0.8,
    "half_endcap": 1,
    "half_pallet": 1.6,
    "full_endcap": 2,
    "full_pallet": 3.2
}

# Estimated units per display type for each product (scaled to split endcap baseline)
display_capacity = {
    "Hellmann's Real Mayonnaise (30 oz)": {"split_endcap": 200},
    "Dove Deep Moisture Body Wash (20 oz)": {"split_endcap": 330},
    "Knorr Rice/Pasta Packet": {"split_endcap": 400},
    "Breyers Natural Vanilla Ice Cream": {"split_endcap": 160},
    "Ben & Jerry's Chocolate Fudge Brownie (16 oz)": {"split_endcap": 180},
    "Dove Beauty Bar (6-pack)": {"split_endcap": 210},
    "Degree Advanced Antiperspirant (2.7 oz)": {"split_endcap": 310},
    "AXE Body Spray for Men (4 oz)": {"split_endcap": 300},
    "TRESemmé Moisture Rich Shampoo (28 oz)": {"split_endcap": 290},
    "SheaMoisture Curl Enhancing Smoothie (12 oz)": {"split_endcap": 250}
}

# Seasonal multipliers (influence on sales)
season_multipliers = {
    "summer": {
        "Hellmann's Real Mayonnaise (30 oz)": 1.3,
        "Breyers Natural Vanilla Ice Cream": 1.4,
        "Ben & Jerry's Chocolate Fudge Brownie (16 oz)": 1.3
    },
    "winter": {
        "Dove Deep Moisture Body Wash (20 oz)": 1.2,
        "Dove Beauty Bar (6-pack)": 1.2,
        "TRESemmé Moisture Rich Shampoo (28 oz)": 1.15
    },
    "spring": {},
    "fall": {}
}

def get_adjusted_profit(row, discount, season, special_event):
    base_profit = row['Profit_Per_Unit']
    adjusted_profit = base_profit - discount

    # Seasonal effect
    season_factor = season_multipliers.get(season.lower(), {}).get(row['Product_Name'], 1.0)

    # Special event boost
    event_factor = 1.25 if special_event else 1.0

    return adjusted_profit * season_factor * event_factor

def get_units_per_display(product_name, display_type):
    base = display_capacity[product_name]["split_endcap"]
    scale = display_types[display_type]
    return int(base * scale)

def recommend_products(store, season, discount, special_event, display_type):
    df = pd.read_csv("unilever_product_sales_dataset.csv")

    # Filter store
    store_df = df[df['Store_ID'].str.lower() == store.lower()]

    recommendations = []

    for _, row in store_df.iterrows():
        product = row['Product_Name']

        # Ice cream placement restriction
        if ("Ice Cream" in product or "Ben & Jerry" in product) and display_type not in ["half_endcap", "full_endcap"]:
            continue

        adjusted_profit = get_adjusted_profit(row, discount, season, special_event)
        units = get_units_per_display(product, display_type)
        total_profit = adjusted_profit * units

        recommendations.append({
            "Product": product,
            "Adjusted_Profit_Per_Unit": round(adjusted_profit, 2),
            "Units_on_Display": units,
            "Expected_Total_Profit": round(total_profit, 2)
        })

    recommendations = sorted(recommendations, key=lambda x: x['Expected_Total_Profit'], reverse=True)
    return recommendations

if __name__ == "__main__":
    print("=== Unilever Product Recommender ===")

    store_id = input("Enter Store ID (e.g., 'Store 1'): ")
    season = input("Enter season (summer, winter, spring, fall): ").strip().lower()
    discount = input("Enter discount per unit (e.g., 0, 1.00): ")
    special_event = input("Is there a special event associated with the product? (yes/no): ").strip().lower()
    display_type = input("Enter display type (e.g., 'full_endcap'): ")

    # Convert inputs to correct types
    try:
        discount = float(discount)
    except ValueError:
        print("Invalid input for minimum profit. Defaulting to $0.")
        discount = 0

    special_event = special_event in ["yes", "y"]

    # Call the recommender
    results = recommend_products(
        store_id, season, discount, special_event, display_type
    )
    
    display_type_map = {
    "quarter_pallet": "1/4 pallet",
    "half_pallet": "1/2 pallet"
    }

    # Show results
    if results:
        top_product = results[0]
        display_desc = display_type_map.get(display_type, display_type.replace('_', ' '))

        print(f"\nWe recommend displaying {top_product['Product']} with an expected total profit of ${top_product['Expected_Total_Profit']:.2f} for the {top_product['Units_on_Display']} units on a {display_desc}st.")
    else:
        print("\nNo products met the criteria.")
