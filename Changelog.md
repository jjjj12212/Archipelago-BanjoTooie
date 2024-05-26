# 1.7-beta
 - Fast Swimming is now an AP Item
 - Double Air is now an AP Item
 - Roysten is 2 checks
 - Logic fix:
  - Golden Goliath required for freeing Dilberta to turn into Stony

# 1.6.2-beta
 - Token Hunt will always generate 15 tokens.

# 1.6.1-beta
 - fix Token Hunt Goal Reminder Message
 - fix Jinjo Tokens

# 1.6-Beta
 - Stop N Swap check locations fixed when not randomized
 - Fix Stop N Swap Not sending checks issue.
 - Logic fix:
  - Inferno area fixed
  - TDL T-Rex jinjo in glitched logic
  - Inferno Access in glitched logic
  - Leg Spring Jinjo in GI fix
 - HAG-1 Open backend changes
 - Wonderwing Challenge will Open HAG-1 once all 32 tokens are collected
 - Fix Jinjo mixup between Black and Purple.
 - Reworked Mumbo Tokens, Rewards + Mumbo Token, No longer removal of reward.
 - Mumbo Token limit decreased to 15 due to technical reasons
 - Some locations got their name changed
   - All Jinjo Village checks will now start with "IoH" instead of "JV".
   - Stop and Swap items start with the world in which they are.
   - All 8 notes around the tent in Witchyworld are now called "Around the Tent"
   - The 3 notes on the Split Up pads and the warp pad in CCL are now called "Central Notes"
 - New Options:
  - exceeding_items_filler option - Items over the required amount are marked as junk/filler. Otherwise, exceeding items stays the same type.
  - disable_overlay_text - Disables the overlay text on Banjo-Tooie. Useful when viewing
  or streaming the BT_Client.

# 1.5.1-Beta
 - Logic changes:
   - All logics: The TDL entrance jinjo can be gotten by beak bombing the switch.
 - Fix for UT
 - DPad Down also shows level unlocks

# 1.5-Beta
 - You can now adjust the Jiggy requirements to open any world (YAML option)
   - Presets for opening worlds: Quick, Normal, Long, Custom
   - When set to Custom, you can adjust each world manually through the YAML.
 - Logic Fixes
   - GI Floor 2 Jinjo
   - Ice Eggs are required for Beginner Logic for UFO Jiggy
   - Canary Mary
   - Pink Egg
   - SeeMee Cheato Page
   - Water Storage Jinjo
 - Fix Heggy Softlock when returning to the shed after hatching eggs
 - Fix Stations when not randomized
 - Fix Trebles when not randomized
 - New Goal: Mumbo Token Hunt
 - New Goal: Wonderwing Challenge

# 1.4.1-Beta
 - logic fix for HAG-1 when open option is set
 - set Prison code: sun, moon, star, moon, sun
 
# 1.4-Beta
 - Refactor Region logic
   - Beginner logic: it is now in logic to leave a level from the main entrance, as long as the level is open.
 - New logic: glitched logic
   - For the time being, selecting the "Hag 1 open" doesn't actually make Hag 1 be open from the very beginning. So you still need 55 jiggies if the end goal is Hag 1. This will be changed soon™.
 - Option to Skip Klungo 1 & 2 (until he is a required check)
 - Item renaming
   - Snake Head Cheato Page is now Treasure Chamber Cheato Page
   - Boulder Honeycomb is now Prospector Boulder Honeycomb
 - Logic changes
   - Fixed various inconsistencies with beginner logic.
   - Advanced
     - Floor 1 guarded jiggy: clockwork shot now in logic.
     - Ancient Swimming Baths Cheato Page: clockwork shot now in logic.
     - Mega-Glowbo: clockwork shot to get the ice key now in logic.
     - Cliff Top jinjo: clockwork shot now in logic.
     - Mrs. Boggy jiggy: the jump from the ticket stand spring pad to the Area 51 is now in logic.
     - Icy Side Pillar Cheato Page: clockwork shot now in logic, from the glide silo.
     - Trash Can Jinjo: clockwork shot now in logic.
     - GI Floor 1 AC notes: clockwork shot and jump with wing whack now in logic.
 - Stop N Swap Added to the pool as a option
  - Items:
    - Blue Mystery Egg
    - Pink Mystery Egg
    - Ice Key
    - Breegull Blaster
    - Jinjo Multiplayer (Nothing)
    - Homing Egg Toggle (Aim Assist disabled until this item is obtained)
  - check Locations:
    - obtaining Eggs
    - obtaining key
    - hatching all three eggs
 - Open Hag-1 Option now opens Hag-1 upon creating a new save-file.

# 1.3.1-Beta
 - Fix Randomize Worlds for beginners. Allow randomization
 - Fix GI access for beginners logic 

# 1.3-Beta
 - Logic fixes with certain collectibles
   - Inferno honeycomb and Cheato page
   - Pig Pool jiggy
   - Water Storage Jinjo: Now with proper logic!
 - Customizable lengths of Boss hunt and Minigame hunt.
   - Can also be randomized
   - If Boss Hunt or Minigame Hunt is selected, Cheato Pages WILL BE RANDOMIZED  
 - New Goal:
   - Jinjo family rescue
    - With customizable length or randomized
 - Lua and Text overlay will remind you of your goal each session 
 - jjjj12212 will no longer be the ONLY ONE having a text overlay on his screen. Everyone gets it now!
 - Fixed randomize worlds when multiple players use it in the same AP. Now everyone wont have the same order.
 - 20 note nests are set to be filler items when randomize_notes are enabled.
 - Fix Universal Tracker showing MT all the time.

# 1.2-Beta
- 2 new Goals added:
  - Minigames Goal: Complete all minigames with optional Canary Mary 4.
  - Boss Goal: Defeat all world bosses except for HAG-1
- Chuffy fix

# 1.1.2-Beta
- Fix uploading to Archipelago Webhost fix
- Hag-1 skip Introductions

# 1.1.1-Beta
- Many notes got renamed
- Notes fix when not randomized
- Universal Tracker fix
- Show level unlocked in BTClient
- Fix Patches
- Logic Changes
  - JRL Toxic Pipe Honeycomb: you can jump from the roof of Jolly's and glide to it in normal and advanced logic.
  - CCL Trash Can Jinjo: advanced logic can get it with just split up and glide.
  - Advanced logic: Clockwork Egg shots are now considered in logic for these items
    - Waterfall jiggy
    - smugglers jiggy
    - floor 5 jiggy
    - Stadium jinjo
    - water storage jinjo
    - floor 2 jinjo
    - central cavern jinjo
    - Icy Side Wind Tunnel jinjo
    - Icicle Grotto Jinjo
    - waste pipe honeycomb
    - styrac honeycomb
    - HFP Train Station honeycomb
    - Snake heads cheato page
    - jade snake grove cheato page
    - haunted cavern cheato page
    - HFP trebleclef
  - Central Cavern jinjo: can be obtained with bill drill and springy step shoes in normal + advanced logic
  - Fixed bug with GI Train Station Honeycomb Logic

# 1.1-Beta
- Dpad changes:
  - Dpad Left - Shows unlocked Magic
  - Dpad Down - Shows unlocked Treble Clef & Stations
  - Dpad Up + L - Refill Consumables
  - Dpad Right + L - Super Banjo
  - Dpad Left + L - Aim Assist
  - Dpad Down + L - Health Regen
- Notes
- Notes Randomized
- Handle AP Notes for Jamjars
- Randomize World Order (NOT "World Entrances")
- Handle framework to customize jiggy amounts (future update)
- Easter eggs removed
- QOL
  - Bosses Cutscenes, no longer have to wait until Banjo Arrives at boss
- change wording for forbid certian AP items on Jinjo Families
- add YAML option to only forbid Magic behind Jinjo Families
- Logic Changes
  - Beginner logic
    - Power Hut Jiggy: (Detonator or Bill Drill) and Split Up
    - Treasure Chamber Jiggy: Egg Aim and (Grip Grab or Access to Flight pad)
    - Snake Head Cheato Page: Access to Flight Pad or (Egg Aim and Grip Grab)
  - Talon Torpedo required from Wasteland to Pine Grove

# 1.0.4-Beta
- Logic Changes:
  - Talon Torpedo required on Normal Logic from Wasteland to Pinegrove.
  - Modify Alcove Jinjo requirements on Normal Logic.
- Real bugfix for Jinjos

# 1.0.3-Beta
- Added glitched logic
- Logic Changes:
  - Flooded Caves Jiggy requires the detonator in beginner logic.
  - Mrs. Boggy jiggy no longer requires explosives in advanced logic.
- Bugfix for Jinjos

# 1.0.2-Beta
- Mrs. Boggy now stays at the park
- restarting connector for "fixing" opening levels no longer required (if skip_puzzle enabled)
- Jinjo Menu shows jinjos
- Chuffy at multiple stations fixed
- Logic changes:
 - Checks pinegrove access if you have Dragon unlocked
 - Pot o' Gold now requires Split Up or Rain dance in advanced logic 


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