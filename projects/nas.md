---
title: NAS Build
year: 2026
order: 1
subtitle: Personal NAS with 3D printed case
image: nas/header.jpg
---

While browsing Printables I came across this elegant [NAS design](https://www.printables.com/model/837218-nas-case-6-bay-3-ssd) by makerunit.
It finally pushed me to build the NAS I had been postponing for a long time: a compact system for backing up my server and desktop, assembled almost entirely from scratch.

After some planning I settled on a motherboard with an integrated Intel N150 CPU, a SilverStone SX500 power supply, 32 GB of Corsair DDR5 SO-DIMM memory, and six 4 TB Seagate IronWolf hard drives.

![Drive bay and panels](nas/01.jpg) | ![All the pieces](nas/02.jpg) | ![Panel logo](nas/03.jpg)

Printing was by far the most time-consuming part of the build.
The design relies on exposed honeycomb infill, with no top or bottom layers, which made the print times especially long.
In the end it took about two weeks to print everything.
I chose PETG for its better thermal resistance.

![Soldering iron tip](nas/04.jpg) | ![Drive bay inserts](nas/05.jpg) | ![Other insert](nas/06.jpg)

The case uses brass threaded inserts, which I was using for the first time.
With the dedicated soldering iron tip, the process turned out to be surprisingly straightforward.

![Drive bay](nas/07.jpg) | ![Fans](nas/08.jpg) | ![Front view](nas/09.jpg) | ![Fans running](nas/vid-fans.mp4)

At this stage the drive bay was fully assembled, with two 92mm PWM fans mounted for cooling.

![Testing the motherboard](nas/10.jpg) | ![Button](nas/11.jpg) | ![Install mockup](nas/12.jpg) | ![Motherboard test](nas/vid-motherboard.mp4)

Before installation, I tested the motherboard together with its 12mm power button to make sure everything worked as expected.

![Empty assembly](nas/13.jpg) | ![Drive bay inserted](nas/14.jpg) | ![Bottom panel](nas/15.jpg) | ![Front view](nas/16.jpg) | ![Back view](nas/17.jpg)

This was the completed assembly.
The drive bay slides into sleds that give rigidity to the overall structure.
The trickiest part was routing the SATA cables: tolerances were tight, but in the end everything fit properly.

The project took shape over several months, between planning, budgeting, printing, and finding time for assembly.
Some of the printed parts warped or shrank slightly, leaving small imperfections that mostly reflect the limits of my printer.
Even so, I am very satisfied with the result.
The six bays leave plenty of room for different storage configurations, and the low-power hardware suits the intended use well, since this system is mainly meant for cold storage and only gets powered on when needed.
