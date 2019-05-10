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

import regex as re
import difflib
import nltk.tokenize
from nltk.metrics import distance

from fuzzywuzzy import fuzz

def literal_text_match(chat_text, rule_text, expand_candidates=True, score_threshold=0.8):
    # check for exact token overlap first
    # logger.info("literal_text_match : %s"%(rule_text))
    tokens_to_match = nltk.tokenize.word_tokenize(rule_text)
    rule_overlap = [(match_indx.span(),
                    chat_text[match_indx.start():match_indx.end()])
                    for match_indx in
                    re.finditer("\s*".join(re.escape(tok)
                                for tok in
                                tokens_to_match),
                                chat_text, re.IGNORECASE)]
    # when we have noisy text.
    # no match found so far so expanding candidates to be matched
    if len(rule_overlap) == 0:
        overlap_candidates = [chat_text[match_indx.start():
                              (match_indx.start() + len(rule_text))]
                              for match_indx in
                              re.finditer(
                                re.escape(rule_text[0:len(rule_text.split()[0])]),
                                chat_text,
                                re.IGNORECASE)]
        if expand_candidates:
            # can't find a potential candidate starting with the first word
            # greedy add character start
            if len(overlap_candidates) == 0:
                overlap_candidates = [chat_text[match_indx.start():
                                        (match_indx.start() + len(rule_text))]
                                      for match_indx in
                                      re.finditer(
                                        re.escape(rule_text[0]),
                                        chat_text,
                                        re.IGNORECASE)]
        best_candidate = ""
        if len(overlap_candidates):
            current_edit_distance = -1
            for candidate in overlap_candidates:
                d = distance.edit_distance(candidate, rule_text)
                if current_edit_distance == -1 or d <= current_edit_distance:
                    current_edit_distance = d
                    best_candidate = candidate
            if len(best_candidate):
                candidate_score = difflib.SequenceMatcher(
                                    None,
                                    best_candidate.lower(),
                                    rule_text.lower()).ratio()
                if candidate_score > score_threshold:
                    rule_overlap = [(match_indx.span(),
                                chat_text[match_indx.start():match_indx.end()])
                                for match_indx in
                                re.finditer(re.escape(best_candidate),
                                            chat_text, re.IGNORECASE)]
    return rule_overlap
