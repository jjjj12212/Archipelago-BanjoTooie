
# SETUP GUIDE FOR BANJO-TOOIE ARCHIPELAGO

## Important

As we are using BizHawk, this guide is only applicable to Windows and Linux systems.

## Required Software/Files

-   BizHawk:  [BizHawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
    -   Version 2.9.1 and later are supported.
    -   Detailed installation instructions for BizHawk can be found at the above link.
    -   Windows users must run the prereq installer first, which can also be found at the above link.
-   Grab the latest release from https://github.com/jjjj12212/Archipelago-BanjoTooie
-   A Banjo-Tooie ROM (USA ONLY).

## Configuring BizHawk

Once BizHawk has been installed, open EmuHawk and change the following settings:

-   Under Config > Customize, check the "Run in background" and "Accept background input" boxes. This will allow you to continue playing in the background, even if another window is selected.
-   Under Config > Hotkeys, many hotkeys are listed, with many bound to common keys on the keyboard. You will likely want to disable most of these, which you can do quickly using  `Esc`.
-   If playing with a controller, when you bind controls, disable "P1 A Up", "P1 A Down", "P1 A Left", and "P1 A Right" as these interfere with aiming if bound. Set directional input using the Analog tab instead.
-   Under N64 enable "Use Expansion Slot". (The N64 menu only appears after loading a ROM.)

It is strongly recommended to associate N64 rom extensions (*.n64, *.z64) to the EmuHawk we've just installed. To do so, we simply have to search any N64 rom we happened to own, right click and select "Open with…", unfold the list that appears and select the bottom option "Look for another application", then browse to the BizHawk folder and select EmuHawk.exe.

## How to Install - Server Side
- Copy banjo_tooie.apworld into the worlds folder in your existing Archipelago folder (\libs\worlds)

## How to install - Client Side

- Copy data/lua/banjo_tooie_connector.lua into data/lua in your existing Archipelago
- Run Launcher.exe and select Banjo-Tooie Client
- Connect the Archipelago Client with the server.
- Open Bizhawk (2.9.1+) and open your Banjo-Tooie (US) game.
- Once you are in the game select screen, apply the banjo_tooie_connector lua script (drag and drop)

### Connect to the Multiserver

Once both the client and the emulator have started, you must connect them together. Navigate to your Archipelago install folder, then to  `data/lua`, and drag+drop the  `banjo_tooie_connector`  script onto the main EmuHawk window. (You could instead open the Lua Console manually, click  `Script`  〉  `Open Script`, and navigate to  `banjo_tooie_connector`  with the file picker.)

To connect the client to the multiserver simply put  `<address>:<port>`  on the textfield on top and press `connect` (if the server uses password, then it will prompt after connection).
