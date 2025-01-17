from code.classes.wire_class import WirePoint

class Segment:
    def __init__(self, segment_start: WirePoint, segment_finish: WirePoint):
        """Ensure consistent order: the segment_start should always be the smaller point"""
        if (segment_start.give_x(), segment_start.give_y(), segment_start.give_z()) > \
           (segment_finish.give_x(), segment_finish.give_y(), segment_finish.give_z()):
            self.segment_start = segment_finish
            self.segment_finish = segment_start
        else:
            self.segment_start = segment_start
            self.segment_finish = segment_finish


    def __eq__(self, other):
        """Equality check based on consistent point ordering"""
        return (self.segment_start, self.segment_finish) == (other.segment_start, other.segment_finish)
    

    def __hash__(self):
        return hash((self.segment_start, self.segment_finish))
    

    def __repr__(self):
        return f"Segment({self.segment_start}, {self.segment_finish})"

