# iam-statement-maker

## What is this?
Writing secure IAM and SCP Policies takes a long time; you need to check the actions for the resources
and then write them into a template.  This is a lot of painful copy and paste work.

This project checks AWS for the latest actions for the resource you are writing an IAM/SCP Policy 
Statement for, it then interactively asks you which actions you would like to include in your 
statement, which effect you would like and for which resource.

## Usage
```
Usage: iam_statement_maker.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  iam  Interactive tool to generate a statement for an IAM policy.
  scp  Interactive tool to generate a statement for an SCP policy.
```

### For IAM

--service Service you want to generate a statement for
--effect effect for the actions you are specifying default='Allow'
--resource resource to apply the effect for the actions for
--add-all do not interactively ask per each action, add all instead
--wrap-in-cfn wrap the statement in a cfn template
--formatoutput you want (yaml or json) default='yaml'


### For SCP

--service Service you want to generate a statement for
--effect effect for the actions you are specifying default='Allow'
--add-all do not interactively ask per each action, add all instead


## Examples

### For IAM
Start an interactive session to specify actions, effect and resources for an s3 resource
```
python statement_maker.py iam --service s3 --resource 'arn:aws:s3:::bucket_name' --effect Allow
```
Start an interactive session to add Allow actions for s3 bucket arn:aws:s3:::bucket_name
```
python statement_maker.py iam --service s3 --resource 'arn:aws:s3:::bucket_name' --effect Allow
```
Allow all s3 actions for all resources, wrapping in cfn
```
python statement_maker.py iam --add-all --service s3 --resource '*' --effect Allow --wrap-in-cfn
```
Allow all s3 actions for all resources, wrapping in cfn using json
```
python statement_maker.py iam --add-all --service s3 --resource '*' --effect Allow --wrap-in-cfn --format json
```

### For SCP
Start an interactive session to specify actions and effect for s3
```
python statement_maker.py scp --service s3 --effect Allow
```
Start an interactive session to add Allow actions for s3
```
python statement_maker.py scp --service s3 --effect Allow
```
Allow all s3 actions
```
python statement_maker.py scp --add-all --service s3 --effect Allow
```


## Docker support
Instead of installing the python dependencies you can use a version of this using docker hub
```
docker run -it eamonnfaherty83/aws-statement-maker scp --add-all --service s3 --effect Allow
```