import yaml
import argparse
import ast
import re
from mergedeep import merge
from argparse import Namespace

def dicts_to_namespaces(config) -> Namespace:
    """ 
    Translate a dictionary of dictionaries to namespaces of namespaces.  Recursively calls itself until reaching the basecase of not being a 
    dictionary, then returns the value at the leaf


    """
    if not isinstance(config, dict) and not isinstance(config, list):
        return config
    if isinstance(config, dict):
        return Namespace(**{key : dicts_to_namespaces(val) for key, val in config.items()})
    
    return [dicts_to_namespaces(val) for val in config]

class YArgumentParser(argparse.ArgumentParser):
    """
    Layer over argparse that merges YAML configuration with command line overrides.

    Allows some variables to be defined at the CLI, and others to be in the YAML.  CLI will always override
    defaults provided in YAML, if provided in both places.

    To override nested YAML use dot notation, e.g.:
    features
        dim: 100

    can be overridden via --features.dim 1000
    """
    def __init__(self, yaml_flag='-c', yaml_dest='--config', yaml_default=['config.yaml'], **kwargs):
        """
        Initialization including specifying the desired YAML file to use in command line interface.

        Example CLI: python <prog> -c / --config config.yaml

        yaml_flag: the one-dash command line shortcut (e.g., -c)
        yaml_dest: the two-dash command line arg (e.g., --config)
        yaml_default: Default value (e.g., config.yaml)
        """
        super().__init__(**kwargs)
        assert(yaml_flag is None or yaml_flag.startswith('-'))
        assert(yaml_dest.startswith('--'))
        if yaml_flag is not None:       
            self.add_argument(yaml_flag, yaml_dest, default=yaml_default, nargs='+')
        else:
            self.add_argument(yaml_dest, default=yaml_default, nargs='+')

        self.yaml_dest = yaml_dest[2:]

    def nest_dict(d):
        nested_dict = {}
        for keystr, value in d.items():
            keys = [key if '[' not in key else int(key[1:-1]) for key in re.findall(r'[a-zA-Z_0-9]+|\[[0-9]+\]', keystr)]

            root = nested_dict
            for key in keys[:-1]:
                if key not in root:
                    root[key] = {}
                root = root[key]
                    
            root[keys[-1]] = value
        return nested_dict

    def parse_args(self, args=None, handle_unk='raise') -> Namespace:
        def checkkey(d, key, handle_unk):
            if key in d:
                return True
            
            if handle_unk == 'raise':
                raise Exception(f"Override unk {key} not in config")
            
            if handle_unk == 'insert':
                root[key] = {}
                return True
            
            if handle_unk == 'pass':
                return False
            
            raise Exception(f'Unknown handle_unk = {handle_unk}')

        """
        Overrides argparse's parse_args, to first recover the yaml configuration file and other true CLI,
        then merges the other CLI with the YAML file.

        Order is:
        1) Defaults from argparse
        2) Values from configs
        3) Values from command line

        Lastly, it combines both into a dict, which is translated into a namespace
        """
        # Default arguments
        args_default, _ = super().parse_known_args([])
        args_default = vars(args_default)

        # Explicitly set through command line
        args_set, overrides = super().parse_known_args(args)
        args_set = vars(args_set)
        args_onlyset = {k : v for k, v in args_set.items() if k not in args_default or v != args_default[k]}

        args_default = YArgumentParser.nest_dict(args_default)
        args_onlyset = YArgumentParser.nest_dict(args_onlyset)

        # Load our yaml configurations
        fins = [open(c) for c in args_set[self.yaml_dest]]
        configs = [yaml.safe_load(fin) for fin in fins]
        fins = [fin.close() for fin in fins]

        config = merge(*configs)

        # Override values in the configurations
        overrides = ' '.join(overrides)
        overrides = [s.strip() for s in overrides.split('--') if s != '']

        for override in overrides:
            splitpoint_start = re.search(' |=|:', override).start()
            splitpoint_end = re.search(' |=|:', override).end()

            keystr, value = override[:splitpoint_start], override[splitpoint_end:]
            keys = [key if '[' not in key else int(key[1:-1]) for key in re.findall(r'[a-zA-Z_0-9]+|\[[0-9]+\]', keystr)]
            root = config

            set_value = True

            for key in keys[:-1]:
                if set_value := checkkey(root, key, handle_unk):
                    root = root[key]
            
            if set_value and checkkey(root, keys[-1], handle_unk):
                if type(root[keys[-1]]) != str:
                    root[keys[-1]] = ast.literal_eval(value)
                else:
                    root[keys[-1]] = value

        config = merge(args_default, config, args_onlyset)
        return dicts_to_namespaces(config)
