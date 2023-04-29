from util import convert
from nettypes import *
from const import *

import math
import Ip

class MaskException(Exception):
    def __init__(self, mask, message=None):
        if message:
            self.message = message
        else:
            self.message = "The mask '{}' is not valid".format(mask)

        super().__init__(self.message)

def ipv4_mask(mask: MaskType) -> int:
    """
    Check the validity of an IPv4 type network mask.

    :param mask: Mask to check validity
    :return: will mask the passed network, if it is valid
    """
    if (mask < MIN_IPV4_OCTET) or (mask > MAX_IPV4_OCTET):
        raise MaskException(mask)

    return mask

def ipv6_mask(mask: MaskType) -> int:
    """
    Check the validity of an IPv6 type network mask.

    :param mask: Mask to check validity
    :return: will mask the passed network, if it is valid
    """    
    if (mask < MIN_IPV6_OCTET) or (mask > MAX_IPV6_OCTET):
        raise MaskException(mask)

    return mask

def mask_result(mask: MaskType, IP_type: str = Ip.Ipv4.type):
    if IP_type == Ip.Ipv4.type:
        return ipv4_mask(mask)
    if IP_type == Ip.Ipv6.type:
        return ipv6_mask(mask)

    raise MaskException(mask)

def IPCalc(IP_supported: [IPType]):
    """
    * Decorator used in functions that take an IP address 
    and a network mask number as arguments.

    * Performs the process of converting the IP address to 
    Ip.Ipv4 or Ip.Ipv6 if it is of type str. Furthermore, 
    the IP address will be checked only in case it is of type str.

    * In 'IP_supported' is the list of supported IP types for the 
    function, and if the IP address passed to the function does 
    not match any IP type in 'IP_supported' an error will be generated.

    * The validity of the mask will be checked, and if 
    it is not valid, an exception will occur.
    """

    def decorator(f):
        def wrapper(*args):
            IP = None
            mask = None

            try:
                IP = args[0]
            except IndexError:
                raise TypeError("{} missing required argument: IP".format(f.__name__))

            try:
                mask = args[1]
            except IndexError:
                raise TypeError("{} missing required argument: mask".format(f.__name__))

            IP_result = None
            if isinstance(IP, str):
                IP_result = Ip.Ip(IP)

            else:
                IP_result = IP
            
            if (not IP_result in IP_supported):
                raise ValueError("Type value passed as argument to IP is not supported!")

            return f(IP_result, mask_result(mask, IP_result.type.lower()), *args[2:])

        return wrapper

    return decorator

def IPCalcMask(IP_supported: [IPType]):
    """
    * Decorator used in functions that receive a mask number as an argument.

    * The function that uses this decorator can also receive a class of type 
    Ip.Ipv4 or Ip.Ipv6 as its second argument, and if it does not receive it, 
    the first argument of 'IP_supported' will be used to specify the type of 
    mask passed, or that is, whether it corresponds to an IPv4 or IPv6 address.

    * In 'IP_supported' is the list of supported IP types for the function, 
    and if the IP class passed to the function does not match any IP type 
    in 'IP_supported' an error will be generated.

    * The validity of the mask will be checked, and if it is not 
    valid, an exception will occur.
    """
    def decorator(f):
        def wrapper(*args):
            IP = None
            mask = None

            try:
                mask = args[0]
            except IndexError:
                raise TypeError("{} missing required argument: mask".format(f.__name__))

            try:
                IP = args[1]
                if (not IP in IP_supported):
                    raise ValueError("Type passed as argument to IP is not supported!") 
            except IndexError:
                pass

            if IP:
                mask = mask_result(mask, IP.type)
            else:
                mask = mask_result(mask, IP_supported[0].type)

            return f(mask, *args[1:])

        return wrapper

    return decorator

def IPCalcIp(IP_supported: [IPType]):
    """
    * Decorator used in functions that take an IP address as argument.

    * Performs the process of converting the IP address to 
    Ip.Ipv4 or Ip.Ipv6 if it is of type str. Furthermore, 
    the IP address will be checked only in case it is of type str.

    * In 'IP_supported' is the list of supported IP types for the 
    function, and if the IP address passed to the function does 
    not match any IP type in 'IP_supported' an error will be generated.

    * The validity of the mask will be checked, 
    and if it is not valid, an exception will occur.
    """
    def decorator(f):
        def wrapper(*args):
            IP = None

            try:
                IP = args[0]
            except IndexError:
                raise TypeError("{} missing required argument: IP".format(f.__name__))

            IP_result = None
            if isinstance(IP, str):
                IP_result = Ip.Ip(IP)

            else:
                IP_result = IP
            
            if (not IP in IP_supported):
                raise ValueError("Type passed as argument to IP is not supported!")

            return f(IP_result, *args[1:])

        return wrapper
    
    return decorator

def join_ip(IP_split: [str], IP_type) -> IPType:
    """
    It joins the binary parts of an IP address contained in a list and returns it.

    Ex:
       ip = join_ip(['00001010', '00000000', '00000100', '00000001'])
       ip == Ip.Ipv4('10.0.4.1')

    :param IP_split: List of binary parts of an IP
    """

    if IP_type == Ip.Ipv4.type:
        return Ip.Ipv4('.'.join([str(convert.bd(bin_oct)) for bin_oct in IP_split]))

    if IP_type == Ip.Ipv6.type:
        return Ip.Ipv6(':'.join([str(convert.bh(bin_oct)) for bin_oct in IP_split]))

@IPCalc([Ip.Ipv4, Ip.Ipv6])
def net_address(IP: GenericIpType, mask: MaskType) -> GenericIpType:
    """
    Calculates the network address based on a 
    reference IP and a reference mask.

    Ex:
        nad = net_address('10.0.4.1', 10)
    Ex:
        nad = net_address(Ip.Ipv4('10.0.4.1'), 10)

    :param IP (str, Ip.Ipv4, Ip.ipv6): Reference IP
    :param mask (int): Reference mask
    """
    IP_bin_split = IP.bin().split(IP.sep)
    mask = mask_result(mask, IP.type)

    net_split = [''] * IP.octs
    bit_count = 0

    for i, bin_oct in enumerate(IP_bin_split):
        for bit in bin_oct:
            if bit_count == mask:
                break

            net_split[i] += bit
            bit_count += 1

    net_split = list(map(lambda bin_oct: bin_oct + ('0' * (IP.bits - len(bin_oct))), net_split))
    
    return join_ip(net_split, IP.type)

@IPCalc([Ip.Ipv4, Ip.Ipv6])
def ip_usable_range(IP: GenericIpType, mask: MaskType) -> (GenericIpType, GenericIpType):
    """
    Calculates the range of usable addresses based on a 
    reference IP and a reference mask.

    :param IP (str, Ip.Ipv4, Ip.ipv6): Reference IP
    :param mask (int): Reference mask    
    """
    if mask >= (IP.octs * IP.bits) - 1:
        return (Ip.Ipv4(empty=True), Ip.Ipv4(empty=True))

    naddr_split = net_address(IP, mask).bin().split(IP.sep)

    first_ip = naddr_split
    first_ip[-1] = first_ip[-1][:-1] + '1'

    last_ip = [''] * IP.octs
    bit_count = 0

    for i, bin_oct in enumerate(naddr_split):
        for bit in bin_oct:
            if bit_count >= mask:
                last_ip[i] += '1'
            else:
                last_ip[i] += bit

            bit_count += 1

    last_ip[-1] = last_ip[-1][:-1] + '0'

    return (join_ip(first_ip, IP.type), join_ip(last_ip, IP.type))

@IPCalc([Ip.Ipv4, Ip.Ipv6])
def broadcast(IP: GenericIpType, mask: MaskType) -> IPType:
    """
    Calculates the broadcast address based on a reference 
    IP and a reference mask.

    :param IP (str, Ip.Ipv4, Ip.ipv6): Reference IP
    :param mask (int): Reference mask       
    """

    ip_usable_range_ = ip_usable_range(IP, mask)
    if ip_usable_range_[0].empty() or ip_usable_range_[1].empty():
        return IP

    last_ip_usable = ip_usable_range_[1].bin().split(IP.sep)

    broadcast = last_ip_usable
    broadcast[-1] = broadcast[-1][:-1] + '1'

    return join_ip(broadcast, IP.type)

@IPCalcMask([Ip.Ipv4, Ip.Ipv6])
def subnet_mask(mask: MaskType, IP: IPType = None) -> IPType:
    """
    Calculates the subnet mask based on a reference IP and a reference mask.

    :param IP (str, Ip.Ipv4, Ip.ipv6): Reference IP
    :param mask (int): Reference mask       
    """
    if not IP:
        raise TypeError("subnet_mask missing required argument: IP")
    
    subnet_mask_splited = [''] * IP.octs

    for i in range(0, IP.bits * IP.octs):
        j = math.ceil((i + 1) / IP.bits) - 1

        if i >= mask:
            subnet_mask_splited[j] += '0'
        else:
            subnet_mask_splited[j] += '1'

    return join_ip(subnet_mask_splited, IP.type)

@IPCalc([Ip.Ipv4, Ip.Ipv6])
def ip_range(IP: GenericIpType, mask: MaskType) -> (IPType, IPType):
    """
    Calculates the range of usable addresses based on a 
    reference IP and a reference mask.

    :param IP (str, Ip.Ipv4, Ip.ipv6): Reference IP
    :param mask (int): Reference mask_result
    """

    first = net_address(IP, mask)
    last = broadcast(IP, mask)

    return (first, last)

@IPCalcMask([Ip.Ipv4, Ip.Ipv6])
def wildcard_mask(mask: MaskType, IP: IPType = None) -> IPType:
    if not IP:
        raise TypeError("wildcard_mask missing required argument: IP")

    subnet_mask_ = subnet_mask(mask, IP).bin().split(IP.sep)
    wm_splited = [''] * IP.octs

    for i, bin_oct in enumerate(subnet_mask_):
        for bit in bin_oct:
            if bit == '1':
                wm_splited[i] += '0'
            else:
                wm_splited[i] += '1'

    return join_ip(wm_splited, IP.type)

@IPCalcMask([Ip.Ipv4])
def ip_class(mask: MaskType) -> str:
    if mask <= IPV4_CLASS_A_END:
        return "A"

    if mask <= IPV4_CLASS_B_END:
        return "B"

    if mask <= IPV4_CLASS_C_END:
        return "C"

@IPCalc([Ip.Ipv4, Ip.Ipv6])
def calc(IP: GenericIpType, mask: MaskType):
    result = {}
    result.update({ 'ip': '{}/{}'.format(IP.IP, mask) })

    if IP.type == Ip.Ipv4.type:
        result.update({ 'broadcast': broadcast(IP, mask).IP })
        result.update({ 'class': ip_class(mask) })
        result.update({ 'usable_range': tuple([ip.IP for ip in ip_usable_range(IP, mask)]) })
    
    result.update({ 'net_address': net_address(IP, mask).IP })
    result.update({ 'range': tuple([ip.IP for ip in ip_range(IP, mask)]) })
    result.update({ 'usable_range': tuple([ip.IP for ip in ip_usable_range(IP, mask)]) })
    result.update({ 'wildcard_mask': wildcard_mask(mask, IP).IP })
    result.update({ 'subnet_mask': subnet_mask(mask, IP).IP })

    return result
