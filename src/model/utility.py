from datetime import datetime


def start_timer():
    global start_time_ms
    start_time_ms = datetime.now()


def stop_timer():
    global end_time_ms
    end_time_ms = datetime.now()


def get_code_time_execution():
    print("DURATION ms:\t", end_time_ms-start_time_ms)
