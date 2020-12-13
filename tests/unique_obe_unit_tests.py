import unittest
import json

from code_pipeline.tests_evaluation import RoadTestEvaluator

from numpy import linspace



import matplotlib.colors as mc
import colorsys

from shapely.geometry import Point, LineString
from matplotlib import pyplot as plt
import matplotlib.patches as patches

from descartes import PolygonPatch


def _adjust_lightness(color, amount=0.5):
    """
        https://stackoverflow.com/questions/37765197/darken-or-lighten-a-color-in-matplotlib
    """
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])


def _plot_road_segments(segments, fig = None, title=None):
    the_figure = fig
    if not the_figure:
        the_figure = plt.figure()

    color_map_turn = ['r', 'b']
    color_map_straights = ['g', 'c']
    # style_map = 's'

    lightness = linspace(0.1, 1.0, num=len(segments))

    # TODO Not sure which one we want to plot here...
    for id, segment in enumerate(segments):

        if segment["type"] == "straight":
            s = 's'
            c = color_map_straights[id % len(color_map_straights)]
        else:
            c = color_map_turn[id % len(color_map_turn)]
            s = 'o'

        c = _adjust_lightness(c, lightness[id])


        # Sector is a list of segments we need to merge their geometry
        # sector_poly = _build_polygon_from_geometry(segment.geometry)
        # https://stackoverflow.com/questions/55522395/how-do-i-plot-shapely-polygons-and-objects-using-matplotlib
        sector_poly = LineString([(p[0], p[1]) for p in segment["points"]]).buffer(8.0, cap_style=2,join_style=2)

        l, = plt.plot(*sector_poly.exterior.xy, marker='.', color=c)
        # _plot_nodes([(p[0], p[1]) for p in segment["points"]], c+s, 5, fig=the_figure )

    plt.gca().set_aspect('equal')

    if title:
        plt.gca().set_title(title)


def _plot_nodes(sample_nodes, style, markersize, fig = None, title=None):
    if not fig:
        plt.figure()

    xs = [n[0] for n in sample_nodes]
    ys = [n[1] for n in sample_nodes]

    plt.plot(xs, ys, style, markersize=markersize)

    plt.gca().set_aspect('equal')

    if title:
        plt.gca().set_title(title)


class UniqueOBETest(unittest.TestCase):

    def _load_execution_data(self, execution_data_file):
        # Load the execution data
        with open(execution_data_file) as input_file:
            execution_data = json.load(input_file)
        return execution_data

    def test_obe(self):
        execution_data_1 = self._load_execution_data("./obes/execution_1/simulation.full.json")
        execution_data_2 = self._load_execution_data("./obes/execution_2/simulation.full.json")

        # Measure Similarity
        road_test_evaluation = RoadTestEvaluator()

        interesting_road_segments_oob_1 = road_test_evaluation.identify_interesting_road_segments(execution_data_1)
        interesting_road_segments_oob_2 = road_test_evaluation.identify_interesting_road_segments(execution_data_2)

        print(interesting_road_segments_oob_1)
        print(interesting_road_segments_oob_2)

        # TODO Given the interesting road segments for each OOB we should be able to compute "Uniqueness"
        # This can be done per competitor or for all the competitors

        # #####
        #
        # _plot_road_segments(interesting_road_segments )
        #
        # # New figure
        # plt.figure()
        # # Extract features from the MN road
        #
        # map_size = 200
        #
        # # plot the map
        # map_boundary = patches.Rectangle((0, 0), map_size, map_size, linewidth=1, edgecolor='black', facecolor='none')
        # plt.gca().add_patch(map_boundary)
        #
        # # plot the actual road as buffer
        # road_poly = road_line.buffer(8.0, cap_style=2,join_style=2)
        # patch = PolygonPatch(road_poly, fc='gray', ec='dimgray')  # ec='#555555', alpha=0.5, zorder=4)
        # plt.gca().add_patch(patch)
        #
        # road_poly_before = segment_before.buffer(8.0, cap_style=2, join_style=2)
        # patch_before = PolygonPatch(road_poly_before , fc='gray', ec='red', alpha=0.5)  # ec='#555555', alpha=0.5, zorder=4)
        # plt.gca().add_patch(patch_before)
        #
        # road_poly_after = segment_after.buffer(8.0, cap_style=2, join_style=2)
        # patch_after = PolygonPatch(road_poly_after, fc='gray', ec='green', alpha=0.5)  # ec='#555555', alpha=0.5, zorder=4)
        # plt.gca().add_patch(patch_after)
        #
        # # plot the interpolated road spine
        # # https://github.com/Toblerity/Shapely/blob/master/docs/code/linestring.py
        # x, y = road_line.xy
        # plt.plot(x, y, 'yellow')
        #
        #
        # x = [p.x for p in positions]
        # y = [p.y for p in positions]
        #
        # plt.plot(x, y, "b*")
        # plt.plot(oob_pos.x, oob_pos.y, "ro")
        # plt.plot(np.x, np.y, "gs")
        #
        # plt.gca().set_aspect('equal', 'box')
        # plt.gca().set(xlim=(-30, map_size + 30), ylim=(-30, map_size + 30))
        #
        # plt.show()