from functions.utils import Point, Segment, orientation, timer
import heapq

class Event:
    def __init__(self, point: Point, segment: Segment, is_left: bool) -> None:
        self.point = point
        self.segment = segment
        self.is_left = is_left

    def __lt__(self, other: 'Event') -> bool:
        return self.point.x < other.point.x or (self.point.x == other.point.x and self.is_left)

def do_segments_intersect(s1: Segment, s2: Segment) -> bool:
    # Check if bounding boxes intersect
    if (max(s1.points[0].x, s1.points[1].x) < min(s2.points[0].x, s2.points[1].x) or
        max(s2.points[0].x, s2.points[1].x) < min(s1.points[0].x, s1.points[1].x) or
        max(s1.points[0].y, s1.points[1].y) < min(s2.points[0].y, s2.points[1].y) or
        max(s2.points[0].y, s2.points[1].y) < min(s1.points[0].y, s1.points[1].y)):
        return False

    # Check orientations
    o1 = orientation(s1.points[0], s1.points[1], s2.points[0])
    o2 = orientation(s1.points[0], s1.points[1], s2.points[1])
    o3 = orientation(s2.points[0], s2.points[1], s1.points[0])
    o4 = orientation(s2.points[0], s2.points[1], s1.points[1])

    return o1 != o2 and o3 != o4

@timer
def sweep_line_intersection(segments1: list[Segment], segments2: list[Segment]) -> tuple[bool, list[tuple[Segment, Segment]]]:
    events: list[Event] = []
    for segment in segments1:
        left, right = sorted(segment.points, key=lambda p: p.x)
        events.append(Event(left, segment, True))
        events.append(Event(right, segment, False))

    for segment in segments2:
        left, right = sorted(segment.points, key=lambda p: p.x)
        events.append(Event(left, segment, True))
        events.append(Event(right, segment, False))

    heapq.heapify(events)

    active_segments1: set[Segment] = set()
    active_segments2: set[Segment] = set()

    intersecting_pairs = []

    while events:
        event = heapq.heappop(events)
        if event.segment in segments1:
            if event.is_left:
                for active_segment in active_segments2:
                    if do_segments_intersect(event.segment, active_segment):
                        intersecting_pairs.append((event.segment, active_segment))
                active_segments1.add(event.segment)
            else:
                active_segments1.remove(event.segment)
        else:
            if event.is_left:
                for active_segment in active_segments1:
                    if do_segments_intersect(event.segment, active_segment):
                        intersecting_pairs.append((event.segment, active_segment))
                active_segments2.add(event.segment)
            else:
                active_segments2.remove(event.segment)

    return len(intersecting_pairs) > 0, intersecting_pairs