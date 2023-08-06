#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import math
from datetime import datetime
from os.path import exists

import pandas as pd
from scipy import spatial


def cartesian(latitude, longitude):  # , elevation=0):
    # Convert to radians
    latitude = latitude * (math.pi / 180)
    longitude = longitude * (math.pi / 180)

    r = 6371  # 6378137.0 + elevation  # relative to centre of the earth
    x = r * math.cos(latitude) * math.cos(longitude)
    y = r * math.cos(latitude) * math.sin(longitude)
    z = r * math.sin(latitude)
    return x, y, z


class NearestPoint:
    def __init__(self, points_dataframe, headers=None, distance_keyword="distance"):

        if isinstance(points_dataframe, pd.DataFrame):
            self.points_dataframe = points_dataframe
        elif isinstance(points_dataframe, str):
            file_exists = exists(points_dataframe)
            assert file_exists, "File does not exist. Please provide absolute path."
            self.points_dataframe = pd.read_csv(points_dataframe)
        else:
            logging.error("points_dataframe should be Dataframe or Dataframe path.")

        self.headers = headers if headers else ["point_id", "latitude", "longitude"]
        self.distance_keyword = distance_keyword
        assert (
            3 == self.headers.__len__()
        ), "Dataframe headers should be 3 items. Select 3 columns from dataframe."

        logging.debug(f"Places generating. {datetime.now()}")
        places = []
        for index, row in self.points_dataframe.iterrows():
            coordinates = [row[self.headers[1]], row[self.headers[2]]]
            cartesian_coord = cartesian(*coordinates)
            places.append(cartesian_coord)
        logging.debug(f"Places generated. {datetime.now()}")

        self.tree = spatial.KDTree(places)

    def get_nearest(self, lat, lon):
        logging.debug(f"Finding nearest point for latitude: {lat} and longitude: {lon}")
        cartesian_coord = cartesian(lat, lon)
        closest = self.tree.query([cartesian_coord], p=2)
        index = closest[1][0]
        return {
            f"{self.headers[0]}": self.points_dataframe.get(self.headers[0])[index].item(),
            f"{self.headers[1]}": self.points_dataframe.get(self.headers[1])[index].item(),
            f"{self.headers[2]}": self.points_dataframe.get(self.headers[2])[index].item(),
            f"{self.distance_keyword}": closest[0][0].item(),
        }
