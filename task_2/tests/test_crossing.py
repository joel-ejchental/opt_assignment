import pytest
from task_2.algos.crossing_api import RLR, RLRRequest, RLRResult


@pytest.mark.parametrize("car_id, stop_line, trajectory, expected_ts", [
    ("CAR1", [[5, 100], [15, 100]], [[10, 7, 90], [11, 8, 95], [12, 7, 98], [13, 7, 102]], 12.5),
    ("CAR2", [[5, 100], [15, 97]], [[10, 7, 90], [11, 8, 95], [12, 7, 98], [13, 7, 102]], 12.35),
    ("CAR3", [[5, 100], [15, 97]], [[10, 7, 90], [11, 8, 95], [12, 7, 98]], None),
    ("CAR4", [[9, 97], [19, 94]], [[10, 7, 90], [11, 8, 95], [12, 7, 98]], None)
])
def test_crossing_time(car_id, stop_line, trajectory, expected_ts):
    rlr = RLR()
    request = RLRRequest(car_id=car_id, stop_line=stop_line, trajectory=trajectory)

    result = rlr.calc_crossing_timestamp(request)

    if expected_ts is None:
        assert result is None, f"Expected no crossing for {car_id}, but got: {result}"
    else:
        assert result is not None, f"Expected crossing for {car_id}, but got None"
        assert result.car_id == car_id, f"Expected car_id {car_id}, got {result.car_id}"
        assert result.crossing_timestamp == expected_ts, f"Expected timestamp {expected_ts}, but got {result.crossing_timestamp}"