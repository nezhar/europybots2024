# SPDX-License-Identifier: BSD-3-Clause

# flake8: noqa F401
from collections.abc import Callable

import numpy as np

from vendeeglobe import (
    Checkpoint,
    Heading,
    Instructions,
    Location,
    Vector,
    config,
)
from vendeeglobe.utils import distance_on_surface


class Bot:
    """
    This is the ship-controlling bot that will be instantiated for the competition.
    """

    def __init__(self):
        self.team = "nezhar"  # This is your team name
        # This is the course that the ship has to follow
        self.course = [
            Checkpoint(latitude=43.797109, longitude=-11.264905, radius=50),
            Checkpoint(latitude=17.440436, longitude=-64.387514, radius=50),
            Checkpoint(latitude=11.264407, longitude=-80.741149, radius=50),
            Checkpoint(latitude=9.817736, longitude=-80.405538, radius=5),
            Checkpoint(latitude=7.764715, longitude=-78.767019, radius=50),
            Checkpoint(latitude=6.042875, longitude=-79.787996, radius=50),
            Checkpoint(latitude=2.806318, longitude=-168.943864, radius=1990.0),
            Checkpoint(latitude=-2.376610, longitude=159.575564, radius=50),
            Checkpoint(latitude=5.821937, longitude=129.145979, radius=50.0),
            Checkpoint(latitude=-0.417495, longitude=125.916342, radius=5.0),
            Checkpoint(latitude=-4.965513, longitude=128.122865, radius=5.0),
            Checkpoint(latitude=-10.141710, longitude=129.713751, radius=5.0),
            Checkpoint(latitude=-15.668984, longitude=77.674694, radius=1190.0),
            Checkpoint(latitude=13.768042, longitude=51.559097, radius=50),
            Checkpoint(latitude=12.246341, longitude=43.582764, radius=5),
            Checkpoint(latitude=27.493460, longitude=34.514343, radius=50),
            Checkpoint(latitude=28.307254, longitude=33.394979, radius=5),
            Checkpoint(latitude=29.066118, longitude=32.946602, radius=5),
            Checkpoint(latitude=29.566118, longitude=32.646602, radius=5),
            Checkpoint(latitude=30.079812, longitude=32.469881, radius=5),
            Checkpoint(latitude=30.724427, longitude=32.431557, radius=5),
            Checkpoint(latitude=32.522225, longitude=32.461793, radius=5),
            Checkpoint(latitude=36.332412, longitude=14.797698, radius=50),
            Checkpoint(latitude=38.278835, longitude=8.499950, radius=50),
            Checkpoint(latitude=35.992628, longitude=-5.406221, radius=5),
            Checkpoint(latitude=36.943703, longitude=-10.866803, radius=5),
            Checkpoint(latitude=46.797109, longitude=-11.264905, radius=5),
            Checkpoint(
                latitude=config.start.latitude,
                longitude=config.start.longitude,
                radius=5,
            ),
        ]

    def run(
        self,
        t: float,
        dt: float,
        longitude: float,
        latitude: float,
        heading: float,
        speed: float,
        vector: np.ndarray,
        forecast: Callable,
        world_map: Callable,
    ) -> Instructions:
        """
        This is the method that will be called at every time step to get the
        instructions for the ship.

        Parameters
        ----------
        t:
            The current time in hours.
        dt:
            The time step in hours.
        longitude:
            The current longitude of the ship.
        latitude:
            The current latitude of the ship.
        heading:
            The current heading of the ship.
        speed:
            The current speed of the ship.
        vector:
            The current heading of the ship, expressed as a vector.
        forecast:
            Method to query the weather forecast for the next 5 days.
            Example:
            current_position_forecast = forecast(
                latitudes=latitude, longitudes=longitude, times=0
            )
        world_map:
            Method to query map of the world: 1 for sea, 0 for land.
            Example:
            current_position_terrain = world_map(
                latitudes=latitude, longitudes=longitude
            )

        Returns
        -------
        instructions:
            A set of instructions for the ship. This can be:
            - a Location to go to
            - a Heading to point to
            - a Vector to follow
            - a number of degrees to turn Left
            - a number of degrees to turn Right

            Optionally, a sail value between 0 and 1 can be set.
        """
        # Initialize the instructions
        instructions = Instructions()

        # Go through all checkpoints and find the next one to reach
        for ch in self.course:
            # Compute the distance to the checkpoint
            dist = distance_on_surface(
                longitude1=longitude,
                latitude1=latitude,
                longitude2=ch.longitude,
                latitude2=ch.latitude,
            )
            instructions.sail = 1.0

            # Check if the checkpoint has been reached
            if dist < ch.radius:
                ch.reached = True
            if not ch.reached:
                instructions.location = Location(
                    longitude=ch.longitude, latitude=ch.latitude
                )
                break

        return instructions
