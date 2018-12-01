# iam-statement-maker

## What is this?
Writing secure IAM Policies takes a long time; you need to check the actions for the resources
and then write them into a template.  This is a lot of painful copy and paste work.

This project checks AWS for the latest actions for the resource you are writing an IAM Policy 
Statement for, it then interactively asks you which actions you would like to include in your 
statement, which effect you would like and for which resource.

## Usage
```
Usage: iam_statement_maker.py [OPTIONS]

  Interactive tool to generate a statement for an IAM policy.  Uses the
  latest list of services and actions from AWS

Options:
  --service TEXT   Service you want to generate a statement for
  --effect TEXT    effect for the actions you are specifying
  --resource TEXT  resource to apply the effect for the actions for
  --use_json       output you want (yaml or json)
  --add_all        do not interactively ask per each action, add all instead
  --help           Show this message and exit.
```


## Examples
Start an interactive session to specify actions, effect and resources for an s3 resource
```
python iam_statement_maker.py --service s3 --resource 'arn:aws:s3:::bucket_name' --effect Allow
```
Start an interactive session to add Allow actions for s3 bucket arn:aws:s3:::bucket_name
```
python iam_statement_maker.py --service s3 --resource 'arn:aws:s3:::bucket_name' --effect Allow
```
Allow all s3 actions for all resources
```
python iam_statement_maker.py --add_all --service s3 --resource '*' --effect Allow
```
