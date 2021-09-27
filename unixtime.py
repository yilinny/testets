import datetime

def convert_to_unix(time):
    time_object= datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S %z')
    unix_time = datetime.datetime.timestamp(time_object)

    return(unix_time)



