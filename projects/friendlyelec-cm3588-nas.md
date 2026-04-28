---
title: FriendlyElec CM3588 NAS
year: 2024
subtitle: SSD home nas based on RK3588
image: home_nas/header.jpg
---

I wanted to build a small, quiet NAS for my family that could handle file storage as well as media serving for an *arr stack.
After some research, I settled on the FriendlyElec CM3588 NAS Kit with a CM3588 core module, 16GB of RAM, and 64GB of on-board eMMC storage.
It covered all the use cases I had in mind.
The platform provides four M.2 NVMe bays which, unlike hard drives, keep the system silent and comparatively power-efficient, along with enough memory and on-board storage for OpenMediaVault and a CPU capable of handling transcoding.
For storage, I chose three Lexar NM620 2TB M.2 PCIe Gen3x4 NVMe SSDs in RAID 5.
That gives the system enough capacity at the maximum speed supported by the kit, while still leaving one bay free for a future upgrade.

![Package received](home_nas/01.jpg)

I ordered the kit from China, and it arrived with the expected accessories and power supply.

![Case](home_nas/02.jpg) | ![Test fit 1](home_nas/03.jpg) | ![Test fit 2](home_nas/04.jpg)

For the enclosure, I found this very nice [design](https://www.printables.com/model/857903-friendlyelec-cm3588-nas-case-desktop-standalone) by Fuzzler and printed it first in PETG.
That turned out to be the wrong choice.
Some of the buttons eventually snapped because the material was too stiff, and in practice the board never reaches temperatures that would make PLA unsuitable.
Even so, the first print was good enough for a test fit and confirmed that the model was the right solution for the build.

![SSDs](home_nas/05.jpg) | ![Installed storage](home_nas/06.jpg)

Once the Lexar SSDs arrived, I mounted them and installed OpenMediaVault.
From there I set up the basic users, permissions, and shared folders.
I then moved over my personal *arr stack Docker Compose setup and adapted it to this system.
That also meant configuring video device passthrough for the containers and verifying that hardware acceleration was working correctly.

![New case 1](home_nas/07.jpg) | ![New case 2](home_nas/08.jpg)

As mentioned above, some of the PETG buttons snapped while I was working with the case.
The original print also had a few minor imperfections caused by warping and shrinkage, so I decided to reprint the entire enclosure in PLA.

![CPU fan](home_nas/09.jpg) | ![ZH1.5 connectors](home_nas/10.jpg) | ![ZH detail](home_nas/11.jpg)

While setting up the NAS, I noticed that temperatures were generally under control, but summers in Italy can be unforgiving.
The board includes a 5V ZH1.5 connector specifically for a CPU fan, and the CM3588 core module has mounting holes for a 40mm fan.
I bought a 40mm 5V 4010 hydraulic-bearing fan and replaced its PH connector with a ZH one.
In hindsight, this was not the best choice.
The fan produces a droning, scratchy noise, and in this build there is no real advantage to using such a low-profile model.
At some point I will probably redesign the top cover to accommodate a taller Noctua fan, which should solve the problem completely.
Even so, the current fan only starts above 50°C and keeps the device below 55°C in practice.
Unless you are sitting very close to it, the noise is not especially noticeable from a few meters away.

![Final fit](home_nas/12.jpg) | ![Closed lid](home_nas/13.jpg) | ![Packed for the trip](home_nas/14.jpg)

After final assembly and testing, I packed the NAS securely and brought it to my family during the summer holidays.

![Final location 1](home_nas/15.jpg) | ![Final location 2](home_nas/16.jpg) | ![Final location 3](home_nas/17.jpg)

It reached its final destination next to the modem and has been working flawlessly ever since.
I still connect remotely from time to time for maintenance and supervised updates, but overall it has been almost completely hands-off.

The RK3588 has turned out to be a surprisingly capable platform.
Transcoding has never run into any obvious bottlenecks, and the various services have behaved without any performance-related issues.
The NAS is also fairly inconspicuous and does not consume much power, so it stays on all the time.
At the moment I do not expect to populate the fourth SSD bay, but the option is still there if storage needs to increase.
I will definitely replace the fan at some point, though, since my workstation in Italy sits right next to it and the intermittent noise is more annoying than I would like.
Overall, this was a very rewarding project and a good exercise in Docker-based service interoperability.
