from djitellopy import tello

me = tello.Tello()
me.connect()
print('Battery Level ', me.get_battery(), "%")

me.takeoff()
me.land()

