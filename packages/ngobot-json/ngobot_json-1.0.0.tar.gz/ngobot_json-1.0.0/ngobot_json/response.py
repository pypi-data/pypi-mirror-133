import json


class Response:

    data = "Successful"
    category = "success"

    def __init__(self, data=data, category=category):
        self.data = data
        self.category = category

    def set_data(self, status, message):
        try:
            success = {
                "status": 200,
                "message": "ok",
                "reason": self.data
            }
            error = {
                "status": 422,
                "message": "Unprocessable Entity",
                "reason": self.data
            }
            if self.category == "error":
                data = {
                    "status": status,
                    "message": message,
                    "data": error
                }
                return json.dumps(data)
            elif self.category == "success":
                data = {
                    "status": status,
                    "message": message,
                    "data": success
                }
                return json.dumps(data)
            else:
                data = {
                    "status": status,
                    "message": message,
                    "data": self.data
                }
                return json.dumps(data)
        except Exception as e:
            data = {
                "status": 500,
                "message": e,
                "data": self.data
            }
        return json.dumps(data)

    # Information responses

    def Continue(self):
        try:
            data = self.set_data(100, "Continue")
            return data
        except Exception as e:
            data = self.set_data(500, e)
            return data

    # Successful responses

    def Success(self):
        try:
            data = self.set_data(200, "Successful")
            return data
        except Exception as e:
            data = self.set_data(500, e)
            return data

    def Created(self):
        try:
            data = self.set_data(201, "Created Successfully")
            return data
        except Exception as e:
            data = self.set_data(500, e)
            return data

    def Accepted(self):
        try:
            data = self.set_data(202, "Processing")
            return data
        except Exception as e:
            data = self.set_data(500, e)
            return data

    # Redirection messages

    def Found(self):
        try:
            data = self.set_data(302, "Found")
            return data
        except Exception as e:
            data = self.set_data(500, e)
            return data

    # Client error responses

    def BadRequest(self):
        try:
            data = self.set_data(400, "Bad Request")
            return data
        except Exception as e:
            data = self.set_data(500, e)
            return data

    def Unauthorized(self):
        try:
            data = self.set_data(401, "Unauthorized")
            return data
        except Exception as e:
            data = self.set_data(500, e)
            return data

    def PaymentRequired(self):
        try:
            data = self.set_data(402, "Payment Required")
            return data
        except Exception as e:
            data = self.set_data(500, e)
            return data

    def Forbidden(self):
        try:
            data = self.set_data(403, "Forbidden")
            return data
        except Exception as e:
            data = self.set_data(500, e)
            return data

    def NotFound(self):
        try:
            data = self.set_data(404, "Not Found")
            return data
        except Exception as e:
            data = self.set_data(500, e)
            return data

    # Server error responses

    def InternalServerError(self):
        try:
            data = self.set_data(500, "Internal Server Error")
            return data
        except Exception as e:
            data = self.set_data(500, e)
            return data
