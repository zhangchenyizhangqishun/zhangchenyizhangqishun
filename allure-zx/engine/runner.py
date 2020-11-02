import requests

from engine import response
from engine.client import HttpSession
from engine.context import Context


class Runner(object):

    def __init__(self, http_client_session=None):
        #self.http_client_session = http_client_session
        # self.http_client_session = http_client_session or requests.Session()
        self.http_client_session = http_client_session or HttpSession()

        self.context = Context()

    def init_config(self, config_dict, level):
        """ create/update context variables binds
        @param (dict) config_dict
            {
                "name": "description content",
                "requires": ["random", "hashlib"],
                "function_binds": {
                    "gen_random_string": \
                        "lambda str_len: ''.join(random.choice(string.ascii_letters + \
                        string.digits) for _ in range(str_len))",
                    "gen_md5": \
                        "lambda *str_args: hashlib.md5(''.join(str_args).\
                        encode('utf-8')).hexdigest()"
                },
                "import_module_functions": ["test.data.debugtalk"],
                "variable_binds": [
                    {"TOKEN": "debugtalk"},
                    {"random": "${gen_random_string(5)}"},
                ]
            }
        @param (str) context level, testcase or testset
        """
        self.context.init_context(level)

        requires = config_dict.get('requires', [])
        self.context.import_requires(requires)

        function_binds = config_dict.get('function_binds', {})
        self.context.bind_functions(function_binds, level)

        module_functions = config_dict.get('import_module_functions', [])
        self.context.import_module_functions(module_functions, level)

        variable_binds = config_dict.get('variable_binds', [])
        self.context.bind_variables(variable_binds, level)

        request_config = config_dict.get('request', {})
        if level == "testset":
            base_url = request_config.pop("base_url", None)
            self.http_client_session = self.http_client_session or HttpSession(base_url)
        else:
            # testcase
            self.http_client_session = self.http_client_session or requests.Session()
        self.context.register_request(request_config, level)

    def run_test(self, url,method,params):

        if str(type(self.http_client_session)).startswith("<class 'locust.clients.HttpSession'>") and method is 'GET':
            # locust show get url with group
            resp = self.http_client_session.get(url=url, params=params, name=url)
        else:
            resp = self.http_client_session.request(url=url, method=method, **params)
        return resp
        # resp_obj = response.ResponseObject(resp)
        # print 'resp_obj = %s'%resp_obj.parsed_dict()
        # return resp_obj.parsed_dict()


    def run_testset(self, testset):
        """ run single testset, including one or several testcases.
        @param (dict) testset
            {
                "name": "testset description",
                "config": {
                    "name": "testset description",
                    "requires": [],
                    "function_binds": {},
                    "variable_binds": [],
                    "request": {}
                },
                "testcases": [
                    {
                        "name": "testcase description",
                        "variable_binds": {}, # optional, override
                        "request": {},
                        "extract_binds": {},  # optional
                        "validators": {}      # optional
                    },
                    testcase12
                ]
            }
        @return (list) test results of testcases
            [
                (success, diff_content),    # testcase1
                (success, diff_content)     # testcase2
            ]
        """
        results = []

        config_dict = testset.get("config", {})
        self.init_config(config_dict, level="testset")
        testcases = testset.get("testcases", [])
        for testcase in testcases:
            result = self.run_test(testcase)
            results.append(result)

        return results

    def run_testsets(self, testsets):
        """ run testsets, including one or several testsets.
        @param testsets
            [
                testset1,
                testset2,
            ]
        @return (list) test results of testsets
            [
                [   # testset1
                    (success, diff_content),    # testcase11
                    (success, diff_content)     # testcase12
                ],
                [   # testset2
                    (success, diff_content),    # testcase21
                    (success, diff_content)     # testcase22
                ]
            ]
        """
        return [self.run_testset(testset) for testset in testsets]
