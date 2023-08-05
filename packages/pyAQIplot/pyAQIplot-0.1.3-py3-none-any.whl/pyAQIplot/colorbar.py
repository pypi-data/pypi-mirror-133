# -*- coding: utf-8 -*-
# Author: TAO Nianze (Augus)
"""
create colour-bar
"""
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import (
    ListedColormap,
    BoundaryNorm,
)
from .structure import rgb


c_map = ListedColormap(rgb)
bounds = [
    25,
    50,
    75,
    100,
    125,
    150,
    175,
    200,
    300,
    400
]
norm = BoundaryNorm(
    bounds,
    c_map.N,
    extend='both',
)


def create_colorbar() -> plt.figure:
    """
    create colour bar
    """
    fig, axis = plt.subplots(
        figsize=(10, 1),
    )
    fig.subplots_adjust(
        bottom=0.5,
    )
    fig.colorbar(
        cm.ScalarMappable(
            norm=norm,
            cmap=c_map,
        ),
        cax=axis,
        orientation='horizontal',
        spacing='proportional',
    )
    return fig
