import math
from typing import List, Dict

from disjoint_set import DisjointSet

from social_distance.lib.types import DetectedObject


class StatisticsCalculator:
    def __init__(self):
        self.safe_distance = 0.0

    def calc(self, objects: List[DetectedObject]) -> Dict[str, int]:
        for p in objects:
            p.safe = True

        violations = 0
        ds = DisjointSet()

        visited = set()
        for i, p1 in enumerate(objects):
            for j, p2 in enumerate(objects):
                if i == j or (j, i) in visited:
                    continue
                visited.add((i, j))
                p1x, p1y = tuple(p1.absolute_position)
                p2x, p2y = tuple(p2.absolute_position)
                distance = math.hypot(p1x - p2x, p1y - p2y)
                if distance < self.safe_distance:
                    p1.safe = False
                    p2.safe = False
                    ds.union(i, j)
                    violations += 1

        violators_count = sum(1 for p in objects if not p.safe)

        return {
            'Total': len(objects),
            'Safe': len(objects) - violators_count,
            'Unsafe': violators_count,
            'Violations': violations,
            'Violation Clusters': len(list(ds.itersets()))
        }
