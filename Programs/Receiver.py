import time
# Function to receive and acknowledge frames
def receive_frames():
    while True:
        # Read the Sender_Buffer file
        with open("Sender_Buffer.txt", "r") as f:
            sender_buffer = f.read().strip().split("\n")
        
        print("Received frames:", sender_buffer)
        
        receiver_buffer = []
        for frame in sender_buffer:
            # Extract frame number (assuming format "Frame No: X, DATA: Y")
            try:
                frame_no = int(frame.split(",")[0].split()[-1])
            except (ValueError, IndexError):
                print(f"Invalid frame format: {frame}")
                continue

            # Simulate correct acknowledgment for even-numbered frames
            if frame_no % 2 == 0:
                ack = f"ACK {frame_no}"
            else:
                ack = f"NACK {frame_no}"
            
            receiver_buffer.append(ack)
        
        # Write ACK/NACK to Receiver_Buffer file
        with open("Receiver_Buffer.txt", "w") as f:
            for ack in receiver_buffer:
                f.write(f"{ack}\n")
        
        print("ACK/NACK sent:", receiver_buffer)
        
        # Simulate delay before checking for new frames
        time.sleep(2)

# Start receiving frames and sending ACK/NACK
receive_frames()
