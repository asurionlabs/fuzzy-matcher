###
# Fuzzy Matcher is an AWS Lambda interface to perform fuzzy matching.
# Fuzzy matching is useful for comparing if string are similar but not necessarily
# exact, such as the spelling of a person's name compared to the name in a contact 
# database.
# 
# Copyright (C) 2018-2019  Asurion, LLC
#
# Fuzzy Matcher is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Fuzzy Matcher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Fuzzy Matcher.  If not, see <https://www.gnu.org/licenses/>.
###

from fuzzywuzzy import fuzz
from ruleparser import literal_text_match

def fuzzy_compare(text, candidates, expand_candidates=True, score_threshold=0.5):
    #print("fuzzy_compare : {0}".format(candidates))
    overlap = []
    for rule_text in candidates:
        rule_overlap = literal_text_match(text, rule_text, expand_candidates, score_threshold)
        #print(rule_overlap)
        if len(rule_overlap) == 0 and len(text) < 2*len(rule_text):
            rule_overlap = [((0, len(text)), text)]

        overlap.append((rule_text, rule_overlap))
    return [(candidate, match[0][1], fuzz.token_sort_ratio(candidate, match[0][1]))
                if len(match) else (candidate, "", 0) for candidate, match in overlap]


def match(text, candidates):
    response_matches = []
    try:
        matches = fuzzy_compare(text, candidates)
        for match in matches:
            response_matches.append({"candidate":match[0], "match":match[1], "score":match[2]})
    except Exception as e:
        print('Error: {0}'.format(e))
    return response_matches
