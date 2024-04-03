# Seat-Smart

## What is it?

Seat-Smart is a Python-based application that demonstrates a single server-multiple client system. It allows clients to book classes through a GUI interface while ensuring security using SSL certification.

## How to Use

### Using on the Same Device:

1. Clone the repository:

   ```bash
   git clone https://github.com/Noodle-bg/SeatSmart
   ```

2. Change directory into the cloned repository:

   ```bash
   cd SeatSmart
   ```

3. Ensure that both `clientgui1.py` and `server.py` have the `HOST` string set as `HOST = 'localhost'`.

4. Open a terminal and run the server:

   ```bash
   python3 server.py
   ```

5. Open another terminal and run the client GUI:

   ```bash
   python3 clientgui1.py
   ```

6. When prompted with the passcode, enter `dhan`.

7. Now the clients should be able to use the software.

### Using on Multiple Devices:

1. Connect all users to one single localhost (hotspot or LAN).

2. Identify the IP address of the server device:

   - Use the `ifconfig` command.
   - Identify the appropriate IP address based on the network card utilized for the local connection.

3. Update all instances of `HOST` in both `clientgui1.py` and `server.py` with the identified IP address.

4. Clone the repository:

   ```bash
   git clone https://github.com/Noodle-bg/SeatSmart
   ```

5. Change directory into the cloned repository:

   ```bash
   cd SeatSmart
   ```

6. Note: All users, both clients and the server, must have the `.crt` files.

7. Follow steps 4-7 from "Using on the Same Device" section.

## How to Run

1. Run the server:

   ```bash
   python3 server.py
   ```

2. Open another terminal and run the client GUI:

   ```bash
   python3 clientgui1.py
   ```

3. When prompted with the passcode, enter `dhan`.

4. Now the clients should be able to use the software.
