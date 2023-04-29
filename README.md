# netcalc

**Netcalc** is a library that allows you to work with net calculations in a simple way.

```python
>>> from netcalc import subnet
>>> sub = subnet.Ipv4('10.0.4.1', 10)
>>> sub.check()
('10.0.4.1', 10)
>>> sub.bin()
'00001010.00000000.00000100.00000001'
>>> sub.hex()
'a.0.4.1'
>>> sub.calc()
{'ip': '10.0.4.1/10', 'broadcast': 
'10.63.255.255', 'class': 'B', 
'net_address': '10.0.0.0', 'range': ('10.0.0.0', '10.63.255.255'), 
'usable_range': ('10.0.0.1', '10.63.255.254'), 
'wildcard_mask': '0.63.255.255', 'subnet_mask': '255.192.0.0'}
```

**netcalc** allows you to work with net calculations in an extremely simple and efficient way. No complicated names and no difficult to understand methods. **netcalc** also supports Ipv6:

```python
>>> from netcalc import subnet
>>> sub = subnet.Ipv6('2001:db8:85a3::8a2e:370:7334', 37)
>>> sub.check()
('2001:db8:85a3:0000:0000:8a2e:370:7334', 37)
>>> sub.bin()
'0010000000000001:0000110110111000:1000010110100011:0000000000000000:0000000000000000:1000101000101110:0000001101110000:0111001100110100'
>>> sub.calc()
{'ip': '2001:db8:85a3:0000:0000:8a2e:370:7334/37', 
'net_address': '2001:db8:8000:0000:0000:0000:0000:0000', 
'range': ('2001:db8:8000:0000:0000:0000:0000:0000', '2001:db8:87ff:ffff:ffff:ffff:ffff:ffff'),
'wildcard_mask': '0000:0000:7ff:ffff:ffff:ffff:ffff:ffff', 
'subnet_mask': 'ffff:ffff:f800:0000:0000:0000:0000:0000'}
```
What else do you need to start using **netcalc**?
