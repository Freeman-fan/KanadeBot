class ForwardMsg:
    def __init__(self):
        self.msg = []

    def AddTextMessage(self, text: str = None):
        if text:
            data = dict()
            data["name"] = "K"
            data["uin"] = "00001"
            data["content"] = [{"type": "text", "data": {"text": text}}]
            message = dict()
            message["type"] = "node"
            message["data"] = data
            self.msg.append(message)

    def AddSignalImageMessage(self, photo_url: str = None):
        if photo_url:
            data = dict()
            data["name"] = "K"
            data["uin"] = "00001"
            data["content"] = f"[CQ:image,file={photo_url}]"
            message = dict()
            message["type"] = "node"
            message["data"] = data
            self.msg.append(message)