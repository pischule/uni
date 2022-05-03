import dataclasses


@dataclasses.dataclass
class Stats:
    time: str
    total: int
    safe: int
    unsafe: int
    violations: int
    violation_clusters: int
