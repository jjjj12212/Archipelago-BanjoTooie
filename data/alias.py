Alias = str
Logic = str

alias: dict[Alias, Logic] = {
	"Notes": "count(NoteNest)*5 + count(BassClef)*10 + count(TrebleClef)*20",
	"AnyEggs": "BlueEggs or FireEggs or GrenadeEggs or IceEggs or ClockworkKazooieEggs",
	"AnyAttack": "GroundRatatatRap or AirRatatatRap or Roll or BeakBarge or BeakBuster or Wonderwing",
	"EggUse": "EggAim or ThirdPersonEggShooting",
	"BillDrill": "BeakBuster and BillDrill",
	"BreegullBash": "GroundRatatatRap and BreegullBash",
	"BeakBayonet": "BreegullBlaster and BeakBayonet",
	"DragonBreath": "GroundRatatatRap and (IoHDragonTransform or HumbaDragon and InstantTransform == 'no_logic')"
}
