import pandas as pd
from analytics import carrier_scorecard, headline_kpis, prepare_shipments

def sample():
    return pd.DataFrame({
        "shipment_id":["A","B"], "carrier":["X","X"], "origin":["L","L"],
        "destination":["D","D"], "promised_date":["2026-01-01","2026-01-01"],
        "delivered_date":["2026-01-01","2026-01-03"], "shipping_cost":[100,200],
        "delay_reason":["","Weather"],
    })

def test_kpis():
    df = prepare_shipments(sample())
    kpi = headline_kpis(df)
    assert kpi["on_time_rate"] == 50
    assert kpi["sla_breaches"] == 1
    assert kpi["cost_per_shipment"] == 150

def test_carrier_scorecard():
    score = carrier_scorecard(prepare_shipments(sample()))
    assert score.iloc[0]["shipments"] == 2
