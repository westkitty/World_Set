"""10_VEGETATION - salt-tolerant growth only."""

import random

from .. import dna
from ..geo import vec


def saltbush(asset):
    rnd = random.Random(11)
    mound = asset.part("mound", "MK_CONCRETE_STRUCT", uv_mode="cyl")
    mound.lathe([(0.0, 0.0), (0.45, 0.0), (0.4, 0.1), (0.2, 0.16), (0.0, 0.18)],
                vec(0, 0, 0), seg=12)
    import math
    twigs = asset.part("twigs", "MK_TIMBER")
    for i in range(24):
        a = rnd.uniform(0, 6.283)
        tilt = rnd.uniform(0.3, 1.0)
        L = rnd.uniform(0.2, 0.5)
        r = rnd.uniform(0.0, 0.3)
        x, y = math.cos(a) * r, math.sin(a) * r
        twigs.box(vec(x, y, 0.08 + L / 2), (0.02, 0.02, L),
                  rot=(tilt * math.sin(a), tilt * math.cos(a), a))
    fr = asset.part("fronds", "MK_TIMBER")
    for i in range(10):
        a = rnd.uniform(0, 6.283)
        x, y = math.cos(a) * 0.2, math.sin(a) * 0.2
        fr.box(vec(x, y, rnd.uniform(0.15, 0.35)), (0.16, 0.02, 0.3),
               rot=(rnd.uniform(-0.5, 0.5), rnd.uniform(-0.5, 0.5), a))
