import time
from channels.middleware import BaseMiddleware


class WebSocketThrottlingMiddleware(BaseMiddleware):
    def __init__(self, inner, rate_limit=1):
        self.rate_limit = rate_limit
        self.message_timestamps = {}
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        user_id = scope.get("user").id

        if user_id:
            current_time = time.time()
            last_message_time = self.message_timestamps.get(user_id, 0)

            if current_time - last_message_time < 1 / self.rate_limit:
                await send(
                    {
                        "type": "websocket.close",
                        "code": 4000,
                        "text": "WebSocket message throttled. Try again later.",
                    }
                )
                return

            self.message_timestamps[user_id] = current_time

        return await super().__call__(scope, receive, send)
