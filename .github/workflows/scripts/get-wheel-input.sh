#!/bin/bash
 
approval=$(gh api -H "Accept: application/vnd.github+json" "/repos/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}/approvals")
comment="$(jq -r '.[0].comment' <<< "$approval")"
echo "item_number=$comment" >> "$GITHUB_OUTPUT"
