# 2.1.1-beta
 - remove Wonderwing's Randomized Notes and Cheato requirement 
 - Fix Issue with duplicate items if randomize_moves disabled
 - Fix Issue with Treble Clefs if randomize_moves disabled

# 2.1-beta
 - The Last 4 BK Moves are in the pool:
    - Ground Rat-a-tat Rap
    - Stilt Stride
    - Beak Barge
    - Beak Bomb
 - 4 additional check locations:
    - Goggles (Amaze-O-Gaze)
    - Scrut (Scrotty's Kid)
    - Scrat (Scrotty's Kid)
    - Scrit (Scrotty's Kid)
 - New item in the Pool: Amaze-O-Gaze
 - Progressive Item Fixes
 - Deathlink Loop fix
 - When you start a seed with BK Moves randomized, you start with 1 random attack:
    - Egg Shoot
    - Egg aim
    - Beak Barge
    - Roll
    - Air Rat-a-tat Rap
    - Ground Rat-a-tat Rap (only in advanced and glitched logic)
    - Beak Buster (only in advanced and glitched logic)
 - New Options:
   - Progressive Shoes (Stilt Stride -> Turbo Trainers -> Spring Boots -> Claw Climbers)
   - Progressive Water Training (Dive -> Double Air -> Faster Swimming)
   - Progressive Bash Attack (Ground Rat-a-tat Rap -> Breegull Bash)
 - 60 FPS Toggle - Hit L + Start in-game to increase the in-game clock to run 60 FPS instead of 30 (may affect CPU performance)
 - Logic fixes:
   - Pillars Jiggy: the clockwork shot is now in the advanced and glitched logic.
   - Jade Snake Grove Access: requires beak bomb if going over the door, in glitched logic.
   - Fix Prospector Boulder
   - Detonator access: you can tag the Humba warp pad using a clockwork, in advanced and glitched logic.
   - GGM Jail Jinjo: Shooting a clockwork through the wall is now part of glitched logic.
   - Scrotty Jiggy: The 3 kids have been separated into their own logic, which may have some slight side-effects.
   - Egg barges (glitch): can now be only done with blue, fire and ice eggs.
   - Saucer of Perl logic modified to also require Amaze-O-Gaze for certain tricks

# 2.0-beta
 - 3 Additional BK Moves to the pool:
    - Beak Buster
    - Turbo Trainers
    - Air Rat-a-tat Rap
    - Blue Eggs (sort of.. read below)
 - 3 additional check locations: GGM Crushing Shed Jiggy Chunks
 - Generation no longer fails when a world cost is set at over 70 jiggies.
 - Deathlink is now implemented.
 - Optional Progressive Beak Buster -> Bill Drill
 - New option for Eggs:
   - Start with Blue Eggs (what we are used to)
   - Randomized Starting Egg
   - Progressive Eggs (Blue -> Fire -> Grenade -> Ice -> Clockwork)
 - Logic fixes:
   - GGM entrance Cheato page: can be gotten with glide and tall jump if not on beginner logic. Advanced and glitched logic get to do it with speed shoes, tall jump, and wing whack or glide. Advanced and glitched logic get to do it with the detonator.
   - Crazy Castle Honeycomb: can be gotten with pack whack, in glitched logic.
   - Spaze Zone honeycomb: can be gotten with a clockwork shot from the tent, if on advanced or glitched logic.
   - Lakeside honeycomb: can be gotten with just split up, if not on beginner logic.

# 1.9.2-beta
 - Logic fixes:
   - Jade Snake Grove Jinjo: fixed impossible jumps by adding parentheses.
   - Chuffy Mumbo Token: moved from the GGM region to the Chuffy region.
   - GGM Mumbo notes: can be gotten with beak buster, if not in beginner logic.
   - Generator Cavern Jiggy: the last jump to the jiggy can be done with talon trot.
   - WW train station: solo Banjo can get it with tall jump, grip grab and pack whack, if not on beginner logic.
   - JRL big fish collectables: the big fish's teeth can be shot from the surface with egg aim, in the advanced and the glitched logic.
   - TDL Boulder Cheato Page: removed impossible jumps.
   - Defeating Weldar: refactored the logic for climbing the ladder. Jumping to the rotating pipe can be done for advanced and glitched logic.
   - Quality Control jiggy: Requires climb in beginner and normal logic. Requires egg aim if doing the clockwork warp, in glitched logic.  Glitched logic no longer needs tall jump or flap flip if you're doing the clockwork warp.
   - Floor 1 Guarded jiggy: requires eggs to get the jiggy the intended way. Beginner logic is forced to use egg aim. The clockwork shot now requires Leg Spring or Tall Jump.
   - Waste Disposal Box Jiggy: fixed the logic for advanced and glitched logic.
   - Humba in Witchyworld: can be reached with Leg Spring, if not on beginner logic.
   - Remade logic for entering Chuffy from every world.
   - Pine Grove Access: jumping out of the water can now be done with more moves.
   - Plateau access: fixed blunder where only beginner logic could access it from Pine Grove and Cliff Top.
 - Cheato Rewards fixed (trust)

# 1.9.1-beta
 - Renamings:
   - GI: Floor 2: Box Room (1)/(2) Note -> GI: Floor 2: Box Room Taller Stack/Shorter Stack Note
 - Logic fixes:
   - Any check in GGM that requires talon trot: Springy Step Shoes can be used to get talon trot, if not on beginner logic.
   - Saucer of peril: normal logic will now require climb to be able to see the red button if sniping the red button with grenades.
   - JRL Underwater doubloons: require explosives to have access to the split up pads if using shack pack.
   - River Passage notes: can be gotten with shack pack, if not on beginner logic.
   - Floor 2: Box Room Shorter Stack Note: needs a jump upgrade to get the note, in beginner logic.
   - HFP collectibles: considers entering the level from the train to reach the top half of lava side.
   - Region access:
     - The following transitions are now always in logic if not playing on beginner logic:
       - Pine Grove to Plateau
       - Cliff Top to Plateau
     - GI outside to floor 3: condition relaxed for the fact that Claw Clamber Boots give a free talon trot.
 - Backward Compatibility for Python 3.8
 - Potential fix for Cheato Rewards

# 1.9-beta
 - Logic fixes:
   - Treasure Chamber Cheato Page: can be gotten with a clockwork shot in advanced and glitched logic.
   - GGM Boulder Jinjo: can be gotten with an egg barge in glitched logic.
   - Power Hut Jiggy: requires climb if using split up to do the jiggy, in beginner and normal logic.
   - Water Storage Cheato page: can be gotten with a leg spring dive in glitched logic.
   - Cactus of Strength Jiggy: The jiggy can be reached with Leg Spring + Glide, if not on beginner logic.
   - Space Zone Honeycomb: Can be reached with Leg Spring + Glide, if not on beginner logic.
   - Underwater doubloons: if not on beginner logic, can be gotten with shack pack.
   - Blubbul notes: can be gotten as the sub.
   - Rocknuts Jiggy: requires Tall Jump in beginner logic.
   - Taxi Pack Silo: Reworked logic.
   - River Passage Notes: can be gotten with the T-rex when not on beginner logic.
   - River Passage Honeycomb: can be gotten with the T-rex in advanced and glitched logic.
   - Scrotty Jiggy: Requires Tall Jump in beginner logic.
   - Chompa Jiggy: needs spring shoes if jumping up the pillar on beginner logic.
   - GI Treble Clef: Reworked logic and changed region.
   - Leg Spring Notes: can be gotten with claw clamber boots and a very long jump, in advanced and glitched logic.
   - GI Checks that require Weldar: needs climb.
   - Underwater Waste Disposal Jiggy: fixed the logic for the swim glitch.
   - GI Access:
     - reworked floor 1 to floor 3 transition for glitched logic.
     - Floor 2 to floor 3: Added pokemongenius' grenade wizardry to glitched logic.
   - Icicle Grotto Cheato Page: Reworked logic.
   - Central Cavern Jinjo: if not on beginner logic, can be gotten with leg spring.
   - Trash Can Jiggy: if not on beginner logic, can be gotten without a flight pad.
   - CCL Glowbo Pool: the note and the glowbo can be gotten without dive in advanced and glitched logic.
   - Cliff Top Jinjo: You don't need climb to get it.
   - Mega Glowbo: Can be reached with beak busters if not on beginner logic.
   - HFP to JRL: Needs Tall jump if doing the glitch.
   - All the checks that are dependant on multiple levels: reworked logic for region access. We now let Archipelago tell us if a region is in logic or not, which should greatly improve the generation time.

# 1.8.3-beta
 - Upon generating with wrong settings, a ValueError is thrown, instead of a generic Exception.
 - Logic Fixes:
   - Pillars Jiggy: can dive underwater with beak buster, if not on beginner logic.
   - Bovina jiggy: reworked the logic.
   - Area 51 notes: can be gotten with leg spring.
   - Inferno jiggy: solo Kazooie needs tall jump (all logics) or leg spring (all except beginner).
   - Jolly notes: can be done with a jump from the tables.
   - TDL Entrance jinjo: requires flight to reach the alcove, in beginner logic.
   - The following checks can use leg spring + glide to reach the top of TDL in advanced and glitched logic:
     - Any check where defeating Terry is required.
     - Any check where the flight pad can be useful.
     - Stomping Plains checks.
   - Under Terry's Nest Jiggy: for advanced and glitched logic, can be gotten without defeating Terry, with a clockwork shot.
   - Stomping Plains Jiggy TDL, for normal and beginner logic, requires talon trot.
   - Waste Disposal notes: removed duplicate logic that was wrong.
   - Stomping Plains Jiggy HFP, for normal and beginner logic, requires both talon trot and tall jump.
   - Humba access in TDL: Beginner logic only gets to do it with a jump upgrade. The other logics can get to Wumba without moves via the tunnel.
   - Roar cage notes: can be gotten with the T-rex.
   - GI Floor 2 to Floor 3: requires climb if doing it as BK.
   - Right train station note: can be gotten with the T-rex.
   - HFP Lava Side Honeycomb: Can be gotten as solo Kazooie, if not on beginner logic.
   - HFP Volcano honeycomb: reworked the solo Kazooie logic for normal logic and above.
   - HFP trebleclef: requires moves for Kazooie to break the ice cube. Reworked the solo Kazooie logic. Advanced and glitched logic can shoot a clockwork from the bottom.
   - Mildred Jinjo: requires some jump upgrade as BK, Leg Spring or Tall Jump if using solo Kazooie, Tall Jump if using Mumbo. Can be gotten with a clockwork shot in Advanced and Glitched logic.
   - Glide Silo: can be reached with Leg Spring.
   - Icicle Grotto Jinjo: reworked logic.
   - HFP Train Station Honeycomb: reworked logic.
   - Volcano jiggy: now has logic.
   - Lava Side Train Station: updated with BK moves (oops)
   - Mumbo notes in HFP: doesn't need anything.
   - Boggy fish jiggy: glitched logic needs talon trot or flap flip to do the superslide.
   - Dragon Brothers Jiggy: requires talon trot or Flap Flip if doing the skip, in advanced or glitched logic.
   - Almost all the CCL checks no longer require (tall jump or talon trot or flight pad or grip grab) to accessed (we thought you'd need one of these to move around in central cavern, but it's not the case.)
   - CCL Humba Jinjo: can be gotten as the bee.
   - Pot o' Gold honeycomb: can be gotten with wing whack or glide, if not on beginner logic.
   - Trash Can honeycomb: can be gotten with glide, if not on beginner logic.
   - Central Cavern jinjo: requires Tall Jump if using the spring pad.
   - Mingy Jongo jiggy: beginner logic gets talon trot to dodge the attacks.
   - Plateau Sign notes: can be gotten with leg spring.
   - In advanced and glitched logic, any check where using (talon trot + flutter + beak buster) can now be done with (talon trot + air rat-a-tat rap + beak buster)
  
# 1.8.2-beta
 - Location Renaming:
   - Clockwork Silo (1)/(2) Note -> Clockwork Silo Bottom/Top Note
 - Logic Fixes:
   - GGM Access code fix for collectibles outside GGM. (Canary Mary in CCL, most notably)
   - GGM access: GGM early can now be done with talon trot, in glitched logic.
   - Waterfall jiggy: reworked the logic for the solo Kazooie jumps.
   - Crazy Castle jiggies: added vertical mobility to reach the pump room and the jiggies.
   - Tent Jinjo: In glitched logic, can be gotten with speed shoes.
   - Space Zone Honeycomb: Can be gotten without grip grab
   - Top Clockwork Silo Note logic fix.
   - Stomping Plains jiggies/jinjo: requires tall jump for solo characters, talon trot or tall jump for Banjo-Kazooie combined.
   - Styracosaurus cave honeycomb: requires tall jump if using the spring pad.
   - GI Train Switch: Requires Climb. Advanced and glitch get to use talon trot + (flutter or ratatat rap) + beak buster.
   - Colosseum Jiggy: reworked the logic with climb.
   - CCL Notes: can be gotten as the bee.
  - Change Blue Egg to Egg Shoot in Moves List.

# 1.8.1-beta
 - Randomize Worlds World 2 was looking at World 3 jiggy requirements. Fixed so its back to World 2 requirements.
 - Added Cheato + Honeycomb Calculations to make sure your pages and honeycombs are in sync
 - King Jingaling is now dead when Skip Jingaling is set (Thanks @Austin)
 - Load lua on Title screen to skip intro by pressing start (Thanks @Austin)
 - Hag-1 Phase cutscenes are now skipped (Thanks @Austin)
 - Logic Fixes:
   - Prospector notes: now takes entering from MT into account.
   - TDL Train Station notes: only the right one needs moves.
   - GI region access: getting from outside the building to floor 2 or 3 requires climb or moves to make it to the back of the building from the Pipe.
   - Quality Control jiggy: added Tall Jump if using Mumbo.
   - Clinker's Cavern Jiggy: added Tall Jump if using Mumbo. Glitched logic requires Climb if doing the jiggy with Breegull Bash.
   - Sabreman Jiggy: requires Tall Jump.
   - Mr. Fit Jiggy:
     - The high jump event can be won with flight for logics other than beginner.
     - requires Tall Jump for the sack race.
     - The sprint race can be won with either the bee or turbo trainers for logics other than beginner. Beginner logic needs turbo trainers. Glitched logic can also do it with a clockwork egg.
   - Pot o' Gold jiggy: requires tall jump if using Mumbo is in logic.
   - Cheese Wedge jiggy: requires tall jump if using Mumbo is in logic.
   - Train logic: entering the train requires Flap Flip or Climb. The train is at the ground level in the GI station, so you don't need these moves here.
   
# 1.8-beta
 - Make Randomize Worlds Compatible with BK Moves (Using Warp Silos)
 - King Jingaling Intro can now be skipped (as an option)
 - Logic fixes:
   - Treasure Chamber Honeycomb: needs talon trot or grip grab, depending on if you enter the room from the top or the bottom.
   - Dive of Death notes: fixed logic for advanced and glitched logic.
   - Ledge Doubloons: now requires tall jumps. Normal logic and above can also use Leg Spring.
   - Icy side Pillar Cheato Page: remade the logic.
   - Glide silo: remade the logic.
   - Volcano honeycomb: remade the logic for all logics. May now require to get it from the volcano in beginner logic.
   - HFP Trebleclef: Changed the logic.
   - Lava Waterfall Jinjo: beginner logic gets to have the moves for the intended strat.

# 1.7.1-beta
 - Location renaming:
   - Capt Blackeye Doubloon -> Captain Blackeye Doubloon
   - Near Jinjo Doubloon -> Near Alcove Jinjo Doubloon
   - TDL: Near Train Station (1)/(2)/(3) Note -> TDL: Train Station Right/Middle/Left Note
   - GGM: Near Prospector's Hut (1)/(2)/(3)/(4)/(5) Note -> Near Prospector's Hut Bottom-Left/Top-Left/Top-Right/Middle-Right/Bottom-Right Note
   - GGM: Fuel Depot (1)/(2)/(3)/(4) Note -> GGM: Fuel Depot Front-Left/Back-Left/Back-Right/Front-Right Note
 - Logic Fixes:
   - Blue Mystery Egg: needs tall jump or beak buster to make it out of the water.
   - Honey B Hive: requires talon trot.
   - Top of Temple jiggy: advanced and glitched logics don't need anything to get it. Normal logic can get it with flap flip.
   - Pillars jiggy: the logic was using the wrong function.
   - Bovina jiggy: requires eggs.
   - Bovina honeycomb: has actual logic.
   - Treasure chamber jiggy and honeycomb: requires eggs.
   - GGM entrance honeycomb: doesn't require flutter and air ratatat rap at the same time when jumping off the rope.
   - waterfall cavern jiggy: requires turbo trainers and (grip grab or some jump upgrade) in beginner logic.
   - crushing shed jiggy: added Beak Barge.
   - Generator Cavern jiggy: added light source to beginner and normal logic. Added flap flip to required moves. Added move requirements to cross decent gaps.
   - Power Hut jiggy: added a light source to normal logic.
   - Anything on slopes in GGM: requires talon trot in beginner logic; talon trot, turbo trainers or using solo Kazooie (if possible) in the others.
   - Big Top Jinjo: Can be gotten with Split-Up.
   - Alcove jinjo: requires turbo trainers if paying Blubber is in logic.
   - JRL pipe honeycomb: requires talon trot if going on the roof as BK.
   - Jolly Notes: can be gotten with Flap Flip or (Tall Jump and Grip Grab) in beginner logic.
   - Getting everything underwater before the octopus is now in logic without oxygenate, in beginner logic.
   - Dragon Brothers jiggy: Pack Whack only required if the moves for the damage boost is in logic, for advanced and glitched logic.
   - Hag 1: added moves to make the fight not too hard. Talon trot and Tall jump for beginner logic, either tall jump or talon trot for normal logic.
 - Moves Dpad shows Unlocked BK Moves.
# 1.7-beta
 - Fast Swimming is now an AP Item
 - Double Air is now an AP Item
 - Roysten is 2 checks
 - Logic fixes:
  - Ledge Doubloons (Advanced and Glitched)
  - Oogle Boogle Jiggy (Glitched)
  - Pot o' Gold (Beginner and Normal)
  - Golden Goliath required for freeing Dilberta to turn into Stony
  - Treasure Chamber for beginner fix
  - Seemee Cheato page
  - Prison Compound touch-up
  - fix SubAqua Aim Note count
  - fix Leg Spring Silo logic
 - Cheato Rewards Option - Cheato gives you a cheat + a additional AP item
  - Pages cannot be set as filler with this option enabled
 - Honey B Rewards Option - Honey B gives you health + a additiona AP item
  - Empty Honeycombs are set as progressive items if this is enabled
 - Randomize BK Moves
  - Cheato Rewards + Honey B Rewards must be enabled
  - Randomize_Worlds is not supported for this for now.
  - 10 randomized moves so far:
   - Dive
   - Flight Pad
   - Flap Flip
   - Egg Shoot
   - Roll
   - Talon Trot (if set to ALL)
   - Tall Jimp (if set to ALL)
   - Climb
   - Flutter
   - Wonderwing
   
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