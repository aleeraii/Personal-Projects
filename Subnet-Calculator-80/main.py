def subnet_calc():
    while True:
        try:
            initial_input = input("Enter IP Address/CIDR: ")
            main_input = initial_input.split('/')
            ip_address = main_input[0]
            cidr_subnet_mask = main_input[1]
            # Checking IP address validity
            a = ip_address.split('.')
            if ((len(a) == 4) and (1 <= int(a[0]) <= 255 and 0 <= int(a[1]) <= 255 and 0 <= int(a[2]) <= 255 and 0 <= int(a[3]) <= 255)) and 0 <= int(cidr_subnet_mask) <= 32:
                break
            else:
                print("\nThe IP or CIDR is INVALID! Please retry!\n")
                continue
        except:
            print("\nThe IP or CIDR is INVALID! Please retry!\n")
            continue

    # checking class of Ip Address
    ip_class = ''
    if 0 <= int(a[0]) <= 127:
        ip_class = "A"
    elif 128 <= int(a[0]) <= 191:
        ip_class = "B"
    elif 192 <= int(a[0]) <= 223:
        ip_class = "C"
    elif 224 <= int(a[0]) <= 239:
        ip_class = "D"
    elif 240 <= int(a[0]) <= 255:
        ip_class = "E"

    cidr = int(cidr_subnet_mask)
    mask = [0, 0, 0, 0]
    for i in range(cidr):
        mask[i // 8] = mask[i // 8] + (1 << (7 - i % 8))

    subnet_mask = ".".join(map(str, mask))

    # Convert mask to binary string
    mask_octets_padded = []
    mask_octets_decimal = subnet_mask.split(".")
    # print mask_octets_decimal

    for octet_index in range(0, len(mask_octets_decimal)):

        # print bin(int(mask_octets_decimal[octet_index]))

        binary_octet = bin(int(mask_octets_decimal[octet_index])).split("b")[1]
        # print binary_octet

        if len(binary_octet) == 8:
            mask_octets_padded.append(binary_octet)

        elif len(binary_octet) < 8:
            binary_octet_padded = binary_octet.zfill(8)
            mask_octets_padded.append(binary_octet_padded)

    # print mask_octets_padded

    decimal_mask = "".join(mask_octets_padded)
    # Example: for 255.255.255.0 => 11111111111111111111111100000000

    # Counting host bits in the mask and calculating number of hosts/subnet
    no_of_zeros = decimal_mask.count("0")
    no_of_ones = 32 - no_of_zeros
    no_of_hosts = abs(2 ** no_of_zeros - 2) # return positive value for mask /32

    # Obtaining wildcard mask
    wildcard_octets = []
    for w_octet in mask_octets_decimal:
        wild_octet = 255 - int(w_octet)
        wildcard_octets.append(str(wild_octet))

    # print wildcard_octets

    wildcard_mask = ".".join(wildcard_octets)
    # print wildcard_mask

    # Convert IP to binary string
    ip_octets_padded = []
    ip_octets_decimal = ip_address.split(".")

    for octet_index in range(0, len(ip_octets_decimal)):

        binary_octet = bin(int(ip_octets_decimal[octet_index])).split("b")[1]

        if len(binary_octet) < 8:
            binary_octet_padded = binary_octet.zfill(8)
            ip_octets_padded.append(binary_octet_padded)

        else:
            ip_octets_padded.append(binary_octet)

    # print ip_octets_padded

    binary_ip = "".join(ip_octets_padded)

    # print binary_ip   #Example: for 192.168.2.100 => 11000000101010000000001001100100

    # Obtain the network address and broadcast address from the binary strings obtained above

    network_address_binary = binary_ip[:(no_of_ones)] + "0" * no_of_zeros
    # print network_address_binary

    broadcast_address_binary = binary_ip[:(no_of_ones)] + "1" * no_of_zeros
    # print broadcast_address_binary

    net_ip_octets = []
    for octet in range(0, len(network_address_binary), 8):
        net_ip_octet = network_address_binary[octet:octet+8]
        net_ip_octets.append(net_ip_octet)

    # print net_ip_octets

    net_ip_address = []
    for each_octet in net_ip_octets:
        net_ip_address.append(str(int(each_octet, 2)))

    # print net_ip_address

    network_address = ".".join(net_ip_address)
    # print network_address

    bst_ip_octets = []
    for octet in range(0, len(broadcast_address_binary), 8):
        bst_ip_octet = broadcast_address_binary[octet:octet+8]
        bst_ip_octets.append(bst_ip_octet)

    # print bst_ip_octets

    bst_ip_address = []
    for each_octet in bst_ip_octets:
        bst_ip_address.append(str(int(each_octet, 2)))

    # print bst_ip_address

    broadcast_address = ".".join(bst_ip_address)
    # print broadcast_address

    # Results for selected IP/mask
    print("\n")
    print("CIDR IP: %s" % initial_input)
    print("Ip Address: %s" % ip_address)
    print("CIDR Subnet Mask: /%s" % no_of_ones)
    print("Subnet Mask: %s" % subnet_mask)
    print("Binary Subnet Mask: %s" % decimal_mask)
    print("IP Class: %s" % ip_class)
    print("Wildcard mask: %s" % wildcard_mask)
    print("Network address is: %s" % network_address)
    print("Broadcast address is: %s" % broadcast_address)
    print("Number of valid hosts per subnet: %s" % no_of_hosts)


# Calling the function
subnet_calc()
