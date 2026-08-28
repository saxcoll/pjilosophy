"""Eras 3–6: Hellenistic through early modern."""
from course_helpers import A, src, txt, PG, MIT, CCEL, WS


def bib(locator, edition, note, url="https://search.worldcat.org/"):
    return src(
        "Library or licensed edition",
        url,
        locator,
        edition,
        license_="in-copyright",
        available=False,
        note=note,
    )


def era_hellenistic():
    return {
        "id": "hellenistic",
        "order": 3,
        "title": "Hellenistic schools",
        "years": "c. 300 BCE–200 CE",
        "intro": (
            "After Aristotle, philosophy becomes a way of life under uncertainty and empire. Epicureans reduce fear by a physics of atoms and a careful hedonism. "
            "Stoics relocate freedom inside what is up to us. Skeptics suspend judgment to find quiet. You are learning three answers to the same question: "
            "how to live when the cosmos will not arrange itself around your wishes."
        ),
        "themes": ["pleasure", "assent", "tranquility", "skepticism"],
        "units": [
            {
                "id": "epicurean-garden",
                "order": 1,
                "title": "The Garden: pleasure without frenzy",
                "professorNote": "Epicurus is short and lucent; Lucretius is the physics and the therapy of death. Read them as one argument in two voices.",
                "assignments": [
                    A(
                        "epicurus-menoeceus",
                        1,
                        "primary",
                        "Letter to Menoeceus",
                        "Epicurus",
                        "Letter to Menoeceus",
                        "Robert Drew Hicks",
                        "The whole letter",
                        "Complete letter (Hicks)",
                        35,
                        "This is the cleanest statement of Epicurean ethics you will get. Pleasure is the end, but not the banquet: natural and necessary desires, the limit of pain, "
                        "the claim that death is nothing to us because when we are, death is not. Prudence is called more precious than philosophy itself. "
                        "Read it against Aristotle’s eudaimonia: a rival account of a complete life, stripped of civic grandeur.",
                        [
                            "The classification of desires (natural/necessary vs empty)",
                            "Why death is ‘nothing to us’ — the symmetry of not-yet and no-longer",
                            "How prudence, not luxury, produces ataraxia",
                        ],
                        [
                            "Is this hedonism, or a discipline against hedonism as the many practice it?",
                            "What must be true of the soul for death to be nothing to us?",
                        ],
                        ["aristotle-posterior-analytics"],
                        "Lucretius will give the atomic physics that is supposed to make this courage possible.",
                        src(MIT, "https://classics.mit.edu/Epicurus/menoec.html", "complete letter", "Hicks; MIT Classics"),
                        txt("epicurus-menoeceus", "Letter to Menoeceus, complete", "full"),
                    ),
                    A(
                        "lucretius-atoms",
                        2,
                        "primary",
                        "Lucretius I: nothing comes from nothing",
                        "Lucretius",
                        "Of the Nature of Things",
                        "William Ellery Leonard",
                        "Book I: atoms, void, the ban on generation from nothing",
                        "De rerum natura Book I (opening through atoms and void; Leonard)",
                        50,
                        "Lucretius turns Epicurus into Latin verse so that fear of the gods and of death can be treated as errors in physics. "
                        "Nothing comes from nothing; nothing passes into nothing; there is void as well as body. "
                        "You have heard this strategy since the atomists. Now it is in the service of a life: if the world is atoms, the thunderbolt is not a judgment.",
                        [
                            "The argument that something cannot arise from nothing",
                            "Why void is required for motion",
                            "How physics is already ethics here — a therapy of fear",
                        ],
                        [
                            "What religious fear is supposed to dissolve if Book I is true?",
                            "Is ‘nothing from nothing’ a physical claim, a logical claim, or both?",
                        ],
                        ["epicurus-menoeceus"],
                        "Book III: why death cannot harm the one who dies.",
                        src(PG, "https://www.gutenberg.org/ebooks/785", "Book I", "Leonard; PG #785"),
                        txt("lucretius-nature", "Book I", "excerpt", "book-i", "book-i"),
                    ),
                    A(
                        "lucretius-death",
                        3,
                        "primary",
                        "Lucretius III: death is nothing to us",
                        "Lucretius",
                        "Of the Nature of Things",
                        "William Ellery Leonard",
                        "Book III: the mortal soul; the argument that death is not an evil",
                        "De rerum natura Book III (the soul’s mortality and the consolation)",
                        50,
                        "If the soul is a fine atomic structure that dissolves, there is no surviving subject to suffer after death. "
                        "The ‘now we are, death is not’ argument returns with images: the unborn, the broken vessel. "
                        "You may reject materialism and still need to say why this consolation fails. That is the sitting.",
                        [
                            "Why the soul must be bodily if it is to move a body",
                            "The no-surviving-subject argument",
                            "The appeal to the time before birth as analogue of the time after death",
                        ],
                        [
                            "Does the argument show that death is not bad, or only that post-mortem experience is impossible?",
                            "What would a Platonic dualist have to deny in Book III’s opening moves?",
                        ],
                        ["lucretius-atoms"],
                        "The Stoics will relocate the good inside assent, not in the dissolution of fear by physics.",
                        src(PG, "https://www.gutenberg.org/ebooks/785", "Book III", "Leonard; PG #785"),
                        txt("lucretius-nature", "Book III", "excerpt", "book-iii", "book-iii"),
                    ),
                ],
            },
            {
                "id": "stoic-discipline",
                "order": 2,
                "title": "Stoic discipline",
                "professorNote": "Epictetus first (the handbook), then Marcus (the notebook). The theory is simple; the difficulty is the use. Do not romanticize either man.",
                "assignments": [
                    A(
                        "epictetus-enchiridion-i",
                        1,
                        "primary",
                        "Enchiridion 1–29: what is up to us",
                        "Epictetus",
                        "Enchiridion",
                        "Thomas W. Higginson (this PG edition)",
                        "Opening half of the Manual, especially §§1–11, 15–21",
                        "Enchiridion §§1–29 (stop before the later social maxims if pressed for time)",
                        40,
                        "The first sentence is the whole school: some things are up to us, some are not. Assent, impulse, desire — these can be trained. Body, property, reputation are not. "
                        "Happiness is not getting the world to obey; it is not demanding that it obey. "
                        "Read this as a theory of freedom after Aristotle’s civic virtue: the slave Epictetus is claiming a freedom a consul might lack.",
                        [
                            "The dichotomy of control, stated without slogan",
                            "How desire and aversion are to be relocated",
                            "What ‘follow nature’ means when nature includes other people’s injustice",
                        ],
                        [
                            "Is this wisdom, or a way of calling losses unimportant so they hurt less?",
                            "Can a Stoic still have duties to others if their welfare is ‘not up to us’?",
                        ],
                        ["lucretius-death"],
                        "Finish the Manual, then watch an emperor try to live it.",
                        src(PG, "https://www.gutenberg.org/ebooks/45109", "Enchiridion first half", "PG #45109"),
                        txt("epictetus-enchiridion", "Enchiridion (use §§1–29)", "full"),
                    ),
                    A(
                        "epictetus-enchiridion-ii",
                        2,
                        "primary",
                        "Enchiridion 30–53: roles, shame, and the philosopher",
                        "Epictetus",
                        "Enchiridion",
                        "Thomas W. Higginson (this PG edition)",
                        "The remainder of the Manual",
                        "Enchiridion §§30–53",
                        35,
                        "The second half applies the dichotomy to roles (father, citizen), to insult, to divination, to the wish to be a philosopher in appearance. "
                        "Notice how social life is not abandoned: you play the role well, without needing the world’s applause. "
                        "This is the ancestor of later ‘interior’ freedom — and of every cheap self-help version. Keep the cheap version out.",
                        [
                            "How roles (son, citizen) can bind without making outcomes ‘up to us’",
                            "The treatment of insult and reputation",
                            "What a philosopher looks like when not performing philosophy",
                        ],
                        [
                            "Does ‘play your role’ collapse into conventional obedience?",
                            "Where would Epictetus tell you to resist a law, if ever?",
                        ],
                        ["epictetus-enchiridion-i"],
                        "Marcus writes the same discipline from the other end of the social scale.",
                        src(PG, "https://www.gutenberg.org/ebooks/45109", "Enchiridion second half", "PG #45109"),
                        txt("epictetus-enchiridion", "Enchiridion (use §§30–53)", "full"),
                    ),
                    A(
                        "marcus-meditations",
                        3,
                        "primary",
                        "Marcus Aurelius, Books II–IV",
                        "Marcus Aurelius",
                        "Meditations",
                        "George Long",
                        "Books II–IV",
                        "Meditations II–IV (Long)",
                        50,
                        "These are notes to himself, not a treatise. That is the point: you see the Stoic machinery under fatigue — death, the court, the body’s complaint. "
                        "Look for the view from above, the reminder that you are a part of the whole, and the refusal to be stained by another’s judgment. "
                        "Compare the tone with Epictetus: same doctrine, different temperature.",
                        [
                            "The ‘view from above’ and what it is for",
                            "How he talks himself out of anger without denying that people act badly",
                            "Death as a natural process, not a catastrophe",
                        ],
                        [
                            "Is this piety toward the cosmos, or a technique for an overworked administrator?",
                            "What would Epicurus dispute in Marcus’s picture of the whole?",
                        ],
                        ["epictetus-enchiridion-ii"],
                        "Skepticism will ask whether you should assent to any of these pictures of nature.",
                        src(PG, "https://www.gutenberg.org/ebooks/2680", "Books II–IV", "Long; PG #2680"),
                        txt("marcus-meditations", "Books II–IV", "excerpt", "book-ii", "book-iv"),
                    ),
                ],
            },
            {
                "id": "living-without-assent",
                "order": 3,
                "title": "Skepticism as a way",
                "professorNote": "Sextus is not Hume. Pyrrhonism aims at quiet by withholding assent, not at a theory that nothing can be known. Catch that difference.",
                "assignments": [
                    A(
                        "sextus-outlines-i",
                        1,
                        "primary",
                        "Sextus: what skepticism is",
                        "Sextus Empiricus",
                        "Pyrrhonic Sketches (Outlines of Pyrrhonism), Book I",
                        "Mary Mills Patrick",
                        "Book I of the Pyrrhonic Sketches as Patrick translates it",
                        "Outlines Book I (definition of skepticism, the modes, ataraxia as the aim)",
                        55,
                        "Skepticism is an ability to set appearances against appearances so that one suspends judgment and a quiet follows. "
                        "It is not the dogma ‘nothing can be known’ — that would be another position. The tropes (modes) are tools, not a metaphysics. "
                        "You will need this when Descartes tries to outflank the skeptic, and when Hume claims a mitigated version.",
                        [
                            "Skepticism as an ability (dunamis), not a thesis",
                            "Why ‘nothing is known’ would be dogmatic",
                            "Ataraxia as the point of epoche, not a side effect the skeptic forgot to want",
                        ],
                        [
                            "Can a skeptic live, if action seems to require belief?",
                            "How does this differ from the Academic skepticism Hume later names?",
                        ],
                        ["marcus-meditations"],
                        "Plotinus will climb the other way: not suspension, but ascent to the One.",
                        src(PG, "https://www.gutenberg.org/ebooks/17556", "Pyrrhonic Sketches Book I", "Patrick; PG #17556"),
                        txt("sextus-outlines", "Book I", "excerpt", "book-i", "book-i"),
                    ),
                ],
            },
        ],
    }


def era_late_antiquity():
    return {
        "id": "late-antiquity",
        "order": 4,
        "title": "Late antiquity and inwardness",
        "years": "c. 200–500 CE",
        "intro": (
            "Platonism becomes a metaphysics of procession from the One; Christianity inherits that ladder and turns it inward. "
            "Augustine is the hinge: the restless heart, the divided will, and time as a distension of the soul. "
            "You are watching philosophy learn to describe a first-person interior that Plato’s Cave only sketched."
        ),
        "themes": ["the One", "will", "time", "interiority"],
        "units": [
            {
                "id": "platonic-ascent",
                "order": 1,
                "title": "From the One to consolation",
                "professorNote": "Plotinus for the structure of reality; Boethius for the imprisoned intellectual who still wants Providence to make sense.",
                "assignments": [
                    A(
                        "plotinus-hypostases",
                        1,
                        "primary",
                        "Plotinus: the three hypostases",
                        "Plotinus",
                        "Enneads (Fifth Ennead, MacKenna)",
                        "Stephen MacKenna",
                        "The stretch on the One, Intellect, and Soul in the hosted MacKenna selection",
                        "Ennead V material as hosted (The Divine Mind / three hypostases)",
                        50,
                        "Reality proceeds: the One beyond being, Intellect that thinks the Forms, Soul that looks both ways. "
                        "This is Plato’s Good rewritten as a cascade. Augustine will read the Platonists and say they saw the country of truth but not the way. "
                        "You only need the three levels and the idea that the lower is an image of the higher — not the whole Enneads.",
                        [
                            "Why the One is not an intellect among others",
                            "Intellect as the realm of Forms — thinking and being together",
                            "Soul’s double look: toward Intellect and toward the sensible",
                        ],
                        [
                            "Is this a religious mysticism, a metaphysics, or both without remainder?",
                            "What happens to the Cave’s prisoner if the ascent is now ontological, not only educational?",
                        ],
                        ["sextus-outlines-i"],
                        "Boethius will ask how a good providence and apparent fortune can coexist.",
                        src(WS, "https://en.wikisource.org/wiki/Plotinus_(MacKenna)", "Fifth Ennead selection", "MacKenna, via Wikisource/CCEL ingest"),
                        txt("plotinus-enneads", "Fifth Ennead selection", "excerpt", "selected", "selected"),
                    ),
                    A(
                        "boethius-consolation",
                        2,
                        "primary",
                        "Boethius: Fortune and the true good",
                        "Boethius",
                        "The Consolation of Philosophy",
                        "H. R. James",
                        "Book I (the complaint) and Book III (the true good)",
                        "Consolation Books I and III",
                        55,
                        "A condemned man is visited by Philosophy, who diagnoses his forgetfulness of his true country. Book III argues that happiness is not Fortune’s gifts but the highest good, which is God — "
                        "and that all seek it even in their errors. You are between Stoic interiority and medieval theism. "
                        "Keep Lady Philosophy’s tone: not comfort as softness, but a reordering of what counts as good.",
                        [
                            "The diagnosis: he has forgotten who he is",
                            "Fortune’s wheel versus a good that cannot be taken",
                            "How Book III identifies happiness with the highest good / God",
                        ],
                        [
                            "Does this console, or does it change the subject from injustice to metaphysics?",
                            "What would Lucretius say is false in the identification of the good with God?",
                        ],
                        ["plotinus-hypostases"],
                        "Augustine will make the turn inward: evil, will, time.",
                        src(PG, "https://www.gutenberg.org/ebooks/14328", "Books I, III", "H. R. James; PG #14328"),
                        txt("boethius-consolation", "Books I and III", "excerpt", "book-i", "book-iii"),
                    ),
                ],
            },
            {
                "id": "augustine-inwardness",
                "order": 2,
                "title": "Augustine: evil, will, time",
                "professorNote": "Three sittings in the Confessions. Do not read them as autobiography only. Each book is a philosophical experiment.",
                "assignments": [
                    A(
                        "augustine-confessions-evil",
                        1,
                        "primary",
                        "Confessions VII: Platonists and evil",
                        "Augustine of Hippo",
                        "Confessions",
                        "E. B. Pusey",
                        "Book VII",
                        "Confessions Book VII",
                        50,
                        "Augustine finds in ‘the books of the Platonists’ the Word, but not the Word made flesh. More important for philosophy: evil as privation, not a rival substance. "
                        "If God is, and is good, evil cannot be a thing with being of its own. This is the metaphysical move against Manichaeism. "
                        "You will hear it again whenever someone says evil is a ‘nothing’ — and you should remember how much work that claim is doing.",
                        [
                            "What the Platonists gave him, and what they did not",
                            "Evil as privation of good, not a positive substance",
                            "The remaining problem: if evil is nothing, why does it weigh on a life?",
                        ],
                        [
                            "Does calling evil a privation explain cruelty, or only block a dualist cosmology?",
                            "Why is the Incarnation, on his telling, something philosophy did not deliver?",
                        ],
                        ["boethius-consolation"],
                        "Book VIII: the will that will not will.",
                        src(PG, "https://www.gutenberg.org/ebooks/3296", "Book VII", "Pusey; PG #3296"),
                        txt("augustine-confessions", "Book VII", "excerpt", "book-vii", "book-vii"),
                    ),
                    A(
                        "augustine-confessions-will",
                        2,
                        "primary",
                        "Confessions VIII: the divided will",
                        "Augustine of Hippo",
                        "Confessions",
                        "E. B. Pusey",
                        "Book VIII",
                        "Confessions Book VIII",
                        50,
                        "He knows what to do and does not do it. The will is split: two wills, neither complete. This is not Aristotle’s akrasia as a lapse of reason’s rule; "
                        "it is a wound in the will itself. The garden, the child’s voice, the taking up of the book — whatever you make of the conversion scene, "
                        "the philosophical payload is the analysis of not being able to will wholly. Later freedom debates live here.",
                        [
                            "The ‘two wills’ and why neither is a second substance",
                            "Habit (consuetudo) as a chain",
                            "What actually ends the deadlock in the narrative — and whether that is an argument",
                        ],
                        [
                            "Is a divided will still one agent, or two?",
                            "What would Epictetus say is missing from Augustine’s account of not doing what one sees?",
                        ],
                        ["augustine-confessions-evil"],
                        "Book XI: what time is, if only the present is.",
                        src(PG, "https://www.gutenberg.org/ebooks/3296", "Book VIII", "Pusey; PG #3296"),
                        txt("augustine-confessions", "Book VIII", "excerpt", "book-viii", "book-viii"),
                    ),
                    A(
                        "augustine-confessions-time",
                        3,
                        "primary",
                        "Confessions XI: what is time?",
                        "Augustine of Hippo",
                        "Confessions",
                        "E. B. Pusey",
                        "Book XI",
                        "Confessions Book XI",
                        55,
                        "If no one asks him, he knows; if he wishes to explain, he does not. Past and future are not; the present has no duration. "
                        "Time is measured in the soul as memory, attention, expectation — a distension. This is one of the origin-points of philosophy of time. "
                        "Read it as a problem forced by Genesis (‘in the beginning’) and by the phenomenology of reciting a psalm.",
                        [
                            "Why past and future seem not to be",
                            "The threefold present: memory, attention, expectation",
                            "Time as distension of the soul (distentio animi)",
                        ],
                        [
                            "If time is in the soul, is there time without a created mind?",
                            "Does the psalm example measure time, or only the soul’s activity?",
                        ],
                        ["augustine-confessions-will"],
                        "Medieval philosophy will ask whether reason can prove what faith believes — starting with Anselm.",
                        src(PG, "https://www.gutenberg.org/ebooks/3296", "Book XI", "Pusey; PG #3296"),
                        txt("augustine-confessions", "Book XI", "excerpt", "book-xi", "book-xi"),
                    ),
                ],
            },
        ],
    }


def era_medieval():
    return {
        "id": "medieval",
        "order": 5,
        "title": "Medieval reason and revelation",
        "years": "c. 1070–1274",
        "intro": (
            "Faith seeks understanding: Anselm tries to prove God from the concept alone; Aquinas insists we start from the world. "
            "In between, Averroes and Maimonides force Latin Christendom to say how philosophy and law/scripture can share a truth. "
            "The move to learn is not ‘the Middle Ages believed in God.’ It is how argument, authority, and demonstration are supposed to fit."
        ),
        "themes": ["faith and reason", "proof", "law", "negative theology"],
        "units": [
            {
                "id": "faith-seeking-understanding",
                "order": 1,
                "title": "Anselm’s argument and the Fool",
                "professorNote": "Read the Proslogion as a prayer that is also a proof. Then let Gaunilo object. Do not skip the objection.",
                "assignments": [
                    A(
                        "anselm-proslogion",
                        1,
                        "primary",
                        "Proslogion 2–4: that than which none greater",
                        "Anselm of Canterbury",
                        "Proslogium",
                        "Sidney Norton Deane",
                        "Chapters 2–4 (with the preface so you hear ‘faith seeking understanding’)",
                        "Proslogium chs. 2–4 (Deane); hosted file includes Gaunilo — stop before Gaunilo for this sitting",
                        40,
                        "God is that than which nothing greater can be thought. The Fool understands the words; what exists in the understanding and in reality is greater than what exists in the understanding alone; "
                        "therefore God exists in reality. This is not a cosmological climb from motion. It is a claim about what the concept already contains. "
                        "Aquinas will reject the strategy. Descartes will revive a cousin of it. Get Anselm’s actual steps, not the cartoon.",
                        [
                            "The definition: ‘that than which nothing greater can be conceived’",
                            "The move from being in the understanding to being in reality",
                            "Why the Fool is said to understand what he denies",
                        ],
                        [
                            "Where, exactly, could a reasonable person refuse the step to extra-mental existence?",
                            "Is this a proof, a clarification of faith, or a spiritual exercise?",
                        ],
                        ["augustine-confessions-time"],
                        "Gaunilo will try the same form with a lost island.",
                        src(CCEL, "https://www.ccel.org/ccel/anselm/basic_works.html", "Proslogium 2–4", "Deane, Open Court; CCEL"),
                        txt("anselm-proslogion", "Proslogium (hosted file opens on the debate; read Anselm’s argument first)", "excerpt", "gaunilo", "gaunilo"),
                    ),
                    A(
                        "gaunilo-and-reply",
                        2,
                        "primary",
                        "Gaunilo’s lost island and Anselm’s reply",
                        "Gaunilo and Anselm",
                        "In Behalf of the Fool; Anselm’s reply",
                        "Sidney Norton Deane",
                        "Gaunilo’s objection and Anselm’s rejoinder",
                        "Hosted sections: Gaunilo, then Anselm’s reply",
                        40,
                        "If the form worked, a most perfect island would exist. Anselm’s reply: the form is not a recipe for any ‘greatest X’; it attaches to a being whose non-existence cannot be conceived. "
                        "Whether that saves the argument is the question. You are learning how ontological arguments live or die by the uniqueness of their subject.",
                        [
                            "The lost-island parody: what it copies and what it hopes to break",
                            "Anselm’s claim that God alone cannot be thought not to exist",
                            "Whether ‘greater’ is being used evaluatively or ontologically",
                        ],
                        [
                            "Does the island fail because islands are contingent, or because ‘greatest island’ is incoherent?",
                            "If you had to side with one of them after this sitting, whom, and on which lemma?",
                        ],
                        ["anselm-proslogion"],
                        "Averroes: whether the Law commands philosophy.",
                        src(CCEL, "https://www.ccel.org/ccel/anselm/basic_works.html", "Gaunilo and reply", "Deane; CCEL"),
                        txt("anselm-proslogion", "Gaunilo and Anselm’s reply", "excerpt", "gaunilo", "reply"),
                    ),
                ],
            },
            {
                "id": "abrahamic-reason",
                "order": 2,
                "title": "Philosophy under the Law",
                "professorNote": "These two sit here because they enter the Latin conversation about faith and reason — not as a tour of Islamic and Jewish thought for its own sake (that would be another course).",
                "assignments": [
                    A(
                        "averroes-decisive",
                        1,
                        "primary",
                        "Averroes: the Law and demonstration",
                        "Averroes (Ibn Rushd)",
                        "Decisive Discourse on the Relation between Religion and Philosophy",
                        "Mohammad Jamil-ur-Rehman",
                        "The Decisive Discourse",
                        "The Decisive Treatise as hosted (PG #65708)",
                        50,
                        "Does the Law command, permit, or forbid the study of philosophy? Averroes argues that demonstration is required for those able, and that truth cannot contradict truth: "
                        "when scripture seems to conflict with demonstration, the apparent sense is to be interpreted. "
                        "Latin ‘Averroism’ will later be a scare-word for double truth. Read him first as trying to prevent that split.",
                        [
                            "The legal question: is philosophizing obligatory for some?",
                            "‘Truth does not contradict truth’ as a rule of interpretation",
                            "Different classes of people, different methods (rhetoric, dialectic, demonstration)",
                        ],
                        [
                            "Is this harmony, or a ranking that makes philosophy the judge of scripture’s sense?",
                            "What danger is he trying to save the community from?",
                        ],
                        ["gaunilo-and-reply"],
                        "Maimonides: how not to speak of God as if God were a magnified creature.",
                        src(PG, "https://www.gutenberg.org/ebooks/65708", "Decisive Discourse", "Jamil-ur-Rehman; PG #65708"),
                        txt("averroes-decisive", "Decisive Discourse", "excerpt", "decisive", "decisive"),
                    ),
                    A(
                        "maimonides-guide",
                        2,
                        "primary",
                        "Maimonides: attributes and perplexity",
                        "Moses Maimonides",
                        "The Guide for the Perplexed",
                        "M. Friedländer",
                        "Introduction plus Part I, chapters 50–52 (attributes)",
                        "Guide: Introduction and I.50–52 (Friedländer)",
                        50,
                        "The Guide is for someone torn between the Law and the philosophers. The attribute chapters teach a discipline: many predicates said of God cannot be real accidents in God. "
                        "Negative theology — saying what God is not — is a way of protecting both unity and speech. Aquinas will borrow and recast this. "
                        "Read for the problem of religious language, not for a complete Maimonidean system.",
                        [
                            "Who the ‘perplexed’ reader is",
                            "Why positive attributes threaten divine simplicity",
                            "What remains of God-talk if many names are negations or relations",
                        ],
                        [
                            "Is negative theology still knowledge of God, or a rule for silence?",
                            "How would Anselm’s ‘greater’ have to be rewritten under this discipline?",
                        ],
                        ["averroes-decisive"],
                        "Aquinas: sacred doctrine, the Five Ways, natural law.",
                        src(PG, "https://www.gutenberg.org/ebooks/73584", "Intro; I.50–52", "Friedländer; PG #73584"),
                        txt("maimonides-guide", "Introduction and I.50–52", "excerpt", "intro", "i-52"),
                    ),
                ],
            },
            {
                "id": "aquinas-ways-and-law",
                "order": 3,
                "title": "Aquinas: demonstration, God, law",
                "professorNote": "Three short scholastic sittings. Learn the form (objections, sed contra, respondeo) as a way of thinking, not as a relic.",
                "assignments": [
                    A(
                        "aquinas-sacred-doctrine",
                        1,
                        "primary",
                        "Summa I q.1: whether sacred doctrine is a science",
                        "Thomas Aquinas",
                        "Summa theologiae",
                        "Fathers of the English Dominican Province",
                        "Prima pars, question 1",
                        "ST I q.1",
                        40,
                        "Is theology a science? Does it need philosophy? Can it prove God, or only take God on authority? "
                        "Question 1 is the methods sitting: sacred doctrine as a science that takes its principles from a higher knowledge (God’s), and that can still use philosophy as a handmaid. "
                        "This is how Aquinas will refuse both ‘fideism’ and ‘philosophy as rival church.’",
                        [
                            "The article-form: objections, sed contra, corpus, replies",
                            "Sacred doctrine as a science whose principles are received",
                            "How philosophy is used without being the source of those principles",
                        ],
                        [
                            "If the principles are revealed, in what sense is this still scientia?",
                            "Where would Averroes and Aquinas agree about demonstration, and where not?",
                        ],
                        ["maimonides-guide"],
                        "Question 2: whether God exists, and the Five Ways.",
                        src(
                            "New Advent",
                            "https://www.newadvent.org/summa/1001.htm",
                            "ST I q.1",
                            "English Dominican Province; New Advent",
                        ),
                        txt("aquinas-summa", "ST I q.1", "excerpt", "st-i-q1", "st-i-q1"),
                    ),
                    A(
                        "aquinas-five-ways",
                        2,
                        "primary",
                        "Summa I q.2: the Five Ways",
                        "Thomas Aquinas",
                        "Summa theologiae",
                        "Fathers of the English Dominican Province",
                        "Prima pars, question 2 (especially a.3, the Five Ways)",
                        "ST I q.2",
                        45,
                        "God’s existence is not self-evident to us (Anselm is refused). It can be demonstrated from effects. "
                        "The Five Ways: motion, efficient cause, contingency, degrees, governance. Each is short. Each depends on a picture of explanation you have from Aristotle: no infinite regress in ordered causes, actuality before potentiality. "
                        "Do not memorize nicknames. Reconstruct one way slowly.",
                        [
                            "Why the ontological argument is set aside in a.1–2",
                            "The shared shape: from observed features to a first that we call God",
                            "What ‘and this we call God’ is doing — naming, not yet describing the Trinity",
                        ],
                        [
                            "Pick one Way. Where is the most disputable premise?",
                            "Does ‘first mover’ already smuggle in a theistic God, or only a terminus of explanation?",
                        ],
                        ["aquinas-sacred-doctrine"],
                        "Natural law: how reason in us participates in eternal law.",
                        src(
                            "New Advent",
                            "https://www.newadvent.org/summa/1002.htm",
                            "ST I q.2",
                            "English Dominican Province; New Advent",
                        ),
                        txt("aquinas-summa", "ST I q.2", "excerpt", "st-i-q2", "st-i-q2"),
                    ),
                    A(
                        "aquinas-natural-law",
                        3,
                        "primary",
                        "Summa I–II qq.90, 94: law and the natural law",
                        "Thomas Aquinas",
                        "Summa theologiae",
                        "Fathers of the English Dominican Province",
                        "I–II q.90 (essence of law) and q.94 (natural law)",
                        "ST I–II q.90 and q.94",
                        50,
                        "Law is an ordinance of reason for the common good, made by who has care of the community, and promulgated. Natural law is the rational creature’s participation in eternal law — "
                        "its first precept: good is to be done and pursued, evil avoided. "
                        "This is the ancestor of later rights talk and of every fight about whether nature grounds ethics. Hume and Moore will try to break the move from is to ought. Remember where the move was built.",
                        [
                            "The four notes of law in q.90",
                            "Eternal, natural, human, divine law as a hierarchy",
                            "The first precept of natural law and how other precepts are said to follow",
                        ],
                        [
                            "Is ‘good is to be done’ a tautology, a perception, or a command?",
                            "What would it take for human law to fail as law, on this account?",
                        ],
                        ["aquinas-five-ways"],
                        "The early modern break: Bacon against idols, Descartes against the whole inherited edifice.",
                        src(
                            "New Advent",
                            "https://www.newadvent.org/summa/2090.htm",
                            "ST I–II q.90, q.94",
                            "English Dominican Province; New Advent",
                        ),
                        txt("aquinas-summa", "ST I–II q.90 and q.94", "excerpt", "st-i-ii-q90", "st-i-ii-q94"),
                    ),
                ],
            },
        ],
    }


def era_early_modern():
    return {
        "id": "early-modern",
        "order": 6,
        "title": "The early modern break",
        "years": "1620–1714",
        "intro": (
            "Authority as a way of knowing comes under suspicion. Bacon catalogues the idols that distort inquiry; Descartes rebuilds from the cogito; "
            "Spinoza identifies God with Nature; Pascal wagers in the dark; Leibniz fills the world with windowless monads. "
            "You are watching metaphysics try to become as certain as geometry — and watching that ambition split."
        ),
        "themes": ["method", "certainty", "God and nature", "substance"],
        "units": [
            {
                "id": "new-organon",
                "order": 1,
                "title": "Idols and method",
                "professorNote": "Bacon for the diagnosis of error; Descartes’ Discourse for the autobiography of a method. Then the Meditations, split.",
                "assignments": [
                    A(
                        "bacon-idols",
                        1,
                        "primary",
                        "Novum Organum I: the idols",
                        "Francis Bacon",
                        "Novum Organum",
                        "n/a (English edition of the Latin)",
                        "Book I aphorisms, especially the four idols",
                        "Novum Organum Book I (idols of Tribe, Cave, Marketplace, Theatre)",
                        45,
                        "Before a new organon, the mind’s built-in distortions must be named. Tribe (human nature), Cave (the individual den), Marketplace (words), Theatre (received systems). "
                        "This is not yet Hume on custom. It is a call to discipline attention toward nature by experiment and tables of instances. "
                        "Read the idols as a theory of error you can still use on yourself.",
                        [
                            "The four idols, with one example each that is not Bacon’s own",
                            "Why words (Marketplace) can fail even when speakers are sincere",
                            "What ‘Theatre’ implies about Aristotle and the schools",
                        ],
                        [
                            "Is Bacon’s remedy a method you could state in steps, or a temperament?",
                            "Which idol would he say is most active when you quote a famous philosopher instead of looking?",
                        ],
                        ["aquinas-natural-law"],
                        "Descartes will try to make method a sequence you can follow from the armchair — then from the stove-heated room.",
                        src(PG, "https://www.gutenberg.org/ebooks/45988", "Book I", "PG #45988"),
                        txt("bacon-novum-organum", "Book I aphorisms", "excerpt", "book-i", "book-i"),
                    ),
                    A(
                        "descartes-discourse",
                        2,
                        "primary",
                        "Discourse on the Method, Parts I–IV",
                        "René Descartes",
                        "Discourse on the Method",
                        "John Veitch",
                        "Parts I–IV (hosted file: Parts II–IV; read those as the method, morals, and cogito)",
                        "Discourse Parts II–IV (Veitch); Part I if your edition has it",
                        50,
                        "The Discourse is the public story: reject what is only probable, follow rules of method, a provisional morality, then the cogito and God as the rescue of certainty. "
                        "It is easier than the Meditations and slightly more dangerous, because it sounds like a life-hack. It is not. It is a claim about what knowledge requires.",
                        [
                            "The rules of method (Part II)",
                            "Why a provisional morality is needed while tearing down the house",
                            "The cogito as it appears here, before the full skeptical machinery",
                        ],
                        [
                            "What survives if you refuse his rules but keep his demand for certainty?",
                            "Is the provisional morality a confession that method cannot guide life, or a temporary scaffold?",
                        ],
                        ["bacon-idols"],
                        "Meditations I–II: doubt, then the ‘I’ that doubts.",
                        src(PG, "https://www.gutenberg.org/ebooks/59", "Parts II–IV", "Veitch; PG #59"),
                        txt("descartes-discourse", "Parts II–IV", "excerpt", "part-2", "part-4"),
                    ),
                ],
            },
            {
                "id": "descartes-meditations",
                "order": 2,
                "title": "The Meditations, in three sittings",
                "professorNote": "Do not read all six in one night. The splits follow the argument’s joints.",
                "assignments": [
                    A(
                        "descartes-meditations-1-2",
                        1,
                        "primary",
                        "Meditations I–II: doubt and the thinking thing",
                        "René Descartes",
                        "Meditations on First Philosophy",
                        "William Molyneux (1680)",
                        "Meditations I and II",
                        "Meditation I (things doubtful); Meditation II (the nature of the mind)",
                        50,
                        "First sitting: the demolition. Senses, dreaming, the malicious deceiver. Then: if I am deceived, I am. The ‘I’ is a thinking thing, known more distinctly than the wax is known by the senses. "
                        "The wax is not a detour; it shows what the intellect does when the sensible qualities change. "
                        "Molyneux’s English is seventeenth-century and public domain. Slow down for the archaism; the argument is the same.",
                        [
                            "Each stage of doubt and what it still leaves standing",
                            "Why the cogito is not an inference from a general premise, as he presents it",
                            "The wax: what remains, and by what faculty it is known",
                        ],
                        [
                            "Does the dreaming argument undermine all sensory belief, or only some?",
                            "Is ‘I am a thinking thing’ a discovery of a substance, or only of an activity?",
                        ],
                        ["descartes-discourse"],
                        "III–IV: God, and why error does not refute clear and distinct perception.",
                        src(PG, "https://www.gutenberg.org/ebooks/70091", "Meditations I–II", "Molyneux; PG #70091"),
                        txt("descartes-meditations", "Meditations I–II", "excerpt", "med-1", "med-2"),
                    ),
                    A(
                        "descartes-meditations-3-4",
                        2,
                        "primary",
                        "Meditations III–IV: God and error",
                        "René Descartes",
                        "Meditations on First Philosophy",
                        "William Molyneux (1680)",
                        "Meditations III and IV",
                        "Meditation III (God); Meditation IV (truth and falsity)",
                        55,
                        "The idea of an infinite God cannot have come from a finite mind, he claims; God exists and is not a deceiver. Then: error comes from the will outrunning the intellect. "
                        "This is the rescue of ‘clear and distinct’ from the evil genius — and the notorious circle if God’s guarantee is proved by perceptions that only God could guarantee. "
                        "Name the circle even if you think there is a way out.",
                        [
                            "The causal principle about ideas and their objective reality",
                            "Why God cannot be a deceiver, on his telling",
                            "Will vs intellect as the account of error",
                        ],
                        [
                            "State the Cartesian circle in one careful sentence.",
                            "Could a finite mind invent the idea of the infinite by negation, as some objectors said?",
                        ],
                        ["descartes-meditations-1-2"],
                        "V–VI: essence of matter, existence of bodies, real distinction of mind and body.",
                        src(PG, "https://www.gutenberg.org/ebooks/70091", "Meditations III–IV", "Molyneux; PG #70091"),
                        txt("descartes-meditations", "Meditations III–IV", "excerpt", "med-3", "med-4"),
                    ),
                    A(
                        "descartes-meditations-5-6",
                        3,
                        "primary",
                        "Meditations V–VI: essence, bodies, dualism",
                        "René Descartes",
                        "Meditations on First Philosophy",
                        "William Molyneux (1680)",
                        "Meditations V and VI",
                        "Meditation V (essence of material things; God again); Meditation VI (existence of bodies; mind–body distinction)",
                        50,
                        "A second ontological argument appears; then the essence of matter as extension. Meditation VI restores the world — not by naive trust in the senses, but by a God who would deceive us if the strong inclination to believe in bodies had no object. "
                        "Mind and body are really distinct because each can be conceived clearly without the other. "
                        "The union remains a fact of sensation and confusion. Spinoza will refuse the two-substance picture.",
                        [
                            "Matter as extension — what is being excluded (weight, color as intrinsic)",
                            "The argument for the existence of bodies",
                            "Real distinction of mind and body, and the leftover problem of their union",
                        ],
                        [
                            "If mind is better known than body, why do we still say we have a body?",
                            "What would have to be true for this dualism to make a living animal unintelligible?",
                        ],
                        ["descartes-meditations-3-4"],
                        "Spinoza: one substance, God-or-Nature.",
                        src(PG, "https://www.gutenberg.org/ebooks/70091", "Meditations V–VI", "Molyneux; PG #70091"),
                        txt("descartes-meditations", "Meditations V–VI", "excerpt", "med-5", "med-6"),
                    ),
                ],
            },
            {
                "id": "after-descartes",
                "order": 3,
                "title": "God-or-Nature, the wager, monads",
                "professorNote": "Three alternatives to Cartesian two-substance theism. None is a footnote.",
                "assignments": [
                    A(
                        "spinoza-ethics-god",
                        1,
                        "primary",
                        "Ethics I: God or Nature",
                        "Benedict de Spinoza",
                        "Ethics",
                        "R. H. M. Elwes",
                        "Part I, through the appendix if your sitting includes it",
                        "Ethics Part I (definitions, axioms, key propositions on substance and God)",
                        60,
                        "One substance, God-or-Nature, infinite attributes. Finite things are modes. Nothing is contingent. "
                        "The geometric form is not decoration: he thinks this can be demonstrated. The appendix against final causes is the ethical payoff of the metaphysics. "
                        "Read slowly. One sitting cannot master Part I; it can show you the claim that Descartes’ two created substances cannot stand.",
                        [
                            "Definitions of substance, attribute, mode",
                            "Why there cannot be two substances of the same nature",
                            "The denial of final causes in the appendix (if present in your stretch)",
                        ],
                        [
                            "Is this pantheism, atheism, or a third thing Spinoza would not name that way?",
                            "What happens to prayer, miracle, and free will if Part I is true?",
                        ],
                        ["descartes-meditations-5-6"],
                        "Pascal: the heart, wretchedness, and the wager — a different use of uncertainty.",
                        src(PG, "https://www.gutenberg.org/ebooks/3800", "Part I", "Elwes; PG #3800"),
                        txt("spinoza-ethics", "Ethics Part I", "excerpt", "part-i", "part-i"),
                    ),
                    A(
                        "pascal-pensees",
                        2,
                        "primary",
                        "Pascal: wretchedness and the wager",
                        "Blaise Pascal",
                        "Pensées",
                        "W. F. Trotter",
                        "The hosted cluster on diversion, wretchedness, and the wager",
                        "Pensées (Trotter): the wager sitting as hosted",
                        40,
                        "Reason cannot settle God; the wager asks you to treat belief as a decision under uncertainty with infinite stake. "
                        "Around it: we run to diversion because we cannot sit quietly in a room; greatness and wretchedness together. "
                        "This is not Aquinas’s demonstration. It is a psychology of the betting animal. You may hate the wager and still need its picture of the human.",
                        [
                            "Why diversion (divertissement) is a philosophical clue, not a moralizing aside",
                            "The structure of the wager: what is staked, what is gained",
                            "What the wager does not claim to prove",
                        ],
                        [
                            "Does the wager require that you can choose belief?",
                            "Is an infinite prize enough to make any finite risk rational — and what does ‘rational’ mean here?",
                        ],
                        ["spinoza-ethics-god"],
                        "Leibniz: a world of monads instead of one substance or two.",
                        src(PG, "https://www.gutenberg.org/ebooks/18269", "wager cluster", "Trotter; PG #18269"),
                        txt("pascal-pensees", "Wager and wretchedness selection", "excerpt", "wager", "wager"),
                    ),
                    A(
                        "leibniz-monadology",
                        3,
                        "primary",
                        "The Monadology",
                        "G. W. Leibniz",
                        "Monadology",
                        "Robert Latta",
                        "The whole Monadology (short)",
                        "Monadology §§1–90 (Latta)",
                        50,
                        "Simple substances without windows, mirroring the universe from a point of view; pre-established harmony instead of Descartes’ pineal traffic. "
                        "This is a complete metaphysical picture in a pamphlet. You will not ‘get’ every scholium. Get: why composites need simples, why monads cannot interact, how God chooses the best of possible worlds.",
                        [
                            "Why a monad has no windows (no genuine influx)",
                            "Perception and apperception — not all monads are minds like ours",
                            "Pre-established harmony as an alternative to occasionalism and to physical influx",
                        ],
                        [
                            "Is the best-possible-world claim a theodicy you can test, or a consequence of God’s definition?",
                            "How does this answer Spinoza’s one-substance claim without returning to Descartes’ two?",
                        ],
                        ["pascal-pensees"],
                        "Empiricism will ask how any of these systems could be known from experience.",
                        src(WS, "https://en.wikisource.org/wiki/Monadology_(Leibniz,_tr._Latta)", "complete", "Latta 1898; Wikisource"),
                        txt("leibniz-monadology", "Monadology, complete", "full"),
                    ),
                ],
            },
        ],
    }
