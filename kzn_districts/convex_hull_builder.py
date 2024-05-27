import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from rich.jupyter import display


class ConvexHullBuilder:
    def __init__(self, points: pd.DataFrame):
        self.__points = points

    @property
    def get_convex_hull(self) -> pd.DataFrame:
        """
        Формат выходного датафрейма:
        - district
            Название района
        - points
            Список точек выпуклой оболочки района
        - center
            Кортеж центра района (lat, lon)
        - color
            Цвет оболочки района
        """
        districts = {}
        data = {'district': [], 'points': [], 'center': [],
             'color': ['green', 'blue', 'yellow', 'red', 'pink', 'white', 'black', 'brown']}
        for i in self.__points['district'].unique():
            lats = self.__points[self.__points["district"] == i]['lat'].to_list()
            lons = self.__points[self.__points["district"] == i]['lon'].to_list()
            districts[i] = [(lats[idx], lons[idx]) for idx in range(len(lats))]
            points, center = self.shell(districts[i])
            data['district'].append(i)
            data['points'].append(points)
            data['center'].append(center)
        df = pd.DataFrame(data)
        return df

    @staticmethod
    def angle(point, dawn_point):
        if point == dawn_point:
            return 0
        vec = (100 * (point[0] - dawn_point[0]), 100 * (point[1] - dawn_point[1]))
        scallar = vec[0] * 1 / math.sqrt(vec[0] ** 2 + vec[1] ** 2)
        return math.acos(scallar)

    @staticmethod
    def centroid(vertexes):
        x_list = [vertex[0] for vertex in vertexes]
        y_list = [vertex[1] for vertex in vertexes]
        _len = len(vertexes)
        x = sum(x_list) / _len
        y = sum(y_list) / _len
        return (x, y)

    def shell(self, points):
        dawn_point = sorted(points, key=lambda x: x[1])[0]

        points = sorted(points, key=lambda x: self.angle(x, dawn_point))

        stack = [points[-1], points[0], points[1]]

        vec1 = (stack[1][0] - stack[0][0], stack[1][1] - stack[0][1])
        vec2 = (stack[2][0] - stack[1][0], stack[2][0] - stack[1][1])
        rotate = vec1[0] * vec2[1] - vec1[1] * vec2[0]

        for i in points[2:]:

            vec1 = (stack[-1][0] - stack[-2][0], stack[-1][1] - stack[-2][1])
            vec2 = (i[0] - stack[-1][0], i[1] - stack[-1][1])

            if (vec1[0] * vec2[1] - vec1[1] * vec2[0]) * rotate > 0:
                stack.append(i)

            else:
                stack.pop(-1)

                vec1 = (stack[-1][0] - stack[-2][0], stack[-1][1] - stack[-2][1])
                vec2 = (i[0] - stack[-1][0], i[1] - stack[-1][1])

                while (vec1[0] * vec2[1] - vec1[1] * vec2[0]) * rotate < 0:
                    stack.pop(-1)
                    vec1 = (stack[-1][0] - stack[-2][0], stack[-1][1] - stack[-2][1])
                    vec2 = (i[0] - stack[-1][0], i[1] - stack[-1][1])
                stack.append(i)

        center = self.centroid(stack)
        return stack, center



