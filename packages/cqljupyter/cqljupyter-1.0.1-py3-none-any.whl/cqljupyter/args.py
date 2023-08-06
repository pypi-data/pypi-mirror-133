import argparse

parser = argparse.ArgumentParser()
parser.add_argument('host', nargs='?', default="127.0.0.1")
parser.add_argument('port', nargs='?')
parser.add_argument('-u', type=str)
parser.add_argument('-p', type=str)
parser.add_argument('--ssl', action='store_true')
args = parser.parse_args()

print(f"{args.host} {args.port} User {args.u} Password {args.p} ssl={args.ssl}")
