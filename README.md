# Noun Group Tagger

## Description
Creates a program that takes a file like WSJ_02-21.pos-chunk as input and produces a file consisting of feature value pairs for use with the maxent trainer and classifier. 

## Features
* Features of the word itself: POS, bio, word, capitalization
* Implemented a check to see whether word is a name or not
* Used a dictionary of words that may indicate a name (Mr., Mrs, Dr., etc)
  * Words that followed these terms and were captilized were termed names
  * Words that followed/preceded names that were capitilized were also deemed names as they are most likely part of the same name
* Implemented a check to see whether word is an organization or not
  * Used a dictionary of words that may indicate an org (Inc., Incorporated, Co.)
  * Words that preceded/follwed words with organization tag and that were capitilized also were tagged as organization
* Applied above features to previous/next 6 words

## Score
31390 out of 32853 tags correct
  accuracy: 95.55
8378 groups in key
8870 groups in response
7624 correct groups
  precision: 85.95
  recall:    91.00
  F1:        88.40
