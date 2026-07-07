import serial
import time

def listen_rfid(port="COM3", baudrate=9600, timeout=5):
    """
    Reads RFID UID from Arduino via Serial.
    SAFE MODE:
    - If hardware not connected → returns None
    - No crash, no error
    """

    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Arduino reset time

        start_time = time.time()

        while time.time() - start_time < timeout:
            if ser.in_waiting:
                uid = ser.readline().decode("utf-8").strip()
                ser.close()
                return uid

        ser.close()
        return None

    except Exception as e:
        # 🔒 FAIL SAFE — PROJECT WILL NOT CRASH
        return None
