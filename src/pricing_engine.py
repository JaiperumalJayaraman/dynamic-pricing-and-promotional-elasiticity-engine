from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def estimate_elasticity(df):
    results = []
    for product, g in df.groupby("product"):
        x = np.log(g[["price"]].values)
        y = np.log(g["units"].values)
        model = LinearRegression().fit(x, y)
        results.append({"product": product, "price_elasticity": model.coef_[0], "r2": model.score(x, y)})
    return pd.DataFrame(results)


def promotion_lift(df):
    grouped = df.groupby(["product", "promotion"])["units"].mean().unstack(fill_value=0)
    grouped["promo_lift"] = grouped.get(1, 0) / grouped.get(0, 1)
    return grouped[["promo_lift"]].reset_index()


def build_scenarios(df, elasticity, promo):
    base = df.groupby("product").agg(base_price=("base_price", "mean"), unit_cost=("unit_cost", "mean"), avg_units=("units", "mean")).reset_index()
    result = []
    for _, row in base.iterrows():
        e = float(elasticity.loc[elasticity.product == row.product, "price_elasticity"].iloc[0])
        lift = float(promo.loc[promo.product == row.product, "promo_lift"].iloc[0])
        for discount in [0.00, 0.05, 0.10, 0.15, 0.20]:
            price = row.base_price * (1 - discount)
            expected_units = row.avg_units * (price / row.base_price) ** e * (lift if discount > 0 else 1.0)
            revenue = price * expected_units
            profit = (price - row.unit_cost) * expected_units
            result.append([row.product, discount, price, expected_units, revenue, profit])
    return pd.DataFrame(result, columns=["product", "discount", "price", "expected_units", "revenue", "profit"])


def recommend(scenarios):
    idx = scenarios.groupby("product")["profit"].idxmax()
    return scenarios.loc[idx].sort_values("profit", ascending=False).reset_index(drop=True)


def run_engine(data_path="outputs/sales_data.csv"):
    out = Path("outputs")
    df = pd.read_csv(data_path)
    elasticity = estimate_elasticity(df)
    promo = promotion_lift(df)
    scenarios = build_scenarios(df, elasticity, promo)
    recommendations = recommend(scenarios)
    elasticity.to_csv(out / "elasticity_results.csv", index=False)
    promo.to_csv(out / "promotion_results.csv", index=False)
    scenarios.to_csv(out / "pricing_scenarios.csv", index=False)
    recommendations.to_csv(out / "pricing_recommendation.csv", index=False)
    return elasticity, promo, scenarios, recommendations
