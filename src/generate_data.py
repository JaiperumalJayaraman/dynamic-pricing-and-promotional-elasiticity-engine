from pathlib import Path
import numpy as np
import pandas as pd


def generate_sales_data(n_rows=2400, seed=42):
    rng = np.random.default_rng(seed)
    products = [f"P{i:02d}" for i in range(1, 13)]
    categories = {p: ["Beverages", "Snacks", "Personal Care"][i % 3] for i, p in enumerate(products)}
    base_prices = {p: rng.uniform(60, 500) for p in products}
    rows = []
    for _ in range(n_rows):
        product = rng.choice(products)
        base = base_prices[product]
        price = base * rng.uniform(0.85, 1.15)
        discount = rng.choice([0.0, 0.05, 0.10, 0.15, 0.20], p=[0.35, 0.15, 0.20, 0.20, 0.10])
        promotion = int(discount > 0)
        elasticity = rng.uniform(-1.8, -0.5)
        promo_lift = rng.uniform(1.05, 1.35) if promotion else 1.0
        demand = 220 * (price / base) ** elasticity * promo_lift
        units = max(1, int(rng.poisson(demand)))
        unit_cost = base * rng.uniform(0.45, 0.70)
        rows.append([product, categories[product], base, price, discount, promotion, units, unit_cost])
    return pd.DataFrame(rows, columns=["product", "category", "base_price", "price", "discount", "promotion", "units", "unit_cost"])


if __name__ == "__main__":
    out = Path("outputs")
    out.mkdir(exist_ok=True)
    generate_sales_data().to_csv(out / "sales_data.csv", index=False)
    print(f"Generated {len(generate_sales_data())} sales records")
