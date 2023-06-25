from dataclasses import dataclass

@dataclass
class ResponseData():
    message:str = '성공'
    data: any = None

    def builder(self, data, message):

        context = {
            'message': message,
            'data': data,
        }
        return context
