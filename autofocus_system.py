import re
import control
import numpy as np
from tf_block import tf_block

# System coefficients
R = 7.5         # Resistance in                 [Ohms]
L = 0.000144    # Inductance in                 [H]
m = 0.00049     # Total mass bobbin and lens    [kg]
b = 0.175       # Damping coefficient           [N sec/m]
k = 13.2264     # Stiffnes                      [N/m]
B = 0.454       # Magnetic flux density         [wb/m^3]
n = 123         # Number of coil turns          [-]
l = 0.01        # Coil effective                [m]

class autofocus_PI:
    def __init__(self, kp, ki):
        self.kp = kp    # Proportional constant         [0, 1.82E5]
        self.ki = ki    # Integral cnst                 [0, 9.018E4 / kp + 507.6364]

        ##### Initiate blocks #####
        # Gc(s) -> PI Controller
        self.Gc = tf_block("Gc","controller","Gc(s)",[kp, kp*ki],[1,0])

        # Gu(s) -> actuator driver
        self.Gu = tf_block("Gu","actuator driver","Gu(s)", [1], [1])

        # Gp(s) -> focusing system
        numGp = np.array([n*B*l])
        denGp = np.array([L*m, L*b + R*m, L*k + R*b + 2*(n*B*l)**2, R*k])
        self.Gp = tf_block("Gp","focusing system","Gp(s)", numGp, denGp)

        # D(s) -> disturbance
        self.Ds = tf_block("Ds","focusing system","Ds(s)", [0], [1])

        # Gs(s) -> sensor
        self.Gs = tf_block("Gs","sensor","Gs(s)",[1],[1])


        self.series = control.series(self.Gc.tf, self.Gp.tf)
        self.system = control.feedback(self.series,1)

    def print_tf(self):
        print(f"The system Transfer Funtion for kp = {self.kp} and ki = {self.ki} is", self.system)

    def time_to_ms(self, t):
        return [ms*1000 for ms in t]

    def step_response(self, t_step = 0, t1 = 0, step = 1, dt = 0.0001):

        t, u = self.get_step_input(t_step,t1,step,dt)

        # Simulate response
        (t, y) = control.forced_response(self.system, t, u)

        t = self.time_to_ms(t)

        return (t, y)

    def get_step_input(self, t_step = 0, t1 = 0, step = 1, dt = 0.0001):
        self.t_step = t_step
        self.t1 = t1
        self.step = step
        self.dt = dt

        # Defining signals
        nt = int(self.t1/self.dt) + 1 # Number of points of sim time
        t = np.linspace(0,self.t1,nt)
        u = self.step*np.ones(nt)
        
        # Create Step input
        if self.t_step:
            for i in range(int(len(u)*(self.t_step/self.t1))):
                u[i] = 0

        return (t, u)