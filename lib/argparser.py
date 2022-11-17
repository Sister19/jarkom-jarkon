from argparse import ArgumentParser

# class to parse user input
class Arguments:
    def __init__(self):
        self.parser = ArgumentParser()
    
    def add_args(self, args: str, desc: str, type_input: type):
        self.parser.add_argument(args, help=desc, type = type_input)
        return self

    def get_attribute(self, attrname: str):
        return self.parser.parse_args().__getattribute__(attrname)