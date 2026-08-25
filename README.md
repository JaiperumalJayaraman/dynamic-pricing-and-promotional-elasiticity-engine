# Dynamic Pricing & Promotional Elasticity Engine

## Problem Statement

Businesses often change prices and run promotions without a clear view of how demand responds. This can create two problems: discounts that increase sales but reduce margin, and price increases that protect margin but reduce volume too much.

This project builds a simple decision-support engine that estimates price elasticity, measures promotional lift, compares pricing scenarios, and recommends a price/promotion combination based on revenue and profit impact.

The project is intentionally lightweight and uses synthetic retail data so it can be cloned and run without external datasets or credentials.

## Approach

1. Generate a realistic synthetic product-sales dataset with price, discount, promotion, units sold, cost and product/category attributes.
2. Estimate demand response using a log-log regression to obtain price elasticity.
3. Measure promotional lift by comparing promoted demand with non-promoted demand while controlling for product/category context.
4. Simulate candidate prices and promotion levels.
5. Calculate expected units, revenue, cost and profit for every scenario.
6. Rank scenarios and return a practical pricing recommendation.
7. Export the analysis and charts for business review.

## Key Insights

- Price elasticity is estimated at product/category level so pricing decisions are not based only on total sales.
- A promotion is evaluated on incremental economics rather than sales volume alone.
- The engine explicitly compares revenue and profit, making margin dilution visible.
- Scenario analysis converts an elasticity estimate into an actionable price corridor.
- The recommendation is designed as a business decision-support output rather than a black-box ML prediction.

## Project Structure

```text
.
├── data/
│   └── .gitkeep
├── outputs/
│   └── .gitkeep
├── src/
│   ├── generate_data.py
│   ├── pricing_engine.py
│   └── run_analysis.py
├── tests/
│   └── test_engine.py
├── requirements.txt
└── README.md
```

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Statistical regression and scenario analysis

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/JaiperumalJayaraman/dynamic-pricing-and-promotional-elasiticity-engine.git
cd dynamic-pricing-and-promotional-elasiticity-engine
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the end-to-end analysis

```bash
python src/run_analysis.py
```

This creates:

- `outputs/sales_data.csv`
- `outputs/elasticity_results.csv`
- `outputs/promotion_results.csv`
- `outputs/pricing_scenarios.csv`
- `outputs/pricing_recommendation.csv`
- `outputs/demand_curve.png`
- `outputs/profit_scenarios.png`

### 4. Run tests

```bash
pytest -q
```

## Business Decision Logic

The engine follows a simple consulting-style framework:

**Demand response → Promotion impact → Scenario economics → Recommendation**

For each scenario:

```text
Revenue = Price × Expected Units
Variable Cost = Unit Cost × Expected Units
Profit = Revenue - Variable Cost
```

Expected demand is adjusted using estimated price elasticity and observed promotional lift.

## Example Decision Questions

The engine can support questions such as:

- Should the business reduce price by 5% or 10%?
- Is a 15% promotion generating enough incremental demand to justify the margin loss?
- Which price point maximizes expected profit?
- Which products are highly price-sensitive?
- Where should promotions be concentrated?

## Scope & Limitations

This is a decision-support prototype, not a production pricing system. The synthetic dataset is designed for demonstration. A production implementation should add experiments/A-B tests, competitor prices, inventory constraints, seasonality, customer segmentation, causal promotion measurement, price floors, and monitoring.
