Preset = str
Trick = str
Logic = str

tricks: dict[Preset, dict[Trick, Logic]] = {
	"Easy Tricks": {
		"Beak Barge Jump": "BeakBarge", # Using Beak Barge off of a ledge can give extra distance.
		"Beak Buster Fall": "BeakBuster", # The hop after using Beak Buster prevents fall damage.
		"Beak Buster Jump": "BeakBuster", # Beak Buster gives a little extra height.
		"Bill Drill Jump": "BillDrill", # Bill Drill's hop at the end gives a little extra height. It can also protect from certain hazards like Dragunda.
		"Breegull Bash Fall": "BreegullBash", # You won't take fall damage during the entire animation of Breegull Bash.
		"Air Rat-A-Tat Grab": "AirRatatatRap", # Air Rat a Rat Rap can grab things just out of reach.
		"Breegull Bash Grab": "BreegullBash", # Breegull Bash can grab things just out of reach.
		"Dragunda Sidle": "true", # With some Dragunda pools, you can run against the wall to avoid damage.
		"Easy Jumps": "true", # Using various combinations of moves, you can reach new areas without intended moves.
		"GI: Extra Loggo Moves": "BreegullBash or BeakBarge or PackWhack", # Some moves other than Bill Drill can unclog Loggo.
		"Ground Rat-a-tat Rap Fall": "GroundRatatatRap", # Using Ground Rat-a-tat Rap off of a ledge can prevent fall damage.
		"Ground Rat-a-tat Rap Jump": "GroundRatatatRap", # Using Ground Rat-a-tat Rap off of a ledge can give extra distance.
		"Pack Whack Fall": "PackWhack", # Pack Whack can slightly delay fall damage.
		"Pack Whack Jump": "PackWhack", # You can always jump while using Pack Whack. Using Pack Whack off of a ledge allows a second use.
		"Pack Whack Slope Jump": "PackWhack", # You Can repeatedly jump out of Pack Whack on a slope to
		"Roll Jump": "Roll", # Rolling off a ledge lets you jump in the air during the animation.
		"Sack Pack Air Jump": "SackPack", # You can jump while hopping around. Ending Sack Pack also gives a little distance.
		"Sack Pack Fall": "SackPack", # Using Sack Pack off of a ledge allows you to prevent fall damage during the animation.
		"Shack Pack Air Jump": "ShackPack", # Walking off of a ledge allows you to jump in the air.
		"Shack Pack Fall": "ShackPack", # Shack Pack can fall a little farther before taking damage. You can also end the move in the air for increased distance.
		"Snooze Pack Fall": "SnoozePack", # Using Snooze Pack off of a ledge prevents fall damage.
		"Taxi Pack Fall": "TaxiPack", # Using Taxi Pack off of a ledge prevents fall damage during the animation. You can also end the move in the air for increased distance
		"Slope Jump": "true", # Going Up slopes without talon trot.
		"Dive Skip": "true", # Skipping Dive by either entering a loading zone or forcing your way into a tunnel.
		"Glide Extension": "true", # Alternating between Glide and either Flutter or Wing Whack makes Kazooie lose height slower.
		"Rooms With Limited Lighting": "true", # Do dark rooms with unintended, limited forms of lighting.
		"Extra Third Person Egg Shooting": "ThirdPersonEggShooting", # Use Third Person Egg Shooting in places where Egg Aim would be intended to be used.
        "Mumbo Wand Fall": "true", # Using Mumbo's Wand to fall without taking damage.
        "Glide In CCL": "Glide" # With how open Cloud Cuckooland is, glide can allow you to reach distant places without flight.
	},
	"Easy Tedious Tricks": {
		"Beak Bomb Tricks": "BeakBomb", # Beak Bomb can be used in unintended ways to reach new areas.
		"Damage Boost": "true", # Taking damage can allow access to new areas.
		"Damage Boost Jump": "true", # Taking damage gives a little extra height.
		"Death Warp": "true", # You can accomplish a task and then die (in game) to keep what you did.
		"Easy Tedious Jumps": "true", # Tedious version of "Easy Jumps".
		"Extra Clockwork Usage": "ClockworkKazooieEggs", # You can use Clockwork Kazooie Eggs to retrieve items out of reach or activate things remotely.
		"Fall Damage": "true", # Taking fall damage can allow access to new areas.
		"GI Quality Control Vent As Banjo": "true", # Banjo can press the button for free, but swapping back and forth can be tedious.
		"GI Guarded Jiggy Without Fighting": "Glide and LegSpring", # You can grab the Jiggy without defeating the Tintops.
		"Instant Transform Trick": "true", # Abusing Instant Transform can allow you to get to new areas.
		"Talon Trot Smuggle": "true", # Turbo Trainers, Springy Step Shoes and Claw Clamber Boots force a Talon Trot that can be held.
		"Talon Trot Smuggle Cross World": "true", # Allows smuggling Talon Trot between worlds.
		"Wonderwing Damage Boost": "Wonderwing", # Dragunda looks like he hurts you in Wonderwing, but you don't take damage.
		"Wonderwing Fall": "Wonderwing", # Wonderwing prevents fall damage.
		"Wonderwing Jump": "Wonderwing", # Jumping while using Wonderwing has a normal height even without Tall Jump.
		"Bovina With Beak Bomb": "BeakBomb", # Beak Bomb the flies to kill them.
		"Tight Timers": "true" # Beating timers (minigames, timed switches) in sub-optimal conditions.
	},
	"Easy Glitches": {
		"Air Rat-a-tat Rap Clip": "AirRatatatRap", # Air Rat-a-tat Rap can interact with things just beyond geometry.
		"EggBarge": """
			BeakBarge
			and ThirdPersonEggShooting
			and LinearEggs
		""", # After shooting a non-Clockwork egg forward, immediately Beak Barge to grab things just beyond geometry.
		"Beak Barge Clip": "BeakBarge", # Getting stuff through geometry with Beak Barge.
		"Ground Rat-A-Tat Clip": "GroundRatatatRap", # Getting stuff through geometry with Ground Rat-A-Tat.
		"Breegull Bash Clip": "BreegullBash", # Breegull Bash can interact with things just beyond geometry.
		"Free Shock Spring Pad": "Wonderwing", # Shock Spring Pads near ledges can be used without Tall Jump by faking of a jump off the ledge.
		"Taxi Pack Clip": "TaxiPack", # Taxi Pack can interact with things just beyond geometry.
		"Pack Whack Clip": "TaxiPack", # Pack Whack can interact with things just beyond geometry.
		"Golden Goliath Clip": "true", # Golden Goliath can interact with things just beyond geometry.
		"Glitched Invincibility": "true", # Being invincible through glitched means.
		"Leg Spring Dive": "LegSpring", # Holding A while doing a Leg Spring lets you sink underwater.
	},
	"Hard Tricks": {
		"Hard Jumps": "true", # Harder version of "Easy Jumps".
		"Slide Jump": "true", # Turning around suddenly plays a sliding animation. Doing this off of a ledge allows you to jump in the air.
		"Flap Flip Slide Extension": "FlapFlip", # Flap Flip off a ledge with neutral joystick. During ascent, hold a direction to gain a little extra distance.
		"Extra Attacks": "true", # Using worse attacks on enemies becomes in logic.
		"Tightrope Walk": "true", # Walking accross narrow platforms, such as the Witchyworld Gondola Wire.
		"Rhythmic Swimming": "true", # As BK underwater, hold A+B and quickly release and repress B after each stroke to swim slightly faster.
        "Terry Without Egg Aim": "true", # Going on the rim of Terry's neat and use third person egg shooting to damage Terry.
        "Glide Wall Climb": "Glide" #Gliding against certain slanted walls can allow you to gain height.
	},
	"Hard Tedious Tricks": {
		"Hard Tedious Jumps": "true", # Tedious version of "Hard Jumps".
		"Bovina With Flap Flip": "FlapFlip and BeakBuster",
		"Rooms In The Dark": "true", # Do dark rooms with no lighting.
        "Bonfire Cavern Flame Sidle": "true", # The side of torches is safe in the bonfire cavern, so you can just go around them.
        "Dodging Stompadon": "true" # Doing an abrupt direction change as Stompadon tries to crush you makes you able to dodge the foot.
	},
	"Hard Glitches": {
		"Beak Bomb Clips": "BeakBomb", # Beak bomb lets you go through gaps in doors.
		"Clip Past Pine Grove Boulder": "true", # You can swim in the top-right corner of the boulder to clip through it backwards.
		"Clockwork Warp": "ClockworkKazooieEggs and EggAim",
		"Clockwork Shot Through Geometry": "ClockworkKazooieEggs and EggUse",
	},
	"Frame Perfect": {
		"Talon Trot Slide Jump": "true", # Landing in Talon Trot plays a sliding animation. Doing this off of a ledge allows a frame perfect jump in the air.
		"Sack Pack Ending Jump": "SackPack", # Exiting Sack Pack allows a frame perfect jump in the air.
	},
}
