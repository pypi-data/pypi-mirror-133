import numpy as np

import napari_tabu
import pytest


def test_something_with_viewer(make_napari_viewer):

    viewer = make_napari_viewer()
    num_dw = len(viewer.window._dock_widgets)
    from napari_tabu._dock_widget import SendBackWidget

    viewer.window.add_dock_widget(
        SendBackWidget(viewer, viewer)
    )
    assert len(viewer.window._dock_widgets) == num_dw + 1

    from napari_tabu._dock_widget import _add_layer_to_viewer

    image_layer = viewer.add_image(np.random.random((10, 10)))
    labels_layer = viewer.add_labels(np.random.random((10, 10)).astype(int))
    points_layer = viewer.add_points(np.random.random((2, 2)))
    shapes_layer = viewer.add_shapes(np.random.random((2, 2)))


    _add_layer_to_viewer(image_layer, viewer)
    _add_layer_to_viewer(labels_layer, viewer)
    _add_layer_to_viewer(points_layer, viewer)
    _add_layer_to_viewer(shapes_layer, viewer)
