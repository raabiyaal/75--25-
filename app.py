import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go
import os 

# Load data inside the app file
file_path = r"Data 75%-25%.xlsx"
df = pd.read_excel(file_path)
df['Period'] = pd.to_datetime(df['Period'])

app = Dash(__name__)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['Period'],
    y=df['Spread'],
    mode='lines',
    line=dict(color='green', width=2),
    name='Spot Spread: 75% – 25%'
))

fig.add_hline(
    y=df['`x'].iloc[0],
    line=dict(color='green', dash='dash', width=2),
    annotation_text="Average Spread: x̄",
    annotation_position="top left",
    name="Average Spread: x̄"
)
fig.add_hline(
    y=df['`x + s'].iloc[0],
    line=dict(color='green', dash='dot', width=2),
    annotation_text="Average Spread: x̄ + σ",
    annotation_position="top left",
    name="Average Spread: x̄ + σ"
)
fig.add_hline(
    y=df['`x – s'].iloc[0],
    line=dict(color='green', dash='dot', width=2),
    annotation_text="Average Spread: x̄ – σ",
    annotation_position="bottom left",
    name="Average Spread: x̄ – σ"
)

fig.update_layout(
    yaxis_title=r'Estimated Annual Interest Expense ($k_d$)',  # subscript fixed with raw string
    yaxis=dict(range=[0, 0.1], tickformat=".0%", dtick=0.01),
    legend=dict(font=dict(size=12)),
    template='simple_white',
    showlegend=True
)

app.layout = html.Div([
    dcc.Graph(figure=fig, style={'width': '90%', 'height': '80vh', 'margin': 'auto'})
])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))  # Get port from environment variable, fallback 8050
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
