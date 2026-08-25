import pandas as pd
from src.pricing_engine import estimate_elasticity, promotion_lift, build_scenarios, recommend


def sample_data():
    return pd.DataFrame({
        "product": ["P01"] * 8,
        "base_price": [100] * 8,
        "price": [80, 90, 100, 110, 120, 90, 100, 110],
        "promotion": [1, 1, 0, 0, 0, 1, 0, 0],
        "units": [260, 220, 180, 150, 130, 230, 180, 150],
        "unit_cost": [55] * 8,
    })


def test_elasticity_has_product():
    result = estimate_elasticity(sample_data())
    assert result.shape[0] == 1
    assert "price_elasticity" in result.columns


def test_promotion_lift_is_positive():
    result = promotion_lift(sample_data())
    assert result.loc[0, "promo_lift"] > 0


def test_recommendation_returns_one_per_product():
    df = sample_data()
    elasticity = estimate_elasticity(df)
    promo = promotion_lift(df)
    scenarios = build_scenarios(df, elasticity, promo)
    result = recommend(scenarios)
    assert len(result) == 1
    assert result.iloc[0]["product"] == "P01"
