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
		"Breegull Bash Grab": "BreegullBash", # Breegull Bash can grab things just out of reach.
		"Dragunda Sidle": "true", # With some Dragunda pools, you can run against the wall to avoid damage.
		"Easy Jumps": "true", # Using various combinations of moves, you can reach new areas without intended moves.
		"GI: Extra Loggo Moves": "BreegullBash or BeakBarge or PackWhack", # Some moves other than Bill Drill can unclog Loggo.
		"Ground Rat-a-tat Rap Fall": "GroundRatatatRap", # Using Ground Rat-a-tat Rap off of a ledge can prevent fall damage.
		"Ground Rat-a-tat Rap Jump": "GroundRatatatRap", # Using Ground Rat-a-tat Rap off of a ledge can give extra distance.
		"Pack Whack Fall": "PackWhack", # Pack Whack can slightly delay fall damage.
		"Pack Whack Jump": "PackWhack", # You can always jump while using Pack Whack. Using Pack Whack off of a ledge allows a second use.
		"Roll Jump": "Roll", # Rolling off a ledge lets you jump in the air during the animation.
		"Sack Pack Air Jump": "SackPack", # You can jump while hopping around. Ending Sack Pack also gives a little distance.
		"Sack Pack Fall": "SackPack", # Using Sack Pack off of a ledge allows you to prevent fall damage during the animation.
		"Shack Pack Air Jump": "ShackPack", # Walking off of a ledge allows you to jump in the air.
		"Shack Pack Fall": "ShackPack", # Shack Pack can fall a little farther before taking damage. You can also end the move in the air for increased distance.
		"Snooze Pack Fall": "SnoozePack", # Using Snooze Pack off of a ledge prevents fall damage.
		"Taxi Pack Fall": "TaxiPack", # Using Taxi Pack off of a ledge prevents fall damage during the animation. You can also end the move in the air for increased distance
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
	},
	"Easy Glitches": {
		"Air Rat-a-tat Rap Clip": "AirRatatatRap", # Air Rat-a-tat Rap can interact with things just beyond geometry.
		"Beak Barge Clip": """
			BeakBarge
			and ThirdPersonEggShooting
			and exclude(AnyEggs, ClockworkKazooieEggs)
		""", # After shooting a non-Clockwork egg forward, immediately Beak Barge to grab things just beyond geometry.
		"Breegull Bash Clip": "BreegullBash", # Breegull Bash can interact with things just beyond geometry.
		"Free Shock Spring Pad": "Wonderwing", # Shock Spring Pads near ledges can be used without Tall Jump by faking of a jump off the ledge.
	},
	"Hard Tricks": {
		"Hard Jumps": "true", # Harder version of "Easy Jumps".
		"Slide Jump": "true", # Turning around suddenly plays a sliding animation. Doing this off of a ledge allows you to jump in the air.
		"Flap Flip Slide Extension": "FlapFlip", # Flap Flip off a ledge with neutral joystick. During ascent, hold a direction to gain a little extra distance.
	},
	"Hard Tedious Tricks": {
		"Hard Tedious Jumps": "true", # Tedious version of "Hard Jumps".
	},
	"Hard Glitches": {

	},
	"Frame Perfect": {
		"Talon Trot Slide Jump": "true", # Landing in Talon Trot plays a sliding animation. Doing this off of a ledge allows a frame perfect jump in the air.
		"Sack Pack Ending Jump": "SackPack", # Exiting Sack Pack allows a frame perfect jump in the air.
	},
}
