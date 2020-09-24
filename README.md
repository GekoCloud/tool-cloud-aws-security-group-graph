# Tool description

Displays your current AWS SecurityGroups dependencies as a Directed Graph. It's
specially helpful when trying to have an overview of the current status, being
able to easily recognize the dependencies between them and quickly identify any
security issue

## Previous requirements

This tool is intended to run on Debian/Ubuntu

```bash
sudo apt install graphviz
```

## Python requirements

1. Python 3.5+
1. Python venv

```bash
sudo apt install python3 python3-venv python3-pip
```

## Prepare the Python environment

```bash
cd security-group-graph
python3 -m venv .
. bin/activate
pip install -r requirements.txt
```

## Set AWS credentials

Ensure you have set your AWS credentials at `~/.aws/credentials`

```ini
[MyProfile]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
region = us-west-2
```

## Plot graph

Generates a PDF containing the directed graph that represents the dependencies
between the AWS SecurityGroups

### Make it executable

```bash
chmod u+x main.py
```

### Show options

```bash
./main.py -h
```

### Run example

```bash
./main.py --ignore "SGforDB" "default" --color 22=red 80=blue 443=blue --aws-profile MyProfile --aws-region us-west-2
```
