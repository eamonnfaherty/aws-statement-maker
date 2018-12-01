import requests
import json
import click
from yaml import safe_dump

@click.command()
@click.option('--service', prompt='Service', help='Service you want to generate a statement for')
@click.option('--effect', prompt='Allow', help='effect for the actions', default='Allow')
@click.option('--resource', prompt='Resource', help='resource to apply the effect for the actions for')
@click.option('--use_json', help='output you want (yaml or json)', is_flag=True)
@click.option('--add_all', help='add all', is_flag=True)
def generate(service, effect, resource, use_json, add_all):
	"""Interactive tool to generate a statement for an IAM policy.  Uses the latest list
of services and actions from AWS"""
	response = requests.get('https://awspolicygen.s3.amazonaws.com/js/policies.js')
	policy_editor_config = response.text.replace('app.PolicyEditorConfig=', '')
	service_map = json.loads(policy_editor_config).get('serviceMap')

	for long_name, details in service_map.items():
		if service in [long_name.lower(), details.get('StringPrefix').lower()]:
			statement = {}
			statement['Effect'] = effect
			statement['Resource'] = resource
			statement['Actions'] = []
			for action in details.get('Actions'):
				if not add_all:
					include = raw_input("action: {} N/y ".format(action))
					if include.lower() == 'y':
						statement['Actions'].append("{}:{}".format(details.get('StringPrefix'), action))
				else:
						statement['Actions'].append("{}:{}".format(details.get('StringPrefix'), action))
			if use_json:
				print json.dumps(statement)
			else:
				print safe_dump(statement)

if __name__ == '__main__':
    generate()
