class ResponseHandler:

    @classmethod
    def success(
        cls,
        message: str,
        data=None,
        meta=None
    ):

        return {
            "success": True,
            "message": message,
            "meta": meta,
            "data": data
        }


    @classmethod
    def error(
        cls,
        message: str,
        errors=None
    ):

        return {
            "success": False,
            "message": message,
            "errors": errors
        }