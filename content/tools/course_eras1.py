"""Era 1: Pre-Socratics, plus course metadata."""
from course_helpers import A, src, txt, PG


def course_meta():
    return {
        "id": "western-philosophy",
        "title": "Western Philosophy: A Guided Reading Course",
        "subtitle": "What to read next, from the Pre-Socratics to now",
        "description": (
            "A professor-designed sequence of exact sittings: the pages that teach the move, "
            "why they come now, what to look for, and the questions that make the next text possible. "
            "Primary texts are the course. Public-domain English translations are hosted in the app; "
            "in-copyright works are assigned as bibliographic readings you obtain legally."
        ),
        "audience": "Self-taught student; no prior philosophy required",
        "estimatedHours": 125,
        "method": (
            "Read in order. Home always names the next unread assignment; do not skip ahead to the famous title. "
            "Each sitting is 20–90 minutes unless the text itself refuses to be cut. Read the assigned pages, "
            "not the surrounding commentary, unless the assignment is marked secondary.\n\n"
            "Keep a notebook. For every sitting, write (1) the claim in one or two sentences without jargon, "
            "(2) the best objection you can find in the text or invent honestly, and (3) one question you could not settle. "
            "Those three lines are the course’s memory.\n\n"
            "When a reading is hosted in the app, read it there. The outbound URL is the bibliographic record and a backup. "
            "When an assignment is bibliographic, get a library or purchased copy. Do not use a pirated scan. "
            "Later units assume earlier ones: Hume will not make sense if you have only a rumor of Descartes; "
            "Kant will not make sense if Hume is a rumor; the twentieth century will not make sense if Kant is a rumor.\n\n"
            "You are not collecting opinions. You are learning a set of moves — how a question is posed, how an argument is forced, "
            "and how a later writer inherits a problem. If a sitting feels too short, reread it. If it feels too long, slow down; "
            "the split assignments exist so you never have to swallow a system in one evening.\n\n"
            "After each sitting, take the quiz. It is not a trap; it is the seminar’s check that you caught the move. "
            "Missed items point you back into the pages, not to a summary."
        ),
    }


def era_presocratic():
    return {
        "id": "ancient-presocratic",
        "order": 1,
        "title": "The Pre-Socratics",
        "years": "c. 600–450 BCE",
        "intro": (
            "Philosophy begins when the world is asked to explain itself without being a story about the gods’ moods. "
            "The Milesians look for an underlying stuff and a process; Heraclitus and Parmenides then force a crisis: "
            "if everything changes, what can be known, and if what is cannot not-be, how can there be change at all? "
            "You are not collecting slogans about water or fire. You are watching the first disciplined fight over nature, logos, and being — "
            "the fight Plato and Aristotle inherit."
        ),
        "themes": ["nature", "logos", "being", "change"],
        "units": [
            {
                "id": "myth-to-physis",
                "order": 1,
                "title": "From myth to nature",
                "professorNote": (
                    "Start with a short orientation, then the Milesians. Burnet is dated, and that is useful: "
                    "you see an older reconstruction of fragments rather than a modern handbook’s smoothness. "
                    "Read him for the fragments and the problem, not for every conjecture."
                ),
                "assignments": [
                    A(
                        "burnet-introduction",
                        1,
                        "secondary",
                        "Why these fragments matter",
                        "John Burnet",
                        "Early Greek Philosophy",
                        "n/a (English original)",
                        "Introduction",
                        "Burnet, Introduction (through the discussion of ‘nature’ and coming-to-be)",
                        40,
                        "You cannot meet Heraclitus or Parmenides as isolated aphorists. Burnet’s opening shows why the first philosophers "
                        "are doing something different from myth even when they still talk of gods, and why ‘nothing comes from nothing’ "
                        "is already a constraint on explanation. Read this so the fragments later feel like arguments, not tattoos.",
                        [
                            "What counts, for Burnet, as the break from mythological explanation",
                            "The principle that nothing comes to be from nothing — and why it will haunt the next units",
                            "How ‘nature’ (physis) is being used as a name for what underlies change",
                        ],
                        [
                            "In one sentence, what is the Milesian project if it is not ‘science’ in our sense?",
                            "Why would a constraint on coming-to-be force a crisis about change?",
                        ],
                        [],
                        "Next you meet the first answers: water, the indefinite, air.",
                        src(PG, "https://www.gutenberg.org/ebooks/67097", "Introduction", "Burnet, 3rd ed.; PG #67097"),
                        txt("burnet-early-greek", "Introduction", "excerpt", "intro", "intro"),
                    ),
                    A(
                        "milesian-school",
                        2,
                        "primary",
                        "Thales, Anaximander, Anaximenes",
                        "John Burnet (presenting Milesian fragments)",
                        "Early Greek Philosophy, ch. I",
                        "Burnet’s English of the fragments and testimonies",
                        "The Milesian School — Thales, Anaximander, Anaximenes",
                        "Burnet, Chapter I (skip later scholarly disputes once you have the three positions)",
                        50,
                        "Three attempts to name what the world is ‘from.’ Thales’ water is less interesting as meteorology than as the claim "
                        "that diverse things share an underlying nature. Anaximander’s apeiron and the language of justice between opposites "
                        "is the first hint that explanation may need something not itself a familiar element. Anaximenes’ air and condensation "
                        "is a process-story: difference is rarefaction and compression. Get these three on the table before flux and being.",
                        [
                            "Whether ‘water’ is an element in our sense or a stand-in for the living, the moist, the source",
                            "Anaximander’s apeiron: why the origin cannot be one of the opposites it explains",
                            "Anaximenes: a mechanism (rarefaction/condensation) rather than a mere name of stuff",
                        ],
                        [
                            "Which Milesian is doing cosmology, and which is already doing a kind of metaphysics?",
                            "If you had to defend one of the three as the most philosophically ambitious, which and why?",
                        ],
                        ["burnet-introduction"],
                        "Xenophanes will attack the gods of the poets; then Heraclitus will refuse a stable stuff altogether.",
                        src(PG, "https://www.gutenberg.org/ebooks/67097", "Chapter I", "Burnet; PG #67097"),
                        txt("burnet-early-greek", "Chapter I, The Milesian School", "excerpt", "milesians", "milesians"),
                    ),
                ],
            },
            {
                "id": "logos-and-flux",
                "order": 2,
                "title": "Logos, critique of the poets, flux",
                "professorNote": "Xenophanes shows that theology can be criticized. Heraclitus shows that order might live inside change. Read the fragments slowly; do not let ‘flux’ become a slogan.",
                "assignments": [
                    A(
                        "xenophanes-poets",
                        1,
                        "primary",
                        "Xenophanes against the poets",
                        "Xenophanes (via Burnet)",
                        "Early Greek Philosophy, ch. II (Xenophanes)",
                        "Burnet",
                        "The Xenophanes pages in ‘Science and Religion’",
                        "Burnet, Chapter II, Xenophanes of Kolophon (the fragments on the gods and on one greatest god)",
                        35,
                        "Before Socrates, someone already says: the poets attribute to the gods theft, adultery, and whatever is a shame among men; "
                        "and that mortals make gods in their own image. This is not atheism as a modern identity. It is the claim that a serious account "
                        "of the divine cannot be a projection of our vices and our local shapes. You need this before you hear Socrates on piety.",
                        [
                            "The ethnological jab: Ethiopians’ gods, Thracians’ gods",
                            "What ‘one god, greatest among gods and men’ does and does not settle",
                            "Whether this is theology, epistemology, or cultural criticism — or all three",
                        ],
                        [
                            "Is Xenophanes replacing myth with a better story, or refusing story-form?",
                            "What would a Xenophanean critique of a modern ‘god of the gaps’ look like?",
                        ],
                        ["milesian-school"],
                        "Heraclitus will keep the divine in the account — as logos and fire — without letting it be a character in a poem.",
                        src(PG, "https://www.gutenberg.org/ebooks/67097", "Chapter II, Xenophanes", "Burnet; PG #67097"),
                        txt("burnet-early-greek", "Chapter II, Xenophanes", "excerpt", "science-religion", "science-religion"),
                    ),
                    A(
                        "heraclitus-fragments",
                        2,
                        "primary",
                        "Heraclitus: logos, strife, the river",
                        "Heraclitus (via Burnet)",
                        "Fragments, in Early Greek Philosophy, ch. III",
                        "John Burnet",
                        "Selected fragments: B1, B2, B12, B50, B51, B80, B123, and the surrounding Burnet discussion",
                        "Burnet, Chapter III, especially the fragments on logos, war, and the river",
                        45,
                        "Heraclitus is the first writer in this course who will punish you for paraphrase. The logos is common, but people live as if they had a private understanding. "
                        "Strife is not a regrettable accident; it is how things hold together. The river fragments do not say ‘nothing is stable’ in the lazy sense — "
                        "they ask how something can be the same while it flows. Read until you can state the view without the word ‘flux.’",
                        [
                            "What ‘logos’ seems to mean in B1–B2 — speech, measure, account, the way things are",
                            "Whether the river fragments imply no stability, or a stability that is the pattern of change",
                            "War/strife as justice (B80) versus a mere celebration of violence",
                        ],
                        [
                            "Can you state Heraclitus’s view without the word ‘flux’?",
                            "If the logos is common, why does he sound so contemptuous of ‘the many’?",
                        ],
                        ["xenophanes-poets"],
                        "Parmenides will deny the road of not-being. Keep Heraclitus’s river in mind as the view being refused.",
                        src(PG, "https://www.gutenberg.org/ebooks/67097", "Chapter III", "Burnet; PG #67097"),
                        txt("burnet-early-greek", "Chapter III, Herakleitos", "excerpt", "heraclitus", "heraclitus"),
                    ),
                ],
            },
            {
                "id": "being-and-eleatics",
                "order": 3,
                "title": "Being and the Eleatic challenge",
                "professorNote": "This is the hinge of early Greek philosophy. If Parmenides is right, cosmology as the Milesians did it is a mistake. Plato’s forms and Aristotle’s potentiality are, in part, replies.",
                "assignments": [
                    A(
                        "parmenides-truth",
                        1,
                        "primary",
                        "Parmenides: the way of truth",
                        "Parmenides (via Burnet)",
                        "Early Greek Philosophy, ch. IV",
                        "John Burnet",
                        "The Way of Truth (and Burnet’s brief frame); glance at the Way of Opinion so you see the contrast",
                        "Burnet, Chapter IV, especially the Way of Truth fragments",
                        50,
                        "Parmenides tells you there are two roads: that it is, and that it is not. The second cannot be thought or said. "
                        "From that he unpacks: what is is ungenerated, imperishable, whole, unmoving. This is not poetry about a sphere for its own sake. "
                        "It is a ban on explaining what is by what is not — coming-to-be, difference, and empty space all come under suspicion. "
                        "If you feel the room tilt, the course is working.",
                        [
                            "The two roads, and why ‘is not’ cannot be a way of inquiry",
                            "What follows for coming-to-be and perishing",
                            "The ‘sphere’ language: metaphor, cosmology, or a claim about completeness",
                        ],
                        [
                            "Does Parmenides deny change, or deny that change can be thought as a passage through not-being?",
                            "What would a Milesian have to give up if this argument holds?",
                        ],
                        ["heraclitus-fragments"],
                        "Zeno will defend this with paradoxes you already half-know. Then pluralists will try to save the appearances.",
                        src(PG, "https://www.gutenberg.org/ebooks/67097", "Chapter IV", "Burnet; PG #67097"),
                        txt("burnet-early-greek", "Chapter IV, Parmenides", "excerpt", "parmenides", "parmenides"),
                    ),
                    A(
                        "zeno-paradoxes",
                        2,
                        "primary",
                        "Zeno’s paradoxes of motion",
                        "Zeno of Elea (via Burnet)",
                        "Early Greek Philosophy, ch. VIII",
                        "John Burnet",
                        "The younger Eleatics — Zeno on plurality and motion",
                        "Burnet, Chapter VIII, Zeno (Achilles, the arrow, dichotomy — as Burnet reconstructs them)",
                        40,
                        "Zeno is not a puzzle-book. He is Parmenides’ bodyguard: if you insist on many things and on motion, you inherit contradictions. "
                        "Read the paradoxes as pressure on the idea that space and time are infinitely divisible, and on the idea that a thing is a sum of parts. "
                        "Aristotle will spend a career answering this; you only need to feel why an answer is required.",
                        [
                            "Whether the target is motion as such, or a certain picture of space/time as points",
                            "The difference between ‘never finishes the halves’ and ‘the arrow is at rest in an instant’",
                            "How plurality (many things) is as threatened as locomotion",
                        ],
                        [
                            "If you had to pick one paradox as philosophically deepest, which, and what assumption does it attack?",
                            "Is Zeno proving Parmenides, or only refuting the opponents’ physics?",
                        ],
                        ["parmenides-truth"],
                        "Empedocles, Anaxagoras, and the atomists will try to keep being from not-being without denying the world of change.",
                        src(PG, "https://www.gutenberg.org/ebooks/67097", "Chapter VIII", "Burnet; PG #67097"),
                        txt("burnet-early-greek", "Chapter VIII, Younger Eleatics", "excerpt", "eleatics", "eleatics"),
                    ),
                ],
            },
            {
                "id": "saving-appearances",
                "order": 4,
                "title": "Saving the appearances",
                "professorNote": "After Parmenides, cosmology has to be a theory of mixture, seeds, or atoms — rearrangement, not generation from nothing. These pages exist so Plato’s ‘participation’ and Aristotle’s ‘potentiality’ do not look like unmotivated jargon.",
                "assignments": [
                    A(
                        "empedocles-anaxagoras",
                        1,
                        "primary",
                        "Mixture, Love and Strife, Mind",
                        "Empedocles and Anaxagoras (via Burnet)",
                        "Early Greek Philosophy, chs. V–VI",
                        "John Burnet",
                        "Empedocles’ four roots and two forces; Anaxagoras on seeds and Nous — Burnet’s fragment selections, not every testimony",
                        "Burnet, Chapter V (the cosmic cycle and the four roots) and Chapter VI (Nous; ‘in everything a portion of everything’)",
                        55,
                        "Empedocles keeps Parmenides’ ban on genuine coming-to-be: what we call birth is mixture of ungenerated roots, driven by Love and Strife. "
                        "Anaxagoras keeps mixture too, but makes Mind the arranger — a first hint that explanation may require intelligence, not only stuff. "
                        "You are watching the invention of a strategy: save change by making it rearrangement.",
                        [
                            "How ‘birth’ is rewritten as mixture so that nothing comes from nothing",
                            "Love and Strife as causes versus as mythic names",
                            "Anaxagoras’s Nous: why mind is introduced, and whether it actually does any work in the fragments",
                        ],
                        [
                            "Is rearrangement enough to explain qualitative difference (life, thought, color)?",
                            "Socrates in the Phaedo will complain that Anaxagoras promised mind and delivered airs and aethers. On this reading, is the complaint fair?",
                        ],
                        ["zeno-paradoxes"],
                        "The atomists give the most economical version of the same strategy: atoms and void.",
                        src(PG, "https://www.gutenberg.org/ebooks/67097", "Chapters V–VI", "Burnet; PG #67097"),
                        txt("burnet-early-greek", "Chapters V–VI", "excerpt", "empedocles", "anaxagoras"),
                    ),
                    A(
                        "atomists-leucippus",
                        2,
                        "primary",
                        "Atoms and void",
                        "Leucippus and Democritus (via Burnet)",
                        "Early Greek Philosophy, ch. IX",
                        "John Burnet",
                        "Leukippos/Democritus: atoms, void, and the denial of genuine coming-to-be",
                        "Burnet, Chapter IX",
                        40,
                        "Void is the Eleatic scandal made productive: ‘what is not’ is allowed as empty place so that atoms can move. "
                        "Atoms themselves are Parmenidean little beings — uncuttable, ungenerated — and the world is their collisions. "
                        "This is the ancestor of every later materialism you will meet, from Lucretius to Hobbes. Read it as a philosophical decision, not as a lucky guess about chemistry.",
                        [
                            "Why void is required if atoms are to move",
                            "How atomic differences (shape, arrangement) are supposed to explain sensible qualities",
                            "What happens to mind, value, and the gods on this picture",
                        ],
                        [
                            "Is the void ‘what is not,’ and if so has Parmenides been answered or ignored?",
                            "What would you still not understand about a living animal if you had a complete atomic inventory?",
                        ],
                        ["empedocles-anaxagoras"],
                        "You now have the problem-space Socrates walks into: nature-explanations that do not yet tell you how to live.",
                        src(PG, "https://www.gutenberg.org/ebooks/67097", "Chapter IX", "Burnet; PG #67097"),
                        txt("burnet-early-greek", "Chapter IX, Leukippos", "excerpt", "atomists", "atomists"),
                    ),
                ],
            },
        ],
    }
