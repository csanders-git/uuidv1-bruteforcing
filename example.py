import uuid
import datetime
import time

def binary_to_mac(mac_int):
    result = []
    for shift in range (0, 48, 8):
        # Shift the byte we care about to the LSB
        shifted = (mac_int >> shift)
        # Grab just the LSB
        adjusted = shifted & 0xff
        # Convert that number to hex
        hex = '{:02x}'.format(adjusted)
        result.append(hex)
    # Flip the list
    result.reverse()
    mac = ":".join(result)
    return mac

def return_mac_binary(mac_int):
    return format(mac_int, '048b')

def get_first_three(node_portion):
    network = binary_to_mac(node_portion)
    splits = network.split(':', 3)
    relevent_splits = splits[:-1]
    result_binary = ""
    for split in relevent_splits:
        dec = int(split, 16)
        binary = format(dec, '08b')
        result_binary += binary
    return result_binary

def generate_all_sequences():
    clock_sequences = []
    for clock_seq in range(0, 16384):
        # This is 255 which guarantees a leading 1 (v1)
        clock_seq_low = clock_seq & 0xff
        # 0x3f is 63 which means it will always have a leading 0
        clock_seq_hi_variant = (clock_seq >> 8) & 0x3f
        low_binary = format(clock_seq_low, '08b')
        hi_binary = format(clock_seq_hi_variant, '08b')
        sequence = int(hi_binary + low_binary, 2)
        clock_sequences.append(sequence)
    return clock_sequences

def generate_times(base_time, variance_seconds):
    # Taken from Daniel Thatcher's guidtools
    # https://github.com/intruder-io/guidtool/
    dt_zero = datetime.datetime(1582, 10, 15)
    base_guid_time = base_time - dt_zero
    base_timestamp = int(base_guid_time.total_seconds() * 1e7)
    start =  int(base_timestamp - (1e7)*variance_seconds)
    end =  int(base_timestamp + (1e7)*variance_seconds)
    for t in range(start, end):
        yield t



nonce = uuid.uuid1()
node_portion = nonce.node
node_time = nonce.time
node_seq = nonce.clock_seq
print(binary_to_mac(node_portion))
first_three_bits = get_first_three(node_portion)
mac = ""

base_time = datetime.datetime.now()
for my_time in generate_times(base_time, 1):
    start = time.time()
    sequences = generate_all_sequences()
    for sequence in sequences:
        for i in range(0, 16777215):
            last_three_bits = format(i, '024b')
            test = str(first_three_bits) + str(last_three_bits)
            test = int(test, 2)
    end = time.time()
    print(f"Took {end-start} seconds to generate all combinations")


