from BaseResponse import BaseResponse

class RespondWithItem(BaseResponse):

    def transform(self, result, transformer, status_code=None, message=None, api_code=None):
        if status_code:
            BaseResponse.status_code = status_code

        if message:
            BaseResponse.message = message

        if api_code:
            BaseResponse.api_code = api_code

        BaseResponse.data = transformer.transform(result)
        return self.handle()