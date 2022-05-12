import numpy as np
from gid_tools.gid_geometry import Gid2DGeometry

def generate_boundary(type: str, geometry: Gid2DGeometry, *params) -> None:
    available = {
        "bullet": _generate_bullet_boundary,
        "lens": _generate_lens_boundary,
    }

    try:
        return available[type.lower()](geometry, *params)
    except KeyError as e:
        raise KeyError(f"Unknown boundary type: {type}. Try any of {list(available.keys())}") from e

def _generate_bullet_boundary(geometry: Gid2DGeometry, radius: float):
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

def _generate_lens_boundary(geometry: Gid2DGeometry, vertical_radius: float, horzontal_radius: float = None):
    if horzontal_radius is None:
        horzontal_radius = 0.5 * vertical_radius

    # Curved inlet
    left = geometry.new_1d_shape('semicircle')
    top = left.new_point([0, vertical_radius])
    left.new_point([-horzontal_radius, 0])
    bot = left.new_point([0, -vertical_radius])

    # Curved outlet
    right = geometry.new_1d_shape('semicircle')
    right.add_point(bot)
    right.new_point([horzontal_radius, 0])
    right.add_point(top)


