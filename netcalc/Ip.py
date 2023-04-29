from util import convert
from const import *

class Ipv4Exception(Exception):
    def __init__(self, IP, message=None):
        if message:
            self.message = message
        else:
            self.message = "The value '{}' is not an valid ipv4 address".format(IP)

        super().__init__(self.message)

class Ipv6Exception(Exception):
    def __init__(self, IP, message=None):
        if message:
            self.message = message
        else:
            self.message = "The value '{}' is not an valid ipv6 address!".format(IP)

        super().__init__(self.message)

class Ipv4:
    """
    Representation of an IPv4 address

    :param IP: IPv4 address in decimal form. Example: '10.0.4.1'.
    :param check: Does the address passed to IP need to be checked when the class is built?
    """

    sep = '.'
    type = 'ipv4'
    bits = IPV4_BIT_COUNT
    octs = IPV4_OCT_COUNT
    thosts = 2 ** (IPV4_OCT_COUNT * IPV4_BIT_COUNT)
    EMPTY = EMPTY_IP

    def __init__(self, IP = None, check = False, empty = False):
        self._IP = IP

        if check:
            self._IP = self.ip_check()

        if empty:
            self._IP = self.EMPTY

    def __len__(self):
        IP_split = self.IP.split(self.sep)

        for i in range(0, IP_split.count('')):
            IP_split.remove('')

        return len(IP_split)

    def __eq__(self, IP):
        try:
            if self.type == IP.type:
                return True

            return False
        except Exception:
            return False

    def __get_IP(self, ip: str = None) -> str:
        if ip:
            return ip

        if self._IP:
            return self._IP

        raise ValueError('The value for IP could not be None!')

    def __get_IP(self) -> str:
        if self.IP:
            return self.IP

        raise ValueError('The value for IP could not be None!')

    @property
    def IP(self) -> str:
        return self._IP

    @IP.setter
    def IP(self, new_ip: str):
        self._IP = new_ip

    def ip_check(self) -> str:
        """
        Checks if the passed Ipv4 address is valid
        """
        IP = self.IP

        if (IP.count('.') != 3) or ('' in IP.split(self.sep)):
            raise Ipv4Exception(IP)

        IP_splited = IP.split(self.sep)
        for octet in IP_splited:
            try:
                if (int(octet) < MIN_IPV4_OCTET) or (int(octet) > MAX_IPV4_OCTET):
                    raise Ipv4Exception(IP)

            except Exception:
                raise Ipv4Exception(IP)

        return IP

    def bin(self) -> str:
        """
        Convert IPv4 address to binary format. The result will be, as in the 
        representation of the type passed, separated by ".".
        """
        IP = self.__get_IP()

        IP_splited = self.ip_check().split(self.sep)
        IP_bin = []

        for octet in IP_splited:
            IP_bin.append(convert.db(octet, IPV4_BIT_COUNT))

        return self.sep.join(IP_bin)

    def hex(self) -> str:
        """
        Convert IPv4 address to binary format. The result will be, as in the 
        representation of the type passed, separated by ".".
        """
        IP = self.__get_IP()

        IP_splited = self.ip_check().split(self.sep)
        IP_bin = []

        for octet in IP_splited:
            IP_bin.append(convert.dh(octet))

        return self.sep.join(IP_bin)

    def empty(self) -> bool:
        if self.IP == self.EMPTY:
            return True

        return False
    
class Ipv6:
    """
    Representation of an IPv6 address

    :param IP: IPv6 address in decimal form. Example: '2001:db8:85a3::8a2e:370:7334'.
    :param check: Does the address passed to IP need to be checked when the class is built?
    """
    
    sep = ':'
    type = 'ipv6'
    bits = IPV6_BIT_COUNT
    octs = IPV6_OCT_COUNT
    thosts = 2 ** (IPV6_OCT_COUNT * IPV6_BIT_COUNT)
    EMPTY = EMPTY_IP

    def __init__(self, IP = None,  check = False, empty = False):
        self._IP = IP
        self.IP = IP

        if check:
            self.IP = self.ip_check()

        if empty:
            self._IP = EMPTY

    def __iter__(self):
        IP_split = self.IP.split(self.sep)

        for i in range(0, IP_split.count('')):
            IP_split.remove('')

        return iter(IP_split) 

    def __len__(self):
        IP_split = self.IP.split(self.sep)

        for i in range(0, IP_split.count('')):
            IP_split.remove('')

        return len(IP_split)

    def __eq__(self, IP):
        try:
            if self.type == IP.type:
                return True

            return False
        except Exception:
            return False

    def __get_IP(self) -> str:
        if self.IP:
            return self.IP

        raise ValueError('The value for IP could not be None!')      

    @property
    def IP(self) -> str:
        return self._IP

    @IP.setter
    def IP(self, new_ip: str):
        while (new_ip.count(':0:')):
            new_ip = new_ip.replace(':0:', ':0000:')

        if new_ip.startswith('0:'):
            new_ip = '000' + new_ip

        if new_ip.endswith(':0'):
            new_ip = new_ip + '000'

        if '::' in new_ip:
            r = self.octs - len(self)
            new_ip = new_ip.replace('::', ':0000:' * r).replace('::', ':')

            if new_ip.startswith(':'):
                new_ip = new_ipP[1:]
            
            elif new_ip.endswith(':'):
                new_ip = new_ip[0:len(new_ip) - 1]

        self._IP = new_ip

    def ip_check(self) -> str:
        """
        Checks if the passed Ipv6 address is valid. Note that 
        this method can be called without the class having been constructed.
        """
        IP = self.__get_IP()
        
        #IP = IP.replace('::', ':0000:')

        if (IP.count(':') != 7) or ('' in IP.split(self.sep)):
            raise Ipv6Exception(IP)

        IP_splited = IP.split(self.sep)
        for octet in IP_splited:
            try:
                octet_decimal = convert.hd(octet)

                if ((octet_decimal < MIN_IPV6_OCTET) or (octet_decimal > MAX_IPV6_OCTET)):
                    raise Ipv6Exception(IP)

            except Exception:
                raise Ipv6Exception(IP)

        return self.sep.join(IP_splited)

    def bin(self) -> str:
        """
        Convert IPv4 address to binary format. The result will be, as in the 
        representation of the type passed, separated by ":".
        """        
        IP = self.__get_IP()
        IP_splited = self.ip_check().split(self.sep)
        IP_bin = []

        for octet in IP_splited:
            IP_bin.append(convert.hb(octet, IPV6_BIT_COUNT))

        return self.sep.join(IP_bin) 

    def hex(self):
        """
        Convert IPv4 address to hex format. The result will be, as in the 
        representation of the type passed, separated by ".".
        """
        IP = self.__get_IP(IP)

        IP_splited = self.ip_check().split(self.sep)
        IP_bin = []

        for octet in IP_splited:
            IP_bin.append(convert.dh(octet))

        return self.sep.join(IP_bin)

    def empty(self) -> bool:
        if self.IP == self.EMPTY:
            return True

        return False

def is_ipv4(IP: str) -> bool:
    try:
        Ipv4(IP, True)
        return True
    except Exception:
        return False

def is_ipv6(IP: str) -> bool:
    try:
        Ipv6(IP, True)
        return True
    except Exception:
        return False

def Ip(IP: Ipv4 | Ipv6 | str) -> Ipv4 | Ipv6 | str:
    if not isinstance(IP, str):
        return IP

    if is_ipv4(IP):
        return Ipv4(IP, True)

    return Ipv6(IP, True)

def is_ipv4_ipv6(IP: any) -> bool:
    if (IP == Ipv4) or (IP == Ipv6):
        return True

    return False
