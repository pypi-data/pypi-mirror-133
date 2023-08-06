import json


def pretty_dict(dct: dict, secrets_hidden: bool = True):
    for key in dct.keys():
        if secrets_hidden and key in ('login', 'username', 'password'):
            dct[key] = '*' * len(dct[key])

    return f'\n{json.dumps(dct, indent=4, sort_keys=True)}'
