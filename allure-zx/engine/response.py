from com.json_processor import JSONProcessor
class ResponseObject(object):

    def __init__(self, resp_obj):
        """ initialize with a requests.Response object
        @param (requests.Response instance) resp_obj
        """
        self.resp_obj = resp_obj

    def parsed_body(self):
        try:
            return self.resp_obj.json()
        except ValueError:
            return self.resp_obj.text

    def parsed_dict(self):
        body = JSONProcessor(self.parsed_body()) if self.parsed_body() != '' else None
        return {
            'status_code': self.resp_obj.status_code,
            'headers': self.resp_obj.headers,
            # 'body': self.parsed_body()
            'body': body

        }

