// Banjo Tooie Luna64 Connector Script
// Created by Mike Jackson (jjjj12212)
/*
    Recommended PJ64 Settings:
    Options -> Conigurations:
        Pause Emulation when not active: unchecked
        Plugins: GlideN64
        Config: Rando Tooie
            Memory size: 8MB

    Graphics -> Frame Buffer
        Emulate Frame Buffer
        frame buffer swap on Vertical Interrupt
        everything else off / never

*/
var SCRIPT_VERSION = 5
var BT_VERSION = "4.11.6"
var PLAYER = ""
var SEED = 0

var BT_SOCK = null
var init = false
var BUFFER = "";

var STATE_OK = "Ok"
var STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
var STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
var STATE_UNINITIALIZED = "Uninitialized"
var PREV_STATE = ""
var CUR_STATE =  STATE_UNINITIALIZED
var FRAME = 0
var VERROR = false
var CLIENT_VERSION = false
var GOAL_PRINTED = false


var DEBUG = false
var DEBUG_SILO = false
var DEBUG_JIGGY = false
var DEBUG_TREBLE = false
var DEBUG_NOTES = false
var DEBUG_HONEY = false
var DEBUG_HEALTHUPGRADE = false
var DEBUG_GLOWBO = false
var DEBUG_ROYSTEN = false
var DEBUG_CHUFFY = false
var DEBUG_STOPNSWAP = false
var DEBUG_STATION = false
var DEBUG_PAGES = false
var DEBUG_CHEATO = false
var DEBUG_JINJO = false
var DEBUG_HONEYCOMB = false
var DEBUG_DOUBLOON = false
var DEBUG_AMAZE = false
var DEBUG_NESTS = false
var DEBUG_SIGNPOSTS = false
var DEBUG_WARPSILOS = false
var DEBUG_WARPPADS = false
var DEBUG_BOGGY_KIDS = false
var DEBUG_ALIEN_KIDS = false
var DEBUG_SKIVVIES = false
var DEBUG_MRFIT = false


var DEBUGLVL2 = false
var DEBUGLVL3 = false
var AP_TIMEOUT_COUNTER = 0

var TOKEN_ANNOUNCE = false;
var SNEAK = false;

var SILO_MESSAGE = "";
var SEND_SILO_MSG = true;

////////////// MAP VARS ////////////-
var CURRENT_MAP = null;

////////////// TOTALS VARS //////////-
var TOTAL_HONEYCOMBS = 0;
var TOTAL_JIGGY = 0;
var TOTAL_MUMBO_TOKENS = 0;
var TOTAL_TREBLE = 0;
var TOTAL_PAGES = 0;
var TOTAL_DOUBLOONS = 0;
var TOTAL_NOTES = 0;
var TOTAL_HEALTHUPGRADE = 0;
var TOTAL_BTTICKETS = 0;
var TOTAL_GRRELICS = 0;
var TOTAL_BEANS = 0;

var WHITE_JINJO = 0;
var ORANGE_JINJO = 0;
var YELLOW_JINJO = 0;
var BROWN_JINJO = 0;
var GREEN_JINJO = 0;
var RED_JINJO = 0;
var BLUE_JINJO = 0;
var PURPLE_JINJO = 0;
var BLACK_JINJO = 0;

var TTRAPS = 0;
var STRAPS = 0;
var TRTRAPS = 0;
var SQTRAPS = 0;
var TITRAPS = 0;

var EGGNEST = 0;
var FEATHERNEST = 0;
var GOLDNEST = 0;

var ENABLE_AP_CHUFFY = false;

var receive_map = { } // [ap_id] = item_id; Required for Async Items


////////////// SKIP VARS ////////////
var OPEN_HAG1 = false;

////////////// GOAL TYPE VARS ////////////
var GOAL_TYPE = null;
var MGH_LENGTH = null;
var BH_LENGTH = null;
var JFR_LENGTH = null;
var TH_LENGTH = null;

//////////////- DEATH LINK //////////////////////
var DEATH_LINK_TRIGGERED = false;
var DEATH_LINK = false

//////////////- TAG LINK ////////////////////////
var TAG_LINK_TRIGGERED = false
var TAG_LINK = false

//////////////// IOH SILO VARS /////////////
var OPEN_SILO = "NONE"

//////////////// DIALOG CHARACTER ////////////////
var DIALOG_CHARACTER = 110

//////////////// ENCOURAGEMENT MESSAGES ////////////////
var ENCOURAGEMENT = [
    " GUH-HUH!",
    " BREEE!",
    " EEKUM BOKUM!",
    " YEEHAW!",
    " JINJOO!!",
    " WAHEY!!!",
    " ROOOOO!!!",
    " OOMANAKA!!!"
]

var DEATH_MESSAGES = [
    "Did you hear that lovely clack,\nMy broomstick gave you such a whack!",
    "AAAH! I see it makes you sad,\nTo know your skills are really bad!",
    "I hit that bird right on the beak,\nLet it be the end of her cheek!",
    "My fiery blast you just tasted,\nGrunty's spells on you are wasted!",
    "Hopeless bear runs to and fro,\nBut takes a whack for being so slow!",
    "So I got you there once more,\nI knew your skills were very poor!",
    "Simply put I'm rather proud,\nYour yelps and screams I heard quite loud!",
    "Grunty's fireball you did kiss,\nYou're so slow I can hardly miss!",
    "In this world you breathe your last,\nNow your friends had better think fast!",
    "This is fun it's quite a treat,\nTo see you suffer in defeat",
    "That death just now, I saw coming,\nYour skill issues are rather stunning!",
    "Seeing this pathetic display,\nIs serotonin in my day",
    "What a selfish thing to do,\nYour friends just died because of you!",
    "You tried something rather stupid,\nI hope no one will try what you did",
    "I see you're having trouble with this seed,\nit's too bad you never learned how to read.",
    "You'll label that one unfair, but I found that beat was rare.",
    "You were not prepared for trouble, so now my minions will be working on the double.",
    "Seeing you trip and fall is rather funny, I get to watch you run out of honey.",
    "Welcome bozos to death's door... \nWait, hold on, you're back for more?",
    "Can't believe you died at this stage, \nWhy don't you look elsewhere on your tracker page!"
]

var ITEM_TABLE = {}; // reverses ROM_ITEM so the key is the Item
var ROM_ITEM_TABLE = [
  "AP_ITEM_GGRAB",
  "AP_ITEM_BBLASTER",
  "AP_ITEM_EGGAIM",
  "AP_ITEM_BDRILL",
  "AP_ITEM_BBAYONET",
  "AP_ITEM_AIREAIM",
  "AP_ITEM_SPLITUP",
  "AP_ITEM_WWHACK",
  "AP_ITEM_TTORP",
  "AP_ITEM_AUQAIM",
  "AP_ITEM_SHPACK",
  "AP_ITEM_GLIDE",
  "AP_ITEM_SNPACK",
  "AP_ITEM_LSPRING",
  "AP_ITEM_CLAWBTS",
  "AP_ITEM_SPRINGB",
  "AP_ITEM_TAXPACK",
  "AP_ITEM_HATCH",
  "AP_ITEM_PACKWH",
  "AP_ITEM_SAPACK",
  "AP_ITEM_FEGGS",
  "AP_ITEM_GEGGS",
  "AP_ITEM_CEGGS",
  "AP_ITEM_IEGGS",
  "AP_ITEM_FSWIM",
  "AP_ITEM_DAIR",
  "AP_ITEM_BBASH",
  "AP_ITEM_AMAZEOGAZE",
  "AP_ITEM_ROAR",
  "AP_ITEM_DIVE",
  "AP_ITEM_FPAD",
  "AP_ITEM_GRAT",
  "AP_ITEM_ROLL",
  "AP_ITEM_ARAT",
  "AP_ITEM_BBARGE",
  "AP_ITEM_TJUMP",
  "AP_ITEM_FLUTTER",
  "AP_ITEM_FFLIP",
  "AP_ITEM_CLIMB",
  "AP_ITEM_BEGGS",
  "AP_ITEM_TTROT",
  "AP_ITEM_BBUST",
  "AP_ITEM_WWING",
  "AP_ITEM_SSTRIDE",
  "AP_ITEM_TTRAIN",
  "AP_ITEM_BBOMB",
  "AP_ITEM_EGGSHOOT",
  "AP_ITEM_PAGES",
  "AP_ITEM_HONEY",
  "AP_ITEM_WJINJO",
  "AP_ITEM_OJINJO",
  "AP_ITEM_YJINJO",
  "AP_ITEM_BRJINJO",
  "AP_ITEM_GJINJO",
  "AP_ITEM_RJINJO",
  "AP_ITEM_BLJINJO",
  "AP_ITEM_PJINJO",
  "AP_ITEM_BKJINJO",
  "AP_ITEM_DOUBLOON",
  "AP_ITEM_JIGGY",
  "AP_ITEM_TREBLE",
  "AP_ITEM_NOTE",
  "AP_ITEM_MUMBOTOKEN",
  "AP_ITEM_IKEY",
  "AP_ITEM_PMEGG",
  "AP_ITEM_BMEGG",
  "AP_ITEM_HEALTHUP",
  "AP_ITEM_HOMINGEGGS",
  "AP_ITEM_CHEATFEATHER",
  "AP_ITEM_CHEATEGG",
  "AP_ITEM_CHEATFALL",
  "AP_ITEM_CHEATHONEY",
  "AP_ITEM_CHEATJUKE",
  "AP_ITEM_MUMBOMT",
  "AP_ITEM_MUMBOGM",
  "AP_ITEM_MUMBOWW",
  "AP_ITEM_MUMBOJR",
  "AP_ITEM_MUMBOTD",
  "AP_ITEM_MUMBOGI",
  "AP_ITEM_MUMBOHP",
  "AP_ITEM_MUMBOCC",
  "AP_ITEM_MUMBOIH",
  "AP_ITEM_HUMBAMT",
  "AP_ITEM_HUMBAGM",
  "AP_ITEM_HUMBAWW",
  "AP_ITEM_HUMBAJR",
  "AP_ITEM_HUMBATD",
  "AP_ITEM_HUMBAGI",
  "AP_ITEM_HUMBAHP",
  "AP_ITEM_HUMBACC",
  "AP_ITEM_HUMBAIH",
  "AP_ITEM_TRAINSWIH",
  "AP_ITEM_TRAINSWTD",
  "AP_ITEM_TRAINSWGI",
  "AP_ITEM_TRAINSWHP1",
  "AP_ITEM_TRAINSWHP2",
  "AP_ITEM_TRAINSWWW",
  "AP_ITEM_CHUFFY",
  "AP_ITEM_GNEST",
  "AP_ITEM_ENEST",
  "AP_ITEM_FNEST",
  "AP_ITEM_MTA",
  "AP_ITEM_GGA",
  "AP_ITEM_WWA",
  "AP_ITEM_JRA",
  "AP_ITEM_TDA",
  "AP_ITEM_GIA",
  "AP_ITEM_HFA",
  "AP_ITEM_CCA",
  "AP_ITEM_CKA",
  "AP_ITEM_H1A",
  "AP_ITEM_WARPMT_HUMBA",
  "AP_ITEM_WARPMT_PRISON",
  "AP_ITEM_WARPMT_MUMBO",
  "AP_ITEM_WARPMT_ENTRANCE",
  "AP_ITEM_WARPMT_KICKBALL",
  "AP_ITEM_WARPGG_TRAIN",
  "AP_ITEM_WARPGG_CRUSHING",
  "AP_ITEM_WARPGG_HUMBA",
  "AP_ITEM_WARPGG_MUMBO",
  "AP_ITEM_WARPGG_ENTRANCE",
  "AP_ITEM_WARPWW_BIGTOP",
  "AP_ITEM_WARPWW_ENTRANCE",
  "AP_ITEM_WARPWW_MUMBO",
  "AP_ITEM_WARPWW_HUMBA",
  "AP_ITEM_WARPWW_SPACE",
  "AP_ITEM_WARPJR_LOCKERS",
  "AP_ITEM_WARPJR_BIGFISH",
  "AP_ITEM_WARPJR_SHIP",
  "AP_ITEM_WARPJR_ATLANTIS",
  "AP_ITEM_WARPJR_ENTRANCE",
  "AP_ITEM_WARPGI_MUMBO",
  "AP_ITEM_WARPGI_HUMBA",
  "AP_ITEM_WARPGI_ENTRANCE",
  "AP_ITEM_WARPGI_ROOF",
  "AP_ITEM_WARPGI_CRUSHER",
  "AP_ITEM_WARPTD_TOP",
  "AP_ITEM_WARPTD_HUMBA",
  "AP_ITEM_WARPTD_MUMBO",
  "AP_ITEM_WARPTD_STOMPING",
  "AP_ITEM_WARPTD_ENTRANCE",
  "AP_ITEM_WARPCC_ENTRANCE",
  "AP_ITEM_WARPCC_CENTER",
  "AP_ITEM_WARPHF_ICICLE",
  "AP_ITEM_WARPHF_HUMBA",
  "AP_ITEM_WARPHF_ICYUPPER",
  "AP_ITEM_WARPHF_LAVAUPPER",
  "AP_ITEM_WARPHF_ENTRANCE",
  "AP_ITEM_WARPCK_HAG1",
  "AP_ITEM_WARPCK_ENTRANCE",
  "AP_ITEM_SILO_JINJO_VILLAGE",
  "AP_ITEM_SILO_WOODED_HOLLOW",
  "AP_ITEM_SILO_PLATEAU",
  "AP_ITEM_SILO_PINE_GROVE",
  "AP_ITEM_SILO_CLIFF_TOP",
  "AP_ITEM_SILO_WASTELAND",
  "AP_ITEM_SILO_QUAGMIRE",
  "AP_ITEM_BTTICKET",
  "AP_ITEM_GRRELIC",
  "AP_ITEM_BEAN",
  "AP_ITEM_MAX",
];
for(var i=0; i < ROM_ITEM_TABLE.length; i++)
{
    ITEM_TABLE[ROM_ITEM_TABLE[i]] = i
}

var TRAP_TABLE = {};
var TRAPS = [
    "AP_TRAP_TRIP",
    "AP_TRAP_SLIP",
    "AP_TRAP_MISFIRE",
    "AP_TRAP_SQUISH",
    "AP_TRAP_TIP"
]

var DIALOG_CHARACTER_TABLE = {}
var DIALOG_KEY_TABLE = [
    "ICON_GLOWBO",
    "ICON_JIGGY",
    "ICON_HONEYCOMB",
    "ICON_SUB",
    "ICON_WASHER",
    "ICON_BANJO",
    "ICON_KAZOOIE",
    "ICON_BOTTLES",
    "ICON_MUMBO",
    "ICON_JINJO_YELLOW",
    "ICON_JINJO_GREEN", // 10
    "ICON_JINJO_BLUE",
    "ICON_JINJO_PURPLE",
    "ICON_JINJO_ORANGE",
    "ICON_BEEHIVE",
    "ICON_GRUNTY",
    "ICON_ZUBBA",
    "ICON_JAMJARS",
    "ICON_BOVINA",
    "ICON_MINJO_WHITE",
    "ICON_MINJO_ORANGE", //20
    "ICON_MINJO_YELLOW",
    "ICON_MINJO_BROWN",
    "ICON_UNOGOPAZ",
    "ICON_CHIEF_BLOATAZIN",
    "ICON_DILBERTA",
    "ICON_STONIES1",
    "ICON_CANARY_MARY",
    "ICON_CHEATO",
    "ICON_GOBI",
    "ICON_DINO_KID1", //30
    "ICON_MR_PATCH",
    "ICON_MOGGY",
    "ICON_SOGGY",
    "ICON_GROGGY",
    "ICON_MRS_BOGGY",
    "ICON_PROSPECTOR",
    "ICON_HUMBA",
    "ICON_UFO",
    "ICON_OLD_KING_COAL",
    "ICON_SSSLUMBER", //40
    "ICON_BOGGY",
    "ICON_BIG_AL",
    "ICON_SALTY_JOE",
    "ICON_CONGA",
    "ICON_PAWNO",
    "ICON_TIPTUP",
    "ICON_JOLLY",
    "ICON_MERRY_MAGGIE",
    "ICON_TERRY",
    "ICON_BARGASAURUS", //50
    "ICON_YELLOW_STONY",
    "ICON_ALIEN",
    "ICON_CHRIS_P_BACON",
    "ICON_CAPTAIN_BLUBBER",
    "ICON_STYRACOSAURUS_MOM",
    "ICON_ROYSTEN",
    "ICON_SAFE",
    "ICON_GUFFO",
    "ICON_MR_FIT",
    "ICON_CAPTAIN_BLACKEYE", //60
    "ICON_JINJO_RED",
    "ICON_JINJO_WHITE",
    "ICON_JINJO_BLACK",
    "ICON_JINJO_BROWN",
    "ICON_CHILLY_WILLY",
    "ICON_CHILLI_BILLI",
    "ICON_MINGY_JONGO",
    "ICON_YELLOW_DODGEM",
    "ICON_MINGELLA",
    "ICON_BLOBBELDA", //70
    "ICON_KLUNGO",
    "ICON_BOTTLES_DEAD",
    "ICON_MINJO_GREEN",
    "ICON_MINJO_RED",
    "ICON_MINJO_BLUE",
    "ICON_MINJO_PURPLE",
    "ICON_MINJO_BLACK",
    "ICON_RABBIT_WORKER1",
    "ICON_UNGA_BUNGA",
    "ICON_JIGGYWIGGY", //80
    "ICON_JIGGYWIGGY_DISCIPLE",
    "ICON_HONEY_B",
    "ICON_BANJO_KAZOOIE",
    "ICON_PIG1",
    "ICON_OOGLE_BOOGLE",
    "ICON_GI_ANNOUNCER",
    "ICON_DINGPOT",
    "ICON_KING_JINGALING_DEAD",
    "ICON_ROCKNUT",
    "ICON_MILDRED", //90
    "ICON_BIGGA_FOOT",
    "ICON_GEORGE",
    "ICON_SABREMAN",
    "ICON_DIPPY",
    "ICON_LOGGO",
    "ICON_KING_JINGALING",
    "ICON_MRS_BOTTLES",
    "ICON_SPECCY",
    "ICON_GOGGLES",
    "ICON_TARGITZAN", //100
    "ICON_CHOMPA",
    "ICON_LORD_WOO_FAK_FAK",
    "ICON_WELDAR",
    "ICON_ALIEN_CHILD",
    "ICON_EVIL_BOTTLES",
    "ICON_DINO_KID2",
    "ICON_DINO_SCRIT_SMALL",
    "ICON_DINO_SCRIT_BIG",
    "ICON_HEGGY", //109
]
var JAMJAR_SILO_TABLE = {}
var JAMJAR_SILO_LOCATIONS = [
    "1230753",
    "1230754",
    "1230755",
    "1230756",
    "1230757",
    "1230758",
    "1230759",
    "1230761",
    "1230762",
    "1230760",
    "1230763",
    "1230764",
    "1230766",
    "1230765",
    "1230767",
    "1230768",
    "1230769",
    "1230770",
    "1230773",
    "1230771",
    "1230772",
    "1230774",
    "1230775",
    "1230776",
]

var UNLOCKED_WORLDS = {}



// Address Map for Banjo-Tooie
var ADDRESS_MAP = {
    "SILO" : {
        "1230753" : {
            addr: 0x1B,
            bit: 3,
            name: 'Egg Aim'
        },
        "1230754" : {
            addr: 0x1B,
            bit: 2,
            name: 'Breegull Blaster'
        },
        "1230755" : {
            addr: 0x1B,
            bit: 1,
            name: 'Grip Grab'
        },
        "1230756" : {
            addr: 0x1E,
            bit: 1,
            name: 'Fire Eggs'
        },
        "1230757" : {
            addr: 0x1B,
            bit: 6,
            name: 'Bill Drill'
        },
        "1230758" : {
            addr: 0x1B,
            bit: 7,
            name: 'Beak Bayonet'
        },
        "1230759" : {
            addr: 0x1E,
            bit: 2,
            name: 'Grenade Eggs'
        },
        "1230760" : {
            addr: 0x1C,
            bit: 0,
            name: 'Airborne Egg Aiming'
        },
        "1230761" : {
            addr: 0x1C,
            bit: 1,
            name: 'Split Up'
        },
        "1230762" : {
            addr: 0x1D,
            bit: 6,
            name: 'Pack Whack'
        },
        "1230763" : {
            addr: 0x1E,
            bit: 4,
            name: 'Ice Eggs'
        },
        "1230764" : {
            addr: 0x1C,
            bit: 2,
            name: 'Wing Whack'
        },
        "1230765" : {
            addr: 0x1C,
            bit: 3,
            name: 'Talon Torpedo'
        },
        "1230766" : {
            addr: 0x1C,
            bit: 4,
            name: 'Sub-Aqua Egg Aiming'
        },
        "1230767" : {
            addr: 0x1E,
            bit: 3,
            name: 'Clockwork Kazooie Eggs'
        },
        "1230768" : {
            addr: 0x1D,
            bit: 3,
            name: 'Springy Step Shoes'
        },
        "1230769" : {
            addr: 0x1D,
            bit: 4,
            name: 'Taxi Pack'
        },
        "1230770" : {
            addr: 0x1D,
            bit: 5,
            name: 'Hatch'
        },
        "1230771" : {
            addr: 0x1D,
            bit: 0,
            name: 'Snooze Pack'
        },
        "1230772" : {
            addr: 0x1D,
            bit: 1,
            name: 'Leg Spring'
        },
        "1230773" : {
            addr: 0x1D,
            bit: 2,
            name: 'Claw Clamber Boots'
        },
        "1230774" : {
            addr: 0x1C,
            bit: 6,
            name: 'Shack Pack'
        },
        "1230775" : {
            addr: 0x1C,
            bit: 7,
            name: 'Glide'
        },
        "1230776" : {
            addr: 0x1D,
            bit: 7,
            name: 'Sack Pack'
        },
	},
    "TREBLE" : {
        "1230781" : {
            addr: 0x86,
            bit: 7,
            name: 'MT: Treble Clef'
        },
        "1230782" : {
            addr: 0x89,
            bit: 0,
            name: 'GGM: Treble Clef'
        },
        "1230783" : {
            addr: 0x8B,
            bit: 1,
            name: 'WW: Treble Clef'
        },
        "1230784" : {
            addr: 0x8D,
            bit: 2,
            name: 'JRL: Treble Clef'
        },
        "1230785" : {
            addr: 0x8F,
            bit: 3,
            name: 'TDL: Treble Clef'
        },
        "1230786" : {
            addr: 0x91,
            bit: 4,
            name: 'GI: Treble Clef'
        },
        "1230787" : {
            addr: 0x93,
            bit: 5,
            name: 'HFP: Treble Clef'
        },
        "1230788" : {
            addr: 0x95,
            bit: 6,
            name: 'CCL: Treble Clef'
        },
        "1230789" : {
            addr: 0x97,
            bit: 7,
            name: 'JV: Treble Clef'
        },
    },
    "STATIONBTN" : {
        "1230790" : {
            addr: 0x27,
            bit: 3,
            name: "Train Switch GI"
        },
        "1230791" : {
            addr: 0x27,
            bit: 4,
            name: "Train Switch TDL"
        },
        "1230792" : {
            addr: 0x35,
            bit: 0,
            name: "Train Switch HFP Lava"
        },
        "1230793" : {
            addr: 0x34,
            bit: 7,
            name: "Train Switch HFP Ice"
        },
        "1230794" : {
            addr: 0x7B,
            bit: 3,
            name: "Train Switch Clifftop"
        },
        "1230795" : {
            addr: 0x0D,
            bit: 6,
            name: "Train Switch WW"
        }
    },
    "CHUFFY" : {
        "1230796" : {
            addr: 0x0B,
            bit: 6,
            name: "King Coal Defeated"
        },
    },
    "JINJO_FAMILY" : {
        "1230676" : {
            addr: 0x4F,
            bit: 0,
            name: 'JV: White Jinjo Family Jiggy'
        },
        "1230677" : {
            addr: 0x4F,
            bit: 1,
            name: 'JV: Orange Jinjo Family Jiggy'
        },
        "1230678" : {
            addr: 0x4F,
            bit: 2,
            name: 'JV: Yellow Jinjo Family Jiggy'
        },
        "1230679" : {
            addr: 0x4F,
            bit: 3,
            name: 'JV: Brown Jinjo Family Jiggy'
        },
        "1230680" : {
            addr: 0x4F,
            bit: 4,
            name: 'JV: Green Jinjo Family Jiggy'
        },
        "1230681" : {
            addr: 0x4F,
            bit: 5,
            name: 'JV: Red Jinjo Family Jiggy'
        },
        "1230682" : {
            addr: 0x4F,
            bit: 6,
            name: 'JV: Blue Jinjo Family Jiggy'
        },
        "1230683" : {
            addr: 0x4F,
            bit: 7,
            name: 'JV: Purple Jinjo Family Jiggy'
        },
        "1230684" : {
            addr: 0x50,
            bit: 0,
            name: 'JV: Black Jinjo Family Jiggy'
        },
    },
    "STOPNSWAP" : {
        "1230953" : {
            addr: 0x77,
            bit: 7,
            name: "Yellow Egg Hatched"
        },
        "1230954" : {
            addr: 0x77,
            bit: 6,
            name: "Pink Egg Hatched"
        },
        "1230955" : {
            addr: 0x77,
            bit: 4,
            name: "Blue Egg Hatched"
        },
        "1230956" : {
            addr: 0x77,
            bit: 5,
            name: "Pink Egg"
        },
        "1230957" : {
            addr: 0x77,
            bit: 3,
            name: "Blue Egg"
        },
        "1230958" : {
            addr: 0x77,
            bit: 2,
            name: "Ice Key"
        }
    },
    "ROYSTEN" : {
        "1230777" : {
            addr: 0x9E,
            bit: 6,
            name: "SM: Roysten Reward 1"
        },
        "1230778" : {
            addr: 0x9E,
            bit: 6,
            name: "SM: Roysten Reward 2"
        }
    },
    "CHEATO" : {
        "1230992" : {
            addr: 0x08,
            bit: 4,
            name: "SM: Cheato Reward 1"
        },
        "1230993" : {
            addr: 0x08,
            bit: 5,
            name: "SM: Cheato Reward 2"
        },
        "1230994" : {
            addr: 0x08,
            bit: 6,
            name: "SM: Cheato Reward 3"
        },
        "1230995" : {
            addr: 0x08,
            bit: 7,
            name: "SM: Cheato Reward 4"
        },
        "1230996" : {
            addr: 0x09,
            bit: 0,
            name: "SM: Cheato Reward 5"
        },
    },
    "HONEYB" : {
        "1230997" : {
            addr: 0x98,
            bit: 2,
            name: "IoH: Honey B's Reward 1"
        },
        "1230998" : {
            addr: 0x98,
            bit: 3,
            name: "IoH: Honey B's Reward 2"
        },
        "1230999" : {
            addr: 0x98,
            name: "IoH: Honey B's Reward 3"
        },
        "1231000" : {
            addr: 0x98,
            bit: 4,
            name: "IoH: Honey B's Reward 4"
        },
        "1231001" : {
            addr: 0x98,
            name: "IoH: Honey B's Reward 5"
        },
    },
    "JCHUNKS" : {
        "1231002" : {
            addr: 0x7D,
            bit: 0,
            name: "GGM: Crushing Shed Jiggy Chunk 1"
        },
        "1231003" : {
            addr: 0x7D,
            bit: 1,
            name: "GGM: Crushing Shed Jiggy Chunk 2"
        },
        "1231004" : {
            addr: 0x7D,
            bit: 2,
            name: "GGM: Crushing Shed Jiggy Chunk 3"
        }
    },
    //Jinjo Jiggies are part of JINJOFAM
    "JIGGIES" : {
        "1230685" : {
            addr: 0x50,
            bit: 1,
            name: 'JV: King Jingaling Jiggy'
        },
        "1230596" : {
            addr: 0x45,
            bit: 0,
            name: 'MT: Targitzan Jiggy'
        },
        "1230597" : {
            addr: 0x45,
            bit: 1,
            name: 'MT: Slightly Sacred Chamber Jiggy'
        },
        "1230598" : {
            addr: 0x45,
            bit: 2,
            name: 'MT: Kickball Jiggy'
        },
        "1230599" : {
            addr: 0x45,
            bit: 3,
            name: 'MT: Bovina Jiggy'
        },
        "1230600" : {
            addr: 0x45,
            bit: 4,
            name: 'MT: Treasure Chamber Jiggy'
        },
        "1230601" : {
            addr: 0x45,
            bit: 5,
            name: 'MT: Golden Goliath Jiggy'
        },
        "1230602" : {
            addr: 0x45,
            bit: 6,
            name: 'MT: Prison Compound Quicksand Jiggy'
        },
        "1230603" : {
            addr: 0x45,
            bit: 7,
            name: 'MT: Pillars Jiggy'
        },
        "1230604" : {
            addr: 0x46,
            bit: 0,
            name: 'MT: Top of Temple Jiggy'
        },
        "1230605" : {
            addr: 0x46,
            bit: 1,
            name: 'MT: Ssslumber Jiggy'
        },
        "1230606" : {
            addr: 0x46,
            bit: 2,
            name: 'GGM: Old King Coal Jiggy'
        },
        "1230607" : {
            addr: 0x46,
            bit: 3,
            name: 'GGM: Canary Mary Jiggy'
        },
        "1230608" : {
            addr: 0x46,
            bit: 4,
            name: 'GGM: Generator Cavern Jiggy'
        },
        "1230609" : {
            addr: 0x46,
            bit: 5,
            name: 'GGM: Waterfall Cavern Jiggy'
        },
        "1230610" : {
            addr: 0x46,
            bit: 6,
            name: 'GGM: Ordinance Storage Jiggy'
        },
        "1230611" : {
            addr: 0x46,
            bit: 7,
            name: 'GGM: Dilberta Jiggy'
        },
        "1230612" : {
            addr: 0x47,
            bit: 0,
            name: 'GGM: Crushing Shed Jiggy'
        },
        "1230613" : {
            addr: 0x47,
            bit: 1,
            name: 'GGM: Waterfall Jiggy'
        },
        "1230614" : {
            addr: 0x47,
            bit: 2,
            name: 'GGM: Power Hut Basement Jiggy'
        },
        "1230615" : {
            addr: 0x47,
            bit: 3,
            name: 'GGM: Flooded Caves Jiggy'
        },
        "1230616" : {
            addr: 0x47,
            bit: 4,
            name: 'WW: Hoop Hurry Jiggy'
        },
        "1230617" : {
            addr: 0x47,
            bit: 5,
            name: 'WW: Dodgems Jiggy'
        },
        "1230618" : {
            addr: 0x47,
            bit: 6,
            name: 'WW: Mr. Patch Jiggy'
        },
        "1230619" : {
            addr: 0x47,
            bit: 7,
            name: 'WW: Saucer of Peril Jiggy'
        },
        "1230620" : {
            addr: 0x48,
            bit: 0,
            name: 'WW: Balloon Burst Jiggy'
        },
        "1230621" : {
            addr: 0x48,
            bit: 1,
            name: 'WW: Dive of Death Jiggy'
        },
        "1230622" : {
            addr: 0x48,
            bit: 2,
            name: 'WW: Mrs. Boggy Jiggy'
        },
        "1230623" : {
            addr: 0x48,
            bit: 3,
            name: 'WW: Star Spinner Jiggy'
        },
        "1230624" : {
            addr: 0x48,
            bit: 4,
            name: 'WW: The Inferno Jiggy'
        },
        "1230625" : {
            addr: 0x48,
            bit: 5,
            name: 'WW: Cactus of Strength Jiggy'
        },
        "1230626" : {
            addr: 0x48,
            bit: 6,
            name: 'JRL: Mini-Sub Challenge Jiggy'
        },
        "1230627" : {
            addr: 0x48,
            bit: 7,
            name: 'JRL: Tiptup Jiggy'
        },
        "1230628" : {
            addr: 0x49,
            bit: 0,
            name: 'JRL: Chris P. Bacon Jiggy'
        },
        "1230629" : {
            addr: 0x49,
            bit: 1,
            name: 'JRL: Pig Pool Jiggy'
        },
        "1230630" : {
            addr: 0x49,
            bit: 2,
            name: "JRL: Smuggler's Cavern Jiggy"
        },
        "1230631" : {
            addr: 0x49,
            bit: 3,
            name: 'JRL: Merry Maggie Jiggy'
        },
        "1230632" : {
            addr: 0x49,
            bit: 4,
            name: 'JRL: Woo Fak Fak Jiggy'
        },
        "1230633" : {
            addr: 0x49,
            bit: 5,
            name: 'JRL: Seemee Jiggy'
        },
        "1230634" : {
            addr: 0x49,
            bit: 6,
            name: 'JRL: Pawno Jiggy'
        },
        "1230635" : {
            addr: 0x49,
            bit: 7,
            name: 'JRL: UFO Jiggy'
        },
        "1230636" : {
            addr: 0x4A,
            bit: 0,
            name: "TDL: Under Terry's Nest Jiggy"
        },
        "1230637" : {
            addr: 0x4A,
            bit: 1,
            name: 'TDL: Dippy Jiggy'
        },
        "1230638" : {
            addr: 0x4A,
            bit: 2,
            name: 'TDL: Scrotty Jiggy'
        },
        "1230639" : {
            addr: 0x4A,
            bit: 3,
            name: 'TDL: Terry Jiggy'
        },
        "1230640" : {
            addr: 0x4A,
            bit: 4,
            name: 'TDL: Oogle Boogle Tribe Jiggy'
        },
        "1230641" : {
            addr: 0x4A,
            bit: 5,
            name: 'TDL: Chompas Belly Jiggy'
        },
        "1230642" : {
            addr: 0x4A,
            bit: 6,
            name: "TDL: Terry's Kids Jiggy"
        },
        "1230643" : {
            addr: 0x4A,
            bit: 7,
            name: 'TDL: Stomping Plains Jiggy'
        },
        "1230644" : {
            addr: 0x4B,
            bit: 0,
            name: 'TDL: Rocknut Tribe Jiggy'
        },
        "1230645" : {
            addr: 0x4B,
            bit: 1,
            name: 'TDL: Code of the Dinosaurs Jiggy'
        },
        "1230646" : {
            addr: 0x4B,
            bit: 2,
            name: 'GI: Underwater Waste Disposal Plant Jiggy'
        },
        "1230647" : {
            addr: 0x4B,
            bit: 3,
            name: 'GI: Weldar Jiggy'
        },
        "1230648" : {
            addr: 0x4B,
            bit: 4,
            name: "GI: Clinker's Cavern Jiggy"
        },
        "1230649" : {
            addr: 0x4B,
            bit: 5,
            name: 'GI: Skivvies Jiggy'
        },
        "1230650" : {
            addr: 0x4B,
            bit: 6,
            name: 'GI: Floor 5 Jiggy'
        },
        "1230651" : {
            addr: 0x4B,
            bit: 7,
            name: 'GI: Quality Control Jiggy'
        },
        "1230652" : {
            addr: 0x4C,
            bit: 0,
            name: 'GI: Floor 1 Guarded Jiggy'
        },
        "1230653" : {
            addr: 0x4C,
            bit: 1,
            name: 'GI: Trash Compactor Jiggy'
        },
        "1230654" : {
            addr: 0x4C,
            bit: 2,
            name: 'GI: Twinkly Packing Jiggy'
        },
        "1230655" : {
            addr: 0x4C,
            bit: 3,
            name: 'GI: Waste Disposal Plant Box Jiggy'
        },
        "1230656" : {
            addr: 0x4C,
            bit: 4,
            name: 'HFP: Dragon Brothers Jiggy'
        },
        "1230657" : {
            addr: 0x4C,
            bit: 5,
            name: 'HFP: Inside the Volcano Jiggy'
        },
        "1230658" : {
            addr: 0x4C,
            bit: 6,
            name: 'HFP: Sabreman Jiggy'
        },
        "1230659" : {
            addr: 0x4C,
            bit: 7,
            name: 'HFP: Boggy Jiggy'
        },
        "1230660" : {
            addr: 0x4D,
            bit: 0,
            name: 'HFP: Icy Side Station Jiggy'
        },
        "1230661" : {
            addr: 0x4D,
            bit: 1,
            name: 'HFP: Oil Drill Jiggy'
        },
        "1230662" : {
            addr: 0x4D,
            bit: 2,
            name: 'HFP: Stomping Plains Jiggy'
        },
        "1230663" : {
            addr: 0x4D,
            bit: 3,
            name: 'HFP: Kickball Jiggy'
        },
        "1230664" : {
            addr: 0x4D,
            bit: 4,
            name: 'HFP: Aliens Jiggy'
        },
        "1230665" : {
            addr: 0x4D,
            bit: 5,
            name: 'HFP: Lava Waterfall Jiggy'
        },
        "1230666" : {
            addr: 0x4D,
            bit: 6,
            name: 'CCL: Mingy Jongo Jiggy'
        },
        "1230667" : {
            addr: 0x4D,
            bit: 7,
            name: 'CCL: Mr Fit Jiggy'
        },
        "1230668" : {
            addr: 0x4E,
            bit: 0,
            name: "CCL: Pot O' Gold Jiggy"
        },
        "1230669" : {
            addr: 0x4E,
            bit: 1,
            name: 'CCL: Canary Mary Jiggy'
        },
        "1230670" : {
            addr: 0x4E,
            bit: 2,
            name: 'CCL: Zubbas Jiggy'
        },
        "1230671" : {
            addr: 0x4E,
            bit: 3,
            name: 'CCL: Jiggium Plant Jiggy'
        },
        "1230672" : {
            addr: 0x4E,
            bit: 4,
            name: 'CCL: Cheese Wedge Jiggy'
        },
        "1230673" : {
            addr: 0x4E,
            bit: 5,
            name: 'CCL: Trash Can Jiggy'
        },
        "1230674" : {
            addr: 0x4E,
            bit: 6,
            name: 'CCL: Superstash Jiggy'
        },
        "1230675" : {
            addr: 0x4E,
            bit: 7,
            name: 'CCL: Jelly Castle Jiggy'
        }
    },
    "JINJOS" : {
        "1230591" : {
            addr: 0x3E,
            bit: 4,
            name: 'IoH:Wooded Hollow Jinjo'
        },
        "1230595" : {
            addr: 0x3F,
            bit: 0,
            name: 'SM: Jinjo'
        },
        "1230594" : {
            addr: 0x3E,
            bit: 7,
            name: 'IoH: Plateau Jinjo'
        },
        "1230551" : {
            addr: 0x39,
            bit: 4,
            name: 'MT: Jade Snake Grove Jinjo'
        },
        "1230552" : {
            addr: 0x39,
            bit: 5,
            name: 'MT: Stadium Jinjo'
        },
        "1230553" : {
            addr: 0x39,
            bit: 6,
            name: 'Mayahem Temple: Targitzan Temple Jinjo'
        },
        "1230554" : {
            addr: 0x39,
            bit: 7,
            name: 'MT: Water Pool Jinjo'
        },
        "1230555" : {
            addr: 0x3A,
            bit: 0,
            name: 'MT: Bridge Jinjo'
        },
        "1230556" : {
            addr: 0x3A,
            bit: 1,
            name: 'GGM: Water Storage Jinjo'
        },
        "1230557" : {
            addr: 0x3A,
            bit: 2,
            name: 'GGM: Jail Jinjo'
        },
        "1230558" : {
            addr: 0x3A,
            bit: 3,
            name: 'GGM: Toxic Gas Cave Jinjo'
        },
        "1230559" : {
            addr: 0x3A,
            bit: 4,
            name: 'GGM: Boulder Jinjo'
        },
        "1230560" : {
            addr: 0x3A,
            bit: 5,
            name: 'GGM: Mine Tracks Jinjo'
        },
        "1230561" : {
            addr: 0x3A,
            bit: 6,
            name: 'WW: Big Top Jinjo'
        },
        "1230562" : {
            addr: 0x3A,
            bit: 7,
            name: 'WW: Cave of Horrors Jinjo'
        },
        "1230563" : {
            addr: 0x3B,
            bit: 0,
            name: 'WW: Van Door Jinjo'
        },
        "1230564" : {
            addr: 0x3B,
            bit: 1,
            name: 'WW: Dodgem Dome Jinjo'
        },
        "1230565" : {
            addr: 0x3B,
            bit: 2,
            name: 'WW: Cactus of Strength Jinjo'
        },
        "1230593" : {
            addr: 0x3E,
            bit: 6,
            name: 'IoH: Clifftop Jinjo'
        },
        "1230566" : {
            addr: 0x3B,
            bit: 3,
            name: 'JRL: Lagoon Alcove Jinjo'
        },
        "1230567" : {
            addr: 0x3B,
            bit: 4,
            name: 'JRL: Blubber Jinjo'
        },
        "1230568" : {
            addr: 0x3B,
            bit: 5,
            name: 'JRL: Big Fish Jinjo'
        },
        "1230569" : {
            addr: 0x3B,
            bit: 6,
            name: 'JRL: Seaweed Sanctum Jinjo'
        },
        "1230570" : {
            addr: 0x3B,
            bit: 7,
            name: 'JRL: Sunken Ship Jinjo'
        },
        "1230592" : {
            addr: 0x3E,
            bit: 5,
            name: 'IoH: Wasteland Jinjo'
        },
        "1230571" : {
            addr: 0x3C,
            bit: 0,
            name: 'TDL: Talon Torp Jinjo'
        },
        "1230572" : {
            addr: 0x3C,
            bit: 1,
            name: 'TDL: Cutscene Skip Jinjo'
        },
        "1230573" : {
            addr: 0x3C,
            bit: 2,
            name: 'TDL: Beside Rocknut Jinjo'
        },
        "1230574" : {
            addr: 0x3C,
            bit: 3,
            name: 'TDL: Big T. Rex Skip Jinjo'
        },
        "1230575" : {
            addr: 0x3C,
            bit: 4,
            name: 'TDL: Stomping Plains Jinjo'
        },
        "1230576" : {
            addr: 0x3C,
            bit: 5,
            name: 'GI: Floor 5 Jinjo'
        },
        "1230577" : {
            addr: 0x3C,
            bit: 6,
            name: 'GI: Leg Spring Jinjo'
        },
        "1230578" : {
            addr: 0x3C,
            bit: 7,
            name: 'GI: Waste Disposal Plant Jinjo'
        },
        "1230579" : {
            addr: 0x3D,
            bit: 0,
            name: 'GI: Boiler Plant Jinjo'
        },
        "1230580" : {
            addr: 0x3D,
            bit: 1,
            name: 'GI: Outside Jinjo'
        },
        "1230581" : {
            addr: 0x3D,
            bit: 2,
            name: 'HFP: Lava Waterfall Jinjo'
        },
        "1230582" : {
            addr: 0x3D,
            bit: 3,
            name: 'HFP: Boiling Hot Pool Jinjo'
        },
        "1230583" : {
            addr: 0x3D,
            bit: 4,
            name: 'HFP: Windy Hole Jinjo'
        },
        "1230584" : {
            addr: 0x3D,
            bit: 5,
            name: 'HFP: Icicle Grotto Jinjo'
        },
        "1230585" : {
            addr: 0x3D,
            bit: 6,
            name: 'HFP: Mildred Ice Cube Jinjo'
        },
        "1230586" : {
            addr: 0x3D,
            bit: 7,
            name: 'CCL: Trash Can Jinjo'
        },
        "1230587" : {
            addr: 0x3E,
            bit: 0,
            name: 'CCL: Cheese Wedge Jinjo'
        },
        "1230588" : {
            addr: 0x3E,
            bit: 1,
            name: 'CCL: Central Cavern Jinjo'
        },
        "1230589" : {
            addr: 0x3E,
            bit: 2,
            name: 'CCL: Mingy Jongo Skull Jinjo'
        },
        "1230590" : {
            addr: 0x3E,
            bit: 3,
            name: 'CCL: Wumba Jinjo'
        }
    },
    "PAGES" : {
        "1230752" : {
            addr: 0x59,
            bit: 3,
            name: 'Spiral Mountain: Cheato Page'
        },
        "1230728" : {
            addr: 0x56,
            bit: 3,
            name: 'MT: Snake Head Cheato Page'
        },
        "1230729" : {
            addr: 0x56,
            bit: 4,
            name: 'MT: Prison Compound Cheato Page'
        },
        "1230730" : {
            addr: 0x56,
            bit: 5,
            name: 'MT: Jade Snake Grove Cheato Page'
        },
        "1230731" : {
            addr: 0x56,
            bit: 6,
            name: 'GGM: Canary Mary Cheato Page'
        },
        "1230732" : {
            addr: 0x56,
            bit: 7,
            name: 'GGM: Entrance Cheato Page'
        },
        "1230733" : {
            addr: 0x57,
            bit: 0,
            name: 'GGM: Water Storage Cheato Page'
        },
        "1230734" : {
            addr: 0x57,
            bit: 1,
            name: 'WW: The Haunted Cavern Cheato Page'
        },
        "1230735" : {
            addr: 0x57,
            bit: 2,
            name: 'WW: The Inferno Cheato Page'
        },
        "1230736" : {
            addr: 0x57,
            bit: 3,
            name: 'WW: Saucer of Peril Cheato Page'
        },
        "1230737" : {
            addr: 0x57,
            bit: 4,
            name: "JRL: Pawno Cheato Page"
        },
        "1230738" : {
            addr: 0x57,
            bit: 5,
            name: 'JRL: Seemee Cheato Page'
        },
        "1230739" : {
            addr: 0x57,
            bit: 6,
            name: 'JRL: Ancient Baths Cheato Page'
        },
        "1230740" : {
            addr: 0x57,
            bit: 7,
            name: "TDL: Dippy's Pool Cheato Page"
        },
        "1230741" : {
            addr: 0x58,
            bit: 0,
            name: 'TDL: Inside the Mountain Cheato Page'
        },
        "1230742" : {
            addr: 0x58,
            bit: 1,
            name: 'TDL: Boulder Cheato Page'
        },
        "1230743" : {
            addr: 0x58,
            bit: 2,
            name: 'GI: Loggo Cheato Page'
        },
        "1230744" : {
            addr: 0x58,
            bit: 3,
            name: 'GI: Floor 2 Cheato Page'
        },
        "1230745" : {
            addr: 0x58,
            bit: 4,
            name: 'GI: Repair Depot Cheato Page'
        },
        "1230746" : {
            addr: 0x58,
            bit: 5,
            name: 'HFP: Lava Side Cheato Page'
        },
        "1230747" : {
            addr: 0x58,
            bit: 6,
            name: 'HFP: Icicle Grotto Cheato Page'
        },
        "1230748" : {
            addr: 0x58,
            bit: 7,
            name: 'HFP: Icy Side Cheato Page'
        },
        "1230749" : {
            addr: 0x59,
            bit: 0,
            name: 'CCL: Canary Mary Cheato Page'
        },
        "1230750" : {
            addr: 0x59,
            bit: 1,
            name: "CCL: Pot O' Gold Cheato Page"
        },
        "1230751" : {
            addr: 0x59,
            bit: 2,
            name: 'CCL: Zubbas Cheato Page'
        },
    },
    "HONEYCOMB" : {
        "1230727" : {
            addr: 0x42,
            bit: 2,
            name: 'Plateau: Honeycomb'
        },
        "1230703" : {
            addr: 0x3F,
            bit: 2,
            name: 'MT: Entrance Honeycomb'
        },
        "1230704" : {
            addr: 0x3F,
            bit: 3,
            name: 'MT: Bovina Honeycomb'
        },
        "1230705" : {
            addr: 0x3F,
            bit: 4,
            name: 'MT: Treasure Chamber Honeycomb'
        },
        "1230706" : {
            addr: 0x3F,
            bit: 5,
            name: 'GGM: Toxic Gas Cave Honeycomb'
        },
        "1230707" : {
            addr: 0x3F,
            bit: 6,
            name: 'GGM: Boulder Honeycomb'
        },
        "1230708" : {
            addr: 0x3F,
            bit: 7,
            name: 'GGM: Train Station Honeycomb'
        },
        "1230709" : {
            addr: 0x40,
            bit: 0,
            name: 'WW: Space Zone Honeycomb'
        },
        "1230710" : {
            addr: 0x40,
            bit: 1,
            name: 'WW: Mumbo Skull Honeycomb'
        },
        "1230711" : {
            addr: 0x40,
            bit: 2,
            name: 'WW: Crazy Castle Honeycomb'
        },
        "1230712" : {
            addr: 0x40,
            bit: 3,
            name: 'JRL: Seemee Honeycomb'
        },
        "1230713" : {
            addr: 0x40,
            bit: 4,
            name: 'JRL: Atlantis Honeycomb'
        },
        "1230714" : {
            addr: 0x40,
            bit: 5,
            name: 'JRL: Waste Pipe Honeycomb'
        },
        "1230715" : {
            addr: 0x40,
            bit: 6,
            name: 'TDL: Lakeside Honeycomb'
        },
        "1230716" : {
            addr: 0x40,
            bit: 7,
            name: 'TDL: Styracosaurus Cave Honeycomb'
        },
        "1230717" : {
            addr: 0x41,
            bit: 0,
            name: 'TDL: River Passage Honeycomb'
        },
        "1230718" : {
            addr: 0x41,
            bit: 1,
            name: 'GI: Floor 3 Honeycomb'
        },
        "1230719" : {
            addr: 0x41,
            bit: 2,
            name: 'GI: Train Station Honeycomb'
        },
        "1230720" : {
            addr: 0x41,
            bit: 3,
            name: 'GI: Chimney Honeycomb'
        },
        "1230721" : {
            addr: 0x41,
            bit: 4,
            name: 'HFP: Inside the Volcano Honeycomb'
        },
        "1230722" : {
            addr: 0x41,
            bit: 5,
            name: 'HFP: Train Station Honeycomb'
        },
        "1230723" : {
            addr: 0x41,
            bit: 6,
            name: 'HFP: Lava Side Honeycomb'
        },
        "1230724" : {
            addr: 0x41,
            bit: 7,
            name: 'CCL: Dirt Patch Honeycomb'
        },
        "1230725" : {
            addr: 0x42,
            bit: 0,
            name: 'CCL: Trash Can Honeycomb'
        },
        "1230726" : {
            addr: 0x42,
            bit: 1,
            name: "CCL: Pot O' Gold Honeycomb"
        },
    },
    "GLOWBO" : {
        "1230046" : {
            addr: 0x05,
            bit: 6,
            name: 'Mega Glowbo'
        },
        "1230686" : {
            addr: 0x42,
            bit: 7,
            name: "MT: Mumbo's Glowbo"
        },
        "1230687" : {
            addr: 0x43,
            bit: 0,
            name: 'MT: Jade Snake Grove Glowbo'

        },
        "1230688" : {
            addr: 0x43,
            bit: 1,
            name: 'GGM: Near Entrance Glowbo'

        },
        "1230689" : {
            addr: 0x43,
            bit: 2,
            name: 'GGM: Mine Entrance 2 Glowbo'

        },
        "1230690" : {
            addr: 0x43,
            bit: 3,
            name: 'WW: The Inferno Glowbo'

        },
        "1230691" : {
            addr: 0x43,
            bit: 4,
            name: "WW: Wumba's Glowbo"

        },
        "1230702" : {
            addr: 0x44,
            bit: 7,
            name: 'Cliff Top: Glowbo'

        },
        "1230692" : {
            addr: 0x43,
            bit: 5,
            name: "JRL: Pawno's Emporium Glowbo"

        },
        "1230693" : {
            addr: 0x43,
            bit: 6,
            name: "JRL: Under Wumba's Wigwam Glowbo"

        },
        "1230694" : {
            addr: 0x43,
            bit: 7,
            name: 'TDL: Unga Bunga Cave Entrance Glowbo'

        },
        "1230695" : {
            addr: 0x44,
            bit: 0,
            name: "TDL: Behind Mumbo's Skull Glowbo"

        },
        "1230696" : {
            addr: 0x44,
            bit: 1,
            name: 'GI: Floor 2 Glowbo'

        },
        "1230697" : {
            addr: 0x44,
            bit: 2,
            name: 'GI: Floor 3 Glowbo'

        },
        "1230698" : {
            addr: 0x44,
            bit: 3,
            name: 'HFP: Lava Side Glowbo'

        },
        "1230699" : {
            addr: 0x44,
            bit: 4,
            name: 'HFP: Icy Side Glowbo'

        },
        "1230700" : {
            addr: 0x44,
            bit: 5,
            name: 'CCL: Green Pool Glowbo'

        },
        "1230701" : {
            addr: 0x44,
            bit: 6,
            name: 'CCL: Central Cavern Glowbo'

        },
    },
    "DOUBLOON" : {
        "1230521" : {
            addr: 0x22,
            bit: 7,
            name: 'JRL: Town Center Pole 1 Doubloon'
        },
        "1230522" : {
            addr: 0x23,
            bit: 0,
            name: 'JRL: Town Center Pole 2 Doubloon'
        },
        "1230523" : {
            addr: 0x23,
            bit: 1,
            name: 'JRL: Town Center Pole 3 Doubloon'
        },
        "1230524" : {
            addr: 0x23,
            bit: 2,
            name: 'JRL: Town Center Pole 4 Doubloon'
        },
        "1230525" : {
            addr: 0x23,
            bit: 3,
            name: 'JRL: Town Center Pole 5 Doubloon'
        },
        "1230526" : {
            addr: 0x23,
            bit: 4,
            name: 'JRL: Town Center Pole 6 Doubloon'
        },
        "1230527" : {
            addr: 0x23,
            bit: 5,
            name: 'JRL: Silo 1 Doubloon'
        },
        "1230528" : {
            addr: 0x23,
            bit: 6,
            name: 'JRL: Silo 2 Doubloon'
        },
        "1230529" : {
            addr: 0x23,
            bit: 7,
            name: 'JRL: Silo 3 Doubloon'
        },
        "1230530" : {
            addr: 0x24,
            bit: 0,
            name: 'JRL: Silo 4 Doubloon'
        },
        "1230531" : {
            addr: 0x24,
            bit: 1,
            name: 'JRL: Toxic Pool 1 Doubloon'
        },
        "1230532" : {
            addr: 0x24,
            bit: 2,
            name: 'JRL: Toxic Pool 2 Doubloon'
        },
        "1230533" : {
            addr: 0x24,
            bit: 3,
            name: 'JRL: Toxic Pool 3 Doubloon'
        },
        "1230534" : {
            addr: 0x24,
            bit: 4,
            name: 'JRL: Toxic Pool 4 Doubloon'
        },
        "1230535" : {
            addr: 0x24,
            bit: 5,
            name: 'JRL: Mumbo Skull 1 Doubloon'
        },
        "1230536" : {
            addr: 0x24,
            bit: 6,
            name: 'JRL: Mumbo Skull 2 Doubloon'
        },
        "1230537" : {
            addr: 0x24,
            bit: 7,
            name: 'JRL: Mumbo Skull 3 Doubloon'
        },
        "1230538" : {
            addr: 0x25,
            bit: 0,
            name: 'JRL: Mumbo Skull 4 Doubloon'
        },
        "1230539" : {
            addr: 0x25,
            bit: 1,
            name: 'JRL: Underground 1 Doubloon'
        },
        "1230540" : {
            addr: 0x25,
            bit: 2,
            name: 'JRL: Underground 2 Doubloon'
        },
        "1230541" : {
            addr: 0x25,
            bit: 3,
            name: 'JRL: Underground 3 Doubloon'
        },
        "1230542" : {
            addr: 0x25,
            bit: 4,
            name: 'JRL: Alcove 1 Doubloon'
        },
        "1230543" : {
            addr: 0x25,
            bit: 5,
            name: 'JRL: Alcove 2 Doubloon'
        },
        "1230544" : {
            addr: 0x25,
            bit: 6,
            name: 'JRL: Alcove 3 Doubloon'
        },
        "1230545" : {
            addr: 0x25,
            bit: 7,
            name: 'JRL: Capt Blackeye 1 Doubloon'
        },
        "1230546" : {
            addr: 0x26,
            bit: 0,
            name: 'JRL: Capt Blackeye 2 Doubloon'
        },
        "1230547" : {
            addr: 0x26,
            bit: 1,
            name: 'JRL: Near Jinjo 1 Doubloon'
        },
        "1230548" : {
            addr: 0x26,
            bit: 2,
            name: 'JRL: Near Jinjo 2 Doubloon'
        },
        "1230549" : {
            addr: 0x26,
            bit: 3,
            name: 'JRL: Near Jinjo 3 Doubloon'
        },
        "1230550" : {
            addr: 0x26,
            bit: 4,
            name: 'JRL: Near Jinjo 4 Doubloon'
        }
    },
    "NOTES" : {
        "1230800" : {
            addr: 0x84,
            bit: 7,
        },
        "1230801" : {
            addr: 0x85,
            bit: 0,
        },
        "1230802" : {
            addr: 0x85,
            bit: 1,
        },
        "1230803" : {
            addr: 0x85,
            bit: 2,
        },
        "1230804" : {
            addr: 0x85,
            bit: 3,
        },
        "1230805" : {
            addr: 0x85,
            bit: 4,
        },
        "1230806" : {
            addr: 0x85,
            bit: 5,
        },
        "1230807" : {
            addr: 0x85,
            bit: 6,
        },
        "1230808" : {
            addr: 0x85,
            bit: 7,
        },
        "1230809" : {
            addr: 0x86,
            bit: 0,
        },
        "1230810" : {
            addr: 0x86,
            bit: 1,
        },
        "1230811" : {
            addr: 0x86,
            bit: 2,
        },
        "1230812" : {
            addr: 0x86,
            bit: 3,
        },
        "1230813" : {
            addr: 0x86,
            bit: 4,
        },
        "1230814" : {
            addr: 0x86,
            bit: 5,
        },
        "1230815" : {
            addr: 0x86,
            bit: 6,
        },
         // EO Mayahem Temple
         "1230816" : {
            addr: 0x87,
            bit: 0,
        },
        "1230817" : {
            addr: 0x87,
            bit: 1,
        },
        "1230818" : {
            addr: 0x87,
            bit: 2,
        },
        "1230819" : {
            addr: 0x87,
            bit: 3,
        },
        "1230820" : {
            addr: 0x87,
            bit: 4,
        },
        "1230821" : {
            addr: 0x87,
            bit: 5,
        },
        "1230822" : {
            addr: 0x87,
            bit: 6,
        },
        "1230823" : {
            addr: 0x87,
            bit: 7,
        },
        "1230824" : {
            addr: 0x88,
            bit: 0,
        },
        "1230825" : {
            addr: 0x88,
            bit: 1,
        },
        "1230826" : {
            addr: 0x88,
            bit: 2,
        },
        "1230827" : {
            addr: 0x88,
            bit: 3,
        },
        "1230828" : {
            addr: 0x88,
            bit: 4,
        },
        "1230829" : {
            addr: 0x88,
            bit: 5,
        },
        "1230830" : {
            addr: 0x88,
            bit: 6,
        },
        "1230831" : {
            addr: 0x88,
            bit: 7,
        },
        // EO GGM
        "1230832" : {
            addr: 0x89,
            bit: 1,
        },
        "1230833" : {
            addr: 0x89,
            bit: 2,
        },
        "1230834" : {
            addr: 0x89,
            bit: 3,
        },
        "1230835" : {
            addr: 0x89,
            bit: 4,
        },
        "1230836" : {
            addr: 0x89,
            bit: 5,
        },
        "1230837" : {
            addr: 0x89,
            bit: 6,
        },
        "1230838" : {
            addr: 0x89,
            bit: 7,
        },
        "1230839" : {
            addr: 0x8A,
            bit: 0,
        },
        "1230840" : {
            addr: 0x8A,
            bit: 1,
        },
        "1230841" : {
            addr: 0x8A,
            bit: 2,
        },
        "1230842" : {
            addr: 0x8A,
            bit: 3,
        },
        "1230843" : {
            addr: 0x8A,
            bit: 4,
        },
        "1230844" : {
            addr: 0x8A,
            bit: 5,
        },
        "1230845" : {
            addr: 0x8A,
            bit: 6,
        },
        "1230846" : {
            addr: 0x8A,
            bit: 7,
        },
        "1230847" : {
            addr: 0x8B,
            bit: 0,
        },
        //EO WW
        "1230848" : {
            addr: 0x8B,
            bit: 2,
        },
        "1230849" : {
            addr: 0x8B,
            bit: 3,
        },
        "1230850" : {
            addr: 0x8B,
            bit: 4,
        },
        "1230851" : {
            addr: 0x8B,
            bit: 5,
        },
        "1230852" : {
            addr: 0x8B,
            bit: 6,
        },
        "1230853" : {
            addr: 0x8B,
            bit: 7,
        },
        "1230854" : {
            addr: 0x8C,
            bit: 0,
        },
        "1230855" : {
            addr: 0x8C,
            bit: 1,
        },
        "1230856" : {
            addr: 0x8C,
            bit: 2,
        },
        "1230857" : {
            addr: 0x8C,
            bit: 3,
        },
        "1230858" : {
            addr: 0x8C,
            bit: 4,
        },
        "1230859" : {
            addr: 0x8C,
            bit: 5,
        },
        "1230860" : {
            addr: 0x8C,
            bit: 6,
        },
        "1230861" : {
            addr: 0x8C,
            bit: 7,
        },
        "1230862" : {
            addr: 0x8D,
            bit: 0,
        },
        "1230863" : {
            addr: 0x8D,
            bit: 1,
        },
        // EO JRL
        "1230864" : {
            addr: 0x8D,
            bit: 3,
        },
        "1230865" : {
            addr: 0x8D,
            bit: 4,
        },
        "1230866" : {
            addr: 0x8D,
            bit: 5,
        },
        "1230867" : {
            addr: 0x8D,
            bit: 6,
        },
        "1230868" : {
            addr: 0x8D,
            bit: 7,
        },
        "1230869" : {
            addr: 0x8E,
            bit: 0,
        },
        "1230870" : {
            addr: 0x8E,
            bit: 1,
        },
        "1230871" : {
            addr: 0x8E,
            bit: 2,
        },
        "1230872" : {
            addr: 0x8E,
            bit: 3,
        },
        "1230873" : {
            addr: 0x8E,
            bit: 4,
        },
        "1230874" : {
            addr: 0x8E,
            bit: 5,
        },
        "1230875" : {
            addr: 0x8E,
            bit: 6,
        },
        "1230876" : {
            addr: 0x8E,
            bit: 7,
        },
        "1230877" : {
            addr: 0x8F,
            bit: 0,
        },
        "1230878" : {
            addr: 0x8F,
            bit: 1,
        },
        "1230879" : {
            addr: 0x8F,
            bit: 2,
        },
        // EO TDL
        "1230880" : {
            addr: 0x8F,
            bit: 4,
        },
        "1230881" : {
            addr: 0x8F,
            bit: 5,
        },
        "1230882" : {
            addr: 0x8F,
            bit: 6,
        },
        "1230883" : {
            addr: 0x8F,
            bit: 7,
        },
        "1230884" : {
            addr: 0x90,
            bit: 0,
        },
        "1230885" : {
            addr: 0x90,
            bit: 1,
        },
        "1230886" : {
            addr: 0x90,
            bit: 2,
        },
        "1230887" : {
            addr: 0x90,
            bit: 3,
        },
        "1230888" : {
            addr: 0x90,
            bit: 4,
        },
        "1230889" : {
            addr: 0x90,
            bit: 5,
        },
        "1230890" : {
            addr: 0x90,
            bit: 6,
        },
        "1230891" : {
            addr: 0x90,
            bit: 7,
        },
        "1230892" : {
            addr: 0x91,
            bit: 0,
        },
        "1230893" : {
            addr: 0x91,
            bit: 1,
        },
        "1230894" : {
            addr: 0x91,
            bit: 2,
        },
        "1230895" : {
            addr: 0x91,
            bit: 3,
        },
        // EO GI
        "1230896" : {
            addr: 0x91,
            bit: 5,
        },
        "1230897" : {
            addr: 0x91,
            bit: 6,
        },
        "1230898" : {
            addr: 0x91,
            bit: 7,
        },
        "1230899" : {
            addr: 0x92,
            bit: 0,
        },
        "1230900" : {
            addr: 0x92,
            bit: 1,
        },
        "1230901" : {
            addr: 0x92,
            bit: 2,
        },
        "1230902" : {
            addr: 0x92,
            bit: 3,
        },
        "1230903" : {
            addr: 0x92,
            bit: 4,
        },
        "1230904" : {
            addr: 0x92,
            bit: 5,
        },
        "1230905" : {
            addr: 0x92,
            bit: 6,
        },
        "1230906" : {
            addr: 0x92,
            bit: 7,
        },
        "1230907" : {
            addr: 0x93,
            bit: 0,
        },
        "1230908" : {
            addr: 0x93,
            bit: 1,
        },
        "1230909" : {
            addr: 0x93,
            bit: 2,
        },
        "1230910" : {
            addr: 0x93,
            bit: 3,
        },
        "1230911" : {
            addr: 0x93,
            bit: 4,
        },
        // EO HFP
        "1230912" : {
            addr: 0x93,
            bit: 6,
        },
        "1230913" : {
            addr: 0x93,
            bit: 7,
        },
        "1230914" : {
            addr: 0x94,
            bit: 0,
        },
        "1230915" : {
            addr: 0x94,
            bit: 1,
        },
        "1230916" : {
            addr: 0x94,
            bit: 2,
        },
        "1230917" : {
            addr: 0x94,
            bit: 3,
        },
        "1230918" : {
            addr: 0x94,
            bit: 4,
        },
        "1230919" : {
            addr: 0x94,
            bit: 5,
        },
        "1230920" : {
            addr: 0x94,
            bit: 6,
        },
        "1230921" : {
            addr: 0x94,
            bit: 7,
        },
        "1230922" : {
            addr: 0x95,
            bit: 0,
        },
        "1230923" : {
            addr: 0x95,
            bit: 1,
        },
        "1230924" : {
            addr: 0x95,
            bit: 2,
        },
        "1230925" : {
            addr: 0x95,
            bit: 3,
        },
        "1230926" : {
            addr: 0x95,
            bit: 4,
        },
        "1230927" : {
            addr: 0x95,
            bit: 5,
        },
        // EO CCL
        "1230928" : {
            addr: 0x95,
            bit: 7,
        },
        "1230929" : {
            addr: 0x96,
            bit: 0,
        },
        "1230930" : {
            addr: 0x96,
            bit: 1,
        },
        "1230931" : {
            addr: 0x96,
            bit: 2,
        },
        "1230932" : {
            addr: 0x96,
            bit: 3,
        },
        "1230933" : {
            addr: 0x96,
            bit: 4,
        },
        "1230934" : {
            addr: 0x96,
            bit: 5,
        },
        "1230935" : {
            addr: 0x96,
            bit: 6,
        },
        "1230936" : {
            addr: 0x96,
            bit: 7,
        },
        "1230937" : {
            addr: 0x97,
            bit: 0,
        },
        "1230938" : {
            addr: 0x97,
            bit: 1,
        },
        "1230939" : {
            addr: 0x97,
            bit: 2,
        },
        "1230940" : {
            addr: 0x97,
            bit: 3,
        },
        "1230941" : {
            addr: 0x97,
            bit: 4,
        },
        "1230942" : {
            addr: 0x97,
            bit: 5,
        },
        "1230943" : {
            addr: 0x97,
            bit: 6,
        }
    },
    "AMAZE" : {
        "1231005" : {
            addr: 0x1E,
            bit: 0,
        }
    },
    "ROAR" : {
        "1231009" : {
            addr: 0x1C,
            bit: 5,
        }
    },
    "H1" : {
        "1230027" : {
           addr: 0x03,
           bit: 3,
           name: "Hag 1 Defeated"
       },
    },
    "NESTS" : {
        1231010: 0x000,
        1231011: 0x001,
        1231012: 0x002,
        1231013: 0x003,
        1231014: 0x004,
        1231015: 0x005,
        1231016: 0x006,
        1231017: 0x007,
        1231018: 0x008,
        1231019: 0x009,
        1231020: 0x00A,
        1231021: 0x00B,
        1231022: 0x00C,
        1231023: 0x00D,
        1231024: 0x00E,
        1231025: 0x00F,
        1231026: 0x010,
        1231027: 0x011,
        1231028: 0x012,
        1231029: 0x013,
        1231030: 0x014,
        1231031: 0x015,
        1231032: 0x016,
        1231033: 0x017,
        1231034: 0x018,
        1231035: 0x019,
        1231036: 0x01A,
        1231037: 0x01B,
        1231038: 0x01C,
        1231039: 0x01D,
        1231040: 0x01E,
        1231041: 0x01F,
        1231042: 0x020,
        1231043: 0x021,
        1231044: 0x022,
        1231045: 0x023,
        1231046: 0x024,
        1231047: 0x025,
        1231048: 0x026,
        1231049: 0x027,
        1231050: 0x028,
        1231051: 0x029,
        1231052: 0x02A,
        1231053: 0x02B,
        1231054: 0x02C,
        1231055: 0x02D,
        1231056: 0x02E,
        1231057: 0x02F,
        1231058: 0x030,
        1231059: 0x031,
        1231060: 0x032,
        1231061: 0x033,
        1231062: 0x034,
        1231063: 0x035,
        1231064: 0x036,
        1231065: 0x037,
        1231066: 0x038,
        1231067: 0x039,
        1231068: 0x03A,
        1231069: 0x03B,
        1231070: 0x03C,
        1231071: 0x03D,
        1231072: 0x03E,
        1231073: 0x03F,
        1231074: 0x040,
        1231075: 0x041,
        1231076: 0x042,
        1231077: 0x043,
        1231078: 0x044,
        1231079: 0x045,
        1231482: 0x046,
        1231080: 0x047,
        1231081: 0x048,
        1231082: 0x049,
        1231083: 0x04A,
        1231084: 0x04B,
        1231085: 0x04C,
        1231086: 0x04D,
        1231087: 0x04E,
        1231088: 0x04F,
        1231089: 0x050,
        1231090: 0x051,
        1231091: 0x052,
        1231092: 0x053,
        1231093: 0x054,
        1231094: 0x055,
        1231095: 0x056,
        1231096: 0x057,
        1231097: 0x058,
        1231098: 0x059,
        1231099: 0x05A,
        1231100: 0x05B,
        1231101: 0x05C,
        1231102: 0x05D,
        1231103: 0x05E,
        1231104: 0x05F,
        1231105: 0x060,
        1231106: 0x061,
        1231107: 0x062,
        1231108: 0x063,
        1231109: 0x064,
        1231110: 0x065,
        1231111: 0x066,
        1231112: 0x067,
        1231113: 0x068,
        1231114: 0x069,
        1231115: 0x06A,
        1231116: 0x06B,
        1231117: 0x06C,
        1231118: 0x06D,
        1231119: 0x06E,
        1231120: 0x06F,
        1231121: 0x070,
        1231122: 0x071,
        1231123: 0x072,
        1231124: 0x073,
        1231125: 0x074,
        1231126: 0x075,
        1231127: 0x076,
        1231128: 0x077,
        1231129: 0x078,
        1231130: 0x079,
        1231131: 0x07A,
        1231132: 0x07B,
        1231133: 0x07C,
        1231134: 0x07D,
        1231135: 0x07E,
        1231136: 0x07F,
        1231137: 0x080,
        1231138: 0x081,
        1231139: 0x082,
        1231140: 0x083,
        1231141: 0x084,
        1231142: 0x085,
        1231143: 0x086,
        1231144: 0x087,
        1231145: 0x088,
        1231146: 0x089,
        1231147: 0x08A,
        1231148: 0x08B,
        1231149: 0x08C,
        1231150: 0x08D,
        1231151: 0x08E,
        1231152: 0x08F,
        1231153: 0x090,
        1231154: 0x091,
        1231155: 0x092,
        1231156: 0x093,
        1231157: 0x094,
        1231158: 0x095,
        1231159: 0x096,
        1231160: 0x097,
        1231161: 0x098,
        1231162: 0x099,
        1231163: 0x09A,
        1231164: 0x09B,
        1231165: 0x09C,
        1231166: 0x09D,
        1231167: 0x09E,
        1231168: 0x09F,
        1231169: 0x0A0,
        1231170: 0x0A1,
        1231171: 0x0A2,
        1231172: 0x0A3,
        1231173: 0x0A4,
        1231174: 0x0A5,
        1231175: 0x0A6,
        1231176: 0x0A7,
        1231177: 0x0A8,
        1231178: 0x0A9,
        1231179: 0x0AA,
        1231180: 0x0AB,
        1231181: 0x0AC,
        1231182: 0x0AD,
        1231183: 0x0AE,
        1231184: 0x0AF,
        1231185: 0x0B0,
        1231186: 0x0B1,
        1231187: 0x0B2,
        1231188: 0x0B3,
        1231189: 0x0B4,
        1231190: 0x0B5,
        1231191: 0x0B6,
        1231192: 0x0B7,
        1231193: 0x0B8,
        1231194: 0x0B9,
        1231195: 0x0BA,
        1231196: 0x0BB,
        1231197: 0x0BC,
        1231198: 0x0BD,
        1231199: 0x0BE,
        1231200: 0x0BF,
        1231201: 0x0C0,
        1231202: 0x0C1,
        1231203: 0x0C2,
        1231204: 0x0C3,
        1231205: 0x0C4,
        1231206: 0x0C5,
        1231207: 0x0C6,
        1231208: 0x0C7,
        1231209: 0x0C8,
        1231210: 0x0C9,
        1231211: 0x0CA,
        1231212: 0x0CB,
        1231213: 0x0CC,
        1231214: 0x0CD,
        1231215: 0x0CE,
        1231216: 0x0CF,
        1231217: 0x0D0,
        1231218: 0x0D1,
        1231219: 0x0D2,
        1231220: 0x0D3,
        1231221: 0x0D4,
        1231222: 0x0D5,
        1231223: 0x0D6,
        1231224: 0x0D7,
        1231225: 0x0D8,
        1231226: 0x0D9,
        1231227: 0x0DA,
        1231228: 0x0DB,
        1231229: 0x0DC,
        1231230: 0x0DD,
        1231231: 0x0DE,
        1231232: 0x0DF,
        1231233: 0x0E0,
        1231234: 0x0E1,
        1231235: 0x0E2,
        1231236: 0x0E3,
        1231237: 0x0E4,
        1231238: 0x0E5,
        1231239: 0x0E6,
        1231240: 0x0E7,
        1231241: 0x0E8,
        1231242: 0x0E9,
        1231243: 0x0EA,
        1231244: 0x0EB,
        1231245: 0x0EC,
        1231246: 0x0ED,
        1231247: 0x0EE,
        1231248: 0x0EF,
        1231249: 0x0F0,
        1231250: 0x0F1,
        1231251: 0x0F2,
        1231252: 0x0F3,
        1231253: 0x0F4,
        1231254: 0x0F5,
        1231255: 0x0F6,
        1231256: 0x0F7,
        1231258: 0x0F8,
        1231257: 0x0F9,
        1231259: 0x0FA,
        1231260: 0x0FB,
        1231261: 0x0FC,
        1231262: 0x0FD,
        1231263: 0x0FE,
        1231264: 0x0FF,
        1231265: 0x100,
        1231266: 0x101,
        1231267: 0x102,
        1231268: 0x103,
        1231269: 0x104,
        1231270: 0x105,
        1231271: 0x106,
        1231272: 0x107,
        1231273: 0x108,
        1231274: 0x109,
        1231275: 0x10A,
        1231276: 0x10B,
        1231277: 0x10C,
        1231278: 0x10D,
        1231279: 0x10E,
        1231280: 0x10F,
        1231281: 0x110,
        1231282: 0x111,
        1231283: 0x112,
        1231284: 0x113,
        1231285: 0x114,
        1231286: 0x115,
        1231287: 0x116,
        1231288: 0x117,
        1231289: 0x118,
        1231290: 0x119,
        1231291: 0x11A,
        1231292: 0x11B,
        1231293: 0x11C,
        1231294: 0x11D,
        1231295: 0x11E,
        1231296: 0x11F,
        1231297: 0x120,
        1231298: 0x121,
        1231299: 0x122,
        1231300: 0x123,
        1231301: 0x124,
        1231302: 0x125,
        1231303: 0x126,
        1231304: 0x127,
        1231305: 0x128,
        1231306: 0x129,
        1231307: 0x12A,
        1231308: 0x12B,
        1231309: 0x12C,
        1231310: 0x12D,
        1231311: 0x12E,
        1231312: 0x12F,
        1231313: 0x130,
        1231314: 0x131,
        1231315: 0x132,
        1231316: 0x133,
        1231317: 0x134,
        1231318: 0x135,
        1231319: 0x136,
        1231320: 0x137,
        1231321: 0x138,
        1231322: 0x139,
        1231323: 0x13A,
        1231324: 0x13B,
        1231325: 0x13C,
        1231326: 0x13D,
        1231327: 0x13E,
        1231328: 0x13F,
        1231329: 0x140,
        1231330: 0x141,
        1231331: 0x142,
        1231332: 0x143,
        1231333: 0x144,
        1231334: 0x145,
        1231336: 0x146,
        1231337: 0x147,
        1231339: 0x148,
        1231340: 0x149,
        1231341: 0x14A,
        1231342: 0x14B,
        1231343: 0x14C,
        1231344: 0x14D,
        1231335: 0x14E,
        1231338: 0x14F,
        1231345: 0x150,
        1231346: 0x151,
        1231347: 0x152,
        1231348: 0x153,
        1231349: 0x154,
        1231350: 0x155,
        1231351: 0x156,
        1231352: 0x157,
        1231353: 0x158,
        1231354: 0x159,
        1231355: 0x15A,
        1231356: 0x15B,
        1231357: 0x15C,
        1231358: 0x15D,
        1231360: 0x15E,
        1231361: 0x15F,
        1231362: 0x160,
        1231359: 0x161,
        1231363: 0x162,
        1231364: 0x163,
        1231365: 0x164,
        1231366: 0x165,
        1231367: 0x166,
        1231368: 0x167,
        1231369: 0x168,
        1231370: 0x169,
        1231371: 0x16A,
        1231372: 0x16B,
        1231373: 0x16C,
        1231374: 0x16D,
        1231375: 0x16E,
        1231376: 0x16F,
        1231377: 0x170,
        1231378: 0x171,
        1231379: 0x172,
        1231380: 0x173,
        1231381: 0x174,
        1231382: 0x175,
        1231383: 0x176,
        1231384: 0x177,
        1231385: 0x178,
        1231386: 0x179,
        1231387: 0x17A,
        1231388: 0x17B,
        1231389: 0x17C,
        1231390: 0x17D,
        1231391: 0x17E,
        1231392: 0x17F,
        1231393: 0x180,
        1231394: 0x181,
        1231395: 0x182,
        1231396: 0x183,
        1231397: 0x184,
        1231398: 0x185,
        1231399: 0x186,
        1231400: 0x187,
        1231401: 0x188,
        1231402: 0x189,
        1231403: 0x18A,
        1231404: 0x18B,
        1231405: 0x18C,
        1231406: 0x18D,
        1231407: 0x18E,
        1231408: 0x18F,
        1231409: 0x190,
        1231410: 0x191,
        1231411: 0x192,
        1231412: 0x193,
        1231413: 0x194,
        1231414: 0x195,
        1231415: 0x196,
        1231416: 0x197,
        1231417: 0x198,
        1231418: 0x199,
        1231419: 0x19A,
        1231420: 0x19B,
        1231421: 0x19C,
        1231422: 0x19D,
        1231423: 0x19E,
        1231424: 0x19F,
        1231425: 0x1A0,
        1231426: 0x1A1,
        1231427: 0x1A2,
        1231428: 0x1A3,
        1231429: 0x1A4,
        1231430: 0x1A5,
        1231431: 0x1A6,
        1231432: 0x1A7,
        1231433: 0x1A8,
        1231434: 0x1A9,
        1231435: 0x1AA,
        1231436: 0x1AB,
        1231437: 0x1AC,
        1231438: 0x1AD,
        1231439: 0x1AE,
        1231440: 0x1AF,
        1231441: 0x1B0,
        1231442: 0x1B1,
        1231443: 0x1B2,
        1231444: 0x1B3,
        1231445: 0x1B4,
        1231446: 0x1B5,
        1231447: 0x1B6,
        1231448: 0x1B7,
        1231449: 0x1B8,
        1231450: 0x1B9,
        1231451: 0x1BA,
        1231452: 0x1BC,
        1231453: 0x1BB,
        1231454: 0x1BD,
        1231455: 0x1BE,
        1231456: 0x1BF,
        1231457: 0x1C0,
        1231458: 0x1C1,
        1231459: 0x1C2,
        1231460: 0x1C3,
        1231461: 0x1C4,
        1231462: 0x1C5,
        1231463: 0x1C6,
        1231464: 0x1C7,
        1231466: 0x1C8,
        1231465: 0x1C9,
        1231467: 0x1CA,
        1231468: 0x1CB,
        1231469: 0x1CC,
        1231470: 0x1CD,
        1231471: 0x1CE,
        1231472: 0x1CF,
        1231473: 0x1D0,
        1231474: 0x1D1,
        1231475: 0x1D2,
        1231476: 0x1D3,
        1231477: 0x1D4,
        1231478: 0x1D5,
        1231479: 0x1D6,
        1231480: 0x1D7,
        1231481: 0x1D8,
    },
    "SIGNPOSTS" : {
        1231483: 0x00,
        1231488: 0x01,
        1231486: 0x02,
        1231485: 0x03,
        1231487: 0x04,
        1231484: 0x05,
        1231489: 0x06,
        1231490: 0x07,
        1231491: 0x08,
        1231492: 0x09,
        1231493: 0x0A,
        1231494: 0x0B,
        1231495: 0x0C,
        1231496: 0x0D,
        1231499: 0x0E,
        1231498: 0x0F,
        1231497: 0x10,
        1231500: 0x11,
        1231501: 0x12,
        1231502: 0x13,
        1231503: 0x14,
        1231504: 0x15,
        1231505: 0x16,
        1231508: 0x17,
        1231507: 0x18,
        1231506: 0x19,
        1231509: 0x1A,
        1231510: 0x1B,
        1231511: 0x1C,
        1231512: 0x1D,
        1231513: 0x1E,
        1231514: 0x1F,
        1231516: 0x20,
        1231517: 0x21,
        1231519: 0x22,
        1231518: 0x23,
        1231515: 0x24,
        1231520: 0x25,
        1231521: 0x26,
        1231522: 0x27,
        1231523: 0x28,
        1231524: 0x29,
        1231525: 0x2A,
        1231526: 0x2B,
        1231531: 0x2C,
        1231532: 0x2D,
        1231533: 0x2E,
        1231534: 0x2F,
        1231527: 0x30,
        1231528: 0x31,
        1231529: 0x32,
        1231530: 0x33,
        1231536: 0x34,
        1231535: 0x35,
        1231538: 0x36,
        1231537: 0x37,
        1231539: 0x38,
        1231540: 0x39,
        1231542: 0x3A,
        1231541: 0x3B,
        1231543: 0x3C,
    },
    "WARPSILOS" : {
        "1231550" : {
            addr: 0x60,
            bit: 5,
        },
        "1231551" : {
            addr: 0x60,
            bit: 6,
        },
        "1231552" : {
            addr: 0x60,
            bit: 7,
        },
        "1231553" : {
            addr: 0x61,
            bit: 0,
        },
        "1231554" : {
            addr: 0x61,
            bit: 1,
        },
        "1231555" : {
            addr: 0x61,
            bit: 2,
        },
        "1231556" : {
            addr: 0x61,
            bit: 3,
        },

    },
    "WARPPADS" : {
        "1231557" : {
            addr: 0x70,
            bit: 4,
        },
        "1231558" : {
            addr: 0x70,
            bit: 5,
        },
        "1231559" : {
            addr: 0x70,
            bit: 6,
        },
        "1231560" : {
            addr: 0x70,
            bit: 7,
        },
        "1231561" : {
            addr: 0x71,
            bit: 0,
        },
        "1231562" : {
            addr: 0x71,
            bit: 1,
        },
        "1231563" : {
            addr: 0x71,
            bit: 2,
        },
        "1231564" : {
            addr: 0x71,
            bit: 3,
        },
        "1231565" : {
            addr: 0x71,
            bit: 4,
        },
        "1231566" : {
            addr: 0x71,
            bit: 5,
        },
        "1231567" : {
            addr: 0x71,
            bit: 6,
        },
        "1231568" : {
            addr: 0x71,
            bit: 7,
        },
        "1231569" : {
            addr: 0x72,
            bit: 0,
        },
        "1231570" : {
            addr: 0x72,
            bit: 1,
        },
        "1231571" : {
            addr: 0x72,
            bit: 2,
        },
        "1231572" : {
            addr: 0x72,
            bit: 3,
        },
        "1231573" : {
            addr: 0x72,
            bit: 4,
        },
        "1231574" : {
            addr: 0x72,
            bit: 5,
        },
        "1231575" : {
            addr: 0x72,
            bit: 6,
        },
        "1231576" : {
            addr: 0x72,
            bit: 7,
        },
        "1231577" : {
            addr: 0x73,
            bit: 0,
        },
        "1231578" : {
            addr: 0x73,
            bit: 1,
        },
        "1231579" : {
            addr: 0x73,
            bit: 2,
        },
        "1231580" : {
            addr: 0x73,
            bit: 3,
        },
        "1231581" : {
            addr: 0x73,
            bit: 4,
        },
        "1231582" : {
            addr: 0x73,
            bit: 5,
        },
        "1231583" : {
            addr: 0x73,
            bit: 6,
        },
        "1231584" : {
            addr: 0x73,
            bit: 7,
        },
        "1231585" : {
            addr: 0x74,
            bit: 0,
        },
        "1231586" : {
            addr: 0x74,
            bit: 1,
        },
        "1231587" : {
            addr: 0x74,
            bit: 2,
        },
        "1231588" : {
            addr: 0x74,
            bit: 3,
        },
        "1231589" : {
            addr: 0x74,
            bit: 4,
        },
        "1231590" : {
            addr: 0x74,
            bit: 5,
        },
        "1231591" : {
            addr: 0x74,
            bit: 6,
        },
        "1231592" : {
            addr: 0x74,
            bit: 7,
        },
        "1231593" : {
            addr: 0x75,
            bit: 0,
        },
        "1231594" : {
            addr: 0x75,
            bit: 4,
        },
        "1231595" : {
            addr: 0x75,
            bit: 5,
        },
    },
    "BOGGY_KIDS" : {
        "1231596" : {
            addr: 0x0C,
            bit: 4,
        },
        "1231597" : {
            addr: 0x0C,
            bit: 5,
        },
        "1231598" : {
            addr: 0x0C,
            bit: 6,
        }
    },
    "ALIEN_KIDS" : {
        "1231599" : {
            addr: 0x69,
            bit: 2,
        },
        "1231600" : {
            addr: 0x69,
            bit: 3,
        },
        "1231601" : {
            addr: 0x69,
            bit: 4,
        }
    },
    "SKIVVIES" : {
        "1231602" : {
            addr: 0x81,
            bit: 1,
        },
        "1231603" : {
            addr: 0x81,
            bit: 2,
        },
        "1231604" : {
            addr: 0x80,
            bit: 7,
        },
        "1231605" : {
            addr: 0x81,
            bit: 0,
        },
        "1231606" : {
            addr: 0x80,
            bit: 6,
        },
        "1231607" : {
            addr: 0x80,
            bit: 5,
        },
    },
    "MRFIT" : {
        "1231608" : {
            addr: 0x76,
            bit: 4,
        },
        "1231609" : {
            addr: 0x76,
            bit: 5,
        },
    },
    "BIGTOP_TICKETS" : {
        "1231610" : {
            addr: 0x9C,
            bit: 4
        },
        "1231611" : {
            addr: 0x9C,
            bit: 5
        },
        "1231612" : {
            addr: 0x9C,
            bit: 6
        },
        "1231613" : {
            addr: 0x9C,
            bit: 7
        },
    },
    "GREEN_RELICS" : {
        "1231614" : {
            addr: 0x5A,
            bit: 5,
        },
        "1231615" : {
            addr: 0x5A,
            bit: 4,
        },
        "1231616" : {
            addr: 0x5B,
            bit: 7,
        },
        "1231617" : {
            addr: 0x5B,
            bit: 6,
        },
        "1231618" : {
            addr: 0x5B,
            bit: 5,
        },
        "1231619" : {
            addr: 0x5B,
            bit: 3,
        },
        "1231620" : {
            addr: 0x5B,
            bit: 4,
        },
        "1231621" : {
            addr: 0x5B,
            bit: 2,
        },
        "1231622" : {
            addr: 0x5B,
            bit: 1,
        },
        "1231623" : {
            addr: 0x5C,
            bit: 2,
        },
        "1231624" : {
            addr: 0x5C,
            bit: 3,
        },
        "1231625" : {
            addr: 0x5C,
            bit: 5,
        },
        "1231626" : {
            addr: 0x5C,
            bit: 4,
        },
        "1231627" : {
            addr: 0x5C,
            bit: 6,
        },
        "1231628" : {
            addr: 0x5C,
            bit: 7,
        },
        "1231629" : {
            addr: 0x5C,
            bit: 1,
        },
        "1231630" : {
            addr: 0x5C,
            bit: 0,
        },
        "1231631" : {
            addr: 0x5D,
            bit: 0,
        },
        "1231632" : {
            addr: 0x5D,
            bit: 1,
        },
        "1231633" : {
            addr: 0x5D,
            bit: 2,
        },
        "1231634" : {
            addr: 0x5D,
            bit: 4,
        },
        "1231635" : {
            addr: 0x5D,
            bit: 3,
        },
        "1231636" : {
            addr: 0x5A,
            bit: 6,
        },
        "1231637" : {
            addr: 0x5A,
            bit: 7,
        },
        "1231638" : {
            addr: 0x5B,
            bit: 0,
        },
    },
    "BEANS" : {
        "1231639" : {
            addr: 0x62,
            bit: 6
        },
        "1231640" : {
            addr: 0x62,
            bit: 5
        }
    },
}

// Checks that needs to be checked Per Map. some silos NEEDS other moves as well to get to.
var ASSET_MAP_CHECK = {
    "ALL" : {
        "JIGGIES" : [ //Jinjo Jiggies
            // Jinjos are part of JinjoFAM
            // "1230676", //Jinjo
            // "1230677", //Jinjo
            // "1230678", //Jinjo
            // "1230679", //Jinjo
            // "1230680", //Jinjo
            // "1230681", //Jinjo
            // "1230682", //Jinjo
            // "1230683", //Jinjo
            // "1230684", //Jinjo
            "1230685", //Jingaling
            "1230638", // Scrotty
//                "1230629", // Pig Pool
//                "1230637" // Dippy
        ],
        "JINJO_FAMILY" :[
            "1230676",
            "1230677",
            "1230678",
            "1230679",
            "1230680",
            "1230681",
            "1230682",
            "1230683",
            "1230684"
        ]
    },
    //SPIRAL MOUNTAIN
    0xAF  : { //SM - Spiral Mountain
        "STOPNSWAP" : ["1230956"],
        "JINJOS" : ["1230595"],
        "PAGES" : ["1230752"],
        "ROYSTEN" : [
            "1230777",
            "1230778"
        ],
        "NESTS" : [
            "1231017",
            "1231018",
            "1231019",
            "1231020",
            "1231021",
            "1231022",
            "1231023",
            "1231024",
            "1231025",
            "1231026",
            "1231027",
            "1231028",
            "1231029",
            "1231030",
            "1231031",
            "1231032",
            "1231033",
            "1231034"
        ]
    },
    0xAE : { //SM - Behind the waterfall
        "STOPNSWAP" : ["1230957"]
    },
    0xAD : { //SM - Grunty's Lair
        "CHEATOR" : [
            "1230992",
            "1230993",
            "1230994",
            "1230995",
            "1230996"
        ],
        "NESTS" : [
            "1231010",
            "1231011",
            "1231012",
            "1231013",
            "1231014",
            "1231015",
            "1231016"
        ]
    },
    0x141 : { // SM - Digger Tunnel
        "NESTS" : ["1231035"]
    },
    //JINJO VILLAGE
    0x142 : { // JV
        "TREBLE" : ["1230789"],
        "STOPNSWAP" : ["1230958"],
        "NESTS" : [
            "1231036",
            "1231037",
            "1231038",
            "1231039",
            "1231040",
            "1231041",
            "1231042",
            "1231043",
            "1231044",
            "1231045",
            "1231046",
            "1231047"
        ],
        "SIGNPOSTS" : ["1231483"],
        "WARPSILOS" : ["1231550"],
    },
    0x143 : { //JV - Bottles' House
        "AMAZE" : ["1231005"],
        "NESTS" : [
            "1231048",
            "1231049",
            "1231050",
            "1231051"
        ]
    },
    //ISLE O' HAGS
    0x155 : { //IoH - Cliff Top
        "JINJOS" : ["1230593"],
        "GLOWBO" : ["1230702"],
        "NOTES" : [
            "1230936",
            "1230937",
            "1230938",
            "1230939",
        ],
        "SILO" : [
            "1230763",
        ],
        "STATIONBTN" : ["1230794"],
        "NESTS" : [
            "1231074",
            "1231075",
            "1231076",
            "1231077",
            "1231078",
            "1231079",
            "1231482",
        ],
        "SIGNPOSTS" : ["1231500"],
        "WARPSILOS" : ["1231554"],
    },
    0x150 : { //IoH - Heggy's Egg Shed
        "STOPNSWAP" : [
            "1230953", // Yellow Egg Hatch
            "1230954", // Pink Egg Hatch
            "1230955" // Blue Egg Hatch
        ]
    },
    0x154 : { //IoH - Pine Grove
        "NOTES" : [
            "1230932",
            "1230933",
            "1230934", // underwater 1
            "1230935", // underwater 2

        ],
        "SILO" : [
            "1230759",
        ],
        "NESTS" : [
            "1231068",
            "1231069",
            "1231070",
            "1231071",
            "1231072",
            "1231073",
        ],
        "SIGNPOSTS" : [
            "1231499",
            "1231498",
            "1231497",
        ],
        "WARPSILOS" : ["1231553"],

    },
    0x157 : { // Pine Grove Humba
        "NESTS" : [
            "1231080",
            "1231081",
        ]
    },
    0x152 : { //IoH - Plateau
        "JINJOS" : [
            "1230594" // Plateau Jinjo
        ],
        "HONEYCOMB" : [
            "1230727" // honey
        ],
        "NOTES" : [
            "1230928", // GGM Sign 1
            "1230929", // GGM Sign 2
            "1230930", // Bee 1
            "1230931", // Bee 2
        ],
        "SILO" : [
            "1230756"
        ],
        "NESTS" : [
            "1231061",
            "1231062",
            "1231063",
            "1231064",
            "1231065",
            "1231066",
            "1231067",
        ],
        "WARPSILOS" : ["1231552"],
    },
    0x153 : { //IoH - Plateau - Honey B's Hive
        "HONEYB" : [
            "1230997",
            "1230998",
            "1230999",
            "1231000",
            "1231001"
        ]
    },
    0x15B : { // PG Digger Tunnel
        "NESTS" : [
            "1231090",
            "1231091",
        ]
    },
    0x15A : { //IoH - Wasteland
        "JINJOS" : [
            "1230592" // Wasteland Jinjo
        ],
        "NOTES" : [
            "1230940",
            "1230941",
            "1230942",
            "1230943",

        ],
        "SILO" : [
            "1230767",
        ],
        "NESTS" : [
            "1231082",
            "1231083",
            "1231084",
            "1231085",
            "1231086",
            "1231087",
            "1231088",
            "1231089",
        ],
        "SIGNPOSTS" : ["1231501"],
        "WARPSILOS" : ["1231555"],
    },
    0x14F : { //IoH - Wooded Hollow
        "JINJOS" : [
            "1230591" // Wooded Hollow Jinjo
        ],
        "NESTS" : [
            "1231052",
            "1231053",
            "1231054",
            "1231055",
            "1231056",
            "1231057",
            "1231058",
            "1231059",
            "1231060"
        ],
        "SIGNPOSTS" : [
            "1231488",
            "1231486",
            "1231485",
            "1231487",
            "1231484",
        ],
        "WARPSILOS" : ["1231551"],
    },
    0x151 : { //IoH - Jiggywiggy's Temple
        "SIGNPOSTS" : [
            "1231489",
            "1231490",
            "1231491",
            "1231492",
            "1231493",
            "1231494",
            "1231495",
            "1231496",
        ]
    },
    0x15C : { // Quagmire
        "NESTS" : [
            "1231092",
            "1231093",
            "1231094",
            "1231095",
            "1231096",
            "1231097",
        ],
        "WARPSILOS" : ["1231556"],

    },
    //MAYAHEM TEMPLE
    0xB8 : { //MT
        "JIGGIES" : [
            "1230599",
            "1230604"
        ],
        "JINJOS" : [
            "1230552", // Stadium
            "1230554", // Pool
            "1230555", // Bridge
        ],
        "PAGES" : [
            "1230728" // Top of Treasure Chamber
        ],
        "HONEYCOMB" : [
            "1230703", // Entrance
            "1230704", // Bovina
        ],
        "NOTES" : [
            "1230800", // MT: First Stairs (1)
            "1230801", // MT: First Stairs (2)
            "1230802", // MT: First Stairs (3)
            "1230803", // MT: First Stairs (4)
            "1230804", // MT: Second Stairs (1)
            "1230805", // MT: Second Stairs (2)
            "1230806", // MT: Second Stairs (3)
            "1230807", // MT: Second Stairs (4)
            "1230808", // MT: Third Stairs (1)
            "1230809", // MT: Third Stairs (2)
            "1230810", // MT: Third Stairs (3)
            "1230811", // MT: Third Stairs (4)
            "1230812", // MT: Top Stairs (1)
            "1230813", // MT: Top Stairs (2)
            "1230814", // MT: Top Stairs (3)
            "1230815", // MT: Top Stairs (4)
        ],
        "TREBLE" : [
            "1230781"
        ],
        "SILO" : [
            "1230753",
            "1230754"
        ],
        "NESTS" : [
            "1231102",
            "1231103",
            "1231104",
            "1231105",
            "1231106",
            "1231107",
            "1231108",
            "1231109",
            "1231110",
            "1231111",
        ],
        "SIGNPOSTS" : ["1231503"],
        "WARPPADS" : [
            "1231557",
            "1231558",
        ]
    },
    0xC4 : { //MT - Jade Snake Grove
        "JIGGIES" : [
            "1230601", // Golden Goliath
            "1230605"  // Ssslumber
        ],
        "JINJOS" : [
            "1230551" // Snake Grove
        ],
        "PAGES" : [
            "1230730" // Snake Grove
        ],
        "GLOWBO" : [
            "1230687"
        ],
        "SILO" : [
            "1230755",
        ],
        "NESTS" : [
            "1231119",
            "1231120",
            "1231121",
        ],
        "SIGNPOSTS" : [
            "1231508",
            "1231507",
            "1231506",
        ],
        "WARPPADS" : [
            "1231560",
        ]
    },
    0xB6 : { // MT - Humba
        "NESTS" : [
            "1231098",
            "1231099",
        ]
    },
    0xBB : { //MT - Mayan Kickball Stadium (Lobby)
        "JIGGIES" : [
            "1230598", // Kickball
        ],
        "WARPPADS" : [
            "1231561",
        ]
    },
    0xB7 : { //MT - Mumbo's Skull
        "GLOWBO" : [
            "1230686"
        ],
        "NESTS" : [
            "1231100",
            "1231101",
        ],
        "SIGNPOSTS" : ["1231502"]
    },
    0xB9 : { //MT - Prison Compound
        "JIGGIES" : [
            "1230602", //quicksand
            "1230603", //pillars
        ],
        "PAGES" : [
            "1230729" // Prison
        ],
        "NESTS" : [
            "1231112",
            "1231113",
            "1231114",
            "1231115",
            "1231116",
            "1231117",
            "1231118",
        ],
        "SIGNPOSTS" : [
            "1231504",
            "1231505",
        ],
        "WARPPADS" : [
            "1231559",
        ]
    },
    0x179 : { // MT - Temple Lobby
        "NESTS" : [
            "1231133",
            "1231134",
            "1231135",
            "1231136",
            "1231137",
            "1231138",
        ]
    },
    0x17A :	{ //MT - Targitzan's Really Sacred Chamber
        "JIGGIES" : [
            "1230596" //Targitzan
        ]
    },
    0x177 :	{ //MT - Targitzan's Slightly Sacred Chamber
        "JIGGIES" : [
            "1230597" //Slightly Sacred Chamber
        ]
    },
    0xC5 : { //MT - Treasure Chamber
        "JIGGIES" : [
            "1230600" //Treasure Chamber
        ],
        "HONEYCOMB" : [
            "1230705", // Treasure
        ]
    },
    0x178 : { //MT - Inside Tatgitzan's Temple
        "JINJOS" : [
            "1230553" // Temple Jiggy
        ],
        "NESTS" : [
            "1231122",
            "1231123",
            "1231124",
            "1231125",
            "1231126",
            "1231127",
            "1231128",
            "1231129",
            "1231130",
            "1231131",
            "1231132",
        ],
        "SIGNPOSTS" : [
            "1231509",
            "1231510",
        ],
        "GREEN_RELICS" : [
            "1231614",
            "1231615",
            "1231616",
            "1231617",
            "1231618",
            "1231619",
            "1231620",
            "1231621",
            "1231622",
            "1231623",
            "1231624",
            "1231625",
            "1231626",
            "1231627",
            "1231628",
            "1231629",
            "1231630",
            "1231631",
            "1231632",
            "1231633",
            "1231634",
            "1231635",
            "1231636",
            "1231637",
            "1231638",
        ]
    },
    //GLITTER GULCH MINE

    0xC7 : { //GGM
        "JIGGIES" : [
            "1230607", // Canary Mary
            "1230612", // Crushing Shed
            "1230613" // Waterfall
        ],
        "JINJOS" : [
            "1230559", // Boulder
            "1230560", // Tracks
        ],
        "PAGES" : [
            "1230731", // Canary
            "1230732", // Entrance
        ],
        "HONEYCOMB" : [
            "1230707", // boulder
        ],
        "GLOWBO" : [
            "1230688", // Entrance
            "1230689" // near mumbo
        ],
        "NOTES" : [
            "1230816", // by Crushing Shed (1)
            "1230817", // by Crushing Shed (2)
            "1230818", // by Crushing Shed (3)
            "1230819", // by Crushing Shed (4)
            "1230820", // Hut Bottom-Left Note
            "1230821", // Hut Top-Left Note
            "1230822", // Hut Top-Right Note
            "1230823", // Hut Mid-Right Note
            "1230824", // Hut Bottom-Right Note
            "1230825", // Mumbo (1)
            "1230826", // Mumbo (2)
            "1230827", // Mumbo (3)
        ],
        "SILO" : [
            "1230757",
        ],
        "JCHUNKS" : [
            "1231002",
            "1231003",
            "1231004"
        ],
        "NESTS" : [
            "1231139",
            "1231140",
            "1231141",
            "1231142",
        ],
        "WARPPADS" : [
            "1231562",
            "1231563",
            "1231565",
            "1231566",
        ]
    },
    0xE9 : { //GGM - Humba
        "WARPPADS" : [ "1231564"]
    },
    0xCC :{ //GGM - Flooded Caves
        "JIGGIES" : [
            "1230615" // Flooded Cave
        ],
        "NESTS" : [
            "1231151",
            "1231152",
        ]
    },
    0xCA :{ //GGM - Fuel Depot
        "NOTES" : [
            "1230828", // Front-left
            "1230829", // Back-left
            "1230830", // Back-Right
            "1230831", // Front-Right
        ],
        "NESTS" : [
            "1231143",
            "1231144",
            "1231145",
            "1231146",
            "1231147",
            "1231148",
        ]
    },
    0xCB : { // GGM - Crushing Shed
        "NESTS" : [
            "1231149",
            "1231150",
        ]
    },
    0xD3 : { //GGM - Generator Cavern
        "JIGGIES" : [
            "1230608" // Generator Cavern
        ],
        "NESTS" : [
            "1231158",
        ],
        "SIGNPOSTS" : ["1231512"]
    },
    0xD4 : { //GGM - Power Hut
        "NESTS" : [
            "1231159",
        ]
    },
    0xD2 : { //GGM - Gloomy Caverns
        "JINJOS" : [
            "1230557" // Jail
        ],
        "NESTS" : [
            "1231154",
            "1231155",
            "1231156",
            "1231157",
        ],
        "SIGNPOSTS" : ["1231511"]
    },
    0xD1 : { //GGM - Inside Chuffy's Boiler
        "JIGGIES" : [
            "1230606" // King Coal
        ],
        "CHUFFY" : [
            "1230796"
        ]
    },
    0x163 : { //GGM - Ordnance Storage Entrance
        "JIGGIES" : [
            "1230610" // Ordnance Storage
        ],
        "SILO" : [
            "1230758"
        ],
        "NESTS" : [
            "1231174",
            "1231175",
            "1231176",
        ]
    },
    0xCF : { //GGM - Power Hut Basement
        "JIGGIES" : [
            "1230614" // Power Hut Basement
        ],
    },
    0xD8 : { //GGM - Prospector's Hut
        "JIGGIES" : [
            "1230611" // Dilberta
        ],
        "NESTS" : [
            "1231164",
        ]
    },
    0xD9 : {  // GGM - Mumbo
        "NESTS" : [
            "1231165",
            "1231166",
            "1231167",
        ]
    },
    0xDA : { //GGM - Toxic Gas Cave
        "JINJOS" : [
            "1230558" // Toxic
        ],
        "HONEYCOMB" : [
            "1230706", // boulder
        ],
        "NESTS" : [
            "1231168",
            "1231169",
        ],
        "SIGNPOSTS" : ["1231513"]
    },
    0xDB : { // GGM - Canary Mary
        "NESTS" : [
            "1231170",
            "1231171",
            "1231172",
            "1231173",
        ]
    },
    0xD7 : { //GGM - Train Station
        "HONEYCOMB" : [
            "1230708", // Train
        ],
        "NESTS" : [
            "1231160",
            "1231161",
            "1231162",
            "1231163",
        ]
    },
    0x121 : { //GGM - Chuffy's Wagon,
        "SIGNPOSTS" : ["1231514"]
    },
    0xCD : { //GGM - Water Storage
        "JINJOS" : [
            "1230556" // Water Storage
        ],
        "PAGES" : [
            "1230733" // Water Tower
        ],
        "TREBLE" : [
            "1230782"
        ],
        "NESTS" : [
            "1231153",
        ]
    },
    0xCE : { //GGM - Waterfall Cavern
        "JIGGIES" : [
            "1230609" // Waterfall Cavern
        ],
    },
    0xD0 : {}, // GGM - Chuffy Cabin
    //WITCHYWORLD
    0xD6 : { //WW
        "JIGGIES" : [
            "1230619", // Saucer of Peril
            "1230621", // Dive of Death
            "1230622", // Mrs Boggy
            "1230625", // Cactus of Strength
        ],
        "JINJOS" : [
            "1230561", // Top of Tent
            "1230563", // Van door
            "1230564", // dogdem dome
            "1230565", // Cactus of Strength
        ],
        "PAGES" : [
            "1230736" // Saucer
        ],
        "HONEYCOMB" : [
            "1230709", // Space Zone
        ],
        "NOTES" : [
            "1230832", // Around the Tent (1)
            "1230833", // Around the Tent (2)
            "1230834", // Around the Tent (3)
            "1230835", // Around the Tent (4)
            "1230836", // Around the Tent (5)
            "1230837", // Around the Tent (6)
            "1230838", // Around the Tent (7)
            "1230839", // Around the Tent (8)
            "1230840", // Area 51 Gate (1)
            "1230841", // Area 51 Gate (2)
            "1230842", // Outside Dodgem Dome (1)
            "1230843", // Outside Dodgem Dome (2)
            "1230844", // Dive of Death (1)
            "1230845", // Dive of Death (2)
            "1230846", // Crazy Castle Entrance (1)
            "1230847", // Crazy Castle Entrance (2)
        ],
        "TREBLE" : [
            "1230783"
        ],
        "SILO" : [
            "1230761",
            "1230760"
        ],
        "NESTS" : [
            "1231177",
            "1231178",
            "1231179",
            "1231180",
            "1231181",
            "1231182",
            "1231183",
            "1231184",
            "1231185",
            "1231186",
            "1231187",
            "1231188",
        ],
        "SIGNPOSTS" : [
            "1231516",
            "1231517",
            "1231519",
            "1231518",
            "1231515",
        ],
        "WARPPADS" : [
            "1231567",
            "1231568",
            "1231569",
            "1231570"
        ],
        "BOGGY_KIDS" : [
            "1231596",
            "1231598"
        ],
        "BIGTOP_TICKETS" : [
            "1231610",
            "1231611",
            "1231612",
            "1231613"
        ]
    },
    0xEA : { //WW - Cave of Horrors
        "JINJOS" : [
            "1230562", // Cave of Horrors
        ],
        "SIGNPOSTS" : ["1231521"],
        "BOGGY_KIDS" : ["1231596"]
    },
    0xE1 : { //WW - Crazy Castle Stockade
        "JIGGIES" : [
            "1230616", // Hoop Hurry
            "1230620", // Balloon Burst
        ],
        "HONEYCOMB" : [
            "1230711", // Crazy Castle
        ],
        "SILO" : [
            "1230762",
        ],
        "NESTS" : [
            "1231189",
            "1231190",
        ],
        "BOGGY_KIDS" : ["1231597"]
    },
    0xE3 : { // WW - Pump Room
        "NESTS" : [
            "1231191",
            "1231192",
        ],
        "SIGNPOSTS" : ["1231520"]
    },
    0xDD : { //WW - Dodgem Dome Lobby
        "JIGGIES" : [
            "1230617", // Dodgem
        ],
        "BOGGY_KIDS" : ["1231596"]
    },
    0xEB : { //WW - Haunted Cavern
        "PAGES" : [
            "1230734" // Alcove
        ],
        "NESTS" : [
            "1231198",
            "1231199",
            "1231200",
        ],
        "SIGNPOSTS" : ["1231522"]
    },
    0xF9 : { //WW - Big Top Tent
        "JIGGIES" : [
            "1230618", // Patches
        ],
        "NESTS" : [
            "1231203",
            "1231204",
            "1231205",
            "1231206",
            "1231207",
            "1231208",
            "1231209",
            "1231210",
            "1231211",
            "1231212",
            "1231213",
            "1231214",
            "1231215",
            "1231216",
            "1231217",
            "1231218",
        ]
    },
    0xE6 : { //WW - Star Spinner
        "JIGGIES" : [
            "1230623", // Star Spinner
        ],
        "NESTS" : [
            "1231193",
            "1231194",
            "1231195",
        ],
        "BOGGY_KIDS" : ["1231597"]
    },
    0xE7 : { //WW - The Inferno
        "JIGGIES" : [
            "1230624", // The Inferno
        ],
        "PAGES" : [
            "1230735" // Inferno
        ],
        "GLOWBO" : [
            "1230690" // near mumbo
        ],
        "NESTS" : [
            "1231196",
            "1231197",
        ],
        "WARPPADS" : [
            "1231571"
        ],
        "BOGGY_KIDS" : [
            "1231597",
            "1231598"
        ]
    },
    0x176 : { // WW - Mumbo Skull
        "HONEYCOMB" : [
            "1230710" // Inferno
        ]
    },
    0xD5 : { //WW - Wumba's Wigwam
        "GLOWBO" : [
            "1230691"
        ]
    },
    0xEC : { // WW - Train Station
        "STATIONBTN" : ["1230795"],
        "NESTS" : [
            "1231201",
            "1231202",
        ],
        "BOGGY_KIDS" : ["1231598"]
    },
    //JOLLY ROGER'S LAGOON
    0x1A7 : { //JRL
        "JIGGIES" : [
            "1230627", // Tiptup
            "1230635", // UFO
            "1230629", // Pig Pool
        ],
        "JINJOS" : [
            "1230566", // alcove
        ],
        "HONEYCOMB" : [
            "1230714" // Pipe
        ],
        "DOUBLOON" : [
            "1230521", // Town Center Pole 1
            "1230522", // Town Center Pole 2
            "1230523", // Town Center Pole 3
            "1230524", // Town Center Pole 4
            "1230525", // Town Center Pole 5
            "1230526", // Town Center Pole 6
            "1230527", // Silo 1
            "1230528", // Silo 2
            "1230529", // Silo 3
            "1230530", // Silo 4
            "1230531", // Toxic Pool 1
            "1230532", // Toxic Pool 2
            "1230533", // Toxic Pool 3
            "1230534", // Toxic Pool 4
            "1230539", // Underground 1
            "1230540", // Underground 2
            "1230541", // Underground 3
            "1230542", // Alcove 1
            "1230543", // Alcove 2
            "1230544", // Alcove 3
            "1230547", // Jinjo 1
            "1230548", // Jinjo 2
            "1230549", // Jinjo 3
            "1230550", // Jinjo 4
        ],
        "NOTES" : [
            "1230848", // Outside Jollys
            "1230849", // Outside Pawno
            "1230850", // Outside Blubber
            "1230851", // Blubbul 1
            "1230852", // Blubbul 2
        ],
        "SILO" : [
            "1230764",
        ],
        "NESTS" : [
            "1231245",
        ],
        "SIGNPOSTS" : ["1231526"],
        "WARPPADS" : [
            "1231572"
        ],
    },
    0xF4 : { //JRL - Ancient Swimming Baths
        "PAGES" : [
            "1230739" // Baths
        ]
    },
    0x1A8 :	{ //JRL - Atlantis
        "JIGGIES" : [
            "1230633", // SEEMEE
        ],
        "JINJOS" : [
            "1230570", // Sunken Ship
        ],
        "PAGES" : [
            "1230738" // SEEMEE
        ],
        "HONEYCOMB" : [
            "1230713", // Atlantis
            "1230712", // SEEMEE
        ],
        "GLOWBO" : [
            "1230693" // near humba
        ],
        "NOTES" : [
            "1230853", // Eel 1
            "1230854", // Eel 2
        ],
        "TREBLE" : [
            "1230784"
        ],
        "NESTS" : [
            "1231246",
            "1231247",
            "1231248",
            "1231249",
            "1231250",
            "1231251",
        ],
        "WARPPADS" : [
            "1231573",
            "1231574"
        ],
    },
    0xFF : { //JRL - Blubber's Wave Race Hire
        "JINJOS" : [
            "1230567", // Blubber
        ],
        "NOTES" : [
            "1230855",
            "1230856",
            "1230857",
        ],
        "SIGNPOSTS" : ["1231524"]
    },
    0xF6 : {  //JRL - Electric Eel's lair
        "SILO" : [
            "1230765",
        ],
    },
    0xF8 : { //JRL - Inside the Big Fish
        "JINJOS" : [
            "1230568", // Big Fish
        ],
        "NESTS" : [
            "1231232",
            "1231233",
        ]
    },
    0xED :	{ //JRL - Jolly's
        "JIGGIES" : [
            "1230631", // Merry Maggie
        ],
        "DOUBLOON" : [
            "1230545", // Blackeye 1
            "1230546" // Blackeye 2
        ],
        "NOTES" : [
            "1230861",
            "1230862",
            "1230863",
        ],
        "SILO" : [
            "1230766",
        ],
        "NESTS" : [
            "1231219",
            "1231220",
            "1231221",
            "1231222",
            "1231223",
            "1231224",
        ]
    },
    0xFC :	{ //JRL - Lord Woo Fak Fak
        "JIGGIES" : [
            "1230632", // Lord Woo
        ],
        "NESTS" : [
            "1231238",
            "1231239",
            "1231240",
            "1231241",
        ]
    },
    0xEE :	{ //JRL - Pawno's Emporium
        "JIGGIES" : [
            "1230634", // Pawno
        ],
        "PAGES" : [
            "1230737" // Pawno
        ],
        "GLOWBO" : [
            "1230692"
        ],
        "NOTES" : [
            "1230858",
            "1230859",
            "1230860",
        ],
        "NESTS" : [
            "1231225",
            "1231226",
            "1231227",
        ]
    },
    0x120 : { // JRL - Humba
        "NESTS" : [
            "1231242",
        ]
    },
    0x1A9 :	{ //JRL - Sea Bottom
        "JIGGIES" : [
            "1230633", // SEEMEE
        ],
        "PAGES" : [
            "1230738" // SEEMEE
        ],
        "HONEYCOMB" : [
            "1230712", // SEEMEE
        ],
        "NESTS" : [
            "1231252",
            "1231253",
            "1231254",
            "1231255",
            "1231256",
            "1231257",
            "1231258",
        ],
        "WARPPADS" : [
            "1231575",
            "1231576"
        ],
    },
    0x181 :	{ //JRL - Sea Botom Cavern
        "JIGGIES" : [
            "1230626", // Mini-Sub Challenge
        ],
    },
    0xF7 : { //JRL - Seaweed Sanctum
        "JINJOS" : [
            "1230569", // Seaweed
        ],
        "NESTS" : [
            "1231228",
            "1231229",
            "1231230",
            "1231231",
        ],
        "SIGNPOSTS" : ["1231523"]
    },
    0x1A6 :	{ //JRL - Smuggler's cavern
        "JIGGIES" : [
            "1230633", // SEEMEE
            "1230630", // Smuggler
        ],
        "PAGES" : [
            "1230738" // SEEMEE
        ],
        "HONEYCOMB" : [
            "1230712", // SEEMEE
        ],
        "NESTS" : [
            "1231243",
            "1231244",
        ],
        "SIGNPOSTS" : ["1231525"]
    },
    0xFA : { //JRL - Temple of the Fishes
        "JIGGIES" : [
            "1230628", // Chris P. Bacon
        ],
        "NESTS" : [
            "1231234",
            "1231235",
            "1231236",
            "1231237",
        ]
    },
    0xEF : { //JRL - Mumbo's Skull
        "DOUBLOON" : [
            "1230535", // Mumbo 1
            "1230536", // Mumbo 2
            "1230537", // Mumbo 3
            "1230538" // Mumbo 4
        ]
    },
    //TERRYDACTYLAND
    0x112 :	{ //TDL
        "JIGGIES" : [
            "1230637", // Dippy
            "1230644", // Rocknut
            "1230645", // Dino Code
        ],
        "JINJOS" : [
            "1230571", // Talon Torp
            "1230572", // Entrance
            "1230573", // Maze Cave
            "1230574", // T-rex
        ],
        "PAGES" : [
            "1230740", // Dippy
            "1230742" // Boulder
        ],
        "HONEYCOMB" : [
            "1230715" // Lakeside
        ],
        "GLOWBO" : [
            "1230694", // near unga bunga
            "1230695" // near mumbo
        ],
        "NOTES" : [
            "1230864", // train 1
            "1230865", // train 2
            "1230866", // train 3
            "1230867", // lakeside 1
            "1230868", // lakeside 2
            "1230869", // lakeside 3
            "1230870", // zigzag 1
            "1230871", // zigzag 2
            "1230872", // zigzag 3
            "1230873", // roarpath 1
            "1230874", // roarpath 2
            "1230875", // roarpath 3
        ],
        "TREBLE" : [
            "1230785"
        ],
        "SILO" : [
            "1230768",
        ],
        "STATIONBTN" : ["1230791"],
        "ROAR" : ["1231009"],
        "NESTS" : [
            "1231259",
            "1231260",
            "1231261",
            "1231262",
            "1231263",
            "1231264",
            "1231265",
            "1231266",
            "1231267",
            "1231268",
            "1231269",
            "1231270",
            "1231271",
            "1231272",
            "1231273",
            "1231274",
            "1231275",
            "1231276",
            "1231277",
            "1231278",
        ],
        "SIGNPOSTS" : ["1231527"],
        "WARPPADS" : [
            "1231577",
            "1231579",
            "1231580",
            "1231581"
        ],
    },
    0x123 : { //TDL - Inside Chompa's Belly
        "JIGGIES" : [
            "1230641", // Chompa
        ],
    },
    0x116 : { //TDL - Inside the Mountain
        "JIGGIES" : [
            "1230636", // Under Terry Nest
        ],
        "PAGES" : [
            "1230741", // Mountain
        ],
        "NESTS" : [
            "1231289",
            "1231290",
            "1231291",
            "1231292",
        ],
        "SIGNPOSTS" : [
            "1231528",
            "1231529",
        ]
    },
    0x115 : { //TDL - Oogle Boogles' Cave
        "JIGGIES" : [
            "1230640", // Oogle Boogle Tribe
        ],
        "NESTS" : [
            "1231285",
            "1231286",
            "1231287",
            "1231288",
        ]
    },
    0x117 : { //TDL - River Passage
        "HONEYCOMB" : [
            "1230717" // Riverside
        ],
        "NOTES" : [
            "1230876",
            "1230877",
            "1230878",
            "1230879",
        ],
        "SILO" : [
            "1230769",
        ],
        "NESTS" : [
            "1231293",
        ],
        "SIGNPOSTS" : ["1231530"]
    },
    0x119 : { // Unga Bunga Cave
        "SILO" : [
            "1230770",
        ],
        "NESTS" : [
            "1231297",
            "1231298",
            "1231299",
            "1231300",
            "1231301",
            "1231302",
        ]
    },
    0x11A : { //TDL - Stomping Plains
        "JIGGIES" : [
            "1230643", // Stomping
        ],
        "JINJOS" : [
            "1230575", // Stomping
        ],
        "NESTS" : [
            "1231303",
            "1231304",
            "1231305",
            "1231306",
            "1231307",
            "1231308",
            "1231309",
        ],
        "WARPPADS" : ["1231578"],
    },
    0x118 :	{ //TDL - Styracosaurus Family Cave
        "HONEYCOMB" : [
            "1230716" // Cave
        ],
        "NESTS" : [
            "1231294",
            "1231295",
            "1231296",
        ]
    },
    0x113 :	{ //TDL - Terry's Nest
        "JIGGIES" : [
            "1230639", // Terry
            "1230642", // Terry's Kids
        ],
        "NESTS" : [
            "1231279",
            "1231280",
        ]
    },
    0x114 :	{ //TDL - Train Station
        "JIGGIES" : [
            "1230644", // Rocknut
        ],
        "NESTS" : [
            "1231281",
            "1231282",
            "1231283",
            "1231284",
        ]
    },
    0x11B : { //TDL - Bonfire Cavern
        "NESTS" : [
            "1231310",
            "1231311",
        ]
    },
    0x171 : { // TDL - Mumbo
        "NESTS" : [
            "1231312",
            "1231313",
        ]
    },
    //GRUNTY INDUSTRIES
    0x100 :	{ //GI
        "JIGGIES" : [
            "1230649", // Skivvy
        ],
        "JINJOS" : [
            "1230580" // Outside
        ],
        "HONEYCOMB" : [
            "1230720" // Chimney
        ],
        "TREBLE" : [
            "1230786"
        ],
        "STATIONBTN" : ["1230790"],
        "NESTS" : [
            "1231314",
            "1231315",
            "1231316",
            "1231317",
            "1231318",
        ],
        "SIGNPOSTS" : ["1231531"],
        "WARPPADS" : ["1231586"],
        "SKIVVIES" : ["1231607"]
    },
    0x10F : { //GI - Basement
        "JIGGIES" : [
            "1230647", // Weldar
        ],
        "NOTES" : [
            "1230892",
            "1230893",
        ],
        "NESTS" : [
            "1231369",
            "1231370",
            "1231371",
            "1231372",
            "1231373",
        ]
    },
    0x110 :	{ //GI - Basement (Repair Depot)
        "PAGES" : [
            "1230745" // Repair Depot
        ],
        "NESTS" : [
            "1231374",
            "1231375",
        ]
    },
    0x111 :	{ //GI - Basement (Waste Disposal)
        "JIGGIES" : [
            "1230646", // Underwater Waste Disposal
            "1230655", // Plant Box
            "1230661", // HFP Oil Drill
            "1230629", // Pig Pool
        ],
        "JINJOS" : [
            "1230578" // Waste Disposal
        ],
        "NOTES" : [
            "1230890",
            "1230891",
        ],
        "SILO" : [
            "1230771",
        ],
        "NESTS" : [
            "1231376",
            "1231377",
            "1231378",
            "1231379",
        ]
    },
    0x101 :	{ //GI - Floor 1
        "JIGGIES" : [
            "1230649", // Skivvy
            "1230652", // Floor 1 Guarded
        ],
        "NOTES" : [
            "1230883",
            "1230884",
        ],
        "SILO" : [
            "1230773",
        ],
        "NESTS" : [
            "1231319",
            "1231320",
            "1231321",
            "1231322",
            "1231323",
            "1231324",
        ],
        "WARPPADS" : ["1231582"],
        "SKIVVIES" : ["1231603"]
    },
    0x105 : { //GI - Elevator Shaft
        "NESTS" : [
            "1231332",
            "1231333",
            "1231334",
        ],
        "SIGNPOSTS" : [
            "1231533",
            "1231534",
        ]
    },
    0x106 :	{ //GI - Floor 2
        "JIGGIES" : [
            "1230649", // Skivvy
        ],
        "JINJOS" : [
            "1230577" // leg spring
        ],
        "PAGES" : [
            "1230744" // Floor 2
        ],
        "GLOWBO" : [
            "1230696" // near humba
        ],
        "NOTES" : [
            "1230885",
            "1230886",
            "1230887",
            "1230888",
            "1230889"
        ],
        "SILO" : [
            "1230772",
        ],
        "NESTS" : [
            "1231335",
            "1231336",
            "1231337",
            "1231338",
            "1231339",
            "1231340",
            "1231341",
            "1231342",
            "1231343",
            "1231344",
        ],
        "WARPPADS" : ["1231583"],
        "SKIVVIES" : ["1231604"]

    },
    0x107 : { //GI - Floor 2 Electromagnetic Chamber
        "NESTS" : [
            "1231345",
            "1231346",
            "1231347",
        ]
    },
    0x108 :	{ //GI - Floor 3
        "HONEYCOMB" : [
            "1230718" // Floor 3
        ],
        "GLOWBO" : [
            "1230697" // on boxes
        ],
        "NOTES" : [
            "1230894",
            "1230895"
        ],
        "NESTS" : [
            "1231348",
            "1231349",
            "1231350",
            "1231351",
            "1231352",
            "1231353",
        ],
        "WARPPADS" : ["1231584"],

    },
    0x109 :	{ //GI - Floor 3 (Boiler Plant)
        "JIGGIES" : [
            "1230649", // Skivvy
        ],
        "JINJOS" : [
            "1230579" // Top of Boiler
        ],
        "NESTS" : [
            "1231354",
            "1231355",
        ],
        "SKIVVIES" : ["1231605"]
    },
    0x10A :	{ //GI - Floor 3 (Packing Room)
        "JIGGIES" : [
            "1230654", // Twinkly Packing
        ],
    },
    0x10B :	{ //GI - Floor 4
        "NESTS" : [
            "1231356",
            "1231357",
            "1231358",
            "1231359",
            "1231360",
            "1231361",
            "1231362",
        ],
        "WARPPADS" : ["1231585"],

    },
    0x10D :	{ //GI - Floor 4 (Quality Control)
        "JIGGIES" : [
            "1230651", // Quality Control
        ],
        "NESTS" : [
            "1231363",
            "1231364",
            "1231365",
        ]
    },
    0x10E :	{ //GI - Floor 5
        "JIGGIES" : [
            "1230649", // Skivvy
            "1230650", // Floor 5
        ],
        "JINJOS" : [
            "1230576" // 5 floor
        ],
        "NESTS" : [
            "1231366",
            "1231367",
            "1231368",
        ],
        "SKIVVIES" : ["1231606"]

    },
    0x187 :	{ //GI - Sewer Entrance
        "JIGGIES" : [
            "1230648", // Clinker
        ],
        "NESTS" : [
            "1231388",
            "1231389",
            "1231390",
            "1231391",
        ]
    },
    0x102 :	{ //GI - Train Station
        "HONEYCOMB" : [
            "1230719" // Train
        ],
        "NOTES" : [
            "1230880",
            "1230881",
            "1230882",
        ],
        "NESTS" : [
            "1231325",
            "1231326",
            "1231327",
        ]
    },
    0x104 :	{ //GI - Trash Compactor
        "JIGGIES" : [
            "1230653", // Trash Compactor
        ],
        "NESTS" : [
            "1231330",
            "1231331",
        ]
    },
    0x103 :	{ //GI - Workers' Quarters
        "JIGGIES" : [
            "1230649", // Skivvy
        ],
        "PAGES" : [
            "1230743" // Loggo
        ],
        "NESTS" : [
            "1231328",
            "1231329",
        ],
        "SIGNPOSTS" : ["1231532"],
        "SKIVVIES" : ["1231602"]

    },
    0x162 : { //GI - Clinker's Cavern
        "NESTS" : [
            "1231380",
            "1231381",
            "1231382",
            "1231383",
            "1231384",
            "1231385",
            "1231386",
            "1231387",
        ]
    },
    //HAILFIRE PEAKS
    0x131 :	{ //HFP - Boggy's Igloo
        "JIGGIES" : [
            "1230659", // Boggy
        ],
    },
    0x12B :	{ //HFP - Chilli Billi
        "JIGGIES" : [
            "1230656", // Brothers
        ],
        "NESTS" : [
            "1231414",
        ]
    },
    0x12C :	{ //HFP - Chilly Willy
        "JIGGIES" : [
            "1230656", // Brothers
        ],
        "NESTS" : [
            "1231415",
        ]
    },
    0x132 :	{ //HFP - Icicle Grotto
        "JINJOS" : [
            "1230584", // Grotto
        ],
        "PAGES" : [
            "1230747" // Icicle
        ],
        "TREBLE" : [
            "1230787"
        ],
        "NESTS" : [
            "1231422",
            "1231423",
            "1231424",
            "1231425",
            "1231426",
            "1231427",
        ],
        "WARPPADS" : ["1231591"],
    },
    0x128 :	{ //HFP - Icy Side
        "JIGGIES" : [
            "1230660", // Icy Train Station
            "1230662", // Stomping
            "1230664", // Aliens
        ],
        "JINJOS" : [
            "1230585", // Mildred
            "1230583" // Windy Hole
        ],
        "PAGES" : [
            "1230748" // Ice Pillar
        ],
        "GLOWBO" : [
            "1230699",
            "1230046" // Mega Glowbo
        ],
        "NOTES" : [
            "1230904",
            "1230905",
            "1230906",
            "1230907",
            "1230908",
            "1230909",
            "1230910",
            "1230911",
        ],
        "SILO" : [
            "1230775",
        ],
        "STATIONBTN" : ["1230793"],
        "NESTS" : [
            "1231403",
            "1231404",
            "1231405",
            "1231406",
            "1231407",
            "1231408",
            "1231409",
        ],
        "WARPPADS" : [
            "1231589",
            "1231590"
        ],
        "ALIEN_KIDS" : [
            "1231599",
            "1231600",
            "1231601"
        ]

    },
    0x133 :	{ //HFP - Inside the Volcano
        "JIGGIES" : [
            "1230657", // Volcano
        ],
        "HONEYCOMB" : [
            "1230721" // Volcano
        ],
        "SIGNPOSTS" : [
            "1231538",
            "1231537",
            "1231539",
        ]
    },
    0x12D :	{ //HFP - Kickball Stadium lobby
        "JIGGIES" : [
            "1230663", // Kickball
        ],
        "NESTS" : [
            "1231416",
            "1231417",
            "1231418",
            "1231419",
            "1231420",
            "1231421",
        ]
    },
    0x127 :	{ //HFP - Lava Side
        "JIGGIES" : [
            "1230658", // Sabreman
            "1230665", // Lava waterfall
            "1230629", // Pig Pool
        ],
        "JINJOS" : [
            "1230581", // Lava waterfall
            "1230582" // Boiling Pool
        ],
        "PAGES" : [
            "1230746" // Lava Side
        ],
        "HONEYCOMB" : [
            "1230723" // Lava Side
        ],
        "GLOWBO" : [
            "1230698"
        ],
        "NOTES" : [
            "1230896",
            "1230897",
            "1230898",
            "1230899",
            "1230900",
            "1230901",
            "1230902",
            "1230903",
        ],
        "SILO" : [
            "1230774",
        ],
        "STATIONBTN" : ["1230792"],
        "NESTS" : [
            "1231392",
            "1231393",
            "1231394",
            "1231395",
            "1231396",
            "1231397",
            "1231398",
            "1231399",
            "1231400",
            "1231401",
            "1231402",
        ],
        "SIGNPOSTS" : [
            "1231536",
            "1231535",
        ],
        "WARPPADS" : [
            "1231587",
            "1231588"
        ],
    },
    0x129 :	{ //HFP - Lava Train Station
        "HONEYCOMB" : [
            "1230722" // Train Station
        ],
        "NESTS" : [
            "1231410",
            "1231411",
        ]
    },
    0x12A : { // HFP - Icy Side Station
        "NESTS" : [
            "1231412",
            "1231413",
        ]
    },
    0x135 : { // HFP - Humba
        "NESTS" : [
            "1231430",
            "1231431",
        ]
    },
    0x134 : { // HFP - Mumbo
        "NESTS" : [
            "1231428",
            "1231429",
        ]
    },
    //CLOUD CUCKOOLAND
    0x136 :	{ //CCL
        "JIGGIES" : [
            "1230667", // Mr Fit
            "1230669", // Canary Mary 3
            "1230671", // Jiggium Plant
            "1230675", // Jelly Castle
            "1230637", // Dippy
        ],
        "PAGES" : [
            "1230749" // Canary Mary
        ],
        "HONEYCOMB" : [
            "1230724", // Dirt Patch
            "1230726", // Pot O Gold
            "1230725" // Trash
        ],
        "GLOWBO" : [
            "1230700"
        ],
        "NESTS" : [
            "1231432",
            "1231433",
            "1231434",
            "1231435",
            "1231436",
            "1231437",
            "1231438",
            "1231439",
            "1231440",
            "1231441",
            "1231442",
            "1231443",
            "1231444",
            "1231445",
            "1231446",
            "1231447",
            "1231448",
            "1231449",
            "1231450",
            "1231451",
            "1231452",
            "1231453",
            "1231454",
            "1231455",
            "1231456",
            "1231457",
            "1231458",
            "1231459",
            "1231460",
            "1231461",
            "1231462",
            "1231463",
            "1231464",
            "1231466",
            "1231465",
        ],
        "WARPPADS" : ["1231592"],
        "MRFIT" : [
            "1231608",
            "1231609"
        ],
        "BEANS" : [
            "1231639",
            "1231640"
        ],
    },
    0x13A :	{ //CCL - Central Cavern
        "JIGGIES" : [
            "1230674", // Superstash
        ],
        "JINJOS" : [
            "1230588" // Central
        ],
        "GLOWBO" : [
            "1230701"
        ],
        "NOTES" : [
            "1230912",
            "1230913",
            "1230914",
            "1230915",
            "1230916",
            "1230917",
            "1230918",
            "1230919",
            "1230920",
            "1230921",
            "1230922",
            "1230923",
            "1230924",
            "1230925",
            "1230926",
            "1230927",
        ],
        "TREBLE" : [
            "1230788"
        ],
        "SILO" : [
            "1230776",
        ],
        "NESTS" : [
            "1231471",
            "1231472",
            "1231473",
            "1231474",
            "1231475",
            "1231476",
            "1231477",
        ],
        "SIGNPOSTS" : [
            "1231540",
            "1231542",
            "1231541",
        ],
        "WARPPADS" : ["1231593"],
    },
    0x138 :	{ //CCL - Inside the Cheese Wedge
        "JIGGIES" : [
            "1230672", // Cheese Wedge
        ],
        "JINJOS" : [
            "1230587" // Cheese
        ],
        "NESTS" : [
            "1231469",
            "1231470",
        ]
    },
    0x13D :	{ //CCL - Inside the Pot o' Gold
        "JIGGIES" : [
            "1230668", // pot o gold
        ],
        "PAGES" : [
            "1230750" // O Gold
        ],
        "NESTS" : [
            "1231478",
            "1231479",
        ]
    },
    0x137 :	{ //CCL - Inside the Trash Can
        "JIGGIES" : [
            "1230673", // Trash Can
        ],
        "JINJOS" : [
            "1230586" // Trash
        ],
        "NESTS" : [
            "1231467",
            "1231468",
        ]
    },
    0x13F :	{ //CCL - Mingy Jongo's Skull
        "JIGGIES" : [
            "1230666", // Mingy Jongo
        ],
        "JINJOS" : [
            "1230589" // Mumbo
        ]
    },
    0x13E :	{ //CCL - Mumbo's Skull
        "JIGGIES" : [
            "1230666", // Mingy Jongo
        ],
        "JINJOS" : [
            "1230589" // Mumbo
        ]
    },
    0x140 :	{ //CCL - Wumba's Wigwam
        "JINJOS" : [
            "1230590" // Balasters
        ],
        "NESTS" : [
            "1231480",
            "1231481",
        ],
        "SIGNPOSTS" : ["1231543"]
    },
    0x139 :	{ //CCL - Zubbas' Nest
        "JIGGIES" : [
            "1230670", // Zubba
        ],
        "PAGES" : [
            "1230751" // Zubba
        ]
    },
    0x15D : { // CK Outside
        "WARPPADS" : [
            "1231594",
            "1231595"
        ],
    }
}


//Array contains objects of {Message, Icon}
var MESSAGE_TABLE = [] 


// Properties of world entrances and associated puzzles
var WORLD_ENTRANCE_MAP = {
    "WORLD 1" : {
        defaultName: "Mayahem Temple",
        defaultCost: 1,
        locationId: "0"
    },
    "WORLD 2" : {
        defaultName: "Glitter Gulch Mine",
        defaultCost: 4,
        locationId: "0"
    },
    "WORLD 3" : {
        defaultName: "Witchyworld",
        defaultCost: 8,
        locationId: "0"
    },
    "WORLD 4" : {
        defaultName: "Jolly Roger's Lagoon",
        defaultCost: 14,
        locationId: "0"
    },
    "WORLD 5" : {
        defaultName: "Terrydactyland",
        defaultCost: 20,
        locationId: "0"
    },
    "WORLD 6" : {
        defaultName: "Grunty Industries",
        defaultCost: 28,
        locationId: "0"
    },
    "WORLD 7" : {
        defaultName: "Hailfire Peaks",
        defaultCost: 36,
        locationId: "0"
    },
    "WORLD 8" : {
        defaultName: "Cloud Cuckooland",
        defaultCost: 45,
        locationId: "0"
    },
    "WORLD 9" : {
        defaultName: "Cauldron Keep",
        defaultCost: 55,
        locationId: "0"
    }
}

/////////////// Used for randomized maps
var MAP_ENTRANCES = {
    0xB8 : {
        name:"Mayahem Temple",
        entranceId:10,
        exitId:2,
        exitMap:0x14F,
        access:[],
        reverse_access:[],
    },
    0xC7 : {
        name: "Glitter Gulch Mine",
        entranceId: 17,
        exitId: 2,
        exitMap: 0x152,
        access: [],
        reverse_access: [],
    },
    0xD6 : {
        name: "Witchyworld",
        entranceId: 18,
        exitId: 2,
        exitMap: 0x154,
        access: [],
        reverse_access: [],
    },
    0x1A7 : {
        name: "Jolly Roger's Lagoon - Town Center",
        entranceId: 3,
        exitId: 5,
        exitMap: 0x155,
        access: [],
        reverse_access: [],
    },
    0x112 : {
        name: "Terrydactyland",
        entranceId: 23,
        exitId: 2,
        exitMap: 0x15A,
        access: [],
        reverse_access: [],
    },
    0x100 : {
        name: "Outside Grunty Industries",
        entranceId: 9,
        exitId: 2,
        exitMap: 0x15C,
        access: [],
        reverse_access: [],
    },
    0x127 : {
        name: "Hailfire Peaks",
        entranceId: 21,
        exitId: 6,
        exitMap: 0x155,
        access: [],
        reverse_access: [],
    },
    0x136 : {
        name: "Cloud Cuckooland",
        entranceId: 20,
        exitId: 5,
        exitMap: 0x15A,
        access: [],
        reverse_access: [],
    },
    0x15D : {
        name: "Cauldron Keep",
        entranceId: 1,
        exitId: 3,
        exitMap: 0x15C,
        access: [],
        reverse_access: [],
    },
    0x17A : {
        name: "Targitzan's Really Sacred Chamber",
        entranceId: 1,
        exitId: 2,
        exitMap: 0x178,
        access: [ITEM_TABLE["AP_ITEM_BBLASTER"]],
        reverse_access: [ITEM_TABLE["AP_ITEM_BBLASTER"]],
    },
    0x0D1 : {
        name: "Inside Chuffy's Boiler",
        entranceId: 1,
        exitId: 2,
        exitMap: 0x0D0,
        access: [],
        reverse_access: [],
    },
    0x0F9 : {
        name: "Big Top Interior",
        entranceId: 1,
        exitId: 3,
        exitMap: 0x0D6,
        access: [],
        reverse_access: [],
    },
    0x0FC : {
        name: "Davy Jones' Locker",
        entranceId: 1,
        exitId: 0x28, //different lockers
        exitMap: 0x1A9,
        access: [ITEM_TABLE["AP_ITEM_GEGGS"], ITEM_TABLE["AP_ITEM_AUQAIM"]],
        reverse_access: [],
    },
    0x113 : {
        name: "Terry's Nest",
        entranceId: 0x05,
        exitId: 0x14,
        exitMap: 0x112,
        access: [],
        reverse_access: [],
    },
    0x110: {
        name: "Repair Depot",
        entranceId: 1,
        exitId: 3,
        exitMap: 0x10F,
        access: [ITEM_TABLE["AP_ITEM_GEGGS"]],
        reverse_access: [],
    },
    0x12B : {
        name: "Chilli Billi Crater",
        entranceId: 1,
        exitId: 0x16,
        exitMap: 0x127,
        access: [ITEM_TABLE["AP_ITEM_IEGGS"]],
        reverse_access: [],
    },
    0x12C : {
        name: "Chilly Willy Crater",
        entranceId: 1,
        exitId: 0x0C,
        exitMap: 0x128,
        access: [],
        reverse_access: [],
    },
    0x13F : {
        name: "Mingy Jongo Skull",
        entranceId: 1,
        exitId: 0x09,
        exitMap: 0x136,
        access: [],
        reverse_access: [],
    },
}

var BTH = {
    RDRAMBase: 0x80000000,
    RDRAMSize: 0x800000,
    base_index: 0x80400000,
    
    version: 0x0,
    pc: 0x4,
        pc_death_us: 0x0,
        pc_death_ap: 0x1,
        pc_tag_us: 0x2,
        pc_tag_ap: 0x3,
        pc_show_txt: 0x4,
    pc_messages: 0x8,
    signpost_messages: 0xC,
    pc_settings: 0x10,
        setting_seed: 0x0,
        setting_victory_condition: 0x4,
        setting_chuffy: 0x5,
        setting_nests: 0x6,
        setting_warppads: 0x7,
        setting_warpsilos: 0x8,
        setting_honeyb_rewards: 0x9,
        setting_cheato_rewards: 0xA,
        setting_randomize_tickets: 0xB,
        setting_randomize_green_relics: 0xC,
        setting_randomize_beans: 0xD,
        setting_puzzle: 0xE,
        setting_backdoors: 0xF,
        setting_gi_open_frontdoor: 0x10,
        setting_klungo: 0x11,
        setting_tot: 0x12,
        setting_minigames: 0x13,
        setting_dialog_character: 0x14,
        setting_max_mumbo_tokens: 0x15,
        setting_signpost_hints: 0x16,
        setting_extra_cheats: 0x17,
        setting_automatic_cheats: 0x18,
        setting_easy_canary: 0x19,
        setting_jiggy_requirements: 0x1A,
        setting_silo_requirements: 0x26,
    pc_items: 0x14,
    pc_traps: 0x18,
    pc_exit_map: 0x1C,
        exit_on_map: 0x0,
        exit_og_map: 0x2,
        exit_to_map: 0x4,
        exit_og_exit: 0x6,
        exit_to_exit: 0x7,
        exit_access_rules: 0x8,
        exit_access_rules_size: 0x6,
        exit_map_struct_size: 0xE,
        world_index: 0,
    n64: 0x20,
        n64_show_text: 0x0,
        n64_death_us: 0x1,
        n64_death_ap: 0x2,
        n64_tag_us: 0x3,
        n64_tag_ap: 0x4,
        current_map: 0x6,
    real_flags: 0x24,
    fake_flags: 0x28,
    nest_flags: 0x2C,
    signpost_flags: 0x30,

    txt_queue: 0
}

function isPointer(value)
{
    return value >= BTH.RDRAMBase && value < BTH.RDRAMBase + BTH.RDRAMSize;
}

function dereferencePointer(addr)
{
    if (addr >= 0 && addr < ((BTH.RDRAMBase + BTH.RDRAMSize) - 4))
    {
        var address = mem.u32[addr];
        if (isPointer(address))
            return address;
        else
        {
            if (DEBUGLVL3)
            {
                console.print("Failed to Defref:")
                console.print(address)
            }
            return null;
        }
    }
    else
    {
        if (DEBUGLVL3)
        {
            console.print("Number too big or not number:")
            console.print(addr.toString())
        }
        return null;
    }
}

function getNestPointer()
{
    var hackPointerIndex = dereferencePointer(BTH.base_index);
	return dereferencePointer(BTH.nest_flags + hackPointerIndex);
}

function getSignpostPointer()
{
    var hackPointerIndex = dereferencePointer(BTH.base_index);
	return dereferencePointer(BTH.signpost_flags + hackPointerIndex);
}

function getSettingPointer()
{
    var hackPointerIndex = dereferencePointer(BTH.base_index);
    if (hackPointerIndex == null)
        return
	return dereferencePointer(BTH.pc_settings + hackPointerIndex);
}

function getSetting(setting_offset)
{
    var addr = getSettingPointer()
    if (addr == null)
    {
        console.print("unable to get Setting Ptr")
    }
    return mem.u8[addr + setting_offset]
}

function writeSetting(setting_offset, value)
{
    if(setting_offset == BTH.setting_seed)
    {
        mem.u32[getSettingPointer() + setting_offset] = value
    }
    else
        mem.u8[getSettingPointer() + setting_offset] = value
}

function setSettingJiggyRequirements(index, jiggy_requirements)
{
    mem.u8[getSettingPointer() + BTH.setting_jiggy_requirements + index] = jiggy_requirements  
}

function setSettingSiloRequirements(index, silo_requirements)
{
    mem.u16[getSettingPointer() + BTH.setting_silo_requirements + (index*2)] =  silo_requirements;
}

// returns true if 'target' has a 'value' at 'position'
function checkBit(target, position) {
    return (target >> position & 1) === 1;
}

function bitSet(num, bit){
    return num | 1<<bit;
}

function checkFakeFlag(offset, byte)
{
    var hackPointerIndex = dereferencePointer(BTH.base_index);
	var fakeptr = dereferencePointer(BTH.fake_flags + hackPointerIndex);
    if (fakeptr == null)
        return false
    var currentValue = mem.u8[fakeptr + offset];
    if (checkBit(currentValue, byte))
        return true;
    return false;
}

function checkRealFlag(offset, byte)
{
    var hackPointerIndex = dereferencePointer(BTH.base_index);
	var realptr = dereferencePointer(BTH.real_flags + hackPointerIndex);
    var currentValue = mem.u8[realptr + offset];
    if (checkBit(currentValue, byte))
        return true;
    return false;
}

function checkNestFlag(bytebit)
{
    var offset_byte = Math.floor(bytebit / 8)
    var bitbit = bytebit % 8

    var nest_addr = getNestPointer()
    var currentValue = mem.u8[nest_addr + offset_byte];
    if (checkBit(currentValue, bitbit))
        return true;
    return false;
}

function checkSignpostFlag(bytebit)
{
    var offset_byte = Math.floor(bytebit / 8)
    var bitbit = bytebit % 8

    var signpost_addr = getSignpostPointer()
    var currentValue = mem.u8[signpost_addr + offset_byte];
    if (checkBit(currentValue, bitbit))
        return true;
    return false;
}

function getItemsPointer()
{
    var hackPointerIndex = dereferencePointer(BTH.base_index);
	return dereferencePointer(BTH.pc_items + hackPointerIndex);
}

function getItem(index)
{
    return mem.u8[index + getItemsPointer()];
}

function setItem(index, value)
{
    mem.u8[index + getItemsPointer()] = value;
}

function getMap()
{
    var hackPointerIndex = dereferencePointer(BTH.base_index);
    if (hackPointerIndex == null)
        return 0x0
	var n64_ptr = dereferencePointer(BTH.n64 + hackPointerIndex);
    return mem.u16[n64_ptr + BTH.current_map]
}

function getTrapPointer()
{
    var hackPointerIndex = dereferencePointer(BTH.base_index);
    if (hackPointerIndex == null)
        return null
	return dereferencePointer(BTH.pc_traps + hackPointerIndex);
}

function sendTrap(index, value)
{
    mem.u8[index + getTrapPointer()] = value;
}

//Test this function closely
function setWorldEntrance(currentWorldId, newWorldId, entranceId, currentMap, newEntanceId, access)
{
    var hackPointerIndex = dereferencePointer(BTH.base_index);
    if (hackPointerIndex == null)
        return false
    var exit_maps_ptr = dereferencePointer(BTH.pc_exit_map + hackPointerIndex);
    if (exit_maps_ptr == null)
        return false

    var world_index = BTH.world_index * BTH.exit_map_struct_size
    BTH.world_index = BTH.world_index + 1
    mem.u16[exit_maps_ptr + world_index + BTH.exit_on_map] = currentMap
    mem.u16[exit_maps_ptr + world_index + BTH.exit_og_map] = currentWorldId
    mem.u16[exit_maps_ptr + world_index + BTH.exit_to_map] = newWorldId
    mem.u8[exit_maps_ptr + world_index + BTH.exit_to_exit] = newEntanceId
    mem.u8[exit_maps_ptr + world_index + BTH.exit_og_exit] = entranceId
    var new_value
    for(var i=0; i <access.length;i++)
    {
        var move_id = access[i]
        var offset_byte = Math.floor(move_id / 8)
        var bitbit = move_id % 8
        var currentValue = mem.u8[exit_maps_ptr + world_index + BTH.exit_access_rules + offset_byte];
        new_value = bitSet(currentValue, bitbit) //check if this work as intended...
        mem.u8[exit_maps_ptr + world_index + BTH.exit_access_rules + offset_byte] = new_value
    }
    if (new_value == null)
    {
        for(offset_byte=0; offset_byte <= BTH.exit_access_rules_size-1; offset_byte++)
        {
            mem.u8[exit_maps_ptr + world_index + BTH.exit_access_rules + offset_byte] = 0
        }
    }
    return true
}

function getPCPointer()
{
    var hackPointerIndex = dereferencePointer(BTH.base_index)
    if (hackPointerIndex == null)
        return null
	return dereferencePointer(BTH.pc + hackPointerIndex)
}

function getPCMsgPointer()
{
    var hackPointerIndex = dereferencePointer(BTH.base_index)
    if (hackPointerIndex == null)
        return null
	return dereferencePointer(BTH.pc_messages + hackPointerIndex)
}

function getPCHintPointer()
{
    var hackPointerIndex = dereferencePointer(BTH.base_index)
    if (hackPointerIndex == null)
        return null
	return dereferencePointer(BTH.signpost_messages + hackPointerIndex)
}

function getPCDeath()
{
    var pcptr = getPCPointer()
    if (pcptr != null)
        return mem.u8[getPCPointer() + BTH.pc_death_us]
    else
        return getNLocalDeath()
}

function getPCTag()
{
    return mem.u8[getPCPointer() + BTH.pc_tag_us]
}

function setPCDeath(DEATH_COUNT)
{
    mem.u8[getPCPointer() + BTH.pc_death_us] = DEATH_COUNT
}

function setPCTag(TAG_COUNT)
{
    mem.u8[getPCPointer() + BTH.pc_tag_us] = TAG_COUNT
}

function getAPDeath()
{
   return mem.u8[getPCPointer() + BTH.pc_death_ap]
}

function getAPTag()
{
   return mem.u8[getPCPointer() + BTH.pc_tag_ap]
}

function setAPDeath(DEATH_COUNT)
{
    mem.u8[getPCPointer() + BTH.pc_death_ap] = DEATH_COUNT
}

function setAPTag(TAG_COUNT)
{
    mem.u8[getPCPointer() + BTH.pc_tag_ap] = TAG_COUNT
}

function getNPointer()
{
    var hackPointerIndex = dereferencePointer(BTH.base_index);
    if (hackPointerIndex == null)
        return
	return dereferencePointer(BTH.n64 + hackPointerIndex);
}

function getNLocalDeath()
{
    var ptptr = getNPointer()
    if (ptptr != null)
        return mem.u8[getNPointer() + BTH.n64_death_us];
    else
        return
}

function getNLocalTag()
{
   return mem.u8[getNPointer() + BTH.n64_tag_us];
}

function setTextQueue(icon_id)
{
    BTH.txt_queue = BTH.txt_queue + 1
    writeSetting(BTH.setting_dialog_character, icon_id)
    mem.u8[getPCPointer() + BTH.pc_show_txt] = BTH.txt_queue
}

function getCurrentQueue()
{
    var ptr = getNPointer()
    if (ptr == null)
        return 0
    return mem.u8[ptr + BTH.n64_show_text];
}

function getPCQueue()
{
    return BTH.txt_queue
}

function setDialog(message, icon_id)
{

    var uppcase_text = message.toUpperCase()
    var overflow = false
    var last_char = 0
    for(var idx = 0; idx < uppcase_text.length; idx++)
    {
        if (idx == 507)
        {
            overflow = true
            mem.u8[getPCMsgPointer() + idx] = 0;
            break;
        }
        last_char = last_char + 1;
        mem.u8[getPCMsgPointer() + idx] = uppcase_text.charCodeAt(idx)
    }
    if (overflow == false)
        mem.u8[getPCMsgPointer() + last_char] = 0
    setTextQueue(icon_id)
}

function setHintMessages(sign_id, message)
{
    var uppcase_text = message.toUpperCase()
    var overflow = false
    var last_char = 0
    for(var idx = 0; idx < uppcase_text.length; idx++)
    {
        if(idx == 150)
        {
            overflow = true
            mem.u8[(getPCHintPointer() + sign_id*150 ) + idx] = 0;
            break;
        }
        last_char = last_char + 1;
        mem.u8[(getPCHintPointer() + sign_id*150 ) + idx] = uppcase_text.charCodeAt(idx);
    }
    if(overflow == false)
       mem.u8[(getPCHintPointer() + sign_id*150 ) + last_char] = 0;
}

function getRomVersion()
{
    var hackPointerIndex = dereferencePointer(BTH.base_index);
    if (hackPointerIndex == null)
        return "0"
	var major = mem.u16[BTH.version + hackPointerIndex];
    var minor = mem.u8[BTH.version + 2 + hackPointerIndex]
    var patch = mem.u8[BTH.version + 3 + hackPointerIndex]
    if (patch == 0)
        return major.toString()+"."+minor.toString()
    else
        return major.toString()+"."+minor.toString()+"."+patch.toString()
}


////////////////////////////////// JIGGIES /////////////////////////////////

function obtain_AP_JIGGY()
{
    if(DEBUG_JIGGY == true)
        console.print("Jiggy Obtained")
    TOTAL_JIGGY = TOTAL_JIGGY + 1
    setItem(ITEM_TABLE["AP_ITEM_JIGGY"], TOTAL_JIGGY)
}

function jiggy_check()
{
    var checks = {}
    if(ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if(ASSET_MAP_CHECK[CURRENT_MAP]["JIGGIES"] != undefined)
        {
            for(var i=0; i< ASSET_MAP_CHECK[CURRENT_MAP]["JIGGIES"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["JIGGIES"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["JIGGIES"][locationId].addr, ADDRESS_MAP["JIGGIES"][locationId].bit)
                if (DEBUG_JIGGY == true)
                    console.print(ADDRESS_MAP["JIGGIES"][locationId].name +":"+checks[locationId].toString())
            }
        }
    }
    for(var i=0; i < ASSET_MAP_CHECK["ALL"]["JIGGIES"].length; i++)
    {
        var locationId = ASSET_MAP_CHECK["ALL"]["JIGGIES"][i]
        checks[locationId] = checkRealFlag(ADDRESS_MAP["JIGGIES"][locationId].addr, ADDRESS_MAP["JIGGIES"][locationId].bit)
    }
    return checks
}

//////////////////////////////// TREBLE ////////////////////////////////

function obtain_AP_TREBLE()
{
    if (DEBUG_TREBLE)
        console.print("Treble Obtained")
    TOTAL_TREBLE = TOTAL_TREBLE + 1
    setItem(ITEM_TABLE["AP_ITEM_TREBLE"], TOTAL_TREBLE)
}

function treble_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["TREBLE"] != undefined)
        {
            for(var i=0; i < ASSET_MAP_CHECK[CURRENT_MAP]["TREBLE"].length; i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["TREBLE"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["TREBLE"][locationId].addr, ADDRESS_MAP["TREBLE"][locationId].bit)
                if (DEBUG_TREBLE)
                    console.print(ADDRESS_MAP["TREBLE"][locationId].name + ":" + checks[locationId].toString())
            }
        }
    }
    return checks
}

////////////////////////Roysten ////////////////////////

function roysten_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["ROYSTEN"] != undefined)
        {
            for(var i=0;i< ASSET_MAP_CHECK[CURRENT_MAP]["ROYSTEN"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["ROYSTEN"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["ROYSTEN"][locationId].addr, ADDRESS_MAP["ROYSTEN"][locationId].bit)
                if (DEBUG_ROYSTEN)
                    console.print(ADDRESS_MAP["ROYSTEN"][locationId].name + ":" + checks[locationId].toString())
            }
        }
    }
    return checks
}

function obtain_roysten_moves(itemId)
{
    if (itemId == 1230831)
    {
        if (getItem(ITEM_TABLE["AP_ITEM_DIVE"]) == 0)
            BTH:setItem(ITEM_TABLE["AP_ITEM_DIVE"], 1)
        else if (getItem(ITEM_TABLE["AP_ITEM_DAIR"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_DAIR"], 1)
        else if (getItem(ITEM_TABLE["AP_ITEM_FSWIM"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_FSWIM"], 1)
    }
    else if (itemId == 1230777)
        setItem(ITEM_TABLE["AP_ITEM_FSWIM"], 1)
    else if (itemId == 1230778)
        setItem(ITEM_TABLE["AP_ITEM_DAIR"], 1)
}

//////////////////////////////// AMAZE-O-GAZE ////////////////////////////////////

function amaze_check() // returns true or false
{
    var check = false
    if(ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["AMAZE"] != undefined)
        {
            for(var i=0; i < ASSET_MAP_CHECK[CURRENT_MAP]["AMAZE"].length; i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["AMAZE"][i]
                check = checkFakeFlag(ADDRESS_MAP["AMAZE"][locationId].addr, ADDRESS_MAP["AMAZE"][locationId].bit)
                if (DEBUG_AMAZE)
                    console.print(ADDRESS_MAP["AMAZE"][locationId].name + ":" + check.toString())
            }  
        }
    }
    return check
}

function obtain_amaze_o_gaze()
{
    setItem(ITEM_TABLE["AP_ITEM_AMAZEOGAZE"], 1)
}

//////////////////////////////// ROAR ////////////////////////////////////////////

function roar_check() // returns true or false
{
    var check = false
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if(ASSET_MAP_CHECK[CURRENT_MAP]["ROAR"] != undefined)
        {
            for(var i=0; i < ASSET_MAP_CHECK[CURRENT_MAP]["ROAR"].length; i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["JCHUNKS"][i]
                check = checkFakeFlag(ADDRESS_MAP["ROAR"][locationId].addr, ADDRESS_MAP["ROAR"][locationId].bit)
                if (DEBUG_AMAZE)
                    console.print(ADDRESS_MAP["ROAR"][locationId].name + ":" + check.toString())
            }
        }
    }
    return check
}

function obtain_roar()
{
    setItem(ITEM_TABLE["AP_ITEM_ROAR"], 1)
}


////////////////////////////// PAGES //////////////////////////////

function pages_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if(ASSET_MAP_CHECK[CURRENT_MAP]["PAGES"] != undefined)
        {
            for(var i=0; i < ASSET_MAP_CHECK[CURRENT_MAP]["PAGES"].length; i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["PAGES"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["PAGES"][locationId].addr, ADDRESS_MAP["PAGES"][locationId].bit)
                if(DEBUG_PAGES)
                    console.print(ADDRESS_MAP["PAGES"][locationId].name+":"+ checks[locationId].toString())
            }
        }
    }
    return checks
}

function obtain_AP_PAGES()
{
    if(DEBUG_PAGES)
        console.print("Cheato Page Obtained")
    TOTAL_PAGES = TOTAL_PAGES + 1
    setItem(ITEM_TABLE["AP_ITEM_PAGES"], TOTAL_PAGES)
}

////////////////////////////// CHEATO REWARDS //////////////////////////////

function cheato_rewards_check()
{
    var checks = {}
    if(ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["CHEATOR"] != undefined)
        {
            for(var i=0; i < ASSET_MAP_CHECK[CURRENT_MAP]["CHEATOR"];i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["CHEATOR"][i]
                checks[locationId] = checkFakeFlag(ADDRESS_MAP["CHEATO"][locationId].addr, ADDRESS_MAP["CHEATO"][locationId].bit)
                if(DEBUG_CHEATO)
                    console.print(ADDRESS_MAP["CHEATO"][locationId].name + ":"+ checks[locationId].toString())
            }
        }
    }
    return checks
}

function obtain_cheats(itemId)
{
    if (itemId == 1230917)
        setItem(ITEM_TABLE["AP_ITEM_CHEATFEATHER"], 1)
    if (itemId == 1230918)
        setItem(ITEM_TABLE["AP_ITEM_CHEATEGG"], 1)
    if (itemId == 1230919)
        setItem(ITEM_TABLE["AP_ITEM_CHEATFALL"], 1)
    if (itemId == 1230920)
        setItem(ITEM_TABLE["AP_ITEM_CHEATHONEY"], 1)
    if (itemId == 1230921)
        setItem(ITEM_TABLE["AP_ITEM_CHEATJUKE"], 1)
}

////////////////////////////// HONEYCOMBS //////////////////////////////

function honeycomb_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if(ASSET_MAP_CHECK[CURRENT_MAP]["HONEYCOMB"] != undefined)
        {
            for(var i=0; i < ASSET_MAP_CHECK[CURRENT_MAP]["HONEYCOMB"].length; i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["HONEYCOMB"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["HONEYCOMB"][locationId].addr, ADDRESS_MAP["HONEYCOMB"][locationId].bit)
                if(DEBUG_HONEY)
                   console.print(ADDRESS_MAP["HONEYCOMB"][locationId].name+":"+ checks[locationId].toString())
            }
        }
    }
    return checks
}

function obtained_AP_HONEYCOMB()
{
    if(DEBUG_HONEYCOMB)
        console.print("Obtain HC")
    TOTAL_HONEYCOMBS = TOTAL_HONEYCOMBS + 1
    setItem(ITEM_TABLE["AP_ITEM_HONEY"], TOTAL_HONEYCOMBS)
}

////////////////////////////// HONEY B REWARDS ///////////////////////////////////

function honey_b_check()
{
    var checks = {}
    var bit1 = 0
    var bit2 = 0
    var bit3 = 0
    var base_location_id = 1230996
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["HONEYB"] != undefined)
        {
            var result_bit1 = checkFakeFlag(0x98, 2)
            var result_bit2 = checkFakeFlag(0x98, 3)
            var result_bit3 = checkFakeFlag(0x98, 4)
            if (result_bit1)
                bit1 = 1
            if (result_bit2)
                bit2 = 2
            if (result_bit3)
                bit3 = 4
            var final_res = bit1 + bit2 + bit3
            for(var i = 1230997; i <= final_res + base_location_id; i++)
            {
                checks[tostring(i)] = true
            }
        }
    }
    return checks
}

function obtained_AP_HEALTHUPGRADE()
{
    if (DEBUG_HEALTHUPGRADE)
        console.print("Obtain Health Upgrade")
    TOTAL_HEALTHUPGRADE = TOTAL_HEALTHUPGRADE + 1
    setItem(ITEM_TABLE["AP_ITEM_HEALTHUP"], TOTAL_HEALTHUPGRADE)
}


////////////////////////////// GLOWBO AND MAGIC //////////////////////////////

function glowbo_check()
{
    var checks = {}
    if(ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if(ASSET_MAP_CHECK[CURRENT_MAP]["GLOWBO"] != undefined)
        {
            for(var i=0;i < ASSET_MAP_CHECK[CURRENT_MAP]["GLOWBO"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["GLOWBO"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["GLOWBO"][locationId].addr, ADDRESS_MAP["GLOWBO"][locationId].bit)
                if (DEBUG_GLOWBO)
                    console.print(ADDRESS_MAP["GLOWBO"][locationId].name+":"+checks[locationId].toString())
            }
        }
    }
    return checks
}

function obtain_AP_MAGIC(itemId)
{
    if (itemId == 1230855)
        setItem(ITEM_TABLE["AP_ITEM_MUMBOMT"], 1)
    else if (itemId == 1230856)
        setItem(ITEM_TABLE["AP_ITEM_MUMBOGM"], 1)
    else if (itemId == 1230857)
        setItem(ITEM_TABLE["AP_ITEM_MUMBOWW"], 1)
    else if (itemId == 1230858)
        setItem(ITEM_TABLE["AP_ITEM_MUMBOJR"], 1)
    else if (itemId == 1230859)
        setItem(ITEM_TABLE["AP_ITEM_MUMBOTD"], 1)
    else if (itemId == 1230860)
        setItem(ITEM_TABLE["AP_ITEM_MUMBOGI"], 1)
    else if (itemId == 1230861)
        setItem(ITEM_TABLE["AP_ITEM_MUMBOHP"], 1)
    else if (itemId == 1230862)
        setItem(ITEM_TABLE["AP_ITEM_MUMBOCC"], 1)
    else if (itemId == 1230863)
        setItem(ITEM_TABLE["AP_ITEM_MUMBOIH"], 1)

    else if (itemId == 1230174)
        setItem(ITEM_TABLE["AP_ITEM_HUMBAMT"], 1)
    else if (itemId == 1230175)
        setItem(ITEM_TABLE["AP_ITEM_HUMBAGM"], 1)
    else if (itemId == 1230176)
        setItem(ITEM_TABLE["AP_ITEM_HUMBAWW"], 1)
    else if (itemId == 1230177)
        setItem(ITEM_TABLE["AP_ITEM_HUMBAJR"], 1)
    else if (itemId == 1230178)
        setItem(ITEM_TABLE["AP_ITEM_HUMBATD"], 1)
    else if (itemId == 1230179)
        setItem(ITEM_TABLE["AP_ITEM_HUMBAGI"], 1)
    else if (itemId == 1230180)
        setItem(ITEM_TABLE["AP_ITEM_HUMBAHP"], 1)
    else if (itemId == 1230181)
        setItem(ITEM_TABLE["AP_ITEM_HUMBACC"], 1)
    else if (itemId == 1230182)
        setItem(ITEM_TABLE["AP_ITEM_HUMBAIH"], 1)
}

//////////////////////////////// DOUBLOONS ////////////////////////////////////

function doubloon_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["DOUBLOON"] != undefined)
        {
            for(var i=0;i < ASSET_MAP_CHECK[CURRENT_MAP]["DOUBLOON"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["DOUBLOON"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["DOUBLOON"][locationId].addr, ADDRESS_MAP["DOUBLOON"][locationId].bit)
                if (DEBUG_DOUBLOON)
                    console.print(ADDRESS_MAP["DOUBLOON"][locationId].name+":"+checks[locationId].toString())
            }
        }
    }
    return checks
}

function obtained_AP_DOUBLOON()
{
    if (DEBUG_DOUBLOON)
        console.print("Doubloon Obtained")
    TOTAL_DOUBLOONS = TOTAL_DOUBLOONS + 1
    setItem(ITEM_TABLE["AP_ITEM_DOUBLOON"], TOTAL_DOUBLOONS)
}

//////////////////////////////// NOTES ////////////////////////////////


function notes_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["NOTES"] != undefined)
        {
            for(var i=0;i < ASSET_MAP_CHECK[CURRENT_MAP]["NOTES"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["NOTES"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["NOTES"][locationId].addr, ADDRESS_MAP["NOTES"][locationId].bit)
                if (DEBUG_NOTES)
                    console.print(locationId + ":" + checks[locationId].toString())
            }
        }
    }
    return checks
}

function obtain_AP_NOTES()
{
    if (DEBUG_NOTES)
        console.print("Note Obtained")
    TOTAL_NOTES = TOTAL_NOTES + 1
    setItem(ITEM_TABLE["AP_ITEM_NOTE"], TOTAL_NOTES)
}

function obtain_AP_BASSCLEF()
{
    if (DEBUG_NOTES)
        console.print("Bassclef Obtained")
    TOTAL_NOTES = TOTAL_NOTES + 2
    setItem(ITEM_TABLE["AP_ITEM_NOTE"], TOTAL_NOTES)
}

//////////////////////////////// JIGGY CHUNKS ////////////////////////////////

function jiggy_chunks_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["JCHUNKS"] != undefined)
        {
            for(var i=0;i < ASSET_MAP_CHECK[CURRENT_MAP]["JCHUNKS"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["JCHUNKS"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["JCHUNKS"][locationId].addr, ADDRESS_MAP["JCHUNKS"][locationId].bit)
            }
        }
    }
    return checks
}

//////////////////////////////// Dino Kids ////////////////////////////////////////

function dino_kids_check()
{
    var checks = {
        "1231006" : false,
        "1231007" : false,
        "1231008" : false,
    }
    if (checks["1231006"] == false)
    {
        var scrut = checkRealFlag(0x0C, 2)
        if (scrut)
            checks["1231006"] = true
    }

    if (checks["1231007"] == false)
    {
        var scrat_healed = checkRealFlag(0x26, 6)
        var scrat_train = checkRealFlag(0x2C, 1)
        if (scrat_healed == true && scrat_train == false)
            checks["1231007"] = true
    }

    if (checks["1231008"] == false)
    {
        var scrit_grow = checkRealFlag(0x26, 7)
        if (scrit_grow)
            checks["1231008"] = true
    }
    return checks
}

////////////////////////////////- BK MOVES ////////////////////////////////////////////

function obtain_bkmove(itemId)
{
    if (itemId == 1230810)
        setItem(ITEM_TABLE["AP_ITEM_DIVE"], 1)
    else if (itemId == 1230811)
        setItem(ITEM_TABLE["AP_ITEM_FPAD"], 1)
    else if (itemId == 1230812)
        setItem(ITEM_TABLE["AP_ITEM_FFLIP"], 1)
    else if (itemId == 1230813)
        setItem(ITEM_TABLE["AP_ITEM_EGGSHOOT"], 1)
    else if (itemId == 1230814)
        setItem(ITEM_TABLE["AP_ITEM_ROLL"], 1)
    else if (itemId == 1230815)
        setItem(ITEM_TABLE["AP_ITEM_TTROT"], 1)
    else if (itemId == 1230816)
        setItem(ITEM_TABLE["AP_ITEM_TJUMP"], 1)
    else if (itemId == 1230817)
        setItem(ITEM_TABLE["AP_ITEM_CLIMB"], 1)
    else if (itemId == 1230818)
        setItem(ITEM_TABLE["AP_ITEM_FLUTTER"], 1)
    else if (itemId == 1230819)
        setItem(ITEM_TABLE["AP_ITEM_WWING"], 1)
    else if (itemId == 1230820)
        setItem(ITEM_TABLE["AP_ITEM_BBUST"], 1)
    else if (itemId == 1230821)
        setItem(ITEM_TABLE["AP_ITEM_TTRAIN"], 1)
    else if (itemId == 1230822)
        setItem(ITEM_TABLE["AP_ITEM_ARAT"], 1)
    else if (itemId == 1230823)
        setItem(ITEM_TABLE["AP_ITEM_BEGGS"], 1)
    else if (itemId == 1230824)
        setItem(ITEM_TABLE["AP_ITEM_GRAT"], 1)
    else if (itemId == 1230825)
        setItem(ITEM_TABLE["AP_ITEM_BBARGE"], 1)
    else if (itemId == 1230826)
        setItem(ITEM_TABLE["AP_ITEM_SSTRIDE"], 1)
    else if (itemId == 1230827)
        setItem(ITEM_TABLE["AP_ITEM_BBOMB"], 1)
}



//////////////////////////////// Stop N Swap ////////////////////////////////

function mystery_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["STOPNSWAP"] != undefined)
        {
            for(var i=0; i < ASSET_MAP_CHECK[CURRENT_MAP]["STOPNSWAP"].length; i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["STOPNSWAP"][i]
                if (locationId == "1230953" || locationId == "1230954" || locationId == "1230955")
                    checks[locationId] = checkRealFlag(ADDRESS_MAP["STOPNSWAP"][locationId].addr, ADDRESS_MAP["STOPNSWAP"][locationId].bit)
                else
                    checks[locationId] = checkFakeFlag(ADDRESS_MAP["STOPNSWAP"][locationId].addr, ADDRESS_MAP["STOPNSWAP"][locationId].bit)
                if (DEBUG_STOPNSWAP)
                    console.print(locationId + ":" + checks[locationId].toString())
            }
        }
    }
    return checks
}

function obtain_mystery_item(itemId)
{
    if (itemId == 1230799)
        setItem(ITEM_TABLE["AP_ITEM_IKEY"], 1)
    else if (itemId == 1230800)
        setItem(ITEM_TABLE["AP_ITEM_BBASH"], 1)
    else if (itemId == 1230801) // Jinjo Multiplayer
        return
    else if (itemId == 1230802)
        setItem(ITEM_TABLE["AP_ITEM_HOMINGEGGS"], 1)
    else if (itemId == 1230803)
        setItem(ITEM_TABLE["AP_ITEM_BMEGG"], 1)
    else if (itemId == 1230804)
        setItem(ITEM_TABLE["AP_ITEM_PMEGG"], 1)
}

////////////////////////////////// Station ////////////////////////////////

function train_station_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["STATIONBTN"] != undefined)
        {
            for(var i=0;i < ASSET_MAP_CHECK[CURRENT_MAP]["STATIONBTN"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["STATIONBTN"][i]
                checks[locationId] = checkFakeFlag(ADDRESS_MAP["STATIONBTN"][locationId].addr, ADDRESS_MAP["STATIONBTN"][locationId].bit)
                if (DEBUG_STATION == true)
                    console.print(locationId + ":" + checks[locationId].toString())
            }
        }
    }
    return checks
}

function obtain_AP_STATIONS(itemId)
{
    if (itemId == 1230790)
        setItem(ITEM_TABLE["AP_ITEM_TRAINSWGI"], 1)
    else if (itemId == 1230791)
        setItem(ITEM_TABLE["AP_ITEM_TRAINSWTD"], 1)
    else if (itemId == 1230792)
        setItem(ITEM_TABLE["AP_ITEM_TRAINSWHP1"], 1)
    else if (itemId == 1230793)
        setItem(ITEM_TABLE["AP_ITEM_TRAINSWHP2"], 1)
    else if (itemId == 1230794)
        setItem(ITEM_TABLE["AP_ITEM_TRAINSWIH"], 1)
    else if (itemId == 1230795)
        setItem(ITEM_TABLE["AP_ITEM_TRAINSWWW"], 1)
}

////////////////////////////////// Chuffy ////////////////////////////////////

function chuffy_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["CHUFFY"] != undefined)
        {
            for(var i=0;i < ASSET_MAP_CHECK[CURRENT_MAP]["CHUFFY"].length; i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["CHUFFY"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["CHUFFY"][locationId].addr, ADDRESS_MAP["CHUFFY"][locationId].bit)
                if (DEBUG_STATION)
                    console.print(locationId + ":" + checks[locationId].toString())
            }
        }
    }
    return checks
}

function obtain_AP_CHUFFY()
{
    if (DEBUG_CHUFFY)
        console.print("Chuffy Obtained")
    setItem(ITEM_TABLE["AP_ITEM_CHUFFY"], 1)
}

////////////////////////////////// JamJars MOVES //////////////////////////////////

function jamjar_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {

        if (ASSET_MAP_CHECK[CURRENT_MAP]["SILO"] != undefined)
        {
            for(var i=0; i < ASSET_MAP_CHECK[CURRENT_MAP]["SILO"].length; i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["SILO"][i]
                checks[locationId] = checkFakeFlag(ADDRESS_MAP["SILO"][locationId].addr, ADDRESS_MAP["SILO"][locationId].bit)
                if (DEBUG_SILO)
                    console.print(locationId + ":" + checks[locationId].toString())
            }
        }
    }
    return checks
}

function obtain_jamjar_moves(itemId)
{
    if (itemId == 1230753)
        setItem(ITEM_TABLE["AP_ITEM_GGRAB"], 1)
    else if (itemId == 1230754)
        setItem(ITEM_TABLE["AP_ITEM_BBLASTER"], 1)
    else if (itemId == 1230755)
        setItem(ITEM_TABLE["AP_ITEM_EGGAIM"], 1)
    else if (itemId == 1230756)
        setItem(ITEM_TABLE["AP_ITEM_FEGGS"], 1)
    else if (itemId == 1230757)
        setItem(ITEM_TABLE["AP_ITEM_BDRILL"], 1)
    else if (itemId == 1230758)
        setItem(ITEM_TABLE["AP_ITEM_BBAYONET"], 1)
    else if (itemId == 1230759)
        setItem(ITEM_TABLE["AP_ITEM_GEGGS"], 1)
    else if (itemId == 1230760)
        setItem(ITEM_TABLE["AP_ITEM_AIREAIM"], 1)
    else if (itemId == 1230761)
        setItem(ITEM_TABLE["AP_ITEM_SPLITUP"], 1)
    else if (itemId == 1230762)
        setItem(ITEM_TABLE["AP_ITEM_PACKWH"], 1)
    else if (itemId == 1230763)
        setItem(ITEM_TABLE["AP_ITEM_IEGGS"], 1)
    else if (itemId == 1230764)
        setItem(ITEM_TABLE["AP_ITEM_WWHACK"], 1)
    else if (itemId == 1230765)
        setItem(ITEM_TABLE["AP_ITEM_TTORP"], 1)
    else if (itemId == 1230766)
        setItem(ITEM_TABLE["AP_ITEM_AUQAIM"], 1)
    else if (itemId == 1230767)
        setItem(ITEM_TABLE["AP_ITEM_CEGGS"], 1)
    else if (itemId == 1230768)
        setItem(ITEM_TABLE["AP_ITEM_SPRINGB"], 1)
    else if (itemId == 1230769)
        setItem(ITEM_TABLE["AP_ITEM_TAXPACK"], 1)
    else if (itemId == 1230770)
        setItem(ITEM_TABLE["AP_ITEM_HATCH"], 1)
    else if (itemId == 1230771)
        setItem(ITEM_TABLE["AP_ITEM_SNPACK"], 1)
    else if (itemId == 1230772)
        setItem(ITEM_TABLE["AP_ITEM_LSPRING"], 1)
    else if (itemId == 1230773)
        setItem(ITEM_TABLE["AP_ITEM_CLAWBTS"], 1)
    else if (itemId == 1230774)
        setItem(ITEM_TABLE["AP_ITEM_SHPACK"], 1)
    else if (itemId == 1230775)
        setItem(ITEM_TABLE["AP_ITEM_GLIDE"], 1)
    else if (itemId == 1230776)
        setItem(ITEM_TABLE["AP_ITEM_SAPACK"], 1)
}

////////////////// Jinjos //////////////////


function jinjo_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["JINJOS"] != undefined)
        {
            for(var i=0; i < ASSET_MAP_CHECK[CURRENT_MAP]["JINJOS"].length; i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["JINJOS"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["JINJOS"][locationId].addr, ADDRESS_MAP["JINJOS"][locationId].bit)
                if (DEBUG_JINJO)
                    console.print(ADDRESS_MAP["JINJOS"][locationId].name + ":" + checks[locationId].toString())
            }
        }
    }
    return checks
}

function obtain_jinjo(itemId)
{
    if (itemId == 1230501)
    {
        WHITE_JINJO = WHITE_JINJO + 1
        setItem(ITEM_TABLE["AP_ITEM_WJINJO"], WHITE_JINJO)
    }
    else if (itemId == 1230502)
    {
        ORANGE_JINJO = ORANGE_JINJO + 1
        setItem(ITEM_TABLE["AP_ITEM_OJINJO"], ORANGE_JINJO)
    }
    else if (itemId == 1230503)
    {
        YELLOW_JINJO = YELLOW_JINJO + 1
        setItem(ITEM_TABLE["AP_ITEM_YJINJO"], YELLOW_JINJO)
    }
    else if (itemId == 1230504)
    {
        BROWN_JINJO = BROWN_JINJO + 1
        setItem(ITEM_TABLE["AP_ITEM_BRJINJO"], BROWN_JINJO)
    }
    else if (itemId == 1230505)
    {
        GREEN_JINJO = GREEN_JINJO + 1
        setItem(ITEM_TABLE["AP_ITEM_GJINJO"], GREEN_JINJO)
    }
    else if (itemId == 1230506)
    {
        RED_JINJO = RED_JINJO + 1
        setItem(ITEM_TABLE["AP_ITEM_RJINJO"], RED_JINJO)
    }
    else if (itemId == 1230507)
    {
        BLUE_JINJO = BLUE_JINJO + 1
        setItem(ITEM_TABLE["AP_ITEM_BLJINJO"], BLUE_JINJO)
    }
    else if (itemId == 1230508)
    {
        PURPLE_JINJO = PURPLE_JINJO + 1
        setItem(ITEM_TABLE["AP_ITEM_PJINJO"], PURPLE_JINJO)
    }
    else if (itemId == 1230509)
    {
        BLACK_JINJO = BLACK_JINJO + 1
        setItem(ITEM_TABLE["AP_ITEM_BKJINJO"], BLACK_JINJO)
    }
}

function jinjo_family_check() // counts AP jinjos and Marks as Completed if true
{
    var checks = {}
    for(var i=0;i < ASSET_MAP_CHECK["ALL"]["JINJO_FAMILY"].length; i++)
    {
        var locationId = ASSET_MAP_CHECK["ALL"]["JINJO_FAMILY"][i]
        checks[locationId] = checkRealFlag(ADDRESS_MAP["JINJO_FAMILY"][locationId].addr, ADDRESS_MAP["JINJO_FAMILY"][locationId].bit)
        if (DEBUG_JINJO)
            console.print(ADDRESS_MAP["JINJO_FAMILY"][locationId].name +":" +checks[locationId].toString())
    }
    return checks
}

////////////////// MUMBO TOKENS ////////////////////////

function obtain_mumbo_token()
{
    TOTAL_MUMBO_TOKENS = TOTAL_MUMBO_TOKENS + 1
    setItem(ITEM_TABLE["AP_ITEM_MUMBOTOKEN"], TOTAL_MUMBO_TOKENS)
}

////////////////////// TRAPS ////////////////////////////
function traps(itemId)
{
    if (itemId == 1230786)
    {
        TTRAPS = TTRAPS + 1
        sendTrap(TRAP_TABLE["AP_TRAP_TRIP"], TTRAPS)
    }
    else if (itemId == 1230787)
    {
        STRAPS = STRAPS + 1
        sendTrap(TRAP_TABLE["AP_TRAP_SLIP"], STRAPS)
    }
    else if (itemId == 1230788)
    {
        TRTRAPS = TRTRAPS + 1
        sendTrap(TRAP_TABLE["AP_TRAP_MISFIRE"], TRTRAPS)
    }
    else if (itemId == 1230789)
    {
        SQTRAPS = SQTRAPS + 1
        sendTrap(TRAP_TABLE["AP_TRAP_SQUISH"], SQTRAPS)
    }
    else if (itemId == 1230833)
    {
        TITRAPS = TITRAPS + 1
        sendTrap(TRAP_TABLE["AP_TRAP_TIP"], TITRAPS)
    }
    end
}


////////////////////// NESTS LOCATIONS //////////////////

function nest_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["NESTS"] != undefined)
        {
            for(var i=0; i < ASSET_MAP_CHECK[CURRENT_MAP]["NESTS"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["NESTS"][i]
                checks[locationId] = checkNestFlag(ADDRESS_MAP["NESTS"][locationId])
                if (DEBUG_NESTS)
                    console.print(locationId + ":" + checks[locationId].toString())
            }   
        }
    }
    return checks
}

function obtain_nests(itemId)
{
    if (itemId == 1230806)
    {
        EGGNEST = EGGNEST + 1
        setItem(ITEM_TABLE["AP_ITEM_ENEST"], EGGNEST)
    }
    else if (itemId == 1230807)
    {
        FEATHERNEST = FEATHERNEST + 1
        setItem(ITEM_TABLE["AP_ITEM_FNEST"], FEATHERNEST)
    }
    else if (itemId == 1230805)
    {
        GOLDNEST = GOLDNEST + 1
        setItem(ITEM_TABLE["AP_ITEM_GNEST"], GOLDNEST)
    }
}

////////////////////// SIGNPOST LOCATIONS //////////////////

function signpost_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["SIGNPOSTS"] != undefined)
        {
            for(var i=0;i < ASSET_MAP_CHECK[CURRENT_MAP]["SIGNPOSTS"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["SIGNPOSTS"][i]
                checks[locationId] = checkSignpostFlag(ADDRESS_MAP["SIGNPOSTS"][locationId])
                if (DEBUG_SIGNPOSTS)
                    console.print(locationId + ":" + checks[locationId].toString())
            }
        }
    }
    return checks
}

////////////////////// SILOS LOCATIONS ////////////////////
function warpsilo_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["WARPSILOS"] != undefined)
        {
            for(var i=0; i < ASSET_MAP_CHECK[CURRENT_MAP]["WARPSILOS"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["WARPSILOS"][i]
                checks[locationId] = checkFakeFlag(ADDRESS_MAP["WARPSILOS"][locationId].addr, ADDRESS_MAP["WARPSILOS"][locationId].bit)
                if (DEBUG_WARPSILOS)
                    console.print(ADDRESS_MAP["WARPSILOS"][locationId].name + ":" + checks[locationId].toString())
            }
        }
    }
    return checks
}

function obtain_silos(itemId)
{
    if (itemId == 1230870)
        setItem(ITEM_TABLE["AP_ITEM_SILO_JINJO_VILLAGE"], 1)
    else if (itemId == 1230871)
        setItem(ITEM_TABLE["AP_ITEM_SILO_WOODED_HOLLOW"], 1)
    else if (itemId == 1230872)
        setItem(ITEM_TABLE["AP_ITEM_SILO_PLATEAU"], 1)
    else if (itemId == 1230873)
        setItem(ITEM_TABLE["AP_ITEM_SILO_PINE_GROVE"], 1)
    else if (itemId == 1230874)
        setItem(ITEM_TABLE["AP_ITEM_SILO_CLIFF_TOP"], 1)
    else if (itemId == 1230875)
        setItem(ITEM_TABLE["AP_ITEM_SILO_WASTELAND"], 1)
    else if (itemId == 1230876)
        setItem(ITEM_TABLE["AP_ITEM_SILO_QUAGMIRE"], 1)
}

////////////////////// WARPPAD LOCATIONS ////////////////////
function warppad_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["WARPPADS"] != undefined)
        {
            for(var i=0;i < ASSET_MAP_CHECK[CURRENT_MAP]["WARPPADS"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["WARPPADS"][i]
                checks[locationId] = checkFakeFlag(ADDRESS_MAP["WARPPADS"][locationId].addr, ADDRESS_MAP["WARPPADS"][locationId].bit)
                if (DEBUG_WARPPADS)
                    console.print(ADDRESS_MAP["WARPPADS"][locationId].name +":"+checks[locationId].toString())
            }
        }
    }
    return checks
}

function obtain_warppads(itemId)
{
    if (itemId == 1230877)
        setItem(ITEM_TABLE["AP_ITEM_WARPMT_ENTRANCE"], 1)
    else if (itemId == 1230878)
        setItem(ITEM_TABLE["AP_ITEM_WARPMT_MUMBO"], 1)
    else if (itemId == 1230879)
        setItem(ITEM_TABLE["AP_ITEM_WARPMT_PRISON"], 1)
    else if (itemId == 1230880)
        setItem(ITEM_TABLE["AP_ITEM_WARPMT_HUMBA"], 1)
    else if (itemId == 1230881)
        setItem(ITEM_TABLE["AP_ITEM_WARPMT_KICKBALL"], 1)
    else if (itemId == 1230882)
        setItem(ITEM_TABLE["AP_ITEM_WARPGG_ENTRANCE"], 1)
    else if (itemId == 1230883)
        setItem(ITEM_TABLE["AP_ITEM_WARPGG_MUMBO"], 1)
    else if (itemId == 1230884)
        setItem(ITEM_TABLE["AP_ITEM_WARPGG_HUMBA"], 1)
    else if (itemId == 1230885)
        setItem(ITEM_TABLE["AP_ITEM_WARPGG_CRUSHING"], 1)
    else if (itemId == 1230886)
        setItem(ITEM_TABLE["AP_ITEM_WARPGG_TRAIN"], 1)
    else if (itemId == 1230887)
        setItem(ITEM_TABLE["AP_ITEM_WARPWW_ENTRANCE"], 1)
    else if (itemId == 1230888)
        setItem(ITEM_TABLE["AP_ITEM_WARPWW_BIGTOP"], 1)
    else if (itemId == 1230889)
        setItem(ITEM_TABLE["AP_ITEM_WARPWW_SPACE"], 1)
    else if (itemId == 1230890)
        setItem(ITEM_TABLE["AP_ITEM_WARPWW_HUMBA"], 1)
    else if (itemId == 1230891)
        setItem(ITEM_TABLE["AP_ITEM_WARPWW_MUMBO"], 1)
    else if (itemId == 1230892)
        setItem(ITEM_TABLE["AP_ITEM_WARPJR_ENTRANCE"], 1)
    else if (itemId == 1230893)
        setItem(ITEM_TABLE["AP_ITEM_WARPJR_ATLANTIS"], 1)
    else if (itemId == 1230894)
        setItem(ITEM_TABLE["AP_ITEM_WARPJR_SHIP"], 1)
    else if (itemId == 1230895)
        setItem(ITEM_TABLE["AP_ITEM_WARPJR_BIGFISH"], 1)
    else if (itemId == 1230896)
        setItem(ITEM_TABLE["AP_ITEM_WARPJR_LOCKERS"], 1)
    else if (itemId == 1230897)
        setItem(ITEM_TABLE["AP_ITEM_WARPTD_ENTRANCE"], 1)
    else if (itemId == 1230898)
        setItem(ITEM_TABLE["AP_ITEM_WARPTD_STOMPING"], 1)
    else if (itemId == 1230899)
        setItem(ITEM_TABLE["AP_ITEM_WARPTD_MUMBO"], 1)
    else if (itemId == 1230900)
        setItem(ITEM_TABLE["AP_ITEM_WARPTD_HUMBA"], 1)
    else if (itemId == 1230901)
        setItem(ITEM_TABLE["AP_ITEM_WARPTD_TOP"], 1)
    else if (itemId == 1230902)
        setItem(ITEM_TABLE["AP_ITEM_WARPGI_ENTRANCE"], 1)
    else if (itemId == 1230902)
        setItem(ITEM_TABLE["AP_ITEM_WARPGI_ENTRANCE"], 1)
    else if (itemId == 1230903)
        setItem(ITEM_TABLE["AP_ITEM_WARPGI_HUMBA"], 1)
    else if (itemId == 1230904)
        setItem(ITEM_TABLE["AP_ITEM_WARPGI_MUMBO"], 1)
    else if (itemId == 1230905)
        setItem(ITEM_TABLE["AP_ITEM_WARPGI_CRUSHER"], 1)
    else if (itemId == 1230906)
        setItem(ITEM_TABLE["AP_ITEM_WARPGI_ROOF"], 1)
    else if (itemId == 1230907)
        setItem(ITEM_TABLE["AP_ITEM_WARPHF_ENTRANCE"], 1)
    else if (itemId == 1230908)
        setItem(ITEM_TABLE["AP_ITEM_WARPHF_LAVAUPPER"], 1)
    else if (itemId == 1230909)
        setItem(ITEM_TABLE["AP_ITEM_WARPHF_ICYUPPER"], 1)
    else if (itemId == 1230910)
        setItem(ITEM_TABLE["AP_ITEM_WARPHF_HUMBA"], 1)
    else if (itemId == 1230911)
        setItem(ITEM_TABLE["AP_ITEM_WARPHF_ICICLE"], 1)
    else if (itemId == 1230912)
        setItem(ITEM_TABLE["AP_ITEM_WARPCC_ENTRANCE"], 1)
    else if (itemId == 1230913)
        setItem(ITEM_TABLE["AP_ITEM_WARPCC_CENTER"], 1)
    else if (itemId == 1230914)
        setItem(ITEM_TABLE["AP_ITEM_WARPCK_ENTRANCE"], 1)
    else if (itemId == 1230915)
        setItem(ITEM_TABLE["AP_ITEM_WARPCK_HAG1"], 1)
}


////////////////////// BOGGY KIDS ////////////////////////////
function boggy_kids_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["BOGGY_KIDS"] != undefined)
        {
            for(var i=0;i < ASSET_MAP_CHECK[CURRENT_MAP]["BOGGY_KIDS"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["BOGGY_KIDS"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["BOGGY_KIDS"][locationId].addr, ADDRESS_MAP["BOGGY_KIDS"][locationId].bit)
                if (DEBUG_BOGGY_KIDS)
                    console.print(ADDRESS_MAP["BOGGY_KIDS"][locationId] +":"+checks[locationId].toString())
            }
        }
    }
    return checks
}

////////////////////// ALIEN KIDS ////////////////////////////
function alien_kids_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["ALIEN_KIDS"] != undefined)
        {
            for(var i=0;i < ASSET_MAP_CHECK[CURRENT_MAP]["ALIEN_KIDS"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["ALIEN_KIDS"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["ALIEN_KIDS"][locationId].addr, ADDRESS_MAP["ALIEN_KIDS"][locationId].bit)
                if (DEBUG_ALIEN_KIDS)
                    console.print(ADDRESS_MAP["ALIEN_KIDS"][locationId]+":"+checks[locationId].toString())
            }
        }
    }
    return checks
}

////////////////////// SKIVVIES ////////////////////////////
function skivvies_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["SKIVVIES"] != undefined)
        {
            for(var i=0;i < ASSET_MAP_CHECK[CURRENT_MAP]["SKIVVIES"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["SKIVVIES"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["SKIVVIES"][locationId].addr, ADDRESS_MAP["SKIVVIES"][locationId].bit)
                if (DEBUG_SKIVVIES)
                    console.print(ADDRESS_MAP["SKIVVIES"][locationId]+":"+checks[locationId].toString())
            }
            if (checkRealFlag(0x81, 3))
            {
                var keys = Object.keys(ADDRESS_MAP["SKIVVIES"])
                for(var i=0;i < keys.length;i++)
                {
                    var locationId = keys[i]
                    checks[locationId] = true
                }
            }
        }
    }
    return checks
}

////////////////////// MR FIT EVENTS ////////////////////////////
function mr_fit_events_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["MRFIT"] != undefined)
        {
            for(var i=0;i < ASSET_MAP_CHECK[CURRENT_MAP]["MRFIT"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["MRFIT"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["MRFIT"][locationId].addr, ADDRESS_MAP["MRFIT"][locationId].bit)
                if (DEBUG_MRFIT)
                    console.print(ADDRESS_MAP["MRFIT"][locationId]+":"+checks[locationId].toString())
            }
        }
    }
    return checks
}

////////////////////// BIGTOP TICKETS ////////////////////////////
function bttickets_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["BIGTOP_TICKETS"] != undefined)
        {
            for(var i=0;i < ASSET_MAP_CHECK[CURRENT_MAP]["BIGTOP_TICKETS"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["BIGTOP_TICKETS"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["BIGTOP_TICKETS"][locationId].addr, ADDRESS_MAP["BIGTOP_TICKETS"][locationId].bit)
            }
        }
    }
    return checks
}

function obtain_AP_TICKETS()
{
    TOTAL_BTTICKETS = TOTAL_BTTICKETS + 1
    setItem(ITEM_TABLE["AP_ITEM_BTTICKET"], TOTAL_BTTICKETS)
}

////////////////////// GREEN RELICS ////////////////////////////
function grrelic_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["GREEN_RELICS"] != undefined)
        {
            for(var i=0;i < ASSET_MAP_CHECK[CURRENT_MAP]["GREEN_RELICS"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["GREEN_RELICS"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["GREEN_RELICS"][locationId].addr, ADDRESS_MAP["GREEN_RELICS"][locationId].bit)
            }
        }
    }
    return checks
}

function obtain_AP_GRRELIC()
{
    TOTAL_GRRELICS = TOTAL_GRRELICS + 1
    setItem(ITEM_TABLE["AP_ITEM_GRRELIC"], TOTAL_GRRELICS)
}

////////////////////// BEANS ////////////////////////////

function beans_check()
{
    var checks = {}
    if (ASSET_MAP_CHECK[CURRENT_MAP] != undefined)
    {
        if (ASSET_MAP_CHECK[CURRENT_MAP]["BEANS"] != undefined)
        {
            for(var i=0;i < ASSET_MAP_CHECK[CURRENT_MAP]["BEANS"].length;i++)
            {
                var locationId = ASSET_MAP_CHECK[CURRENT_MAP]["BEANS"][i]
                checks[locationId] = checkRealFlag(ADDRESS_MAP["BEANS"][locationId].addr, ADDRESS_MAP["BEANS"][locationId].bit)
            }
        }
    }
    return checks
}

function obtain_AP_BEANS()
{
    TOTAL_BEANS = TOTAL_BEANS + 1
    setItem(ITEM_TABLE["AP_ITEM_BEAN"], TOTAL_BEANS)
}

///////////////////////// PROGRESSIVE ITEMS /////////////////////////////////////

function obtain_progressive_moves(itemId)
{
    if (itemId == 1230828) // Progressive Beak Buster
    {
        if (getItem(ITEM_TABLE["AP_ITEM_BBUST"]) == 0)
            obtain_bkmove(1230820);
        else
            setItem(ITEM_TABLE["AP_ITEM_BDRILL"], 1)
    }
    else if(itemId == 1230829) // Progressive Eggs
    {
        if (getItem(ITEM_TABLE["AP_ITEM_FEGGS"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_FEGGS"], 1)
        else if (getItem(ITEM_TABLE["AP_ITEM_GEGGS"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_GEGGS"], 1)
        else if (getItem(ITEM_TABLE["AP_ITEM_IEGGS"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_IEGGS"], 1)
        else if (getItem(ITEM_TABLE["AP_ITEM_CEGGS"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_CEGGS"], 1)
    }
    else if(itemId == 1230830) // Progressive Shoes
    {
        if (getItem(ITEM_TABLE["AP_ITEM_SSTRIDE"]) == 0)
            obtain_bkmove(1230826);
        else if (getItem(ITEM_TABLE["AP_ITEM_TTRAIN"]) == 0)
            obtain_bkmove(1230821);
        else if (getItem(ITEM_TABLE["AP_ITEM_SPRINGB"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_SPRINGB"], 1)
        else if (getItem(ITEM_TABLE["AP_ITEM_CLAWBTS"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_CLAWBTS"], 1)
    }
    else if(itemId == 1230831)
        obtain_roysten_moves(itemId);
    else if(itemId == 1230832)
    {
        if (getItem(ITEM_TABLE["AP_ITEM_GRAT"]) == 0)
            obtain_bkmove(1230824);
        else if (getItem(ITEM_TABLE["AP_ITEM_BBASH"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_BBASH"], 1)
    }
    else if(itemId == 1230782) // Progressive Flight
    {
        if (getItem(ITEM_TABLE["AP_ITEM_FPAD"]) == 0)
            obtain_bkmove(1230811);
        else if (getItem(ITEM_TABLE["AP_ITEM_BBOMB"]) == 0)
            obtain_bkmove(1230827);
        else if (getItem(ITEM_TABLE["AP_ITEM_AIREAIM"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_AIREAIM"], 1)
    }
    else if(itemId == 1230783) // Progressive Egg Aim
    {
        if (getItem(ITEM_TABLE["AP_ITEM_EGGSHOOT"]) == 0)
            obtain_bkmove(1230813);
        else if (getItem(ITEM_TABLE["AP_ITEM_EGGAIM"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_EGGAIM"], 1)
    }
    else if(itemId == 1230784) // Progressive Adv Water Training
    {
        if (getItem(ITEM_TABLE["AP_ITEM_DIVE"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_DIVE"], 1)
        else if (getItem(ITEM_TABLE["AP_ITEM_AUQAIM"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_AUQAIM"], 1)
        else if (getItem(ITEM_TABLE["AP_ITEM_TTORP"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_TTORP"], 1)
        else if (getItem(ITEM_TABLE["AP_ITEM_DAIR"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_DAIR"], 1)
        else if (getItem(ITEM_TABLE["AP_ITEM_FSWIM"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_FSWIM"], 1)
    }
    else if(itemId == 1230785) // Progressive Adv Egg Aim
    {
        if (getItem(ITEM_TABLE["AP_ITEM_EGGSHOOT"]) == 0)
            obtain_bkmove(1230813);
        else if (getItem(ITEM_TABLE["AP_ITEM_AMAZEOGAZE"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_AMAZEOGAZE"], 1)
        else if (getItem(ITEM_TABLE["AP_ITEM_EGGAIM"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_EGGAIM"], 1)
        else if (getItem(ITEM_TABLE["AP_ITEM_BBLASTER"]) == 0)
            setItem(ITEM_TABLE["AP_ITEM_BBLASTER"], 1)
    }
}



//////////////////// GAME FUNCTIONS ////////////////

function zoneWarp(zone_table)
{
    // from name -> to name
    var keys = Object.keys(zone_table)
    for(var i=0;i < keys.length; i++)
    {

        var orig_world = keys[i]
        var new_world = zone_table[orig_world]

        var success = false
        var orig_table = {}
        var orig_map = 0x0
        var new_table = {}
        var new_map = 0x0;

        var map_keys = Object.keys(MAP_ENTRANCES)

        for(var m=0; m < map_keys.length;m++)
        {
            var world_id = map_keys[m]
            var world_table = MAP_ENTRANCES[world_id]

            if (world_table.name == orig_world)
            {
                orig_table = world_table
                orig_map = world_id
            }
            if (world_table.name == new_world)
            {
                new_table = world_table
                new_map = world_id
            }
        } 
        while (success == false)
        {
            setWorldEntrance(orig_map, new_map, orig_table.entranceId, orig_table.exitMap, new_table.entranceId, new_table.access)
            success = setWorldEntrance(new_table.exitMap, orig_table.exitMap, new_table.exitId, new_map, orig_table.exitId, orig_table.reverse_access)
            if (orig_map == 0xC7) // Glitter Gulch Mine
                setWorldEntrance(orig_map, new_map, 16, orig_table.exitMap, new_table.entranceId, new_table.access)
        }
    }
}

function hag1_open()
{
    if (getItem(ITEM_TABLE["AP_ITEM_H1A"]) == 1)
        return
    if (GOAL_TYPE == 1 || GOAL_TYPE == 2 || GOAL_TYPE == 5)
        return

    var opened = false
    if (GOAL_TYPE == 0 && (OPEN_HAG1 == true || (OPEN_HAG1 == false && TOTAL_JIGGY >= 70)))
    {
        setItem(ITEM_TABLE["AP_ITEM_H1A"], 1)
        opened = true
    }
    else if (GOAL_TYPE == 4 && TOTAL_MUMBO_TOKENS >= 32)
    {
        setItem(ITEM_TABLE["AP_ITEM_H1A"], 1)
        opened = true
    }
    else if (GOAL_TYPE == 6 && TOTAL_MUMBO_TOKENS >= BH_LENGTH)
    {
        setItem(ITEM_TABLE["AP_ITEM_H1A"], 1)
        opened = true
    }
    if (opened)
    {
        var msg = "HAG-1 is now open!"
        if (DIALOG_CHARACTER == 110)
            MESSAGE_TABLE.push({Message: msg, Icon: 87})
        else
            MESSAGE_TABLE.push({Message: msg, Icon: DIALOG_CHARACTER})
    }
}


function check_open_level()  // See if entrance conditions for a level have been met
{
    if (DEBUG)
        console.print(TOTAL_JIGGY)

    var keys = Object.keys(WORLD_ENTRANCE_MAP)
    for(var i=0;i< keys.length; i++)
    {
        var values = WORLD_ENTRANCE_MAP[keys[i]]
        if (TOTAL_JIGGY >= values["defaultCost"])
        {
            UNLOCKED_WORLDS[values["locationId"]] = true
        }
    }
    hag1_open()
}

function unlock_worlds(itemId)
{
    if (itemId == 1230944)
        setItem(ITEM_TABLE["AP_ITEM_MTA"], 1)
    else if (itemId == 1230945)
        setItem(ITEM_TABLE["AP_ITEM_GGA"], 1)
    else if (itemId == 1230946)
        setItem(ITEM_TABLE["AP_ITEM_WWA"], 1)
    else if (itemId == 1230947)
        setItem(ITEM_TABLE["AP_ITEM_JRA"], 1)
    else if (itemId == 1230948)
        setItem(ITEM_TABLE["AP_ITEM_TDA"], 1)
    else if (itemId == 1230949)
        setItem(ITEM_TABLE["AP_ITEM_GIA"], 1)
    else if (itemId == 1230950)
        setItem(ITEM_TABLE["AP_ITEM_HFA"], 1)
    else if (itemId == 1230951)
        setItem(ITEM_TABLE["AP_ITEM_CCA"], 1)
    else if (itemId == 1230952)
        setItem(ITEM_TABLE["AP_ITEM_CKA"], 1)
}

//////////////////////////////// ITEM GET MESSAGES ////////////////////////////////

const station_names = {
    1230794 : "Train Station in Isle O' Hags",
    1230791 : "Train Station in Terrydactyland",
    1230790 : "Train Station in Grunty Industries",
    1230792 : "Train Station on the Lava Side of Hailfire Peaks",
    1230793 : "Train Station on the Icy Side of Hailfire Peaks",
    1230795 : "Train Station in Witchyworld",
}

const magic_names = {
    1230855 : "Golden Goliath",
    1230856 : "Levitate",
    1230857 : "Power",
    1230858 : "Oxygenate",
    1230859 : "Enlarge",
    1230860 : "EMP",
    1230861 : "Life Force",
    1230862 : "Rain Dance",
    1230863 : "Heal",
}

const transformation_names = {
    1230174 : {name: "Stony", attribute: "strong"},
    1230175 : {name: "Detonator", attribute: "explosive"},
    1230176 : {name: "Money Van", attribute: "fast"},
    1230177 : {name: "Submarine", attribute: "high-tech"},
    1230178 : {name: "T-Rex", attribute: "scary"},
    1230179 : {name: "Washing Machine", attribute: "useful"},
    1230180 : {name: "Snowball", attribute: "cool"},
    1230181 : {name: "Bee", attribute: "cute"},
    1230182 : {name: "Dragon", attribute: "dangerous"},
}

const cheat_names = {
    1230917 : "Feathers Cheat",
    1230918 : "Egg Cheat",
    1230919 : "Fallproof Cheat",
    1230920 : "Honeyback Cheat. Press D-Pad Down to Toggle this Cheat",
    1230921 : "Jukebox Cheat",
}

function display_item_message(msg_table)
{
    // Cancel if not for this player
    if (msg_table["to_player"] != PLAYER)
        return

    // Select item for current level of progressive move upgrades
    msg_table = convert_progressive_move_message(msg_table)

    // Select text depending on item id
    var msg_text = get_item_message_text(msg_table["item_id"], msg_table["item"], msg_table["player"])
    if(msg_text == null)
        return

    // Select character icon depending on item id
    var msg_icon = get_item_message_char(msg_table["item_id"]);
    if (!msg_icon)
        return

    MESSAGE_TABLE.push({Message: msg_text, Icon: msg_icon})
}

function convert_progressive_move_message(msg_table)
{
    var item_id = msg_table["item_id"]
    if (item_id == 1230828) // Progressive Beak Buster
    {
        if (getItem(ITEM_TABLE["AP_ITEM_BDRILL"]) == 1)
        {
            msg_table["item_id"] = 1230757
            msg_table["item"] = "Bill Drill"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_BBUST"]) == 1)
        {
            msg_table["item_id"] = 1230820
            msg_table["item"] = "Beak Buster"
        }
    }
    else if (item_id == 1230829) // Progressive Eggs
    {
        if (getItem(ITEM_TABLE["AP_ITEM_CEGGS"]) == 1)
        {
            msg_table["item_id"] = 1230767
            msg_table["item"] = "Clockwork Eggs"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_IEGGS"]) == 1)
        {
            msg_table["item_id"] = 1230763
            msg_table["item"] = "Ice Eggs"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_GEGGS"]) == 1)
        {
            msg_table["item_id"] = 1230759
            msg_table["item"] = "Grenade Eggs"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_FEGGS"]) == 1)
        {
            msg_table["item_id"] = 1230756
            msg_table["item"] = "Fire Eggs"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_BEGGS"]) == 1)
        {
            msg_table["item_id"] = 1230823
            msg_table["item"] = "Blue Eggs"
        }
    }
    else if (item_id == 1230830) // Progressive Shoes
    {
        if (getItem(ITEM_TABLE["AP_ITEM_CLAWBTS"]) == 1)
        {
            msg_table["item_id"] = 1230773
            msg_table["item"] = "Claw Clamber Boots"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_SPRINGB"]) == 1)
        {
            msg_table["item_id"] = 1230768
            msg_table["item"] = "Springy Step Shoes"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_TTRAIN"]) == 1)
        {
            msg_table["item_id"] = 1230821
            msg_table["item"] = "Turbo Trainers"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_SSTRIDE"]) == 1)
        {
            msg_table["item_id"] = 1230826
            msg_table["item"] = "Stilt Stride"
        }
    }
    else if (item_id == 1230831) // Progressive Water Training
    {
        if (getItem(ITEM_TABLE["AP_ITEM_FSWIM"]) == 1)
        {
            msg_table["item_id"] = 1230777
            msg_table["item"] = "Fast Swimming"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_DAIR"]) == 1)
        {
            msg_table["item_id"] = 1230778
            msg_table["item"] = "Double Air"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_DIVE"]) == 1)
        {
            msg_table["item_id"] = 1230810
            msg_table["item"] = "Dive"
        }
    }
    else if (item_id == 1230832) // Progressive Bash Attack
    {
        if (getItem(ITEM_TABLE["AP_ITEM_BBASH"]) == 1)
        {
            msg_table["item_id"] = 1230800
            msg_table["item"] = "Breegull Bash"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_GRAT"]) == 1)
        {
            msg_table["item_id"] = 1230824
            msg_table["item"] = "Ground Rat-a-tat Rap"
        }
    }
    else if (item_id == 1230782) // Progressive Flight
    {
        if (getItem(ITEM_TABLE["AP_ITEM_AIREAIM"]) == 1)
        {
            msg_table["item_id"] = 1230760
            msg_table["item"] = "Airborne Egg Aiming"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_BBOMB"]) == 1)
        {
            msg_table["item_id"] = 1230827
            msg_table["item"] = "Beak Bomb"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_FPAD"]) == 1)
        {
            msg_table["item_id"] = 1230811
            msg_table["item"] = "Flight Pad"
        }
    }
    else if (item_id == 1230783) // Progressive Egg Aim
    {
        if (getItem(ITEM_TABLE["AP_ITEM_EGGAIM"]) == 1)
        {
            msg_table["item_id"] = 1230755
            msg_table["item"] = "Egg Aim"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_EGGSHOOT"]) == 1)
        {
            msg_table["item_id"] = 1230813
            msg_table["item"] = "Third Person Egg Shooting"
        }
    }
    else if (item_id == 1230784) // Progressive Adv Water Training
    {
        if (getItem(ITEM_TABLE["AP_ITEM_FSWIM"]) == 1)
        {
            msg_table["item_id"] = 1230777
            msg_table["item"] = "Fast Swimming"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_DAIR"]) == 1)
        {
            msg_table["item_id"] = 1230778
            msg_table["item"] = "Double Air"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_TTORP"]) == 1)
        {
            msg_table["item_id"] = 1230765
            msg_table["item"] = "Talon Torpedo"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_AUQAIM"]) == 1)
        {
            msg_table["item_id"] = 1230766
            msg_table["item"] = "Sub-Aqua Egg Aiming"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_DIVE"]) == 1)
        {
            msg_table["item_id"] = 1230810
            msg_table["item"] = "Dive"
        }
    }
    else if (item_id == 1230785) // Progressive Adv Egg Aim
    {
        if (getItem(ITEM_TABLE["AP_ITEM_BBLASTER"]) == 1)
        {
            msg_table["item_id"] = 1230754
            msg_table["item"] = "Breegull Blaster"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_EGGAIM"]) == 1)
        {
            msg_table["item_id"] = 1230755
            msg_table["item"] = "Egg Aim"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_AMAZEOGAZE"]) == 1)
        {
            msg_table["item_id"] = 1230779
            msg_table["item"] = "Amaze-O-Gaze"
        }
        else if (getItem(ITEM_TABLE["AP_ITEM_EGGSHOOT"]) == 1)
        {
            msg_table["item_id"] = 1230813
            msg_table["item"] = "Third Person Egg Shooting"
        }
    }
    return msg_table
}

function get_item_message_text(item_id, item, player)
{
    var own = player == PLAYER

    if((item_id >= 1230753 && item_id <= 1230780)  // BT Moves
        || (item_id >= 1230810 && item_id <= 1230827) // BK Moves
        || (item_id >= 1230782 && item_id <= 1230785) // Progessive Moves 1
        || (item_id >= 1230828 && item_id <= 1230832) // Progessive Moves 2
        || (item_id == 1230800 || item_id == 1230802)) // Stop'n'Swap Moves
    {
        return own ? "You can now use " + item+"." : player + " taught you how to use "+item
    }
    else if (1230944 <= item_id && item_id <= 1230952) // Worlds
    {
        return own ? item +" is now open!" : player +" has just opened "+item
    }
    else if (item_id == 1230796) // Chuffy
    {
        var special = ENABLE_AP_CHUFFY ? "\nDon't forget that you can call Chuffy at any unlocked station." : ""
        return own ? "You can now use "+item+"."+special : player+" has just repaired "+item+". "+special
    }
    else if (1230790 <= item_id && item_id <= 1230795) // Stations
    {
        return own ? "You can now use the "+station_names[item_id]+"." : player+" has just opened the "+station_names[item_id]
    }
    else if (1230855 <= item_id && item_id <= 1230863) // Mumbo Magic
    {
        if (DIALOG_CHARACTER == 110 || DIALOG_CHARACTER == 8)
        {
            // Mumbo flavor text
            return own ? "Mumbo now use mighty "+magic_names[item_id] +" spell. Bear go visit Mumbo to try." : player +" told Mumbo mighty "+magic_names[item_id] +" spell. Bear go visit Mumbo to try."
        }
        else
        {
            // Basic text
            return own ? "Mumbo can now use the "+magic_names[item_id] +" spell." : player +" has just unlocked Mumbo's "+magic_names[item_id] +" spell."
        }
    }
    else if (1230174 <= item_id && item_id <= 1230182) // Humba Transformations
    {
        if (DIALOG_CHARACTER == 110 || DIALOG_CHARACTER == 37)
        {
            // Humba flavor text
            if (item_id == 1230182)
            {
                return own ? "Wumba now make bird "+transformation_names[item_id]["name"] +". Very "+transformation_names[item_id]["attribute"] +"!" : player +" told Wumba how to make bird "+transformation_names[item_id]["name"] +". Very "+transformation_names[item_id]["attribute"] +"!"
            }
            else
            {
                return own ? "Wumba now make bear "+transformation_names[item_id]["name"] +". Very "+transformation_names[item_id]["attribute"] +"!" : player +" told Wumba how to make bear "+transformation_names[item_id]["name"] +". Very "+transformation_names[item_id]["attribute"] +"!"
            }
        }
        else
        {
            // Basic text
            if (item_id == 1230182)
            {
                return own ? "Kazooie can now be transformed into a "+transformation_names[item_id]["name"] +"." : player +" has just unlocked the "+transformation_names[item_id]["name"] +" transformation."
            }
            else
            {
                return own ? "Banjo can now be transformed into a "+transformation_names[item_id]["name"] +"." : player +" has just unlocked the "+transformation_names[item_id]["name"] +" transformation."
            }
        }
    }
    else if(1230870 <= item_id && item_id <= 1230876) // Silos
    {
        return own ? ""+item +" is now open!" : player +" has just opened the "+item +"!"
    }
    else if (1230877 <= item_id && item_id <= 1230915) // Warppads
    {
        return own ? "You can now use the "+item +"" : player +" has just unlocked the "+item +""
    }
    else if (1230917 <= item_id && item_id <= 1230921) // Cheats
    {
        return own ? "You can now use the "+cheat_names[item_id] +"." : player +" has just sent you the "+cheat_names[item_id] +"."
    }
    return null
}

function get_item_message_char(item_id)
{
    // Default character is used depending on the item
    if (DIALOG_CHARACTER == 110)
    {
        if (1230753 <= item_id && item_id <= 1230776) // BT Moves
            return 17 // Jamjars
        else if (item_id == 1230779) // Amaze O' Gaze
            return 99 // Goggles
        else if (item_id == 1230780) // Roar
            return 50 // Bargasaurus
        else if (item_id == 1230800 || item_id == 1230802) // Stop'n'Swap Moves
            return 109 // Heggy
        else if (1230810 <= item_id || item_id <= 1230827) // BK Moves
            return 7 // Bottles
        else if ((1230777 <= item_id && item_id <= 1230778)
            || (item_id == 1230831)) // Water Moves
            return 56 // Roysten
        else if ((1230828 <= item_id && item_id <= 1230830)
            || (item_id == 1230832)
            || (1230782 <= item_id && item_id <= 1230785)) // Progressive Moves
            return 7 // Bottles
        else if (item_id == 1230944) // Mayahem Temple
            return 100 // Targitzan
        else if (item_id == 1230945) // Glitter Gulch Mine
            return 39 // Old King Coal
        else if (item_id == 1230946 || item_id == 1230795) // Witchy World
            return 31 // Mr Patch
        else if (item_id == 1230947) // Jolly Roger's Lagoon
            return 102 // Lord Woo Fak Fak
        else if (item_id == 1230948 || item_id == 1230791) // Terrydactyland
            return 49 // Terry
        else if (item_id == 1230949 || item_id == 1230790) // Grunty Industries
            return 103 // Weldar
        else if (item_id == 1230950 || item_id == 1230793) // Hailfire Peaks
            return 65 // Chilly Willy
        else if (item_id == 1230792)
            return 66
        else if (item_id == 1230951) // Cloud Cuckooland
            return 27 // Canary Mary
        else if (item_id == 1230952) // Cauldron Keep
            return 71 // Klungo
        else if (item_id == 1230794) // Isle O' Hags Station
            return 8 // Mumbo
        else if (item_id == 1230796) // Chuffy
            return 39 // Old King Coal
        else if (1230855 <= item_id && item_id <= 1230863) // Mumbo Magic
            return 8 // Mumbo
        else if (1230174 <= item_id && item_id <= 1230182) // Humba Transformations
            return 37 // Humba
        else if (1230870 <= item_id && item_id <= 1230876) // Silos
            return 17 // Jamjars
        else if (1230877 <= item_id && item_id <= 1230881) // Warppad MT
            return 100 // Targitzan
        else if (1230882 <= item_id && item_id <= 1230886) // Warppad GM
            return 39 // Old King Coal
        else if (1230887 <= item_id && item_id <= 1230891) // Warppad WW
            return 31 // Mr Patch
        else if (1230892 <= item_id && item_id <= 1230896) // Warppad JR
            return 102 // Lord Woo Fak Fak
        else if (1230897 <= item_id && item_id <= 1230901) // Warppad TD
            return 49 // Terry
        else if (1230902 <= item_id && item_id <= 1230906) // Warppad GI
            return 103 // Weldar
        else if (1230907 <= item_id && item_id <= 1230911) // Warppad HP
            return 65 // Chilly Willy
        else if (1230912 <= item_id && item_id <= 1230915) // Warppad CC
            return 27 // Canary
        else if (1230917 <= item_id && item_id <= 1230921) // Cheats
            return 28 // Cheato
        else // Default
            return 7 // Bottles
    // Completely random character
    }
    else if (DIALOG_CHARACTER == 255)
        return Math.floor(Math.random() * (109))
    // Fixed dialog character has been selected
    else
        return DIALOG_CHARACTER
}

/////////////// AP Functions /////////////////////

function processAGIItem(item_list)
{
    //console.print(item_list)
    var keys = Object.keys(item_list)
    for(var i = 0; i < keys.length; i++)
    {
        var ap_id = i
        var memlocation = item_list[ap_id]
        if(receive_map[ap_id] == undefined)
        {
            //console.print("Added "+ memlocation.toString() + " to the Map\r\n")
            if(memlocation >= 1230944 && memlocation <= 1230952) // Worlds
                unlock_worlds(memlocation)
            else if(memlocation >= 1230810 && memlocation <= 1230827) // BK Moves
                obtain_bkmove(memlocation)
            else if((memlocation >= 1230855 && memlocation <= 1230863) || (memlocation >= 1230174 && memlocation <= 1230182)) // Magic
                obtain_AP_MAGIC(memlocation)
            else if(memlocation >= 1230753 && memlocation <= 1230776) // Jamjar Moves
                obtain_jamjar_moves(memlocation)
            else if(memlocation >= 1230790 && memlocation <= 1230795) // Station Btns
                obtain_AP_STATIONS(memlocation);
            else if(memlocation >= 1230501 && memlocation <= 1230509) // Jinjos
                obtain_jinjo(memlocation)
            else if(memlocation >= 1230777 && memlocation <= 1230778) // Roysten Moves
                obtain_roysten_moves(memlocation)
            else if(memlocation >= 1230828 && memlocation <= 1230832) // Progressive Moves
                obtain_progressive_moves(memlocation)
            else if(memlocation >= 1230782 && memlocation <= 1230785) // More Progressive Moves
                obtain_progressive_moves(memlocation)
            else if(memlocation >= 1230799 && memlocation <= 1230804) // StopNSwap
                obtain_mystery_item(memlocation)
            else if(memlocation >= 1230786 && memlocation <= 1230789) // Traps
                traps(memlocation)
            else if(memlocation >= 1230805 && memlocation <= 1230807) // Nests
                obtain_nests(memlocation)
            else if(memlocation >= 1230870 && memlocation <= 1230876) // Silos
                obtain_silos(memlocation)
            else if(memlocation >= 1230877 && memlocation <= 1230915) // Warppads
                obtain_warppads(memlocation)
            else if(memlocation >= 1230917 && memlocation <= 1230921) // Cheats
                obtain_cheats(memlocation)
            else if(memlocation == 1230514) // Doubloon
                obtained_AP_DOUBLOON()
            else if(memlocation == 1230515) // Jiggy
            {
                obtain_AP_JIGGY()
                check_open_level() // check if the current jiggy count opens a new level
            }
            else if(memlocation == 1230516) // Treble Clef
                obtain_AP_TREBLE()
            else if(memlocation == 1230831) // Progressive Water Training
                obtain_roysten_moves(memlocation)
            else if(memlocation == 1230513) // Cheato Item
                obtain_AP_PAGES()
            else if(memlocation == 1230512) // Honeycomb Item
                obtained_AP_HONEYCOMB()
            else if(memlocation == 1230916) // Health Upgrade Item
                obtained_AP_HEALTHUPGRADE()
            else if(memlocation == 1230797) // Notes
                obtain_AP_NOTES()
            else if(memlocation == 1230781) // Bassclefs
                obtain_AP_BASSCLEF()
            else if(memlocation == 1230796) // Chuffy
                obtain_AP_CHUFFY()
            else if(memlocation == 1230779) // amaze-o-gaze
               obtain_amaze_o_gaze()
            else if(memlocation == 1230780) // Roar
                obtain_roar()
            else if(memlocation == 1230798) // Mumbo Token
            {
                obtain_mumbo_token()
                check_open_level() // check if the current jiggy count opens a new level
            }
            else if(memlocation == 1230833) // Tip Trap
                traps(memlocation)
            else if(memlocation == 1230922) // BigTop Tickets
                obtain_AP_TICKETS()
            else if(memlocation == 1230923) // Green Relic
                obtain_AP_GRRELIC()
            else if(memlocation == 1230924) // Beans
                obtain_AP_BEANS()
            receive_map[ap_id] = memlocation
        }
    }
}


function mumbo_announce()
{
    if(GOAL_TYPE == 5 && TOKEN_ANNOUNCE == false)
    {
        if (TOTAL_MUMBO_TOKENS >= TH_LENGTH)
        {
            var message = "You have found enough Mumbo Tokens! Time to party at Bottles' House!"
            console.print(message+"\r\n")
            if (DIALOG_CHARACTER == 110)
                MESSAGE_TABLE.push({Message: message, Icon: 8})
            else
                MESSAGE_TABLE.push({Message: message, Icon: DIALOG_CHARACTER})
            TOKEN_ANNOUNCE = true
        }
    }
    if (GOAL_TYPE == 3 && TOKEN_ANNOUNCE == false)
    {
        if (TOTAL_MUMBO_TOKENS >= JFR_LENGTH)
        {
            var message = "You have found enough Mumbo Tokens! Time to party at Bottles' House!"
            print(message+"\r\n")
            if (DIALOG_CHARACTER == 110)
                MESSAGE_TABLE.push({Message: message, Icon: 8})
            else
                MESSAGE_TABLE.push({Message: message, Icon: DIALOG_CHARACTER})
            TOKEN_ANNOUNCE = true
        }
    }
}

function process_block(json_object)
{
    // Sometimes the block is nothing, if this is the case then quietly stop processing
    //console.print("Got Block Data")
    if (json_object == null)
        return
    if (json_object.slot_player != null)
        return
    if (json_object.items != null)
        processAGIItem(json_object.items)
    if (json_object.messages != null)
    {
        var keys = Object.keys(json_object.messages)
        for(var i = 0; i < keys.length; i++)
        {
            display_item_message(json_object.messages[keys[i]])
        }
    }
    if (json_object.triggerDeath == true && DEATH_LINK == true)
    {
        var death = getAPDeath()
        setAPDeath(death + 1)
        var randomDeathMsg = DEATH_MESSAGES[Math.floor(Math.random() * (DEATH_MESSAGES.length))]

        MESSAGE_TABLE.push({Message: randomDeathMsg, Icon: 15})

    }
    if (json_object.triggerTag == true && TAG_LINK == true)
    {
        var tag = getAPTag()
        setAPTag(tag + 1)
    }

    if (DEBUGLVL3 == true)
        console.print(json_object)
}

function SendToBTClient()
{
    var retTable = {}
    var detect_death = false
    var detect_tag = false

    if (getPCDeath() != getNLocalDeath() && DEATH_LINK == false)
    {
        var randomDeathMsg = DEATH_MESSAGES[Math.floor(Math.random() * (DEATH_MESSAGES.length))]
        MESSAGE_TABLE.push({Message: randomDeathMsg, Icon: 15})
        var died = getPCDeath()
        setPCDeath(died + 1)
    }
    if (getPCDeath() != getNLocalDeath() && DEATH_LINK == true && DEATH_LINK_TRIGGERED == false)
    {
        detect_death = true
        var died = getPCDeath()
        setPCDeath(died + 1)
        DEATH_LINK_TRIGGERED = true
        var randomDeathMsg = DEATH_MESSAGES[Math.floor(Math.random() * (DEATH_MESSAGES.length))]
         MESSAGE_TABLE.push({Message: randomDeathMsg, Icon: 15})
    }
    else
        DEATH_LINK_TRIGGERED = false

    if (getPCTag() != getNLocalTag() && TAG_LINK == false)
    {
        var tag = getPCTag()
        setPCTag(tag + 1)
    }
    if (getPCTag() != getNLocalTag() && TAG_LINK == true && TAG_LINK_TRIGGERED == false)
    {
        detect_tag = true
        var tag = getPCTag()
        setPCTag(tag + 1)
        TAG_LINK_TRIGGERED = true
    }
    else
        TAG_LINK_TRIGGERED = false

    retTable["scriptVersion"] = SCRIPT_VERSION;
    retTable["playerName"] = PLAYER;
    retTable["deathlinkActive"] = DEATH_LINK;
    retTable["taglinkActive"] = TAG_LINK;
    retTable["isDead"] = detect_death;
    retTable["isTag"] = detect_tag;
    retTable["jiggies"] = jiggy_check()
    retTable["jinjos"] = jinjo_check()
    retTable["pages"] = pages_check()
    retTable["honeycomb"] = honeycomb_check()
    retTable["glowbo"] = glowbo_check()
    retTable["doubloon"] = doubloon_check()
    retTable["notes"] = notes_check()
    retTable["hag"] = checkRealFlag(ADDRESS_MAP["H1"]["1230027"].addr, ADDRESS_MAP["H1"]["1230027"].bit)
    retTable["unlocked_moves"] = jamjar_check();
    retTable["treble"] = treble_check();
    retTable["stations"] = train_station_check();
    retTable["chuffy"] = chuffy_check();
    retTable["jinjofam"] = jinjo_family_check();
    retTable["worlds"] = UNLOCKED_WORLDS;
    retTable["mystery"] = mystery_check();
    retTable["roysten"] = roysten_check();
    retTable["cheato_rewards"] = cheato_rewards_check();
    retTable["honeyb_rewards"] = honey_b_check();
    retTable["jiggy_chunks"] = jiggy_chunks_check();
    retTable["goggles"] = amaze_check();
    retTable["roar"] = roar_check();
    retTable["dino_kids"] = dino_kids_check();
    retTable["nests"] = nest_check();
    retTable["signposts"] = signpost_check();
    retTable["silos"] = warpsilo_check();
    retTable["warppads"] = warppad_check();
    retTable["boggy_kids"] = boggy_kids_check();
    retTable["alien_kids"] = alien_kids_check();
    retTable["skivvies"] = skivvies_check();
    retTable["fit_events"] = mr_fit_events_check();
    retTable["bt_tickets"] = bttickets_check();
    retTable["green_relics"] = grrelic_check();
    retTable["beans"] = beans_check();

    retTable["DEMO"] = false;
    retTable["sync_ready"] = "true"

    if (CURRENT_MAP == null)
        retTable["banjo_map"] = 0x0;
    else
        retTable["banjo_map"] = CURRENT_MAP;
    if (DEBUGLVL3 == true)
        print("Send Data")

    var msg = JSON.stringify(retTable)+"\n"
    BT_SOCK.write(msg) 
}

function getSlotData()
{
    var retTable = {getSlot: true}
    if(DEBUGLVL2 == true)
        print("Encoding getSlot");
    var msg = JSON.stringify(retTable)+"\n"
    BT_SOCK.write(msg)
    BT_SOCK.on('data', function(d){
        if(DEBUGLVL2 == true)
            console.print("Processing Slot Data");
        AP_TIMEOUT_COUNTER = 0
        try {
            var data = ""
            if(d.toString().length == 1) //empty packet
                return
            if(BUFFER.length > 0)
            {
                BUFFER = BUFFER + d.toString()
                var data = JSON.parse(BUFFER)
            } else {
                var data = JSON.parse(d.toString())
            }
            if(data.slot_seed != undefined)
            {
                process_slot(data)
                BUFFER = ""
            }
            if(data.items != undefined)
            {
                process_block(data)
                console.log("Block Processed")
                BUFFER = ""
            }
        } catch(error) 
        {
            //console.log(error)
            //console.log(BUFFER)
            //console.log(d.toString())
            //console.log(d.toString().length)
            if(BUFFER == 0)
                BUFFER = d.toString()
            return
        }     
    })
}

function process_slot(json_object)
{
    //console.print(json_object)
    //try{
    if(DEBUGLVL3 == true)
    {
        print("slot_data")
        print(block)
        print("EO_slot_data")
    }
    if(json_object.slot_player != undefined && json_object.slot_player != "")
        PLAYER = json_object.slot_player
    if(json_object.slot_seed != undefined && json_object.slot_seed != "")
    {
        SEED = json_object.slot_seed
        writeSetting(BTH.setting_seed, SEED)
    }

    if (json_object.slot_dialog_character != undefined && json_object.slot_dialog_character != "")
        DIALOG_CHARACTER = json_object.slot_dialog_character
    if (json_object.slot_deathlink != undefined && json_object.slot_deathlink != 0)
        DEATH_LINK = true
    if (json_object.slot_taglink != undefined && json_object.slot_taglink != 0)
        TAG_LINK = true
    if (json_object.slot_tower_of_tragedy != undefined)
        writeSetting(BTH.setting_tot, json_object.slot_tower_of_tragedy)
    if(json_object.slot_randomize_bk_moves != undefined)
    {
        var ENABLE_AP_BK_MOVES = json_object.slot_randomize_bk_moves
        if(ENABLE_AP_BK_MOVES == 0)
        {
            setItem(ITEM_TABLE["AP_ITEM_DIVE"], 1)
            setItem(ITEM_TABLE["AP_ITEM_FPAD"], 1)
            setItem(ITEM_TABLE["AP_ITEM_FFLIP"], 1)
            setItem(ITEM_TABLE["AP_ITEM_EGGSHOOT"], 1)
            setItem(ITEM_TABLE["AP_ITEM_ROLL"], 1)
            setItem(ITEM_TABLE["AP_ITEM_TTROT"], 1)
            setItem(ITEM_TABLE["AP_ITEM_TJUMP"], 1)
            setItem(ITEM_TABLE["AP_ITEM_CLIMB"], 1)
            setItem(ITEM_TABLE["AP_ITEM_FLUTTER"], 1)
            setItem(ITEM_TABLE["AP_ITEM_WWING"], 1)
            setItem(ITEM_TABLE["AP_ITEM_BBUST"], 1)
            setItem(ITEM_TABLE["AP_ITEM_TTRAIN"], 1)
            setItem(ITEM_TABLE["AP_ITEM_ARAT"], 1)
            setItem(ITEM_TABLE["AP_ITEM_BEGGS"], 1)
            setItem(ITEM_TABLE["AP_ITEM_GRAT"], 1)
            setItem(ITEM_TABLE["AP_ITEM_BBARGE"], 1)
            setItem(ITEM_TABLE["AP_ITEM_SSTRIDE"], 1)
            setItem(ITEM_TABLE["AP_ITEM_BBOMB"], 1)
        }
        else if(ENABLE_AP_BK_MOVES == 1)
        {
            setItem(ITEM_TABLE["AP_ITEM_TJUMP"], 1)
            setItem(ITEM_TABLE["AP_ITEM_TTROT"], 1)
        }
    }
    if(json_object.slot_speed_up_minigames != undefined && json_object.slot_speed_up_minigames != 0)
        writeSetting(BTH.setting_minigames, json_object.slot_speed_up_minigames)
    if(json_object.slot_skip_puzzles != undefined && json_object.slot_skip_puzzles != 0)
        writeSetting(BTH.setting_puzzle, json_object.slot_skip_puzzles)
    if(json_object.slot_backdoors != undefined && json_object.slot_backdoors != 0)
        writeSetting(BTH.setting_backdoors, json_object.slot_backdoors)
    if (json_object.slot_open_gi_entrance != undefined && json_object.slot_open_gi_entrance != 0)
        writeSetting(BTH.setting_gi_open_frontdoor, json_object.slot_open_gi_entrance)
    if (json_object.slot_randomize_tickets != undefined && json_object.slot_randomize_tickets != 0)
        writeSetting(BTH.setting_randomize_tickets, json_object.slot_randomize_tickets)
    if (json_object.slot_randomize_green_relics != undefined && json_object.slot_randomize_green_relics != 0)
        writeSetting(BTH.setting_randomize_green_relics, json_object.slot_randomize_green_relics)
    if (json_object.slot_randomize_beans != undefined && json_object.slot_randomize_beans != 0)
        writeSetting(BTH.setting_randomize_beans, json_object.slot_randomize_beans)
    if (json_object.slot_skip_klungo != undefined && json_object.slot_skip_klungo != 0)
        writeSetting(BTH.setting_klungo, json_object.slot_skip_klungo)
    if (json_object.slot_victory_condition != undefined)
    {
        GOAL_TYPE = json_object.slot_victory_condition
        writeSetting(BTH.setting_victory_condition, json_object.slot_victory_condition)
    }
    if (json_object.slot_randomize_chuffy != undefined && json_object.slot_randomize_chuffy != 0)
        writeSetting(BTH.setting_chuffy, json_object.slot_randomize_chuffy)
    if (json_object.slot_nestsanity != undefined && json_object.slot_nestsanity != 0)
        writeSetting(BTH.setting_nests, json_object.slot_nestsanity)
    if (json_object.slot_extra_cheats != undefined && json_object.slot_extra_cheats != 0)
        writeSetting(BTH.setting_extra_cheats, json_object.slot_extra_cheats)
    if (json_object.slot_easy_canary != undefined && json_object.slot_easy_canary != 0)
        writeSetting(BTH.setting_easy_canary, json_object.slot_easy_canary)
    if (json_object.slot_minigame_hunt_length != undefined && json_object.slot_minigame_hunt_length != "")
        MGH_LENGTH = json_object.slot_minigame_hunt_length
    if (json_object.slot_boss_hunt_length != undefined && json_object.slot_boss_hunt_length != "")
        BH_LENGTH = json_object.slot_boss_hunt_length
    if (json_object.slot_jinjo_family_rescue_length != undefined && json_object.slot_jinjo_family_rescue_length != "")
        JFR_LENGTH = json_object.slot_jinjo_family_rescue_length
    if (json_object.slot_token_hunt_length != undefined && json_object.slot_token_hunt_length != "")
        TH_LENGTH = json_object.slot_token_hunt_length
    if (json_object.slot_world_requirements != undefined)
    {
        var keys = Object.keys(json_object.slot_world_requirements)
        for (var i = 0; i < keys.length; i++) 
        {
            var level = keys[i]
            var proper_level_name = level
            var locationId = json_object.slot_world_order[level]
            if(level == "Mayahem Temple")
            {
                setSettingJiggyRequirements(0, json_object.slot_world_requirements[level])
            }
            else if(level == "Glitter Gulch Mine")
            {
                setSettingJiggyRequirements(1, json_object.slot_world_requirements[level])
            }
            else if(level == "Witchyworld")
            {
                setSettingJiggyRequirements(2, json_object.slot_world_requirements[level])
            }
            else if(level == "Jolly Roger's Lagoon - Town Center")
            {
                proper_level_name = "Jolly Roger's Lagoon"
                setSettingJiggyRequirements(3, json_object.slot_world_requirements[level])
            }
            else if(level == "Terrydactyland")
            {
                setSettingJiggyRequirements(4, json_object.slot_world_requirements[level])
            }
            else if(level == "Outside Grunty Industries")
            {
                proper_level_name = "Grunty Industries"
                setSettingJiggyRequirements(5, json_object.slot_world_requirements[level])
            }
            else if(level == "Hailfire Peaks")
            {
                setSettingJiggyRequirements(6, json_object.slot_world_requirements[level])
            }
            else if(level == "Cloud Cuckooland")
            {
                setSettingJiggyRequirements(7, json_object.slot_world_requirements[level])
            }
            else if(level == "Cauldron Keep")
            {
                setSettingJiggyRequirements(8, json_object.slot_world_requirements[level])
            }
            var map = Object.keys(WORLD_ENTRANCE_MAP)
            for(var m=0;m < map.length;m++)
            {
                var world = map[m]
                if(WORLD_ENTRANCE_MAP[world].defaultName == level)
                {
                    WORLD_ENTRANCE_MAP[world]["defaultCost"] = json_object.slot_world_requirements[level]
                    WORLD_ENTRANCE_MAP[world]["locationId"] = locationId.toString()
                }
            }
        }
    }
    if (json_object.slot_silo_costs != undefined)
    {
        var key = Object.keys(json_object.slot_silo_costs)
        for (var i = 0; i < keys.length; i++) 
        {
            var locationId = key[i]
            var value =  json_object.slot_silo_costs[locationId]
            setSettingSiloRequirements(JAMJAR_SILO_TABLE[locationId], value)
        }
    }
    if (json_object.slot_preopened_silo != undefined)
    {
        var values = Object.keys(json_object.slot_preopened_silo)
        for(var i = 0; i < values.length; i++)
        {
            if (json_object.slot_preopened_silo[i] == 1230870)
            {
                setItem(ITEM_TABLE["AP_ITEM_SILO_JINJO_VILLAGE"], 1)
                SILO_MESSAGE = "The Isle O' Hags Jinjo Village Silo is open."
            }
            if (json_object.slot_preopened_silo[i] == 1230871)
            {
                setItem(ITEM_TABLE["AP_ITEM_SILO_WOODED_HOLLOW"], 1)
                SILO_MESSAGE = "The Isle O' Hags Wooded Hollow Silo is open."
                //console.print("The Isle O' Hags Wooded Hollow Silo is open.")
            }
            if (json_object.slot_preopened_silo[i] == 1230872)
            {
                setItem(ITEM_TABLE["AP_ITEM_SILO_PLATEAU"], 1)
                SILO_MESSAGE = "The Isle O' Hags Plateau Silo is open."
            }
            if (json_object.slot_preopened_silo[i] == 1230873)
            {
                setItem(ITEM_TABLE["AP_ITEM_SILO_PINE_GROVE"], 1)
                SILO_MESSAGE = "The Isle O' Hags Pine Grove Silo is open."
            }
            if (json_object.slot_preopened_silo[i] == 1230874)
            {
                setItem(ITEM_TABLE["AP_ITEM_SILO_CLIFF_TOP"], 1)
                SILO_MESSAGE = "The Isle O' Hags Cliff Top Silo is open."
            }
            if (json_object.slot_preopened_silo[i] == 1230875)
            {
                setItem(ITEM_TABLE["AP_ITEM_SILO_WASTELAND"], 1)
                SILO_MESSAGE = "The Isle O' Hags Wasteland Silo is open."
            }
            if (json_object.slot_preopened_silo[i] == 1230876)
            {
                setItem(ITEM_TABLE["AP_ITEM_SILO_QUAGMIRE"], 1)
                SILO_MESSAGE = "The Isle O' Hags Quagmire Silo is open."
            }
        }
    }
    if (json_object.slot_randomize_warp_pads != undefined && json_object.slot_randomize_warp_pads != 0)
        writeSetting(BTH.setting_warppads, json_object.slot_randomize_warp_pads)
    if (json_object.slot_cheato_rewards != undefined && json_object.slot_cheato_rewards != 0)
        writeSetting(BTH.setting_cheato_rewards, json_object.slot_cheato_rewards)
    if (json_object.slot_honeyb_rewards != undefined && json_object.slot_honeyb_rewards != 0)
        writeSetting(BTH.setting_honeyb_rewards, json_object.slot_honeyb_rewards)
    if (json_object.slot_auto_enable_cheats != undefined && json_object.slot_auto_enable_cheats != 0)
        writeSetting(BTH.setting_automatic_cheats, json_object.slot_auto_enable_cheats)
    if (json_object.slot_randomize_silos != undefined && json_object.slot_randomize_silos != 0)
        writeSetting(BTH.setting_warpsilos, json_object.slot_randomize_silos)
    if (json_object.slot_hints != undefined && (json_object.slot_hints_activated != 0 || json_object.slot_randomize_signposts != 0))
    {
        writeSetting(BTH.setting_signpost_hints, 1)
        var sign_id = 0
        var keys = Object.keys(json_object.slot_hints)
        for (var i = 0; i < keys.length; i++)
        {
            var sign_locationId = keys[i]
            var hintdata = json_object.slot_hints[sign_locationId]
            sign_id = ADDRESS_MAP["SIGNPOSTS"][sign_locationId]
            setHintMessages(sign_id, hintdata["text"])
        }
    }
    if (json_object.slot_version != undefined && json_object.slot_version != "")
    {
        CLIENT_VERSION = json_object.slot_version
        if (CLIENT_VERSION != BT_VERSION)
        {
            VERROR = true
            return false
        }
        var ROMversion = getRomVersion()
        if (ROMversion != CLIENT_VERSION)
        {
            VERROR = true
            return false
        }
    }
    if (json_object.slot_open_hag1 != undefined && json_object.slot_open_hag1 != 0)
    {
        OPEN_HAG1 = true
        hag1_open()
    }
    if (json_object.slot_zones != undefined)
    {
        zoneWarp(json_object.slot_zones) //issue
    }
    printGoalInfo();
    console.print("Slot Data Processed!\r\n")
    //} catch(err) { console.log(err)}
    return true
}

function printGoalInfo()
{
    var randomEncouragment = ENCOURAGEMENT[Math.floor(Math.random() * (ENCOURAGEMENT.length))]
    if (GOAL_TYPE != null && MGH_LENGTH != null && BH_LENGTH != null &&
        JFR_LENGTH != null && TH_LENGTH != null)
    {
        var message = ""
        if (GOAL_TYPE == 0)
        {
            message = "You need to hunt down Grunty in her HAG1 and put her back in the ground!\nGood Luck and" + randomEncouragment;
            //console.print("You need to hunt down Grunty in her HAG1 and put her back in the ground!\nGood Luck and" + randomEncouragment+"\r\n")
            writeSetting(BTH.setting_max_mumbo_tokens, 0)
        }
        else if (GOAL_TYPE == 1 && MGH_LENGTH == 15)
        {
            message = "You are hunting down all 15 of the Mumbo Tokens found in Grunty's dastardly minigames!\nGood luck and" + randomEncouragment;
            writeSetting(BTH.setting_max_mumbo_tokens, MGH_LENGTH)
        }
        else if (GOAL_TYPE == 1 && MGH_LENGTH < 15)
        {
            message = "You are hunting for " + MGH_LENGTH.toString() + " Mumbo Tokens from Grunty's dastardly minigames!\nGood Luck and" + randomEncouragment;
            writeSetting(BTH.setting_max_mumbo_tokens, MGH_LENGTH)
        }
        else if ( GOAL_TYPE == 2 && BH_LENGTH == 8)
        {
            message = "You are hunting down all 8 Mumbo Tokens from each world boss!\nGood Luck and" + randomEncouragment;
            writeSetting(BTH.setting_max_mumbo_tokens, BH_LENGTH)
        }
        else if ( GOAL_TYPE == 2 && BH_LENGTH < 8)
        {
            message = "You are hunting for " + BH_LENGTH.toString() + " Mumbo Tokens from the 8 world bosses!\nGood Luck and" + randomEncouragment;
            writeSetting(BTH.setting_max_mumbo_tokens, BH_LENGTH)
        }
        else if ( GOAL_TYPE == 3 && JFR_LENGTH == 9)
        {
            message ="You are trying to rescue all 9 Jinjo families and retrieve their Mumbo Tokens!\nGood Luck and" + randomEncouragment;
            writeSetting(BTH.setting_max_mumbo_tokens, JFR_LENGTH)
        }
        else if ( GOAL_TYPE == 3 && JFR_LENGTH < 9)
        {
            message = "You are trying to rescue " + JFR_LENGTH.toString() + " of the 9 Jinjo families and retrieve their Mumbo Tokens!\nGood Luck and" + randomEncouragment;
            writeSetting(BTH.setting_max_mumbo_tokens, JFR_LENGTH)
        }
        else if ( GOAL_TYPE == 4)
        {
            message ="You absolute mad lad! You're doing the Wonder Wing Challenge!\nGood Luck and" + randomEncouragment;
            writeSetting(BTH.setting_max_mumbo_tokens, 32)
        }
        else if ( GOAL_TYPE == 5)
        {
            message = "You are trying to find " + TH_LENGTH.toString() + " Mumbo Tokens scattered throughout the Isle O' Hags!\nGood Luck and" + randomEncouragment;
            writeSetting(BTH.setting_max_mumbo_tokens, TH_LENGTH)
        }
        else if ( GOAL_TYPE == 6)
        {
            message = "You need to defeat " + BH_LENGTH.toString() + " Bosses in order to defeat HAG-1!\nGood Luck and" + randomEncouragment;
            writeSetting(BTH.setting_max_mumbo_tokens, BH_LENGTH)
        }
        if (GOAL_PRINTED == false)
        {
            if (DIALOG_CHARACTER == 110)
                MESSAGE_TABLE.push({Message: message, Icon: 5})
            else
                MESSAGE_TABLE.push({Message: message, Icon: DIALOG_CHARACTER})
            GOAL_PRINTED =true
        }
    }
}


function receive()
{
    if(PLAYER == "" && SEED == 0)
    {
        getSlotData()
    }
    else
    {
        // SEND the message
        SendToBTClient()
        console.print("Sent BTClient Data\r\n")
        /*
            BELOW IS PART OF GetSlotData.. its a listening event.
            BT_SOCK.on('data', function(d){
                if(DEBUGLVL3 == true)
                    console.print("Processing Block\r\n");
                AP_TIMEOUT_COUNTER = 0
                try {
                    var data = JSON.parse(d.toString())
                    process_block(data)   
                } 
                catch(error) 
                {
                    return
                }     
            })
        */
        if (DEBUGLVL3 == true)
        {
            print("Finish");
        }
    }
}

function messageQueue()
{
    var processed = false;
    if (getCurrentQueue() == getPCQueue())
    {
        for(var i = 0; i < MESSAGE_TABLE.length; i++)
        {
            setDialog(MESSAGE_TABLE[i].Message, MESSAGE_TABLE[i].Icon)
            processed = true
            break
        }
        if (processed)
        {
            MESSAGE_TABLE = MESSAGE_TABLE.reverse()
            MESSAGE_TABLE.pop()
            MESSAGE_TABLE = MESSAGE_TABLE.reverse()
        }
        else
            writeSetting(BTH.setting_dialog_character, DIALOG_CHARACTER)
    }
}

///Main Loop




function main(){
    if(init == false)
    {
        init = true
        if(getRomVersion() == "0")
        {
            console.error("This is the vanilla rom. Please use the patched version of Banjo-Tooie.\r\n")
            WRONGROM()
        }
        console.print("We only support Bizhawk Version 2... Oh this is PJ64... nevermind...\r\n")
        console.print("Banjo-Tooie Archipelago Version " + BT_VERSION+"\r\n")
        console.print("Starting server\r\n")
        var SERVER = new Server({port: 21221})
        SERVER.on('connection', function(socket){
            BT_SOCK = socket
            console.print("Connected\r\n")
        })
        
        for(var i=0; i < ROM_ITEM_TABLE.length; i++)
        {
            ITEM_TABLE[ROM_ITEM_TABLE[i]] = i
        }
        for(var i=0; i < TRAPS.length; i++)
        {
            TRAP_TABLE[TRAPS[i]] = i
        }
        for(var i=0; i < DIALOG_KEY_TABLE.length; i++)
        {
            DIALOG_CHARACTER_TABLE[DIALOG_KEY_TABLE[i]] = i
        }
        for(var i=0; i < JAMJAR_SILO_LOCATIONS.length; i++)
        {
            JAMJAR_SILO_TABLE[JAMJAR_SILO_LOCATIONS[i]] = i
        }
        // console.print(ADDRESS_MAP["STATIONBTN"]["1230791"])
        // console.print(ASSET_MAP_CHECK[0x108]["NOTES"])
        //console.print(MAP_ENTRANCES[0x12B].access)

        // 0x12B : {
        // name: "Chilli Billi Crater",
        // entranceId: 1,
        // exitId: 0x16,
        // exitMap: 0x127,
        // access: [ITEM_TABLE["AP_ITEM_IEGGS"]],
        // reverse_access: [],
    }
    FRAME = FRAME + 1
    if(BT_SOCK != null)
    {
        if (FRAME % 30 == 1)
        {
            CURRENT_MAP = getMap()
            receive()
            messageQueue()
            mumbo_announce()
            if(PLAYER != null)
            {
                if (VERROR)
                {
                    console.print("ERROR: version mismatch. Please obtain the same version for everything")
                    console.print("The versions that you are currently using are:")
                    console.print("Connector Version: " + BT_VERSION)
                    console.print("Client Version: " + CLIENT_VERSION)
                    console.print("ROM Version: " + getRomVersion())
                    BT_SOCK.close()
                    SERVER.close()
                    return
                }
                if ((CURRENT_MAP != 0x158 && CURRENT_MAP != 0x18B && CURRENT_MAP != 0x0) && GOAL_PRINTED == true)
                {
                    GOAL_PRINTED = false
                }
                if (CURRENT_MAP == 0x158 && GOAL_PRINTED == false)
                {
                    printGoalInfo()
                }
                if (CURRENT_MAP == 0xAF && SEND_SILO_MSG == true)
                {
                    if (DIALOG_CHARACTER == 110)
                        MESSAGE_TABLE.push({Message: SILO_MESSAGE, Icon: 17})
                    else
                        MESSAGE_TABLE.push({Message: SILO_MESSAGE, Icon: DIALOG_CHARACTER})
                    SEND_SILO_MSG = false
                }
                else if (CURRENT_MAP == 0x142 && SEND_SILO_MSG == true)
                {
                    SEND_SILO_MSG = false
                }
            }
        }
    }
}

events.ondraw(function(){
    main()
})