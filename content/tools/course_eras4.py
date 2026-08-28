"""Eras 7–11: empiricism through the present-day bridge."""
from course_helpers import A, src, txt, PG, MIT
from course_eras3 import bib


def era_empiricism():
    return {
        "id": "empiricism",
        "order": 7,
        "title": "Empiricism and the new science",
        "years": "1651–1779",
        "intro": (
            "If all knowledge comes from experience, what happens to innate ideas, substance, causation, the self, and God? "
            "Hobbes builds a politics from bodies in motion; Locke fills the blank slate and then a theory of property and consent; "
            "Berkeley removes matter; Hume wakes Kant. This era is the pressure test of Descartes’ rationalism."
        ),
        "themes": ["experience", "causation", "person", "sovereignty"],
        "units": [
            {
                "id": "political-bodies",
                "order": 1,
                "title": "Bodies, fear, and property",
                "professorNote": "Hobbes and Locke disagree about the state of nature and about what a sovereign is for. Read them as a pair.",
                "assignments": [
                    A(
                        "hobbes-state-of-nature",
                        1,
                        "primary",
                        "Leviathan 13–14: the natural condition",
                        "Thomas Hobbes",
                        "Leviathan",
                        "n/a (English original)",
                        "Chapters 13–14",
                        "Leviathan chs. 13–14",
                        45,
                        "Without a common power, life is a war of all against all — not because people are cartoon villains, but because equality of vulnerability plus the right of nature (to everything needful for life) makes preemptive violence rational. "
                        "The first two natural laws: seek peace; be willing to lay down liberty when others do, in a contract. "
                        "This is Machiavelli’s honesty turned into a science of bodies.",
                        [
                            "Why equality, not monstrous vice, drives the war",
                            "The right of nature versus the law of nature",
                            "What a covenant is, and why it needs a sword",
                        ],
                        [
                            "Is the state of nature a history, a thought experiment, or a warning about civil war?",
                            "Can there be injustice before a sovereign, on this account?",
                        ],
                        ["leibniz-monadology"],
                        "Chapters 17–21: the generation of the commonwealth and the liberty that remains.",
                        src(PG, "https://www.gutenberg.org/ebooks/3207", "chs. 13–14", "1651; PG #3207"),
                        txt("hobbes-leviathan", "Chapters XIII–XIV", "excerpt", "ch-13", "ch-14"),
                    ),
                    A(
                        "hobbes-sovereign",
                        2,
                        "primary",
                        "Leviathan 17–21: the mortal god",
                        "Thomas Hobbes",
                        "Leviathan",
                        "n/a (English original)",
                        "Chapters 17–18 and 21",
                        "Leviathan chs. 17–18, 21 (18 is in the hosted stretch toward 21)",
                        50,
                        "The commonwealth is generated when authorization creates an artificial person. The sovereign is not a party to the covenant in the way subjects are. "
                        "Liberty of subjects is the silence of the law — and the inalienable right to defend one’s life. "
                        "Locke will deny that you can consent to arbitrary power. Keep Hobbes’s claim sharp so the denial has an object.",
                        [
                            "Authorization and the artificial person",
                            "Why the sovereign is not bound as a fellow covenanter",
                            "The remaining liberty: self-defense, and gaps in law",
                        ],
                        [
                            "Is this absolutism, or a theory of the minimum conditions of peace?",
                            "Where does Hobbes leave room, if any, for resistance?",
                        ],
                        ["hobbes-state-of-nature"],
                        "Locke: property in the state of nature, before government.",
                        src(PG, "https://www.gutenberg.org/ebooks/3207", "chs. 17–21", "PG #3207"),
                        txt("hobbes-leviathan", "Chapters XVII–XXI", "excerpt", "ch-17", "ch-21"),
                    ),
                    A(
                        "locke-property",
                        3,
                        "primary",
                        "Second Treatise V: property",
                        "John Locke",
                        "Second Treatise of Government",
                        "n/a (English original)",
                        "Chapter V, with II (state of nature) as frame; glance at XIX on dissolution",
                        "Second Treatise chs. II, V, and XIX as hosted",
                        50,
                        "The state of nature already has law (reason), not Hobbes’s war. Property begins in the person, then in mixing labor with what is common, limited by spoilage and enough-and-as-good. "
                        "Money later relaxes the spoilage limit — a hinge many readers miss. Chapter XIX: government dissolves when it betrays trust. "
                        "This is the ancestor of liberal revolution and of later critiques of accumulation.",
                        [
                            "Labor-mixing as a title, and the two provisos",
                            "What money does to the original limits",
                            "Dissolution versus Hobbesian authorization that cannot be withdrawn",
                        ],
                        [
                            "Does ‘enough and as good’ still hold after money?",
                            "What makes Locke’s state of nature not already a government?",
                        ],
                        ["hobbes-sovereign"],
                        "Now Locke’s Essay: where ideas come from.",
                        src(PG, "https://www.gutenberg.org/ebooks/7370", "chs. II, V, XIX", "PG #7370"),
                        txt("locke-second-treatise", "chs. II, V, XIX", "excerpt", "ch-2", "ch-19"),
                    ),
                ],
            },
            {
                "id": "ideas-and-qualities",
                "order": 2,
                "title": "Ideas, qualities, minds",
                "professorNote": "Locke’s epistemology, then Berkeley’s shock. Hume will finish the demolition of necessary connection.",
                "assignments": [
                    A(
                        "locke-no-innate",
                        1,
                        "primary",
                        "Essay I: against innate principles",
                        "John Locke",
                        "An Essay Concerning Human Understanding",
                        "n/a (English original)",
                        "Book I, especially chs. 1–2",
                        "Essay Book I (hosted: I.2 onward in the file’s sections)",
                        45,
                        "No innate speculative or practical principles. Universal consent is a bad test, and children and ‘idiots’ are a better one. "
                        "The mind begins as white paper. This is the charter of British empiricism. Descartes’ innate idea of God is in the dock.",
                        [
                            "Why universal consent would not prove innateness even if it existed",
                            "The appeal to those who have not learned the supposed maxims",
                            "What ‘white paper’ does and does not mean (not: no faculties)",
                        ],
                        [
                            "Could a disposition to form an idea be innate even if the idea is not?",
                            "What happens to morality if there are no innate practical principles?",
                        ],
                        ["locke-property"],
                        "Book II: simple ideas, and primary vs secondary qualities.",
                        src(PG, "https://www.gutenberg.org/ebooks/10615", "Book I", "PG #10615"),
                        txt("locke-essay", "Book I", "excerpt", "i-2", "i-2"),
                    ),
                    A(
                        "locke-qualities",
                        2,
                        "primary",
                        "Essay II.8: primary and secondary qualities",
                        "John Locke",
                        "An Essay Concerning Human Understanding",
                        "n/a (English original)",
                        "Book II, ch. 8 (and enough of II.1 to see sensation and reflection)",
                        "Essay II.1 and II.8",
                        45,
                        "Ideas come from sensation and reflection. Primary qualities (bulk, figure, motion) are in bodies; secondary (color, sound, taste) are powers to produce ideas in us. "
                        "This is the corpuscular world meeting the mind. Berkeley will say the distinction cannot be maintained. "
                        "Get Locke’s distinction clean before the attack.",
                        [
                            "Sensation vs reflection as the two fountains",
                            "Primary qualities as inseparable from body",
                            "Secondary qualities as powers — not nothing, but not ‘in the object’ as yellow is in the idea",
                        ],
                        [
                            "If color is a power, is the world colorless when unobserved, on Locke’s view?",
                            "What problem about resemblance (idea resembling quality) is already visible?",
                        ],
                        ["locke-no-innate"],
                        "Berkeley: to be is to be perceived.",
                        src(PG, "https://www.gutenberg.org/ebooks/10615", "II.1, II.8", "PG #10615"),
                        txt("locke-essay", "II.1 and II.8", "excerpt", "ii-1", "ii-8"),
                    ),
                    A(
                        "berkeley-principles",
                        3,
                        "primary",
                        "Berkeley: Principles, opening",
                        "George Berkeley",
                        "A Treatise Concerning the Principles of Human Knowledge",
                        "n/a (English original)",
                        "Introduction and §§1–33",
                        "Principles, Introduction and opening sections (as hosted)",
                        50,
                        "Abstract general ideas are a Lockean fiction that makes skepticism inevitable. Ordinary objects are collections of ideas. "
                        "Matter as an unthinking substance behind ideas is unnecessary and unintelligible. God sustains the order of ideas. "
                        "This is not ‘everything is a dream.’ It is an attempt to save common sense and science without material substance.",
                        [
                            "The attack on abstract general ideas",
                            "What an apple is, if it is a collection of ideas",
                            "Why matter is said to do no explanatory work",
                        ],
                        [
                            "Does Berkeley abolish the external world, or only a philosopher’s extra object?",
                            "What role must God play if ideas persist when you leave the room?",
                        ],
                        ["locke-qualities"],
                        "Hume: causation as custom, not insight into necessity.",
                        src(PG, "https://www.gutenberg.org/ebooks/4723", "Intro + §§1–33", "PG #4723"),
                        txt("berkeley-principles", "Introduction and opening principles", "excerpt", "intro-main", "intro-main"),
                    ),
                ],
            },
            {
                "id": "hume-mitigated",
                "order": 3,
                "title": "Hume’s mitigated skepticism",
                "professorNote": "Five sittings. Causation and induction first; then miracles; then the self; then design. This is the engine room of later philosophy.",
                "assignments": [
                    A(
                        "hume-enquiry-ideas",
                        1,
                        "primary",
                        "Enquiry II and IV: ideas and induction",
                        "David Hume",
                        "An Enquiry Concerning Human Understanding",
                        "n/a (English original)",
                        "Sections II and IV",
                        "Enquiry sec. 2 (origin of ideas) and sec. 4 (sceptical doubts)",
                        50,
                        "All ideas copy impressions (with a famous missing-shade exception). Relations of ideas vs matters of fact. "
                        "Matters of fact rest on cause and effect; cause and effect are not known a priori; the inference from past to future is not demonstrative. "
                        "This is the problem of induction. If you only remember the slogan, you have not read Section IV.",
                        [
                            "The copy principle, and why the missing shade matters",
                            "Relations of ideas vs matters of fact",
                            "Why the future resembling the past is not a demonstration",
                        ],
                        [
                            "Is the missing shade a counterexample, or a curiosity he can isolate?",
                            "What would a ‘justification’ of induction have to look like, if Hume is right about the options?",
                        ],
                        ["berkeley-principles"],
                        "Sections V and VII: custom, and the idea of necessary connection.",
                        src(PG, "https://www.gutenberg.org/ebooks/9662", "secs. 2, 4", "PG #9662"),
                        txt("hume-enquiry", "Sections II and IV", "excerpt", "sec-2", "sec-4"),
                    ),
                    A(
                        "hume-enquiry-causation",
                        2,
                        "primary",
                        "Enquiry V and VII: custom and necessity",
                        "David Hume",
                        "An Enquiry Concerning Human Understanding",
                        "n/a (English original)",
                        "Sections V and VII",
                        "Enquiry sec. 5 (sceptical solution) and sec. 7 (necessary connexion)",
                        50,
                        "Custom or habit is the skeptical solution: we believe, we are not compelled by insight. Necessary connection is not an impression in the objects; "
                        "it is the mind’s feeling in the transition. This is the sentence Kant said woke him. "
                        "Read VII until you can say what is missing when you look at one billiard ball.",
                        [
                            "Custom as the guide of life — not a new demonstration",
                            "The hunt for the impression of necessity",
                            "Two definitions of cause (regularity vs the mind’s determination)",
                        ],
                        [
                            "Does Hume deny causation, or deny a certain idea of it?",
                            "If necessity is in the mind, why does science still work?",
                        ],
                        ["hume-enquiry-ideas"],
                        "Miracles, then personal identity, then design.",
                        src(PG, "https://www.gutenberg.org/ebooks/9662", "secs. 5, 7", "PG #9662"),
                        txt("hume-enquiry", "Sections V and VII", "excerpt", "sec-5", "sec-7"),
                    ),
                    A(
                        "hume-enquiry-miracles",
                        3,
                        "primary",
                        "Enquiry X: of miracles",
                        "David Hume",
                        "An Enquiry Concerning Human Understanding",
                        "n/a (English original)",
                        "Section X",
                        "Enquiry sec. 10",
                        40,
                        "A miracle is a violation of the laws of nature. The wise man proportions belief to evidence. Testimony for a miracle must outweigh the uniform experience that constitutes the law — "
                        "and in practice it never does, given the passions of religion and the love of wonder. "
                        "This is a rule of historical method, not a proof that God cannot act.",
                        [
                            "The definition of miracle via laws of nature",
                            "Why testimony is structurally weaker here than in ordinary history",
                            "The practical maxim, as opposed to a metaphysical ban",
                        ],
                        [
                            "Does the argument beg the question by assuming the laws cannot be violated?",
                            "What would Hume say about a miracle you yourself seemed to see?",
                        ],
                        ["hume-enquiry-causation"],
                        "The self as a bundle: Treatise I.4.6.",
                        src(PG, "https://www.gutenberg.org/ebooks/9662", "sec. 10", "PG #9662"),
                        txt("hume-enquiry", "Section X", "excerpt", "sec-10", "sec-10"),
                    ),
                    A(
                        "hume-treatise-identity",
                        4,
                        "primary",
                        "Treatise I.4.6: personal identity",
                        "David Hume",
                        "A Treatise of Human Nature",
                        "n/a (English original)",
                        "Book I, Part 4, Section 6",
                        "Treatise I.4.6",
                        40,
                        "There is no impression of a simple, continuing self. The mind is a bundle of perceptions in flux, tied by memory and association. "
                        "Identity is a fiction we substitute, as with a republic or a river. Locke’s forensic person is in trouble — or at least his supporting soul-substance is. "
                        "This sitting is short and dense. Reread the bundle image until it is not a meme.",
                        [
                            "The failed search for a constant impression of self",
                            "The bundle (or theatre) image — and its limits",
                            "Memory’s role in the fiction of identity",
                        ],
                        [
                            "If there is no self, who is worried about personal identity?",
                            "Does Hume explain the feeling of identity, or explain it away?",
                        ],
                        ["hume-enquiry-miracles"],
                        "Dialogues: design, evil, and the limits of natural religion.",
                        src(PG, "https://www.gutenberg.org/ebooks/4705", "I.4.6", "PG #4705"),
                        txt("hume-treatise", "I.4.6 personal identity", "excerpt", "i-4-6", "i-4-6"),
                    ),
                    A(
                        "hume-dialogues-design",
                        5,
                        "primary",
                        "Dialogues II, X–XI: design and evil",
                        "David Hume",
                        "Dialogues Concerning Natural Religion",
                        "n/a (English original)",
                        "Parts II, X, and XI",
                        "Dialogues Parts II, X–XI",
                        50,
                        "Cleanthes’ design argument from the world’s machine-like order; Philo’s analogical doubts (why this designer, why not a team, a juvenile god, a vegetable). "
                        "Then evil: the world’s misery as evidence against a morally perfect author, or at least against our analogical theology. "
                        "You are watching natural religion come apart without a cheap atheist’s victory lap. Note who speaks last, and do not over-identify Hume with one voice.",
                        [
                            "The analogical structure of the design argument",
                            "Philo’s competing analogies",
                            "The problem of evil as a constraint on what we may infer about the cause of the world",
                        ],
                        [
                            "Does Philo refute design, or only our right to a particular picture of the designer?",
                            "After Parts X–XI, what if anything remains of ‘natural religion’?",
                        ],
                        ["hume-treatise-identity"],
                        "Political and moral Enlightenment: Rousseau, Smith, then Kant’s answer to Hume.",
                        src(PG, "https://www.gutenberg.org/ebooks/4583", "Parts II, X–XI", "PG #4583"),
                        txt("hume-dialogues", "Parts II, X–XI", "excerpt", "part-2", "part-11"),
                    ),
                ],
            },
        ],
    }


def era_enlightenment():
    return {
        "id": "enlightenment",
        "order": 8,
        "title": "Enlightenment politics and the Copernican turn",
        "years": "1755–1788",
        "intro": (
            "Rousseau relocates legitimacy in the general will; Smith explains moral judgment through the impartial spectator; "
            "Kant answers Hume by turning the question around: objects conform to our forms of intuition and categories, and morality is autonomy under a universal law. "
            "You do not need the whole Critique. You need the turn, and the Groundwork’s formulas."
        ),
        "themes": ["general will", "autonomy", "a priori", "duty"],
        "units": [
            {
                "id": "freedom-and-sympathy",
                "order": 1,
                "title": "Freedom, the general will, sympathy",
                "professorNote": "Rousseau’s diagnosis and his contract, then Smith’s moral psychology — a different Enlightenment than Kant’s.",
                "assignments": [
                    A(
                        "rousseau-inequality",
                        1,
                        "primary",
                        "Discourse on Inequality, Part I",
                        "Jean-Jacques Rousseau",
                        "Discourse on the Origin of Inequality",
                        "G. D. H. Cole",
                        "Part I (natural man)",
                        "Second Discourse, Part I (Cole)",
                        50,
                        "Natural man is not Hobbes’s combatant. Pity, limited needs, and the absence of amour-propre come first; inequality as we know it is a social product. "
                        "This is a conjectural history in the service of a moral claim: we have made ourselves miserable by institutions we take as nature. "
                        "The Social Contract will try to name a legitimate bond.",
                        [
                            "Natural vs social inequality",
                            "Amour de soi versus amour-propre (as the Discourse sets them up)",
                            "Why ‘state of nature’ here is not a lost paradise you could return to by camping",
                        ],
                        [
                            "Is this anthropology, or a mirror held up to Paris?",
                            "What in Hobbes is being refused at the root?",
                        ],
                        ["hume-dialogues-design"],
                        "Social Contract I: the problem of legitimate authority.",
                        src(PG, "https://www.gutenberg.org/ebooks/46333", "Inequality Part I", "Cole; PG #46333"),
                        txt("rousseau-contract-discourses", "Discourse Part I", "excerpt", "inequality-1", "inequality-1"),
                    ),
                    A(
                        "rousseau-contract-i",
                        2,
                        "primary",
                        "Social Contract I: born free",
                        "Jean-Jacques Rousseau",
                        "The Social Contract",
                        "G. D. H. Cole",
                        "Book I",
                        "Social Contract Book I",
                        45,
                        "Man is born free, and everywhere in chains. The problem: find a form of association that defends each with the force of all, while each obeys only himself. "
                        "The solution named: the social compact, alienation of rights to the whole, the general will. "
                        "Force is not right. Slavery cannot be made legitimate by conquest. This is the Enlightenment’s most explosive pamphlet-length politics.",
                        [
                            "Why right cannot be reduced to force",
                            "The compact’s exchange: natural liberty for civil liberty",
                            "The general will as what the compact creates, not a poll of private interests",
                        ],
                        [
                            "Can you ‘obey only yourself’ after alienating your rights to the community?",
                            "What is the difference between the general will and the will of all?",
                        ],
                        ["rousseau-inequality"],
                        "Book II: law, the legislator, the people.",
                        src(PG, "https://www.gutenberg.org/ebooks/46333", "Book I", "Cole; PG #46333"),
                        txt("rousseau-contract-discourses", "Social Contract Book I", "excerpt", "contract-i", "contract-i"),
                    ),
                    A(
                        "rousseau-contract-ii",
                        3,
                        "primary",
                        "Social Contract II: law and the legislator",
                        "Jean-Jacques Rousseau",
                        "The Social Contract",
                        "G. D. H. Cole",
                        "Book II",
                        "Social Contract Book II",
                        45,
                        "Sovereignty is inalienable and indivisible. Law is the register of the general will. The legislator is a paradoxical figure: he founds a people that cannot yet found itself. "
                        "This is where later readers smell danger (the people forced to be free) and where others hear the only serious alternative to representation-as-private-interest. "
                        "Read the danger and the hope in the same pages.",
                        [
                            "Inalienability of sovereignty",
                            "What a law must look like to be general",
                            "The legislator’s problem: wisdom without authority of the ordinary kind",
                        ],
                        [
                            "Is ‘forced to be free’ a contradiction, a threat, or a theory of education into citizenship?",
                            "Could this work in a large commercial state, on Rousseau’s own terms?",
                        ],
                        ["rousseau-contract-i"],
                        "Smith: moral judgment without a general will.",
                        src(PG, "https://www.gutenberg.org/ebooks/46333", "Book II", "Cole; PG #46333"),
                        txt("rousseau-contract-discourses", "Social Contract Book II", "excerpt", "contract-ii", "contract-ii"),
                    ),
                    A(
                        "smith-moral-sentiments",
                        4,
                        "primary",
                        "Smith: sympathy and the impartial spectator",
                        "Adam Smith",
                        "The Theory of Moral Sentiments",
                        "n/a (English original)",
                        "Part I, Section I",
                        "TMS I.i (propriety, sympathy)",
                        45,
                        "We judge by sympathy: changing places in fancy with the other, and watching whether passions match. "
                        "The impartial spectator is the internalized other who corrects self-love. This is a moral psychology for commercial society that is not Hobbesian fear and not Rousseau’s general will. "
                        "Philosophy of economics later split Smith in two; you are reading the moralist first.",
                        [
                            "Sympathy as imaginative exchange, not pity only",
                            "Propriety as a mean of passion relative to the spectator",
                            "How the impartial spectator is supposed to arise",
                        ],
                        [
                            "Can an impartial spectator ever be more than my culture’s average gaze?",
                            "What would Kant say is missing if morality is a sentiment of propriety?",
                        ],
                        ["rousseau-contract-ii"],
                        "Kant: the Copernican turn.",
                        src(PG, "https://www.gutenberg.org/ebooks/67363", "TMS I.i", "PG #67363"),
                        txt("smith-tms", "Part I, Section I", "excerpt", "i-i", "i-i"),
                    ),
                ],
            },
            {
                "id": "kant-copernican",
                "order": 2,
                "title": "Kant’s Copernican turn",
                "professorNote": "Prefaces and Introduction of the first Critique. That is the turn. The Groundwork then does morals without swallowing the whole second Critique.",
                "assignments": [
                    A(
                        "kant-cpr-prefaces",
                        1,
                        "primary",
                        "CPR: Prefaces A and B, Introduction",
                        "Immanuel Kant",
                        "Critique of Pure Reason",
                        "J. M. D. Meiklejohn",
                        "Preface to the first edition, Preface to the second, Introduction",
                        "CPR Prefaces A & B; Introduction (Meiklejohn)",
                        70,
                        "Metaphysics has been a battlefield. Hume interrupted dogmatic slumber: if causation is not read off the world, how is necessary science possible? "
                        "The Copernican hypothesis: objects conform to our way of knowing, not the reverse. Synthetic a priori judgments become the question. "
                        "The Aesthetic is folded into this sitting via the Introduction’s claim that space and time are the forms of sensibility — if your hosted file’s ‘intro’ stretch includes that turn, stay with it; if not, the Prefaces already name the hypothesis you must be able to state.",
                        [
                            "What the Copernican analogy is supposed to change in the method of metaphysics",
                            "Analytic vs synthetic; a priori vs a posteriori — four boxes, one famous problem",
                            "Why Hume on causation is the provocation, not a side remark",
                        ],
                        [
                            "State the Copernican turn without the word ‘Copernican.’",
                            "What is lost if we never get to things in themselves — and what Kant thinks is gained?",
                        ],
                        ["smith-moral-sentiments"],
                        "Groundwork: the moral law as autonomy.",
                        src(PG, "https://www.gutenberg.org/ebooks/4280", "Prefaces and Introduction", "Meiklejohn; PG #4280"),
                        txt("kant-cpr", "Prefaces A/B and Introduction", "excerpt", "preface-a", "intro"),
                    ),
                    A(
                        "kant-groundwork-i",
                        2,
                        "primary",
                        "Groundwork I: good will and duty",
                        "Immanuel Kant",
                        "Fundamental Principles of the Metaphysic of Morals",
                        "Thomas Kingsmill Abbott",
                        "Preface and First Section",
                        "Groundwork Preface + Section I (Abbott)",
                        50,
                        "Nothing is good without qualification except a good will. The good will is not good by what it effects. Duty is acting from respect for law, not from inclination — "
                        "even a sympathetic helper may lack moral worth if the maxim is not the law. "
                        "This offends, and it is supposed to: it isolates the moral motive. Section II will give the formulas.",
                        [
                            "Good will vs gifts of nature and fortune",
                            "Acting in accordance with duty vs from duty",
                            "The first mention of a universal law as the content of the will",
                        ],
                        [
                            "Can a person who enjoys helping still act from duty?",
                            "Why isn’t happiness the unqualified good, given Aristotle?",
                        ],
                        ["kant-cpr-prefaces"],
                        "Section II: the categorical imperative in its formulas.",
                        src(PG, "https://www.gutenberg.org/ebooks/5682", "Section I", "Abbott; PG #5682"),
                        txt("kant-groundwork", "Preface and First Section", "excerpt", "sec-1", "sec-1"),
                    ),
                    A(
                        "kant-groundwork-ii",
                        3,
                        "primary",
                        "Groundwork II: the categorical imperative",
                        "Immanuel Kant",
                        "Fundamental Principles of the Metaphysic of Morals",
                        "Thomas Kingsmill Abbott",
                        "Second Section (formulas of universal law, humanity, kingdom of ends)",
                        "Groundwork Section II",
                        55,
                        "Hypothetical imperatives depend on ends you happen to have. The categorical imperative does not. "
                        "Formulas: act only on maxims you can will as universal law; treat humanity as an end, never merely as a means; a kingdom of ends. "
                        "Autonomy is the will’s property of being a law to itself. Heteronomy is every other principle (happiness, feeling, divine command as external). "
                        "This is the moral Copernican turn. Mill will deny that you can ignore consequences this way.",
                        [
                            "Categorical vs hypothetical imperatives",
                            "At least two formulas, and whether they are supposed to be equivalent",
                            "Autonomy vs heteronomy as the source of spurious principles",
                        ],
                        [
                            "Does ‘universal law’ rule out too much (the lying example) or too little?",
                            "Is treating humanity as an end a different insight, or the same law in another accent?",
                        ],
                        ["kant-groundwork-i"],
                        "After Kant: Hegel’s struggle for recognition; Mill’s liberty and utility; then the century’s explosions.",
                        src(PG, "https://www.gutenberg.org/ebooks/5682", "Section II", "Abbott; PG #5682"),
                        txt("kant-groundwork", "Second Section", "excerpt", "sec-2", "sec-2"),
                    ),
                ],
            },
        ],
    }
