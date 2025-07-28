from djitellopy import Tello
import socket
import time

# Initialize and connect to Tello
tello = Tello()
tello.connect()
print('Battery Level ', tello.get_battery(), "%")

# Create a UDP socket to send EXT command
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)

# Send EXT command to enable mled (matrix LED)
# dot_matrix_cmd = "EXT mled m 8 8 3C4200818181423C"
# udp_socket.sendto(dot_matrix_cmd.encode('utf-8'), tello_address)


heart_hex = "EXT mled m 8 8 6699818142241800"
udp_socket.sendto(heart_hex.encode('utf-8'), tello_address)

# Wait a few seconds for the display
time.sleep(5)

# Optional: clear the display
clear_cmd = "EXT mled m 8 8 0000000000000000000000000000000000000000000000000000000000000000"
udp_socket.sendto(clear_cmd.encode('utf-8'), tello_address)

# End connection
tello.end()
