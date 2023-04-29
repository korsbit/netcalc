from nettypes import *
import calc
import Ip

class Ipv4(Ip.Ipv4):
    def __init__(self, IP:  GenericIpType, mask: IPType):
        super().__init__(IP)
        self.mask = mask

        self.check()

    def net_address(self):
        return calc.net_address(self.IP, self.mask)

    def usable_range(self):
        return calc.ip_usable_range(self.IP, self.mask)

    def range(self):
        return calc.ip_range(self.IP, self.mask)

    def ipclass(self):
        return calc.ip_class(self.mask)

    def submask(self):
        return calc.subnet_mask(self.mask, Ip.Ipv4)

    def wildmask(self):
        return calc.wildcard_mask(self.mask, Ip.Ipv4)

    def broadcast(self):
        return calc.broadcast(self.IP, self.mask)

    def check(self):
        mask_result = calc.ipv4_mask(self.mask)
        IP_result = self.ip_check()

        return (IP_result, mask_result)

    def calc(self):
        return calc.calc(self.IP, self.mask)

class Ipv6(Ip.Ipv6):
    def __init__(self, IP:  GenericIpType, mask: IPType):
        super().__init__(IP)
        self.mask = mask

        self.check()

    def net_address(self):
        return calc.net_address(self.IP, self.mask)

    def range(self):
        return calc.ip_range(self.IP, self.mask)

    def submask(self):
        return calc.subnet_mask(self.mask, Ip.Ipv6)

    def wildmask(self):
        return calc.wildcard_mask(self.mask, Ip.Ipv6)

    def check(self):
        mask_result = calc.ipv6_mask(self.mask)
        IP_result = self.ip_check()

        return (IP_result, mask_result)

    def calc(self):
        return calc.calc(self.IP, self.mask)
