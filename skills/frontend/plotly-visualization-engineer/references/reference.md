# Plotly Reference

## Table of Contents

1. Chart selection matrix
2. Plotly Express patterns
3. Graph Objects enhancements
4. Dashboard composition
5. Performance and export

## 1. Chart Selection Matrix

- Trend over time: line/area.
- Category comparison: bar/dot.
- Distribution: histogram/box/violin.
- Relationship: scatter/bubble.
- Hierarchy: treemap/sunburst.
- Geospatial: choropleth/scattermap.

## 2. Plotly Express Patterns

- Use `color` for category, `size` for magnitude, `facet_*` for segmentation.
- Keep hover templates concise and informative.
- Use `animation_frame` for state transitions over time.

## 3. Graph Objects Enhancements

- Add secondary axes for mixed units.
- Add custom annotations and threshold bands.
- Build subplots for coordinated analysis.

## 4. Dashboard Composition

- Top row: KPI and trend overview.
- Mid row: segment and correlation views.
- Bottom row: detail table or drill-down plots.

## 5. Performance and Export

- Downsample large timeseries.
- Pre-aggregate heavy datasets.
- Export interactive HTML for sharing.
