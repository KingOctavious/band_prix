from lexicon import Lexicon
from part_of_speech import Part_Of_Speech as pos

country_nouns = [
  ['America'],
	['American flag', 'American flags'],
  ['barbeque'],
	['beer'],
	['biscuit', 'biscuits'],
	['boot', 'boots'],
	['burger', 'burgers'],
	['can of beer', 'cans of beer'],
	['corn field', 'corn fields'],
	['cousin', 'cousins'],
	['cowboy hat', 'cowboy hats'],
	['cow', 'cows'],
	['cousin', 'cousins'],
	['dog', 'dogs'],
	['huntin\' dog', 'huntin\' dogs'],
	['fishin\' boat'],
	['farm'],
	['front porch', 'blue jeans'],
	['guitar', 'guitars'],
	['gun', 'guns'],
	['hog', 'hogs'],
	['horse', 'horses'],
	['iced tea', 'collared greens'],
	['lemonade'],
	['jug of moonshine', 'jugs of moonshine'],
	['memory', 'memories'],
	['mud field'],
	['pickup', 'pickup trucks'],
	['rockin\' chair', 'rockin\' chairs'],
	['shotgun', 'shotguns'],
	['tobacco'],
	['tractor'],
	['truck', 'trucks'],
	['twelve pack', 'twelve packs'],
	['wheat field', 'wheat fields']
]

country_verbs = [
	'always had',
	'bought',
	'daydreamed about',
	'drank with',
	'forgave',
	'found',
	'got',
	'hosed off',
  'kissed',
	'laid with',
	'looked at',
	'lost',
	'loved',
	'never forgot',
	'picked up',
	'pulled out',
	'remembered',
	'reminisced upon',
	'sang about',
	'sat with',
	'saw',
	'shot',
	'savored',
	'stared at',
	'talked about',
	'thought about',
	'wanted',
	'went fishin\' with',
	'went hunting with',
	'wished for'
]

country_adjectives = [
  'Alabama',
  'all-American',
	'American',
	'baby\'s',
	'best',
	'brand new',
	'cheap',
  'corn-fed',
	'country',
#	'Daddy\'s,
	'dang',
	'dern',
	'dirty',
	'doggone',
	'down-home',
	'family',
	'fancy',
#	'girlfriend\'s',
	'good old',
#	'Granddaddy\'s',
#	'Grandmomma\'s',
	'lucky',
  'Mississippi',
#	'Momma\'s',
	'muddy',
	'neighborhood',
	'ol\'',
	'old',
	'old-fashioned',
	'scuffed',
	'shiny',
	'Sunday',
  'supersized',
	'Tennessee',
	'Texas',
	'trusty',
	'worn-out'
]

country_exclamations = [
	'awww yeah',
	'dang',
  'doggonit',
	'get down',
	'heck yeah',
  'hot dang',
	'hot dog',
	'uh huh',
  'wee hoo',
  'woo doggy',
	'yeah buddy',
	'yeeha'
]

metal_nouns = [
	['abomination', 'abominations'],
	['afterlife'],
	['angel', 'angels'],
	['ash', 'ashes'],
	['beast', 'beasts'],
	['blood', 'thoughts'],
  ['bone', 'bones'],
	['chain', 'chains'],
	['coffin', 'coffins'],
	['corpse', 'corpses'],
	['darkness'],
	['death'],
	['demon', 'demons'],
	['despair', 'depths'],
	['dream', 'dreams'],
	['electric chair', 'electric chairs'],
  ['eve', 'evenings'],
	['eye', 'eyes'],
	['feeling', 'feelings'],
	['fire', 'fires'],
	['flesh'],
	['grave', 'graves'],
	['hammer', 'hammers'],
  ['headstone', 'headstones'],
  ['innocence', 'innocents'], # Yes, I know these are two different things
	['killer', 'killers'],
	['knight', 'knights'],
	['life', 'lives'],
	['memory', 'memories'],
	['night', 'nights'],
	['nightmare', 'nightmares'],
	['ocean', 'oceans'],
  ['paradise'],
  ['parasite', 'parasites'],
	['penance'],
	['pit', 'pits'],
  ['prisoner', 'prisoners'],
  ['sea', 'seas'],
	['skull', 'skulls'],
	['serpent', 'serpents'],
	['skeleton', 'skeletons'],
	['stone', 'stones'],
  ['sword', 'swords'],
	['tomb', 'tombs'],
	['triumph'],
  ['void'],
	['war', 'wars']
]

metal_adjectives = [
	'ancient',
	'black',
	'bleeding',
	'blessed',
	'burning',
	'cold',
	'creeping',
  'cruel',
	'dark',
	'dead',
	'desolate',
	'desperate',
	'doomed',
	'dry',
	'dying',
	'empty',
	'eternal',
  'fiery',
	'forgotten',
	'golden',
	'guilty',
	'immortal',
	'infinite',
  'iron',
	'looming',
	'lost',
	'marching',
	'metal',
  'mangled',
  'misshapen',
	'noble',
  'pathetic',
  'pleading',
  'primordial',
  'remoreseful',
	'scorched',
	'screaming',
  'spiked',
	'steel',
	'victorious',
	'undead',
	'unforgiven',
	'weeping'
]

metal_verbs = [
	'bore',
	'buried',
	'captured',
	'cast away',
	'created',
	'destroyed',
  'devoured',
	'died with',
  'disdained',
	'doomed',
  'drank',
	'electrocuted',
	'enshrined',
	'entombed',
	'eviscerated',
  'executed',
	'found',
	'hunted',
	'gazed upon',
	'glorified',
	'hated',
	'killed',
	'lived with',
	'looked at',
	'lost',
	'materialized',
	'planted',
	'pulverized',
	'ravaged',
	'remembered',
	'rocked',
	'saw',
	'smashed',
	'took'
]

metal_exclamations = [
  'oh yeah',
  'that\'s right',
  'whooo',
  'yeah'
]

jam_band_nouns = [
	['bard', 'bards'],
	['bird', 'birds'],
	['cloud', 'clouds'],
	['drug', 'drugs'],
	['egg', 'eggs'],
	['elf', 'elves'],
	['elixir', 'elixirs'],
	['fire', 'fires'],
	['flower', 'flowers'],
	['fountain', 'fountains'],
	['fruit', 'fruits'],
	['gazelle', 'gazelles'],
	['ghost', 'ghosts'],
	['guitar', 'guitars'],
	['herb', 'herbs'],
	['hero', 'heroes'],
	['hookah', 'hookahs'],
	['honey'],
	['jellyfish', 'jellyfish'],
	['jester', 'jesters'],
	['light', 'lights'],
	['life', 'lives'],
	['madman', 'madmen'],
	['mountain', 'mountains'],
	['mushroom', 'mushrooms'],
	['ocean', 'oceans'],
	['oracle', 'oracles'],
  ['paradise', 'people'],
	['party', 'parties'],
	['potion', 'potions'],
	['pudding'],
	['rain'],
	['rainbow', 'rainbows'],
	['room', 'rooms'],
	['sage', 'sages'],
	['smoke'],
	['star', 'stars'],
	['sun', 'suns'],
	['sunshine', 'people'],
	['temple', 'temples'],
	['tree', 'trees'],
	['turtle', 'turtles'],
	['waterfall', 'waterfalls'],
	['whale', 'whales'],
	['wine']
]

jam_band_adjectives = [
	'ancient',
	'blazing',
	'bouncing',
	'breathing',
	'cosmic',
	'dancing',
	'drifting',
	'eternal',
	'floating',
	'flying',
  'frozen',
  'giant',
	'glowing',
	'golden',
	'happy',
	'hazy',
	'hidden',
  'incandescent',
	'invisible',
	'jumping',
	'laughing',
	'lazy',
	'living',
	'luminescent',
	'magic',
	'melting',
	'newborn',
	'pulsing',
	'purple',
	'rainbow',
	'round',
	'running',
	'shining',
	'singing',
	'silver',
	'sleeping',
	'smiling',
	'spinning',
  'tiny',
	'tired',
	'twilight',
	'warm'
]

jam_band_verbs = [
	'befriended',
	'beheld',
	'breathed',
	'danced with',
	'drank',
	'drank with',
	'dreamed of',
	'found',
	'gazed upon',
	'inhaled',
	'journeyed with',
	'laughed with',
	'learned about',
	'lived with',
	'looked at',
	'lost',
	'loved',
	'melted',
	'met',
	'never forgot',
	'painted',
	'remembered',
	'sang with',
	'saw',
	'sought',
	'smelled',
	'smoked',
	'talked with',
	'told the story of',
	'walked with',
	'welcomed'
]

jam_band_exclamations = [
  'blaze it',
  'oh yeah',
  'that\'s right',
  'whooo',
  'yeah'
]


cm_nouns = []
for item in country_nouns:
  cm_nouns.append(item)
for item in metal_nouns:
  cm_nouns.append(item)

cm_verbs = []
for item in country_verbs:
  cm_verbs.append(item)
for item in metal_verbs:
  cm_verbs.append(item)

cm_adjectives = []
for item in country_adjectives:
  cm_adjectives.append(item)
for item in metal_adjectives:
  cm_adjectives.append(item)



country = Lexicon('country', country_nouns, country_verbs, country_adjectives, country_exclamations)
metal = Lexicon('heavy metal', metal_nouns, metal_verbs, metal_adjectives, metal_exclamations)
jam_band = Lexicon('jam band', jam_band_nouns, jam_band_verbs, jam_band_adjectives, jam_band_exclamations)

country_metal = Lexicon('country metal fusion', cm_nouns, cm_verbs, cm_adjectives, metal_exclamations)



genres_lexicons = [
  (country, 'country'),
  (metal, 'heavy metal'),
  (jam_band, 'jam band')
]
