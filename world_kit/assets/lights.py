"""08_LIGHTS - the only emissive geometry in the kit."""

from .. import dna
from ..geo import vec


def lamp_wall(asset):
    bp = asset.part("backplate", "MK_STEEL_PRIMER")
    bp.box(vec(0, 0.03, 0.16), (0.16, 0.04, 0.28))
    arm = asset.part("arm", "MK_STEEL_PRIMER", uv_mode="cyl")
    arm.cyl(vec(0, -0.05, 0.2), 0.02, 0.02, 0.18, axis="Y", seg=8)
    cap = asset.part("cap", "MK_BRASS", uv_mode="cyl")
    cap.lathe([(0.0, 0.24), (0.16, 0.24), (0.13, 0.16), (0.05, 0.12), (0.0, 0.12)],
              vec(0, -0.14, 0.02), seg=16)
    glow = asset.part("glow", "MK_EMISSIVE_AMBER", uv_mode="cyl")
    glow.lathe([(0.0, 0.0), (0.11, 0.03), (0.09, 0.14), (0.0, 0.18)], vec(0, -0.14, 0.02), seg=16)
    cage = asset.part("cage", "MK_STEEL_AGED", uv_mode="cyl")
    for i in range(4):
        import math
        a = math.pi / 4 + i * math.pi / 2
        cage.cyl(vec(math.cos(a) * 0.13, -0.14 + math.sin(a) * 0.13, 0.1), 0.008, 0.008, 0.16,
                 axis="Z", seg=6)


def lamp_pendant(asset):
    chain = asset.part("chain", "MK_STEEL_AGED", uv_mode="cyl")
    for z in (-0.06, -0.2, -0.34):
        chain.cyl(vec(0, 0, z), 0.012, 0.012, 0.12, axis="Z", seg=6)
    shade = asset.part("shade", "MK_STEEL_PAINTED", uv_mode="cyl")
    shade.lathe([(0.02, -0.42), (0.24, -0.58), (0.26, -0.62), (0.05, -0.66), (0.02, -0.68)],
                vec(0, 0, 0), seg=20)
    glow = asset.part("glow", "MK_EMISSIVE_AMBER", uv_mode="cyl")
    glow.lathe([(0.0, -0.5), (0.08, -0.54), (0.06, -0.64), (0.0, -0.67)], vec(0, 0, 0), seg=16)
    asset.origin = vec(0, 0, 0)
