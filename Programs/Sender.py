import time

# Function to send frames
def send_frames(frames, window_size):
    current_frame = 0
    acked_frames = [False] * len(frames)  # Keeps track of acknowledged frames

    while current_frame < len(frames):
        sender_buffer = []

        # Send frames in the window, skip already acknowledged frames
        for i in range(window_size):
            frame_index = current_frame + i
            if frame_index < len(frames) and not acked_frames[frame_index]:
                frame = f"Frame No: {frame_index}, DATA: {frames[frame_index]}"
                sender_buffer.append(frame)

        if sender_buffer:
            # Write frames to Sender_Buffer file
            with open("Sender_Buffer.txt", "w") as f:
                for frame in sender_buffer:
                    f.write(f"{frame}\n")

            print("Frames sent:", sender_buffer)

        # Wait for receiver acknowledgment
        time.sleep(2)

        # Read the Receiver_Buffer file for ACK/NACK
        with open("Receiver_Buffer.txt", "r") as f:
            ack_data = f.read().strip().split("\n")

        print("Received ACK/NACK:", ack_data)

        # Process ACK/NACK
        for ack in ack_data:
            if "ACK" in ack:
                ack_no = int(ack.split()[1])
                acked_frames[ack_no] = True
            elif "NACK" in ack:
                nack_no = int(ack.split()[1])
                acked_frames[nack_no] = False
                current_frame = nack_no  # Retransmit the NACK-ed frame

        # Move the window forward only if all frames in the current window are acknowledged
        if all(acked_frames[current_frame:current_frame + window_size]):
            current_frame += window_size

# Input the window size and the message
window_size = int(input("Enter the Window Size: "))
message = input("Enter the message to send: ")

# Create frames with 1 character per frame
frames = [char for char in message]

# Send frames using sliding window
send_frames(frames, window_size)
