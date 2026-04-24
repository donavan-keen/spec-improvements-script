#! /usr/bin/env bash
current_dir=$(pwd)
cd $1
# After
gh run list -L 1000 -w "Spec CI" --created ">2026-03-25" -s completed --json status,conclusion,workflowName,startedAt,updatedAt --template '{{range .}}{{ .workflowName }},{{ .status }},{{ .conclusion }},{{ .startedAt }},{{ .updatedAt }}{{"\n"}}{{end}}' >$current_dir/tmp/after.csv

# Before:
gh run list -L 1000 -w "Spec CI" --created "2026-01-12..2026-02-10" -s completed --json status,conclusion,workflowName,startedAt,updatedAt --template '{{range .}}{{ .workflowName }},{{ .status }},{{ .conclusion }},{{ .startedAt }},{{ .updatedAt }}{{"\n"}}{{end}}' >$current_dir/tmp/before.csv

cd $current_dir
