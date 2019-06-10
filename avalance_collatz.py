import random, string

def get_hash (orig_bit_string, iv, output_length):

    msg_len = len(orig_bit_string)
    padding_block = False
    block_index = 0

    while(block_index*output_length < msg_len):

        # check if last block
        next_block_index = (block_index+1)*output_length    
        if next_block_index >= msg_len: # this is the last block

            bit_string = orig_bit_string[block_index*output_length:msg_len]
            
            # check if there is space for 64 bits
            space_left = next_block_index - msg_len
            if space_left < 64:
                bit_string.zfill(output_length)
                msg_len_bit = ""
                padding_block = True       

            else: # last block can contain last 64   
                while(len(bit_string) + 64 < output_length): # padding 0's to the last block
                    bit_string += "0"

                msg_len_bit = format(msg_len, 'b')
                msg_len_bit.zfill(64)

            if(block_index == 0): # first and last block
                hash_input = iv + bit_string + msg_len_bit
                xl = iv
            else: 
                hash_input = bit_hash_output + bit_string + msg_len_bit
                xl = bit_hash_output
            xr = bit_string + msg_len_bit

        else: # not last block

            # bit_string Definition if not last block
            bit_string = orig_bit_string[block_index*output_length:block_index*output_length+output_length]

            if(block_index == 0): # first and last block
                hash_input = iv + bit_string
                xl = iv
            else: 
                hash_input = bit_hash_output + bit_string
                xl = bit_hash_output
            xr = bit_string
        
        s = ""
        i = 0
        int_hash = int(hash_input, 2)

        while (i < output_length):
            if (int_hash % 2 == 0): # even
                temp = format(int_hash, 'b')
                temp = "0" + temp[0:len(temp)-1] # bitwise shift to the right or divide by two
                int_hash = int(temp, 2)
                s = "0" + s
            else: #odd
                int_hash = (3*int_hash) +1
                temp = format(int_hash, 'b')
                temp = "0" + temp[0:len(temp)-1] # bitwise shift to the right or divide by two
                int_hash = int(temp, 2)
                s = "1" + s
            i += 1
        
        hash_bit = format(int_hash, 'b')
        hash_bit = hash_bit.zfill(output_length*2)

        xpl = hash_bit[0:output_length]
        xpr = hash_bit[output_length:output_length*2]

        # xors
        hash_output = int(xl, 2) ^ int(xr, 2)
        hash_output = hash_output ^ int(xpl, 2)
        hash_output = hash_output ^ int(xpr, 2)
        hash_output = hash_output ^ int(s, 2)
        bit_hash_output = format(hash_output, 'b')
        bit_hash_output = bit_hash_output.zfill(output_length)
        
        block_index += 1

    if (padding_block == True):
        pb_content = "0"

        while(len(pb_content) + 64 < output_length): # padding 0's to the last block
            pb_content += "0"

        msg_len_bit = format(msg_len, 'b')
        msg_len_bit.zfill(64)
        hash_input = bit_hash_output + bit_string + msg_len_bit

        xl = bit_hash_output
        xr = bit_string + msg_len_bit
        s = ""
        i = 0
        int_hash = int(hash_input, 2)

        while (i < output_length):
            if (int_hash % 2 == 0): # even
                temp = format(int_hash, 'b')
                temp = "0" + temp[0:len(temp)-1] #bitwise shift to the right or divide by two
                int_hash = int(temp, 2)
                s = "0" + s
            else: #odd
                int_hash = (3*int_hash) +1
                temp = format(int_hash, 'b')
                temp = "0" + temp[0:len(temp)-1] #bitwise shift to the right or divide by two
                int_hash = int(temp, 2)
                s = "1" + s
            i += 1
        
        hash_bit = format(int_hash, 'b')
        hash_bit = hash_bit.zfill(output_length*2)

        xpl = hash_bit[0:output_length]
        xpr = hash_bit[output_length:output_length*2]

        # xors
        hash_output = int(xl, 2) ^ int(xr, 2)
        hash_output = hash_output ^ int(xpl, 2)
        hash_output = hash_output ^ int(xpr, 2)
        hash_output = hash_output ^ int(s, 2)
        bit_hash_output = format(hash_output, 'b')
        bit_hash_output = bit_hash_output.zfill(output_length)

    return bit_hash_output;
    # end of get_hash

# get preliminary input
output_length = 1024
input_string = ''.join(random.choice(string.ascii_letters + string.digits) for a in range(int(output_length/8)))
input_bits = ''.join(format(ord(char), 'b').zfill(8) for char in input_string)
print("input_bits: ", len(input_bits))
iv_string = ''.join(random.choice(string.ascii_letters + string.digits) for a in range(int(output_length/8)))
iv_bits = ''.join(format(ord(char), 'b').zfill(8) for char in iv_string)

# initial loop values
iterations = output_length
counter = [None] * (iterations - 1)
x = 0

# loop
while (x < iterations):
    
    bit_hash_output = get_hash(input_bits, iv_bits, output_length)

    if(x > 0):
        counter[x-1] = 0
        y = 0
        while(y < output_length):
            if(prev_hash_output[y] != bit_hash_output[y]):
                counter[x-1] += 1
            y += 1

    prev_hash_output = bit_hash_output
    temp_list = list(input_bits)
    if(input_bits[x] == "0"):        
        temp_list[x] = "1"
    else:
        temp_list[x] = "0"
    input_bits = ''.join(temp_list)

    print("x: ", x)
    x += 1

# compute average changed bits
x = 0
total = 0
while(x < iterations-1):
    total += counter[x]
    x += 1
average = total/(iterations-1)
print("Average: ", average)
percentage = average/output_length
print("Percentage: ", percentage)