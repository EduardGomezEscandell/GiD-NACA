import numpy as np
from src.gid_tools.gid_geometry import Gid2DGeometry

def generate_boundary(type: str, geometry: Gid2DGeometry, *params) -> None:
    available = {
        "bullet": _generate_bullet_boundary,
        "lens": _generate_lens_boundary,
        "rectangle": _generate_rectangle_boundary,
        "none": lambda *_: None,
    }

    try:
        return available[type.lower()](geometry, *params)
    except KeyError as e:
        raise KeyError(f"Unknown boundary type: {type}. Try any of {list(available.keys())}") from e

def _generate_bullet_boundary(geometry: Gid2DGeometry, radius: float) -> None:
    # Curved inlet
    sc = geometry.new_1d_shape('semicircle')
    top_center = sc.new_point([0, radius])
    sc.new_point([-radius, 0])
    bot_center = sc.new_point([0, -radius])

    # Straight walls and outlet
    bot_right = geometry.new_point([radius, -radius])
    top_right = geometry.new_point([radius, radius])

    geometry.new_1d_shape('line', bot_center, bot_right)
    geometry.new_1d_shape('line', bot_right, top_right)
    geometry.new_1d_shape('line', top_right, top_center)

def _generate_lens_boundary(geometry: Gid2DGeometry, height: float, width: float = None) -> None:
    if width is None:
        width = 0.5 * height

    # Curved inlet
    left = geometry.new_1d_shape('semicircle')
    top = left.new_point([0, height])
    left.new_point([-width, 0])
    bot = left.new_point([0, -height])

    # Curved outlet
    right = geometry.new_1d_shape('semicircle')
    right.add_point(bot)
    right.new_point([width, 0])
    right.add_point(top)

def _generate_rectangle_boundary(geometry: Gid2DGeometry, width: float, height: float = None) -> None:
    if height is None:
        height = width

    with geometry.new_1d_shape('polygon') as p:
        p.new_point([-width, -height])
        p.new_point([ width, -height])
        p.new_point([ width,  height])
        p.new_point([-width,  height])




