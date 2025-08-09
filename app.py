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
    annotation_position="top left"
)
fig.add_hline(
    y=df['`x + s'].iloc[0],
    line=dict(color='green', dash='dot', width=2),
    annotation_text="Average Spread: x̄ + σ",
    annotation_position="top left"
)
fig.add_hline(
    y=df['`x – s'].iloc[0],
    line=dict(color='green', dash='dot', width=2),
    annotation_text="Average Spread: x̄ – σ",
    annotation_position="bottom left"
)

fig.update_layout(
    title='Estimates of the Credit Curve Spread: 75% – 25% LTVs\nMortgage Loans for the Years 1996 through 1Q 2025',
    yaxis_title='Estimated Annual Interest Expense ($k_d$)',
    yaxis=dict(range=[0, 0.1], tickformat=".0%", dtick=0.01),
    legend=dict(font=dict(size=12)),
    template='simple_white'
)

app.layout = html.Div([
    html.H1("Credit Curve Spread Dashboard", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig, style={'width': '90%', 'height': '80vh', 'margin': 'auto'})
])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))  # default 8050 if not set
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)


