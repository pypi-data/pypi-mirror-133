def time_to_sec(time):
    global x
    x = 0

    if time.endswith('s'):
        x = int(time[:-1])
    elif time.endswith('m'):
        x = int(time[:-1])*60
    elif time.endswith('h'):
        x =(int(time[:-1])*60)*60
    elif time.endswith('d'):
        x = ((int(time[:-1])*60)*60)*24

    return int(x)