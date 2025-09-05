from dataclasses import dataclass

from tra_spline import CubicSpline
from tra_planner import LinearLocalPlanner
from quick_mavlink import QuickMav
from quick_extCom import QuickExtCom
from quick_state import QuickState

import sys, select
import time

@dataclass
class QuickBezier(QuickMav, QuickExtCom, QuickState):
    pVel : float = 0.1 #projected velocity
    step : float = 1.0

    def __init__(self, address='localhost:14550', baudrate=57600, external=False):
        #initialising MAVLink
        QuickMav.__init__(address, baudrate)
        self.master.sendheartbeat()
        self.master.setFlightmode('OFFBOARD')

        #initialising external communication
        if external == True:
            QuickExtCom.__init__(self, address, baudrate)

        self.splineList = []
        self.llp = LinearLocalPlanner(self.spline_list, self.pVel)
        print("BEZIER ENGAGED")

    def initNudge(self):
        _initX, _initY = 0, 0

        _point_array = np.array([[_initX, _initY], [0.25 + _initX, _initY], [-0.25 + _initX, _initY], [_initX, _initY]], dtype=np.float64)
        _bez_curve = CubicSpline(p0=_point_array[0][:], p1=_point_array[1][:], p2=_point_array[2][:], p3=_point_array[3][:])
        
        self.splineList.append(_bez_curve)

    def genRandomCurve(self):
        #temp variables 
        _min_val = -1.0
        _max_val = 1.0

        _val1 = max(min(random.uniform(_min_val, _max_val), _max_val), _min_val)
        _val2 = max(min(random.uniform(_min_val, _max_val), _max_val), _min_val)
        _val3 = max(min(random.uniform(_min_val, _max_val), _max_val), _min_val)

        _py = self.pos[1],
              _val1,
              _val2,
              _val3]

        _point_array = np.array([[self.pos[0], _py[0]], [(self.step * 0.25) + self.pos[0], _py[1]], [(self.step * 0.5) + self.pos[0], _py[2]], [(self.step * 0.75) + self.pos[0], _py[3]]], dtype=np.float64)
        _bez_curve = CubicSpline(p0=_point_array[0][:], p1=_point_array[1][:], p2=_point_array[2][:], p3=_point_array[3][:])
        self.splineList.append(_bez_curve)
      
    def getVelSetpoint(self):
        self.llp.update_position(np.array([self.pos[0], slef.pos[1]]))
        _direction = self.llp.get_control_target(np.array([self.pos[0], self.pos[1]]))
        return direction[0], direction[1]

    def takeoff(self, z):
        print("attempting to take off")

        for i in range(100):
            self.sendPositionTarget(_time, self.pos[0], self.splineList[0, 2], z)
            time.sleep(1/self.freq)
        arm()
        for i in range(100):
            self.sendPositionTarget(_time, self.pos[0], self.splineList[0, 2], z)
            time.sleep(1/self.freq)

    def go2FirstCurve(self):
        _time = int(time.time * 1e6)
        while True:
            self.sendPositionTarget(_time, self.splineList[0, 1], self.splineList[0, 2], -1.0)

            time.sleep(1/self.freq)
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:   
                _line = sys.stdin.readline()
                if l_ine.strip() == "":
                    print("BEZIER ENGAGED")
                    break

    #for debugging or visualisation
    def resetFiles():
        _filename = 'log/pos.txt'
        with open(_filename, 'w') as _f:
            _f.write('x1\ty1\tz1\tx2\ty2\tz2\tx_sp\ty_sp\tz_sp\tt\n')

        _filename_q = 'log/q.txt'
        with open(_filename_q, 'w') as _fq:
            _fq.write('x1\ty1\tz1\tx2\ty2\tz2\tt\n')

        _filename_ang = 'log/ang.txt'
        with open(_filename_ang, 'w') as _fa:
            _fa.write('x1\ty1\tz1\tx2\ty2\tz2\tt\n')

        _filename_v = 'log/vel.txt'
        with open(_filename_v, 'w') as _fv:
            _fv.write('x1\ty1\tz1\tx2\ty2\tz2\tx_sp\ty_sp\tz_sp\tt\n')

        _filename_b = 'log/b.txt'
        with open(_filename_b, 'w') as _fb:
            _fb.write('\n')

        _filename_bezier = 'log/bezier.txt'
        with open(_filename_bezier, 'w') as _fbezier:
            _fbezier.write('\n')

    def append_bezier(signum=None, frame=None):
        with open('log/bezier.txt', "w") as f:
            for curve in self.splineList:
                for points in curve:
                    for x, y in points:
                        f.write(f"{x} {y}\n")
                    f.write("\n") 
        sys.exit(0)


    def printData(x1, y1, z1, x2, y2, z2, t, name):
        row = np.array([[x1, y1, z1, x2, y2, z2, t]])
        with open(name, 'a') as f:
            np.savetxt(f, row, fmt='%.6f', delimiter='\t')

    def printDataSP(x1, y1, z1, x2, y2, z2, x_sp, y_sp, z_sp, t, name):
        row = np.array([[x1, y1, z1, x2, y2, z2, x_sp, y_sp, z_sp, t]])
        with open(name, 'a') as f:
            np.savetxt(f, row, fmt='%.6f', delimiter='\t')

    def printAll():
    #quaternion debug
        append_row(self.q[1], self.q[2], self.q[3], self.qFil[0], self.qFil[1], self.qFil[2], time.time() - self.timeBoot, filename_q)
    #angle debug
        append_row(self.rot[0], self.rot[1], self.rot[2], self.rot[0], self.rot[1], self.rot[2], time.time() - self.timeBoot, filename_ang)
    #pos debug
        append_row_pos(self.pos[0], self.pos[1], self.pos[2], self.pos[0], self.pos[1], self.pos[2], 0, 0, 0, time.time() - self.timeBoot, filename)
    #vel debug
        append_row_pos(self.vel[0], self.vel[1], self.vel[2], self.vel[0], self.vel[1], self.vel[2], 0, 0, 0, time.time() - self.timeBoot, filename_v)


