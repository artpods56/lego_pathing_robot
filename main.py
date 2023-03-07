from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Icon
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch



hub = InventorHub()
hub.speaker.volume(0)

right_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
left_motor = Motor(Port.A)
neck_motor = Motor(Port.D,reset_angle=True)
sens = ColorSensor(Port.B)
sens.lights.off()
robot = DriveBase(left_motor=left_motor, right_motor=right_motor, wheel_diameter=53,axle_track=108)



def scan(motor,sensor):

    max_rotate = motor.run_until_stalled(-200, duty_limit=40)
    motor.run_target(200,0)

    min_v = 100
    max_v = 0
    target_v = 0
    
    for i in range(max_rotate,abs(max_rotate),2):
        ref_v = sensor.reflection()
        if ref_v < min_v:
            min_v = ref_v
        if ref_v > max_v:
            max_v = ref_v
        motor.run_target(200,i)
        
    target_v = (min_v + max_v)/2

    if motor.done():
        print("Scan completed.")
        print(f"Values: {min_v},{max_v},{target_v}")
    
    
    motor.run_target(200,0)
    motor.stop()
    return target_v
    
threshold_v = scan(neck_motor,sens) 


def fix_pos(neck,sensor,threshold):

    if sensor.reflection() <= threshold+10:
        n_angle = neck.angle()
        neck.run_target(200,0)
        return -n_angle
    max_rotate = 80
    if neck.angle() >= 0:   
        for i in range(max_rotate,-max_rotate,-4):
            ref_v = sensor.reflection()
            neck.run_target(200,i)
            if ref_v <= threshold:
                return -neck.angle()
        return -90
    if neck.angle() < 0:
        for i in range(-abs(max_rotate),max_rotate,4):
            ref_v = sensor.reflection()
            neck.run_target(200,i)
            if ref_v <= threshold:
                return -neck.angle() 
        return 90 
    return 0
        
def follow(robot,neck,sensor,threshold):

    prev_distance = 0
    prev_angle = 0
    moves = []

    while True:
        if any(hub.buttons.pressed()):
            hub.display.icon(Icon.ARROW_RIGHT_DOWN)
            break
        angle = fix_pos(neck,sensor,threshold)

        if abs(angle) == 90:
            angle = -angle
        elif abs(angle) <= 50:
            angle = angle * 0.75
        elif abs(angle) > 50:
            angle = angle * 0.8
        if abs(angle) <= 20:
            angle = 0

        if robot.done():
            robot.straight(25)
            robot.turn(angle)
        
            
        real_dist = robot.distance() - prev_distance
        print(f"Real dist: {real_dist} Turn angle: {angle}")
        moves.append([real_dist,angle])
        if abs(prev_angle) == 90 and abs(angle) == 90:
            break

        prev_angle = angle
        prev_distance = robot.distance()
        
    return moves

log = follow(robot,neck_motor,sens,threshold_v)
print(log)
