import math

from environment import cast_ray, cast_ray_circle

def test_cast_ray():
    tests = []
    # L1 vertical up
    ## L2 vertical x diff y1&&y2 < l1y
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-1, -5), (-1, -8)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1<ly1 && y2<ly1"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-1, 1), (-1, -8)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1<ly1 && y2<ly1 y1 eq"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-1, -8), (-1, 1)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1<ly1 && y2<ly1 reverse y2 eq"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-1, 1), (-1, 1)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1<ly1 && y2<ly1 reverse y1 eq y2 eq"
    })
    
    ## L2 vertical x diff y1^y2 < l1y
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-2, 5), (-2, -3)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1<ly1 ^  y2<ly1 y1>"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-2, -2), (-2, 4)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1<ly1 ^  y2<ly1 y2>"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-2, 5), (-2, 1)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1<ly1 ^  y2<ly1 y1> y2 eq"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-2, 1), (-2, 4)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1<ly1 ^  y2<ly1 y2> y1 eq"
    })
    
    ## L2 vertical x diff y1&&y2 > l1y
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-3, 6), (-3, 4)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1>ly1 && y2>ly1"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-3, 3), (-3, 7)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1>ly1 && y2>ly1 reverse"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-3, 1), (-3, 4)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1>ly1 && y2>ly1 y1 eq"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-3, 3), (-3, 1)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1>ly1 && y2>ly1 y2 eq reverse"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-3, 1), (-3, 1)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1>ly1 && y2>ly1 y1 eq y2 eq"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-5, 4), (-5, 4)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1>ly1 && y2>ly1 y1 eq y2 eq 2"
    })
    
    ## L2 vertical x same y1&&y2 < l1y
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, -5), (2, -8)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x same y1<ly1 && y2<ly1"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 1), (2, -8)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1<ly1 && y2<ly1 y1 eq"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 1), (2, 1)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1<ly1 && y2<ly1 reverse y1 eq y2 eq"
    })
    
    ## L2 vertical x same y1^y2 < l1y
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 5), (2, -3)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1<ly1 ^  y2<ly1 y1>"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, -2), (2, 4)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1<ly1 ^  y2<ly1 y2>"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 5), (2, 1)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1<ly1 ^  y2<ly1 y1> y2 eq"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 1), (2, 4)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1<ly1 ^  y2<ly1 y2> y1 eq"
    })
    
    ## L2 vertical x same y1&&y2 > l1y
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 6), (2, 4)], 
        "out": [True, 3], 
        "name": "L1 vertical up, l2 vertical x same y1>ly1 && y2>ly1"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 3), (2, 7)], 
        "out": [True, 2], 
        "name": "L1 vertical up, l2 vertical x same y1>ly1 && y2>ly1 reverse"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 1), (2, 4)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1>ly1 && y2>ly1 y1 eq"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 3), (2, 1)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1>ly1 && y2>ly1 y2 eq reverse"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 1), (2, 1)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1>ly1 && y2>ly1 y1 eq y2 eq"
    })
    tests.append({
        "l1": [(-15, 24), math.pi / 2], 
        "l2": [(-15, 24), (-15, 24)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1>ly1 && y2>ly1 y1 eq y2 eq 2"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 3), (2, 3)], 
        "out": [True, 2], 
        "name": "L1 vertical up, l2 vertical x same y1>ly1 && y2>ly1 y1 eq y2 eq x"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 7.5), (2, 7.5)], 
        "out": [True, 6.5], 
        "name": "L1 vertical up, l2 vertical x same y1>ly1 && y2>ly1 y1 eq y2 eq x 2"
    })
    
    ## L2 not vertical
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(5, -2), (1, 10)], 
        "out": [True, 6], 
        "name": "L1 vertical up, l2 not vertical test 1 normal"
    })
    tests.append({
        "l1": [(5, -2), math.pi / 2], 
        "l2": [(3, -5), (2, 4)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 not vertical test 2 normal"
    })
    tests.append({
        "l1": [(2, -3), math.pi / 2], 
        "l2": [(-10, -3), (8, 9)], 
        "out": [True, 8], 
        "name": "L1 vertical up, l2 not vertical test 3 normal"
    })
    tests.append({
        "l1": [(5, 3.5), math.pi / 2], 
        "l2": [(-4, 2), (8, 4)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 not vertical test 4 l2 through p1"
    })
    tests.append({
        "l1": [(5, 3.5), math.pi / 2], 
        "l2": [(5, 3.5), (5, 3.5)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 not vertical test 4 l2 eq p1"
    })
    
    
    # L1 vertical down
    ## L2 vertical x diff y1&&y2 > l1y
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(2, 3), (2, 7)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1>ly1 && y2>ly1"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(2, 2), (2, 3)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1>ly1 && y2>ly1 y1 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(2, 7), (2, 2)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1>ly1 && y2>ly1 reverse y2 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(2, 2), (2, 2)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1>ly1 && y2>ly1 reverse y1 eq y2 eq"
    })
    
    ## L2 vertical x diff y1^y2 > l1y
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(1, -5), (1, 4)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1>ly1 ^  y2>ly1 y1<"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(1, 7), (-2, -3)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1>ly1 ^  y2>ly1 y2<"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(5, -4), (5, 2)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1>ly1 ^  y2>ly1 y1< y2 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(-2, 2), (-2, -6)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1>ly1 ^  y2>ly1 y2< y1 eq"
    })
    
    ## L2 vertical x diff y1&&y2 < l1y
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(-3, 1), (-3, -4)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1<ly1 && y2<ly1"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(-3, 2), (-3, -5)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1<ly1 && y2<ly1 y1 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(-3, -4), (-3, 2)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1<ly1 && y2<ly1 y2 eq reverse"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(-3, 2), (-3, 2)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1<ly1 && y2<ly1 y1 eq y2 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(11, -14), (11, -14)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1<ly1 && y2<ly1 y1 eq y2 eq"
    })
    
    ## L2 vertical x same y1&&y2 > l1y
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 3), (3, 5)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 && y2>ly1"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 7), (3, 2.5)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 && y2>ly1 reverse"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 2), (3, 4)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 && y2>ly1 y1 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 6.5), (3, 2)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 && y2>ly1 reverse y2 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 2), (3, 2)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 && y2>ly1 reverse y1 eq y2 eq"
    })
    
    ## L2 vertical x same y1^y2 > l1y
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, -4), (3, 5)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 ^  y2>ly1 y1<"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 4), (3, -3)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 ^  y2>ly1 y2<"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, -9), (3, 2)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 ^  y2>ly1 y1< y2 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 2), (3, -6)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 ^  y2>ly1 y2< y1 eq"
    })
    
    ## L2 vertical x same y1&&y2 < l1y
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, -8), (3, -4.5)], 
        "out": [True, 6.5], 
        "name": "L1 vertical down, l2 vertical x same y1<ly1 && y2<ly1"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, -5), (3, -10)], 
        "out": [True, 7], 
        "name": "L1 vertical down, l2 vertical x same y1<ly1 && y2<ly1 reverse"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 2), (3, -4)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1<ly1 && y2<ly1 y1 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, -6), (3, 2)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1<ly1 && y2<ly1 y2 eq reverse"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 2), (3, 2)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1<ly1 && y2<ly1 y1 eq y2 eq"
    })
    tests.append({
        "l1": [(-10, 25), 3 * math.pi / 2], 
        "l2": [(-10, 25), (-10, 25)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1<ly1 && y2<ly1 y1 eq y2 eq 2"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, -4), (3, -4)], 
        "out": [True, 6], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 && y2>ly1 y1 eq y2 eq x"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, -6.5), (3, -6.5)], 
        "out": [True, 8.5], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 && y2>ly1 y1 eq y2 eq x 2"
    })
    
    ## L2 not vertical
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(6, 3.5), (-8, -7)], 
        "out": [True, 0.75], 
        "name": "L1 vertical down, l2 not vertical test 1 normal"
    })
    tests.append({
        "l1": [(5, -2), 3 * math.pi / 2], 
        "l2": [(-8, 6), (12, 4)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 not vertical test 2 normal"
    })
    tests.append({
        "l1": [(-4, 0), 3 * math.pi / 2], 
        "l2": [(6, 1.5), (-10.5, -6)], 
        "out": [True, 3.04545454545], 
        "name": "L1 vertical down, l2 not vertical test 3 normal"
    })
    tests.append({
        "l1": [(-2, 3), 3 * math.pi / 2], 
        "l2": [(-5, 4), (1, 2)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 not vertical test 4 l2 through p1"
    })
    tests.append({
        "l1": [(2, -4), 3 * math.pi / 2], 
        "l2": [(2, -4), (2, -4)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 not vertical test 4 l2 eq p1"
    })
    
    # L1 not vertical
    ## L2 vertical TODO: check all of these, intersect with l1 direction is also intersection.
    tests.append({
        "l1": [(3, 2), 2.456], 
        "l2": [(-6, 12), (-6, 4)], 
        "out": [True, 11.6272466696], 
        "name": "L1 not vertical, l2 vertical test 1"
    })
    tests.append({
        "l1": [(3, 2), 2.456], 
        "l2": [(4, 12), (4, 4)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 vertical test 2 no intersect"
    })
    tests.append({
        "l1": [(3, 2), 4], 
        "l2": [(4, 12), (4, 4)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 vertical test 3 no intersect"
    })
    tests.append({
        "l1": [(3, 2), 4], 
        "l2": [(4, 12), (4, 2)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 vertical test 4 no intersect"
    })
    tests.append({
        "l1": [(3, 2), 4], 
        "l2": [(2, 12), (2, -2)], 
        "out": [True, 1.52988565647], 
        "name": "L1 not vertical, l2 vertical test 5"
    })
    tests.append({
        "l1": [(3, 2), 4], 
        "l2": [(2.5, 12), (2.5, -2)], 
        "out": [True, 0.764942828233], 
        "name": "L1 not vertical, l2 vertical test 6"
    })
    tests.append({
        "l1": [(3, 2), 5], 
        "l2": [(2.5, 12), (2.5, -2)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 vertical test 7 no intersect"
    })
    tests.append({
        "l1": [(4, 1), 5], 
        "l2": [(4.1, 12), (4.1, -2)], 
        "out": [True, 0.352532008582], 
        "name": "L1 not vertical, l2 vertical test 8"
    })
    tests.append({
        "l1": [(4, 1), 5], 
        "l2": [(4.1, 12), (4.1, 0.7)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 vertical test 9 no intersect"
    })
    tests.append({
        "l1": [(4, 1), 1], 
        "l2": [(4.1, 12), (4.1, 0.7)], 
        "out": [True, 0.185081571768], 
        "name": "L1 not vertical, l2 vertical test 10"
    })
    tests.append({
        "l1": [(4, 1), 3.5], 
        "l2": [(4, 12), (4, 0.9)], 
        "out": [True, 0], 
        "name": "L1 not vertical, l2 vertical test 11 touches p1"
    })
    tests.append({
        "l1": [(4, 1), 3.5], 
        "l2": [(4, 12), (4, 1)], 
        "out": [True, 0], 
        "name": "L1 not vertical, l2 vertical test 12 l2 end on p1"
    })
    tests.append({
        "l1": [(4, 1), 3.5], 
        "l2": [(4, 1), (4, 12)], 
        "out": [True, 0], 
        "name": "L1 not vertical, l2 vertical test 13 l2 start on p1"
    })
    tests.append({
        "l1": [(4, 1), 3.5], 
        "l2": [(4, 1), (4, 1)], 
        "out": [True, 0], 
        "name": "L1 not vertical, l2 vertical test 14 l2 start and end on p1"
    })
    
    ## L2 not vertical
    # Both horizontal
    tests.append({
        "l1": [(4, 1), 0], 
        "l2": [(3, 2), (5, 2)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 1 both horizontal no intersect"
    })
    tests.append({
        "l1": [(4, 1), math.pi], 
        "l2": [(10, -2), (-3, -2)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 2 both horizontal no intersect 2"
    })
    tests.append({
        "l1": [(2, 2), 0], 
        "l2": [(-3, 2), (1, 2)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 3 both horizontal intersect l2 before p1"
    })
    tests.append({
        "l1": [(2, 2), math.pi], 
        "l2": [(4, 2), (6, 2)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 4 both horizontal intersect l2 before p1 other way"
    })
    tests.append({
        "l1": [(2, 2), 0], 
        "l2": [(4, 2), (6, 2)], 
        "out": [True, 2], 
        "name": "L1 not vertical, l2 not vertical test 5 both horizontal intersect l2 after p1"
    })
    tests.append({
        "l1": [(2, 2), math.pi], 
        "l2": [(-3, 2), (1, 2)], 
        "out": [True, 1], 
        "name": "L1 not vertical, l2 not vertical test 6 both horizontal intersect l2 after p1 other way"
    })
    tests.append({
        "l1": [(2, 3), 0], 
        "l2": [(-5, 3), (10, 3)], 
        "out": [True, 0], 
        "name": "L1 not vertical, l2 not vertical test 7 both horizontal intersect l2 around p1"
    })
    tests.append({
        "l1": [(2, 3), 0], 
        "l2": [(2, 3), (10, 3)], 
        "out": [True, 0], 
        "name": "L1 not vertical, l2 not vertical test 8 both horizontal intersect l2 around p1 l2 start on p1"
    })
    tests.append({
        "l1": [(2, 3), 0], 
        "l2": [(-5, 3), (2, 3)], 
        "out": [True, 0], 
        "name": "L1 not vertical, l2 not vertical test 9 both horizontal intersect l2 around p1 l2 end on p1"
    })
    tests.append({
        "l1": [(2, 3), 0], 
        "l2": [(2, 3), (2, 3)], 
        "out": [True, 0], 
        "name": "L1 not vertical, l2 not vertical test 10 both horizontal intersect l2 around p1 l2 start and end on p1"
    })
    
    # l1 not horizontal
    tests.append({
        "l1": [(2, 3), 0.5], 
        "l2": [(2, 5), (5, 5)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 11 l1 not horizontal q1 no intersect"
    })
    tests.append({
        "l1": [(2, 3), 0.5], 
        "l2": [(2, 5), (5.7, 5)], 
        "out": [True, 4.17165928587], 
        "name": "L1 not vertical, l2 not vertical test 12 l1 not horizontal q1 intersect"
    })
    
    tests.append({
        "l1": [(2, 3), 2], 
        "l2": [(2, 5), (7, 5)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 13 l1 not horizontal q2 no intersect"
    })
    tests.append({
        "l1": [(2, 3), 2], 
        "l2": [(-2, 5), (7, 5)], 
        "out": [True, 2.19950034059], 
        "name": "L1 not vertical, l2 not vertical test 14 l1 not horizontal q2 intersect"
    })
    
    tests.append({
        "l1": [(2, 3), 4.5], 
        "l2": [(1.5, -1), (6, -1)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 15 l1 not horizontal q3 no intersect"
    })
    tests.append({
        "l1": [(2, 3), 4.5], 
        "l2": [(1, -1), (6, -1)], 
        "out": [True, 4.09194553469], 
        "name": "L1 not vertical, l2 not vertical test 16 l1 not horizontal q3 intersect"
    })
    
    tests.append({
        "l1": [(2, 3), 5.5], 
        "l2": [(1, -1), (6, -1)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 17 l1 not horizontal q4 no intersect"
    })
    tests.append({
        "l1": [(2, 3), 5.5], 
        "l2": [(1, -1), (6.5, -1)], 
        "out": [True, 5.66941371745], 
        "name": "L1 not vertical, l2 not vertical test 18 l1 not horizontal q4 intersect"
    })
    
    # l2 not horizontal
    tests.append({
        "l1": [(1, 3), 0], 
        "l2": [(1, 5), (3, 3.5)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 19 l2 not horizontal l1 right test 1 no intersect"
    })
    tests.append({
        "l1": [(1, 3), 0], 
        "l2": [(3, 6), (-2, 1)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 20 l2 not horizontal l1 right test 2 no intersect"
    })
    tests.append({
        "l1": [(1, 3), 0], 
        "l2": [(1, -3), (8, 6)], 
        "out": [True, 4.66666666667], 
        "name": "L1 not vertical, l2 not vertical test 21 l2 not horizontal l1 right test 3 intersect"
    })
    tests.append({
        "l1": [(1, 3), 0], 
        "l2": [(7, -3), (-2.5, 7.5)], 
        "out": [True, 0.571428571429], 
        "name": "L1 not vertical, l2 not vertical test 22 l2 not horizontal l1 right test 4 intersect"
    })
    tests.append({
        "l1": [(1, 3), 0], 
        "l2": [(0, -3), (10, 8)], 
        "out": [True, 4.45454545455], 
        "name": "L1 not vertical, l2 not vertical test 23 l2 not horizontal l1 right test 5 intersect"
    })
    
    tests.append({
        "l1": [(1, 3), math.pi], 
        "l2": [(0, -3), (10, 8)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 19 l2 not horizontal l1 left test 1 no intersect"
    })
    tests.append({
        "l1": [(1, 3), math.pi], 
        "l2": [(-1, 6), (5, -2)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 20 l2 not horizontal l1 left test 2 no intersect"
    })
    tests.append({
        "l1": [(1, 3), math.pi], 
        "l2": [(-1, 6), (4, -3)], 
        "out": [True, 0.333333333333], 
        "name": "L1 not vertical, l2 not vertical test 21 l2 not horizontal l1 left test 3 intersect"
    })
    tests.append({
        "l1": [(1, 3), math.pi], 
        "l2": [(2, 6), (-3, -4.5)], 
        "out": [True, 0.428571428571], 
        "name": "L1 not vertical, l2 not vertical test 22 l2 not horizontal l1 left test 4 intersect"
    })
    tests.append({
        "l1": [(1, 3), math.pi], 
        "l2": [(5, 4), (-10, 2.25)], 
        "out": [True, 4.57142857143], 
        "name": "L1 not vertical, l2 not vertical test 23 l2 not horizontal l1 left test 5 intersect"
    })
    
    # Both not horizontal but parallel
    tests.append({
        "l1": [(1, 3), math.pi / 4], 
        "l2": [(5, 4), (-1, -2)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 24 both not horizontal but parallel"
    })
    tests.append({
        "l1": [(1, 3), 5 * math.pi / 8], 
        "l2": [(1, 1), (1 + 5 * math.cos(5 * math.pi / 8), 1 + 5 * math.sin(5 * math.pi / 8))], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 25 both not horizontal but parallel 2"
    })
    tests.append({
        "l1": [(1, 3), 1.234], 
        "l2": [(1, 1), (1 + 10 * math.cos(1.234), 1 + 10 * math.sin(1.234))], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 26 both not horizontal but parallel 3"
    })
    
    # Both not horizontal but not quite parallel
    tests.append({
        "l1": [(1, 3), math.pi / 4 - 0.001], 
        "l2": [(5, 6), (-1, 0)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 27 both not horizontal but not quite parallel"
    })
    tests.append({
        "l1": [(1, 3), 5 * math.pi / 8 - 0.02], 
        "l2": [(1, 1), (1 + 6 * math.cos(5 * math.pi / 8), 1 + 6 * math.sin(5 * math.pi / 8))], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 28 both not horizontal but not quite parallel 2"
    })
    tests.append({
        "l1": [(1, 3), 1.234 - 0.2], 
        "l2": [(1, 1), (1 + 3 * math.cos(1.234), 1 + 3 * math.sin(1.234))], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 29 both not horizontal but not quite parallel 3"
    })
    
    # Both not horizontal not parallel
    tests.append({
        "l1": [(1, 3), 1.234 - 0.2], 
        "l2": [(1, 2), (1 + 3 * math.cos(1.234), 2 + 3 * math.sin(1.234))], 
        "out": [True, 1.66339266735], 
        "name": "L1 not vertical, l2 not vertical test 30 both not horizontal but not parallel 1 intersect"
    })
    tests.append({
        "l1": [(-1, 2.5), 4.613], 
        "l2": [(2, -0.5), (-3, -2)], 
        "out": [True, 4.04020584779], 
        "name": "L1 not vertical, l2 not vertical test 31 both not horizontal but not parallel 2 intersect"
    })
    tests.append({
        "l1": [(3.2, 4.6), 3.65], 
        "l2": [(0.5, -1.5), (-4, 1.8)], 
        "out": [True, 7.16713212629], 
        "name": "L1 not vertical, l2 not vertical test 32 both not horizontal but not parallel 3 intersect"
    })
    tests.append({
        "l1": [(3.2, 4.6), 3.65], 
        "l2": [(2, 3.9), (-4, 0.6)], 
        "out": [True, 6.29905891177], 
        "name": "L1 not vertical, l2 not vertical test 32 both not horizontal but not parallel 4 intersect"
    })
    
    tests.append({
        "l1": [(3.2, 4.6), 3.64], 
        "l2": [(2, 3.9), (-4, 0.6)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 32 both not horizontal but not parallel 5 no intersect"
    })
    tests.append({
        "l1": [(1.6, -2.1), 2.9], 
        "l2": [(2.3, 5.23), (-4.7, 1.4)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 32 both not horizontal but not parallel 6 no intersect"
    })
    tests.append({
        "l1": [(3.2, -2.9), 5.4], 
        "l2": [(4, -2), (-2, 4.3)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 32 both not horizontal but not parallel 7 no intersect"
    })
    
    tests.append({
        "l1": [(-2.4, 1.3), 1.456], 
        "l2": [(-1, -2.3), (2.8, 4.5)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 32 both not horizontal but not parallel 8 no intersect"
    })
    
    test_id = 1
    succeeded = 0
    failed = 0
    total_tests = 0
    
    # Run normal tests.
    normal_tests_data = {"messages": [], "passed": 0, "failed": 0, "total": 0}
    normal_tests_data["messages"].append("Normal tests:")
    for test in tests:
        result = cast_ray(test["l1"], test["l2"])
        test_result = test_check_result(result, test["out"])
        pass_string = "passed"
        if not test_result:
            if test_id < 100:
                pass_string = f"failed\t\tname: {test['name']}"
            else:
                pass_string = f"failed\tname: {test['name']}"
            pass_string += f" (expected {test['out']}, got {result})"
            failed += 1
            normal_tests_data["failed"] += 1
        else:
            succeeded += 1
            normal_tests_data["passed"] += 1
        if not test_result:
            normal_tests_data["messages"].append(f"Test #{test_id} {pass_string}")
        total_tests += 1
        normal_tests_data["total"] += 1
        test_id += 1
    print(f"{normal_tests_data['messages'][0]} {normal_tests_data['passed']}/{normal_tests_data['total']} ({normal_tests_data['passed'] / normal_tests_data['total'] * 100:.2f}%)")
    for message in normal_tests_data["messages"][1:]:
        print(message)
    if len(normal_tests_data["messages"]) > 1:
        print()
    
    # Run tests with points in l2 reversed.
    reversed_tests_data = {"messages": [], "passed": 0, "failed": 0, "total": 0}
    reversed_tests_data["messages"].append("Test with l2 reversed:")
    for test in tests:
        result = cast_ray(test["l1"], (test["l2"][1], test["l2"][0]))
        test_result = test_check_result(result, test["out"])
        pass_string = "passed"
        if not test_result:
            if test_id < 100:
                pass_string = f"failed\t\tname: {test['name']}"
            else:
                pass_string = f"failed\tname: {test['name']}"
            pass_string += f" (expected {test['out']}, got {result})"
            failed += 1
            reversed_tests_data["failed"] += 1
        else:
            succeeded += 1
            reversed_tests_data["passed"] += 1
        if not test_result:
            reversed_tests_data["messages"].append(f"Test #{test_id} {pass_string}")
        total_tests += 1
        reversed_tests_data["total"] += 1
        test_id += 1
    print(f"{reversed_tests_data['messages'][0]} {reversed_tests_data['passed']}/{reversed_tests_data['total']} ({reversed_tests_data['passed'] / reversed_tests_data['total'] * 100:.2f}%)")
    for message in reversed_tests_data["messages"][1:]:
        print(message)
    if len(reversed_tests_data["messages"]) > 1:
        print()
    
    print(f"Result: {succeeded}/{total_tests} passed ({succeeded / total_tests * 100:.2f}%)")
    print()

def test_cast_ray_circle():
    tests = []
    
    # L1 vertical up
    # Up
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(-2, 4), 1], 
        "out": [False, 0], 
        "name": "L1 vertical up circle up left no intersect"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(-0.5, 4), 1.5], 
        "out": [True, 2], 
        "name": "L1 vertical up circle up left touch"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(-0.3, 5), 1.5], 
        "out": [True, 2.25166852265], 
        "name": "L1 vertical up circle up left intersect"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(1, 5), 0.8], 
        "out": [True, 2.2], 
        "name": "L1 vertical up circle up center intersect"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(1.7, 5), 1.2], 
        "out": [True, 2.02532056552], 
        "name": "L1 vertical up circle up right intersect"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(2.3, 5.674), 1.3], 
        "out": [True, 3.674], 
        "name": "L1 vertical up circle up right touch", 
        "tolerance": 0.00000001
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(5.3, 3.8), 1.45], 
        "out": [False, 0], 
        "name": "L1 vertical up circle up right no intersect"
    })
    
    # Middle
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(-3.5, 2.5), 1.35], 
        "out": [False, 0], 
        "name": "L1 vertical up circle middle left no intersect"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(-0.3, 2), 1.3], 
        "out": [True, 0], 
        "name": "L1 vertical up circle middle left touch"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(-0.3, 1.7), 1.62], 
        "out": [True, 0], 
        "name": "L1 vertical up circle middle left intersect"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(1, 1.7), 1.349], 
        "out": [True, 0], 
        "name": "L1 vertical up circle middle center intersect"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(1.6, 1.7), 1.349], 
        "out": [True, 0], 
        "name": "L1 vertical up circle middle right intersect"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(2.6, 2.4), 1.6], 
        "out": [True, 0.4], 
        "name": "L1 vertical up circle middle right touch"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(6.65, 1.93), 4.3], 
        "out": [False, 0], 
        "name": "L1 vertical up circle middle right no intersect"
    })
    
    # Down
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(-3, -2), 2.4], 
        "out": [False, 0], 
        "name": "L1 vertical up circle down left no intersect"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(-1.6, -2), 2.6], 
        "out": [False, 0], 
        "name": "L1 vertical up circle down left would touch no intersect"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(-0.4, -2), 2.45], 
        "out": [False, 0], 
        "name": "L1 vertical up circle down left would intersect no intersect"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(1, -2), 2.45], 
        "out": [False, 0], 
        "name": "L1 vertical up circle down center would intersect no intersect"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(1.43, -1), 1.47], 
        "out": [False, 0], 
        "name": "L1 vertical up circle down right would intersect no intersect"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(2.6, -1), 1.6], 
        "out": [False, 0], 
        "name": "L1 vertical up circle down right would touch no intersect"
    })
    tests.append({
        "l1": [(1, 2), math.pi / 2], 
        "c" : [(4.5, -1.5), 1.84], 
        "out": [False, 0], 
        "name": "L1 vertical up circle down right no intersect"
    })
    
    # L1 vertical down
    # Up
    tests.append({
        "l1": [(1.5, 2.5), 3 * math.pi / 2], 
        "c" : [(-2, 4.6), 1.84], 
        "out": [False, 0], 
        "name": "L1 vertical down circle up left no intersect"
    })
    tests.append({
        "l1": [(1.5, 2.5), 3 * math.pi / 2], 
        "c" : [(-0.4, 4.6), 1.9], 
        "out": [False, 0], 
        "name": "L1 vertical down circle up left would touch no intersect"
    })
    tests.append({
        "l1": [(1.5, 2.5), 3 * math.pi / 2], 
        "c" : [(0.34, 6.7), 2.6], 
        "out": [False, 0], 
        "name": "L1 vertical down circle up left would intersect no intersect"
    })
    tests.append({
        "l1": [(1.5, 2.5), 3 * math.pi / 2], 
        "c" : [(1.5, 4.8), 1.2], 
        "out": [False, 0], 
        "name": "L1 vertical down circle up center would intersect no intersect"
    })
    tests.append({
        "l1": [(1.5, 2.5), 3 * math.pi / 2], 
        "c" : [(1.83, 4.3), 1.4], 
        "out": [False, 0], 
        "name": "L1 vertical down circle up right would intersect no intersect"
    })
    tests.append({
        "l1": [(1.5, 2.5), 3 * math.pi / 2], 
        "c" : [(3.15, 5.42), 1.65], 
        "out": [False, 0], 
        "name": "L1 vertical down circle up right would touch no intersect"
    })
    tests.append({
        "l1": [(1.5, 2.5), 3 * math.pi / 2], 
        "c" : [(5.94, 6.17), 2.13], 
        "out": [False, 0], 
        "name": "L1 vertical down circle up right no intersect"
    })
    
    # Middle
    tests.append({
        "l1": [(1.5, 2), 3 * math.pi / 2], 
        "c" : [(-3, 1.5), 2], 
        "out": [False, 0], 
        "name": "L1 vertical down circle middle left no intersect"
    })
    tests.append({
        "l1": [(1.5, 2), 3 * math.pi / 2], 
        "c" : [(-1, 2), 2.5], 
        "out": [True, 0], 
        "name": "L1 vertical down circle middle left touch"
    })
    tests.append({
        "l1": [(1.5, 2), 3 * math.pi / 2], 
        "c" : [(0.4, 1.5), 2.3], 
        "out": [True, 0], 
        "name": "L1 vertical down circle middle left intersect"
    })
    tests.append({
        "l1": [(1.5, 2), 3 * math.pi / 2], 
        "c" : [(1.5, 1.64), 2], 
        "out": [True, 0], 
        "name": "L1 vertical down circle middle center intersect"
    })
    tests.append({
        "l1": [(1.5, 2), 3 * math.pi / 2], 
        "c" : [(2.21, 2), 1.78], 
        "out": [True, 0], 
        "name": "L1 vertical down circle middle right intersect"
    })
    tests.append({
        "l1": [(1.5, 2), 3 * math.pi / 2], 
        "c" : [(3.35, 1.24), 1.85], 
        "out": [True, 0.76], 
        "name": "L1 vertical down circle middle right touch"
    })
    tests.append({
        "l1": [(1.5, 2), 3 * math.pi / 2], 
        "c" : [(3.67, 1.16), 1.34], 
        "out": [False, 0], 
        "name": "L1 vertical down circle middle right no intersect"
    })
    
    # Down
    tests.append({
        "l1": [(1, 2), 3 * math.pi / 2], 
        "c" : [(-3.5, -2.4), 2], 
        "out": [False, 0], 
        "name": "L1 vertical down circle down left no intersect"
    })
    tests.append({
        "l1": [(1, 2), 3 * math.pi / 2], 
        "c" : [(-3.3, -4.14), 4.3], 
        "out": [True, 6.14], 
        "name": "L1 vertical down circle down left touch", 
        "tolerance": 0.0000001
    })
    tests.append({
        "l1": [(1, 2), 3 * math.pi / 2], 
        "c" : [(-3.4, -5.1), 4.7], 
        "out": [True, 5.44772883581], 
        "name": "L1 vertical down circle down left intersect"
    })
    tests.append({
        "l1": [(1, 2), 3 * math.pi / 2], 
        "c" : [(1, -10.24), 4.37], 
        "out": [True, 7.87], 
        "name": "L1 vertical down circle down center intersect"
    })
    tests.append({
        "l1": [(1, 2), 3 * math.pi / 2], 
        "c" : [(3.56, -6), 5.25], 
        "out": [True, 3.4164533383], 
        "name": "L1 vertical down circle down right intersect"
    })
    tests.append({
        "l1": [(1, 2), 3 * math.pi / 2], 
        "c" : [(4.5, -5), 3.5], 
        "out": [True, 7], 
        "name": "L1 vertical down circle down right touch", 
        "float_error": True
    })
    tests.append({
        "l1": [(1, 2), 3 * math.pi / 2], 
        "c" : [(7, -3.6), 4.15], 
        "out": [False, 0], 
        "name": "L1 vertical down circle down right no intersect"
    })
    
    # L1 not vertical
    # Up (in front of l1)
    tests.append({
        "l1": [(-1.5, 1.8), 2.481], 
        "c":  [(-11.4, 3.2), 3.56], 
        "out": [False, 0], 
        "name": "L1 not vertical circle up left no intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 3.481], 
        "c":  [(-8.4, -6.2), 3.56], 
        "out": [False, 0], 
        "name": "L1 not vertical circle up left no intersect 2"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 1.234], 
        "c":  [(-3.1015, 8), 3.56], 
        "out": [False, 0], 
        "name": "L1 not vertical circle up left just not touch"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 0], 
        "c":  [(5, 4.42), 2.62], 
        "out": [True, 6.5], 
        "name": "L1 not vertical circle up left touch", 
        "tolerance": 0.00000001
    })
    tests.append({
        "l1": [(-1.5, 1.8), 5.2], 
        "c":  [(4, -5), 2.23], 
        "out": [True, 7.10999313185], 
        "name": "L1 not vertical circle up left intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), math.pi], 
        "c":  [(-5, 1.8), 2.2], 
        "out": [True, 1.3], 
        "name": "L1 not vertical circle up center intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 2.34], 
        "c":  [(-8, 12), 3.3], 
        "out": [True, 9.61104103842], 
        "name": "L1 not vertical circle up right intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), math.pi], 
        "c":  [(-8, -1.8), 3.6], 
        "out": [True, 6.5], 
        "name": "L1 not vertical circle up right touch", 
        "float_error": True
    })
    tests.append({
        "l1": [(-1.5, 1.8), 3.82], 
        "c":  [(-8, 1.19), 3.6], 
        "out": [False, 0], 
        "name": "L1 not vertical circle up right just not touch"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 1.56], 
        "c":  [(6.3, 9.4), 3.41], 
        "out": [False, 0], 
        "name": "L1 not vertical circle up right no intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 5.3], 
        "c":  [(-5, -9), 5], 
        "out": [False, 0], 
        "name": "L1 not vertical circle up right no intersect 2"
    })
    
    # Middle (circle encompassing line perpendicular to and going through l1)
    tests.append({
        "l1": [(-1.5, 1.8), 3.4], 
        "c":  [(0, -6), 5], 
        "out": [False, 0], 
        "name": "L1 not vertical circle middle left no intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 1.3], 
        "c":  [(-7, 3), 3], 
        "out": [False, 0], 
        "name": "L1 not vertical circle middle left no intersect 2"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 4], 
        "c":  [(0.91, 0), 3], 
        "out": [False, 0], 
        "name": "L1 not vertical circle middle left just not touch"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 0], 
        "c":  [(-1.5, 3.8), 2], 
        "out": [True, 0], 
        "name": "L1 not vertical circle middle left touch"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 2], 
        "c":  [(-3, 1), 2], 
        "out": [True, 0], 
        "name": "L1 not vertical circle middle left intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 5], 
        "c":  [(-1.5, 1.8), 3], 
        "out": [True, 0], 
        "name": "L1 not vertical circle middle center intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 3.6], 
        "c":  [(-2, 3.5), 3], 
        "out": [True, 0], 
        "name": "L1 not vertical circle middle right intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), math.pi], 
        "c":  [(-1.5, 4.8), 3], 
        "out": [True, 0], 
        "name": "L1 not vertical circle middle right touch"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 2.5], 
        "c":  [(0.3, 4.25), 3], 
        "out": [False, 0], 
        "name": "L1 not vertical circle middle right just not touch"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 6], 
        "c":  [(-3.5, -5), 4], 
        "out": [False, 0], 
        "name": "L1 not vertical circle middle right no intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 1], 
        "c":  [(7, -3.6), 2], 
        "out": [False, 0], 
        "name": "L1 not vertical circle middle right no intersect 2"
    })
    
    # Down (behind l1)
    tests.append({
        "l1": [(-1.5, 1.8), 5.5], 
        "c":  [(-3, 9), 2], 
        "out": [False, 0], 
        "name": "L1 not vertical circle down left no intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 2.3], 
        "c":  [(-5, -5.5), 2], 
        "out": [False, 0], 
        "name": "L1 not vertical circle down left no intersect 2"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 4], 
        "c":  [(3.045, 4), 2], 
        "out": [False, 0], 
        "name": "L1 not vertical circle down left would just not touch"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 0], 
        "c":  [(-6, 4), 2.2], 
        "out": [False, 0], 
        "name": "L1 not vertical circle down left would touch no intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 3], 
        "c":  [(5, -1), 2.2], 
        "out": [False, 0], 
        "name": "L1 not vertical circle down left would intersect no intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), math.pi], 
        "c":  [(6.7, 1.8), 3.67], 
        "out": [False, 0], 
        "name": "L1 not vertical circle down center would intersect no intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 1], 
        "c":  [(-3, -5), 4.5], 
        "out": [False, 0], 
        "name": "L1 not vertical circle down right would intersect no intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 0], 
        "c":  [(-5.4, -0.65), 2.45], 
        "out": [False, 0], 
        "name": "L1 not vertical circle down right would touch no intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 2.5], 
        "c":  [(5.004, 0), 2.45], 
        "out": [False, 0], 
        "name": "L1 not vertical circle down right would just not touch"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 4.7], 
        "c":  [(-7, 5), 2.45], 
        "out": [False, 0], 
        "name": "L1 not vertical circle down right no intersect"
    })
    tests.append({
        "l1": [(-1.5, 1.8), 3.2], 
        "c":  [(5, 5.3), 2.45], 
        "out": [False, 0], 
        "name": "L1 not vertical circle down right no intersect 2"
    })
    
    test_id = 1
    succeeded = 0
    failed = 0
    total_tests = 0
    
    # Run normal tests.
    tests_data = {"messages": [], "passed": 0, "failed": 0, "total": 0}
    tests_data["messages"].append("Tests:")
    for test in tests:
        result = cast_ray_circle(test["l1"], test["c"])
        if "tolerance" in test.keys():
            test_result = test_check_result(result, test["out"], test["tolerance"])
        else:
            test_result = test_check_result(result, test["out"])
        float_error_ignore = test["float_error"] if "float_error" in test.keys() else False
        pass_string = f"passed (float_error_ignore: {float_error_ignore})"
        if not test_result and not float_error_ignore:
            if test_id < 100:
                pass_string = f"failed\t\tname: {test['name']}"
            else:
                pass_string = f"failed\tname: {test['name']}"
            pass_string += f" (expected {test['out']}, got {result})"
            failed += 1
            tests_data["failed"] += 1
        else:
            succeeded += 1
            tests_data["passed"] += 1
        if not test_result:
            tests_data["messages"].append(f"Test #{test_id} {pass_string}")
        total_tests += 1
        tests_data["total"] += 1
        test_id += 1
    print(f"{tests_data['messages'][0]} {tests_data['passed']}/{tests_data['total']} ({tests_data['passed'] / tests_data['total'] * 100:.2f}%)")
    for message in tests_data["messages"][1:]:
        print(message)
    if len(tests_data["messages"]) > 1:
        print()
    
    print(f"Result: {succeeded}/{total_tests} passed ({succeeded / total_tests * 100:.2f}%)")
    print()

def test_check_result(result, expected_output, tolerance=0.000000001):
    result = list(result)
    expected_output = list(expected_output)
    if not result[0] == expected_output[0]:
        return False
    if expected_output[1] == 0:
        if not (result[1] >= -tolerance and result[1] <= tolerance):
            return False
    else:
        if not (result[1] >= expected_output[1] * (1 - tolerance) \
            and result[1] <= expected_output[1] * (1 + tolerance)):
            return False
    return True

def main():
    print("cast_ray()")
    test_cast_ray()
    print("cast_ray_circle()")
    test_cast_ray_circle()

if __name__ == "__main__":
    main()
