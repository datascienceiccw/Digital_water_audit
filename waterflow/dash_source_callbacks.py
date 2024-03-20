from dash import html, dcc, Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output
import pandas as pd
from .dash_source_useful_fn import (normalize_sizes, create_pie_chart_for_source, create_pie_chart_for_tank, find_nearest_location,
                              plot_ground_water_level, plot_ground_water_level_last_year, create_ground_water_map,
                              plot_monthly_rainfall_across_years, plot_total_annual_rainfall, create_rainfall_map,
                              create_treemap_for_tank)
from decouple import config
MAPBOX_ACCESS_TOKEN = config("MAPBOX_ACCESS_TOKEN")

def register_callbacks_for_source_water_distribution(app, user):
    @app.callback(
        Output('water-distribution-content-container', 'children'),
        [Input('water-distribution-selection', 'value')]
    )
    def update_water_distribution_content(selected_value):
        if selected_value == 'source_distribution':
            fig = create_pie_chart_for_source(user, "Source Category")
            return dcc.Graph(id="water-source-distribution-plot", figure=fig, config={
                'responsive': True  # Ensure the graph is responsive
            })

        elif selected_value == 'tank_distribution':
            fig = create_treemap_for_tank(user, "Tank Category")
            return dcc.Graph(id="water-tank-distribution-plot", figure=fig, config={
                'responsive': True  # Ensure the graph is responsive
            })


def register_callbacks_for_ground_water_level(app, user):
    @app.callback(
        Output('content-container', 'children'),
        [Input('data-selection', 'value')]
    )
    def update_ground_water_content(selected_value):
        nearest_station, lat, lon = find_nearest_location(
            user, "waterflow/ground_water_level_combined_sorted.csv")

        if selected_value == 'overall':
            fig = plot_ground_water_level(nearest_station, pd.read_csv(
                "waterflow/ground_water_level_combined_sorted.csv"))
            return dcc.Graph(id="ground-water-level-plot", figure=fig)

        elif selected_value == 'last_year':
            fig = plot_ground_water_level_last_year(nearest_station, pd.read_csv(
                "waterflow/ground_water_level_combined_sorted.csv"))
            return dcc.Graph(id="ground-water-level-plot-last-year", figure=fig)

        elif selected_value == 'map':
            create_ground_water_map(lat, lon)
            return html.Iframe(srcDoc=open('templates/ground_water_map.html').read(), width='100%', height='500px')

        return html.Div("Select an option to view the data.")


def register_callbacks_for_rainwater(app, user):
    @app.callback(
        Output('rainfall-content-container', 'children'),
        [Input('rainfall-data-selection', 'value')]
    )
    def update_rainfall_content(selected_value):
        if selected_value == 'monthly':
            fig = plot_monthly_rainfall_across_years()
            return dcc.Graph(id="monthly-rainfall-plot", figure=fig)
        elif selected_value == 'annual':
            fig = plot_total_annual_rainfall()
            return dcc.Graph(id="annual-rainfall-plot", figure=fig)
        elif selected_value == 'map':
            create_rainfall_map(user)  # Ensure user info is passed correctly
            return html.Iframe(srcDoc=open('templates/chennai_rainfall_map.html').read(), width='100%', height='600px')


def register_callbacks_for_ground_water_quality(app):
    @app.callback(
        Output('ground-water-map', 'figure'),
        [Input('attribute-selector', 'value')]
    )
    def update_ground_water_map(selected_attribute):
        df = pd.read_csv(
            'waterflow/ground_water_quality_merged_sorted_chennai.csv')
        df = df[df[selected_attribute].notna()]

        # Group by location to calculate average values
        grouped_df = df.groupby(['Latitude', 'Longitude'], as_index=False)[
            selected_attribute].mean()
        # Normalize bubble sizes based on the average values
        normalized_sizes = normalize_sizes(grouped_df[selected_attribute])

        fig = go.Figure(go.Scattermapbox(
            lat=grouped_df['Latitude'],
            lon=grouped_df['Longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=normalized_sizes,
                color=grouped_df[selected_attribute],
                colorscale='Viridis',
                showscale=True,
                sizemode='diameter',
                colorbar=dict(title=f"Average {selected_attribute}"),
            ),
            # Displaying average value rounded to 2 decimal places
            text=grouped_df[selected_attribute].apply(lambda x: f"{x:.2f}"),
            hovertemplate='<b>Average Value</b>: %{text} (across years)<extra></extra>'
        ))

        fig.update_layout(
            mapbox=dict(
                accesstoken=MAPBOX_ACCESS_TOKEN,
                style='dark',
                zoom=10,
                center=dict(lat=13.0827, lon=80.2707)
            ),
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )

        return fig

    @app.callback(
        Output('ground-water-quality-line-chart', 'figure'),
        [Input('ground-water-map', 'clickData'),
         Input('attribute-selector', 'value')]
    )
    def update_line_chart(clickData, selected_attribute):
        if clickData is None or 'points' not in clickData:
            return {
                'data': [],
                'layout': {
                    'title': 'Select a Bubble on the Map',
                    'xaxis': {'title': 'Year'},
                    'yaxis': {'title': f'{selected_attribute}'}
                },
            }

        lat = clickData['points'][0]['lat']
        lon = clickData['points'][0]['lon']
        df = pd.read_csv(
            'waterflow/ground_water_quality_merged_sorted_chennai.csv')
        df['Date Collection'] = pd.to_datetime(df['Date Collection'])

        station_data = df[(df['Latitude'] == lat) & (df['Longitude'] == lon)]

        if station_data.empty:
            raise PreventUpdate

        fig = px.line(
            station_data,
            x='Date Collection',
            y=selected_attribute,
            markers=True,
            title=f'Time Series for {selected_attribute}',
            color_discrete_sequence=['#00008B']
        )

        fig.update_layout(
            xaxis_title='Date',
            yaxis_title=f'{selected_attribute}',
            title_font=dict(size=20, family='Arial', color='rgb(37,37,37)'),
            xaxis=dict(
                showline=True,
                showgrid=False,
                gridcolor='rgb(230, 230, 230)',
                showticklabels=True,
                linecolor='#8B8000',
                linewidth=2,
                ticks='outside',
                tickfont=dict(family='Arial', size=12,
                              color='rgb(82, 82, 82)'),
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
                tickfont=dict(family='Arial', size=12,
                              color='rgb(82, 82, 82)'),
            ),
            autosize=True,
            margin=dict(autoexpand=True, l=100, r=20, t=110, b=70),
            showlegend=False,
            plot_bgcolor='white'
        )
        fig.update_traces(marker=dict(color='black', size=7),
                          selector=dict(mode='markers'))

        return fig


def register_surface_water_callbacks(app):
    @app.callback(
        Output('surface-water-map', 'figure'),
        [Input('surface-water-attribute-selector', 'value')]
    )
    def update_surface_water_map(selected_attribute):
        df = pd.read_csv('waterflow/surface_water_quality_chennai.csv')
        df = df[df[selected_attribute].notna()]

        # Group by location to calculate average values for the map
        avg_df = df.groupby(['Latitude', 'Longitude'], as_index=False)[selected_attribute].mean()
        
        # Normalize bubble sizes based on the average values
        normalized_sizes = normalize_sizes(avg_df[selected_attribute])

        fig = go.Figure(go.Scattermapbox(
            lat=avg_df['Latitude'],
            lon=avg_df['Longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=normalized_sizes,
                color=avg_df[selected_attribute],
                colorscale='hot',
                showscale=True,
                sizemode='diameter'
            ),
            text=avg_df[selected_attribute].apply(lambda x: f'{x:.2f}'),
            hovertemplate='<b>Average Value</b>: %{text} (across years)<extra></extra>'
        ))

        fig.update_layout(
            mapbox=dict(
                accesstoken=MAPBOX_ACCESS_TOKEN, 
                style='dark',
                zoom=10,
                center=dict(lat=13.0827, lon=80.2707)
            ),
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )

        return fig

    @app.callback(
        Output('surface-water-quality-line-chart', 'figure'),
        [Input('surface-water-map', 'clickData'),
         Input('surface-water-attribute-selector', 'value')]
    )
    def update_surface_water_line_chart(clickData, selected_attribute):
        if clickData is None or 'points' not in clickData:
            return {
                'data': [],
                'layout': {
                    'title': 'Select a Bubble on the Map',
                    'xaxis': {'title': 'Year'},
                    'yaxis': {'title': f'{selected_attribute}'}
                },
            }

        lat = clickData['points'][0]['lat']
        lon = clickData['points'][0]['lon']
        df = pd.read_csv('waterflow/surface_water_quality_chennai.csv')
        df['Date Collection'] = pd.to_datetime(df['Date Collection'])
        station_data = df[(df['Latitude'] == lat) & (df['Longitude'] == lon)]
        
        if station_data.empty:
            raise PreventUpdate

        fig = px.line(
            station_data,
            x='Date Collection',
            y=selected_attribute,
            markers=True,
            title=f'Time Series for {selected_attribute}',
            color_discrete_sequence=['#00008B']
        )

        fig.update_layout(
            xaxis_title='Date',
            yaxis_title=f'{selected_attribute}',
            title_font=dict(size=20, family='Arial', color='rgb(37,37,37)'),
            xaxis=dict(
                showline=True,
                showgrid=False,
                gridcolor='rgb(230, 230, 230)',
                showticklabels=True,
                linecolor='#8B8000',
                linewidth=2,
                ticks='outside',
                tickfont=dict(family='Arial', size=12,
                              color='rgb(82, 82, 82)'),
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
                tickfont=dict(family='Arial', size=12,
                              color='rgb(82, 82, 82)'),
            ),
            autosize=True,
            margin=dict(autoexpand=True, l=100, r=20, t=110, b=70),
            showlegend=False,
            plot_bgcolor='white'
        )
        fig.update_traces(marker=dict(color='black', size=7),
                          selector=dict(mode='markers'))

        return fig
