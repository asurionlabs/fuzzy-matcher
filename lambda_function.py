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

import json
import fuzzy_match


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):

    operation = event['httpMethod']
    if operation == "POST":
        payload = json.loads(event['body'])
        #print("payload: " + str(payload))

        response = { 'status' : 'OK'}
        response['output'] = fuzzy_match.match(payload['text'], payload['candidates'])

        return respond(None, response)
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))

