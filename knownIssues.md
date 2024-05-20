# Known Issues
- Treble clef at JV will appear when you already collected it upon loading a save game OR disapear when you got it via AP.
    - Workaround: exit the map and come back in.
- WW train switch hit when exiting Chuffy
- Jinjo Menu not appearing after receiving a Jinjo
    - Workaround: Collect your first Jinjo check location
- CCL Notes count changes when close to Silo
    - visual bug only. The notes near Silo is close proximity to Silo, had to lower the range for checking notes in order to properly collect them.

- fighting HAG-1 sometimes doesn't trigger Goal

- Major Issue: Objects such as Jinjos and Notes respawns "randomly" and sometimes not send the check. Related to this, Jiggies also doesn't spawn.
    - This is an issue with the current framework. I speculate that it is related to the BMM / AMM / AGI tables not flipping the correct flags 
      or getting stuck somewhere.
    - Minor remedy: We should add the Jiggy spawn flags into the NON_AGI_MAP. Once you unpause, unset the flags for the jiggies that Hasn't spawn yet.
    - Minor remedy: Skip_Puzzle as a core feature. This will remove the "uniqueness" of Wooded Hollow and Jiggy Wiggy Temple.
    - Minor remedy: Split out Jinjos, Notes, and Jiggies into their own tables so they have their own functions. This may help as well.
