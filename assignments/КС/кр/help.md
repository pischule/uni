# Контрольная по КС

![image](https://user-images.githubusercontent.com/41614960/119050468-95a3bb80-b9ca-11eb-927e-358f4df9c5e7.png)

---


## router 1
```
enable
config t

interface FastEthernet 0/0
ip address 200.200.1.1 255.255.255.0
no shutdown

interface serial 0/0
ip address 200.200.4.1 255.255.255.0
clock rate 64000
no shutdown

interface serial 0/1
ip address 200.200.5.1 255.255.255.0
clock rate 64000
no shutdown

router rip
version 2
network 200.200.1.0
network 200.200.4.0
network 200.200.5.0

exit

do wr
```

---

## pc1

property|value
--|--
**ip** |      200.200.1.2
**netmask** | 255.255.255.0
**gateway** | 200.200.1.1

---

## router 2

```
enable
config t

interface FastEthernet 0/0
ip address 200.200.2.1 255.255.255.0
no shutdown

interface serial 0/0
ip address 200.200.4.2 255.255.255.0
clock rate 64000
no shutdown

interface serial 0/1
ip address 200.200.6.1 255.255.255.0
clock rate 64000
no shutdown

router rip
version 2
network 200.200.2.0
network 200.200.4.0
network 200.200.6.0

exit
do wr
```

---

## pc2

property|value
--|--
**ip** |      200.200.2.2
**mask** |    255.255.255.0
**gateway** | 200.200.2.1

---

## router 3


```
enable
config t

interface FastEthernet 0/0
ip address 200.200.3.1 255.255.255.0
no shutdown

interface serial 0/0
ip address 200.200.5.2 255.255.255.0
clock rate 64000
no shutdown

interface serial 0/1
ip address 200.200.6.2 255.255.255.0
clock rate 64000
no shutdown

router rip
version 2
network 10.0.0.0
network 200.200.3.0
network 200.200.5.0
network 200.200.6.0

exit
do wr
```

---

## server

```
desktop -> ip
```

property|value
--|--
**ip** |      200.200.3.2
**mask** |    255.255.255.0
**gateway** | 200.200.3.1

```
services -> dhcp
```

property|value
--|--
**service** |        on
**gateway** |        200.200.3.1
**start ip** |       200.200.3.3
**mask** |           255.255.255.0
**number of users** | 5

save

---

## pc3

```
desktop -> ip -> dhcp
```

---

## pc4

```
desktop -> ip -> dhcp
```

