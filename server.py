import socket
import threading
import json
import ssl
import time
from queue import Queue

HOST = 'localhost'
PORT = 9999
CERT_FILE = 'server.crt'
KEY_FILE = 'server.key'

classes_info = {
    'AFLL': {'teacher': 'Mr. Sharma', 'timing': '10:00 AM', 'seats': 2},
    'OS': {'teacher': 'Ms. Preet', 'timing': '12:00 PM', 'seats': 3},
    'CN': {'teacher': 'Dr. Ganesh', 'timing': '2:00 PM', 'seats': 1},
    'DAA': {'teacher': 'Dr. Prasad', 'timing': '4:00 PM', 'seats': 6}
}

user_bookings = {}

class QueueItem:
    def __init__(self, client_addr, class_name, num_seats):
        self.client_addr = client_addr
        self.class_name = class_name
        self.num_seats = num_seats
        self.timestamp = time.time()

def display_classes(classes_info):
    print("Classes:")
    for class_name, details in classes_info.items():
        print(f"\nClass: {class_name}")
        print(f"Teacher: {details['teacher']}")
        print(f"Timing: {details['timing']}")
        print(f"Available seats: {details['seats']}")


def handle_client(conn, addr):
    print(f"Connected by {addr}")
    conn = ssl.wrap_socket(conn, keyfile=KEY_FILE, certfile=CERT_FILE, server_side=True)

    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            print(f"Disconnected from {addr}")
            break

        if data == 'get_classes':
            conn.send(json.dumps(classes_info).encode('utf-8'))
        elif data.startswith('book_class'):
            _, class_name, num_seats_str = data.split()
            num_seats = int(num_seats_str)
            if class_name in classes_info and classes_info[class_name]['seats'] >= num_seats:
                if class_name not in user_bookings:
                    user_bookings[class_name] = {}
                if addr not in user_bookings[class_name]:
                    user_bookings[class_name][addr] = 0
                if user_bookings[class_name][addr] + num_seats <= 3:
                    classes_info[class_name]['seats'] -= num_seats
                    user_bookings[class_name][addr] += num_seats
                    conn.send("Booking successful".encode('utf-8'))
                else:
                    conn.send("Booking failed. Maximum 3 seats allowed per user for this class".encode('utf-8'))
            else:
                conn.send("Booking failed. Not enough seats available".encode('utf-8'))
        elif data.startswith('cancel_booking'):
            _, class_name, num_seats_str = data.split()
            num_seats = int(num_seats_str)
            if class_name in classes_info and addr in user_bookings[class_name]:
                if user_bookings[class_name][addr] >= num_seats:
                    classes_info[class_name]['seats'] += num_seats
                    user_bookings[class_name][addr] -= num_seats
                    conn.send("Booking cancelled successfully".encode('utf-8'))

                    # Check queue for waiting clients
                    if class_name in booking_queue:
                        while not booking_queue[class_name].empty():
                            queue_item = booking_queue[class_name].get()
                            if time.time() - queue_item.timestamp <= 600:  # Check if within 10 minutes
                                conn.send(f"Seats are now available for class {queue_item.class_name}. You can book {queue_item.num_seats} seat(s).".encode('utf-8'))
                                break
                else:
                    conn.send("Cancellation failed. You have not booked this many seats".encode('utf-8'))
            else:
                conn.send("Class not found or no booking found".encode('utf-8'))

    conn.close()

# Create a queue dictionary to hold the queue for each class
booking_queue = {class_name: Queue() for class_name in classes_info.keys()}

def main():
    # SSL 
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server started on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("Server shutting down...")
        server.close()

if __name__ == "__main__":
    main()
