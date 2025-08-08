import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go

# Load data
file_path = "Data 75%-25%.xlsx"
df = pd.read_excel(file_path)
df.columns = [col.strip(" `") for col in df.columns]
df['Period'] = pd.to_datetime(df['Period'])
df['Spread_mult100'] = df['Spread'] * 100

# Horizontal lines data
lines = {
    'Average Spread: x': df['x'].iloc[0] * 100,
    'Average Spread: x + σ': df['x + s'].iloc[0] * 100,
    'Average Spread: x – σ': df['x – s'].iloc[0] * 100,
}

line_styles = {
    'Average Spread: x': dict(dash='dash', width=2),
    'Average Spread: x + σ': dict(dash='dot'),
    'Average Spread: x – σ': dict(dash='dot'),
}

# Create figure
def create_figure():
    fig = go.Figure()

    # Main line
    fig.add_trace(go.Scatter(
        x=df['Period'],
        y=df['Spread_mult100'],
        mode='lines',
        name='Spot Spread: 75% – 25%',
        line=dict(color='green'),
        hovertemplate='Spread: %{y:.2f}%<extra></extra>'
    ))

    # Horizontal lines
    for label, y_val in lines.items():
        fig.add_trace(go.Scatter(
            x=[df['Period'].min(), df['Period'].max()],
            y=[y_val, y_val],
            mode='lines+text',
            name=label,
            line=dict(color='green', **line_styles[label]),
            text=[label, ''],
            textposition='top right',
            hoverinfo='skip'
        ))

    fig.update_layout(
        title=dict(
            text='Estimates of the Credit Curve Spread: 75% – 25% LTVs<br>Mortgage Loans for the Years 1996 through 1Q 2025',
            x=0.5,
            xanchor='center'
        ),
        yaxis=dict(
            title="Estimated Annual Interest Expense (k<sub>d</sub>)",
            ticks="outside",
            showgrid=True,
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='LightPink',
            ticksuffix="%",
        ),
        xaxis=dict(
            tickformat='%Y',
            dtick="M24",
            hoverformat='%Y-%m-%d'
        ),
        hovermode='x unified',
        template='plotly_white',
        legend=dict(y=0.99, x=0.01),
        margin=dict(t=60, l=60, r=40, b=60),
        height=900  # fixed height to avoid scroll issues
    )

    return fig

# Initialize Dash app
app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='spread-graph',
        figure=create_figure(),
        style={'height': '90vh'}  # optional: set height relative to viewport height
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
