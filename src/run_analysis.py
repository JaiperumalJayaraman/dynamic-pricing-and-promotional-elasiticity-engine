from pathlib import Path
import matplotlib.pyplot as plt
from generate_data import generate_sales_data
from pricing_engine import run_engine


if __name__ == "__main__":
    out = Path("outputs")
    out.mkdir(exist_ok=True)
    generate_sales_data().to_csv(out / "sales_data.csv", index=False)
    elasticity, promo, scenarios, recommendations = run_engine()

    plt.figure(figsize=(8, 5))
    for product in scenarios["product"].unique()[:5]:
        g = scenarios[scenarios.product == product]
        plt.plot(g["price"], g["expected_units"], marker="o", label=product)
    plt.xlabel("Price")
    plt.ylabel("Expected Units")
    plt.title("Price vs Expected Demand")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "demand_curve.png", dpi=150)
    plt.close()

    top = recommendations.head(8)
    plt.figure(figsize=(9, 5))
    plt.bar(top["product"], top["profit"])
    plt.xlabel("Product")
    plt.ylabel("Expected Profit")
    plt.title("Recommended Scenario Profit")
    plt.tight_layout()
    plt.savefig(out / "profit_scenarios.png", dpi=150)
    plt.close()

    print("Analysis complete.")
    print("Top recommendations:")
    print(recommendations[["product", "discount", "price", "expected_units", "profit"]].head(10).to_string(index=False))
