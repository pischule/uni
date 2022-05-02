import csv
from io import StringIO
from typing import List

from social_distance.core.stats import Stats


def stats_to_string_csv(stats: List[Stats]) -> str:
    fieldnames = ['time', 'total', 'safe', 'unsafe', 'violations', 'violation_clusters']
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for s in stats:
        writer.writerow(s.__dict__)
    return output.getvalue()


if __name__ == '__main__':
    s1 = Stats(time=1, total=2, safe=3, unsafe=4, violations=5, violation_clusters=6)
    s2 = Stats(time=2, total=3, safe=4, unsafe=5, violations=6, violation_clusters=7)

    print(stats_to_string_csv([s1, s2]))