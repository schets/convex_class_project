"""
Porter Stemmer

This is the Porter stemming algorithm. It follows the algorithm
presented in

Porter, M. "An algorithm for suffix stripping." Program 14.3 (1980): 130-137.

Martin Porter, the algorithm's inventor, maintains a web page about the
algorithm at

    http://www.tartarus.org/~martin/PorterStemmer/

which includes another Python implementation and other implementations
in many languages.

I've taken this from the nltk toolkit and trimmed out functionality which
isn't used in the matlab version, as well as added a command line interface
for testing

I did this to reduce the external dependencies needed to run this to more common ones

https://github.com/nltk/nltk
"""

__docformat__ = 'plaintext'

__vowels = frozenset(['a', 'e', 'i', 'o', 'u'])

def _is_consonant(word, i):
    """Returns True if word[i] is a consonant, False otherwise

    A consonant is defined in the paper as follows:

        A consonant in a word is a letter other than A, E, I, O or
        U, and other than Y preceded by a consonant. (The fact that
        the term `consonant' is defined to some extent in terms of
        itself does not make it ambiguous.) So in TOY the consonants
        are T and Y, and in SYZYGY they are S, Z and G. If a letter
        is not a consonant it is a vowel.
    """
    if word[i] in __vowels:
        return False
    if word[i] == 'y':
        if i == 0:
            return True
        else:
            return not _is_consonant(word, i - 1)
    return True

def _measure(stem):
    """Returns the 'measure' of stem, per definition in the paper

    From the paper:

        A consonant will be denoted by c, a vowel by v. A list
        ccc... of length greater than 0 will be denoted by C, and a
        list vvv... of length greater than 0 will be denoted by V.
        Any word, or part of a word, therefore has one of the four
        forms:

            CVCV ... C
            CVCV ... V
            VCVC ... C
            VCVC ... V

        These may all be represented by the single form

            [C]VCVC ... [V]

        where the square brackets denote arbitrary presence of their
        contents. Using (VC){m} to denote VC repeated m times, this
        may again be written as

            [C](VC){m}[V].

        m will be called the \measure\ of any word or word part when
        represented in this form. The case m = 0 covers the null
        word. Here are some examples:

            m=0    TR,  EE,  TREE,  Y,  BY.
            m=1    TROUBLE,  OATS,  TREES,  IVY.
            m=2    TROUBLES,  PRIVATE,  OATEN,  ORRERY.
    """
    cv_sequence = ''

    # Construct a string of 'c's and 'v's representing whether each
    # character in `stem` is a consonant or a vowel.
    # e.g. 'falafel' becomes 'cvcvcvc',
    #      'architecture' becomes 'vcccvcvccvcv'
    for i in range(len(stem)):
        if _is_consonant(stem, i):
            cv_sequence += 'c'
        else:
            cv_sequence += 'v'

    # Count the number of 'vc' occurences, which is equivalent to
    # the number of 'VC' occurrences in Porter's reduced form in the
    # docstring above, which is in turn equivalent to `m`
    return cv_sequence.count('vc')

def _has_positive_measure(stem):
    return _measure(stem) > 0

def _contains_vowel(stem):
    """Returns True if stem contains a vowel, else False"""
    for i in range(len(stem)):
        if not _is_consonant(stem, i):
            return True
    return False

def _ends_double_consonant(word):
    """Implements condition *d from the paper

    Returns True if word ends with a double consonant
    """
    return (
        len(word) >= 2
        and word[-1] == word[-2]
        and _is_consonant(word, len(word) - 1)
    )

def _ends_cvc(word):
    """Implements condition *o from the paper

    From the paper:

        *o  - the stem ends cvc, where the second c is not W, X or Y
              (e.g. -WIL, -HOP).
    """
    return (
        len(word) >= 3
        and _is_consonant(word, len(word) - 3)
        and not _is_consonant(word, len(word) - 2)
        and _is_consonant(word, len(word) - 1)
        and word[-1] not in ('w', 'x', 'y')
    )

def _replace_suffix(word, suffix, replacement):
    """Replaces `suffix` of `word` with `replacement"""
    assert word.endswith(suffix), "Given word doesn't end with given suffix"
    if suffix == '':
        return word + replacement
    else:
        return word[: -len(suffix)] + replacement

def _apply_rule_list(word, rules):
    """Applies the first applicable suffix-removal rule to the word

    Takes a word and a list of suffix-removal rules represented as
    3-tuples, with the first element being the suffix to remove,
    the second element being the string to replace it with, and the
    final element being the condition for the rule to be applicable,
    or None if the rule is unconditional.
    """
    for rule in rules:
        suffix, replacement, condition = rule
        if suffix == '*d' and _ends_double_consonant(word):
            stem = word[:-2]
            if condition is None or condition(stem):
                return stem + replacement
            else:
                # Don't try any further rules
                return word
        if word.endswith(suffix):
            stem = _replace_suffix(word, suffix, '')
            if condition is None or condition(stem):
                return stem + replacement
            else:
                # Don't try any further rules
                return word

    return word

def _step1a(word):
    """Implements Step 1a from "An algorithm for suffix stripping"

    From the paper:

        SSES -> SS                         caresses  ->  caress
        IES  -> I                          ponies    ->  poni
                                           ties      ->  ti
        SS   -> SS                         caress    ->  caress
        S    ->                            cats      ->  cat
    """

    return _apply_rule_list(
        word,
        [
            ('sses', 'ss', None),  # SSES -> SS
            ('ies', 'i', None),  # IES  -> I
            ('ss', 'ss', None),  # SS   -> SS
            ('s', '', None),  # S    ->
        ],
    )

def _step1b(word):
    """Implements Step 1b from "An algorithm for suffix stripping"

    From the paper:

        (m>0) EED -> EE                    feed      ->  feed
                                           agreed    ->  agree
        (*v*) ED  ->                       plastered ->  plaster
                                           bled      ->  bled
        (*v*) ING ->                       motoring  ->  motor
                                           sing      ->  sing

    If the second or third of the rules in Step 1b is successful,
    the following is done:

        AT -> ATE                       conflat(ed)  ->  conflate
        BL -> BLE                       troubl(ed)   ->  trouble
        IZ -> IZE                       siz(ed)      ->  size
        (*d and not (*L or *S or *Z))
           -> single letter
                                        hopp(ing)    ->  hop
                                        tann(ed)     ->  tan
                                        fall(ing)    ->  fall
                                        hiss(ing)    ->  hiss
                                        fizz(ed)     ->  fizz
        (m=1 and *o) -> E               fail(ing)    ->  fail
                                        fil(ing)     ->  file

    The rule to map to a single letter causes the removal of one of
    the double letter pair. The -E is put back on -AT, -BL and -IZ,
    so that the suffixes -ATE, -BLE and -IZE can be recognised
    later. This E may be removed in step 4.
    """

    # (m>0) EED -> EE
    if word.endswith('eed'):
        stem = _replace_suffix(word, 'eed', '')
        if _measure(stem) > 0:
            return stem + 'ee'
        else:
            return word

    rule_2_or_3_succeeded = False

    for suffix in ['ed', 'ing']:
        if word.endswith(suffix):
            intermediate_stem = _replace_suffix(word, suffix, '')
            if _contains_vowel(intermediate_stem):
                rule_2_or_3_succeeded = True
                break

    if not rule_2_or_3_succeeded:
        return word

    return _apply_rule_list(
        intermediate_stem,
        [
            ('at', 'ate', None),  # AT -> ATE
            ('bl', 'ble', None),  # BL -> BLE
            ('iz', 'ize', None),  # IZ -> IZE
            # (*d and not (*L or *S or *Z))
            # -> single letter
            (
                '*d',
                intermediate_stem[-1],
                lambda stem: intermediate_stem[-1] not in ('l', 's', 'z'),
            ),
            # (m=1 and *o) -> E
            (
                '',
                'e',
                lambda stem: (_measure(stem) == 1 and _ends_cvc(stem)),
            ),
        ],
    )

def _step1c(word):
    """Implements Step 1c from "An algorithm for suffix stripping"

    From the paper:

    Step 1c

        (*v*) Y -> I                    happy        ->  happi
                                        sky          ->  sky
    """

    def nltk_condition(stem):
        """
        This has been modified from the original Porter algorithm so
        that y->i is only done when y is preceded by a consonant,
        but not if the stem is only a single consonant, i.e.

           (*c and not c) Y -> I

        So 'happy' -> 'happi', but
           'enjoy' -> 'enjoy'  etc

        This is a much better rule. Formerly 'enjoy'->'enjoi' and
        'enjoyment'->'enjoy'. Step 1c is perhaps done too soon; but
        with this modification that no longer really matters.

        Also, the removal of the contains_vowel(z) condition means
        that 'spy', 'fly', 'try' ... stem to 'spi', 'fli', 'tri' and
        conflate with 'spied', 'tried', 'flies' ...
        """
        return len(stem) > 1 and _is_consonant(stem, len(stem) - 1)

    def condition(stem):
        return _contains_vowel(stem)

    return _apply_rule_list(
        word,
        [
            (
                'y',
                'i',
                 condition,
            )
        ],
    )

def _step2(word):
    """Implements Step 2 from "An algorithm for suffix stripping"

    From the paper:

    Step 2

        (m>0) ATIONAL ->  ATE       relational     ->  relate
        (m>0) TIONAL  ->  TION      conditional    ->  condition
                                    rational       ->  rational
        (m>0) ENCI    ->  ENCE      valenci        ->  valence
        (m>0) ANCI    ->  ANCE      hesitanci      ->  hesitance
        (m>0) IZER    ->  IZE       digitizer      ->  digitize
        (m>0) ABLI    ->  ABLE      conformabli    ->  conformable
        (m>0) ALLI    ->  AL        radicalli      ->  radical
        (m>0) ENTLI   ->  ENT       differentli    ->  different
        (m>0) ELI     ->  E         vileli        - >  vile
        (m>0) OUSLI   ->  OUS       analogousli    ->  analogous
        (m>0) IZATION ->  IZE       vietnamization ->  vietnamize
        (m>0) ATION   ->  ATE       predication    ->  predicate
        (m>0) ATOR    ->  ATE       operator       ->  operate
        (m>0) ALISM   ->  AL        feudalism      ->  feudal
        (m>0) IVENESS ->  IVE       decisiveness   ->  decisive
        (m>0) FULNESS ->  FUL       hopefulness    ->  hopeful
        (m>0) OUSNESS ->  OUS       callousness    ->  callous
        (m>0) ALITI   ->  AL        formaliti      ->  formal
        (m>0) IVITI   ->  IVE       sensitiviti    ->  sensitive
        (m>0) BILITI  ->  BLE       sensibiliti    ->  sensible
    """

    rules = [
        ('ational', 'ate', _has_positive_measure),
        ('tional', 'tion', _has_positive_measure),
        ('enci', 'ence', _has_positive_measure),
        ('anci', 'ance', _has_positive_measure),
        ('izer', 'ize', _has_positive_measure),
        ('bli', 'ble', _has_positive_measure),
        ('alli', 'al', _has_positive_measure),
        ('entli', 'ent', _has_positive_measure),
        ('eli', 'e', _has_positive_measure),
        ('ousli', 'ous', _has_positive_measure),
        ('ization', 'ize', _has_positive_measure),
        ('ation', 'ate', _has_positive_measure),
        ('ator', 'ate', _has_positive_measure),
        ('alism', 'al', _has_positive_measure),
        ('iveness', 'ive', _has_positive_measure),
        ('fulness', 'ful', _has_positive_measure),
        ('ousness', 'ous', _has_positive_measure),
        ('aliti', 'al', _has_positive_measure),
        ('iviti', 'ive', _has_positive_measure),
        ('biliti', 'ble', _has_positive_measure),
        ('logi', 'log', _has_positive_measure)
    ]

    return _apply_rule_list(word, rules)

def _step3(word):
    """Implements Step 3 from "An algorithm for suffix stripping"

    From the paper:

    Step 3

        (m>0) ICATE ->  IC              triplicate     ->  triplic
        (m>0) ATIVE ->                  formative      ->  form
        (m>0) ALIZE ->  AL              formalize      ->  formal
        (m>0) ICITI ->  IC              electriciti    ->  electric
        (m>0) ICAL  ->  IC              electrical     ->  electric
        (m>0) FUL   ->                  hopeful        ->  hope
        (m>0) NESS  ->                  goodness       ->  good
    """
    return _apply_rule_list(
        word,
        [
            ('icate', 'ic', _has_positive_measure),
            ('ative', '', _has_positive_measure),
            ('alize', 'al', _has_positive_measure),
            ('iciti', 'ic', _has_positive_measure),
            ('ical', 'ic', _has_positive_measure),
            ('ful', '', _has_positive_measure),
            ('ness', '', _has_positive_measure),
        ],
    )

def _step4(word):
    """Implements Step 4 from "An algorithm for suffix stripping"

    Step 4

        (m>1) AL    ->                  revival        ->  reviv
        (m>1) ANCE  ->                  allowance      ->  allow
        (m>1) ENCE  ->                  inference      ->  infer
        (m>1) ER    ->                  airliner       ->  airlin
        (m>1) IC    ->                  gyroscopic     ->  gyroscop
        (m>1) ABLE  ->                  adjustable     ->  adjust
        (m>1) IBLE  ->                  defensible     ->  defens
        (m>1) ANT   ->                  irritant       ->  irrit
        (m>1) EMENT ->                  replacement    ->  replac
        (m>1) MENT  ->                  adjustment     ->  adjust
        (m>1) ENT   ->                  dependent      ->  depend
        (m>1 and (*S or *T)) ION ->     adoption       ->  adopt
        (m>1) OU    ->                  homologou      ->  homolog
        (m>1) ISM   ->                  communism      ->  commun
        (m>1) ATE   ->                  activate       ->  activ
        (m>1) ITI   ->                  angulariti     ->  angular
        (m>1) OUS   ->                  homologous     ->  homolog
        (m>1) IVE   ->                  effective      ->  effect
        (m>1) IZE   ->                  bowdlerize     ->  bowdler

    The suffixes are now removed. All that remains is a little
    tidying up.
    """
    measure_gt_1 = lambda stem: _measure(stem) > 1

    return _apply_rule_list(
        word,
        [
            ('al', '', measure_gt_1),
            ('ance', '', measure_gt_1),
            ('ence', '', measure_gt_1),
            ('er', '', measure_gt_1),
            ('ic', '', measure_gt_1),
            ('able', '', measure_gt_1),
            ('ible', '', measure_gt_1),
            ('ant', '', measure_gt_1),
            ('ement', '', measure_gt_1),
            ('ment', '', measure_gt_1),
            ('ent', '', measure_gt_1),
            # (m>1 and (*S or *T)) ION ->
            (
                'ion',
                '',
                lambda stem: _measure(stem) > 1 and stem[-1] in ('s', 't'),
            ),
            ('ou', '', measure_gt_1),
            ('ism', '', measure_gt_1),
            ('ate', '', measure_gt_1),
            ('iti', '', measure_gt_1),
            ('ous', '', measure_gt_1),
            ('ive', '', measure_gt_1),
            ('ize', '', measure_gt_1),
        ],
    )

def _step5a(word):
    """Implements Step 5a from "An algorithm for suffix stripping"

    From the paper:

    Step 5a

        (m>1) E     ->                  probate        ->  probat
                                        rate           ->  rate
        (m=1 and not *o) E ->           cease          ->  ceas
    """
    # Note that Martin's test vocabulary and reference
    # implementations are inconsistent in how they handle the case
    # where two rules both refer to a suffix that matches the word
    # to be stemmed, but only the condition of the second one is
    # true.
    # Earlier in step2b we had the rules:
    #     (m>0) EED -> EE
    #     (*v*) ED  ->
    # but the examples in the paper included "feed"->"feed", even
    # though (*v*) is true for "fe" and therefore the second rule
    # alone would map "feed"->"fe".
    # However, in THIS case, we need to handle the consecutive rules
    # differently and try both conditions (obviously; the second
    # rule here would be redundant otherwise). Martin's paper makes
    # no explicit mention of the inconsistency; you have to infer it
    # from the examples.
    # For this reason, we can't use _apply_rule_list here.
    if word.endswith('e'):
        stem = _replace_suffix(word, 'e', '')
        if _measure(stem) > 1:
            return stem
        if _measure(stem) == 1 and not _ends_cvc(stem):
            return stem
    return word

def _step5b(word):
    """Implements Step 5a from "An algorithm for suffix stripping"

    From the paper:

    Step 5b

        (m > 1 and *d and *L) -> single letter
                                controll       ->  control
                                roll           ->  roll
    """
    return _apply_rule_list(
        word, [('ll', 'l', lambda stem: _measure(word[:-1]) > 1)]
    )

def stem(word):
    stem = word.lower()

    if len(word) <= 2:
        # With this line, strings of length 1 or 2 don't go through
        # the stemming process, although no mention is made of this
        # in the published algorithm.
        return word

    stem = _step1a(stem)
    stem = _step1b(stem)
    stem = _step1c(stem)
    stem = _step2(stem)
    stem = _step3(stem)
    stem = _step4(stem)
    stem = _step5a(stem)
    stem = _step5b(stem)

    return stem

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Print out trimmed words')
    parser.add_argument('words', metavar='W', type=str, nargs='+',
                        help='word to be trimmed')

    args = parser.parse_args()
    print(" ".join(stem(word) for word in args.words))
