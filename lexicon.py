from part_of_speech import Part_Of_Speech as pos
import random

class Lexicon:
  articles_and_possessive_pronouns = [
    'her',
    'his',
    'my',
    'our',
    'the',
    'their',
    'your'
  ]

  conjunctions = [
    'and',
    'but',
    'yet',
    'so'
  ]

  pronouns = [
    'he',
    'I',
    'she',
    'someone',
    'they',
    'you'
  ]

  def __init__(self, name, nouns, verbs, adjectives):
    self.name = name
    self.nouns = nouns
    self.verbs = verbs
    self.adjectives = adjectives

  def get_word(self, part_of_speech, index=-1):
    PART_OF_SPEECH_GROUPS = {
      pos.ADJECTIVE: self.adjectives,
      pos.AND: ['and'],
      pos.ARTICLE_OR_POSS_PRONOUN: self.articles_and_possessive_pronouns,
      pos.CONJUNCTION: self.conjunctions,
      pos.NOUN: self.nouns,
      pos.PL_NOUN: self.nouns,
      pos.PRONOUN: self.pronouns,
      pos.VERB: self.verbs
    }

    if index == -1:
      index = round(random.uniform(0, len(PART_OF_SPEECH_GROUPS[part_of_speech]) - 1))

    word = '' # Just to be safe

    # Nouns and plural nouns exist together inside lists withinin the 
    # `self.nouns` list, so we have to treat them a bit differently.
    if part_of_speech == pos.NOUN:
      word = self.nouns[index][0]
    elif part_of_speech == pos.PL_NOUN:
      found = False
      while not found:
        noun_group = self.nouns[index]
        if len(noun_group) == 2:
          word = noun_group[1]
          found = True
        else:
          index += 1
          if index >= len(self.nouns) - 1:
            index = 0

    # We also treat a couple other parts of speech a little bit differently to
    # give certain words a greater chance of being used.
    elif part_of_speech == pos.PRONOUN:
      CHANCE_FOR_I = 50
      if random.uniform(0, 99) <= CHANCE_FOR_I:
        word = 'I'
      else:
        word = self.pronouns[index]

    elif part_of_speech == pos.ARTICLE_OR_POSS_PRONOUN:
      CHANCE_FOR_THE = 80
      if random.uniform(0, 99) <= CHANCE_FOR_THE:
        word = 'the'
      else:
        word = self.articles_and_possessive_pronouns[index]

    else:
      word = PART_OF_SPEECH_GROUPS[part_of_speech][index]

    return word
