"""Reusable KPI calculations for shipment performance."""
import pandas as pd

REQUIRED_COLUMNS = {
    "shipment_id", "carrier", "origin", "destination", "promised_date",
    "delivered_date", "shipping_cost", "delay_reason",
}

def prepare_shipments(data: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
    df = data.copy()
    for col in ["promised_date", "delivered_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    df["transit_days"] = (df["delivered_date"] - df["promised_date"]).dt.days
    df["days_late"] = df["transit_days"].clip(lower=0)
    df["on_time"] = df["delivered_date"] <= df["promised_date"]
    df["route"] = df["origin"] + " → " + df["destination"]
    return df

def headline_kpis(df: pd.DataFrame) -> dict:
    total = len(df)
    return {
        "shipments": total,
        "on_time_rate": float(df["on_time"].mean() * 100) if total else 0.0,
        "sla_breaches": int((~df["on_time"]).sum()) if total else 0,
        "average_days_late": float(df.loc[~df["on_time"], "days_late"].mean() or 0),
        "cost_per_shipment": float(df["shipping_cost"].mean() or 0),
    }

def carrier_scorecard(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("carrier", as_index=False)
        .agg(shipments=("shipment_id", "count"), on_time_rate=("on_time", "mean"),
             avg_cost=("shipping_cost", "mean"), avg_days_late=("days_late", "mean"))
        .assign(on_time_rate=lambda x: (x["on_time_rate"] * 100).round(1))
        .sort_values(["on_time_rate", "avg_cost"], ascending=[False, True])
    )
