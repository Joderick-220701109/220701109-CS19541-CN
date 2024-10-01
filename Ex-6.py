def to_binary(char):
    return format(ord(char), '08b')

def calculate_redundant_bits(m):
    r = 0
    while (1 << r) < (m + r + 1):
        r += 1
    return r

def insert_redundant_bits(data, m, r):
    encoded = ['0'] * (m + r)
    j = 0
    for i in range(1, m + r + 1):
        if (i & (i - 1)) == 0:  # Power of 2 positions for redundant bits
            continue
        encoded[i - 1] = data[j]
        j += 1

    # Calculating redundant bits
    for i in range(r):
        pos = (1 << i)
        xor_sum = 0
        for j in range(pos - 1, m + r, pos * 2):
            for k in range(j, min(j + pos, m + r)):
                xor_sum ^= int(encoded[k])
        encoded[pos - 1] = str(xor_sum)

    return ''.join(encoded)

def apply_hamming_code(text):
    binary_data = ''.join([to_binary(char) for char in text])
    print(f"Binary representation: {binary_data}")

    m = len(binary_data)
    r = calculate_redundant_bits(m)
    encoded_data = insert_redundant_bits(binary_data, m, r)

    print(f"Encoded data with redundant bits: {encoded_data}")
    print(f"Redundant bit positions: {[1 << i for i in range(r)]}")
    return encoded_data, r

def check_and_correct(encoded_data, r):
    m = len(encoded_data) - r
    error_position = 0

    for i in range(r):
        pos = (1 << i)
        xor_sum = 0
        for j in range(pos - 1, len(encoded_data), pos * 2):
            for k in range(j, min(j + pos, len(encoded_data))):
                xor_sum ^= int(encoded_data[k])
        error_position |= (xor_sum << i)

    if error_position:
        print(f"Error found at position: {error_position}")
        corrected_data = list(encoded_data)
        corrected_data[error_position - 1] = '0' if encoded_data[error_position - 1] == '1' else '1'
        print(f"Corrected data: {''.join(corrected_data)}")
    else:
        print("No error found.")
        corrected_data = list(encoded_data)

    return ''.join(corrected_data), error_position

def extract_original_data(corrected_data, r):
    m = len(corrected_data) - r
    data_bits = []

    for i in range(1, m + r + 1):
        if (i & (i - 1)) != 0:  # Non-redundant bit positions
            data_bits.append(corrected_data[i - 1])

    binary_str = ''.join(data_bits)
    return ''.join([chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8)])

def main():
    # Sender side
    text = input("Enter the text to encode: ")
    encoded_data, r = apply_hamming_code(text)

    # Ask user to change any bit
    change = input("Do you want to change any bit in the encoded data? (yes/no): ").strip().lower()
    if change == 'yes':
        position = int(input(f"Enter the bit position to change (1-{len(encoded_data)}): "))
        if 1 <= position <= len(encoded_data):
            is_redundant = position in [1 << i for i in range(r)]
            encoded_data = list(encoded_data)
            encoded_data[position - 1] = '0' if encoded_data[position - 1] == '1' else '1'
            encoded_data = ''.join(encoded_data)
            print(f"Data after bit change: {encoded_data}")
            if is_redundant:
                print(f"Note: You changed a redundant bit at position {position}.")
        else:
            print("Invalid position. No changes made.")

    # Receiver side
    corrected_data, error_position = check_and_correct(encoded_data, r)
    if change == 'yes' and is_redundant and error_position == position:
        print("The change in the redundant bit was correctly detected.")
    elif change == 'yes' and is_redundant and error_position != position:
        print("The change in the redundant bit was not detected.")
    original_text = extract_original_data(corrected_data, r)

    print(f"Decoded text: {original_text}")

if __name__ == "__main__":
    main()
