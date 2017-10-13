import yaml

with open("first_yaml_example.yaml", 'r') as stream:
    for x in yaml.load_all(stream):
        print(x)
        print(type(x))
