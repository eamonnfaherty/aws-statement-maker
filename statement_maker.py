import requests
import json
import click
from yaml import dump
import yaml


class Sub(object):
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.string


def sub_representer(dumper, data):
    return dumper.represent_scalar(u'!Sub', data.string)


yaml.add_representer(Sub, sub_representer)


def get_details_for_service(service):
    response = requests.get('https://awspolicygen.s3.amazonaws.com/js/policies.js')
    policy_editor_config = response.text.replace('app.PolicyEditorConfig=', '')
    service_map = json.loads(policy_editor_config).get('serviceMap')
    for long_name, details in service_map.items():
        if service in [long_name.lower(), details.get('StringPrefix').lower()]:
            return details


def get_statement(details, effect, add_all):
    statement = {
        'Effect': str(effect),
        'Action': []
    }
    for action in details.get('Actions'):
        if not add_all:
            include = raw_input("action: {} N/y ".format(action))
            if include.lower() == 'y':
                statement['Action'].append("{}:{}".format(details.get('StringPrefix'), action))
        else:
            statement['Action'].append("{}:{}".format(details.get('StringPrefix'), action))
    return statement


def print_it(statement, params):
    if params.get('format') == 'json':
        print json.dumps(statement)
    else:
        print dump(statement, default_flow_style=False)


@click.group()
@click.pass_context
def main(ctx):
    pass


@main.command()
@click.option('--service', prompt='Service', help='Service you want to generate a statement for')
@click.option('--effect', prompt='Allow', help='effect for the actions you are specifying', default='Allow')
@click.option('--resource', prompt='Resource', help='resource to apply the effect for the actions for')
@click.option('--add-all', help='do not interactively ask per each action, add all instead', is_flag=True)
@click.option('--wrap-in-cfn', help='wrap the statement in a cfn template', is_flag=True)
@click.option('--format', type=click.Choice(['yaml', 'json']), help='output you want (yaml or json)', default='yaml')
@click.pass_context
def iam(ctx, service, effect, resource, add_all, wrap_in_cfn, format):
    """Interactive tool to generate a statement for an IAM policy.  Uses the latest list of services and actions
    from AWS"""
    details = get_details_for_service(service)
    statement = get_statement(details, effect, add_all)
    statement['Resource'] = str(resource)
    if wrap_in_cfn:
        statement = {
            "Parameters": {
                "ManagedPolicyName": {
                    "Type": "String"
                }
            },
            "Resources": {
                "Policy": {
                    "Type": "AWS::IAM::ManagedPolicy",
                    "Properties": {
                        "ManagedPolicyName": Sub(u'${ManagedPolicyName}') if format == 'yaml' else {
                            "Fn::Sub": '${ManagedPolicyName}'},
                        "PolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": [statement]
                        }
                    }
                }
            }
        }
    print_it(statement, ctx.params)


@main.command()
@click.option('--service', prompt='Service', help='Service you want to generate a statement for')
@click.option('--effect', prompt='Allow', help='effect for the actions you are specifying', default='Allow')
@click.option('--add-all', help='do not interactively ask per each action, add all instead', is_flag=True)
@click.pass_context
def scp(ctx, service, effect, add_all):
    """Interactive tool to generate a statement for an SCP policy.  Uses the latest list of services and actions
    from AWS"""
    details = get_details_for_service(service)
    statement = get_statement(details, effect, add_all)
    ctx.params.update()
    print json.dumps(statement)


if __name__ == '__main__':
    main()
