# Logistics Performance Intelligence

An interactive operations dashboard that calculates delivery, SLA, cost and carrier KPIs from shipment-level data and highlights the causes of late deliveries.

## KPIs

- On-time delivery rate
- SLA breach rate
- Average transit time
- Cost per shipment
- Carrier and route performance
- Delay-reason Pareto analysis
- Late-shipment exception table

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app loads `data/shipments.csv` by default and also accepts a user-uploaded CSV.

## Required columns

`shipment_id, carrier, origin, destination, promised_date, delivered_date, shipping_cost, delay_reason`

## Testing

```bash
pytest
```

## Technology

Python · pandas · Streamlit · Plotly · pytest

## Business use

A logistics team can use this dashboard during daily reviews to identify SLA risk, compare carrier reliability, prioritize late shipments and focus corrective action on the largest delay categories.
