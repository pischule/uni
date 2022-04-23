import math

from social_distance.lib.types import ContextMapper, FrameContext
from disjoint_set import DisjointSet


class StatisticsCalculator(ContextMapper):
    def __init__(self):
        self.safe_distance = 0.0

    def map(self, context: FrameContext) -> FrameContext:
        for p in context.detected_objects:
            p.safe = True

        violations = 0
        ds = DisjointSet()

        visited = set()
        for i, p1 in enumerate(context.detected_objects):
            for j, p2 in enumerate(context.detected_objects):
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

        violators = sum([1 for p in context.detected_objects if not p.safe])

        context.violations = violations
        context.violators = violators
        context.violation_clusters = len(list(ds.itersets()))

        return context
