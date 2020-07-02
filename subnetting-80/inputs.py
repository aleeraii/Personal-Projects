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
        try:
            subnet_name = input("Subnet Name: ")
            if subnet_name:

                num_hosts = int(input("Number of Hosts: "))
                number_of_hosts.append(num_hosts)
                subnets_name.append(subnet_name)
                subnets_num += 1
            else:
                if len(subnets_name) != 0:
                    break
                else:
                    subnets_num = 2
                    break
        except ValueError:
            print("Kindly Enter valid number of hosts")


main()
