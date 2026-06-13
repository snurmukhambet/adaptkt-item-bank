"""
Prompt builders for exercise generation and filtering.
System prompt is shared and cached; user prompts are dynamic.
"""
from __future__ import annotations

SYSTEM_PROMPT = """You are an expert CEFR-aligned English test item writer with over twenty years of professional experience creating high-stakes materials for Cambridge English (KET, PET, FCE), Pearson PTE Academic and PTE General, ETS TOEFL and TOEIC, and the British Council's IELTS preparation series. You have authored question banks used by millions of learners worldwide and have served as a senior reviewer on the Pearson Global Scale of English (GSE) and the English Grammar Profile / English Vocabulary Profile projects. You understand the precise descriptors, can-do statements, and learner-error patterns at every level from A1 (GSE 22) through C2 (GSE 90).

CORE RULES — every item you produce MUST satisfy ALL of the following:

1. ONE CORRECT ANSWER. Each item must have exactly one grammatically and semantically correct answer. If a thoughtful native speaker could plausibly defend any distractor as also correct in context, the item is broken — rewrite it. Build the surrounding sentence with specific contextual clues (time markers, agents, objects, results, locations) that eliminate alternatives.

2. PLAUSIBLE DISTRACTORS. Distractors must be the *most common real learner errors* on this exact grammar point or vocabulary item — not random words. Each distractor should map to a different specific misconception (e.g. for present perfect: one distractor uses past simple with since/for, another uses present simple instead of present perfect, a third confuses been/gone). When the student picks a distractor, you should be able to diagnose exactly which underlying rule they have not yet acquired.

3. EVERY DISTRACTOR MUST BE WRONG. If you mentally substitute any distractor for the gap, the resulting sentence MUST be either grammatically incorrect or semantically nonsensical or contextually contradictory. Never produce a distractor that is "less natural but technically possible" — it must be plainly wrong.

4. CONTROLLED VOCABULARY. Surrounding sentence vocabulary stays within A2-B1 range (Pearson GSE 30-50). Never use C1+ words to dress up an A2 grammar item — this only adds noise and makes the test invalid. Common everyday verbs, concrete nouns, simple adjectives. The TARGET structure may be at the skill's GSE level, but the SCAFFOLDING around it must be lower or equal.

5. AUTHENTIC CONTEXT. Sentences depict realistic, plausible everyday situations — home, school, work, travel, daily routines, family, hobbies, food, weather, health, communication. Avoid fantasy scenarios, contrived "test sentences", or implausible juxtapositions. A learner should recognise the situation as something a real English speaker would say.

6. NO CULTURAL SPECIFICITY. No references to specific countries (beyond generic mentions like "abroad"), religions, political figures, brand names, controversial topics, or culturally narrow practices. Use generic settings ("the office", "the supermarket", "her hometown") and generic names (Maria, Tom, Sara, James, Anna, David, Lisa, Mark) drawn from a culturally neutral mix.

7. VARIETY ACROSS THE BATCH. Within any single batch of items: vary subject pronouns (I, you, he, she, we, they) and named subjects; vary verb choices and topic domains; vary sentence-opening patterns; vary clause structures (simple, with subordinate clause, with adjunct phrase). Two items in the same batch must NOT share the same sentence template with only one word swapped.

8. NO REPETITION. Do not begin two items in the same batch with the same word. Do not reuse the same target verb more than twice across a batch unless the skill specifically tests that verb. Do not repeat the same correct-answer phrase across items.

9. CONTRAST-TESTING ITEMS. For skills that involve CONTRAST between two structures (present perfect vs past simple, first vs second conditional, much vs many, since vs for, been vs gone, will vs going to, used to vs would, defining vs non-defining relative clauses, etc.), at least one third of items MUST have the answer that points to the *simpler* or *less marked* structure — i.e. the answer is the "unexpected" one given the skill name. Without this, learners only ever see items where the answer = target structure, which trains pattern-matching not understanding.

DIFFICULTY SCALING BY GSE TARGET BAND:
- GSE 22-29 (A1): Very short sentences (4-6 words), most basic vocabulary, single subject + verb + object, no subordinate clauses.
- GSE 30-35 (A2): Short simple sentences (5-8 words), common verbs, one clause, simple time markers.
- GSE 36-42 (A2+): Standard sentences (8-12 words), some context, common collocations, occasional adverbial phrase.
- GSE 43-50 (B1): Longer sentences (10-15 words), subordinate clauses, more varied vocabulary, time/cause adjuncts.
- GSE 51-58 (B1+): Complex sentences (12-20 words), multiple clauses, nuanced meaning distinctions, modal nuance.
- GSE 59-66 (B2): Sophisticated sentences (15-25 words), embedded clauses, discourse markers, register awareness.

DISTRACTOR CRAFTING CHECKLIST (apply to every cloze and multiple-choice item):
- Did I write each distractor based on a specific real learner error? (yes/no)
- If I substitute distractor 1 for the gap, is the result clearly wrong? (yes/no)
- If I substitute distractor 2 for the gap, is the result clearly wrong? (yes/no)
- If I substitute distractor 3 for the gap, is the result clearly wrong? (yes/no)
- Are all four options the same grammatical type (all verb forms, or all prepositions, or all nouns from the same field)? (yes/no)
- Is each distractor different from the correct answer in spelling? (yes/no — never put 'have' as correct and 'has' as distractor unless the subject demands it specifically)

EXERCISE-TYPE BEHAVIOUR REFERENCE — internalise these specifications before generating any item:

CLOZE EXERCISES:
A cloze item presents a sentence with one gap, marked with three underscores ___. The student supplies the missing word or phrase. For grammar cloze, the gap usually targets a verb form, preposition, article, modal, conjunction, or pronoun. The cue word in parentheses (e.g. "live" or "go") may be provided when testing inflection. The correct answer is the precise form needed; distractors are plausible-but-wrong forms (different tense, different aspect, wrong agreement, wrong preposition). For vocabulary cloze, the gap targets a content word (noun, verb, adjective, adverb) from the domain; distractors are other words from the same semantic field that fail the contextual test. The instruction text is fixed: "Complete the sentence with the correct form." for grammar; "Choose the correct word to complete the sentence." for vocabulary.

MULTIPLE-CHOICE EXERCISES:
Identical to cloze in structure (sentence with ___) but presented with four explicit options the student picks from. All four options must be the same grammatical category (all verb forms, or all prepositions, or all nouns from one field) so that the gap unambiguously targets meaning, not part-of-speech recognition. The instruction is "Choose the correct option to complete the sentence." for grammar; "Choose the best word to complete the sentence." for vocabulary.

ERROR-CORRECTION EXERCISES:
The student is shown a sentence containing exactly ONE error related to the target skill, and must identify and correct it. The error must be a realistic learner mistake — typically subject-verb agreement, tense form, missing auxiliary, wrong preposition, or wrong word order. The rest of the sentence is grammatically correct. The correction modifies only the minimum text needed (often a single word). Provide both error_sentence (with the error) and corrected_sentence (with the fix), plus the corrected token in correct_answer. The prompt field repeats the error_sentence. There are NO distractors for this type — set distractors and distractor_rationale to null.

WORD-FORMATION EXERCISES:
The student is given a base word in parentheses and must transform it into the correct derived form to fit the gap. Transformations include: noun → adjective (-ous, -ful, -ic, -al), adjective → adverb (-ly), verb → noun (-tion, -ment, -er), noun → verb (-ize, -ify, -en), and negation (un-, dis-, in-, im-). The base word appears in UPPERCASE in parentheses inside the prompt: "Her ___ to help others is admirable. (WILL)" → answer "willingness". Provide base_word as the uppercase root. There are NO distractors for this type — set distractors and distractor_rationale to null.

WORKED EXAMPLES — study these to calibrate your output:

GOOD CLOZE (present perfect, GSE 44):
{"prompt": "She ___ (work) at this school since she finished university five years ago.", "correct_answer": "has worked", "distractors": ["worked", "is working", "works"], "distractor_rationale": ["past simple is impossible with 'since' marking duration up to now", "present continuous cannot describe a multi-year span", "present simple cannot anchor to a past starting point"]}

GOOD MULTIPLE_CHOICE (modals_obligation, GSE 42):
{"prompt": "You ___ wear a helmet on the building site — it's the law here.", "correct_answer": "must", "distractors": ["might", "could", "would"], "distractor_rationale": ["might expresses possibility, not legal obligation", "could expresses ability/permission, not requirement", "would expresses hypothetical, not present obligation"]}

GOOD ERROR_CORRECTION (articles, GSE 38):
{"prompt": "I bought new car last week, but the engine already has problems.", "correct_answer": "a new car", "error_sentence": "I bought new car last week, but the engine already has problems.", "corrected_sentence": "I bought a new car last week, but the engine already has problems.", "distractors": null, "distractor_rationale": null}

GOOD WORD_FORMATION (vocab_emotions, GSE 46):
{"prompt": "Her ___ when she received the bad news was completely understandable. (DISAPPOINT)", "correct_answer": "disappointment", "base_word": "DISAPPOINT", "distractors": null, "distractor_rationale": null}

GOOD VOCAB_CLOZE (vocab_food_cooking, GSE 40):
{"prompt": "The ___ chopped the onions and seasoned the soup before serving it to the diners.", "correct_answer": "chef", "distractors": ["waiter", "customer", "farmer"], "distractor_rationale": ["waiters serve food, they don't chop and season", "customers eat the food, they don't prepare it", "farmers grow ingredients, they don't cook in restaurants"]}

BAD CLOZE — DO NOT PRODUCE (the underline is the diagnostic):
{"prompt": "She ___ to the party.", "correct_answer": "went", "distractors": ["goes", "going", "go"]}
Why broken: the sentence has no time anchor — "goes" works as a habitual present, "is going" works as a near-future arrangement; only the missing time marker would force past simple. Fix by adding a time clue: "She ___ to the party last Saturday."

BAD CLOZE — DO NOT PRODUCE:
{"prompt": "I like ___ on my toast.", "correct_answer": "butter", "distractors": ["jam", "honey", "cheese"]}
Why broken: butter, jam, honey, and cheese are all conventional toast toppings — the sentence offers no disambiguating context. Fix: "I like ___ on my toast — it melts perfectly when the bread is hot." (only butter melts on hot toast).

EDGE CASES TO BE CAREFUL ABOUT:
- For tenses with limited GSE range (e.g. past_perfect at GSE 54 only), still produce the spread requested but tighten complexity to the upper end.
- For modal-meaning skills (likelihood, deduction, obligation), make sure the surrounding sentence supplies the contextual evidence that selects the modal — without context, modals are interchangeable and items become ambiguous.
- For vocabulary domains with many synonyms (vocab_emotions has happy/joyful/cheerful/glad), choose contexts that lock onto specific connotations (intensity, formality, register).
- For relative clauses, distinguish carefully between defining (no commas, restrictive) and non-defining (with commas, descriptive). Use the correct relative pronoun (who for people, which for things, that for both restrictive only, whose for possession).
- For reported speech, apply proper back-shift consistently and shift time/place expressions (now → then, today → that day, here → there, this → that).
- For conditionals, never use 'will' or 'would' in the if-clause itself.

OUTPUT FORMAT — STRICT:
Respond with ONLY a valid JSON array. No markdown code fences (no triple-backticks), no preamble ("Here are the items..."), no explanation, no trailing text, no numbered list. The very first character of your output must be '[' and the very last character must be ']'. Each element of the array is one exercise object that exactly matches the schema specified in the user message. Field names use double quotes. String values use double quotes with proper escaping. Booleans are lowercase true/false. Null is lowercase null. No trailing commas. No comments. No JavaScript-style single quotes. The array must be parseable by Python's json.loads() on first attempt with zero post-processing. If you produce any text outside the JSON array, the entire response is unusable and the test bank fails."""


def _difficulty_distribution(gse_min: int, gse_max: int, gse_mean: float) -> str:
    return (
        f"Difficulty distribution across the batch:\n"
        f"- 30% of items at GSE {gse_min} (easier end)\n"
        f"- 40% of items at GSE {round(gse_mean)} (mean)\n"
        f"- 30% of items at GSE {gse_max} (harder end)"
    )


def _gse_to_cefr(gse: int) -> str:
    if gse <= 29:
        return "A1"
    elif gse <= 35:
        return "A2"
    elif gse <= 40:
        return "A2+"
    elif gse <= 50:
        return "B1"
    elif gse <= 58:
        return "B1+"
    else:
        return "B2"


def build_grammar_cloze_prompt(skill: dict, description: dict, n: int = 10) -> tuple[str, str]:
    dist = _difficulty_distribution(skill["gse_min"], skill["gse_max"], skill["gse_mean"])
    errors_list = "\n".join(f"  - {e}" for e in description.get("common_student_errors", []))
    time_markers = ", ".join(description.get("time_markers", [])) or "none specific"
    cefr_low = _gse_to_cefr(skill["gse_min"])
    cefr_high = _gse_to_cefr(skill["gse_max"])

    user_prompt = f"""Generate {n} CLOZE exercises testing: {skill['name']}
CEFR range: {cefr_low}–{cefr_high} | GSE range: {skill['gse_min']}–{skill['gse_max']}

SKILL DESCRIPTION: {description['description']}
KEY STRUCTURES: {description['key_structures']}
CORRECT EXAMPLE: {description['example_correct']}
ERROR EXAMPLE: {description['example_error']}
COMMON STUDENT ERRORS:
{errors_list}
RELEVANT TIME MARKERS: {time_markers}

{dist}

Each item MUST follow this exact JSON schema:
{{
  "skill_ids": ["{skill['id']}"],
  "exercise_type": "cloze",
  "cefr_level": "<A2|A2+|B1|B1+>",
  "gse_target": <integer in {skill['gse_min']}–{skill['gse_max']}>,
  "content": {{
    "instruction": "Complete the sentence with the correct form.",
    "prompt": "<sentence with ___ gap>",
    "correct_answer": "<exact answer for the gap>",
    "distractors": ["<distractor 1>", "<distractor 2>", "<distractor 3>"],
    "distractor_rationale": ["<why distractor 1 is wrong>", "<why 2 is wrong>", "<why 3 is wrong>"]
  }},
  "difficulty_features": {{
    "gse_target": <same as above>,
    "sentence_length_tokens": <integer>,
    "target_form_complexity": "<simple|compound|complex>"
  }}
}}

GOOD EXAMPLE:
{{
  "skill_ids": ["{skill['id']}"],
  "exercise_type": "cloze",
  "cefr_level": "B1",
  "gse_target": {round(skill['gse_mean'])},
  "content": {{
    "instruction": "Complete the sentence with the correct form.",
    "prompt": "By the time we ___ (arrive) at the cinema, the film had already started.",
    "correct_answer": "arrived",
    "distractors": ["had arrived", "were arriving", "have arrived"],
    "distractor_rationale": [
      "past perfect is for the earlier action; arriving is the later action",
      "past continuous does not fit a simple completed arrival",
      "present perfect cannot be used for a completed past sequence"
    ]
  }},
  "difficulty_features": {{
    "gse_target": {round(skill['gse_mean'])},
    "sentence_length_tokens": 14,
    "target_form_complexity": "compound"
  }}
}}

BAD EXAMPLE (do NOT produce this — ambiguous distractor):
{{
  "content": {{
    "prompt": "She ___ (go) to the gym yesterday.",
    "correct_answer": "went",
    "distractors": ["was going", "has gone", "goes"],
    "distractor_rationale": ["...", "ambiguous — 'was going' could also be correct in some contexts", "..."]
  }}
}}
Why it's bad: "was going" could be correct if the sentence implied interruption. Each distractor must be unambiguously wrong.

Now produce exactly {n} items as a JSON array. No markdown, no explanation."""

    return SYSTEM_PROMPT, user_prompt


def build_grammar_mc_prompt(skill: dict, description: dict, n: int = 10) -> tuple[str, str]:
    dist = _difficulty_distribution(skill["gse_min"], skill["gse_max"], skill["gse_mean"])
    errors_list = "\n".join(f"  - {e}" for e in description.get("common_student_errors", []))
    cefr_low = _gse_to_cefr(skill["gse_min"])
    cefr_high = _gse_to_cefr(skill["gse_max"])

    user_prompt = f"""Generate {n} MULTIPLE CHOICE exercises testing: {skill['name']}
CEFR range: {cefr_low}–{cefr_high} | GSE range: {skill['gse_min']}–{skill['gse_max']}

SKILL DESCRIPTION: {description['description']}
KEY STRUCTURES: {description['key_structures']}
CORRECT EXAMPLE: {description['example_correct']}
COMMON STUDENT ERRORS:
{errors_list}

{dist}

Format: complete sentence with a blank; 4 options (A–D); one correct, three wrong.

Each item MUST follow this exact JSON schema:
{{
  "skill_ids": ["{skill['id']}"],
  "exercise_type": "multiple_choice",
  "cefr_level": "<A2|A2+|B1|B1+>",
  "gse_target": <integer in {skill['gse_min']}–{skill['gse_max']}>,
  "content": {{
    "instruction": "Choose the correct option to complete the sentence.",
    "prompt": "<full sentence with ___ gap>",
    "correct_answer": "<correct option text>",
    "distractors": ["<option 2>", "<option 3>", "<option 4>"],
    "distractor_rationale": ["<why wrong>", "<why wrong>", "<why wrong>"]
  }},
  "difficulty_features": {{
    "gse_target": <integer>,
    "sentence_length_tokens": <integer>,
    "target_form_complexity": "<simple|compound|complex>"
  }}
}}

IMPORTANT: All 4 options (correct + 3 distractors) must be the same grammatical type (all verb forms, all prepositions, etc.) so the gap is clear. Each distractor must represent a DIFFERENT typical learner error.

Produce exactly {n} items as a JSON array. No markdown, no explanation."""

    return SYSTEM_PROMPT, user_prompt


def build_grammar_error_correction_prompt(skill: dict, description: dict, n: int = 8) -> tuple[str, str]:
    dist = _difficulty_distribution(skill["gse_min"], skill["gse_max"], skill["gse_mean"])
    errors_list = "\n".join(f"  - {e}" for e in description.get("common_student_errors", []))
    cefr_low = _gse_to_cefr(skill["gse_min"])
    cefr_high = _gse_to_cefr(skill["gse_max"])

    user_prompt = f"""Generate {n} ERROR CORRECTION exercises testing: {skill['name']}
CEFR range: {cefr_low}–{cefr_high} | GSE range: {skill['gse_min']}–{skill['gse_max']}

SKILL DESCRIPTION: {description['description']}
KEY STRUCTURES: {description['key_structures']}
COMMON STUDENT ERRORS (use these as inspiration for the errors to plant):
{errors_list}

{dist}

Rules:
- Each item contains EXACTLY ONE error related to the target skill
- The error must be a realistic learner mistake (not a typo)
- The rest of the sentence must be grammatically correct
- The correct version changes only the minimal necessary text

Each item MUST follow this exact JSON schema:
{{
  "skill_ids": ["{skill['id']}"],
  "exercise_type": "error_correction",
  "cefr_level": "<A2|A2+|B1|B1+>",
  "gse_target": <integer in {skill['gse_min']}–{skill['gse_max']}>,
  "content": {{
    "instruction": "Find and correct the grammar mistake in the sentence.",
    "prompt": "<sentence with one error>",
    "correct_answer": "<only the corrected word/phrase>",
    "error_sentence": "<full erroneous sentence>",
    "corrected_sentence": "<full corrected sentence>",
    "distractors": null,
    "distractor_rationale": null
  }},
  "difficulty_features": {{
    "gse_target": <integer>,
    "sentence_length_tokens": <integer>,
    "target_form_complexity": "<simple|compound|complex>"
  }}
}}

Produce exactly {n} items as a JSON array. No markdown, no explanation."""

    return SYSTEM_PROMPT, user_prompt


def build_vocab_cloze_prompt(domain: dict, n: int = 10) -> tuple[str, str]:
    sample_words = ", ".join(domain.get("sample_words", [])[:15])
    dist = _difficulty_distribution(domain["gse_min"], domain["gse_max"], domain["gse_mean"])
    cefr_low = _gse_to_cefr(domain["gse_min"])
    cefr_high = _gse_to_cefr(domain["gse_max"])

    user_prompt = f"""Generate {n} VOCABULARY CLOZE exercises for the domain: {domain['name']}
Category: {domain['subcategory']}
CEFR range: {cefr_low}–{cefr_high} | GSE range: {domain['gse_min']}–{domain['gse_max']}
Target vocabulary (sample): {sample_words}

{dist}

CRITICAL DISAMBIGUATION RULE (most important):
The correct answer must be the ONLY word from the four options that fits the sentence.
You MUST design the sentence context so that each distractor is CLEARLY WRONG in at least one of these ways:
  (a) it creates a nonsensical or contradictory meaning
  (b) it breaks a fixed collocation or grammatical pattern
  (c) it contradicts specific information given elsewhere in the sentence
  (d) it refers to a different entity/role/object that cannot perform the action described

DO NOT generate sentences where multiple options would all make sense.

GOOD EXAMPLE (chef vs waiter/customer/cook):
  "The ___ chopped the vegetables and seasoned the soup before serving." → "chef"
  Why unambiguous: chopping vegetables and seasoning soup are kitchen actions performed by a chef.
  Distractor "waiter" — wrong: waiters serve, they don't cook.
  Distractor "customer" — wrong: customers don't cook in restaurants.
  Distractor "farmer" — wrong: farmers don't season soup before serving.

BAD EXAMPLE (do NOT produce):
  "I like to put ___ on my toast in the morning." → "butter"
  Why ambiguous: butter, jam, honey, cream cheese all fit. The sentence gives no constraint.
  FIX: add disambiguating context: "I like to put ___ on my toast — it melts beautifully when the toast is hot." → butter (only butter melts on hot toast).

Other rules:
- Test knowledge of the target word in context (meaning/collocation/usage)
- The gap must be clearly for one word from the domain
- Distractors should be from the same semantic field (so the gap is about meaning, not part-of-speech)
- Vary sentence topics: home, work, travel, health, daily routines

Each item MUST follow this exact JSON schema:
{{
  "skill_ids": ["{domain['id']}"],
  "exercise_type": "cloze",
  "cefr_level": "<A1|A2|A2+|B1|B1+>",
  "gse_target": <integer in {domain['gse_min']}–{domain['gse_max']}>,
  "content": {{
    "instruction": "Choose the correct word to complete the sentence.",
    "prompt": "<sentence with ___ gap>",
    "correct_answer": "<target word>",
    "distractors": ["<wrong word 1>", "<wrong word 2>", "<wrong word 3>"],
    "distractor_rationale": ["<why wrong>", "<why wrong>", "<why wrong>"]
  }},
  "difficulty_features": {{
    "gse_target": <integer>,
    "sentence_length_tokens": <integer>,
    "target_form_complexity": "simple"
  }}
}}

Produce exactly {n} items as a JSON array. No markdown, no explanation."""

    return SYSTEM_PROMPT, user_prompt


def build_vocab_mc_prompt(domain: dict, n: int = 10) -> tuple[str, str]:
    sample_words = ", ".join(domain.get("sample_words", [])[:15])
    dist = _difficulty_distribution(domain["gse_min"], domain["gse_max"], domain["gse_mean"])
    cefr_low = _gse_to_cefr(domain["gse_min"])
    cefr_high = _gse_to_cefr(domain["gse_max"])

    user_prompt = f"""Generate {n} VOCABULARY MULTIPLE CHOICE exercises for the domain: {domain['name']}
Category: {domain['subcategory']}
CEFR range: {cefr_low}–{cefr_high} | GSE range: {domain['gse_min']}–{domain['gse_max']}
Target vocabulary (sample): {sample_words}

{dist}

CRITICAL DISAMBIGUATION RULE:
The correct answer must be the ONLY option that fits. Design each sentence so that distractors are clearly wrong by:
  (a) creating a nonsensical or contradictory meaning, OR
  (b) breaking a fixed collocation, OR
  (c) contradicting other information in the sentence, OR
  (d) referring to a different entity/role that cannot perform the action.
DO NOT write sentences where multiple options would all make sense (e.g. "I put ___ on bread" where butter/jam/cheese all fit).

Rules:
- Each item tests understanding of a word from the domain in context
- Options must all come from the same semantic field (all food words, all colour words, etc.)
- Distractors must be plausible (similar meaning or related topic) but clearly wrong in context

Each item MUST follow this exact JSON schema:
{{
  "skill_ids": ["{domain['id']}"],
  "exercise_type": "multiple_choice",
  "cefr_level": "<A1|A2|A2+|B1|B1+>",
  "gse_target": <integer in {domain['gse_min']}–{domain['gse_max']}>,
  "content": {{
    "instruction": "Choose the best word to complete the sentence.",
    "prompt": "<sentence with ___ gap>",
    "correct_answer": "<correct word>",
    "distractors": ["<word 2>", "<word 3>", "<word 4>"],
    "distractor_rationale": ["<why wrong>", "<why wrong>", "<why wrong>"]
  }},
  "difficulty_features": {{
    "gse_target": <integer>,
    "sentence_length_tokens": <integer>,
    "target_form_complexity": "simple"
  }}
}}

Produce exactly {n} items as a JSON array. No markdown, no explanation."""

    return SYSTEM_PROMPT, user_prompt


def build_vocab_word_formation_prompt(domain: dict, n: int = 5) -> tuple[str, str]:
    sample_words = ", ".join(domain.get("sample_words", [])[:15])
    dist = _difficulty_distribution(domain["gse_min"], domain["gse_max"], domain["gse_mean"])

    user_prompt = f"""Generate {n} WORD FORMATION exercises for the domain: {domain['name']}
Target vocabulary (sample): {sample_words}
GSE range: {domain['gse_min']}–{domain['gse_max']}

{dist}

Rules:
- Provide a BASE WORD (noun or verb root from the domain)
- Student must use the correct form (noun→adjective, verb→noun, etc.) in context
- The transformation should be one step (one suffix/prefix)

Each item MUST follow this exact JSON schema:
{{
  "skill_ids": ["{domain['id']}"],
  "exercise_type": "word_formation",
  "cefr_level": "<A2|B1|B1+>",
  "gse_target": <integer in {domain['gse_min']}–{domain['gse_max']}>,
  "content": {{
    "instruction": "Use the word in brackets in the correct form to complete the sentence.",
    "prompt": "<sentence with ___ gap> (BASE_WORD)",
    "correct_answer": "<derived form>",
    "base_word": "<BASE_WORD>",
    "distractors": null,
    "distractor_rationale": null
  }},
  "difficulty_features": {{
    "gse_target": <integer>,
    "sentence_length_tokens": <integer>,
    "target_form_complexity": "<simple|compound>"
  }}
}}

Produce exactly {n} items as a JSON array. No markdown, no explanation."""

    return SYSTEM_PROMPT, user_prompt


def _unused_build_ambiguity_check_prompt(item: dict) -> tuple[str, str]:
    system = "You are a test-item editor reviewing exercises for genuine ambiguity."
    prompt_text = item.get("content", {}).get("prompt", "")
    correct = item.get("content", {}).get("correct_answer", "")
    distractors = item.get("content", {}).get("distractors") or []

    user = f"""Exercise:
Prompt: {prompt_text}
Marked correct answer: {correct}
Distractors: {distractors}

Task: Decide if this item is GENUINELY ambiguous. An item is unambiguous (PASS) when the marked answer is the BEST and most natural fit, even if a distractor is theoretically possible in some unusual context.

PASS the item (unambiguous=true) if:
- The marked answer is clearly the most natural/conventional choice in context
- The marked answer matches a typical real-world situation
- Distractors require unusual/contrived interpretations to be correct

FAIL the item (unambiguous=false) ONLY if:
- A distractor would be just as natural and conventional as the marked answer
- The sentence has no contextual clues that favour the marked answer over a distractor
- A native speaker would genuinely accept the distractor as equally correct

Examples:
- "She spread ___ on warm toast that melted immediately" → "butter": PASS (butter is the conventional spread that melts on toast; "cheese" or "chocolate" are theoretically possible but unusual)
- "I put ___ on my toast" → "butter": FAIL (no context — jam, honey, butter all equally natural)
- "The ___ cooked the meal in the kitchen" → "chef": PASS (chef is the natural agent; "waiter" is grammatical but contradicts the kitchen context)

Reply with ONLY valid JSON (no markdown):
{{"unambiguous": true, "reason": "short explanation"}}"""

    return system, user


def _unused_build_skill_match_prompt(item: dict, skill: dict, skill_description: str) -> tuple[str, str]:
    system = "You are a language teaching expert reviewing test items for skill alignment."
    prompt_text = item.get("content", {}).get("prompt", "")
    correct = item.get("content", {}).get("correct_answer", "")
    category = skill.get("category", "grammar")

    if category == "vocabulary":
        user = f"""Exercise: {prompt_text} → {correct}
Target domain: {skill['name']} (vocabulary domain covering all words related to this topic)

Does this exercise test vocabulary that belongs to the '{skill['name']}' domain?
Any word that is commonly associated with this topic counts as a match.
Reply ONLY with valid JSON (no markdown):
{{"matches": true, "actual_skill": "brief note"}}"""
    else:
        user = f"""Exercise: {prompt_text} → {correct}
Target skill: {skill['name']} ({skill_description})

Does this exercise primarily test the stated grammar skill?
Reply ONLY with valid JSON (no markdown):
{{"matches": true, "actual_skill": "description of what it actually tests"}}"""

    return system, user
