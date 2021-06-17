# Canon LBP 2900

Installation on Fedora Linux (tested on Fedora 34).

https://www.abclinuxu.cz/hardware/vystupni-zarizeni/tiskarny/canon/lbp2900

1. Download driver: https://www.canon.cz/support/consumer_products/products/printers/laser/i-sensys_lbp2900.html?type=drivers&language=&os=linux

2. Unpack, then run:

```
cd ~/Downloads/linux-capt-drv-v271-uken/64-bit_Driver/RPM
sudo dnf install -y ./cndrvcups-capt-2.71-1.x86_64.rpm ./cndrvcups-common-3.21-1.x86_64.rpm 
```

3. Run:

```
sudo systemctl restart cups
```

4. Turn on printer, detect:

```
$ dmesg
...
[91556.850829] usb 1-6.3: new high-speed USB device number 11 using xhci_hcd
[91557.002216] usb 1-6.3: New USB device found, idVendor=04a9, idProduct=2676, bcdDevice= 1.00
[91557.002238] usb 1-6.3: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[91557.002247] usb 1-6.3: Product: Canon CAPT USB Device
[91557.002254] usb 1-6.3: Manufacturer: Canon
[91557.002259] usb 1-6.3: SerialNumber: 0000B17BDED9
[91557.094339] usblp 1-6.3:1.0: usblp0: USB Bidirectional printer dev 11 if 0 alt 0 proto 2 vid 0x04A9 pid 0x2676
[91557.094394] usbcore: registered new interface driver usblp
[91562.304523] usblp0: removed
[91562.309938] usblp 1-6.3:1.0: usblp0: USB Bidirectional printer dev 11 if 0 alt 0 proto 2 vid 0x04A9 pid 0x2676
```

5. Check that the file exists:

```
/dev/usb/lp0
```

6. Unpack source to get PPD file:
   
```
cd ~/Downloads/linux-capt-drv-v271-uken/Src/
tar xzvf ./cndrvcups-capt-2.71-1.tar.gz
cd cndrvcups-capt-2.71/ppd
```

7. Create spooler

```
$ sudo lpadmin -p LBP2900 -m ./CNCUPSLBP2900CAPTK.ppd -v ccp:/var/ccpd/fifo0 -E
lpadmin: Printer drivers are deprecated and will stop working in a future version of CUPS.
```

8. Connect spooler to USB port of the printer

```
$ sudo ccpdadmin -p LBP2900 -o /dev/usb/lp0

 CUPS_ConfigPath = /etc/cups/
 LOG Path        = None
 UI Port         = 59787

 Entry Num  : Spooler	: Backend	: FIFO path		: Device Path 	: Status 
 ----------------------------------------------------------------------------
     [0]    : LBP2900 	:  		:                 	: /dev/usb/lp0 	: New!!

```

9. Run control daemon

```
$ sudo /etc/init.d/ccpd start

Reloading systemd:                                         [  OK  ]
Starting ccpd (via systemctl):                             [  OK  ]
```

10. After restart, only the step 9 should be performed