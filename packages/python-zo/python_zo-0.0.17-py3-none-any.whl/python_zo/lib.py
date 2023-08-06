import argparse
import configparser
import csv
import json
import os
import re

from itertools import permutations
from jinja2 import Environment, FileSystemLoader, BaseLoader
from .filters import apply_filters, first_lower, unknown_types
from .classes import Table


def load_schema(p):
	content = json.load(open(p))
	for v in content['data']:
		v['_field'] = {y['key']: y for y in v['fields']}
	content['data'].sort(key=lambda x: x["key"])
	return content


def mix_all(args):
	for x, y in permutations(args, 2):
		y_map = {yy['key']: yy for yy in y['data']}
		for v in x['data']:
			k = v['key']
			if x['kind'] == 'gql' and k not in y_map and k.startswith('Input') and k[5:] in y_map:
				k = k[5:]
			if k not in y_map: continue
			vv = y_map.get(k, {})
			v[y['kind']], f_map = vv, vv['_field']
			for f in v['fields']:
				f[y['kind']] = f_map.get(f['key']) or f_map.get(f.get('nameExact'))


def load_file(name, args):
	init_path = os.path.join(args.template_path, name)
	if os.path.exists(init_path):
		target = {}
		exec(open(init_path).read(), target)
		return target
	return {}


def walk(path):
	return [os.path.join(root, f) for root, folders, files in os.walk(path) for f in files]


def apply_vars(tpl, my_vars):
	return re.sub(r'{{\s*([^}\s]+)\s*}}', lambda x: my_vars.get(x.group(1)) or 'None', tpl)


def render_template(env, schemas, args):
	schema = schemas[0]
	tpls = set(env.list_templates())
	classes = load_file('classes.py', args)
	table = classes.get('Table', lambda x: x)

	if args.cmd == 'scaffold':
		db_model = api_field = None
		if args.graphql.count("/") != 1:
			return print('--graphql pattern should be like "Query/MySettings"')
		gql_type, gql_model = args.graphql.split("/")
		for schema in schemas:
			if schema['kind'] == 'spanner':
				for m in schema['data']:
					if m['key'] == args.model:
						db_model = m
						break
			if schema['kind'] == 'gql':
				for m in schema['data']:
					if m['key'] == gql_type:
						for f in m['fields']:
							if f['key'] == gql_model:
								api_field = f
		if not db_model:
			return print('model not specified or not found')
		if not api_field:
			return print(gql_model, 'not found')

		if args.verb.count('/') != 1:
			return print('verb must be in pattern Get/Getter')
		verb, verb_er = args.verb.split('/', maxsplit=2)

		skel_path = os.path.join(args.template_path, 'skel')
		skels = walk(skel_path)
		if not skels:
			return print('skel folder not found in template')

		for skel in skels:
			content = open(skel).read()
			# print('rendering', skel)
			env = Environment(loader=BaseLoader())
			apply_filters(env, {})
			var_filters = load_file('filters.py', args)
			custom_filters = var_filters.get('apply_filters', lambda *_: None)
			custom_filters(env, {})
			my_args = dict(
				usecase=args.usecase,
				service=first_lower(verb_er), Service=verb_er,
				apiType=first_lower(verb), ApiType=verb,
				nameType=db_model['name'] + verb, NameType=db_model['Name'] + verb,
				api=api_field,
			)
			my_vars = table(Table(db_model, **my_args))
			rel_path = apply_vars(os.path.relpath(skel, skel_path), my_vars)
			if 'None' in rel_path: continue
			template = env.from_string(content)
			output = template.render(my_vars)
			out_path = os.path.join(args.out_path, rel_path).replace('.jinja2', '').replace('.j2', '')
			if os.path.exists(out_path) and not args.force:
				print('  output file exists', os.path.relpath(rel_path))
				print(output)
			else:
				print('file written', out_path)
				with open(out_path, 'w', encoding="utf8") as dst:
					dst.write(output)

	elif args.cmd == 'generate':
		targets = {args.out_path: schema['data']} if args.one_file else {os.path.join(args.out_path, x[args.name_key] + args.suffix): [x] for x in schema['data']}

		for f, tbls in targets.items():
			type_contents = []
			type_tpls = [x for x in tpls if x.startswith("type.")]
			if type_tpls:
				template = env.get_template(type_tpls[0])
				tbl_map = {x['key']: x for x in tbls}
				for x in tbls:
					out = template.render(table(Table(x, M=tbl_map)))
					if out.strip():
						type_contents.append(out)

			headers = []
			header_tpls = [x for x in tpls if x.startswith("header.")]
			if header_tpls:
				template1 = env.get_template(header_tpls[0])
				headers.append(template1.render(tables=schema['data'], unknown_types=[y for x in tbls for y in unknown_types(x['fields'])]))

			footers = []
			footer_tpls = [x for x in tpls if x.startswith("footer.")]
			if footer_tpls:
				template3 = env.get_template(footer_tpls[0])
				footers.append(template3.render(tables=schema['data']))

			if not type_contents:
				print(f'[{os.path.basename(f)}] no template found\n')
				continue

			output = headers + type_contents + footers

			with open(f, 'w', encoding="utf8") as dst:
				dst.write('\n'.join(output))


def parse_args():
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(dest="cmd")
	subparsers.required = True

	parser_g = subparsers.add_parser('generate', help='generate')
	parser_g.add_argument('-o', '--out-path', help="output file path")
	parser_g.add_argument('--src-json-paths', nargs='+')
	parser_g.add_argument('--template-path', required=True)
	parser_g.add_argument('--one-file', action='store_true', default=False)
	parser_g.add_argument('--suffix', nargs='?', default="")
	parser_g.add_argument('--name-key', nargs='?', default="nameDb")

	parser_s = subparsers.add_parser('scaffold', help='scaffold')
	parser_s.add_argument('--model', help="spanner model (eg. User)", required=True)
	parser_s.add_argument('--graphql', help="graphql pattern (Query/MySettings or Mutation/SetSetting)", required=True)
	parser_s.add_argument('--verb', default="Get/Getter", help="verb (eg. Get/Getter or Find/Finder", required=True)
	parser_s.add_argument('--usecase', default="usecase", help="usecase rel path (eg. usecase or usecase/user)")
	parser_s.add_argument('-o', '--out-path', help="output file path")
	parser_s.add_argument('-f', '--force', help="force overwrite", action="store_true")

	args = parser.parse_args()
	# print(args)
	if args.cmd == 'scaffold' and os.path.exists('.zo'):
		config = configparser.ConfigParser()
		config.read('.zo')
		if 'scaffold' in config:
			args.src_json_paths = config['scaffold'].get('src_json_paths', '').split('\n')
			args.template_path = config['scaffold'].get('template_path')
			args.out_path = config['scaffold'].get('out_path')
	return args


def main():
	args = parse_args()
	env = Environment(loader=FileSystemLoader(args.template_path))
	mappings_path = os.path.join(args.template_path, 'mappings.csv')
	mappings = {(x[0], x[1]): x[2] for x in os.path.exists(mappings_path) and csv.reader(open(mappings_path).read().strip().splitlines()[1:]) or []
				if len(x) == 3 and x[0].strip() and x[0].strip()[0] != "#"}
	apply_filters(env, mappings)
	var_filters = load_file('filters.py', args)
	custom_filters = var_filters.get('apply_filters', lambda *_: None)
	custom_filters(env, mappings)

	schemas = [load_schema(x) for x in args.src_json_paths]
	mix_all(schemas)
	render_template(env, schemas, args)
