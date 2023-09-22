"""Typing test implementation"""
import sys

from utils import *
from ucb import main, interact, trace
from datetime import datetime

HW_SOURCE_FILE = 'cats.py'


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.

    >>> ps = ['short', 'really long', 'tiny']
    >>> s = lambda p: len(p) <= 5
    >>> choose(ps, s, 0)
    'short'
    >>> choose(ps, s, 1)
    'tiny'
    >>> choose(ps, s, 2)
    ''
    """
    for i in paragraphs:
        if not select(i):
            paragraphs.remove(i)
    if k >= len(paragraphs):
        return ''
    else:
        return paragraphs[k]


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    >>> dogs = about(['dogs', 'hounds'])
    >>> dogs('"DOGS" stands for Department of Geophysical Science.')
    True
    >>> dogs("Do gs and ho unds don't count")
    False
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'

    def f(paragraph):
        for word in topic:
            if word in paragraph.lower():
                return True
        return False

    return f


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy("12345", "12345")
    100.0
    >>> accuracy("a  b  c  d", "b  a  c  d")
    50.0
    >>> accuracy("Cat", "cat")
    0.0
    >>> accuracy("cats.", "cats")
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    if len(typed_words) == 0:
        return 0.0
    leng = min(len(typed_words), len(reference_words))
    count = 0
    for i in range(leng):
        if typed_words[i] == reference_words[i]:
            count += 1
    return count / len(typed_words) * 100


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.
    
    >>> wpm("12345", 3)
    20.0
    >>> wpm("", 10)
    0.0
    >>> wpm("a b c", 20)
    3.0
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    return len(typed) / 5 / (elapsed / 60)


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.

    >>> abs_diff = lambda w1, w2, limit: abs(len(w2) - len(w1))
    >>> autocorrect("cul", ["culture", "cult", "cultivate"], abs_diff, 10)
    'cult'
    >>> autocorrect("cul", ["culture", "cult", "cultivate"], abs_diff, 0)
    'cul'
    >>> autocorrect("wor", ["worry", "car", "part"], abs_diff, 10)
    'car'
    """
    if user_word in valid_words:
        return user_word
    minlen = limit + 1
    ans = user_word
    for i in valid_words:
        j = diff_function(user_word, i, limit)
        if j < minlen:
            minlen = j
            ans = i
    return ans


def sphinx_swap(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.

    >>> big_limit = 10
    >>> sphinx_swap("car", "cad", big_limit)
    1
    >>> sphinx_swap("this", "that", big_limit)
    2
    >>> sphinx_swap("one", "two", big_limit)
    3
    >>> sphinx_swap("awful", "awesome", 3) > 3
    True
    >>> sphinx_swap("awful", "awesome", 4) > 4
    True
    >>> from construct_check import check
    >>> # ban while or for loops
    >>> check(HW_SOURCE_FILE, 'missing_digits', ['While', 'For'])
    True
    """
    if len(start) == 0:
        return len(goal)
    a = sphinx_swap(start[1:], goal[1:], limit)
    return a if start[0] == goal[0] else 1 + a


def feline_fixes(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL.
    
    >>> big_limit = 10
    >>> feline_fixes("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> feline_fixes("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> feline_fixes("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    >>> limit = 2
    >>> feline_fixes("ckiteus", "kittens", limit) > limit
    True
    >>> sphinx_swap("ckiteusabcdefghijklm", "kittensnopqrstuvwxyz", limit) > limit
    True
    """
    if len(start) == 0:
        return len(goal)
    elif len(goal) == 0:
        return len(start)
    if start[0] == goal[0]:
        return feline_fixes(start[1:], goal[1:], limit)
    else:
        return 1 + min(min(feline_fixes(start, goal[1:], limit), feline_fixes(start[1:], goal, limit)),
                       feline_fixes(start[1:], goal[1:], limit))


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server.
    
    >>> typed = ['I', 'have', 'begun']
    >>> prompt = ['I', 'have', 'begun', 'to', 'type']
    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> report_progress(typed, prompt, 1, print_progress) # print_progress is called on the report
    ID: 1 Progress: 0.6
    0.6
    >>> report_progress(['I', 'begun'], prompt, 2, print_progress)
    ID: 2 Progress: 0.2
    0.2
    >>> report_progress(['I', 'hve', 'begun', 'to', 'type'], prompt, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    i = 0
    while i < len(typed):
        if typed[i] == prompt[i]:
            i += 1
        else:
            break
    progress = i / len(prompt)
    d = {}
    d['id'] = id
    d['progress'] = progress
    send(d)
    return progress


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.

    >>> p = [[1, 4, 6, 7], [0, 4, 6, 9]]
    >>> words = ['This', 'is', 'fun']
    >>> game = time_per_word(p, words)
    >>> all_words(game)
    ['This', 'is', 'fun']
    >>> all_times(game)
    [[3, 2, 1], [4, 2, 3]]
    >>> p = [[0, 2, 3], [2, 4, 7]]
    >>> game = time_per_word(p, ['hello', 'world'])
    >>> word_at(game, 1)
    'world'
    >>> all_times(game)
    [[2, 1], [2, 3]]
    >>> time(game, 0, 1)
    1
    """
    times = []
    for i in times_per_player:
        tmp = []
        for j in range(1, len(i)):
            tmp.append(i[j] - i[j - 1])
        times.append(tmp)
    ans = game(words, times)
    return ans


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest

    >>> p0 = [2, 2, 3]
    >>> p1 = [6, 1, 2]
    >>> fastest_words(game(['What', 'great', 'luck'], [p0, p1]))
    [['What'], ['great', 'luck']]
    >>> p0 = [2, 2, 3]
    >>> p1 = [6, 1, 3]
    >>> fastest_words(game(['What', 'great', 'luck'], [p0, p1]))  # with a tie, choose the first player
    [['What', 'luck'], ['great']]
    >>> p2 = [4, 3, 1]
    >>> fastest_words(game(['What', 'great', 'luck'], [p0, p1, p2]))
    [['What'], ['great'], ['luck']]
    """
    words = all_words(game)  # An index for each word
    times = all_times(game)  # An index for each player
    ans = []
    for i in range(len(times)):
        ans.append([])
    for i in range(len(times[0])):
        minnum = sys.maxsize
        minindex = -1
        for j in range(len(times)):
            if times[j][i] < minnum:
                minnum = times[j][i]
                minindex = j
        ans[minindex].append(words[i])
    return ans


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
