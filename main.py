from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
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
    values = [min_v,max_v,target_v]
    motor.stop()
    return values
    
scanned_v = scan(neck_motor,sens) 



def log():
    pass


def follow_line(robot,sensor,values):
    black = values[0]
    white = values[1]
    threshold = values[2]

    drive_speed = 50
    prop_gain = 2
    tab = []
    prev_dist = 0
    prev_ref_v = white

    while True:
        ref_v = sensor.reflection()
        deviation = ref_v - threshold 
        turn_rate = prop_gain * deviation
        robot.drive(drive_speed,turn_rate)
        dist = robot.distance()
        print(f"total_distance: {dist},made_turn: {turn_rate}, ref_value: {ref_v}, deviation: {deviation}")
        tab.append([dist,turn_rate])
        prev_dist = dist
    
        #wait(2000)
    return tab
#tab = follow_line(robot,sens,scanned_v)
#print(tab)


#x = matrix(sens,scanned_v)

def fix_pos(neck,sensor,threshold):
    if sensor.reflection() <= threshold:
        return -neck.angle()
    max_rotate = neck.run_until_stalled(-200, duty_limit=40)/2
    lowest_ref, low_ref_angle = 100, 0
    
    for i in range(max_rotate,abs(max_rotate)):
        ref_v = sensor.reflection()
        neck.run_target(200,i)
        if ref_v <= threshold:
            return -neck.angle()
        

def follow(robot,neck,sensor,values):
    black = values[0]
    white = values[1]
    threshold = values[2]
    prev_distance = 0

    log = []

    prop_gain = 0.75

    while True and len(log) <= 35:
        angle = fix_pos(neck,sensor,threshold)
        #error = ref_v - threshold 
        #turn_rate = prop_gain * error + angle

        robot.turn(angle)
        real_dist = robot.distance() - prev_distance
        print(f"Real dist: {real_dist} Turn angle: {angle}")
        log.append([real_dist,angle])
        prev_distance = robot.distance()
        if robot.done():
            robot.straight(30)
    return log

tab = follow(robot,neck_motor,sens,scanned_v)

print(tab)