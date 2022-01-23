"""
Code adapted from https://github.com/ivmech/ivPID
License
"""

class PID:
    def __init__(self, P=0.2, I=0.0, D=0.0, delta_time=0.1):

        self.Kp, self.Ki, self.Kd = P, I, D
        self.sample_time = delta_time
        
        self.PTerm, self.ITerm, self.DTerm = 0.0, 0.0, 0.0
        self.last_error, self.int_error = 0.0, 0.0
        self.windup_guard = 20.0
        
        self.SetPoint = 0.0
        self.output = 0.0

    def update(self, feedback_value, current_time=None):
        """Calculates PID value for given reference feedback
            u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}
        """
        error = self.SetPoint - feedback_value
        delta_time = self.sample_time
        delta_error = error - self.last_error

        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Remember last error for next calculation
            self.last_error = error

            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)