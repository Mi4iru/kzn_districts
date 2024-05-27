import pandas as pd
from ipyleaflet import Map, Marker, Polygon, FullScreenControl, LegendControl
from ipywidgets import Layout


class MapRenderer:
    def __init__(self, district_data: pd.DataFrame, points_data: pd.DataFrame):
        self.__points_data = points_data
        self.__district_data = district_data

    def get_map(self) -> Map:
        """
        TODO:
        - Создать карту с центром в центре города (с медианой lat и медианой lon)
        - Для каждого района нарисовать Polygon с цветом районом
        - Для каждого района нарисовать неперемещаемый Marker в центре района с title=<название_района>
        - Для каждого района добавить в LegendControl цвет с соответствующим именем района
        - Добавить FullScreenControl в карту
        - Использовать в карте Layout(width='100%', height='800px')
        """
        layout = Layout(width='100%', height='800px')
        m = Map(
            center=(55.795355, 49.107272),
            zoom=11,
            layout=layout
        )
        d = {}

        for idx, row in self.__district_data.iterrows():
            d[row['district']] = row['color']
            points = row['points'][2:-2]
            points = points.replace('(', '')
            points = [i for i in points.split('), ')]
            points = [i.split(', ') for i in points]
            for i in range(len(points)):
                points[i] = (float(points[i][0]), float(points[i][1]))
                polygon = Polygon(

                    locations=points,
                    color=row['color'],
                    fill_color=row['color'],
                    fill_opacity=0.02
                )
                m.add(polygon)
                center = row['center']
                center = [float(i) for i in center[1:-1].split(', ')]
                marker = Marker(location=center, draggable=False, title=row['district'])
                m.add(marker)
        legend = LegendControl(d, title='Районы Казани', position='bottomright')
        m.add(legend)
        m.add(FullScreenControl())
        return m
