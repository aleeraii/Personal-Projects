addzero = lambda x: (x not in "10") and '0' or x
def ip2network_address(ip, cidr):
    ip = ip.split('.')
    netmask = cidr2mask(cidr)
    bin_mask_list = ip2binlist(netmask)
    for x in range(len(ip)):
        ip[x] = int(ip[x]) & int(bin_mask_list[x], 2)
    if int(cidr) < 31:
        network_address = "%s.%s.%s.%s" % (ip[0], ip[1], ip[2], ip[3])
        first_avail_ip = "%s.%s.%s.%s" % (ip[0], ip[1], ip[2], ip[3] + 1)
        avail_host_numbers = 2 ** (32 - int(cidr)) - 2
        complement_bin_list = mask2complement_bin_list(netmask)
        broadcast_address = '.'.join([str(ip[x] + int(complement_bin_list[x], 2)) for x in range(4)])
        last_avail_ip_list = broadcast_address.split('.')[0:3]
        last_avail_ip_list.append(str(int(broadcast_address.split('.')[-1]) - 1))
        last_avail_ip = '.'.join(last_avail_ip_list)
    elif int(cidr) == 31:
        broadcast_address = network_address = None
        first_avail_ip = "%s.%s.%s.%s" % (ip[0], ip[1], ip[2], ip[3])
        last_avail_ip = "%s.%s.%s.%s" % (ip[0], ip[1], ip[2], ip[3] + 1)
        avail_host_numbers = 2
    else:
        broadcast_address = network_address = None
        first_avail_ip = "%s.%s.%s.%s" % (ip[0], ip[1], ip[2], ip[3])
        last_avail_ip = first_avail_ip
        avail_host_numbers = 1
    return avail_host_numbers, netmask, network_address, first_avail_ip, last_avail_ip, broadcast_address


def mask2cidr(mask='255.255.255.0'):
    '''
    1.  '255.11111.266.4' to '255.255.255.0' to 24
    2.  '255.128.255.0'  to 9
    '''
    mask_list = mask.split('.')
    mask_list = map(int, mask_list)  # int list
    notexcess = lambda x: (x > 255) and 255 or x  # if any one bigger than 255, set to 255
    # addzero= lambda x : ( x not in "10" ) and '0' or x    # set as global func
    mask_list = map(notexcess, mask_list)
    binmask_total = ''
    for x in mask_list:
        # for x in range(4):
        binmask = "%8s" % bin(x).split('0b')[1]  # '    1101'
        binmask = ''.join(map(addzero, list(binmask)))  # '00001101'  , addzero
        binmask_total += binmask
    try:
        zindex = binmask_total.index('0')
    except ValueError:
        zindex = 32
    return zindex


def cidr2mask(cidr='24'):
    cidr = int(cidr)
    fullnet = '0b11111111'
    zeronet = '0b00000000'
    if cidr <= 8:
        hosts = 8 - cidr
        net = '0b' + '1' * cidr + '0' * hosts
        net = (net, zeronet, zeronet, zeronet)
    elif 8 < cidr <= 16:
        hosts = 16 - cidr
        net = '0b' + '1' * (cidr - 8) + '0' * hosts
        net = (fullnet, net, zeronet, zeronet)
    elif 16 < cidr <= 24:
        cidr = cidr - 16
        hosts = 8 - cidr
        net = '0b' + '1' * cidr + '0' * hosts
        net = (fullnet, fullnet, net, zeronet)
    else:
        cidr = cidr - 24
        hosts = 8 - cidr
        # print cidr,hosts
        net = '0b' + '1' * cidr + '0' * hosts
        net = (fullnet, fullnet, fullnet, net)
    netmask = '.'.join([str(int(net[x], 2)) for x in range(len(net))])
    return netmask


def cidr2hex(cidr='24'):
    netmask = cidr2mask(cidr)
    bin_mask_list = ip2binlist(netmask)
    hex_list = [hex(int(b, 2)).split('0x')[1].upper() for b in bin_mask_list]
    return hex_list


def mask2complement_bin_list(mask='255.255.255.0'):
    xcomplement_bin_list = ip2binlist(mask)
    anti = lambda x: (x == '1') and '0' or '1'
    complement_bin_list = [''.join(map(anti, list(x))) for x in xcomplement_bin_list]
    return complement_bin_list


def ipmask2network_address(ip, mask):
    cidr = mask2cidr(mask)
    return ip2network_address(ip, cidr)


def ip2binlist(ip):
    iplist = ip.split('.')
    iplist = map(int, iplist)
    binlist = []
    for x in iplist:
        binmask = "%8s" % bin(x).split('0b')[1]  # '    1101'
        binmask = ''.join(map(addzero, list(binmask)))  # '00001101'  , addzero
        binlist.append(binmask)
    return binlist


binlist2hexlist = lambda binlist: [hex(int(b, 2)).split('0x')[1].upper() for b in binlist]


def ip2hexlist(ip):
    binlist = ip2binlist(ip)
    hex_list = [hex(int(b, 2)).split('0x')[1].upper() for b in binlist]
    return hex_list


def binlist2ip(binlist):
    add_bin_prefix = lambda binstr: '0b' + binstr
    bin2int = lambda bstr: str(int(bstr, 2))
    binlist = map(add_bin_prefix, binlist)
    ip = '.'.join(map(bin2int, binlist))
    return ip


def hexlist2ip(hexlist):
    add_hex_prefix = lambda xstr: '0x' + xstr
    hex2int = lambda bstr: str(int(bstr, 16))
    hexlist = map(add_hex_prefix, hexlist)
    ip = '.'.join(map(hex2int, hexlist))
    return ip


def hexlist2binlist(hexlist):
    ip = hexlist2ip(hexlist)
    return ip2binlist(ip)


def hostamount2cidr(amount=1):
    constant_hostnumber_list = []
    for cidr in range(32, -1, -1):
        constant_hostnumber_list.append(ip2network_address(cidr=cidr)[0])
        if ip2network_address(cidr=cidr)[0] >= amount:
            return cidr


def ip2class(ip):
    classful_dict = {
        int('1' * 1 + '0' * (8 - 1), 2): 'B',
        int('1' * 2 + '0' * (8 - 2), 2): 'C',
        int('1' * 3 + '0' * (8 - 3), 2): 'D',
        int('1' * 4 + '0' * (8 - 4), 2): 'E',
    }
    ip = ip2binlist(ip)[0]  # ip,  <type 'str'>
    if int(ip, 2) > 255:  # typo, should be 0 <= ip <= 255
        return None
    flags = []
    for leading in classful_dict.keys():
        if (int(ip, 2) & leading) == leading:
            flags.append(leading)
    if len(flags) == 0:
        return 'A'
    return classful_dict[max(flags)]


def bin2binlist(binstr):
    raw_list = []
    result_list = []
    for x in list(binstr):
        if len(raw_list) != 7:
            raw_list.append(x)
        else:
            raw_list.append(x)
            result_list.append(''.join(raw_list))
            raw_list = []
    return result_list


def subnetting(ip, subnet_amount):
    default_netbits_dict = {
        'A': 8,
        'B': 16,
        'C': 24,
    }

    c = ip2class(ip)
    if c not in default_netbits_dict.keys():
        print("\nWarning, Class %s not allowed subnetting.\n" % c)
        # help_info()
    default_cidr = 23
    default_network_address = ip2network_address(ip, default_cidr)[2]
    default_network_address_bin_list = ip2binlist(default_network_address)
    default_network_address_bin_str = ''.join(default_network_address_bin_list)
    # print default_network_address_bin_str
    # print bin2binlist(default_network_address_bin_str)
    int2binlist = lambda i: [bin(x).split('0b')[1].zfill(i) for x in range(2 ** i)]

    if subnet_amount:
        subnet_amount = int(subnet_amount)
        network_address_list = []
        subnet_bits = min([subnet_bits for subnet_bits in range(32) if 2 ** subnet_bits >= subnet_amount])
        cidr = subnet_bits + default_cidr
        avail_host_amount = ip2network_address(ip, cidr)[0]
        if subnet_bits > 0:
            flag = 'subnet'
            sub_binlist = int2binlist(subnet_bits)
            for subbinstr in sub_binlist:
                fullbinstr = ''.join(
                    [list(default_network_address_bin_str)[x] for x in range(default_cidr)]) + subbinstr + '0' * (
                                         32 - cidr)
                # print fullbinstr
                binlist = bin2binlist(fullbinstr)
                # print binlist
                network_address_list.append(binlist2ip(binlist))
        else:
            flag = 'supernet'
            subnet_amount = 1
            network_address = ip2network_address(ip, cidr)[2]
            network_address_list.append(network_address)
        return cidr, c, flag, len(network_address_list), network_address_list, avail_host_amount

def main():
    while True:
        try:
            ip_address = input("Enter IP Address: ")
            cidr_subnet_mask = input("Enter CIDR: ")
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

    print("Please enter subnets, an empty line will end input procedure")
    subnets_num = 0
    subnets_name = []
    number_of_hosts = []
    while True:
        subnet_name = input("Subnet Name: ")
        if subnet_name:
            subnets_name.append(subnet_name)
            num_hosts = int(input("Number of Hosts: "))
            number_of_hosts.append(num_hosts)
            subnets_num += 1
        else:
            if len(subnets_name) != 0:
                break
            else:
                subnets_num = 2
                break

    cidr, c, flag, subnet_amount, network_address_list, avail_host_amount = subnetting(ip_address, subnets_num)
    print("Subnet Name".ljust(20) + "Used Hosts".ljust(20) + "Available Hosts".ljust(20) + 'Network'.ljust(20) +
          "Broadcast".ljust(20) + "Prefix".ljust(20))

    if len(network_address_list) >= subnets_num:
        for i in range(subnets_num):
            ip = network_address_list[i]
            a,b,c,d,e,broadcast = ip2network_address(ip,cidr)
            if len(number_of_hosts) != 0 and avail_host_amount != 0:
                if avail_host_amount >= number_of_hosts[i]:
                    used_hosts = number_of_hosts[i]
                    print(subnets_name[i].ljust(20) + str(used_hosts).ljust(20) + str(avail_host_amount).ljust(20)
                          + str(network_address_list[i]).ljust(20) + str(broadcast).ljust(20) + str(cidr).ljust(20))
                elif avail_host_amount < number_of_hosts[i]:
                    used_hosts = avail_host_amount
                    print(subnets_name[i].ljust(20) + str(used_hosts).ljust(20) + str(avail_host_amount).ljust(20)
                          + str(network_address_list[i]).ljust(20) + str(broadcast).ljust(20) + str(cidr).ljust(20))
    elif len(network_address_list)<subnets_num:
        for i in range(network_address_list):
            ip = network_address_list[i]
            a, b, c, d, e, broadcast = ip2network_address(ip, cidr)
            if len(number_of_hosts) != 0 and avail_host_amount != 0:
                if avail_host_amount >= number_of_hosts[i]:
                    used_hosts = number_of_hosts[i]
                    print(subnets_name[i].ljust(20)+str(used_hosts).ljust(20)+str(avail_host_amount).ljust(20)
                          +str(network_address_list[i]).ljust(20)+str(broadcast).ljust(20)+str(cidr).ljust(20))
                elif avail_host_amount < number_of_hosts[i]:
                    used_hosts = avail_host_amount
                    print(subnets_name[i].ljust(20) + str(used_hosts).ljust(20) + str(avail_host_amount).ljust(20)
                          + str(network_address_list[i]).ljust(20) + str(broadcast).ljust(20) + str(cidr).ljust(20))


main()
