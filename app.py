import pandas as pd
import plotly.express as px
import streamlit as st
from analytics import carrier_scorecard, headline_kpis, prepare_shipments

st.set_page_config(page_title="Logistics Intelligence", page_icon="🚚", layout="wide")
st.title("🚚 Logistics Performance Intelligence")
st.caption("Daily SLA, carrier, route and exception monitoring.")

uploaded = st.sidebar.file_uploader("Upload shipment CSV", type="csv")
source = uploaded if uploaded else "data/shipments.csv"

try:
    df = prepare_shipments(pd.read_csv(source))
except Exception as exc:
    st.error(str(exc))
    st.stop()

carriers = st.sidebar.multiselect("Carrier", sorted(df["carrier"].unique()))
if carriers:
    df = df[df["carrier"].isin(carriers)]

kpi = headline_kpis(df)
cols = st.columns(5)
cols[0].metric("Shipments", f"{kpi['shipments']:,}")
cols[1].metric("On-time rate", f"{kpi['on_time_rate']:.1f}%")
cols[2].metric("SLA breaches", f"{kpi['sla_breaches']:,}")
cols[3].metric("Avg. days late", f"{kpi['average_days_late']:.1f}")
cols[4].metric("Cost/shipment", f"₹{kpi['cost_per_shipment']:,.0f}")

left, right = st.columns(2)
score = carrier_scorecard(df)
left.plotly_chart(px.bar(score, x="carrier", y="on_time_rate", color="on_time_rate",
                         range_y=[0, 100], title="Carrier on-time performance"), use_container_width=True)
reasons = (df.loc[~df["on_time"], "delay_reason"].fillna("Unknown").value_counts().reset_index())
reasons.columns = ["delay_reason", "shipments"]
right.plotly_chart(px.bar(reasons, x="shipments", y="delay_reason", orientation="h",
                          title="Late deliveries by reason"), use_container_width=True)

routes = df.groupby("route", as_index=False).agg(shipments=("shipment_id","count"), on_time_rate=("on_time","mean"))
routes["on_time_rate"] = (routes["on_time_rate"] * 100).round(1)
st.plotly_chart(px.scatter(routes, x="shipments", y="on_time_rate", text="route",
                           size="shipments", title="Route volume vs reliability"), use_container_width=True)

st.subheader("Priority exceptions")
exceptions = df.loc[~df["on_time"]].sort_values("days_late", ascending=False)
st.dataframe(exceptions, use_container_width=True)
st.download_button("Download exceptions", exceptions.to_csv(index=False), "late_shipments.csv", "text/csv")
