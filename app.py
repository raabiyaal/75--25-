import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_javascript import st_javascript

# Set Streamlit page layout wide
st.set_page_config(layout="wide")

# Remove default Streamlit padding
st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
    </style>
""", unsafe_allow_html=True)

# Get viewport height from browser using JavaScript (returns a string)
viewport_height_str = st_javascript("window.innerHeight")

# Convert viewport height to int, fallback to 700 if failed
try:
    viewport_height = int(viewport_height_str)
except (TypeError, ValueError):
    viewport_height = 700

# You can subtract some pixels if you want margin (optional)
chart_height = viewport_height - 100  # leave 100px for other UI elements

# File path to your Excel file
file_path = "Data 75%-25%.xlsx"

# Read and clean data
df = pd.read_excel(file_path)
df.columns = [col.strip(" `") for col in df.columns]
df['Period'] = pd.to_datetime(df['Period'])
df['Spread_mult100'] = df['Spread'] * 100

# Horizontal line values
lines = {
    'Average Spread: x': df['x'].iloc[0] * 100,
    'Average Spread: x + σ': df['x + s'].iloc[0] * 100,
    'Average Spread: x – σ': df['x – s'].iloc[0] * 100,
}

# Create figure
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
line_styles = {
    'Average Spread: x': dict(dash='dash', width=2),
    'Average Spread: x + σ': dict(dash='dot'),
    'Average Spread: x – σ': dict(dash='dot'),
}

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

# Update layout with dynamic height
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
    height=chart_height
)

# Display plotly chart with full container width
st.plotly_chart(fig, use_container_width=True)
