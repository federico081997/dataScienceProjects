# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(
    r"C:\Users\fedem\OneDrive\Desktop\DataScience\Course10\spacex_launch_dash.csv"
)
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id="launch-site-dropdown",
            options=[
                {"label": "All Sites", "value": "ALL"},
                {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
                {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
            ],
            value="ALL",
            placeholder="Select a Launch Site...",
            searchable=True,
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            # marks={0: "0", 100: "100"},
            value=[min_payload, max_payload],
        ),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="launch-site-dropdown", component_property="value"),
)
def get_pie_chart(entered_site):
    data = spacex_df
    if entered_site == "ALL":
        fig = px.pie(
            data,
            values="class",
            names="Launch Site",
            title="Successful Lauches for all Sites",
        )
        return fig
    else:
        filtered_df = data[data["Launch Site"] == entered_site]
        class_counts = filtered_df["class"].value_counts().reset_index()
        class_counts.columns = ["class", "count"]  # rename columns

        fig = px.pie(
            class_counts,
            values="count",
            names="class",
            title=f"Successful Lauches for Site {entered_site}",
        )
        return fig


# TASK 4:
# Add a callback function for `launch-site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="launch-site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def get_scatter_chart(entered_site, entered_payload):
    min_payload, max_payload = entered_payload
    # First, filter by payload range (applies to both ALL and specific sites)
    payload_filtered_df = spacex_df[
        (spacex_df["Payload Mass (kg)"] >= min_payload)
        & (spacex_df["Payload Mass (kg)"] <= max_payload)
    ]
    if entered_site == "ALL":
        fig = px.scatter(
            payload_filtered_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Correlation Between Payload and Success for all Sites",
            labels={"class", "Launch Outcome"},
        )
        return fig
    else:
        site_df = payload_filtered_df[
            payload_filtered_df["Launch Site"] == entered_site
        ]
        fig = px.scatter(
            site_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title=f"Correlation between Payload and Success for Site {entered_site}",
            labels={"class", "Launch Outcome"},
        )
        return fig


# Run the app
if __name__ == "__main__":
    app.run()
