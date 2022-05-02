import dataclasses


@dataclasses.dataclass
class Stats:
    time: float
    total: int
    safe: int
    unsafe: int
    violations: int
    violation_clusters: int
