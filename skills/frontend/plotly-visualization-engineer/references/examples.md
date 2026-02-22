# Plotly Examples

## Faceted Trend

```python
fig = px.line(df, x="date", y="revenue", color="region", facet_col="channel")
```

## Animated Scatter

```python
fig = px.scatter(df, x="gdp", y="life_exp", size="population", animation_frame="year")
```

## Subplots

```python
fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
```
