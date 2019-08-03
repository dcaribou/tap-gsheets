#!/usr/bin/env bats

@test "read a single worksheet" {
  run tap-gsheets -c config.conf --overrides '{"sheet_name": "Tap Gsheets Integration Tests"}'

  [ $status -eq 0 ]
  [ $(echo ${lines[*]} | jq --compact-output 'select(.type=="SCHEMA")' | wc -l) -eq 1 ]
  [ $(echo ${lines[*]} | jq --compact-output 'select(.type=="RECORD")' | wc -l) -eq 2 ]
}

@test "read a two worksheets in the same spreadsheet" {
  run tap-gsheets \
    -c config.conf \
    --overrides '{"sheets": [{"name": "Tap Gsheets Integration Tests", "worksheets":["Sheet1","OtherWorksheet"]}]}'

  [ $status -eq 0 ]
  [ $(echo ${lines[*]} | jq --compact-output 'select(.type=="SCHEMA")' | wc -l) -eq 2 ]
  [ $(echo ${lines[*]} | jq --compact-output 'select(.type=="RECORD")' | wc -l) -eq 4 ]
}
