'''
mixers.py

Classes to wrap motor controllers into a functional drive unit.
'''

import time


class BaseMixer():

    def update_angle(self, angle):
        pass

    def update_throttle(self, throttle):
        pass

    def update(self, throttle=0, angle=0):
        '''Convenience function to update
        angle and throttle at the same time'''
        self.update_angle(angle)
        self.update_throttle(throttle)



class AckermannSteeringMixer(BaseMixer):
    '''
    Mixer for vehicles steered by changing the angle of the front wheels.
    This is used for RC cars
    '''
    def __init__(self, 
                 steering_actuator=None, 
                 throttle_actuator=None):
        self.steering_actuator = steering_actuator
        self.throttle_actuator = throttle_actuator


    def update(self, throttle, angle):
        self.steering_actuator.update(angle)
        self.throttle_actuator.update(throttle)



class DifferentialDriveMixer:
    """
    Mixer for vehicles driving differential drive vehicle.
    Currently designed for cars with 2 wheels.
    """
    def __init__(self, left_motor, right_motor):

        self.left_motor = left_motor
        self.right_motor = right_motor
                
        self.angle=0
        self.throttle=0
    

    def update(self, throttle, angle):
        self.throttle = throttle
        self.angle = angle
        
        if throttle == 0 and angle == 0:
           self.stop()
        else:
            
            l_speed = ((self.left_motor.speed + throttle)/3 - angle/5)
            r_speed = ((self.right_motor.speed + throttle)/3 + angle/5)
            l_speed = min(max(l_speed, -1), 1)
            r_speed = min(max(r_speed, -1), 1)
            
            self.left_motor.turn(l_speed)
            self.right_motor.turn(r_speed)
            
            
    def test(self, seconds=1):
        telemetry = [(0, -.5), (0, -.5), (0, 0), (0, .5), (0, .5),  (0, 0), ]
        for t in telemetry:
            
            
            self.update(*t)
            print('throttle: %s   angle: %s' % (self.throttle, self.angle))
            print('l_speed: %s  r_speed: %s' % (self.left_motor.speed, 
                                                self.right_motor.speed))
            time.sleep(seconds)
            
        print('test complete')
        
        
    def stop(self):
        self.left_motor.turn(0)
        self.right_motor.turn(0)
