# 0.6-beta
- Location name corrections
- More Logic Fixes:
  - Bovina's Jiggy now requires Airborne Egg Aiming
  - Dippy's Pool is now in the CCL region
  - Note Logic now correctly expects either method of reaching Plateau
  - Oogle Boogle Jiggy now requires Bill Drill and Grip Grab
  - Lord Woo Fak Fak now expects Mumbo if fighting him without Sub
  - Removed Egg Aim from requirements for Cave of Horrors
  - Added Egg Aim and Grenade Eggs to requirements for Mr. Patch
  - Witchyworld Train Station now allows Leg Spring
  - Grunty Industries 3rd Floor Honeycomb now allows Solo Kazooie
  - Split Up is now required for The Inferno Jiggy
  - Money Van is now required for Saucer of Peril to access Mumbo's Skull
- Implemented generic Jiggy item
- Bugfixes:
  - Async items are now received properly
  - Hints no longer send checks
  - Saving and Quitting while touching a jiggy no longer sends false checks

# 0.5.1-beta
- Fixed logic errors:
  - Pig Pool now requires access to HFP and CCL
  - JRL Doubloons hard require Split Up
  - Power Hut Basement now requires Split Up or Fire (Fire Eggs, Dragon Kazooie)
  - Note requirements for silos
  - Weldar now requires Bill Drill and Grenade Eggs
  - Stomping Plains: Both Jiggies added to TDL region, require Ice Eggs/Springy Step Boots
  - More places where explosives are needed allow Clockwork Eggs
  - Snowball is now needed to press Ice Train Station switch
  - Hailfire Peaks Kickball Stadium walls can be broken with Mumbo's wand
  - Smuggler's Cavern now requires explosives
  - Forbid items on Jinjo Families that are required to collect Jinjos
- Fast swimming is now fixed
- Received moves are now usable when obtained
- Updated item and location names to make reading spoiler logs easier

# 0.5-beta
- Implemented Cheato Pages
- Implemented Glowbos
- Skip most cutscenes and one-time dialogues
- Fixed some typos
- Fixed bug where lua script would crash randomly
- Implemented Banjo Advanced Jamjar Moves
- Implemented detailed logics for Archipelago randomization

# v0.4-beta
- Fixed issue when unchecked locations are sent when saving and quiting.

# v0.3-alpha
- Implemented Empty Honeycombs
- Jiggywiggy Temple Fixes after completing the second puzzle
- Fixed issue for checking totals in Jiggywiggy Temple
- Fixed Typo for Mayahem Temple
- change MasterMap dictionary/map (Development)
- Fix Typo for Jolly Rogers Lagoon
- Fix Typo for Doubloons (for future implementation)
- Skip First Jinjo Cutscene
- Handle both true and false values for Honeycombs
- Tower of Terror is now skippable in YAML options

# v0.2-alpha
- Implemented Victory Condition
- Implemented Slot data in BTclient and Lua
- Fixed issue for uploading the generated world on archipelago website