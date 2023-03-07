
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
        try:
            ref_v = sensor.reflection()
            deviation = ref_v - threshold 
            turn_rate = prop_gain * deviation
            robot.drive(drive_speed,turn_rate)
            dist = robot.distance()
            print(f"total_distance: {dist},made_turn: {turn_rate}, ref_value: {ref_v}, deviation: {deviation}")
            tab.append([dist,turn_rate])
            prev_dist = dist
        except KeyboardInterrupt:
            break
    return tab