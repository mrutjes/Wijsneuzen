import pytest
from classes.segment_class import Segment
from classes.wire_class import WirePoint

def test_segment_initialization():
    segment = Segment(WirePoint(0, 0, 0), WirePoint(1, 0, 0))
    assert segment.segment_start == WirePoint(0, 0, 0)
    assert segment.segment_finish == WirePoint(1, 0, 0)

def test_segment_initialization_reverse():
    segment = Segment(WirePoint(1, 0, 0), WirePoint(0, 0, 0))
    assert segment.segment_start == WirePoint(0, 0, 0)
    assert segment.segment_finish == WirePoint(1, 0, 0)