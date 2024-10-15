import json

class FuncResponse():
    def __init__(self, response_code: int, response_data: str):
        self.response_code = response_code
        self.response_data = response_data


    