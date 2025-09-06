import sys
sys.path.append("include")

from include.quick_bezier import QuickBezier


def main():
    b = QuickBezier()
    b.resetLogFiles()
    b.freq = 20
    
    #state update and refeed
    b.refeed()
    b.updateRefeedState()
    b.allocatePrev()

    #setting the projected velocity
    b.pVel = 0.1

    #bezier generation
    b.genRandomCurve()
    b.takeoff(-1.0)
    b.go2FirstCurve()
    while True:
        b.traverseCurve()

        if b.llp.closest_u >= 0.9:
            b.genRandomCurve()
            b.llp.transition()

        b.printAll()

if __name__ == "__main__":
    main()
