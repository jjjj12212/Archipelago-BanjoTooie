# 1.0.1-Beta
- Various logic bug fixes.
- Logic changes:
 - Beginner and normal logic only need Clockwork Eggs for superstash.
 - Intermediate logic doesn't need faster swimming, oxygenate or ice eggs to reach the Seemee Cheato page.
 - Advanced logic got (Pack Whack or Claw Clamber Boots) added to the Dragon Brothers logic to prevent softlocks.
 - Advanced logic can get the JRL trebleclef with the sub.
 

# 1.0-Beta
- Jinjos are now added to the pool
  - In-game, it will use a set pattern as its easier to control for logic / AP sending correct Jinjo colour
  - Pausing -> Jinjos will display your AP Jinjos, not in-game located Jinjos
  - minor issue: Jinjo Menu will not appear until you collected at least 1 Jinjo Check Location
- Added Experimental "fail-safe" (Thanks to Adeleine64DS for the suggestion)
  - Auto Flush Bizhawk Ram between loading zones. Should avoid hard crashes during gameplay and lose "a lot" of progress
- YAML Option name changes
  - multiworld_ to randomize_
- Doubloons near Wing Wack Silo will not have any Unlockable Silo Moves (bug fix for this silo) 
- Fix Levitation pad for Chuffy gone when Chuffy is not in the pool.
- Logic for Jinjos and Jinjo Family Jiggies
  - Jinjo Family Option to NOT allow Moves behind them
  - Jinjo Faimly Jiggies WILL NOT allow other Jinjos behind them
- Handle Multiple Logic behaviours based on YAML options
  - Beginner - Intended Banjo-Tooie strats
  - Normal - Same as previous versions
  - Advanced - Will require tricks

# 0.9.2-Beta
- Logic Change
  - GI: Guarded Jiggy now requires Split Up With Claw Climbers whereas before you only needed Claw Climbers
  - Hailfire Peak Honeycomb Logic
  - fix HAG 1 requirements
- fix King Coal defeated bug
- fix open level sanity check

# 0.9-Beta
- The Big Train Update!
  - Stations can now be randomized
  - Chuffy can now be an AP Item
    - Once obtained, you can summon Chuffy at a unlocked station, but you still need to beat Old King Coal to travel.
  - Beating Old King Coal is now an additional check
- Logic Changes
- Dpad Up: Banjo Tiptoes
- Dpad right: display unlocked moves in lua console
- Dpad down: display collected Treble Clefs
- Dpad left: aim assist (homing eggs)
- Text within Bizhawk on relevant items
- correct MT Glowbo location checks
- Fix for Puzzle Check dump.
- Skip Puzzles as an Option
- Hag 1 require 55 Jiggies Option

# 0.8.2-beta
- Swapped wrong Glowbos.  

# 0.8-beta
- Treble Clefs are added
- Rule Fixes
- Add Archipelago Documents
- Swap MT Glowbo locations when Glowbos are set to False
- Cheato Pages are set to Filler via YAML Option (Normal Items in BTClient)


# 0.7-beta
- Project name change to now be "Banjo-Tooie"
- world folder changed to banjo_tooie
- yaml change to "Banjo-Tooie"
- lua client name change
- doubloons
- Move doubloons slightly near JamJar's Silo (JRL)
  - Jamjar's "influence" has decreased to 300 due to Doubloons. (JRL)
- JRL Puzzle bugfix
- Fix bug where all moves are learnt when learning first move.
- Logic Changes:
 - doubloon requirement checks require 28 doubloons, gernade or clockwork eggs or Drill Bill 
 - change Note Logic
 - change requirements for JRL Pipe Honeycomb
 - change requirements for HFP lava side Honeycomb
 - change Superstash requirements
 - change Leg Spring requirements
 - Speed up minigames YAML option



# 0.6.2-beta
- Hotfix for lua client crashing
- Update logic for Generator Cavern
- Update YAML Template

# 0.6.1-beta
- Implement Starting Inventory
- Hotfix for receiving items

# 0.6-beta
- Location name corrections
- More Logic Fixes:
  - Bovina's Jiggy now requires Airborne Egg Aiming with flight
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
  - Kazooie no longer needs anything to cross Cauldron Keep's moat
  - Dippy's Pool Cheato Page now requires Springy-Step Shoes
  - Ancient Swimming Baths Cheato Page now allows Wing Whack
  - Added more clockwork logic
  - Fixed a lot of misc. WW, JRL, and HFP logic
  - Stealing food with Chuffy no longer in logic
  - More locations in GGM/WW now allow for solo Kazooie
- Implemented generic Jiggy item
- Bugfixes:
  - Async items are now received properly
  - Hints no longer send checks
  - Saving and Quitting while touching a jiggy no longer sends false checks
  - Witchyworld Pads no longer floating
  - sending items don't duplicate
- QOL: 
  - Split Up Pads in Ancient Baths moved to better location
  - Jamjar Silo proximity only allow learnable moves for the silos on the same map
  - Receiving Eggs from Archipelago fills your eggs

- Jinjo Jiggies have been removed temporarily for causing logic issues that were difficult to solve.
  - Jinjo Families will now give a guaranteed local Jiggy, but are not considered for logic

- Major overhaul on the lua client.

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