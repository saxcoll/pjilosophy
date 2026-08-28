"""Eras 9–11: nineteenth century, public-domain twentieth, present-day bridge."""
from course_helpers import A, src, txt, PG, WS
from course_eras3 import bib


def era_nineteenth():
    return {
        "id": "nineteenth",
        "order": 9,
        "title": "German idealism and the nineteenth century",
        "years": "1807–1887",
        "intro": (
            "Kant’s dualisms do not stay still. Hegel makes recognition a social process; Schopenhauer names will beneath representation; "
            "Mill rebuilds morals and liberty without Kantian form; Kierkegaard refuses the System; Marx turns Hegel on history and class; "
            "Nietzsche genealogizes morals. Read selections, not systems. The assignment is the move, not the monument."
        ),
        "themes": ["recognition", "utility", "existence", "genealogy"],
        "units": [
            {
                "id": "after-kant",
                "order": 1,
                "title": "Recognition and will",
                "professorNote": "Hegel’s lordship and bondage is the one stretch of the Phenomenology that a first course must have. Schopenhauer is the no that follows the yes of idealism.",
                "assignments": [
                    A(
                        "hegel-lordship",
                        1,
                        "primary",
                        "Hegel: lordship and bondage",
                        "G. W. F. Hegel",
                        "Phenomenology of Spirit",
                        "J. B. Baillie",
                        "The lordship and bondage episode (self-consciousness)",
                        "Phenomenology: Independence and Dependence of Self-Consciousness (Baillie)",
                        55,
                        "Self-consciousness exists only as recognized. Two selves meet; a struggle; one becomes lord, one bondsman. "
                        "The twist: the lord is stuck in a dead end of consumption, while the bondsman’s work on the thing becomes a path to independent consciousness. "
                        "This is not a history of slavery as such. It is a claim about how a self becomes a self. Marx and later recognition theory start here. Baillie is 1910 and public domain; later translations are better but not hostable.",
                        [
                            "Why recognition cannot be one-sided",
                            "The struggle and the roles of lord and bondsman",
                            "Why work, not victory, becomes the engine of a new self-consciousness",
                        ],
                        [
                            "Is the bondsman’s ‘independence’ a liberation you would want, or only a stage?",
                            "What in Descartes’ cogito is being refused by making the self social from the start?",
                        ],
                        ["kant-groundwork-ii"],
                        "Schopenhauer: the world as will, not as Hegelian spirit.",
                        src(
                            "Marxists Internet Archive",
                            "https://www.marxists.org/reference/archive/hegel/works/ph/phba.htm",
                            "Lordship and Bondage",
                            "Baillie 1910",
                        ),
                        txt("hegel-phenomenology", "Lordship and Bondage", "excerpt", "lordship", "lordship"),
                    ),
                    A(
                        "schopenhauer-will",
                        2,
                        "primary",
                        "Schopenhauer: world as idea and as will",
                        "Arthur Schopenhauer",
                        "The World as Will and Idea",
                        "R. B. Haldane and J. Kemp",
                        "Opening of Book I (world as idea) and Book II (world as will)",
                        "World as Will and Idea, openings of Books I–II",
                        50,
                        "The world is my idea: Kant’s objects-as-appearances, said without Kant’s remaining optimism about practical reason. "
                        "Beneath representation, will — blind striving, objectified in bodies and in nature. "
                        "Nietzsche will twist this. For now, feel the metaphysical pessimism as a philosophical thesis, not a mood.",
                        [
                            "‘The world is my idea’ — what is being claimed about subject and object",
                            "Will as the thing-in-itself, in Schopenhauer’s appropriation of Kant",
                            "Why this picture leans toward suffering rather than progress",
                        ],
                        [
                            "Has he named the thing-in-itself, against Kant’s ban, or only relabeled it?",
                            "What ethics would follow if will is endless striving?",
                        ],
                        ["hegel-lordship"],
                        "Mill: a different nineteenth century — utility and the liberty of the individual.",
                        src(PG, "https://www.gutenberg.org/ebooks/38427", "Books I–II openings", "Haldane & Kemp; PG #38427"),
                        txt("schopenhauer-will", "Books I and II openings", "excerpt", "book-i", "book-ii"),
                    ),
                ],
            },
            {
                "id": "liberty-and-utility",
                "order": 2,
                "title": "Mill: utility and liberty",
                "professorNote": "Utilitarianism first, so On Liberty is not a free-speech slogan detached from a theory of the good.",
                "assignments": [
                    A(
                        "mill-utilitarianism",
                        1,
                        "primary",
                        "Utilitarianism I–II",
                        "John Stuart Mill",
                        "Utilitarianism",
                        "n/a (English original)",
                        "Chapters I–II (hosted file emphasizes II; read I in any complete edition if II assumes it)",
                        "Utilitarianism chs. I–II",
                        50,
                        "The right act promotes happiness. Mill’s defense against ‘swine’ is qualitative: some pleasures are higher, as competent judges attest. "
                        "This is both a reply to Kant (consequences matter) and a reply to crude Bentham. "
                        "Watch the competent-judge move: it is empirical in ambition and aristocratic in method.",
                        [
                            "The greatest happiness principle, stated without cartoon",
                            "Higher and lower pleasures — the test of competent judges",
                            "How this is supposed to avoid reducing humans to swine",
                        ],
                        [
                            "Do competent judges smuggle in a non-utilitarian ranking of lives?",
                            "Can you will a lying maxim as universal law and still be a utilitarian? Where do the theories split?",
                        ],
                        ["schopenhauer-will"],
                        "On Liberty: the harm principle and individuality.",
                        src(PG, "https://www.gutenberg.org/ebooks/11224", "chs. I–II", "PG #11224"),
                        txt("mill-utilitarianism", "Chapter II (and I if present)", "excerpt", "ch-2", "ch-2"),
                    ),
                    A(
                        "mill-liberty-harm",
                        2,
                        "primary",
                        "On Liberty I–II: the harm principle",
                        "John Stuart Mill",
                        "On Liberty",
                        "n/a (English original)",
                        "Chapters I–II",
                        "On Liberty chs. I–II",
                        55,
                        "The sole end for which power may be exercised over a member of a civilized community, against his will, is to prevent harm to others. "
                        "Chapter II: liberty of thought and discussion — not because all opinions are true, but because truth needs collision, and because silencing assumes infallibility. "
                        "This is the classic liberal sitting. Read the exceptions (children, ‘backward’ societies) as part of the argument, not as an awkward footnote you skip.",
                        [
                            "The harm principle, including what it is not (not: offense, not: paternalism for adults)",
                            "The infallibility argument against silencing",
                            "Dead dogma vs living truth",
                        ],
                        [
                            "Is ‘harm’ stable enough to limit the state, or does it expand on demand?",
                            "Does the discussion of ‘barbarians’ undermine the universality of the principle?",
                        ],
                        ["mill-utilitarianism"],
                        "Chapter III: individuality as an element of well-being.",
                        src(PG, "https://www.gutenberg.org/ebooks/34901", "chs. I–II", "PG #34901"),
                        txt("mill-on-liberty", "Chapters I–II", "excerpt", "ch-1", "ch-2"),
                    ),
                    A(
                        "mill-liberty-individuality",
                        3,
                        "primary",
                        "On Liberty III: individuality",
                        "John Stuart Mill",
                        "On Liberty",
                        "n/a (English original)",
                        "Chapter III",
                        "On Liberty ch. III",
                        40,
                        "Individuality is not a taste for eccentricity. It is a condition of human development and of social progress. "
                        "Custom is a despot; genius needs oxygen. This chapter connects the harm principle to Mill’s idea of a flourishing human — "
                        "and shows why liberty is, for him, a utilitarian instrument, not a side-constraint from nowhere.",
                        [
                            "Why individuality is an ingredient of well-being, not a luxury",
                            "The despotism of custom",
                            "How this chapter is supposed to support, not compete with, utility",
                        ],
                        [
                            "Can a utilitarian really protect the eccentric when the majority’s happiness would crush them?",
                            "What would Rousseau’s general will say to this praise of being unlike others?",
                        ],
                        ["mill-liberty-harm"],
                        "Kierkegaard against the System; Marx against the class structure of that same century.",
                        src(PG, "https://www.gutenberg.org/ebooks/34901", "ch. III", "PG #34901"),
                        txt("mill-on-liberty", "Chapter III", "excerpt", "ch-3", "ch-3"),
                    ),
                ],
            },
            {
                "id": "existence-and-history",
                "order": 3,
                "title": "Existence and historical materialism",
                "professorNote": "Two refusals of Hegelian reconciliation: the single individual before God, and class struggle as the motor of history.",
                "assignments": [
                    A(
                        "kierkegaard-fear",
                        1,
                        "primary",
                        "Kierkegaard: Fear and Trembling (Hollander)",
                        "Søren Kierkegaard",
                        "Fear and Trembling (selection)",
                        "L. M. Hollander",
                        "The Fear and Trembling section in Hollander’s 1923 Selections",
                        "Hollander, Selections: Fear and Trembling",
                        55,
                        "Abraham’s trial cannot be mediated into the ethical universal. Faith is a paradox: the single individual is higher than the universal, in fear and trembling. "
                        "Hollander’s 1923 translation is public domain and incomplete as a scholarly edition; it is enough to meet the knight of faith against Hegelian ‘both/and.’ "
                        "If you later read a complete Hong or Hannay, you are deepening, not replacing, this sitting.",
                        [
                            "Why Abraham cannot explain himself in ethical language",
                            "The teleological suspension of the ethical — what is suspended, and toward what",
                            "How this is a refusal of Hegel’s mediation",
                        ],
                        [
                            "Is the knight of faith distinguishable from a murderer except by an inner we cannot see?",
                            "What remains of Kantian universal law if this paradox is allowed?",
                        ],
                        ["mill-liberty-individuality"],
                        "Marx: history as class struggle, not as the odyssey of Spirit.",
                        src(PG, "https://www.gutenberg.org/ebooks/60333", "Fear and Trembling selection", "Hollander 1923; PG #60333"),
                        txt("kierkegaard-selections", "Fear and Trembling", "excerpt", "fear", "fear"),
                    ),
                    A(
                        "marx-manifesto",
                        2,
                        "primary",
                        "Manifesto, parts I–II",
                        "Karl Marx and Friedrich Engels",
                        "The Communist Manifesto",
                        "Samuel Moore",
                        "Sections I and II",
                        "Manifesto I–II (Moore/Engels 1888)",
                        45,
                        "The history of hitherto existing society is the history of class struggles. The bourgeoisie has played a revolutionary part — and produced its own gravediggers. "
                        "Part II: the relation of communists to the proletariat; abolition of bourgeois property as the key. "
                        "Read it as a philosophical claim about what drives history and what a person is (a social ensemble), not only as a political pamphlet you already have opinions about.",
                        [
                            "Class struggle as the structure of history",
                            "The bourgeoisie’s revolutionary and self-undermining role",
                            "What ‘abolition of private property’ targets (bourgeois property, not every toothbrush)",
                        ],
                        [
                            "Is this a moral condemnation, a scientific prediction, or both?",
                            "How does the bondsman’s labor in Hegel become, here, a world-historical class?",
                        ],
                        ["kierkegaard-fear"],
                        "Nietzsche: morals have a history that is not Mill’s progress or Marx’s class — a genealogy of values.",
                        src(PG, "https://www.gutenberg.org/ebooks/61", "I–II", "Moore; PG #61"),
                        txt("marx-manifesto", "Parts I–II", "excerpt", "i", "ii"),
                    ),
                ],
            },
            {
                "id": "revaluation",
                "order": 4,
                "title": "Nietzsche’s genealogy",
                "professorNote": "Genealogy first (the method), then a few Gay Science blows (God, recurrence) so you have the temperature as well as the argument.",
                "assignments": [
                    A(
                        "nietzsche-genealogy-i",
                        1,
                        "primary",
                        "Genealogy, First Essay: good and evil",
                        "Friedrich Nietzsche",
                        "On the Genealogy of Morals",
                        "Horace B. Samuel",
                        "Preface (if in your stretch) and First Essay",
                        "Genealogy, First Essay (Samuel)",
                        50,
                        "‘Good’ did not always mean the opposite of evil. Knightly-aristocratic values (good/bad) are inverted by a priestly slave revolt into good/evil — a moralization of ressentiment. "
                        "This is a historical hypothesis with philosophical teeth: our highest values may be an inverted wound. "
                        "You need not accept the history to feel the method: ask who needed this value, and what it did.",
                        [
                            "Good/bad vs good/evil as two value-systems",
                            "Ressentiment as a creative, not merely reactive, force",
                            "What a ‘slave revolt in morals’ is supposed to have changed",
                        ],
                        [
                            "If this genealogy is true, does it refute the values, or only explain them?",
                            "Where would Mill’s competent judges sit in this story?",
                        ],
                        ["marx-manifesto"],
                        "Second Essay: guilt, debt, bad conscience.",
                        src(PG, "https://www.gutenberg.org/ebooks/52319", "First Essay", "Samuel; PG #52319"),
                        txt("nietzsche-genealogy", "First Essay", "excerpt", "essay-i", "essay-i"),
                    ),
                    A(
                        "nietzsche-genealogy-ii",
                        2,
                        "primary",
                        "Genealogy, Second Essay: guilt and bad conscience",
                        "Friedrich Nietzsche",
                        "On the Genealogy of Morals",
                        "Horace B. Samuel",
                        "Second Essay",
                        "Genealogy, Second Essay",
                        50,
                        "Guilt as Schuld: debt. Memory is burned in by pain. Bad conscience is the instinct of cruelty turned inward when it cannot discharge outward. "
                        "The sovereign individual, the right to make promises — a late product, not the starting point of morality. "
                        "This essay is the darker half of the method. It will haunt Freud and every later story about internalization.",
                        [
                            "The creditor–debtor origin of guilt",
                            "Bad conscience as internalized cruelty",
                            "The ‘sovereign individual’ as an achievement, not a given",
                        ],
                        [
                            "Does this reduce justice to cruelty with a ledger, or explain how justice became possible?",
                            "What would Augustine’s divided will look like in this vocabulary?",
                        ],
                        ["nietzsche-genealogy-i"],
                        "Gay Science: the madman, and the heaviest weight.",
                        src(PG, "https://www.gutenberg.org/ebooks/52319", "Second Essay", "Samuel; PG #52319"),
                        txt("nietzsche-genealogy", "Second Essay", "excerpt", "essay-ii", "essay-ii"),
                    ),
                    A(
                        "nietzsche-gay-science",
                        3,
                        "primary",
                        "Gay Science: the madman and recurrence",
                        "Friedrich Nietzsche",
                        "The Joyful Wisdom (The Gay Science)",
                        "Thomas Common / Paul V. Cohn",
                        "The hosted selection, with attention to the madman (§125) and the heaviest weight (§341) in Common’s numbering",
                        "Joyful Wisdom, hosted selection (seek 125 and 341)",
                        40,
                        "The madman: God is dead, and we have killed him — not a cheer, a diagnosis of a vacuum. Eternal recurrence as the heaviest weight: would you will this life again, innumerable times? "
                        "These are tests of affirmation after genealogy has unhooked you from inherited tables. "
                        "Common’s English is of its time; the thoughts are the assignment.",
                        [
                            "Why ‘God is dead’ is a claim about us, not a cosmic autopsy",
                            "Recurrence as an ethical test rather than an astrophysical theory",
                            "How this follows the Genealogy rather than replacing it",
                        ],
                        [
                            "Is the madman announcing liberation, mourning, or both?",
                            "What would it mean to fail the recurrence test and still go on living as before?",
                        ],
                        ["nietzsche-genealogy-ii"],
                        "America and Cambridge: pragmatism and the analytic turn, still in the public domain.",
                        src(PG, "https://www.gutenberg.org/ebooks/52124", "selected aphorisms", "Complete Works vol. 10; PG #52124"),
                        txt("nietzsche-gay-science", "Hosted selection (madman / recurrence)", "excerpt", "selected", "selected"),
                    ),
                ],
            },
        ],
    }


def era_twentieth_pd():
    return {
        "id": "twentieth-pd",
        "order": 10,
        "title": "The turn into the twentieth century",
        "years": "1878–1922",
        "intro": (
            "Two families, still public domain: American pragmatism (ideas as habits of action; race and double consciousness as philosophy) "
            "and the early analytic sequence (Moore’s open question, Russell’s problems, the Tractatus’s picture theory and silence). "
            "After 1922 the legal situation changes. This era is the last stretch you can read entire in the app."
        ),
        "themes": ["pragmatism", "sense-data", "picture theory", "double consciousness"],
        "units": [
            {
                "id": "american-pragmatism",
                "order": 1,
                "title": "Pragmatism and double consciousness",
                "professorNote": "Peirce’s maxim, James’s application, Dewey’s reconstruction, Du Bois’s veil. This is not a detour from ‘real’ philosophy.",
                "assignments": [
                    A(
                        "peirce-ideas-clear",
                        1,
                        "primary",
                        "Peirce: How to Make Our Ideas Clear",
                        "Charles Sanders Peirce",
                        "How to Make Our Ideas Clear",
                        "n/a (English original)",
                        "The whole 1878 essay",
                        "Popular Science Monthly, January 1878 (complete)",
                        45,
                        "The meaning of a conception is the sum of its practical bearings — conceivable effects on conduct and experience. "
                        "Belief is a habit of action. This is the pragmatic maxim, before James popularizes and (Peirce thinks) loosens it. "
                        "Read it as a third way between Cartesian intuition and British psychology.",
                        [
                            "The four methods of fixing belief (briefly) and why science is preferred",
                            "The pragmatic maxim, in Peirce’s wording",
                            "What would make two ideas the same idea",
                        ],
                        [
                            "Does this reduce truth to usefulness, or only clarify meaning?",
                            "How would Descartes’ ‘clear and distinct’ fail this test?",
                        ],
                        ["nietzsche-gay-science"],
                        "James: pragmatism as a method and as a theory of truth’s cash-value.",
                        src(WS, "https://en.wikisource.org/wiki/How_to_Make_Our_Ideas_Clear", "complete essay", "1878; Wikisource"),
                        txt("peirce-ideas-clear", "Complete essay", "full"),
                    ),
                    A(
                        "james-pragmatism",
                        2,
                        "primary",
                        "James: Pragmatism, Lectures I–II",
                        "William James",
                        "Pragmatism",
                        "n/a (English original)",
                        "Lectures I–II",
                        "Pragmatism, Lectures I–II",
                        50,
                        "The tender-minded and tough-minded; pragmatism as a mediator. Lecture II: the pragmatic method, and Peirce named. "
                        "Truth as what works in the way of belief — James’s more expansive cash-value talk. "
                        "Keep Peirce in the room so you can see where James widens the maxim toward temperament and religion.",
                        [
                            "The two temperaments and why philosophy has been their war",
                            "The pragmatic method as a way of settling metaphysical disputes",
                            "Where James’s ‘what works’ might outrun Peirce’s conceivable effects",
                        ],
                        [
                            "Is pragmatism a theory of meaning, of truth, or of how to live among options?",
                            "What dispute (free will, the Absolute) is supposed to dissolve when you ask for cash-value?",
                        ],
                        ["peirce-ideas-clear"],
                        "The Will to Believe: when evidence is not enough and the option is forced.",
                        src(PG, "https://www.gutenberg.org/ebooks/5116", "Lectures I–II", "PG #5116"),
                        txt("james-pragmatism", "Lectures I–II", "excerpt", "lec-1", "lec-2"),
                    ),
                    A(
                        "james-will-to-believe",
                        3,
                        "primary",
                        "James: The Will to Believe",
                        "William James",
                        "The Will to Believe",
                        "n/a (English original)",
                        "The title essay",
                        "The Will to Believe (1896 essay)",
                        40,
                        "When an option is living, forced, and momentous, and intellect cannot decide, it can be rational to let the passional nature choose — especially in religion and trust. "
                        "Clifford’s ‘insufficient evidence’ is refused as a moral rule for all belief. "
                        "This is not a license for wishful thinking about ordinary facts. Watch the restrictions.",
                        [
                            "Living / forced / momentous options",
                            "The quarrel with Clifford",
                            "Why friendship and religion are the examples, not chemistry",
                        ],
                        [
                            "Does James license believing what is false if it pays?",
                            "How does this sit with Peirce’s method of science?",
                        ],
                        ["james-pragmatism"],
                        "Dewey: philosophy reconstructed as a social instrument.",
                        src(PG, "https://www.gutenberg.org/ebooks/26659", "title essay", "PG #26659"),
                        txt("james-will-to-believe", "The Will to Believe", "excerpt", "essay", "essay"),
                    ),
                    A(
                        "dewey-reconstruction",
                        4,
                        "primary",
                        "Dewey: Reconstruction in Philosophy I–II",
                        "John Dewey",
                        "Reconstruction in Philosophy",
                        "n/a (English original)",
                        "Chapters I–II",
                        "Reconstruction in Philosophy chs. I–II (1920)",
                        45,
                        "Philosophy is not a rival physics of the eternal. It grows from social crisis and imagination; it should be reconstructed as a method of moral and political intelligence. "
                        "The 1920 date puts it in the public domain. Later Dewey is often still in copyright — this sitting is the legal, and a fair, introduction.",
                        [
                            "The origin of philosophy in a clash of custom and new knowledge",
                            "What ‘reconstruction’ asks philosophers to stop doing",
                            "Intelligence as experimental and social, not contemplative only",
                        ],
                        [
                            "Is this the end of metaphysics, or a relocation of its job?",
                            "What would Kant’s a priori look like if Dewey is right about origins?",
                        ],
                        ["james-will-to-believe"],
                        "Du Bois: the veil, double consciousness — philosophy of a social self.",
                        src(PG, "https://www.gutenberg.org/ebooks/40089", "chs. I–II", "1920; PG #40089"),
                        txt("dewey-reconstruction", "Chapters I–II", "excerpt", "ch-1", "ch-2"),
                    ),
                    A(
                        "dubois-souls",
                        5,
                        "primary",
                        "Du Bois: Of Our Spiritual Strivings",
                        "W. E. B. Du Bois",
                        "The Souls of Black Folk",
                        "n/a (English original)",
                        "Chapter I",
                        "Souls, ch. I (1903)",
                        40,
                        "The problem of the twentieth century is the color-line. Double consciousness: seeing oneself through a veil, two souls, two thoughts. "
                        "This is philosophy of mind and political philosophy at once — a social account of self-knowledge Hegel would recognize and James’s student could write. "
                        "It belongs in a Western philosophy course because the Western self was never only European.",
                        [
                            "The veil as a structure of seeing and being seen",
                            "Double consciousness — not ‘low self-esteem,’ a split of perspectives",
                            "How emancipation’s aftermath frames the philosophical problem",
                        ],
                        [
                            "Is double consciousness only a wound, or also a way of knowing the world the veil hides from others?",
                            "How does this complicate Locke’s and Hume’s first-person self?",
                        ],
                        ["dewey-reconstruction"],
                        "Moore, Russell, Wittgenstein: the analytic beginning, still PD.",
                        src(PG, "https://www.gutenberg.org/ebooks/408", "ch. I", "1903; PG #408"),
                        txt("dubois-souls", "Chapter I", "excerpt", "ch-1", "ch-1"),
                    ),
                ],
            },
            {
                "id": "analytic-turn",
                "order": 2,
                "title": "The early analytic sequence",
                "professorNote": "Moore’s open question, Russell’s table, induction, the value of philosophy, then the Tractatus in two sittings. After that, copyright walls.",
                "assignments": [
                    A(
                        "moore-principia",
                        1,
                        "primary",
                        "Moore: the open-question argument",
                        "G. E. Moore",
                        "Principia Ethica",
                        "n/a (English original)",
                        "Chapter I (subject-matter of ethics; naturalistic fallacy)",
                        "Principia Ethica ch. I (1903)",
                        50,
                        "Good is a simple, unanalyzable quality. Any identification of good with a natural property (pleasure, evolutionary fitness) leaves an open question: but is that good? "
                        "This is the naturalistic fallacy as Moore names it. Mill’s utility and Aristotle’s function are in the room. "
                        "Later metaethics will attack Moore; you need the argument in its original force.",
                        [
                            "The distinction between good and things that are good",
                            "The open-question argument",
                            "What ‘naturalistic fallacy’ does and does not mean (not: ‘never mention nature’)",
                        ],
                        [
                            "Does the open question prove simplicity, or only our linguistic habits?",
                            "How would Mill answer: is ‘pleasure is good’ tautological on his view?",
                        ],
                        ["dubois-souls"],
                        "Russell: appearance, matter, and why philosophy is not just tables.",
                        src(PG, "https://www.gutenberg.org/ebooks/53430", "ch. I", "1903; PG #53430"),
                        txt("moore-principia-ethica", "Chapter I", "excerpt", "ch-1", "ch-1"),
                    ),
                    A(
                        "russell-problems-appearance",
                        2,
                        "primary",
                        "Russell: appearance, acquaintance, description",
                        "Bertrand Russell",
                        "The Problems of Philosophy",
                        "n/a (English original)",
                        "Chapters I and V",
                        "Problems of Philosophy chs. I, V (1912)",
                        45,
                        "The table as a lesson: sense-data vs physical object. Then: knowledge by acquaintance and by description — how we can think about things we are not acquainted with. "
                        "This is the analytic classroom’s first morning. It is also a reply to idealism (Berkeley) without naïve realism.",
                        [
                            "Why the table’s appearance is not simply the table",
                            "Sense-data as what we are directly acquainted with",
                            "Knowledge by description as the bridge to other minds and to physics",
                        ],
                        [
                            "Has Russell refuted Berkeley, or only offered a different hypothesis?",
                            "What are you acquainted with, if not the table?",
                        ],
                        ["moore-principia"],
                        "Induction, and why philosophy is still worth doing.",
                        src(PG, "https://www.gutenberg.org/ebooks/5827", "chs. I, V", "1912; PG #5827"),
                        txt("russell-problems", "Chapters I and V", "excerpt", "ch-1", "ch-5"),
                    ),
                    A(
                        "russell-problems-induction",
                        3,
                        "primary",
                        "Russell: induction and the value of philosophy",
                        "Bertrand Russell",
                        "The Problems of Philosophy",
                        "n/a (English original)",
                        "Chapters VI and XV",
                        "Problems chs. VI, XV",
                        40,
                        "The principle of induction cannot be proved by experience without circularity; we assume it. Chapter XV: the value of philosophy is in the questions, the enlargement of the self, not in a body of settled doctrine. "
                        "After Hume and before the Tractatus, this is a humane analytic credo. It is also your permission to keep going when systems fail.",
                        [
                            "Why induction is a principle, not a theorem of experience",
                            "What philosophy is not (a rival of the special sciences’ results)",
                            "The enlargement of the not-Self as a value",
                        ],
                        [
                            "Is Russell’s induction principle a confession of Hume’s point or an answer to it?",
                            "After this chapter, what would it mean for this course to ‘finish’?",
                        ],
                        ["russell-problems-appearance"],
                        "Tractatus: the picture theory, then silence.",
                        src(PG, "https://www.gutenberg.org/ebooks/5827", "chs. VI, XV", "PG #5827"),
                        txt("russell-problems", "Chapters VI and XV", "excerpt", "ch-6", "ch-15"),
                    ),
                    A(
                        "tractatus-picture",
                        4,
                        "primary",
                        "Tractatus 1–5: world, picture, proposition",
                        "Ludwig Wittgenstein",
                        "Tractatus Logico-Philosophicus",
                        "C. K. Ogden",
                        "Propositions 1 through the 5s, as hosted",
                        "Tractatus props. 1–5 (Ogden 1922)",
                        55,
                        "The world is all that is the case. A proposition is a picture of a state of affairs. Logical form is shown, not said. "
                        "Ogden’s 1922 translation is public domain. You will later hear that Wittgenstein rejected this book. Read it first as if he meant it. "
                        "Do not hunt mysticism yet; hunt the picture theory.",
                        [
                            "1–1.2: world as facts, not things",
                            "The picture theory: how a proposition can be true or false",
                            "What cannot be said but only shown (logical form)",
                        ],
                        [
                            "If the limits of language are the limits of the world, what happens to ethics and the self?",
                            "Is this metaphysics, or a ban on metaphysics?",
                        ],
                        ["russell-problems-induction"],
                        "The ending: what we cannot speak about.",
                        src(PG, "https://www.gutenberg.org/ebooks/5740", "props. 1–5", "Ogden 1922; PG #5740 / Wikisource"),
                        txt("wittgenstein-tractatus", "Propositions 1–5", "excerpt", "p1", "p4"),
                    ),
                    A(
                        "tractatus-silence",
                        5,
                        "primary",
                        "Tractatus 6–7: the ladder and silence",
                        "Ludwig Wittgenstein",
                        "Tractatus Logico-Philosophicus",
                        "C. K. Ogden",
                        "Propositions 6–7",
                        "Tractatus props. 6–7",
                        35,
                        "The general form of the proposition; then the propositions of the book as elucidatory — a ladder to be thrown away. "
                        "Whereof one cannot speak, thereof one must be silent. Ethics, aesthetics, the mystical: they show themselves. "
                        "This is the last in-app primary text of the course’s PD spine. The next era is a map of what you must obtain legally.",
                        [
                            "The ladder remark — what it does to the status of the book you just read",
                            "Proposition 7 as a rule, not a poetic sigh",
                            "How this ending both fulfills and undermines the picture theory",
                        ],
                        [
                            "If the book is nonsense by its own light, why read it?",
                            "What would a second Wittgenstein have to change first: pictures, or silence?",
                        ],
                        ["tractatus-picture"],
                        "Present-day bridge: in-copyright works, assigned exactly, not hosted.",
                        src(PG, "https://www.gutenberg.org/ebooks/5740", "props. 6–7", "Ogden 1922"),
                        txt("wittgenstein-tractatus", "Propositions 6–7", "excerpt", "p6", "p6"),
                    ),
                ],
            },
        ],
    }


def era_present():
    note_lib = (
        "Get a printed or licensed library copy. Do not use a pirated PDF. This course does not host the work."
    )
    return {
        "id": "present-day",
        "order": 11,
        "title": "How to keep going",
        "years": "1922–present",
        "intro": (
            "The rest of the century is still in copyright in the United States. You will read it as a student reads assigned chapters: legally, with a physical or licensed copy. "
            "The assignments below are exact. They complete the spine: language after the Tractatus, being and existence, the analytic/continental split, justice, power, and inner moral vision. "
            "Two final maps tell you how the living debates are clustered so you are not abandoned in 1922."
        ),
        "themes": ["language", "existence", "justice", "power", "mind"],
        "units": [
            {
                "id": "language-being-existence",
                "order": 1,
                "title": "Language, being, existence",
                "professorNote": "Three in-copyright landmarks. The quiz checks whether you found the assigned move, not whether you memorized a biography.",
                "assignments": [
                    A(
                        "wittgenstein-investigations",
                        1,
                        "bibliographic",
                        "Philosophical Investigations §§1–43",
                        "Ludwig Wittgenstein",
                        "Philosophical Investigations",
                        "G. E. M. Anscombe (standard English)",
                        "§§1–43 (language-games, ostension, family resemblance)",
                        "PI §§1–43",
                        60,
                        "The later Wittgenstein returns to Augustine’s picture of words as names and breaks it: meaning as use, language-games, the impossibility of a private ostensive definition as the whole story. "
                        "This is the repudiation of the Tractatus’s picture theory from inside the same life. You need a legal copy (Anscombe’s translation is still in copyright).",
                        [
                            "The shopkeeper / five red apples example — what it is for",
                            "Language-game as a comparison, not a theory of everything",
                            "Why ‘meaning as use’ is not ‘words mean whatever I like’",
                        ],
                        [
                            "What in Tractatus 1–4 cannot survive §§1–43?",
                            "Is family resemblance a theory of concepts, or a warning against theories of concepts?",
                        ],
                        ["tractatus-silence"],
                        "Heidegger: the question of being, which the Tractatus treated as something to be silent about — or as nonsense.",
                        bib(
                            "PI §§1–43",
                            "Anscombe translation; any standard bilingual edition",
                            note_lib,
                            "https://search.worldcat.org/search?q=Philosophical+Investigations+Wittgenstein",
                        ),
                    ),
                    A(
                        "heidegger-being-time",
                        2,
                        "bibliographic",
                        "Being and Time, Introduction §§1–4",
                        "Martin Heidegger",
                        "Being and Time",
                        "Macquarrie & Robinson (standard English; in copyright)",
                        "Introduction, §§1–4 (the question of being; Dasein as the being that asks)",
                        "SZ Introduction §§1–4 (German 1927; English 1962 is in copyright)",
                        70,
                        "The question of being has been forgotten. The being who can ask it is Dasein — existence as ours, not a Cartesian subject with properties. "
                        "The German original’s US status is not a free pass to host an English translation: Macquarrie (1962) is in copyright, and URAA complications attend the German. "
                        "Obtain a legal copy. Read only the Introduction’s first four sections; that is the question, not the whole book.",
                        [
                            "Why ‘being’ is not a being among beings",
                            "Dasein as the entity that understands being",
                            "What is being refused in the Cartesian starting point",
                        ],
                        [
                            "Is this a new method, or a new subject-matter?",
                            "How would Russell’s table look if the first question were being, not sense-data?",
                        ],
                        ["wittgenstein-investigations"],
                        "Sartre: existence precedes essence, in public prose.",
                        bib(
                            "SZ Int. §§1–4",
                            "Macquarrie & Robinson or a later licensed English",
                            note_lib + " Do not host or download unauthorized scans of the English.",
                            "https://search.worldcat.org/search?q=Being+and+Time+Heidegger",
                        ),
                    ),
                    A(
                        "sartre-existentialism",
                        3,
                        "bibliographic",
                        "Existentialism Is a Humanism",
                        "Jean-Paul Sartre",
                        "Existentialism Is a Humanism",
                        "Carol Macomber or earlier licensed English",
                        "The lecture entire (it is short) with attention to ‘existence precedes essence’ and anguish/abandonment/despair",
                        "The 1946 lecture (in copyright)",
                        50,
                        "Existence precedes essence: there is no given human nature that lets you off the hook. In choosing, you choose an image of the human. "
                        "Anguish, abandonment, despair are technical here, not moods. This is the public, compressed Sartre — a door, not Being and Nothingness. "
                        "Get a legal edition of the lecture.",
                        [
                            "What ‘existence precedes essence’ denies (a maker’s blueprint for the human)",
                            "How a choice is supposed to bind all humans as an image",
                            "Why this is offered as a humanism, against the charge of quietism",
                        ],
                        [
                            "Does ‘choosing for all’ smuggle in a Kantian universal without the moral law?",
                            "What would a materialist (Hobbes, Marx) say is missing from this freedom?",
                        ],
                        ["heidegger-being-time"],
                        "Analytic mid-century: Quine against two dogmas; Anscombe against a certain modern moral philosophy.",
                        bib(
                            "the lecture",
                            "Any licensed English of Existentialism Is a Humanism",
                            note_lib,
                            "https://search.worldcat.org/search?q=Existentialism+is+a+Humanism+Sartre",
                        ),
                    ),
                ],
            },
            {
                "id": "mind-language-science",
                "order": 2,
                "title": "Analytic shocks: language, science, intention",
                "professorNote": "Two essays that reorganized the field. Read them as assigned chapters, not as internet paraphrases.",
                "assignments": [
                    A(
                        "quine-two-dogmas",
                        1,
                        "bibliographic",
                        "Quine: Two Dogmas of Empiricism",
                        "W. V. O. Quine",
                        "Two Dogmas of Empiricism",
                        "n/a (English original, 1951)",
                        "The whole essay (it is the assignment)",
                        "From a Philosophical Review reprint or From a Logical Point of View — licensed copy",
                        55,
                        "The analytic/synthetic distinction and reductionism are dogmas. Meaning holism: statements meet the tribunal of experience as a corporate body. "
                        "Empiricism after Hume and Carnap has to live without a sharp language/world split at the sentence level. "
                        "Do not quote long stretches into notes you share; understand the two dogmas and the holism claim.",
                        [
                            "What the two dogmas are",
                            "Why synonymy does not easily save analyticity",
                            "The web of belief — what is being said about revision",
                        ],
                        [
                            "What happens to Kant’s synthetic a priori if there is no analytic/synthetic cut?",
                            "Is holism a skepticism, or a picture of science?",
                        ],
                        ["sartre-existentialism"],
                        "Anscombe: intention, and modern moral philosophy’s vocabulary problem.",
                        bib(
                            "complete essay",
                            "Quine, ‘Two Dogmas of Empiricism’ (1951)",
                            note_lib,
                            "https://search.worldcat.org/search?q=Two+Dogmas+of+Empiricism+Quine",
                        ),
                    ),
                    A(
                        "anscombe-modern-moral",
                        2,
                        "bibliographic",
                        "Anscombe: Modern Moral Philosophy (and a look at Intention §§1–5 if you have it)",
                        "G. E. M. Anscombe",
                        "Modern Moral Philosophy",
                        "n/a (English original, 1958)",
                        "The whole 1958 paper; optionally Intention §§1–5 for the action-theoretic companion",
                        "Philosophy 33 (1958) via library; Intention (1957) is also in copyright",
                        50,
                        "Moral philosophy should be laid aside until we have an adequate philosophy of psychology. The surviving ‘ought’ is a law-sense without a lawgiver — incoherent. "
                        "This is the paper that helped restart virtue ethics and that refuses both Kantian duty-talk and consequentialism as then practiced. "
                        "If you also open Intention, take only the opening sections on what it is to act intentionally.",
                        [
                            "Why she wants a philosophy of psychology first",
                            "The diagnosis of ‘ought’ as a survivor of a divine-law conception",
                            "What she is asking us to stop doing in ethics class",
                        ],
                        [
                            "Does this refute Kant, or only a thin classroom Kant?",
                            "How would Aristotle’s hexis fit her demand for a psychology?",
                        ],
                        ["quine-two-dogmas"],
                        "Justice, power, and the sovereignty of good — still bibliographic.",
                        bib(
                            "the 1958 paper",
                            "Anscombe, ‘Modern Moral Philosophy’",
                            note_lib,
                            "https://search.worldcat.org/search?q=Modern+Moral+Philosophy+Anscombe",
                        ),
                    ),
                ],
            },
            {
                "id": "ethics-politics-power",
                "order": 3,
                "title": "Justice, power, the good",
                "professorNote": "Three different late-century ways of doing moral and political philosophy. None replaces the others.",
                "assignments": [
                    A(
                        "rawls-justice",
                        1,
                        "bibliographic",
                        "Rawls: Theory of Justice, §§1–4 and 11–14",
                        "John Rawls",
                        "A Theory of Justice",
                        "n/a (English original, 1971)",
                        "Revised edition if possible: ch. 1 §§1–4 (the role of justice; original position) and §§11–14 (two principles, equal liberty, difference principle)",
                        "TJ §§1–4, 11–14 (1971/1999)",
                        75,
                        "Justice as fairness: the original position and veil of ignorance as a device, not a history. Two principles: equal basic liberties; social and economic inequalities to be arranged for the greatest benefit of the least advantaged, under fair equality of opportunity. "
                        "This is the social-contract tradition after Hume’s and Rousseau’s and Kant’s — a Kantian procedure with economic content. "
                        "Library copy. Read the assigned sections only; the book is a doorstop.",
                        [
                            "The original position as a point of view, not a place",
                            "The two principles, in order",
                            "Why the difference principle is not simple equality and not maximax for the talented",
                        ],
                        [
                            "What would Mill’s harm principle say is missing, or already included?",
                            "Is the veil of ignorance a moral insight or an economic thought experiment?",
                        ],
                        ["anscombe-modern-moral"],
                        "Foucault: power that does not look like a sovereign’s sword.",
                        bib(
                            "TJ §§1–4, 11–14",
                            "Rawls, A Theory of Justice",
                            note_lib,
                            "https://search.worldcat.org/search?q=A+Theory+of+Justice+Rawls",
                        ),
                    ),
                    A(
                        "foucault-discipline",
                        2,
                        "bibliographic",
                        "Foucault: Discipline and Punish, Panopticism",
                        "Michel Foucault",
                        "Discipline and Punish",
                        "Alan Sheridan (English; in copyright)",
                        "The ‘Panopticism’ chapter (Part III, ch. 3 in the English)",
                        "Surveiller et punir: ‘Le panoptisme’ / English ‘Panopticism’",
                        55,
                        "Bentham’s Panopticon becomes a diagram of modern power: visibility, internalization of the gaze, discipline as producing subjects rather than merely forbidding acts. "
                        "This is a genealogical sitting after Nietzsche, applied to prisons, schools, barracks. "
                        "Sheridan’s English is in copyright. Obtain it legally. One chapter is enough for the move.",
                        [
                            "The Panopticon as an architectural and social diagram",
                            "Power as productive, not only repressive",
                            "How this differs from Hobbes’s visible sovereign",
                        ],
                        [
                            "Is this a theory of modernity, or a reading of a prison plan overextended?",
                            "What would Rawls’s original position look like if the parties were already disciplinary subjects?",
                        ],
                        ["rawls-justice"],
                        "Murdoch: moral vision, attention, the Good — against a certain existentialist will.",
                        bib(
                            "Panopticism chapter",
                            "Foucault, Discipline and Punish, Sheridan trans.",
                            note_lib,
                            "https://search.worldcat.org/search?q=Discipline+and+Punish+Foucault",
                        ),
                    ),
                    A(
                        "murdoch-sovereignty",
                        3,
                        "bibliographic",
                        "Murdoch: The Sovereignty of Good (title essay)",
                        "Iris Murdoch",
                        "The Sovereignty of Good",
                        "n/a (English original, 1970)",
                        "The essay ‘The Sovereignty of Good Over Other Concepts’ (the volume’s central piece)",
                        "The Sovereignty of Good, title essay",
                        50,
                        "Against a picture of the moral agent as a naked will issuing choices: moral life is a matter of vision, attention, unselfing — Platonic Good without cheap mysticism. "
                        "This is a late-century reply to Sartre and to a certain analytic thinness, written in English you must obtain legally. "
                        "One essay, read slowly, is the assignment.",
                        [
                            "What is wrong, for her, with existentialist/Kantian will as the whole of morals",
                            "Attention (and M’s example of the mother-in-law) as moral activity",
                            "The Good as a magnetic, not a chosen, orientation",
                        ],
                        [
                            "Is this Platonism you already had in the Cave, or a new use of it?",
                            "How would Mill’s competent judges sit with ‘unselfing’?",
                        ],
                        ["foucault-discipline"],
                        "Two maps: where the living conversations are.",
                        bib(
                            "title essay",
                            "Murdoch, The Sovereignty of Good",
                            note_lib,
                            "https://search.worldcat.org/search?q=The+Sovereignty+of+Good+Murdoch",
                        ),
                    ),
                ],
            },
            {
                "id": "keep-going-maps",
                "order": 4,
                "title": "Maps for the living debates",
                "professorNote": "These are bibliographic assignments without a single book: they tell you how to continue. The quiz checks that you can place a problem in a family.",
                "assignments": [
                    A(
                        "map-analytic",
                        1,
                        "bibliographic",
                        "Map: analytic philosophy after Quine",
                        "Various",
                        "A path, not one book",
                        "",
                        "Skim a handbook table of contents or SEP entries (not hosted) for: philosophy of language after Kripke; philosophy of mind (identity theory, functionalism, consciousness); epistemology after Gettier",
                        "Use Stanford Encyclopedia or a library handbook — do not paste copyrighted articles into this app",
                        40,
                        "You now have tools: sense-data, use, holism, intention. The living analytic debates cluster around: reference and necessity (Kripke’s lectures — in copyright); "
                        "mind (the mind-body problem after dualism you met in Descartes); knowledge (Gettier’s short paper — in copyright — broke the justified-true-belief analysis). "
                        "This sitting is orientation. Write a one-page map of three problems you could actually start next, with a legal first text for each.",
                        [
                            "One language problem that is not ‘picture vs use’ restated",
                            "One mind problem that is not ‘Descartes was a dualist’ restated",
                            "What Gettier-style cases are for (justification vs knowledge)",
                        ],
                        [
                            "Name three next readings, legal to obtain, and why each fits this course’s spine.",
                            "Where would you put ethics after Anscombe and Rawls on this map?",
                        ],
                        ["murdoch-sovereignty"],
                        "A second map: continentals, political theory, and the rest of the world this course only touched.",
                        bib(
                            "your one-page map",
                            "SEP / library handbooks",
                            "Use encyclopedia and library resources. Do not scrape paid articles into the repo.",
                            "https://plato.stanford.edu/",
                        ),
                    ),
                    A(
                        "map-continental-ethics",
                        2,
                        "bibliographic",
                        "Map: continental, political, and moral continuations",
                        "Various",
                        "A path, not one book",
                        "",
                        "Place: phenomenology after Heidegger (Merleau-Ponty, Levinas); critical theory (Habermas); feminist philosophy; philosophy of race after Du Bois; bioethics / mind as public issues",
                        "Library and SEP; no pirated books",
                        40,
                        "The other half of ‘how to keep going’: phenomenology of the body; ethics of the other; discourse and democracy; feminist critiques of the ‘neutral’ subject you met from Descartes to Rawls; "
                        "philosophy of race as continuation of Du Bois, not an optional module. "
                        "Again: a one-page map, three legal starting points. You have finished the guided sequence when you can assign yourself the next sitting.",
                        [
                            "One phenomenological problem that is not ‘Heidegger said being’",
                            "One political problem after Rawls/Foucault (recognition, domination, gender, race)",
                            "How this course’s ancient ethics (Aristotle, Stoics) might still speak in applied ethics",
                        ],
                        [
                            "Which continuation is most urgent for you, and which earlier assignment made it so?",
                            "What would you tell a friend is the one move this course taught that summaries cannot?",
                        ],
                        ["map-analytic"],
                        "There is no last reading. There is a next one you can now choose with judgment.",
                        bib(
                            "your second one-page map",
                            "SEP / library",
                            "Legal sources only.",
                            "https://plato.stanford.edu/",
                        ),
                    ),
                ],
            },
        ],
    }
