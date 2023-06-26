import dash
from dash import html, dcc
import numpy as np
from dash.dependencies import Input, Output, State, ALL
from dash import callback_context
from scipy.spatial.distance import cdist
from typing import List, Tuple

WIDTH: float = 100
HEIGHT: float = 100
INTERVAL: int = 64  # Milliseconds
DEBUG = False


def main_dash():
    # Create the Dash application
    app = initialize_dash_app()

    play: bool = False
    creature_positions: np.ndarray[float, np.dtype[np.float64]] = np.array([])
    food_positions: np.ndarray[float, np.dtype[np.float64]] = np.array([])

    @app.callback(
        Output("frame-counter", "children"),
        Output("map-container", "children"),
        Input("interval-component", "n_intervals"),
        Input("start-button", "n_clicks"),
        Input("stop-button", "n_clicks"),
        State("num-creatures-input", "value"),
        State("num-food-input", "value"),
        State("num-growth-rate-input", "value"),
    )
    def update_interval(
        frame_counter: int,
        start_clicks: int,
        stop_clicks: int,
        num_creatures: int,
        num_food: int,
        food_growth_rate: float,
        width: float = WIDTH,
        height: float = HEIGHT,
    ) -> Tuple[int, List[html.Div]]:
        nonlocal play, creature_positions, food_positions

        if DEBUG == True:
            print("Frame Counter:", frame_counter)
            print("Start Clicks:", start_clicks)
            print("Stop Clicks:", stop_clicks)
            print("Num Creatures:", num_creatures)
            print("Num Food:", num_food)

        ctx = callback_context

        if ctx.triggered:
            # Get the ID of the component that triggered the callback
            triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

            if triggered_id == "start-button":
                # Check if the start button was clicked
                creature_positions = initialize_creatures(num_creatures, width, height)
                food_positions = initialize_food(num_food, width, height)
                play = True

                # Reset the stop button click count
                stop_clicks = 0
                if DEBUG:
                    print("Start!")

            elif triggered_id == "stop-button":
                # Check if the stop button was clicked
                play = False
                creature_positions = np.array([])
                food_positions = np.array([])

                # Reset the start button click count
                start_clicks = 0
                if DEBUG:
                    print("Stop!")

        if play:
            # Update the positions based on simulation logic
            creature_positions = update_positions(creature_positions)
            food_positions = eat_food(food_positions, creature_positions)
            food_positions = grow_food(food_positions, food_growth_rate)

            if DEBUG:
                print("Playing!")

        # Create the creature elements, food elements, and map elements
        creature_elements = [
            html.Div(
                style={
                    "position": "absolute",
                    "left": f"{position[0] / width * 100}%",
                    "top": f"{position[1] / height * 100}%",
                    "width": "10px",
                    "height": "10px",
                    "background-color": "red",
                    "border-radius": "50%",  # Make the element round
                }
            )
            for position in creature_positions
        ]

        food_elements = [
            html.Div(
                style={
                    "position": "absolute",
                    "left": f"{position[0] / width * 100}%",
                    "top": f"{position[1] / height * 100}%",
                    "width": "5px",
                    "height": "5px",
                    "background-color": "green",
                }
            )
            for position in food_positions
        ]

        map_elements = creature_elements + food_elements

        return frame_counter, map_elements

    # Run the Dash application
    app.run_server(debug=True)


def initialize_dash_app() -> dash.Dash:
    # Create the Dash application
    app = dash.Dash(__name__)

    # Define the layout of the application
    app.layout = html.Div(
        [
            html.Label("Initial number of Creatures:"),
            dcc.Input(id="num-creatures-input", type="number", min=1, value=5),
            html.Label("Initial number of Food:"),
            dcc.Input(id="num-food-input", type="number", min=1, value=10),
            html.Label("Food Growth Rate:"),
            dcc.Input(id="num-growth-rate-input", type="number", min=0, value=0.5),
            html.Button("Start", id="start-button", n_clicks=0),
            html.Button("Stop", id="stop-button", n_clicks=0),
            dcc.Interval(id="interval-component", interval=INTERVAL, n_intervals=0),
            html.Div(id="frame-counter"),
            html.Div(
                id="map-container",
                style={
                    "backgroundColor": "white",
                    "border": "1px solid black",
                    "width": "100%",  # Twice as long
                    "margin": "auto",  # Center the container
                    "height": "600px",  # Set the height of the container
                    "position": "relative",  # Enable positioning of elements inside the container
                },
            ),
        ]
    )

    return app
