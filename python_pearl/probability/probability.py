#/usr/local/env python3
#-*- coding:utf-8 -*-

'''概率论'''

from fractions import Fraction
# from __future__ import division

def P(event, space): 
    """The probability of an event, given a sample space of equiprobable outcomes.
    event can be either a set of outcomes, or a predicate (true for outcomes in the event)."""
    if callable(event):
        event = such_that(event, space)
    return Fraction(len(event & space), len(space))

def such_that(predicate, collection): 
    "The subset of elements in the collection for which the predicate is true."
    return {e for e in collection if predicate(e)}


def even(n): return n % 2 == 0



D = {1, 2, 3, 4, 5, 6}

print(such_that(even, D))
print(P(even, D))


D12 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

print(such_that(even, D12))

print(P(even, D12))


S = {'BG', 'BB', 'GB', 'GG'}

def two_boys(outcome): return outcome.count('B') == 2

def older_is_a_boy(outcome): return outcome.startswith('B')


P(two_boys, such_that(older_is_a_boy, S))

def at_least_one_boy(outcome): return 'B' in outcome

print(P(two_boys, such_that(at_least_one_boy, S)))

print(such_that(at_least_one_boy, S))


sexesdays = {sex + day 
             for sex in 'GB' 
             for day in '1234567'}

S3        = {older + younger 
             for older in sexesdays 
             for younger in sexesdays}

print(sorted(S3))

P(at_least_one_boy, S3)

P(at_least_one_boy, S)
P(two_boys, S3)
P(two_boys, S)
P(two_boys, such_that(at_least_one_boy, S3))
P(two_boys, such_that(at_least_one_boy, S))

def at_least_one_boy_tues(outcome): return 'B3' in outcome
P(two_boys, such_that(at_least_one_boy_tues, S3))

def observed_boy_tues(outcome): return 'b3' in outcome

S3b = {older + younger + '/' + observation
       for older in sexesdays 
       for younger in sexesdays
       for observation in [older.lower()+'??', '??'+younger.lower()]}

P(two_boys, such_that(observed_boy_tues, S3b))

from IPython.display import HTML

def table(space, n=1, event=two_boys, condition=older_is_a_boy):
    """Display sample space in a table, color-coded: green if event and condition is true; 
    yellow if only condition is true; white otherwise."""
    # n is the number of characters that make up the older child.
    olders = sorted(set(outcome[:n] for outcome in space))
    return HTML('<table>' +
                cat(row(older, space, event, condition) for older in olders) +
                '</table>' + 
                str(P(event, such_that(condition, space))))

def row(older, space, event, condition):
    "Display a row where an older child is paired with each of the possible younger children."
    thisrow = sorted(outcome for outcome in space if outcome.startswith(older))
    return '<tr>' + cat(cell(outcome, event, condition) for outcome in thisrow) + '</tr>'

def cell(outcome, event, condition): 
    "Display outcome in appropriate color."
    color = ('lightgreen' if event(outcome) and condition(outcome) else
             'yellow' if condition(outcome) else
             'ghostwhite')
    return '<td style="background-color: {}">{}</td>'.format(color, outcome)    

cat = ''.join

with open('demo.html', mode='w', encoding='utf‐8') as a_file:
    a_file.write(table(S, 1, two_boys, older_is_a_boy))
	# a_file.write(table(S, 1, two_boys, at_least_one_boy))
	table(S3, 2, two_boys, at_least_one_boy)
	table(S3, 2, two_boys, at_least_one_boy_tues)

B = {'heads/Monday/interviewed', 'heads/Tuesday/sleep',
     'tails/Monday/interviewed', 'tails/Tuesday/interviewed'}
def T(property):
    "Return a predicate that is true for all outcomes that contain the property as a substring."
    return lambda outcome: property in outcome

heads = T("heads")
interviewed = T("interviewed")

P(heads, such_that(interviewed, B))
P(heads, B) 







