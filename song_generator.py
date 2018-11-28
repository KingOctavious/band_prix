from lexicon import Lexicon
from part_of_speech import Part_Of_Speech as pos
import lexicons as lex
import random


def build_predicate_structure():
  pred_structure = []

  structure_options = [
    [pos.ARTICLE_OR_POSS_PRONOUN, pos.NOUN],
    [pos.ARTICLE_OR_POSS_PRONOUN, pos.ADJECTIVE, pos.NOUN],
    [pos.ARTICLE_OR_POSS_PRONOUN, pos.ADJECTIVE, pos.ADJECTIVE, pos.NOUN],
    [pos.PL_NOUN],
    [pos.ADJECTIVE, pos.PL_NOUN]
  ]

  CHANCE_FOR_DUAL_PRED = 10
  preds = 1
  if random.uniform(0, 99) <= CHANCE_FOR_DUAL_PRED:
    preds = 2

  for x in range(0, preds):
    chosen_structure = structure_options[random.randint(0, len(structure_options) - 1)]
    for item in chosen_structure:
      pred_structure.append(item)

    if preds > 1 and x < preds - 1:
      pred_structure.append(pos.AND)

  return pred_structure


def build_predicate(predicate_structure, lexicon, preferred_noun_group='', theme_heavily_weighted=False):
  predicate = []

  use_preferred_noun_group = False
  if preferred_noun_group != '':
    CHANCE_TO_USE_PREFERRED = 20
    if theme_heavily_weighted:
      CHANCE_TO_USE_PREFERRED = 50
    use_preferred_noun_group = random.uniform(0, 99) <= CHANCE_TO_USE_PREFERRED

  if use_preferred_noun_group:
    return preferred_noun_group

  else:
    for item in predicate_structure:
      predicate.append(lexicon.get_word(item))

    return ' '.join(predicate)


def build_subject_structure():
  subject_structure = []

  subjects = 1

    # Disabling > 1 subjects for now. Usually sounds awkward 
  # in current construction.
  # CHANCE_FOR_DUAL_SUBJECT = 10
  # if random.uniform(0, 99) <= CHANCE_FOR_DUAL_SUBJECT:
  #   subjects = 2

  CHANCE_FOR_LONE_PRONOUN = 80
  for x in range(0, subjects):
    if random.uniform(0, 99) <= CHANCE_FOR_LONE_PRONOUN:
      structure_options = [[pos.PRONOUN]]

    else:
      structure_options = [
        [pos.ARTICLE_OR_POSS_PRONOUN, pos.NOUN],
        [pos.ARTICLE_OR_POSS_PRONOUN, pos.ADJECTIVE, pos.NOUN],
        [pos.ARTICLE_OR_POSS_PRONOUN, pos.ADJECTIVE, pos.ADJECTIVE, pos.NOUN],
        [pos.PL_NOUN],
        [pos.ADJECTIVE, pos.PL_NOUN]
      ]

    chosen_structure = structure_options[random.randint(0, len(structure_options) - 1)]
    for item in chosen_structure:
      subject_structure.append(item)

    if subjects > 1 and x < subjects - 1:
      subject_structure.append(pos.AND)

  return subject_structure


def build_subject(subject_structure, lexicon, preferred_noun_group='', theme_heavily_weighted=False):
  subject = []

  use_preferred_noun_group = False
  if preferred_noun_group != '':
    CHANCE_TO_USE_PREFERRED = 20
    if theme_heavily_weighted:
      CHANCE_TO_USE_PREFERRED = 50
    use_preferred_noun_group =  random.uniform(0, 99) <= CHANCE_TO_USE_PREFERRED

  if use_preferred_noun_group:
    return preferred_noun_group

  else:
    for x in range(0, len(subject_structure)):
      new_word = lexicon.get_word(subject_structure[x])
      if x - 1 >= 0:
        if subject[x - 1] == 'and':
          # If first word is "I", change it, because that causes some awkward
          # phrasing.
          while subject[x - 2] == 'I':
            subject[x - 2] = lexicon.get_word(subject_structure[x - 2])
          # Then make sure the word after "and" is different from the word
          # before "and".
          while new_word == subject[x - 2]:
            new_word = lexicon.get_word(subject_structure[x])

      subject.append(new_word)

    return ' '.join(subject)


def build_line(lexicon, theme_noun_group='', theme_heavily_weighted=False):
  # If there is a theme_noun_group, let it only apply to subject OR predicate,
  # not both.
  #
  # Remember that this only allows the CHANCE that the theme will be used.
  subj_or_pred = random.uniform(1, 20)

  if (subj_or_pred <= 10):
    subj = build_subject(build_subject_structure(), lexicon, theme_noun_group, theme_heavily_weighted)
    pred = build_predicate(build_predicate_structure(), lexicon)  
  else:
    subj = build_subject(build_subject_structure(), lexicon)
    pred = build_predicate(build_predicate_structure(), lexicon, theme_noun_group, theme_heavily_weighted)  

  verb = lexicon.get_word(pos.VERB)

  return subj + ' ' + verb + ' ' + pred


# build_song
#
# Returns title:lyrics tuple
def build_song(lexicon):
  theme_noun_group = build_predicate(build_predicate_structure(), lexicon)
  # To keep things interesting, avoid a theme of simply "I"
  while theme_noun_group == 'I':
    theme_noun_group = build_predicate(build_predicate_structure(), lexicon)

  # `True` argument means high chance to use theme in refrain
  refrain = build_line(lexicon, theme_noun_group, True)
  refrain = refrain[0].upper() + refrain[1:]

  lyrics = []
  for x in range(0, 8):
    line = ''
    # Chance for conjunction every other line
    if random.randint(0, 1) == 1 and x % 2 == 1:
      line += lexicon.get_word(pos.CONJUNCTION) + ' '
    line += build_line(lexicon, theme_noun_group)
    line = line[0].upper() + line[1:]
    lyrics.append(line)

  exclamation = lexicon.get_word(pos.EXCLAMATION)
  exclamation = exclamation[0].upper() + exclamation[1:]

  lyrics.insert(4, refrain)
  lyrics.insert(4, refrain)
  lyrics.insert(4, exclamation)
  lyrics.append(refrain)
  lyrics.append(refrain)

  title_options = [
    theme_noun_group, 
    refrain,
    lyrics[0]
  ]

  title = title_options[random.randint(0, len(title_options) - 1)].title()
  
  return (title, lyrics)
