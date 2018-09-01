#!/usr/bin/env python

import os
import datetime
import requests


def main():
    PRIVATE_TOKEN = os.environ['PRIVATE_TOKEN']
    URL = os.environ['WIKI_COVERAGE_URL']
    coverage = os.environ['COVERAGE']
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_sha = os.environ['CI_COMMIT_SHA']
    new_line = '| {} | {} | {} |\n'.format(time, commit_sha, coverage)
    headers = {'Private-Token': PRIVATE_TOKEN}
    response = requests.get(
        URL,
        headers=headers)
    content = response.json().get('content')
    new_content = '{}{}'.format(content, new_line)
    response = requests.put(URL, data={
        'content': new_content,
        'title': 'coverage',
    }, headers=headers)


if __name__ == '__main__':
    main()
