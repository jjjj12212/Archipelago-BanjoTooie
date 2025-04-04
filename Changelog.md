# 4.4.2
  - Logic fixes:
    - Simple Random Starting Egg doesn't assume you start with Blue Eggs
  - Location Groups added (thanks to Axu_AP)
    - Mayahem Temple
    - Glitter Gulch Mine
    - Witchyworld
    - Jolly Roger's Lagoon
    - Terrydactyland
    - Grunty Industries
    - Hailfire Peaks
    - Cloud Cuckooland
    - Isle O' Hags

    - Cheato Rewards
    - Jinjo Rewards
    - Honey B Rewards

    - Jiggies
    - Jinjos
    - Empty Honeycombs
    - Cheato Pages
    - Notes
    - Treble Clefs
    - Doubloons
    - Signposts
    - Jamjars Silos
    - Glowbos
    - Train Switches
    - Stop 'n' Swop
    - Nests
    - Warp Silos
    - Warp Pads
    - Bosses
    - Minigames

# 4.4.1
  - Logic fixes:
    - Landing on the roof in GI is back in logic.
  - You are now required to use Bizhawk 2.10. 2.9.1 and lower are not supported... again.

# 4.4
  - Warp Pads and Silos can now be randomized.
    - Warp Pads and Silos are unusable until you receive the corresponding item.
    - Getting near them gives a check.
  - Options
    - Randomize Warp Pads
    - Randomize Silos
    - Open Silos rework
      - You can now choose how many silos are pre-opened, from 0 to 7.
    - New Egg Behaviour Option
      - Simple Randomize Starting Eggs (you will start with a random egg, but it won't be Clockworks).
    - Open Hag 1
      - Was moved among the victory condition options
    - Added options replace_extra_jiggies and replace_extra_notes.
      - Disable these options will cause the game to always have exactly 900 notes and 90 jiggies instead of potentially some of them being other filler items.
  - Improved the hint system
    - Underscores (_) and long names should no longer cause an issue while reading the hint in game.
    - Hints to progression items are slightly more likely to show than hints to useless items, but slower locations are still likely to be hinted.
    - These locations no longer show up in signpost hints:
      - Excluded locations;
      - World openings;
      - Boss, minigame and jinjo family Mumbo Token locations.
    - Cryptic hints are now clearer
      - One of a kind progression items will be hinted as "legendary one-of-a-kind".
      - Currency-like items (plentiful progression items, like Notes in Banjo-Tooie) will be hinted as "great" instead of "wonderful". This might not be perfect for all games.
      - Useful, but not required items will be hinted as "good"
      - Fillers (normal items) will be hinted as "useless"
      - Multi-classification items are hinted as "weird"
      - Traps are hinted as "bad" items.
  - Notes, Cheato Pages, Honeycombs are no longer considered during progression balancing, they may be spread more evenly across the playthrough.
  - Mumbo Tokens will be considered for progression balancing.
  - Jamjars will now announce which Move Silo is unlocked when you get enough notes!
  - Archipelago Menu contains a menu for Warp Silos and Warp Pads.
  - Everdrive fix for signpost checks
  - Logic Fixes
    - Due to warp pads being randomized and constraints from the existing code, a lot of the solo Kazooie exploration has been removed from the logic. It may return in the future.
    - Honey B Rewards: can now be gotten by getting the Claw Clamber Boots from Cliff Top.
    - Cactus of Strength Jinjo: removed climb + talon trot + air rat-a-tat rap from easy tricks because it was too hard.
    - Bunch of Logic fixes.
  - We are temporarily supporting Bizhawk 2.9.1 until the next Archipelago major release is out. (Version 6)

# 4.3
  - You are now required to use Bizhawk 2.10. 2.9.1 and lower are not supported.
  - New filler options
    - We retired the "traps" option in favor of "max_traps". Now you can set a hard limit for how much suffering you want!
    - We now allow you full customization of how likely each filler or trap item would appear in the filler pool.
    - Jiggies, 5-Pack Notes and Doubloons can all now appear as filler items!
      - You are guaranteed enough to access all checks, plus a reasonable buffer. The rest can be replaced with other filler items.
      - You can also customize how likely these appear by changing the appropriate settings.
      - Yes, you can have a jiggy jamboree if you want (up to 250 jiggies)
  - Read hints will now be added to Archipelego.
    - Due to a limitation, only your own locations will be added as hints in AP; your items in other people worlds won't be added.
  - Fixed a bug where some regions can be logically inaccessible despite having the required items to reach them.
  - Logic fixes
    - Plateau stuff: talon trot can be gotten from the Cliff Top Claw Clamber Boots.
    - MT to GGM: Intended logic no longer logically requires the stony.
    - Nests Near Bill Drill silo: can be gotten with the detonator
    - Prospector Notes: for intended logic, added tall jump + grip grab for all the notes except top-right.
    - Chuffy Signpost: fixed a bug where intended logic was looking for the HFP train station to reach Chuffy from IOH
    - Saucer of Peril, WW to GGM: Fixed logic to grip grab the wire.
    - Humba in WW: requires Flap Flip if you climb there as BK.
    - Mrs Boggy Jiggy: Now requires moves to reach the burger switch
    - Jolly's Notes: can be gotten with roll.
    - Springy Step Shoes silo: Springy Step Shoes readded
    - Stomping Plains stuff: talon trot can be gotten from shoes, the jiggy can be gotten by crossing with separate character then combining at the end.
    - Inside the Mountain Egg Nests: can be gotten with Shack Pack
    - GI Floor 1 High pipe nests: reworked logic to fix tall jump + claw clamber boots not being in logic.
    - Oil Drill Notes: if not on intended logic, can be gotten with Claw Clamber Boots.
    - HFP Colosseum stuff: reworked intended and easy tricks logic for crossing the pillars to the colosseum.
    - CCL Sack Race Note, Cheese Wedge Exit Note: Can be gotten with glide + claw clamber boots
    - CCL Green Pool Stuff: Jumping from the outside to skip dive is now in easy tricks.
    - CCL Indoors Glowbo: can be gotten with Shack Pack
  - The generation now throws an OptionError when a yaml has incompatible options.
  - Lots of Test fixes (development)
  - Should now be compatible with other AP games that uses get_all_state()
  - changed Dialog messages when receiving your own items (normanhenges)

# 4.2.1
  - randomize BK moves requires either randomize notes, nestanity, or randomize signposts to fix generation issues
  - progressive shoes now requires nestanity, or randomize signposts

# 4.2.0
  - New victory condition: Boss Hunt + Hag 1.
    - Defeat bosses chosen from a new yaml option, then defeat Hag 1 to win.
  - Signposts can now have hints!
    - You can choose how many hints there are among the 61 signposts in the game.
    - You can choose how many of those hints are directed to moves, the rest hint at slow locations.
    - You can choose whether a hint tells what item is on a location (clear hint), or only tells how good the item is (cryptic hint).
  - Signpost can now be checks, independantly of if the signposts contain hints or not.
  - New trap: tip trap.
    - Upon receiving the trap, you will receive one of the vanilla sign texts as a dialogue. No, you cannot skip the textbox!
  - You can choose whether you want to be able to use SUPERBANJO, SUPERBADDY, NESTKING, HONEYKING at will during gameplay.
  - New option to make Canary Mary minigames much easier.
  - New options
    - Boss Hunt + Hag 1 length
    - Choose how many signposts give hints.
    - Choose how many signpost give move hints.
    - Choose how clear signpost hints are.
    - Choose if signposts are checks.
    - Weight options for traps. You can now specify how likely a trap will be Golden Eggs, a Trip Trap, a Slip Trap, a Transform Trap, a Squish Trap, or a Tip Trap
    - Easy Canary Mary
    - Extra Cheats
  - Removed Knuckles from the game
  - jjjj12212 can't math. fix item location matching when jinjos are not randomized.
  - Fixed number of progression jiggies when Hag 1 is closed
  - Fixed generation issue when you had nestsanity off and cheato page randomization off.
  - Chuffy is back in GGM when the train is derailed, due to the fact that the signpost inside the wagon can be gotten without Chuffy.
  - The jukebox in Jolly's is fixed from the start.
  - This update features the first fixes from the PR.
  - Better error message when getting a version mismatch in the Lua connector.
  - Logic fixes
    - MT to HFP access: added entering the stadium with the beak bomb glitch if backdoors is active
    - GGM to WW: the transition was removed by mistake, it got readded.
    - GI Elevator doors: removed clockworks from the logic. It doesn't work.
    - Plateau Sign Notes: Removed split up + tall jump from easy tricks logic
    - Quagmire feather nests: if not on intended logic, can be gotten with beak buster
    - Pillar Nests: reworked logic
    - Generator Cavern Jiggy: In hard tricks and glitch logics, added flap flip + beak buster, and flap flip + grip grab.
    - Dodgem Dome Jiggy: Added talon trot as a requirement if doing the clockwork warp
    - Inside the Mountain Egg Nests: Can be gotten by sinking as the T-rex
    - Alcove Doubloons: fixed a bug where they would sometimes be in logic without split up or explosives
    - Pig Pool Jiggy: the waste disposal switch can be pressed with the dragon Kazooie flame.
    - Springy Step Shoes Silo: Removed Springy Step Shoes as a way to get it
    - Oogle Boogle cave stuff: is now in logic if entering TDL from the backdoor is possible
    - TDL Waterfall alcove nests: in glitched logic, can be gotten as the big T-rex with its head.
    - TDL trebleclef: same as above
    - Floor 4 to Floor 4 Back (past the crushers): added talon trot to the clockwork warp for added ease
    - Elevator shaft: now properly links to the back of floor 2, 3, and 4 in logic.
    - Floor 1 Guarded Jiggy: For nonintended logics, leg spring + glide through the front window is now in logic.
    - Outside GI Left of Building Feather Nest: removed split up + tall jump, since it's not possible
    - Quality Control Jiggy and Nests: added talon trot to the clockwork warp for added ease
    - Clinker's Cavern Jiggy and nests: same as above
    - Floor 4 nest near battery door: same as above
    - Floor 3 glowbo: added logic. Yes, it really took this long to realise that it did not have any logic.
    - Floor 2 Scaffolding Nests: reworked logic.
    - Icy Side Train Station nests: swapped logic of both nests
    - icy side train station jiggy: added clockwork shot to hard tricks and glitches logic if going inside the train station
    - Inside Trash Can nests: reworked solo Kazooie logic
    - Dippy Note: on easy tricks logic, can be gotten with beak buster. On hard tricks and glitches logic, can be gotten with no moves.
    - Dippy Jiggy: same as above, as far as diving goes.
    - Glowbo pool stuff: easy tricks can do it with beak buster

# 4.1
  - Multiplayer Jinjo is back for Token Hunt
  - Fixed issue where items and checks were not balanced in Token hunt
  - Fixed issue where if you start with a progressive item, items / checks are not balanced
  - Golden egg nests are now traps
    - They will only appear if traps and nestanity are enabled.
  - New Option:
    - Set Nest ratios to traps. (From Dev :Dardy)
  - Fix generation issues where there wouldn't be enough locations to reach your first world with McJiggy Special
  - Logic fixes:
    - TDL to Chuffy: if not on intended logic, can be done with flap flip + beak buster
    - HFP to MT, Colosseum Egg Nests, Colosseum Cheato page, Top of HFP access: The walls can be broken with Dragon Kazooie! Thanks to JXJacob for figuring this out!
    - Colosseum Egg Nests: removed Mumbo from intended logic
    - Mildred Jinjo: can be gotten with Dragon Kazooie
    - HFP to JRL: added air rat-a-tat as a possibility, if doing the glitch
    - SM Waterfall Platform: can be gotten with talon trot
    - Cliff Top Feather Nest 3: if not on intended logic, can be gotten with beak buster. If on hard tricks or glitches, can also be gotten with flutter
    - Cheese Wedge Jiggy: if using glitches, checks for flight pad. Doing clockwork warps as solo Kazooie is now in logic
    - Prison Compound Quicksand Jiggy and Cheato page, Pillar jiggy and nests: Fixed bug where you didn't need grip grab if using flap flip to climb the jail cell
    - Prison Compound Feather Nests: added clockwork shot in hard tricks logic
    - Fuel Depot nests: If getting them from GGM, detonator is required
    - Area 51 nests: moved to a new region to allow getting the nests from TDL
    - Area 51 notes: added glide as a way to get them, if not on intended logic
    - Dodgem Dome Jinjo: if not on intended logic, can be gotten with leg spring + glide
    - Space Zone Honeycomb: Removed tightrope walk as solo Kazooie from easy tricks logic
    - Waste Disposal Pump Room collectables: in hard tricks and glitch logics, you can clear the pipes with tall jump + beak buster, tall jump + flutter, or talon trot + (flutter or air rat-a-tat rap) + beak buster
    - Oogle Boogle Jiggy: added tall jump to use the spring pad
    - Trash Compactor Jiggy: added tall jump as a requirement if pack whacking accross
    - Trash Compactor Nests: if not on intended logic, having a clockwork walk to the nests is now in logic
    - Air conditionning fan feather nests: removed leg spring from intended and easy tricks, due to its difficulty. The other logics also require Wing Whack or Glide to get these nests.
    - Air conditionning near repair depot nests: Getting them as solo Kazooie is now in hard tricks and glitch logics
    - Floor 3 notes: added leg spring as a possibility
    - Aliens Jiggy: Fixed bug where it checked if you could reach Atlantis
    - HFP trebleclef, volcano honeycomb, glide silo, ice pillar Cheato page, icicle grotto spring pad nest, icicle grotto top nests: for intended logic, only going through icicle grotto is now considered.
  - Potential fix for the rare console only random crash
  - Fix for not being able to do certain minigames if speed_up_minigames is off
  - You can no longer enter the HAG-1 fight early in the Wonderwing Challenge by completing the Jiggywiggy Challenge for that door
  - A message will show if instant transform fails because you haven't visited the Wigwam/Skull yet
  - Deathlink and Traps will no longer happen in most minigames

# 4.0.1
  - Renamings:
    - Quagmire Feather Nests:
      - 1 -> Left Feather Nest
      - 2 -> Back Feather Nest
      - 3 -> High Feather Nest
  - Logic fixes:
    - Another Digger Tunnel to Pine Grove: if nestsanity is on, it checks to see if you can leave the tunnel with dive or beak buster
    - Gruntilda Lair: moved into its own region. This fixes nests that were not in logic with flap flip + climb
      - For hard tricks and glitches logics, can be reached with tall jump + beak buster, or talon trot + flutter + beak buster
    - Gruntilda's Lair Top Egg Nests: easy tricks logic can get them with grip grab or beak buster. Hard tricks and glitches logics can also get them with flutter, air rat-a-tat rap or a clockwork shot
    - Prison Compound collectibles: the top of the prison cell can be reached with just Flap Flip
    - Chuffy Access: if not on intended logic, can be reached with just flap flip from HFP
    - Fuel Depot nests: refactored logic to make it so that getting the detonator puts them in logic
    - Under Terry's Nest Jiggy: removed the clockwork shop to get it early, as it's too hard
    - Top-Left of Superstash Egg Nest 2: fixed bug that made it use the wrong logic
    - Quagmire Feather Nests: fixed logics that were swapped
    - Trash Compactor Nests: fixed typo in logic
    - Volcano jiggy: on hard tricks and glitches logics, can be done with split up
    - Pot o Gold collectibles: the pot o gold can be reached with glide, if on hard tricks or glitches logics.
    - Cheese Wedge Exit Note: if not on intended logic, can be gotten with split up + springy step shoes
  - Fix early Claw Clamber Boots if CK entrance is your first entrance
  - AP Menu -> Options -> Reset has been renamed to Back to Jinjo Village to be clearer on its function
  - AP Nests will now sparkle on collection, similar to collecting non-AP nests
  - Sparkles appear around you when instant transforming
  - Fix for CCL: Wumba's Wigwam Egg Nest 2 not always marking as collected
  - Fixed the HFP Dragon Brothers having Storm Trooper aim
  - Unogopaz will no longer crash the game if you approach as Banjo, instant transform to Stony, then attempt to talk to him
  - Traps will be postponed while paused and during the Canary Mary races
  - Zubba's Nest door will now auto open if you instant transform to Bee, once you've opened it normally before
  - You will be forced to Bee when entering Zubba's Nest

# 4.0
  - Banjo-Tooie Rom Patch Released!
    - The patch is NOT built per seed. It is built per version. So you will only be prompt to patch your game once per version.
    - Reworked the lua AGAIN!!! To better fit the new ROM
    - Sent items now shows up normally in game when received
    - Items that do not have their own icons (like moves). A in-game dialog will appear.
    - Gruntilda will mock you when you die in game.
    - You can set the Character in the dialog Or keep it default or completely randomized.
    - Pause Menu now has a Archipelago Menu. Those you are familiar with the lua console menus are now moved to this menu.
      - You can respawn or reset you game within this menu as well as access certain cheats
    - Special Opening Credits
    - Contains ALL of our existing features!
    - This Randomizer is fully compatible with the Everdrive! You will need to run a special application that we provide while you have a USB cable connected. We know the Everdrive X7 is compatible. (Your everdrive needs a USB port. (2.5 is not compatible)). The Expansion Pak is required.
    - You can now "Instant" Transform to mumbo or Humba Transformation with the left D-pad. HOWEVER! Due to logic issues, you will have to enter Mumbo's Skull or Humba's Wigwam to unlock the "Instant" transformation (no longer requires map transitions).
      - There are a few maps where you cannot do this, but you will get sound feedback saying that you cannot transform.
  - New Features / Changes!
    - Nestsanity
      - All feather and egg nests are checks. 473 new locations!
      - When this option is selected, the following fillers are added into the game:
        - Egg Nest: gives 1 nest worth of your least filled eggs
        - Feather Nest: gives 1 nest worth of your least filled feathers
        - Golden Egg Nest: You get golden eggs for 60 seconds
      - Uncollected nests have the Archipelago logo as their texture
    - More Progressive items
      - Adv. Water Training - Dive to Sub Aqua Aiming to Talon Torpedo to Double Air to Faster Swimming.
      - Flight - Flight Pad to Beak Bomb to Airborne Egg Aim
      - Egg Aim - Third Person Egg Shooting to Egg Aim
      - Adv. Egg Aiming - Third Person Egg Shooting to Amaze-O-Gaze to Egg Aim to Breegull Blaster
    - Options to reduce the amount of notes to be collected
      - Bassclefs (10 notes). 1 Bassclef adds 1 Big-O-Pants (up to 30)
      - Swap with additional Trebleclefs. 1 additional Trebleclef adds 3 Big-O-Pants (up to 21)
    - Traps!
      - Replaces ALL Big-O-Pants with 4 Very Special Traps
      - The Traps are:
        - <b>Redacted</b>
        - <b>Redacted</b>
        - <b>Redacted</b>
        - <b>Redacted</b>
    - Jamjar Silo costs are now Randomized
      - Either Completely random
      - Progressive (vanilla costs, but they get reordered based on the order in which the levels open)
    - Remove Cheato as Filler Option
    - Remove Refill cheat
    - Remove Bizhawk messages option
    - Custom World Costs are no longer seperate options in the yaml, but rather a single string.
    - Completing Jinjo Family Rescue or Token Hunt requires you to take them to Bottles' House to complete your run.
    - If you don't have Chuffy and it is randomized, Chuffy will not be at GGM Station.
    - If you are doing the Wonderwing Challenge, you no longer always start with Wonderwing as your attack
  - Renamings:
    - Scrotty Kids have their names changed with their problem, to avoid confusion
  - Logic fixes:
    - Targitzan Jiggy, Pink Mystery Egg, the entirety of Atlantis: fixed a bug where progressive eggs made it so that getting those checks never became in logic
    - Prison Compound access: refactored to delete legacy code
    - Bovina Jiggy: can be done with ice eggs
    - Dodgem Dome Jiggy: fixed the logic for the clockwork warp, for glitch logic
    - Area 51 honeycomb: refactored logic due to new fuel depot region
    - Pig Pool Jiggy: if not on intended logic, you can jump over the pipes in the waste disposal with tall jump + beak buster, or talon trot + flutter + beak buster
    - Stomping Plains collectables: reworked the logic to remove redundancy
    - TDL Entrance jinjo: for intended and easy trick logics, jumping onto the pillar and into the alcove is no longer in logic, due to its difficulty
    - TDL Train station: for intended and easy tricks, require a jump upgrade to enter
    - Unga Bunga Entrance Glowbo: if not on intended logic, can be gotten with a beak buster. Hard tricks and glitch logics can get it with air rat-a-tat rap
    - GI Floor 2 Taller Box Stack Note: removed damage boost from easy tricks logic
    - Waste Disposal (water pump room): can be reached with just talon trot.
    - HFP Ladder Notes: intended and easy tricks logics can get them with split up
    - Dragon Brothers Jiggy: reworked the logic with moves that are required for the damage boost
    - Trash Can Honeycomb: can be gotten with the bee
    - Superstash jiggy: if jumping from the sack pack entrance to reach the switch near superstash, you need climb
    - Mr. Fit jiggy: hard tricks and glitch logics can shoot a clockwork for the high jump event
    - Plateau to Pine Grove: shooting the fire switch in third person as solo Kazooie is now in all logics except intended
    - Floor 1 access: flying into the floor 1 window to access floor 1 is now in logic
    - TDL to hatch: refactored logic
  - Other fixes:
    - Correct issue that where certain victory lengths was not considered during generation

# 3.5.3-beta
  - Logic Fixes:
    - MT Honeycomb: takes glitched access into JSG into account for the stony.
    - Treasure Chamber Jiggy: added condition to make sure you can reach the treasure chamber.
    - GGM Entrance Glowbo: In hard tricks and glitches logics, can be gotten with nothing by jumping on the right side of the slope.
    - GGM Mumbo Notes: if not on intended logic, can be gotten with turbo trainers or springy step shoes.
    - Alcove Doubloons: For hard tricks and glitch logics, can be gotten with:
      - Pack Whack + Tall Jump + Grip Grab
      - Tall Jump + Wing Whack
      - Tall Jump + Glide
    - Chompa Jiggy: For hard tricks and glitch logics, added beak buster as a way to reach the flight pad.
    - Glitched access to the top of TDL: if going through the insides of the mountain, requires tall jump, grip grab, or beak buster to reach the flight pad.
    - GI Train station honeycomb: if not on intended logic, can be gotten with leg spring.
    - Air Conditionning Plant Note 2: in intended logic, added moves to cross the gap.
    - Dragon Brothers jiggy: added moves to jump over the tongue
    - HFP Kickball Jiggy: takes glitched access into JSG into account for the stony.
    - CCL Humba Jinjo: Uses logic that was meant to be in use for the past 2 months. Oops!
      - From the logs from 3.0-beta: "can be gotten with leg spring, if not on beginner logic. Advanced and glitched logic can get it with a clockwork shot."
  - Fix UT getting accurate counts for Notes and Jiggies
  - BTClient allows CLI but untested with arguments (jjjj12212's evironment isn't able to...)

# 3.5.2-beta
  - Renamings:
    - Area 51 notes: renamed to left and right notes.
    - GI locations: will now have the floor in the name.
  - Logic fixes:
    - GI got a significant region refactor. Many different regions got added. This has many side-effects on the logic, including logic changes to the following locations.
      - Guarded Jiggy, Weldar Jiggy, Underwater waste disposal jiggy, repair depot Cheato page, Weldar Mumbo token: moved to floor 1.
      - GI Train Switch: moved to Outside Back
      - GI Trebleclef, Outside Jinjo, Floor 2 Cheato Page: Moved to outside
      - Worker Jiggy: moved to floor 2
      - Boiler Plant Jinjo, Twinklies Packaging jiggy: moved to boiler plant
      - Clinker's Cavern jiggy, Quality Control Jiggy: moved to back of floor 4
      - Floor 5 jiggy, Floor 5 jinjo, Chimney honeycomb: moved to floor 5
    - MT Entrance Honeycomb: in glitch logic, can be gotten with breegull bash.
    - GGM: Can be entered from Water Storage.
    - Flooded caves jiggy: the final platform can be reached with grip grab or beak buster
    - Left Area 51 note: added long jump requirement if getting it as Banjo-Kazooie.
    - Pig Pool Jiggy: accessing the JRL pipe from the slit above Jolly's is in all logics
    - Checks that require the TDL flight pad: fixed a bug where the flight pad was in logic without flight pad.
    - Unga Bunga Glowbo: can be gotten with turbo trainers or springy step shoes, if not on intended logic.
    - Central Cavern Jinjo: No longer needs bill drill on advanced and glitched logic. You can use the shoes near the split up pads

# 3.5.1-beta
  - Logic fixes:
    - Treasure Chamber Jiggy: checks if you have talon trot, if you're reaching the top from the inside. Also, if not on intended logic, takes getting the relic from TDL into consideration.
    - Snake Head Cheato Page: Checks if you have talon trot, if you're reaching the top from the inside. For intended logic, no longer requires egg aim if reaching it by flight.
    - Plateau to GGM: For GGM early, doing it with talon trot + air rat-a-tat rap + beak buster is no longer in logic.
    - GGM Entrance Cheato page: going for it as you enter the level is no longer in logic, due to technical reasons.
    - Bill Drill silo: can be gotten with talon trot + flutter + grip grab, or tall jump + grip grab.
    - Plateau Sign notes: if not on intended logic, can be gotten with
      - split up + tall jump
      - split up + glide
      - split up + grip grab
    - Saucer of peril: the door can be opened with a clockwork shot, in hard tricks and glitches logics.
    - Dive of Death notes: In glitch logic, can be gotten with pack whack or taxi pack.
    - Pig Pool Jiggy: checks to see if you can press the button in the Waste Disposal. Also, all logics except intended can use turbo trainers to reach the pipe.
    - Mumbo in TDL: can be reached with no moves. Intended logic still requires stilt stride.
    - Mumbo Glowbo in TDL: Same as a above.
    - TDL Entrance Jinjo: removed stilt stride as a way to get talon trot.
    - TDL Unga Bunga Glowbo: If not on intended logic, can be gotten with the T-rex.
    - Springy Step Shoes silo: If not on intended logic, added springy step shoes and turbo trainers as a way to get talon trot.
    - Central Cavern Jinjo: If you're using Springy Step Shoes, it also checks that you have bill drill. It can also be gotten with bill drill + springy step shoes + grip grab.
  - CCL exit Bubble will appear even though CCL is closed. (no more save+quit)
  - Additional fixes for Transformations
  - Buttonbinding changes:
    - L = Humba
    - L+R = Mumbo
  - fix backdoor with oogle boogle

# 3.5-beta
  - Logic fixes:
    - Water Storage Cheato page: if not on intended logic, solo Banjo can get it with tall jump, pack whack, grip grab, climb, and dive.
    - Dive of Death Notes: hard tricks logic and glitches logic get to get them with glide or leg spring. Easy tricks gets tall jump to make retrying easier.
    - Oogle Boogle Jiggy: Requires talon trot to reach the Claw Clamber Boots, as well as a way to pass the Area 51 gate.
    - TDL Train Switch: Can be gotten with tall jump + grip grab. If not on intended logic, can be gotten with tall jump + air rat-a-tat-rap, or springy step shoes.
    - T-Rex Roar: fixed bug that caused the check to always be in logic.
    - Loggo Cheato page: If using the intended logic, unblocking Loggo with bill drill is required. Other logics can also use grenades, beak barge, breegull bash, or Pack Whack.
    - Twinklies Packaging Jiggy: considers bringing Kazooie to the boiler plant into the logic. Intended logic requires turbo trainers. Other logics require turbo trainers if doing it as BK is in logic.
    - Floor 2 to Floor 3: checks for the flight pad if using the washing machine for the flight pad switch. Hard tricks and glitches logic can damage boost as the washing machine to the floor 4 warp pad then escape as BK with springy step shoes.
    - Boggy Jiggy: sliding into the water as you poop a clockwork for invincibility is in glitched logic.
    - Hot Pool Jinjo: same as above.
    - HFP Trebleclef: if you climb Icicle Grotto as Banjo-Kazooie, it will require moves for you to be able to cross the last gaps on the icicles. Also, the clockwork shot in tricks and glitches logics now require egg aim.
  - Open Backdoor YAML Option
    - Makes side entrances easier to tranverse...if you got the right moves.
  - Kill banjo if you get stuck using L+R+C Down (Doesn't trigger deathlink)
  - D-pad right will show which level as on which entrance.

# 3.4.1-beta
  - Logic Fixes:
    - Dilberta Jiggy moved to MT region.
  - Additional fixes for Instant Transformation

# 3.4-beta
 - Hints show the entrance to a level if loading zones are randomized
 - Fixed the ice key that despawns if you get the mega glowbo first
 - Grunty's Industries -> Grunty Industries
 - exceeding_items_filler option removed
   - The generation now works as if this action is always active
   - Filler items are now useful instead of normal
 - Cheato pages: if Cheato rewards are not randomized, they are always a normal item
 - Logic fixes:
   - TDL Entrance Jinjo: removed beak buster to enter the alcove in easy tricks logic
   - CCL Cheese Wedge Note: in tricks and glitches logic, can be gotten with just climb
   - Fixed Cauldron Keep's broken entrance in logic
 - *Experimental: Hold L before entering a loading screen to transform as Mumbo
    - Only if you have logical access to Mumbo and Mumbo unlocked for a world.
    - Hold L again to transform back to Banjo
    - Enter Mumbo's hut will transform you back to Banjo to avoid Softlocking
 - *Experimental: Hold R before entering a loading screen to tranform into Humba transformation
    - Only if you have logical access to Humba and Humba is unlocked for a world.
    - Hold R again to transform back to Banjo

# 3.3.3-beta
 - If you choose to have 1 silo open, your first silo will now always lead to the first level (unless Mayahem Temple is your first level. In which case, The silo is randomly selected).
 - Logic Fixes:
   - Prison Compound Cheato Page: For beginner logic, you need tall jump to jump from the water to the platforms.
   - Prison Compound Jiggy: For beginner logic, you need tall jump to jump from the water to the platforms.
   - MT Pillars Jiggy: For beginner logic, you need tall jump to jump from the water to the platforms, if going through the top of Prison Compound.
   - GGM Entrance Glowbo: for advanced and glitched logic, can be gotten with a clockwork.
   - Back-left Fuel Depot Note: for advanced and glitched logic, can be gotten with a clockwork.
   - TDL to Wasteland: fixed the broken transition.
   - Hot Waterfall Jinjo: removed the damage boost from normal logic.
   - Sack Race Note: removed Leg Spring + (Wing Whack or glide) from normal logic.
   - Trash Can Jiggy and Jinjo: Added Leg Spring + Wing Whack as an option to reach the Trash Can, in advanced and glitched logic.
   - Defeating Hag 1: beginner and normal logic get a 2nd type of egg to help with damaging.
  - Logic names are now: Intended / Easy Tricks / Hard Tricks / Glitches

# 3.3.2-beta
 - Fix Skivvy Jiggy
 - Fix Open Silos if BK Moves is not randomized.
 - Fix Canary Mary Cutscene (also made CCL Transitioning Faster)
 - Fix TDL Train Station softlock

# 3.3.1-beta
 - Logic fixes:
   - JRL to Cliff Top: removed transition if randomized.
   - Quagmire to Cauldron Keep: Now goes by the entrance first.

# 3.3-beta
- Open Silo Option
 - Choice between:
   - Opening 0 IoH silos. Note this does not apply if you are randomizing BK moves and Worlds.
   - Open 1 Random Silo. Note that if randomizing BK moves and Worlds, this will go to your first world.
   - Open All Silos.
- Randomize World Entrance loading zones
 - This also includes Cauldron Keep's entrance
 - Grunty Industries and Cauldron Keep cannot appear your first loading zone.
- Deathlink now works under water and in toxic caves, and kills much faster.
- Implement Inventory Items from Item Pool
- Readme update
- Added the rest of the general Archipelago settings in the yaml
- Renamings:
  - Note and doubloon locations: remade the numbering so that reading the names is more fluid.
  - Tall jump -> Tall Jump
- Logic fixes:
  - Targitzan Jiggy: Ice Eggs + Beak Bayonet is one way to do the boss fight. Also, now checking for suitable eggs in advanced and glitched logic.
  - Bovina jiggy: Beak Bombs are back in advanced and glitched logic, after being accidentally removed many versions ago.
  - Defeating Old King Coal: Beak Buster removed as an attack for advanced and glitched logic.
  - Flooded Caves jiggy: removed impossible jumps. Also, advanced and glitched logic can shoot a clockwork to the jiggy.
  - Water Storage Cheato page: checks for accesss to split up pads if doing the leg spring dive glitch.
  - Dive of Death notes: for normal logic, requires dive or tall jump.
  - JRL Pipe Honeycomb: the clockwork shot is now in the glitched logic. You can reach the spot for the shot with solo Kazooie, in advanced and glitched logic.
  - Seeweed Sanctum jinjo: in normal logic: you can get the jinjo with flap flip + beak buster. Every logic except beginner: pack whack + grip grab is one way to do it.
  - TDL Right Train Station Note: T-rex no longer part of beginner logic. All other logics can get it with split up, turbo trainers or springy step shoes. Advanced and glitched logic can get it with a clockwork shot.
  - TDL Entrance Jinjo: for normal logic, requires flutter, air rat-a-tat rap, split up, or beak buster to reach the alcove if you can't fly in. All logics except beginner: split up can be used to poop a grenade on the switch.
  - TDL Train Switch: can be pressed with split up.
  - River Passage Honeycomb: You can use split up for it, if not on beginner logic.
  - Roar Cage notes: if not on beginner logic, you can use split up.
  - GI Trebleclef: using the flight pad is now in logic.
  - Mega-Glowbo: you can use flutter or air rat-a-tat rap to reach the mega-glowbo, if not on beginner logic.
  - CCL Entrance Jinjo: Can be gotten with split up + flight pad, if not on beginner logic.
  - Mingy Jongo Jiggy: Removed clockwork eggs and roll for beginner and normal logic, due to their difficulty.
  - CCL Indoors Glowbo: Removed elevation requirement for logics other than beginner, since you can reach the footrace track from the red skull.


# 3.2-beta
 - Logic fixes:
  - Atlantis access: fixed dumb mistake that required egg aim or third person egg shooting to reach atlantis, in beginner and normal logic.
  - JRL Pipe Honeycomb: if using leg spring, wing whack is no longer required. Advanced and glitched logic can shoot a clockwork to the honeycomb.
  - HFP to JRL: Shack Pack can be used to dive in the pool, in HFP.
  - Icicle Grotto Jinjo: needs tall jump for beginner logic.
  - HFP: the access to lower icy side and the top of HFP now use the same logic, since there's the tunnel behind the icy side train switch that was overlooked. Also, split up is no longer an option to reach the top of HFP in beginner logic.
  - Volcano honeycomb: if going through icicle grotto from the bottom, requires talon trot. Added missing tall jump requirement for beginner logic.
  - Icy side Pillar Cheato page: added talon trot requirement if going through icicle grotto as BK, in advanced and glitched logic.
  - Sack Race Note: reworked logic.
  - Central Cavern jinjo: can be gotten with the bee.
  - Pot of Gold honeycomb: can be gotten with the bee.
 - Framework Core modification
  - 2 RAM addresses are checked on every frame due to Chuffy.
  - This Fixes Train Station giving free Checks and game stopped sending Checks.
 - More Gruntilda Insults on Deathlink
 - Custom Jiggy amounts, Minimium for all worlds to open is 1 Jiggy.
 - Minor change with Roysten Flags

# 3.1.2-beta
 - Fix Blue Eggs getting removed permanently

# 3.1.1-beta
 - Fix Cheato page on Second Floor

# 3.1-beta
 - Lots of bug fixes:
  - Fix Crashing when removing associated Egg near Silo + Crashing transitioning maps
  - Fix Heggy
  - Fix Honeycomb CCL Location
  - Fix Cutscene Jiggies
  - Fix HAG1 Complete
  - Fix Totals Menu + Unlocked Worlds Menu
  - Fix Train Switches
  - Modify Checking of Transitioning to different Maps. (found in-game bug that we had to workaround)
 - Jingaling skip is no longer an option. Its part of the randomizer
 - If using Refill cheat, it will double your eggs and feather
 - Must return to Banjo's House for handing in all Mumbo Tokens to complete the game.
 - Enable all Totals Screen

# 3.0-beta
  - Starting attack: If not on beginner logic, wonderwing can be your starting attack.
  - Wonderwing challenge: if you can have wonderwing as your starting attack, you will get it!
  - Logic fixes:
    - Jade Snake Grove jinjo: in glitched logic, you can kick the jinjo as the golden goliath.
    - Treasure Chamber jiggy: you can shoot any egg, including clockworks, at the snake heads.
    - Old King Coal: checks for different attacks based on logic. Beginners need eggs, normal needs a mobile attack, others need any working attack.
    - GGM Entrance Honeycomb: you can get it by fluttering as you enter the level.
    - Prospector honeycomb: If not on beginner logic, you don't need any moves to reach the boulder.
    - GGM Mumbo Notes: Advanced and glitched logic can get the notes with beak buster.
    - Generator Cavern jiggy: normal logic can jump from the sign to the ladder with solo Banjo, and can reach the jiggy with leg spring + fire eggs. So can advanced and glitched logics, but without fire eggs.
    - Blubber jinjo: Beginner logic can get it with flap flip. All other logics can also get it with leg spring.
    - TDL treble clef: glitched logic can get it with ground rat-a-tat rap.
    - TDL Entrance Jinjo: talon trot can be gotten from shoes, if not on beginner logic.
    - Lava side train switch: solo Kazooie can hit it with leg spring or tall jump, if not on beginner logic.
    - Icy side train switch: checks that lower icy side is reachable.
    - Boggy Igloo collectibles: reworked logic.
    - HFP ice cubes: reworked logic for most of them. Can be broken with beak buster, wonderwing and the snowball. Also takes into account the fact that clockworks are not considered as explosives in beginner logic.
    - CCL Humba Jinjo: can be gotten with leg spring, if not on beginner logic. Advanced and glitched logic can get it with a clockwork shot.
    - Sack Race Exit Note: beginner logic needs some sort of elevation. The others don't.
    - Cheese Wedge note: the item is now mapped to the correct logic.
    - Top of HFP access: normal logic no longer can do it with split up.
  - Lua Framework rework:
   - Seperates items to become their own functions and send to BTClient only the items on a given map (so not everything all the time!)
   - Each item is mapped to a Banjo-Tooie Map on the Lua. So only a given map it will check for those flags instead of everything.
   - Better code handling between map transitions
   - Resolves outstanding bugs such as:
    - Wrong Item Count. This is now accurate when collecting an item
    - Train switches automatically getting switched. Fixed
    - Roysten not behind boulder. Fixed
    - Treble Clef at JV is still there after loading an existing game. Fixed
    - Exploiting Fire Eggs in Plateau. Fixed
    - WW Split up pads buggy. Fixed
    - Dragon Brothers not giving jiggy. Fixed
    - Heggy hardlocking. Fixed
   - Baby T-Rex Roar is now in the Pool
   - Smooth Banjo is fixed when entering a new map
   - Remove Jinjo forbid options from Lua
   - Change disable Text Overlay YAML Option to Enable Text Overlay
   - Ability to change Text Overlay Colour
   - If Deathlink enabled, Gruntilda will now mock you if you die in the BTClient for all to see!

# 2.1.4-beta
  - Logic fixes:
    - TDL Boulder Cheato Page: Added missing Grip Grab. Advanced and Glitched logic can fall into the alcove from the top.
    - Lower icy side collectibles: reworked the logic on how lower icy side can be reached.
    - Top of HFP collectibles: if not on beginner logic, the top of HFP can be reached with the snowball.
    - Ice Cube notes: no longer consider ice eggs or beak buster as part of the logic. And they consider Kazooie moves. And they consider the snowball.
    - Any check where any attack move would be enough: now takes progressive moves into consideration.
    - wind tunnel Jinjo: for the clockwork shot, checks if you can reach the top of HFP.

# 2.1.3-beta
  - The logic code has been completely rewritten to make it more readable. The only functional changes to the logic are listed below.
  - Name changes:
    - BH: Goggles Amaze-o-Gaze -> IoH: Amaze-o-Gaze Goggles
    - Egg Shoot -> Third Person Egg Shooting
    - CCL Green Pool Glowbo -> CCL Outdoors Pool Glowbo
    - CCL Central Cavern Glowbo -> CCL Indoors Pool Glowbo
  - Logic fixes:
   - Fuel Depot notes: Now have actual logic.
   - Prospector notes: can be gotten with no moves, if not on beginner logic.
   - GGM Entrance Cheato Page: For normal logic, requires tall jump if jumping from the rope with rat-a-tat rap.
   - Generator Cavern jiggy: For normal logic, removed split up for a light source. Oops.
   - Cactus of Strength Jinjo: Can be reached with leg spring. Also, jumping from the gondola platform can now be done with air rat-a-tat.
   - Hoop Hurry Jiggy: added move requirements to reach the pump room. Beginner logic gets turbo trainers.
   - Balloon Burst Jiggy: added move requirements to reach the pump room.
   - JRL Alcove Jinjo: if doing the slope abuse, it now requires flutter or air rat-a-tat rap.
   - Terry's Kids Jiggy: Tall jump is now a hard requirement, due to the egg in the Oogle cave.
   - GI Floor 2 Cheato page: Added logic to account for BK moves and glitched logic.
   - GI Floor 4 Jinjo: requires wing whack or the ability to shoot eggs if you do not have access to the roof. It also takes reaching the back of the building by leaving floor 2.
   - Volcano Jiggy: now requires a way to cross the gaps in the volcano.
   - Lava Side Train Switch: removed impossible jumps from the logic.
   - Trash Can Jiggy: reworked the logic.
   - Trash Can Jinjo: reworked logic.
   - CCL Central Cavern glowbo: changed the logic to be more permissive.
   - Central Cavern jinjo: If using the springy step shoes, can now be done with split up, flutter or air rat-a-tat rap.
   - GI Outside to GI Floor 3: now considers leaving floor 2 to reach the back of the building.
   - Floor 1 to Floor 3: The Leg Spring from the treble clef to the window with the flight pad is now in advanced and glitched logics.
   - Cauldron Keep Access: fixed glitched logic by taking BK moves into account. The other logics also no longer require Climb.

# 2.1.2-beta
 - Logic fixes:
   - Pot of gold: fixed logic for new BK moves.
   - Targitzan jiggy: requires blue eggs, fire eggs or grenade eggs, in beginner and normal logic.
   - GGM Entrance Cheato page: Getting it with the detonator is no longer in logic, due to its difficulty.
   - CCL Dippy Pool Notes: can be gotten with shack pack, if not on beginner logic.
   - fix in Region access for Progressive Items
 - Fixed missing states Glitch Logic for Pot of Gold
 - Banjo-Tooie AP will now check Generated, BTClient and Lua Versions. If any mismatch, it will let you know and no longer run.

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
- change wording for forbid certain AP items on Jinjo Families
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
