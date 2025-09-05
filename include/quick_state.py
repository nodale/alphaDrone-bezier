from dataclasses import dataclass

import numpy as np

@dataclass
class QuickState:
    
    pos : np.zeros(3) #x, y, z
    vel : np.zeros(3) #vx, vy, vz
    q : np.zeros(4) #w, x, y, z
    rot : np.zeros(3) #roll, pitch, yaw
    rotRates : np.zeros(3) #rates : roll, pitch, yaw

    posP : np.zeros(3) #x, y, z
    velP : np.zeros(3) #vx, vy, vz
    rotP : np.zeros(3) #roll, pitch, yaw
    qP : np.zeros(4) #w, x, y, z

    posFil : np.zeros(3) #x, y, z
    velFil : np.zeros(3) #vx, vy, vz
    qFil : np.zeros(4) #w, x, y, z
    rotFil : np.zeros(3) #roll, pitch, yaw
    rotRatesFil : np.zeros(3) #rates : roll, pitch, yaw

    alphaPos : float = 1.0
    alphaVel : float = 1.0
    alphaQ  : float = 1.0
    alphaRot : float = 1.0

    def getEulerRates(self, dt):
        _q1 = np.array([self.q[0], self.q[1], self.q[2], self.q[3]])
        _q2 = np.array([self.qP[0], self.qP[1], self.qP[2], self.qP[3]])
        
        _q_conj = np.array([self.q[0], -self.q[1], -self.q[2], -self.q[3]])
        
        _w1, _x1, _y1, _z1 = _q_conj
        _w2, _x2, _y2, _z2 = _q2
        _q_rel = np.array([
            _w1*_w2 - _x1*_x2 - _y1*_y2 - _z1*_z2,
            _w1*_x2 + _x1*_w2 + _y1*_z2 - _z1*_y2,
            _w1*_y2 - _x1*_z2 + _y1*_w2 + _z1*_x2,
            _w1*_z2 + _x1*_y2 - _y1*_x2 + _z1*_w2
        ])
        _q_rel /= np.linalg.norm(_q_rel)
        
        _angle = 2*np.arccos(np.clip(_q_rel[0], -1, 1))
        if _angle < 1e-8:
            return np.zeros(3)
        _axis = _q_rel[1:] / np.sin(angle/2)
        _omega = (_angle/dt) * _axis
        
        _w, _x, _y, _z = _q1
        _roll  = np.arctan2(2*(_w*_x + _y*_z), 1 - 2*(_x*_x + _y*_y))
        _pitch = np.arcsin(np.clip(2*(_w*_y - _z*_x), -1, 1))
        
        _phi, _theta = _roll, _pitch
        _T = np.array([
            [1, np.sin(_phi)*np.tan(_theta), np.cos(_phi)*np.tan(_theta)],
            [0, np.cos(_phi),              -np.sin(_phi)],
            [0, np.sin(_phi)/np.cos(_theta), np.cos(_phi)/np.cos(_theta)]
        ])

        rotRates = _T @ _omega 

    def q2Euler(self):
        _sinr_cosp = 2 * (self.q[0] * self.q[1] + self.q[2] * self.q[3])
        _cosr_cosp = 1 - 2 * (self.q[1]**2 + self.q[2]**2)
        self.[0] = math.atan2(_sinr_cosp, _cosr_cosp)

        _sinp = 2 * (self.q[0] * self.q[2] - self.q[3] * self.q[1])
        _sinp = max(-1.0, min(1.0, _sinp))  #clamp
        self.[1] = math.asin(_sinp)

        _siny_cosp = 2 * (self.q[0] * self.q[3] + self.q[1] * self.q[2])
        _cosy_cosp = 1 - 2 * (self.q[2]**2 + self.q[3]**2)
        self.rot[2] = math.atan2(_siny_cosp, _cosy_cosp)

    def allocatePrev(self):
        self.posP = self.pos
        self.velP = self.vel
        self.qP = self.q
        self.rotP = self.rot

    def lpf(new_value, prev_value, alpha=0.6):
        return alpha * new_value + (1 - alpha) * prev_value

    def filter(self, position=False, velocity=False, quat=False, rotation=False):
        if position==True:
            for i in self.pos:
                self.posFil[i] = self.lpf(self.pos[i], self.posP[i], self.alphaPos)

        if velocity==True:
            for i in self.vel:
                self.velFil[i] = self.lpf(self.vel[i], self.velP[i], self.alphaVel)

        if quat==True:
            for i in self.quat:
                self.qFil[i] = self.lpf(self.q[i], self.qP[i], self.alphaQ)

        if rotation==True:
            for i in self.rot:
                self.rotFil[i] = self.lpf(self.rot[i], self.rotP[i], self.alphaRot)

    #TODO
    #create a filter based on successive gradient
