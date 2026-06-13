"""
Grammar skill descriptions for all 60 skills in taxonomy_v2.json.
Each entry drives the quality of Claude's generation prompt.
"""
from typing import TypedDict


class SkillDescription(TypedDict):
    description: str
    key_structures: str
    example_correct: str
    example_error: str
    common_student_errors: list[str]
    time_markers: list[str]


SKILL_DESCRIPTIONS: dict[str, SkillDescription] = {
    "past_simple": {
        "description": "Regular (-ed) and irregular past simple for completed actions at a specific past time",
        "key_structures": "S + V-ed/V2; Did + S + V?; S + didn't + V",
        "example_correct": "She finished her homework an hour ago.",
        "example_error": "She finish her homework an hour ago.",
        "common_student_errors": [
            "Using present simple instead of past simple",
            "Incorrect irregular forms (goed, buyed, catched, thinked)",
            "Forgetting did/didn't in questions and negatives",
            "Double past marking: didn't finished, didn't went",
        ],
        "time_markers": ["yesterday", "last week", "last night", "ago", "in 2019", "when I was young"],
    },

    "connectors_basic": {
        "description": "Basic coordinating and subordinating connectors linking clauses: and, but, or, so, because",
        "key_structures": "Clause + and/but/or/so/because + clause",
        "example_correct": "I was tired, so I went to bed early.",
        "example_error": "I was tired, because I went to bed early.",
        "common_student_errors": [
            "Confusing so (result) with because (reason)",
            "Using but instead of or in alternatives",
            "Placing connector at start of sentence: 'Because I was tired, ...' — not an error but sometimes over-used",
            "Using and to connect contrasting ideas instead of but",
        ],
        "time_markers": [],
    },

    "quantifiers_basic": {
        "description": "Basic quantifiers with countable and uncountable nouns: some, any, much, many, a lot of, enough, how much/many",
        "key_structures": "some/any + noun; much + uncountable; many + countable plural; a lot of + noun",
        "example_correct": "There isn't much milk left in the fridge.",
        "example_error": "There isn't many milk left in the fridge.",
        "common_student_errors": [
            "Using much with countable nouns (much books)",
            "Using many with uncountable nouns (many water)",
            "Using some in negatives/questions where any is required",
            "Omitting 'of' in a lot of",
        ],
        "time_markers": [],
    },

    "future_will": {
        "description": "Will for predictions, spontaneous decisions, promises, and offers about the future",
        "key_structures": "S + will + V; S + won't + V; Will + S + V?",
        "example_correct": "I think it will rain tomorrow.",
        "example_error": "I think it rains tomorrow.",
        "common_student_errors": [
            "Using present simple instead of will for predictions",
            "Using going to instead of will for spontaneous decisions",
            "Omitting will in conditional result clauses (If it rains, I go home)",
            "Contracting incorrectly: he'll not instead of he won't",
        ],
        "time_markers": ["tomorrow", "next week", "soon", "in the future", "one day"],
    },

    "prepositions_place_movement": {
        "description": "Prepositions showing static location (in, on, at, next to, opposite) and directional movement (to, into, out of, through, past)",
        "key_structures": "in/on/at + place; go/walk/run + to/into/past/through + place",
        "example_correct": "The keys are on the table next to the lamp.",
        "example_error": "The keys are at the table next to the lamp.",
        "common_student_errors": [
            "Confusing in (enclosed space) vs on (surface) vs at (point/location)",
            "Using to with home: go to home → go home",
            "Using in instead of into for movement: she walked in the room",
            "Confusing on/onto for movement onto surfaces",
        ],
        "time_markers": [],
    },

    "verb_complementation_basic": {
        "description": "Verbs followed by -ing form: enjoy, mind, avoid, finish, like, love, hate, prefer as gerund objects or subjects",
        "key_structures": "like/love/hate/enjoy/avoid/mind + -ing; -ing + V (gerund as subject)",
        "example_correct": "She enjoys reading novels in her free time.",
        "example_error": "She enjoys to read novels in her free time.",
        "common_student_errors": [
            "Using to-infinitive after enjoy/avoid/mind/finish",
            "Using base verb after these verbs (enjoys read)",
            "Confusing like + -ing (general preference) vs would like + to-inf (specific wish)",
        ],
        "time_markers": [],
    },

    "time_expressions": {
        "description": "Time expressions and markers that anchor sentences to a time frame: frequency adverbs, duration phrases, sequencers",
        "key_structures": "always/usually/often/sometimes/never + V; for/since/ago/already/yet/still; first/then/after that/finally",
        "example_correct": "She has already finished the report.",
        "example_error": "She already finished the report.",
        "common_student_errors": [
            "Using ago with present perfect (I have finished it 2 days ago)",
            "Using since with duration (since two hours → for two hours)",
            "Placing frequency adverbs after main verb (I go always to school)",
            "Confusing still vs yet in negatives",
        ],
        "time_markers": ["already", "yet", "still", "just", "ago", "since", "for", "always", "never", "sometimes"],
    },

    "determiners_deictics": {
        "description": "Demonstratives this/that/these/those and other deictic determiners to point to people, objects, or ideas in context",
        "key_structures": "this/that + singular noun; these/those + plural noun; this one vs that one",
        "example_correct": "Can you pass me that red pen on your desk?",
        "example_error": "Can you pass me this red pen on your desk?",
        "common_student_errors": [
            "Confusing proximity: this (near) vs that (far)",
            "Using singular this/that with plural nouns",
            "Omitting noun: 'this is good' vs 'this book is good'",
            "Overusing 'the' where a demonstrative is needed",
        ],
        "time_markers": [],
    },

    "prepositions_time": {
        "description": "Prepositions of time: at (clock times), on (days/dates), in (months/years/periods), during, by, until, from…to",
        "key_structures": "at + time; on + day/date; in + month/year/season; during + noun; by/until + deadline",
        "example_correct": "The meeting starts at 9 o'clock on Monday.",
        "example_error": "The meeting starts in 9 o'clock on Monday.",
        "common_student_errors": [
            "Using in instead of at for clock times",
            "Using in instead of on for days of the week",
            "Confusing by (deadline) vs until (duration up to a point)",
            "Using during + clause instead of during + noun phrase",
        ],
        "time_markers": ["at", "on", "in", "during", "by", "until", "from", "to"],
    },

    "articles": {
        "description": "Use of a/an (first mention, classification), the (shared knowledge, unique referents), and zero article (generalisations, proper nouns, uncountable/plural generics)",
        "key_structures": "a/an + singular countable (first mention); the + known/unique referent; Ø + plural/uncountable generalisation",
        "example_correct": "I saw a dog in the park. The dog was barking loudly.",
        "example_error": "I saw dog in park. Dog was barking loudly.",
        "common_student_errors": [
            "Omitting articles entirely (I have dog)",
            "Using the for generalisations (The dogs are friendly animals)",
            "Using a/an with uncountable nouns (a water, an information)",
            "Wrong article before vowel sounds: a apple → an apple",
        ],
        "time_markers": [],
    },

    "question_forms": {
        "description": "Wh- questions (what, where, when, who, how), yes/no questions with auxiliary inversion, tag questions, and negative questions",
        "key_structures": "Wh- + aux + S + V?; Do/Does/Did + S + V?; S + aux + V, tag?",
        "example_correct": "Where did she go last night?",
        "example_error": "Where she went last night?",
        "common_student_errors": [
            "Omitting auxiliary inversion: 'Where you live?' instead of 'Where do you live?'",
            "Using do/does with be: 'Does she be tired?'",
            "Incorrect tag question polarity (positive statement + positive tag)",
            "Wrong tense in Wh- questions: 'Where did she goes?'",
        ],
        "time_markers": [],
    },

    "superlatives": {
        "description": "Superlative adjectives (-est, most + adj) with the, and superlative adverbs for comparing within a group",
        "key_structures": "the + adj-est; the most + adj; the least + adj; one of the + superlative + plural noun",
        "example_correct": "Mount Everest is the highest mountain in the world.",
        "example_error": "Mount Everest is the most high mountain in the world.",
        "common_student_errors": [
            "Using most with short adjectives (most tall → tallest)",
            "Omitting the before superlative",
            "Double superlative: the most tallest",
            "Incorrect irregular forms (goodest, badest, more better)",
        ],
        "time_markers": [],
    },

    "present_continuous": {
        "description": "Present continuous for actions happening now, temporary situations, and fixed future arrangements",
        "key_structures": "S + am/is/are + V-ing; S + am/is/are + not + V-ing; Am/Is/Are + S + V-ing?",
        "example_correct": "She is studying for her exam right now.",
        "example_error": "She studies for her exam right now.",
        "common_student_errors": [
            "Using present simple for in-progress actions",
            "Using present continuous for stative verbs (I am knowing → I know)",
            "Omitting be auxiliary (she studying right now)",
            "Wrong be agreement: he are working",
        ],
        "time_markers": ["now", "right now", "at the moment", "currently", "today", "this week", "tonight"],
    },

    "modals_permission_requests": {
        "description": "Modal verbs for seeking permission (can, could, may) and making requests (can, could, would)",
        "key_structures": "Can/Could/May + I + V? (permission); Can/Could/Would + you + V? (request)",
        "example_correct": "Could you please open the window?",
        "example_error": "Would you can open the window?",
        "common_student_errors": [
            "Using two modals together: could would, might can",
            "Using infinitive with to after modal: could to go",
            "Confusing can (informal) vs may (formal) for permission",
            "Omitting please in formal requests",
        ],
        "time_markers": [],
    },

    "modals_preferences": {
        "description": "Expressing preferences and desires with want to, would like to, would rather, would love to, prefer",
        "key_structures": "would like/love/prefer + to-inf; would rather + base V; prefer + -ing/noun + to + -ing/noun",
        "example_correct": "I would rather stay home than go to the party.",
        "example_error": "I would rather to stay home than to go to the party.",
        "common_student_errors": [
            "Adding to after would rather: I'd rather to go",
            "Using would like with -ing: I'd like going → I'd like to go",
            "Confusing prefer + -ing/noun vs would prefer + to-inf",
            "Using want instead of would like in formal contexts",
        ],
        "time_markers": [],
    },

    "modals_suggestions": {
        "description": "Modal verbs and phrases for making suggestions (should, could, why don't, how about, let's, shall we) and offers (shall I, would you like)",
        "key_structures": "Should/Could + S + V; Why don't we + V?; How about + -ing?; Shall I/we + V?",
        "example_correct": "Why don't we take a taxi instead of walking?",
        "example_error": "Why don't we to take a taxi instead of walking?",
        "common_student_errors": [
            "Adding to after suggestion modals: should to go",
            "Using must instead of should for suggestions",
            "How about + infinitive instead of -ing: How about go?",
            "Shall used for non-first person (Shall he...?)",
        ],
        "time_markers": [],
    },

    "future_going_to": {
        "description": "Going to for plans and intentions already decided, and for predictions based on present evidence",
        "key_structures": "S + am/is/are + going to + V; S + isn't/aren't + going to + V",
        "example_correct": "Look at those dark clouds! It's going to rain.",
        "example_error": "Look at those dark clouds! It will rain.",
        "common_student_errors": [
            "Using will instead of going to for pre-planned intentions",
            "Omitting be: she going to travel",
            "Using gonna in formal writing",
            "Confusing going to (evidence-based prediction) vs will (general prediction)",
        ],
        "time_markers": ["tomorrow", "next week", "this weekend", "soon"],
    },

    "ditransitive_patterns": {
        "description": "Ditransitive verbs (give, send, show, tell, teach, buy, make) with double object or prepositional dative, and factitive patterns (make, find, keep + object + adjective)",
        "key_structures": "give sb sth / give sth to sb; make sb adj; find sth adj; keep sth adj",
        "example_correct": "She gave her friend a birthday present.",
        "example_error": "She gave to her friend a birthday present.",
        "common_student_errors": [
            "Inserting to before indirect object in double-object order",
            "Wrong preposition: give sth for sb instead of to sb",
            "Omitting object pronoun: she gave him vs she gave",
            "Confusing make sb do (causative) vs make sb adj (factitive)",
        ],
        "time_markers": [],
    },

    "adverb_formation_position": {
        "description": "Forming adverbs from adjectives (-ly), irregular adverbs (hard, fast, well), and their position relative to verbs and adjectives",
        "key_structures": "adj + -ly = adverb; adverb before adj; adverb after verb/object; frequency adverb before main verb",
        "example_correct": "She speaks English fluently and confidently.",
        "example_error": "She speaks English fluent and confident.",
        "common_student_errors": [
            "Using adjective form instead of adverb (drive careful → carefully)",
            "Wrong position: she fluently speaks English",
            "Hardely/fastly instead of hard/fast",
            "Goodly instead of well",
        ],
        "time_markers": [],
    },

    "modals_ability": {
        "description": "Can for present ability, could for past ability or polite possibility, be able to for all tenses where can/could is unavailable",
        "key_structures": "can/can't + V (present); could/couldn't + V (past); will be able to + V; was/were able to + V",
        "example_correct": "She could swim when she was five years old.",
        "example_error": "She can swim when she was five years old.",
        "common_student_errors": [
            "Using can for past ability instead of could",
            "Using could for specific past achievement instead of was able to",
            "Adding to after can: can to swim",
            "Using will can instead of will be able to",
        ],
        "time_markers": ["when I was young", "before", "already", "by next year"],
    },

    "possessives_genitive": {
        "description": "Possessive adjectives (my, your, his, her, our, their), possessive pronouns (mine, yours), and genitive 's / s' for ownership",
        "key_structures": "my/your/his/her/its/our/their + noun; noun + 's + noun; the … of …",
        "example_correct": "Is this your jacket or is it mine?",
        "example_error": "Is this your jacket or is it yours jacket?",
        "common_student_errors": [
            "Confusing possessive adjective vs pronoun: this is mine book → my book / this is mine",
            "Apostrophe errors: its vs it's; friends' vs friend's",
            "Using of instead of 's for people: the book of Maria → Maria's book",
            "Using her for his/its: the dog lost her bone",
        ],
        "time_markers": [],
    },

    "adjective_position_formation": {
        "description": "Position of adjectives before nouns and after linking verbs; order of multiple adjectives; formation by suffix (-ful, -less, -ous, -al, -ive, -ed, -ing)",
        "key_structures": "opinion-size-age-shape-colour-origin-material + noun; adj after be/seem/look/feel/taste/sound",
        "example_correct": "It was a beautiful old wooden table.",
        "example_error": "It was a wooden old beautiful table.",
        "common_student_errors": [
            "Wrong adjective order (colour before size: big blue → blue big)",
            "Using adjective instead of adverb after verb (she looks beautifully → beautiful)",
            "Suffix errors: bored vs boring, tired vs tiring",
            "Omitting hyphen in compound adjectives: well known → well-known",
        ],
        "time_markers": [],
    },

    "present_perfect": {
        "description": "Present perfect for life experiences (ever/never), recent past with current relevance (just/already/yet), and ongoing situations starting in the past (for/since)",
        "key_structures": "S + have/has + V3; Have/Has + S + V3?; S + haven't/hasn't + V3",
        "example_correct": "I have lived in this city since 2018.",
        "example_error": "I live in this city since 2018.",
        "common_student_errors": [
            "Using past simple with since/for: I lived here since 2018",
            "Using present simple instead of present perfect with since/for",
            "Using present perfect with definite past time: I have seen him yesterday",
            "Confusing been (visited and returned) vs gone (went and still there)",
        ],
        "time_markers": ["ever", "never", "already", "yet", "just", "recently", "since", "for", "so far", "up to now"],
    },

    "pronouns_indefinite_impersonal": {
        "description": "Indefinite pronouns (someone, anyone, everyone, no one, something, anything, everything, nothing) and impersonal you/one/they for general statements",
        "key_structures": "some-/any-/every-/no- + one/body/thing/where; You/One/They + V (impersonal)",
        "example_correct": "Has anyone seen my keys? I can't find them anywhere.",
        "example_error": "Has someone seen my keys? I can't find them somewhere.",
        "common_student_errors": [
            "Using someone/somewhere in questions/negatives instead of anyone/anywhere",
            "Using everyone + plural verb (everyone are → everyone is)",
            "Double negative: I don't know nothing → I don't know anything",
            "Confusing no one (no-space) vs nobody (one word)",
        ],
        "time_markers": [],
    },

    "present_simple_uses": {
        "description": "Special uses of present simple beyond habit/routine: instantaneous actions (I declare, I promise), sports commentary, instructions/recipes, historic present, and stative verbs",
        "key_structures": "S + V (stative: know, believe, contain, belong, mean, seem, own)",
        "example_correct": "I understand what you mean now.",
        "example_error": "I am understanding what you mean now.",
        "common_student_errors": [
            "Using continuous with stative verbs: I am knowing, she is believing",
            "Using simple present instead of continuous for actions in progress",
            "Forgetting third-person -s in stative contexts",
            "Using have instead of having for stative possession: she is having a car",
        ],
        "time_markers": ["now", "at the moment"],
    },

    "comparatives": {
        "description": "Comparative adjectives (-er/more) and adverbs for comparing two things; double comparatives (the more…the more); as…as",
        "key_structures": "adj-er + than; more + adj + than; less + adj + than; as + adj/adv + as; the more…the more",
        "example_correct": "This exercise is more difficult than the previous one.",
        "example_error": "This exercise is more difficult that the previous one.",
        "common_student_errors": [
            "Using that instead of than after comparative",
            "Double comparative: more better, more faster",
            "Using most instead of more for two items",
            "Wrong irregular forms: more good → better, more bad → worse",
        ],
        "time_markers": [],
    },

    "modals_obligation": {
        "description": "Must/have to for strong obligation; should/ought to for advice and weaker obligation; mustn't (prohibition) vs don't have to (no obligation)",
        "key_structures": "must/have to + V; should/ought to + V; mustn't + V; don't have to + V",
        "example_correct": "You don't have to come if you're busy.",
        "example_error": "You mustn't come if you're busy.",
        "common_student_errors": [
            "Confusing mustn't (forbidden) vs don't have to (not necessary)",
            "Using must for past: I musted → I had to",
            "Using should with have to meaning: you should wear a seatbelt (ok) vs you have to (legal obligation)",
            "Adding to after must: must to go",
        ],
        "time_markers": [],
    },

    "prepositions_other": {
        "description": "Logical, instrumental, and causal prepositions: by (means/agent), with (instrument/accompaniment), for (purpose/duration), about (subject), against, despite, because of, due to",
        "key_structures": "travel by + transport; pay by + method; write with + instrument; for + purpose; despite/because of + noun",
        "example_correct": "She succeeded despite all the difficulties.",
        "example_error": "She succeeded although all the difficulties.",
        "common_student_errors": [
            "Using although (conjunction) instead of despite (preposition)",
            "Confusing because (conjunction) vs because of (preposition)",
            "Using with instead of by for means of transport (go with bus → by bus)",
            "Wrong preposition in fixed phrases: interested at → interested in",
        ],
        "time_markers": [],
    },

    "quantifiers_advanced": {
        "description": "Advanced quantifiers with precise semantic differences: a little vs little, a few vs few; neither/either/each with singular nouns; hardly any, the majority of",
        "key_structures": "a little (some, positive) vs little (almost none) + uncountable; a few vs few + countable; each/either/neither + singular noun",
        "example_correct": "There is little hope of finding a solution today.",
        "example_error": "There is a little hope of finding a solution today.",
        "common_student_errors": [
            "Confusing a little (positive) vs little (negative/pessimistic)",
            "Using neither/either with plural verb: neither of them are → is",
            "Using each with plural verb: each student have → has",
            "Confusing hardly any (almost none) vs not any",
        ],
        "time_markers": [],
    },

    "time_clauses": {
        "description": "Subordinate time clauses introduced by when, before, after, while, until, as soon as, by the time; present simple/perfect in future time clauses",
        "key_structures": "When/Before/After/While/Until/As soon as + S + present simple, S + will + V",
        "example_correct": "I'll call you as soon as I arrive.",
        "example_error": "I'll call you as soon as I will arrive.",
        "common_student_errors": [
            "Using will in time clause: when I will finish → when I finish",
            "Confusing while (simultaneous) vs when (point in time)",
            "Using past tense in future time clause: when I arrived → when I arrive",
            "Confusing until (up to a point) vs when (at the point)",
        ],
        "time_markers": ["when", "before", "after", "while", "until", "as soon as", "by the time"],
    },

    "emphatic_do": {
        "description": "Emphatic do/does/did to add stress or contrast to affirmative statements, often in response to doubt or denial",
        "key_structures": "S + DO/DOES/DID + base V (emphatic); auxiliary carried forward: He thinks I don't care, but I DO.",
        "example_correct": "I do understand your point, but I still disagree.",
        "example_error": "I understand your point, but I still disagree. (missing emphasis)",
        "common_student_errors": [
            "Omitting emphatic do when context requires it",
            "Using emphatic do with be/have auxiliary (I do am tired → I AM tired)",
            "Using emphatic do with -ing: I do working → I do work",
            "Adding emphatic do in already-affirmative sentences without contrast meaning",
        ],
        "time_markers": [],
    },

    "past_continuous": {
        "description": "Past continuous for actions in progress at a past moment, background scenes, and interrupted actions (was/were doing + when + past simple)",
        "key_structures": "S + was/were + V-ing; was/were + V-ing + when + V2",
        "example_correct": "She was reading a book when the phone rang.",
        "example_error": "She read a book when the phone rang.",
        "common_student_errors": [
            "Using past simple for ongoing background action",
            "Reversing which verb takes continuous vs simple after when",
            "Using was/were + base form: was read instead of was reading",
            "Using past continuous for completed sequences: I was cooking and eating (→ cooked and ate)",
        ],
        "time_markers": ["when", "while", "at that moment", "at 8 o'clock last night", "all morning"],
    },

    "present_perfect_continuous": {
        "description": "Present perfect continuous for ongoing or recently-stopped actions with visible present results, emphasising duration and continuity with for/since",
        "key_structures": "S + have/has been + V-ing; How long have/has + S + been + V-ing?",
        "example_correct": "They have been waiting for over an hour.",
        "example_error": "They are waiting for over an hour.",
        "common_student_errors": [
            "Using present continuous instead of present perfect continuous with for/since",
            "Using present perfect simple where continuous is more natural for duration",
            "Omitting been: have waiting → have been waiting",
            "Using stative verbs in continuous form: have been knowing",
        ],
        "time_markers": ["for", "since", "all day", "lately", "recently", "how long"],
    },

    "word_formation_nouns_verbs": {
        "description": "Deriving nouns from verbs and adjectives with suffixes (-tion/-sion, -ment, -ness, -ity, -er/-or/-ist) and verbs from nouns/adjectives (-ize/-ise, -en, -ify)",
        "key_structures": "decide → decision; improve → improvement; happy → happiness; able → ability; teach → teacher",
        "example_correct": "The government's decision to raise taxes surprised everyone.",
        "example_error": "The government's decide to raise taxes surprised everyone.",
        "common_student_errors": [
            "Using verb instead of noun form in subject/object position",
            "Wrong suffix selection: improvement vs improveness",
            "Spelling errors: excitment → excitement; busines → business",
            "Using agent noun incorrectly: an economy → an economist",
        ],
        "time_markers": [],
    },

    "coordination_correlative": {
        "description": "Correlative conjunctions: both…and, either…or, neither…nor for connecting parallel structures (nouns, adjectives, verbs, clauses)",
        "key_structures": "both A and B; either A or B; neither A nor B; not only A but also B",
        "example_correct": "Neither the manager nor the employees were informed in advance.",
        "example_error": "Neither the manager or the employees were informed in advance.",
        "common_student_errors": [
            "Using or instead of nor in neither…nor",
            "Subject-verb agreement with neither…nor (the closer subject rules)",
            "Using both with or: both A or B → both A and B",
            "Not only A but B (missing also): not only fast but also accurate",
        ],
        "time_markers": [],
    },

    "future_forms_contrast": {
        "description": "Contrast between will (prediction, spontaneous decision), going to (plan/intention, evidence-based prediction), present continuous (fixed arrangement), and present simple (scheduled timetable)",
        "key_structures": "will vs going to vs present continuous vs present simple for future meaning",
        "example_correct": "The train leaves at 8:15 tomorrow morning.",
        "example_error": "The train will leave at 8:15 tomorrow morning.",
        "common_student_errors": [
            "Using will for pre-arranged personal plans (→ going to or present continuous)",
            "Using will for timetabled events (→ present simple)",
            "Using present continuous for predictions without evidence (→ will or going to)",
            "Treating all four forms as interchangeable",
        ],
        "time_markers": ["tomorrow", "tonight", "next Friday", "at 3pm"],
    },

    "phrasal_verbs": {
        "description": "Common two- and three-part phrasal verbs with intransitive and transitive uses, separable vs inseparable, and particle placement with pronouns",
        "key_structures": "turn off/on, give up, look after, find out, carry out; separable: turn it off, give it up; inseparable: look after it",
        "example_correct": "Can you look after my dog while I'm away?",
        "example_error": "Can you look my dog after while I'm away?",
        "common_student_errors": [
            "Separating inseparable phrasal verbs: look after it → look it after",
            "Not separating separable ones with pronouns: turn off it → turn it off",
            "Wrong particle: put up with (tolerate) vs put with",
            "Literal interpretation instead of idiomatic meaning",
        ],
        "time_markers": [],
    },

    "complement_clauses": {
        "description": "Noun/complement clauses introduced by that, whether, if, wh-words as objects of verbs like know, think, believe, tell, say, wonder, find out",
        "key_structures": "know/think/believe + that + clause; wonder + whether/if + clause; find out + wh- + clause",
        "example_correct": "Do you know whether the library is open on Sundays?",
        "example_error": "Do you know whether is the library open on Sundays?",
        "common_student_errors": [
            "Inverting subject-verb in embedded question (know where does he live → where he lives)",
            "Omitting that: I think he coming → I think that he is coming",
            "Confusing if (yes/no) vs whether (more formal, two alternatives)",
            "Using do/does/did in embedded questions",
        ],
        "time_markers": [],
    },

    "pronouns_reflexive": {
        "description": "Reflexive pronouns (myself, yourself, himself, herself, itself, ourselves, yourselves, themselves) for reflexive actions, emphasis, and without help",
        "key_structures": "S + V + reflexive (reflexive action); S + reflexive + V (emphatic); by + reflexive (alone/without help)",
        "example_correct": "She taught herself to play the guitar.",
        "example_error": "She taught her to play the guitar.",
        "common_student_errors": [
            "Using object pronoun instead of reflexive: hurt him (→ himself)",
            "Using reflexive where object pronoun is correct: she helped herself → she helped her (someone else)",
            "Myself vs I as subject: Myself did it → I did it",
            "Themselves vs each other: they hurt themselves vs each other",
        ],
        "time_markers": [],
    },

    "second_conditional": {
        "description": "Second conditional for hypothetical or unlikely present/future situations: if + past simple in condition, would + base verb in result",
        "key_structures": "If + S + V-ed (past simple), S + would + V; I/he/she/it + were (subjunctive)",
        "example_correct": "If I had more time, I would learn another language.",
        "example_error": "If I would have more time, I would learn another language.",
        "common_student_errors": [
            "Using would in the if-clause: if I would have",
            "Using was instead of were in formal second conditional: if I was rich (acceptable in informal, but was/were contrast is tested)",
            "Confusing second conditional (hypothetical) with first (realistic)",
            "Using could/might instead of would (not wrong, but often tested)",
        ],
        "time_markers": ["if", "would", "could", "imagine"],
    },

    "verb_complementation_advanced": {
        "description": "Verbs whose meaning changes depending on whether followed by to-infinitive or -ing: stop, remember, forget, try, regret, mean, go on",
        "key_structures": "stop + -ing (cease) vs stop + to-inf (in order to); remember + -ing (past) vs remember + to-inf (duty); try + -ing (experiment) vs try + to-inf (attempt)",
        "example_correct": "I remember posting the letter last Friday.",
        "example_error": "I remember to post the letter last Friday.",
        "common_student_errors": [
            "Using remember + to-inf for a memory of a past action",
            "Using stop + to-inf when meaning ceasing",
            "Treating all verbs as taking only one form",
            "Confusing forget + -ing (a past event forgotten) vs forget + to-inf (a duty forgotten)",
        ],
        "time_markers": [],
    },

    "used_to_would_past": {
        "description": "Used to and would for past habits and repeated actions no longer true; used to (also for past states); be/get used to + -ing for familiarity",
        "key_structures": "used to + base V (past habit/state); would + base V (past habit only); be/get used to + -ing",
        "example_correct": "When I was a child, I used to walk to school every day.",
        "example_error": "When I was a child, I was used to walk to school every day.",
        "common_student_errors": [
            "Using was used to + base verb instead of used to (confusing with be used to)",
            "Using would for past states: I would know him well → used to know",
            "Adding to: I used to would go",
            "Using past simple where used to clarifies that it no longer happens",
        ],
        "time_markers": ["when I was young", "as a child", "in those days", "back then"],
    },

    "passive_present_past": {
        "description": "Passive voice with present simple (is/are + past participle) and past simple (was/were + past participle); agent with by; reasons for passivisation",
        "key_structures": "S + is/are + V3 (present passive); S + was/were + V3 (past passive); by + agent (optional)",
        "example_correct": "The report was written by the team last month.",
        "example_error": "The report was wrote by the team last month.",
        "common_student_errors": [
            "Using past simple instead of past participle: was write, was went",
            "Wrong be form: the report were written (singular subject)",
            "Omitting by when agent is needed for clarity",
            "Confusion of active/passive voice in complex sentences",
        ],
        "time_markers": ["last week", "yesterday", "every day", "recently"],
    },

    "infinitive_constructions": {
        "description": "To-infinitive after adjectives (easy to do, happy to help), after question words (how to, what to), after too/enough, and split infinitives",
        "key_structures": "adj + enough + to-inf; too + adj + to-inf; wh- word + to-inf; be + adj + to-inf",
        "example_correct": "The bag is too heavy for me to carry.",
        "example_error": "The bag is too heavy for me to carrying.",
        "common_student_errors": [
            "Using -ing instead of to-inf after too/enough",
            "Omitting for + object before infinitive when subjects differ",
            "Confusing too (excess → impossible) vs enough (sufficient)",
            "Using that-clause instead of infinitive: I didn't know what I should do → what to do",
        ],
        "time_markers": [],
    },

    "conditionals_zero_first": {
        "description": "Zero conditional for universal truths (if + present, present); first conditional for realistic future possibilities (if + present simple, will + base verb)",
        "key_structures": "If + present simple, present simple (zero); If + present simple, will + V (first)",
        "example_correct": "If you heat ice, it melts.",
        "example_error": "If you will heat ice, it melts.",
        "common_student_errors": [
            "Using will in the if-clause of first conditional",
            "Using present simple result clause for first conditional (→ will + V)",
            "Confusing zero (scientific fact) vs first (specific realistic case)",
            "Using when instead of if for hypothetical (though when implies certainty)",
        ],
        "time_markers": ["if", "when", "always", "every time", "unless"],
    },

    "modals_likelihood": {
        "description": "Modal verbs for degrees of likelihood and inference: must (certain positive), can't (certain negative), could/might/may (possible), should (expected)",
        "key_structures": "must + V (deduction); can't + V (negative deduction); might/may/could + V (possibility); should + V (expectation)",
        "example_correct": "She's not answering — she must be asleep.",
        "example_error": "She's not answering — she must be sleeping. (could be correct, but testing deduction not aspect)",
        "common_student_errors": [
            "Using must for obligation when deduction is meant",
            "Confusing can't (deduction) vs don't have to (obligation)",
            "Using maybe/perhaps as modal (not wrong but tests modal verb specifically)",
            "Using may instead of might for less probable deductions",
        ],
        "time_markers": [],
    },

    "connectors_result_cause": {
        "description": "Connectors expressing result (so, therefore, as a result, consequently) and cause (because, since, as, due to, owing to) at sentence and discourse level",
        "key_structures": "…, so + clause; therefore/as a result/consequently + clause; because/since/as + clause; due to/owing to/because of + noun phrase",
        "example_correct": "The concert was cancelled due to the heavy rain.",
        "example_error": "The concert was cancelled because of the heavy rain was too strong.",
        "common_student_errors": [
            "Using due to/because of before a clause (they need a noun phrase)",
            "Using therefore + clause without proper punctuation/sentence boundary",
            "Confusing since (cause, formal) vs since (time) by context",
            "Double-marking cause: because due to",
        ],
        "time_markers": [],
    },

    "relative_clauses_defining": {
        "description": "Defining relative clauses with who (people), which (things), that (people/things), where (places), whose (possession), and when; omission of contact clauses",
        "key_structures": "noun + who/which/that/where/whose + clause; omit pronoun when it is the object",
        "example_correct": "The woman who called you left a message.",
        "example_error": "The woman which called you left a message.",
        "common_student_errors": [
            "Using which for people instead of who",
            "Keeping the pronoun when the relative pronoun is the object: the book that I read it",
            "Using what instead of that/which: the thing what happened",
            "Confusing defining (no commas) vs non-defining (commas)",
        ],
        "time_markers": [],
    },

    "agreement_substitution": {
        "description": "Short responses expressing agreement/disagreement using so/neither + inverted auxiliary, and substitution with do/be/have to avoid repetition",
        "key_structures": "So + aux + S (positive agreement); Neither/Nor + aux + S (negative agreement); …and so do I / …and neither can she",
        "example_correct": "'I love jazz.' 'So do I.'",
        "example_error": "'I love jazz.' 'So I do.'",
        "common_student_errors": [
            "Using subject-auxiliary order: So I do instead of So do I",
            "Choosing wrong auxiliary tense: 'I went' — 'So do I' → 'So did I'",
            "Confusing so (agree with positive) vs neither (agree with negative)",
            "Using too/either as short response without the auxiliary structure",
        ],
        "time_markers": [],
    },

    "reported_speech_questions": {
        "description": "Reporting yes/no questions with if/whether and wh-questions; tense back-shift; no auxiliary inversion in reported questions",
        "key_structures": "S + asked + if/whether + S + V (reported yes/no); asked + wh- + S + V (wh-question)",
        "example_correct": "She asked me where I had been the night before.",
        "example_error": "She asked me where had I been the night before.",
        "common_student_errors": [
            "Keeping direct question word order: asked where was I",
            "Using do/does/did in reported questions: asked where did I go → where I had gone",
            "Not applying tense back-shift",
            "Using that instead of if/whether for yes/no questions",
        ],
        "time_markers": ["the day before", "the previous day", "then", "there"],
    },

    "passive_continuous_perfect": {
        "description": "Extended passive forms: present continuous passive (is being done), past continuous passive (was being done), present perfect passive (has been done), past perfect passive (had been done)",
        "key_structures": "is/are being + V3; was/were being + V3; has/have been + V3; had been + V3",
        "example_correct": "The bridge has been closed for repairs since Monday.",
        "example_error": "The bridge has been closing for repairs since Monday.",
        "common_student_errors": [
            "Using active continuous instead of passive: is closing → is being closed",
            "Omitting been in perfect passives: has repaired → has been repaired",
            "Confusing has been done (present perfect passive) vs is done (present simple passive)",
            "Using wrong participle: has been wrote → has been written",
        ],
        "time_markers": ["since", "for", "currently", "at the time"],
    },

    "past_perfect": {
        "description": "Past perfect (had + past participle) for events completed before another past event; often used with by the time, when, before, after, already",
        "key_structures": "S + had + V3 (+ before/when/by the time + past simple); S + hadn't + V3",
        "example_correct": "When I arrived at the station, the train had already left.",
        "example_error": "When I arrived at the station, the train already left.",
        "common_student_errors": [
            "Using past simple instead of past perfect for the earlier event",
            "Using past perfect for all past actions without sequence justification",
            "Confusing had + V3 with was + V3 (passive): had written vs was written",
            "Omitting already/yet/just which signal past perfect context",
        ],
        "time_markers": ["by the time", "when", "before", "after", "already", "just", "never"],
    },

    "reported_speech_statements": {
        "description": "Reporting statements with say/tell; tense back-shift (present → past, will → would, can → could); pronoun and time expression changes",
        "key_structures": "said (that) + back-shifted clause; told + object + (that) + back-shifted clause; time expression shifts: today → that day, tomorrow → the next day",
        "example_correct": "She said she would call me the next day.",
        "example_error": "She said she will call me tomorrow.",
        "common_student_errors": [
            "No tense back-shift in reported clause",
            "Using say instead of tell before an object: said me → told me",
            "Keeping direct time expressions: tomorrow → the next day",
            "Keeping direct pronouns: she said 'I am' → she said she was",
        ],
        "time_markers": ["the next day", "the day before", "that day", "then", "there"],
    },

    "reduced_relatives_passive": {
        "description": "Reduced relative clauses using a past participle instead of a full relative clause: the letter written by… (= the letter that was written by…)",
        "key_structures": "noun + past participle + phrase; noun + past participle = reduced passive relative",
        "example_correct": "The documents submitted last week are now under review.",
        "example_error": "The documents that submitted last week are now under review.",
        "common_student_errors": [
            "Omitting that was/were in full form when not reducing: the documents submitted (ok) vs the documents that submitted (wrong)",
            "Using present participle instead of past participle for passive meaning",
            "Adding that before the participle when reducing",
            "Confusing reduced active (the man running) vs reduced passive (the man arrested)",
        ],
        "time_markers": [],
    },

    "intentions_plans": {
        "description": "Expressing future intentions with intend to, plan to, mean to, be thinking of, be about to, be due to",
        "key_structures": "intend/plan/mean + to-inf; be thinking of/about + -ing; be about to + base V; be due to + base V",
        "example_correct": "We are planning to expand the business next year.",
        "example_error": "We are planning expanding the business next year.",
        "common_student_errors": [
            "Using -ing instead of to-inf after intend/plan/mean",
            "Confusing be about to (imminent) vs be going to (general intention)",
            "Using plan + -ing without of: planning going → planning to go or thinking of going",
            "Omitting to: intend do → intend to do",
        ],
        "time_markers": ["next year", "soon", "at some point", "by the end of the year"],
    },

    "connectors_concession_contrast": {
        "description": "Connectors expressing concession and contrast: although, though, even though, despite, in spite of, however, nevertheless, on the other hand, whereas",
        "key_structures": "Although/Even though + clause, clause; Despite/In spite of + noun/-ing, clause; However/Nevertheless + clause",
        "example_correct": "Although she was tired, she continued working.",
        "example_error": "Despite she was tired, she continued working.",
        "common_student_errors": [
            "Using despite/in spite of before a full clause (need -ing or noun)",
            "Using although/though before a noun phrase (need despite)",
            "Using however without proper punctuation (comma or semicolon before)",
            "Double contrast: although…but (only one needed)",
        ],
        "time_markers": [],
    },

    "modals_wishes_regrets": {
        "description": "Expressing wishes and regrets about present/past with I wish + past simple (present wish), I wish + past perfect (past regret), If only, should have, could have",
        "key_structures": "I wish + past simple (present wish); I wish + past perfect (past regret); should have/could have/would have + V3",
        "example_correct": "I wish I had studied harder for the exam.",
        "example_error": "I wish I would have studied harder for the exam.",
        "common_student_errors": [
            "Using would in wish clause: I wish I would know (→ knew)",
            "Confusing wish + past simple (unreality now) vs wish + past perfect (regret about past)",
            "Using should of instead of should have",
            "Confusing if only (stronger emotion) vs I wish",
        ],
        "time_markers": [],
    },

    "passive_get_causative": {
        "description": "Informal passive with get (get + V3) and causative have/get (have/get + object + V3) for arranging someone else to do something",
        "key_structures": "get + V3 (informal passive); have/get + object + V3 (causative); get/be + adj (result state)",
        "example_correct": "I need to get my car serviced before the long trip.",
        "example_error": "I need to get my car to service before the long trip.",
        "common_student_errors": [
            "Adding to-inf instead of bare V3 in causative: get it to repaired",
            "Confusing have sth done (arrange) vs do sth yourself",
            "Using get passively where formal passive (be + V3) is more appropriate in writing",
            "Confusing get + adj (become) vs get + V3 (passive/causative)",
        ],
        "time_markers": [],
    },

    "cleft_fronting": {
        "description": "Cleft sentences for focus and emphasis: it is/was…that/who; what-clefts (What I need is…); fronting of adverbials and objects for contrast or emphasis; ellipsis",
        "key_structures": "It is/was + focus + that/who + clause; What + S + V + is/was + focus; Fronting: Never have I…; Ellipsis: A: Did you go? B: Yes, I did.",
        "example_correct": "It was Maria who found the solution, not John.",
        "example_error": "It was Maria that found the solution, not John. (acceptable, but testing who for people)",
        "common_student_errors": [
            "Using which instead of who in it-cleft for people",
            "Inverted subject-verb after negative fronting: Never I have seen (→ Never have I seen)",
            "What-cleft without correct be form: What I need are → is (if singular complement)",
            "Omitting that/who in cleft: It was Maria found it",
        ],
        "time_markers": [],
    },

    "third_conditional": {
        "description": "Third conditional for hypothetical situations in the past that did not happen: if + past perfect in condition, would have + past participle in result",
        "key_structures": "If + S + had + V3, S + would have + V3; mixed conditional: If + past perfect, S + would + V (now)",
        "example_correct": "If she had left earlier, she would have caught the train.",
        "example_error": "If she would have left earlier, she would have caught the train.",
        "common_student_errors": [
            "Using would have in the if-clause",
            "Using simple past instead of past perfect in if-clause",
            "Using would of instead of would have",
            "Confusing second vs third conditional (unreal now vs unreal past)",
        ],
        "time_markers": [],
    },
}


def get_description(skill_id: str) -> SkillDescription | None:
    return SKILL_DESCRIPTIONS.get(skill_id)
