from shapely.geometry import LineString, Point
import os
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class RLRRequest:
    car_id: str
    stop_line: List[List[float]]        
    trajectory: List[List[float]] 


@dataclass
class RLRResult:
    car_id: str
    crossing_timestamp: float


class RLR:
    
    def calc_crossing_timestamp(self, request: RLRRequest):
        p1, p2 = request.stop_line
        stop_line = LineString([p1, p2])

        for i in range(len(request.trajectory) - 1):
            t_prev, x_prev, y_prev = request.trajectory[i]
            t_next, x_next, y_next = request.trajectory[i + 1]
            vehicle_segment = LineString([(x_prev, y_prev), (x_next, y_next)])

            if vehicle_segment.intersects(stop_line):
                intersection_point = vehicle_segment.intersection(stop_line)
                segment_length = vehicle_segment.length
                dist_to_intersection = Point(x_prev, y_prev).distance(intersection_point)
                time_delta = t_next - t_prev

                crossing_timestamp = round(t_prev + (dist_to_intersection / segment_length) * time_delta, 2)
                result = RLRResult(request.car_id, crossing_timestamp)

                self.write_result_to_file(result)
                return result

        return None 

    @staticmethod
    def write_result_to_file(result: RLRResult):
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        events_dir = os.path.join(parent_dir, 'events')
        os.makedirs(events_dir, exist_ok=True)
        file_path = os.path.join(events_dir, 'crossing_events.txt')

        with open(file_path, 'a') as f:
            f.write(f'car_id: {result.car_id}\n')
            f.write(f'crossing_timestamp: {result.crossing_timestamp}\n') 
            f.write('---\n')
