#!/usr/bin/env bash

# Use this one-liner to produce a JSON literal from the Git log:
git checkout -b master
git log \
    --pretty=format:'{%n  "commit": "%H",%n  "author": "%aN <%aE>",%n  "date": "%ad",%n  "message": "%f"%n},' \
    $@ | \
    perl -pe 'BEGIN{print "["}; END{print "]\n"}' | \
    perl -pe 's/},]/}]/' > './static/log.json'
