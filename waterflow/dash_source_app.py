from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
from .dash_source_useful_fn import (create_source_water_distribution_dashboard_layout,
                                    create_rainfall_map, create_quality_bubble_map,
                                    create_ground_water_dashboard_layout, create_rainfall_dashboard_layout,
                                    create_surface_water_quality_map)
from .dash_source_callbacks import (register_callbacks_for_ground_water_quality,
                                    register_callbacks_for_source_water_distribution,
                                    register_callbacks_for_ground_water_level,
                                    register_callbacks_for_rainwater,
                                    register_surface_water_callbacks)


def create_tabs(user, app):
    create_rainfall_map(user)

    tree_map_tab = dbc.Card(
        dbc.CardBody(
            [
                html.Div(create_source_water_distribution_dashboard_layout(user),
                         className='mt-5 p-2 border rounded bg-light'),
            ]
        ),
        className="custom-tab", style={'background-color': '#111212'}
    )

    rainwater_tab = dbc.Card(
        dbc.CardBody(
            [
                html.Div(create_rainfall_dashboard_layout(),
                         className='mt-5 p-2 border rounded bg-light'),
            ]
        ),
        className="custom-tab", style={'background-color': '#111212'}
    )
    ground_water_level_tab = dbc.Card(
        dbc.CardBody(
            [
                html.Div(create_ground_water_dashboard_layout(user),
                         className='mt-5 p-2 border rounded bg-light'),
            ]
        ),
        className="custom-tab", style={'background-color': '#111212'}
    )
    ground_water_quality_tab = dbc.Card(
        dbc.CardBody(
            [
                html.Div(create_quality_bubble_map(user),
                         className='mt-5 p-2 border rounded bg-light'),
            ]
        ),
        className="custom-tab", style={'background-color': '#111212'}
    )
    surface_water_quality_tab = dbc.Card(
        dbc.CardBody(
            [
                html.Div(create_surface_water_quality_map(user),
                         className='mt-5 p-2 border rounded bg-light'),
            ]
        ),
        className="custom-tab", style={'background-color': '#111212'}
    )

    tabs = html.Div([
        dbc.Tabs(
            [
                dbc.Tab(tree_map_tab, tab_id="tab-1", label="Source Water",
                        label_style={'font-size': '20px'}),
                dbc.Tab(rainwater_tab, tab_id="tab-2", label="Rainwater",
                        label_style={'font-size': '20px'}),
                dbc.Tab(ground_water_level_tab, tab_id="tab-3", label="Ground Water Level",
                        label_style={'font-size': '20px'}),
                dbc.Tab(ground_water_quality_tab, tab_id="tab-4", label="Ground Water Quality",
                        label_style={'font-size': '20px'}),
                dbc.Tab(surface_water_quality_tab, tab_id="tab-5", label="Surface Water Quality",
                        label_style={'font-size': '20px'}),
            ],
            id="tabs",
            active_tab="tab-1",
            className="nav nav-tabs d-flex justify-content-around bg-light badge badge-primary text-wrap ",
            style={'position': 'fixed', 'top': 0,
                   'zIndex': 1000, 'width': '100%', }
        ),
    ],
    )

    return tabs


def create_user_dash_app(user):
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = DjangoDash('SourceWaterAnalytics',
                     external_stylesheets=external_stylesheets)

    app.layout = html.Div([
        create_tabs(user, app)
    ],)

    @app.expanded_callback(
        Output("iframe-container", "children"),
        [Input("tabs", "active_tab")]
    )
    def update_iframe(active_tab):
        if active_tab == "tab-1":
            return html.Iframe(src="/show-map-view/")
        else:
            return html.Div()

    register_callbacks_for_source_water_distribution(app, user)
    register_callbacks_for_ground_water_level(app, user)
    register_callbacks_for_ground_water_quality(app)
    register_callbacks_for_rainwater(app, user)
    register_surface_water_callbacks(app)

    return app
