---
title: MeshCore BRICK.EXE
year: 2025
subtitle: MeshCore radio with large battery
image: mesh_radio/header.jpg
---

I had been following Meshtastic for some time and had already tested it with friends, but its limits in range and reachability pushed me to look for alternatives.
That led me to MeshCore and, eventually, to building a dedicated device around the RAKwireless WisBlock platform.
The hardware is based on the RAK19007 WisBlock Base Board with a RAK4631 WisBlock Core, which combines a very low-power Nordic nRF52840 MCU with a Semtech SX1262 LoRa transceiver.
I paired it with the RAK12500 GNSS module and the RAK1921 OLED display.
The last step was finding a suitable enclosure, and I eventually settled on this versatile [case model](https://www.printables.com/model/286657-rak19007rak5005-case-for-meshtastic) by TonyG.

![Front](mesh_radio/01.jpg) | ![Back](mesh_radio/02.jpg)

I chose the ribbed version of the case, with the opening for the display.
It also includes a side push button, which works as the user button for navigating the menu.

![Sourcing glass](mesh_radio/03.jpg) | ![Fitting glass](mesh_radio/04.jpg) | ![Fitting glass](mesh_radio/05.jpg) | ![Front view](mesh_radio/06.jpg)

This version of the case needed a protective cover for the display.
Since I did not have any thin acrylic or hobby glass on hand, I cut a small rectangle from an old transparent plastic case with a rotary tool.
I then cleaned up the edges with very fine sandpaper and adjusted the size until it fit tightly into the opening.

![Display front](mesh_radio/07.jpg) | ![Display back](mesh_radio/08.jpg) | ![Display mounted](mesh_radio/09.jpg) | ![Display ON](mesh_radio/10.jpg) | ![Display test](mesh_radio/vid-test-display.mp4)

With the screen cover sorted out, I moved on to soldering the display and the user button, then mounting the assembly into the case with the supplied screws.

![Batteries](mesh_radio/11.jpg) | ![Battery holders](mesh_radio/12.jpg) | ![Unsuitable back cover](mesh_radio/13.jpg) | ![Large back cover](mesh_radio/14.jpg)

I explored several options for the battery system.
I bought both 21700 and 18650 lithium cells and tested a few different configurations.
In the end, I went with two 21700 cells in parallel for their much higher capacity.
That decision required a larger back cover, which I improvised rather clumsily for this first version.
I plan to revisit that part of the design once I have enough CAD experience to model a cleaner and more deliberate replacement.

![Before final assembly](mesh_radio/15.jpg) | ![Complete assembly](mesh_radio/16.jpg)

Once everything was assembled, the radio was ready.
Even with GPS enabled, the runtime is over 20 days.

This was a very satisfying project to put together.
The case design is clever and reflects the modular nature of the WisBlock system well.
One of the main advantages of the build is that the battery can be swapped for different form factors and capacities by simply removing the back cover and disconnecting the link between the board and the pack.
As mentioned above, the current back cover is still the weakest part of the build, since it was made with the single goal of accommodating the larger battery.
I would also like to build slimmer and more portable variants around 18650 cells in case I decide to use the radio away from home.
Thanks to local MeshCore repeaters, I have already been able to receive messages from users in cities some distance away.
I am very curious to keep testing the radio’s capabilities and to follow MeshCore as the project continues to develop quickly.
