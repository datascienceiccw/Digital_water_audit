# data_preprocessing.py
from decouple import config
MAPBOX_ACCESS_TOKEN = config("MAPBOX_ACCESS_TOKEN")
from dash import html, dcc, Input, Output
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, Input, Output
from geopy.geocoders import Nominatim
import dash_bootstrap_components as dbc

from .models import (
    SourceWaterProfile,
    TanksCapacities,

)
import pydeck as pdk
import pandas as pd
from .models import BasicDetails
from math import radians, cos, sin, sqrt, atan2

def normalize_sizes(sizes, min_size=10, max_size=50):
    min_val, max_val = min(sizes), max(sizes)
    return [((size - min_val) / (max_val - min_val)) * (max_size - min_size) + min_size for size in sizes]



def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    r = 6371

    return c * r


def find_nearest_location(user, csv_file_path):
    df = pd.read_csv(csv_file_path)
    pincode = BasicDetails.objects.filter(user=user).first().pin_code
    user_lat, user_lon = get_lat_long_from_pincode(pincode)

    min_distance = float('inf')
    nearest_location = None

    for index, row in df.iterrows():
        lat, lon = row['lat'], row['long']
        distance = haversine(user_lat, user_lon, lat, lon)
        if distance < min_distance:
            min_distance = distance
            nearest_location = (row['Station_name'], lat, lon)

    return nearest_location


def get_lat_long_from_pincode(pincode):
    geolocator = Nominatim(user_agent="django-plotly-dash-app")
    location = geolocator.geocode(pincode)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None, None


def create_source_water_distribution_dashboard_layout(user):
    layout = html.Div([
        dcc.RadioItems(
            id='water-distribution-selection',
            options=[
                {'label': 'Source Water Cost and Consumption Distribution',
                    'value': 'source_distribution'},
                {'label': 'Tank Capacity Distribution',
                    'value': 'tank_distribution'},
            ],
            value='source_distribution',  # Default value
            inline=True,
            className='mb-4 mx-auto d-flex justify-content-around',
            style={'font-size': '1.2em', 'font-weight': 'bold'}
        ),
        html.Div(id='water-distribution-content-container')
    ], style={'background-color': '#aed3fc'}, className='p-3 border border-3 rounded')

    return layout


def create_pie_chart_for_source(user, source_category):
    sources = SourceWaterProfile.objects.filter(user=user)
    labels = [source.get_source_name_display() for source in sources]

    # Values for cost and daily consumption
    cost_values = [source.source_water_cost *
                   source.source_daily_consumption for source in sources]
    consumption_values = [
        source.source_daily_consumption for source in sources]

    total_cost, average_cost = sum(cost_values), sum(
        cost_values) / len(cost_values) if cost_values else 0
    fig = make_subplots(rows=1, cols=2, specs=[
                        [{'type': 'pie'}, {'type': 'pie'}]])

    # Adding cost distribution pie chart
    fig.add_trace(
        go.Pie(
            labels=labels,
            values=cost_values,
            name="Cost Distribution",
            hovertemplate="<b>%{label}:</b> ₹%{value}<br><b>Percentage:</b> %{percent}",
            texttemplate="%{label}: %{percent}<br>(₹%{value:,.1f})",
            marker=dict(colors=px.colors.qualitative.Plotly),
            hole=0.4
        ),
        row=1, col=1
    )

    # Adding daily consumption distribution pie chart
    fig.add_trace( 
        go.Pie(
            labels=labels,
            values=consumption_values,
            name="Daily Consumption Distribution",
            hovertemplate="<b>%{label}:</b> %{value} kl<br><b>Percentage:</b> %{percent}",
            texttemplate="%{label}: %{percent}<br>(%{value} kl)",
            marker=dict(colors=px.colors.qualitative.Plotly),
            hole=0.4
        ),
        row=1, col=2
    )
    # Updating the layout for a cleaner look
    fig.update_layout(
        title_text=f"Source Water Distribution: {source_category}",
        autosize=True,
        annotations=[
            dict(
                text='Cost Distribution',
                x=0.23,  # Adjust for better positioning
                y=-0.1,  # Adjust for better positioning
                xref='paper',
                yref='paper',
                xanchor='center',
                yanchor='bottom',
                showarrow=False,
                font_size=12
            ),
            dict(
                text='Daily Consumption Distribution',
                x=0.77,  # Adjust for better positioning
                y=-0.1,  # Adjust for better positioning
                xref='paper',
                yref='paper',
                xanchor='center',
                yanchor='bottom',
                showarrow=False,
                font_size=12
            )
        ]
    )

    fig.add_annotation(
        x=0.5,  # Center the text
        y=1.04,  # Position below the pie charts
        xref="paper",
        yref="paper",
        text=f"Total Cost: ₹{total_cost:,.2f}, Average Cost: ₹{average_cost:,.2f}/source",
        font=dict(size=10),
        showarrow=False,
        xanchor='center',
        yanchor='top'
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=80),
    )
    return fig




def create_pie_chart_for_tank(user, tank_category):
    tanks = TanksCapacities.objects.filter(user=user)
    labels = [tank.get_tank_name_display() for tank in tanks]
    values = [tank.capacity for tank in tanks]

    # Define a soothing color palette
    soothing_colors = ['#89CFF0', '#F5DEB3', '#FFDFD3', '#E0BBE4', '#957DAD', '#D291BC', '#FEC8D8', '#FFDF00', '#FF7F50', '#FFBF00']

    # Ensure the color list is as long as the number of labels
    colors = soothing_colors * (len(labels) // len(soothing_colors)) + soothing_colors[:len(labels) % len(soothing_colors)]

    # Creating the pie chart with Plotly Express
    fig = px.pie(
        names=labels,
        values=values,
        title=f'Tank Capacity Distribution: {tank_category}',
        color_discrete_sequence=colors,  # Apply the soothing color palette
        hole=0.4
    )

    # Update traces for better hover and text template
    fig.update_traces(
        hovertemplate="<b>%{label}:</b> %{value} kl<br><b>Percentage:</b> %{percent}",
        texttemplate="%{label}: %{percent}<br>(%{value:,.1f} kl)"
    )

    # Adjusting layout for clear visualization
    fig.update_layout(
        margin=dict(t=50, b=0, l=0, r=0),
        uniformtext_minsize=12,
        uniformtext_mode='hide'
    )

    return fig

def create_treemap_for_tank(user, tank_category):
    tanks = TanksCapacities.objects.filter(user=user)
    labels = [tank.get_tank_name_display() for tank in tanks]
    values = [tank.capacity for tank in tanks]
    parents = [''] * len(tanks)  # As it's the top level, there are no parents

    # Creating the treemap with Plotly Express
    fig = px.treemap(
        names=labels,
        parents=parents,
        values=values,
        title=f'Tank Capacity Distribution: {tank_category}',
        color=values,
        color_continuous_scale='blues',  # Color scale can be adjusted
    )

    # Update layout for a cleaner look
    fig.update_layout(
        margin=dict(t=50, b=0, l=0, r=0),
        coloraxis_colorbar=dict(title='Tank Capacity'),
        height=500,
        width=1000
    )

    return fig


# def plot_monthly_rainfall_across_years():
#     data_long = pd.read_csv("waterflow/chennai-monthly-rains-long.csv")
#     fig = px.line(
#         data_long,
#         x="Month",
#         y="Rainfall_mm",
#         animation_frame="Year",
#         range_y=[0, data_long["Rainfall_mm"].max() * 1.1],
#         labels={"Rainfall_mm": "Rainfall (mm)"},
#         title="Monthly Rainfall in Chennai Across Years",
#         template="plotly_white",
#     )

#     fig.update_traces(line=dict(width=5), marker=dict(size=7))
#     fig.update_layout(
#         xaxis_title="Month",
#         yaxis_title="Rainfall (mm)",
#         xaxis={"type": "category"},
#         yaxis=dict(autorange=False),
#         font=dict(family="Arial, sans-serif",
#                   size=12, color="rgb(168, 119, 3)"),
#         legend=dict(title="Legend", x=1, y=1),
#         hovermode="x unified",
#         plot_bgcolor="white",
#         paper_bgcolor="white",
#     )

#     fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
#     fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 1000
#     fig.layout.updatemenus[0].buttons[0].args[1]["transition"][
#         "easing"
#     ] = "cubic-in-out"

#     return fig


def plot_monthly_rainfall_across_years():
    data_long = pd.read_csv("waterflow/chennai-monthly-rains-long.csv")

    # Create the initial bar chart with text labels
    fig = px.bar(
        data_long,
        x="Month",
        y="Rainfall_mm",
        animation_frame="Year",
        range_y=[0, data_long["Rainfall_mm"].max() * 1.1],
        labels={"Rainfall_mm": "Rainfall (mm)"},
        title="Monthly Rainfall in Chennai Across Years",
        color="Rainfall_mm",
        color_continuous_scale='blues',
        
    )

    # Update layouts and axes
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Rainfall (mm)",
        xaxis={"type": "category"},
        yaxis=dict(autorange=False),
        font=dict(family="Arial, sans-serif", size=12, color="rgb(168, 119, 3)"),
        legend=dict(title="Legend", x=1, y=1),
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        coloraxis_showscale=True, 
        barmode='group',
    )

    # Configure animation
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 1000
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["easing"] = "cubic-in-out"
    
    for frame in fig.frames:
        for data in frame.data: 
            data['text'] = data['y'].round(2)
            data['textposition'] = 'outside'
            data['textfont'] = dict(color='black')

    return fig


# def plot_total_annual_rainfall():
#     data_2000_onwards = pd.read_csv(
#         "waterflow/chennai-monthly-rains-2000-onwards.csv")
#     fig = px.bar(
#         data_2000_onwards,
#         x="Year",
#         y="Total",
#         labels={"Total": "Total Annual Rainfall (mm)"},
#         title="Total Annual Rainfall in Chennai",
#     )

#     fig.update_layout(
#         xaxis_title="Year",
#         yaxis_title="Total Annual Rainfall (mm)",
#         xaxis={"type": "category"},
#         font=dict(family="Arial, sans-serif",
#                   size=12, color="rgb(168, 119, 3)"),
#         plot_bgcolor="white",
#         paper_bgcolor="white",
#     )

#     return fig

def plot_total_annual_rainfall():
    data_2000_onwards = pd.read_csv(
        "waterflow/chennai-monthly-rains-2000-onwards.csv")
    fig = px.line(
        data_2000_onwards,
        x="Year",
        y="Total",
        labels={"Total": "Total Annual Rainfall (mm)"},
        title="Total Annual Rainfall in Chennai",
        markers=True,  # Add markers to the line chart
    )

    # Update layouts and axes
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Total Annual Rainfall (mm)",
        xaxis={"type": "category"},
        font=dict(family="Arial, sans-serif", size=12, color="rgb(168, 119, 3)"),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    # Update marker and line style
    fig.update_traces(
        line=dict(width=2),  # Set line width
        marker=dict(size=7, color="darkslateblue"),  # Set marker size and color
    )

    return fig




def create_rainfall_map(user):
    pincode = BasicDetails.objects.filter(user=user).first().pin_code
    lat, long = get_lat_long_from_pincode(pincode)
    user_location_data = pd.DataFrame({"latitude": [lat], "longitude": [long]})
    df = pd.read_excel(
        "waterflow/chennai-all-stations-daily-rainfall-lat-long.xlsx",
        sheet_name="Sheet2",
    )

    df["rainfall_scaled"] = df["Average Rainfall"]

    df["Average Rainfall"] = df["Average Rainfall"].round(2)

    df["normalized_value"] = (df["rainfall_scaled"] - df["rainfall_scaled"].min()) / (
        df["rainfall_scaled"].max() - df["rainfall_scaled"].min()
    )

    # Define a color gradient function
    def get_color(value):
        blue = [0, 0, 255, 255]  # Low values
        red = [255, 0, 0, 255]  # High values
        return [int(red[i] + (blue[i] - red[i]) * value) for i in range(4)]

    df["color"] = df["normalized_value"].apply(get_color)
    user_location_layer = pdk.Layer(
        "ScatterplotLayer",
        user_location_data,
        get_position=["longitude", "latitude"],
        get_color="[255, 255, 217, 100]",  # Red color, semi-transparent
        get_radius=2000,  # Adjust the size of the circle
        pickable=False,

    )
    # Define a layer to visualize the data
    layer = pdk.Layer(
        "ColumnLayer",  # Specify the layer type
        data=df,  # Pass the DataFrame
        get_position="[Longitude, Latitude]",  # Define position coordinates
        get_elevation="rainfall_scaled",  # Elevation based on average rainfall
        elevation_scale=1,  # Scale the elevation for better visualization
        get_fill_color="color",  # Set fill color (red with transparency)
        radius=200,  # Set radius for the columns
        pickable=True,  # Allow clicking on the columns
        auto_highlight=True,  # Highlight columns on hover
        extruded=True,

    )

    # Set the initial viewport point for the map
    view_state = pdk.ViewState(
        latitude=13.0827,
        longitude=80.2707,
        zoom=11,
        pitch=50,  # Adjust the pitch for better 3D effect
    )

    # Render the map
    r = pdk.Deck(
        layers=[user_location_layer, layer],
        initial_view_state=view_state,
        tooltip={
            "text": "Place: {Station} \n Average Rainfall: {Average Rainfall} mm/year"},
    )

    r.to_html("templates/chennai_rainfall_map.html")


def create_rainfall_dashboard_layout():
    layout = html.Div([
        dbc.RadioItems(
            id='rainfall-data-selection',
            options=[
                {'label': 'Monthly Rainfall Across Years', 'value': 'monthly'},
                {'label': 'Total Annual Rainfall', 'value': 'annual'},
                {'label': 'Rainfall Map', 'value': 'map'},
            ],
            value='monthly',  # Default value
            inline=True,
            className='mb-4 mx-auto d-flex justify-content-around',
            style={'font-size': '1.2em', 'font-weight': 'bold'}
        ),
        html.Div(id='rainfall-content-container')
    ], className='p-3 border border-3 rounded', style={'background-color': '#aed3fc'})
    return layout


def plot_ground_water_level(station_name, df):
    station_df = df[df['Station_name'] == station_name].copy()

    # Ensure 'Date' is in the correct datetime format and sorted
    station_df['Date'] = pd.to_datetime(station_df['Date'])
    station_df.sort_values('Date', inplace=True)

    fig = px.line(station_df, x='Date', y='level',
                  title=f'Ground Water Level for Station: {station_name}',
                  markers=True,  # Add markers to the line
                  line_shape='linear',  # Define the line shape
                  color_discrete_sequence=['#00008B'],
                  )  # Set a color sequence

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Water Level (meters)',
        title_font=dict(size=20, family='Arial', color='rgb(37,37,37)'),
        xaxis=dict(
            showline=True,
            showgrid=False,
            gridcolor='rgb(240, 240, 240)',
            showticklabels=True,
            linecolor='#8B8000',
            linewidth=2,
            ticks='outside',
            tickfont=dict(family='Arial', size=12, color='rgb(82, 82, 82)'),
            tickangle=45  # Angle the date labels to prevent overlap
        ),
        yaxis=dict(
            showline=True,
            showgrid=False,
            gridcolor='rgb(240, 240, 240)',
            showticklabels=True,
            linecolor='#8B8000',
            linewidth=2,
            ticks='outside',
            tickfont=dict(family='Arial', size=12, color='rgb(82, 82, 82)'),
            autorange="reversed"
        ),
        autosize=True,
        margin=dict(autoexpand=True, l=100, r=20, t=110, b=70),
        showlegend=True,
        plot_bgcolor='white'
    )
    fig.update_layout(
        xaxis={"mirror": "allticks", 'side': 'top'},
    )
    # Customize the hover template
    fig.update_traces(
        hovertemplate='Date: %{x|%Y-%m-%d}<br>Level: %{y:.2f} meters')

    return fig


def plot_ground_water_level_last_year(station_name, df):
    # Filter the DataFrame for the given station name
    station_df = df[df['Station_name'] == station_name].copy()

    # Filter the DataFrame for the last year
    last_year = station_df['Year'].max()
    last_year_df = station_df[station_df['Year'] == last_year].copy()

    # Ensure 'Date' is in the correct datetime format and sorted
    last_year_df['Date'] = pd.to_datetime(last_year_df['Date'])
    last_year_df.sort_values('Date', inplace=True)

    # Create the plot
    fig = px.line(last_year_df, x='Date', y='level',
                  title=f'Ground Water Level for Station: {station_name} in {last_year}',
                  markers=True,
                  line_shape='linear',
                  color_discrete_sequence=['#00008B'])

    # Customize the layout
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Water Level (meters)',
        title_font=dict(size=20, family='Arial', color='rgb(37,37,37)'),
        xaxis=dict(
            showline=True,
            showgrid=False,
            gridcolor='rgb(230, 230, 230)',
            showticklabels=True,
            linecolor='#8B8000',
            linewidth=2,
            ticks='outside',
            tickfont=dict(family='Arial', size=12, color='rgb(82, 82, 82)'),
            tickangle=45
        ),
        yaxis=dict(
            showline=True,
            showgrid=False,
            gridcolor='rgb(230, 230, 230)',
            showticklabels=True,
            linecolor='#8B8000',
            linewidth=2,
            ticks='outside',
            tickfont=dict(family='Arial', size=12, color='rgb(82, 82, 82)'),
            autorange="reversed"
        ),
        autosize=True,
        margin=dict(autoexpand=True, l=100, r=20, t=110, b=70),
        showlegend=False,
        plot_bgcolor='white'
    )
    fig.update_layout(
        xaxis={"mirror": "allticks", 'side': 'top'},
    )

    fig.update_traces(
        hovertemplate='Date: %{x|%Y-%m-%d}<br>Level: %{y:.2f} meters')

    return fig


def create_ground_water_map(lat, long):
    user_location_data = pd.DataFrame({"latitude": [lat], "longitude": [long]})
    df = pd.read_csv(
        "waterflow/ground_water_level_combined_sorted.csv",
    )

    df = df.groupby('Station_name').agg({
        'State': 'first',
        'District': 'first',
        'Agency_name': 'first',
        'Date': 'first',  # Assuming you want to keep the first date, adjust if needed
        'level': 'mean',  # Calculate the mean level
        'lat': 'first',
        'long': 'first',
        'Telemetry': 'first',
        'Year': 'first'  # Assuming you want to keep the first year, adjust if needed
    }).reset_index()

    df["level_scaled"] = df["level"] * 500

    df["level"] = df["level"].round(2)

    df["normalized_value"] = (df["level_scaled"] - df["level_scaled"].min()) / (
        df["level_scaled"].max() - df["level_scaled"].min()
    )

    # Define a color gradient function
    def get_color(value):
        blue = [0, 0, 255, 255]  # Low values
        red = [255, 0, 0, 255]  # High values
        return [int(red[i] + (blue[i] - red[i]) * value) for i in range(4)]

    df["color"] = df["normalized_value"].apply(get_color)
    user_location_layer = pdk.Layer(
        "ScatterplotLayer",
        user_location_data,
        get_position=["longitude", "latitude"],
        get_color="[255, 255, 217, 100]",  # Red color, semi-transparent
        get_radius=2000,  # Adjust the size of the circle
        pickable=False,

    )
    # Define a layer to visualize the data
    layer = pdk.Layer(
        "ColumnLayer",  # Specify the layer type
        data=df,  # Pass the DataFrame
        get_position="[long, lat]",  # Define position coordinates
        get_elevation="level_scaled",  # Elevation based on average rainfall
        elevation_scale=1,  # Scale the elevation for better visualization
        get_fill_color="color",  # Set fill color (red with transparency)
        radius=200,  # Set radius for the columns
        pickable=True,  # Allow clicking on the columns
        auto_highlight=True,  # Highlight columns on hover
        extruded=True,

    )

    # Set the initial viewport point for the map
    view_state = pdk.ViewState(
        latitude=13.0827,
        longitude=80.2707,
        zoom=11,
        pitch=50,  # Adjust the pitch for better 3D effect
    )

    # Render the map
    r = pdk.Deck(
        layers=[user_location_layer, layer],
        initial_view_state=view_state,
        tooltip={
            "text": "Place: {Station_name} \n Ground Water Level: {level} metres (across years)"},
    )

    r.to_html("templates/ground_water_map.html")


def create_ground_water_dashboard_layout(user):
    return html.Div([
        dbc.RadioItems(
            id='data-selection',
            options=[
                {'label': 'Overall Ground Water Level', 'value': 'overall'},
                {'label': 'Recently measured Ground Water Level', 'value': 'last_year'},
                {'label': 'Ground Water Map', 'value': 'map'},
            ],
            value='overall',
            inline=True,
            className='mb-4 mx-auto d-flex justify-content-around',
            style={'font-size': '1.2em', 'font-weight': 'bold'},
        ),
        html.Div(id='content-container', children='Select an option')
    ], className='m-3 p-3 border border-3 rounded', style={'background-color': '#aed3fc'})


def create_quality_bubble_map(user):
    df = pd.read_csv(
        'waterflow/ground_water_quality_merged_sorted_chennai.csv')

    attributes = [col for col in df.columns if col not in ['Latitude', 'Longitude', 'Station Name', 'State Name',
                                                           'District Name', 'Basin Name', 'Sub Basin Name', 'Agency Name', 'Date Collection'] and df[col].notna().any()]

    if not attributes:
        return html.Div("No attributes with available data.")

    initial_attribute = attributes[0]

    layout = html.Div([
        html.Div([
            dcc.Dropdown(
                id='attribute-selector',
                options=[{'label': attr, 'value': attr}
                         for attr in attributes],
                value=initial_attribute
            )], className='p-3 w-90'),  # Adjust the dropdown width as necessary
        html.Div([  # Container Div for map and line chart
            html.Div([
                dcc.Graph(id='ground-water-map')
            ], className='p-1', style={'width': '60%'}),  # Set width to 60% for the map
            html.Div([
                dcc.Graph(id='ground-water-quality-line-chart')
            ], className='p-1', style={'width': '40%'}),  # Set width to 40% for the line chart
        ], className='d-flex'),  # Flexbox layout to arrange children side by side
    ], className='p-3 border border-3 rounded', style={'background-color': '#aed3fc'})

    return layout


def create_surface_water_quality_map(user):
    df = pd.read_csv('waterflow/surface_water_quality_chennai.csv')

    attributes = [col for col in df.columns if col not in ['Latitude', 'Longitude', 'Station Name', 'State Name', 'District Name', 'Basin Name', 'Sub Basin Name', 'Agency Name', 'Date Collection'] and df[col].notna().any()]
    initial_attribute = attributes[0]

    layout = html.Div([
        html.Div([
            dcc.Dropdown(
                id='surface-water-attribute-selector',
                options=[{'label': attr, 'value': attr} for attr in attributes],
                value=initial_attribute
            )], className='p-3 w-90'),  
        html.Div([  
            html.Div([
                dcc.Graph(id='surface-water-map')
            ], className='p-1', style={'width': '60%'}),  
            html.Div([
                dcc.Graph(id='surface-water-quality-line-chart')
            ], className='p-1', style={'width': '40%'}),  
        ], className='d-flex'),  
    ], className='p-3 border border-3 rounded', style={'background-color': '#aed3fc'})

    return layout
