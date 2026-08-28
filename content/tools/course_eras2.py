"""Eras 2–4: classical, Hellenistic, late antiquity."""
from course_helpers import A, src, txt, PG, MIT, CCEL


def era_classical():
    return {
        "id": "ancient-classical",
        "order": 2,
        "title": "Socrates, Plato, Aristotle",
        "years": "c. 470–322 BCE",
        "intro": (
            "Socrates makes philosophy a way of testing a life in public. Plato writes that testing as drama, then builds a metaphysics of Forms "
            "to explain how we can know and how a city can be just. Aristotle refuses to let the Forms do that work from outside the world: "
            "substance, nature, and happiness have to be understood in things and in activity. By the end of this era you should be able to "
            "state what a Socratic question is, what the Cave is for, and what Aristotle means by eudaimonia and virtue — not as slogans."
        ),
        "themes": ["method", "justice", "knowledge", "substance", "happiness"],
        "units": [
            {
                "id": "socratic-method",
                "order": 1,
                "title": "The Socratic test",
                "professorNote": "Three short dialogues. Euthyphro is the method; Apology is the life; Crito is the political cost. Do not skip Euthyphro because it is about ‘piety’ — it is about definition.",
                "assignments": [
                    A(
                        "plato-euthyphro",
                        1,
                        "primary",
                        "Euthyphro: piety and definition",
                        "Plato",
                        "Euthyphro",
                        "Benjamin Jowett",
                        "The whole dialogue",
                        "Stephanus 2a–16a (complete)",
                        50,
                        "Euthyphro is sure he knows what piety is because he is prosecuting his father. Socrates asks for the form — the one thing by which pious acts are pious — "
                        "and every answer either names an example, or collapses into a circle (loved by the gods because pious, or pious because loved). "
                        "This is the Socratic move you will need for the rest of the course: a definition that can survive ‘why?’. "
                        "The famous fork — is it pious because the gods love it, or do they love it because it is pious? — is the ancestor of every later fight about whether value is will or intellect.",
                        [
                            "The demand for a single form, not a list of pious actions",
                            "The Euthyphro dilemma and which horn Euthyphro actually occupies",
                            "How the dialogue ends: aporia as a result, not an accident",
                        ],
                        [
                            "Why isn’t ‘what the gods love’ a definition even if it happens to be true of all pious things?",
                            "Does Socrates know what piety is, or only how to show that Euthyphro doesn’t?",
                        ],
                        ["atomists-leucippus"],
                        "Apology will show what this habit of questioning looks like when a city puts it on trial.",
                        src(PG, "https://www.gutenberg.org/ebooks/1642", "complete dialogue", "Jowett; PG #1642"),
                        txt("plato-euthyphro", "Stephanus 2a–16a", "full"),
                    ),
                    A(
                        "plato-apology",
                        2,
                        "primary",
                        "Apology: philosophy on trial",
                        "Plato",
                        "Apology",
                        "Benjamin Jowett",
                        "The whole speech",
                        "Stephanus 17a–42a (complete)",
                        60,
                        "Read this as a public argument about what a life of examination is worth. The oracle story is not autobiography for its own sake: it frames ignorance as a discipline. "
                        "Notice how Socrates distinguishes his old accusers (the comic reputation) from the formal charges, and how he refuses to beg. "
                        "The unexamined life line is cheap if you quote it; expensive if you ask what examination costs a city and a family. "
                        "Jowett is imperfect, but he is public domain and readable. Keep the Stephanus numbers in mind if you later compare a better translation.",
                        [
                            "What Socrates says he does not know — and what he claims to know about death and duty",
                            "The oracle, the cross-examination of politicians, poets, and craftsmen",
                            "Why he will not stop philosophizing even to save his life",
                        ],
                        [
                            "Is the claim of ignorance a method, a pose, or a moral stance?",
                            "What would it mean for a city to take his offer of a ‘penalty’ (free meals) seriously?",
                        ],
                        ["plato-euthyphro"],
                        "Crito asks whether the man who defied the jury should defy the laws by escaping.",
                        src(PG, "https://www.gutenberg.org/ebooks/1656", "complete", "Jowett; PG #1656"),
                        txt("plato-apology", "Stephanus 17a–42a", "full"),
                    ),
                    A(
                        "plato-crito",
                        3,
                        "primary",
                        "Crito: the laws and the just man",
                        "Plato",
                        "Crito",
                        "Benjamin Jowett",
                        "The whole dialogue",
                        "Stephanus 43a–54e (complete)",
                        45,
                        "Crito has money, friends, and a plan. Socrates answers with a personification of the Laws: you were free to leave; you stayed; escape would destroy the legal order you have used. "
                        "Whether or not you accept that argument, you now have an early social-contract claim on the table — and a severe thesis: one must not return injustice for injustice. "
                        "Read it against Apology. The same man who will not flatter a jury will not injure the city to save his skin.",
                        [
                            "The principle: never do injustice, even in return",
                            "The Laws’ speech: agreement, gratitude, persuasion-or-obedience",
                            "What counts as ‘destroying the laws’ by a single escape",
                        ],
                        [
                            "Does the Laws’ speech assume a consent Socrates never actually gave?",
                            "Can the Apology’s defiance of the jury be made consistent with Crito’s obedience to the laws?",
                        ],
                        ["plato-apology"],
                        "Meno turns the method on virtue and knowledge — and introduces recollection.",
                        src(PG, "https://www.gutenberg.org/ebooks/1657", "complete", "Jowett; PG #1657"),
                        txt("plato-crito", "Stephanus 43a–54e", "full"),
                    ),
                ],
            },
            {
                "id": "knowledge-and-virtue",
                "order": 2,
                "title": "Can virtue be taught?",
                "professorNote": "Meno is two sittings because the slave-boy demonstration and the distinction between knowledge and true belief are easy to rush. Do not rush them.",
                "assignments": [
                    A(
                        "plato-meno-inquiry",
                        1,
                        "primary",
                        "Meno: the paradox of inquiry and the slave",
                        "Plato",
                        "Meno",
                        "Benjamin Jowett",
                        "From the opening through the geometry lesson and the theory of recollection",
                        "Stephanus 70a–86c",
                        55,
                        "Meno wants a straight answer: can virtue be taught? Socrates wants a definition of virtue. Then the famous paradox: you cannot search for what you do not know, "
                        "because you would not recognize it. The slave-boy scene is not a math class. It is Plato’s first serious bid to explain how learning is possible — recollection, the soul’s prior acquaintance with truth. "
                        "You may reject recollection. You may not skip the problem it is trying to solve.",
                        [
                            "Meno’s first definitions and why they fail (lists, parts, not the whole)",
                            "The paradox of inquiry, stated carefully",
                            "What the slave is supposed to have shown: that he ‘recollected,’ not that he was taught in the ordinary sense",
                        ],
                        [
                            "Does the geometry lesson actually support recollection, or only that leading questions can elicit a proof?",
                            "Restate the paradox so that it is not a cheap trick.",
                        ],
                        ["plato-crito"],
                        "The second sitting: knowledge versus true opinion, and the political sting in the tail.",
                        src(PG, "https://www.gutenberg.org/ebooks/1643", "70a–86c", "Jowett; PG #1643"),
                        txt("plato-meno", "Stephanus 70a–86c", "full"),
                    ),
                    A(
                        "plato-meno-knowledge",
                        2,
                        "primary",
                        "Meno: knowledge, true belief, and virtue",
                        "Plato",
                        "Meno",
                        "Benjamin Jowett",
                        "From after the recollection episode to the end",
                        "Stephanus 86c–100b",
                        40,
                        "If virtue is knowledge, it should be teachable — but Athens has no teachers of virtue in the way it has teachers of horsemanship. "
                        "The distinction between knowledge and true opinion (the statues of Daedalus that run away unless tethered) is one of the most useful tools in the whole course. "
                        "Right opinion can guide action; it is not yet understanding. Watch how the dialogue’s political irony undercuts a simple ‘virtue is knowledge’ slogan.",
                        [
                            "Knowledge vs true opinion: the tethering image",
                            "Why the great Athenians could not teach their sons virtue",
                            "Whether the dialogue ends in a theory or in a deliberately unstable result",
                        ],
                        [
                            "If true opinion is as useful as knowledge for action, why prefer knowledge?",
                            "What would a teacher of virtue have to possess that a successful politician might lack?",
                        ],
                        ["plato-meno-inquiry"],
                        "The Republic will ask what justice is in a soul and a city — and will give you the Cave.",
                        src(PG, "https://www.gutenberg.org/ebooks/1643", "86c–100b", "Jowett; PG #1643"),
                        txt("plato-meno", "Stephanus 86c–100b", "full"),
                    ),
                ],
            },
            {
                "id": "justice-and-city",
                "order": 3,
                "title": "Justice, the soul, and the Cave",
                "professorNote": "Do not read the whole Republic. Read the argument about justice, then the metaphysics of education (sun, line, cave). That is the stretch that teaches the Platonic move.",
                "assignments": [
                    A(
                        "plato-republic-book-i",
                        1,
                        "primary",
                        "Republic I: three failed accounts of justice",
                        "Plato",
                        "Republic",
                        "Benjamin Jowett",
                        "Book I entire",
                        "Stephanus 327a–354c",
                        70,
                        "Book I is a Socratic demolition: Cephalus (paying debts, telling truth), Polemarchus (helping friends, harming enemies), Thrasymachus (the advantage of the stronger). "
                        "You need Thrasymachus in your bones before you meet Hobbes or Nietzsche. Socrates’ replies here are not yet the full theory of justice; they are the clearing of the site. "
                        "Notice that the book ends without a definition — on purpose.",
                        [
                            "Why ‘giving back what is owed’ fails (the madman’s weapon)",
                            "Thrasymachus: justice as another’s good; the tyrant as happy",
                            "Socrates’ arguments that the unjust life is not the stronger life — and where they feel thin",
                        ],
                        [
                            "State Thrasymachus’s position so that it is as strong as you can make it.",
                            "Has Socrates refuted ‘might makes right,’ or only a sloppy version of it?",
                        ],
                        ["plato-meno-knowledge"],
                        "Books II–IV will rebuild justice as a structure in city and soul.",
                        src(PG, "https://www.gutenberg.org/ebooks/55201", "Book I", "Jowett 3rd ed. with Stephanus; PG #55201"),
                        txt("plato-republic", "Republic Book I, 327–354", "excerpt", "book-i", "book-i"),
                    ),
                    A(
                        "plato-republic-soul-city",
                        2,
                        "primary",
                        "Republic II and IV: city, soul, the virtues",
                        "Plato",
                        "Republic",
                        "Benjamin Jowett",
                        "Glaucon’s challenge; the origin of the city; the four virtues in the city; justice in the soul (Book IV)",
                        "Stephanus 357a–367e (Glaucon/Adeimantus); then 427d–445e (virtues in city and soul). You may skim the long city-founding middle of II–III.",
                        75,
                        "Glaucon’s Gyges ring is the adult version of Thrasymachus: why be just if you can be unjust without cost? "
                        "Plato’s strategy is analogical — justice writ large in a city, then in a soul with three parts. "
                        "The payoff in Book IV: justice as each part doing its work, in city and in soul. You do not need the censorship arguments of Book III for this course; you need the structure.",
                        [
                            "Glaucon’s threefold classification of goods and where he places justice",
                            "The three parts of the soul and their civic counterparts",
                            "Justice as a structural relation, not a list of actions",
                        ],
                        [
                            "Does the city-soul analogy prove anything, or only illustrate a hypothesis?",
                            "If justice is psychic order, what happens to justice as a relation to other people?",
                        ],
                        ["plato-republic-book-i"],
                        "Now the Cave: what education is, if the soul has parts and the world has levels.",
                        src(PG, "https://www.gutenberg.org/ebooks/55201", "II 357–367; IV 427–445", "Jowett; PG #55201"),
                        txt("plato-republic", "Books II and IV selections", "excerpt", "book-ii", "book-iv"),
                    ),
                    A(
                        "plato-republic-cave",
                        3,
                        "primary",
                        "Sun, line, and Cave",
                        "Plato",
                        "Republic",
                        "Benjamin Jowett",
                        "The Good as sun; the divided line; the Cave and the return",
                        "Stephanus 506b–521b (end of VI through the Cave and the philosopher’s return)",
                        60,
                        "This is the image everyone knows and almost no one reads slowly. The sun is not a pretty metaphor for ‘enlightenment.’ It is a claim about what makes knowable things knowable — the Good. "
                        "The line ranks images, sensibles, mathematical thought, and dialectic. The Cave is a story about education as turning, and about the political cost of returning to the prisoners. "
                        "You now have Plato’s epistemology and his politics in one stretch. That is enough Republic.",
                        [
                            "What the sun is supposed to do for sight and generation — analogically, what the Good does for knowledge and being",
                            "The four segments of the line, with an example in each",
                            "Why the released prisoner is compelled to go back down",
                        ],
                        [
                            "Is the Cave a theory of knowledge, a theory of politics, or a theory of conversion — and can it be all three without confusion?",
                            "What would it mean to ‘look at the sun’ without Plato’s Forms?",
                        ],
                        ["plato-republic-soul-city"],
                        "Aristotle will try to explain being and change without a separate realm of Forms.",
                        src(PG, "https://www.gutenberg.org/ebooks/55201", "506b–521b", "Jowett; PG #55201"),
                        txt("plato-republic", "Republic 506b–521b (sun, line, cave)", "excerpt", "book-vi", "book-vii"),
                    ),
                ],
            },
            {
                "id": "aristotle-nature",
                "order": 4,
                "title": "Substance, nature, and causes",
                "professorNote": "Two sittings: how to say what a thing is (Categories), then how change is possible without Parmenides’ contradiction (Physics II).",
                "assignments": [
                    A(
                        "aristotle-categories-substance",
                        1,
                        "primary",
                        "Categories 1–5: substance",
                        "Aristotle",
                        "Categories",
                        "E. M. Edghill",
                        "Chapters 1–5",
                        "Categories 1–5 (especially ch. 5 on primary substance)",
                        50,
                        "Before ethics, you need Aristotle’s grammar of being. Things are said in many ways, but not chaotically: there are categories. "
                        "Primary substance — this horse, this human — is the subject that qualities inhere in. That is a decision against treating universals as more real than the animals in front of you. "
                        "If you later hear ‘substance’ in Descartes or Locke, this is the ancestor they are rewriting.",
                        [
                            "Homonyms, synonyms, paronyms — why the opening is not pedantry",
                            "Primary vs secondary substance",
                            "Why substance is ‘neither said of a subject nor in a subject’",
                        ],
                        [
                            "What is lost if we treat ‘human’ as more real than Socrates?",
                            "How is this already a reply to a certain reading of Plato’s Forms?",
                        ],
                        ["plato-republic-cave"],
                        "Physics II will add nature, matter/form, and the four causes.",
                        src(PG, "https://www.gutenberg.org/ebooks/2412", "chs. 1–5", "Edghill; PG #2412"),
                        txt("aristotle-categories", "Categories 1–5", "excerpt", "cat-1", "cat-5"),
                    ),
                    A(
                        "aristotle-physics-nature",
                        2,
                        "primary",
                        "Physics II: nature and the four causes",
                        "Aristotle",
                        "Physics",
                        "R. P. Hardie and R. K. Gaye",
                        "Book II, chapters 1–3 (nature; four causes)",
                        "Physics II.1–3 (Bekker 192b–195b)",
                        50,
                        "Nature is an inner principle of motion and rest — not a nickname for ‘everything.’ The four causes (material, formal, efficient, final) are not a dusty list; "
                        "they are four answers to ‘why?’ that Parmenides and the atomists each tried to collapse. Final cause will offend you if you think modern physics. "
                        "Read it as a claim about living things and artifacts first. You need this for Aquinas later, and for every later fight about teleology.",
                        [
                            "Nature vs art: the difference between growing and being built",
                            "The four ‘becauses,’ with one example that uses all four",
                            "Why chance is not a fifth kind of cause on a par with these",
                        ],
                        [
                            "Can you explain a tree without a ‘that for the sake of which’?",
                            "How does form-in-matter let Aristotle keep change without Parmenides’ contradiction?",
                        ],
                        ["aristotle-categories-substance"],
                        "Ethics: what the human ergon is, and what a virtue is.",
                        src(MIT, "https://classics.mit.edu/Aristotle/physics.2.ii.html", "Physics II.1–3", "Hardie & Gaye; MIT Classics"),
                        txt("aristotle-physics", "Physics Book II", "excerpt", "phys-ii", "phys-ii"),
                    ),
                ],
            },
            {
                "id": "aristotle-ethics-first-philosophy",
                "order": 5,
                "title": "Happiness, virtue, wisdom",
                "professorNote": "Three sittings, not a survey of the corpus. Happiness and virtue first; then a sliver of Metaphysics so ‘first philosophy’ is not a rumor; then demonstration so you see what Aristotle thinks knowledge is.",
                "assignments": [
                    A(
                        "aristotle-ne-happiness",
                        1,
                        "primary",
                        "Nicomachean Ethics I: happiness",
                        "Aristotle",
                        "Nicomachean Ethics",
                        "W. D. Ross",
                        "Book I, especially I.1–7 (the good, eudaimonia, the function argument)",
                        "NE I.1–I.7 (Bekker 1094a–1098b); skim I.8–13 if you have time",
                        60,
                        "Every craft aims at some good; the highest good for a human life is eudaimonia — not a mood, but a complete activity of the soul in accordance with virtue. "
                        "The function argument is the hinge: if a human has an ergon, it has to do with reason. You may reject the idea that humans have a function. "
                        "You must first hear it as Aristotle states it, not as a later sermon about ‘purpose.’",
                        [
                            "The difference between eudaimonia and pleasure, honor, or money",
                            "The function (ergon) argument, premise by premise",
                            "Why a complete life is required — why one swallow does not make a spring",
                        ],
                        [
                            "What is eudaimonia, on this account, in words you would use of a living person?",
                            "Why does Aristotle think a human has a function at all?",
                        ],
                        ["aristotle-physics-nature"],
                        "Book II: virtue as a mean in the soul’s habits.",
                        src(MIT, "https://classics.mit.edu/Aristotle/nicomachaen.1.i.html", "NE I", "Ross; MIT Classics"),
                        txt("aristotle-nicomachean-ethics", "NE Book I", "excerpt", "ne-i", "ne-i"),
                    ),
                    A(
                        "aristotle-ne-virtue",
                        2,
                        "primary",
                        "Nicomachean Ethics II: moral virtue",
                        "Aristotle",
                        "Nicomachean Ethics",
                        "W. D. Ross",
                        "Book II entire (virtue as habit; the mean)",
                        "NE II (1103a–1109b)",
                        55,
                        "Virtue is not a feeling and not a mere capacity. It is a hexis — a stable disposition — formed by action, aiming at a mean relative to us, defined by reason as the prudent person would define it. "
                        "The mean is not mediocrity; it is hitting the mark in fear, anger, giving, truth-telling. "
                        "This is the ethics the Stoics will radicalize and Kant will refuse to found on habit.",
                        [
                            "Why virtues of character are acquired by habituation",
                            "The mean ‘relative to us’ — not a geometric midpoint",
                            "The list of virtues as a map of situations, not a personality test",
                        ],
                        [
                            "Can a person know the mean and still not be virtuous? What is missing?",
                            "Pick one virtue and say what the two vices are — and why the mean is not ‘being moderate about everything.’",
                        ],
                        ["aristotle-ne-happiness"],
                        "A short look at first philosophy, then demonstration — so ethics is not floating free of Aristotle’s idea of knowledge.",
                        src(MIT, "https://classics.mit.edu/Aristotle/nicomachaen.2.ii.html", "NE II", "Ross; MIT Classics"),
                        txt("aristotle-nicomachean-ethics", "NE Book II", "excerpt", "ne-ii", "ne-ii"),
                    ),
                    A(
                        "aristotle-metaphysics-wisdom",
                        3,
                        "primary",
                        "Metaphysics: wonder, wisdom, being qua being",
                        "Aristotle",
                        "Metaphysics",
                        "W. D. Ross",
                        "I.1–2 (wisdom, experience, wonder) and IV.1–2 (being qua being; focal meaning)",
                        "Metaphysics I.1–2 (980a–983a) and IV.1–2 (1003a–1004a)",
                        50,
                        "All humans by nature desire to know. Wisdom is knowledge of first causes and principles. Book IV then names the science that studies being insofar as it is being — not numbers, not nature in motion, but what it is to be. "
                        "‘Being is said in many ways’ but not as a heap of homonyms: there is a focal meaning around substance. "
                        "This sliver is enough to make later ontology recognizable.",
                        [
                            "The ladder: sensation, memory, experience, art, wisdom",
                            "Why first philosophy is not physics",
                            "Focal meaning: how ‘healthy’ helps explain how ‘being’ is said in many ways",
                        ],
                        [
                            "What would it mean to study being without studying some particular kind of being?",
                            "How does this continue, and refuse, the Cave’s ranking of knowledge?",
                        ],
                        ["aristotle-ne-virtue"],
                        "Posterior Analytics: what a demonstration is, and why not everything can be demonstrated.",
                        src(MIT, "https://classics.mit.edu/Aristotle/metaphysics.1.i.html", "Met. I.1–2; IV.1–2", "Ross; MIT Classics"),
                        txt("aristotle-metaphysics", "Metaphysics I and IV (openings)", "excerpt", "met-i", "met-iv"),
                    ),
                    A(
                        "aristotle-posterior-analytics",
                        4,
                        "primary",
                        "Posterior Analytics I.1–3: demonstration and first principles",
                        "Aristotle",
                        "Posterior Analytics",
                        "G. R. G. Mure",
                        "Book I, chapters 1–3",
                        "APo I.1–3 (71a–73a)",
                        40,
                        "You cannot demonstrate everything: some things are first. Knowledge of a conclusion is through demonstration; the principles are known another way (nous, induction). "
                        "This is the ancestor of every later fight about foundations — Descartes’ clear and distinct ideas, Hume’s missing impression, Moore’s intuitions. "
                        "Read it as a constraint: a science has a shape, and infinite regress is not a shape.",
                        [
                            "What a demonstration is (syllogism from true, primary, immediate premises)",
                            "The regress problem if every premise must itself be demonstrated",
                            "The difference between knowing that and knowing why",
                        ],
                        [
                            "If first principles are not demonstrated, how are they more than prejudices?",
                            "What would Hume say is missing from this picture of knowledge?",
                        ],
                        ["aristotle-metaphysics-wisdom"],
                        "The schools after Aristotle will treat philosophy as a way of life under empire — starting with Epicurus.",
                        src(MIT, "https://classics.mit.edu/Aristotle/posteri.1.i.html", "APo I.1–3", "Mure; MIT Classics"),
                        txt("aristotle-posterior-analytics", "Posterior Analytics I.1–3", "excerpt", "pa-i", "pa-i"),
                    ),
                ],
            },
        ],
    }
