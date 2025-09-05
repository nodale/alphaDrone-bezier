import sys
sys.path.append("include")

from include.quick_bezier import QuickBezier

def main():
    b = QuickBezier()
    b.genRandomCurve()
    
    #state update and refeed

    #bezier generation

if __name__ == "__main__":
    main()
