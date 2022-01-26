import json
import time

from bson.json_util import dumps, loads

from aiortc import VideoStreamTrack
import numpy as np

from app.core.models.mediapipe import MediapipeHolistic
from app.core.models.sign import SignModel
from app.services.cache import CacheService


class VideoTransform(VideoStreamTrack):
    kind = "video"

    def __init__(self, track, db, cache: CacheService):
        super().__init__()  # don't forget this!
        self.track = track
        self.channel = None
        self.frames = []
        self.db = db
        self.cache = cache
        self.predictions = []

    async def recv(self):
        frame = await self.track.recv()
        img = frame.to_ndarray(format="bgr24")

        results = MediapipeHolistic().process_image(img)

        self.frames.append(results)

        if len(self.frames) == 30:
            pred = SignModel().predict(np.array([self.frames]))[0]
            pred_id = np.argmax(pred) + 1

            self.predictions.append(np.argmax(pred))

            if np.unique(self.predictions[-5:])[0] == np.argmax(pred):
                if pred[np.argmax(pred)] > 0.3:
                    async def f():
                        return await self.db["words"].find_one({"label": int(pred_id)})

                    word = loads(await self.cache.remember(f"word_{pred_id}", f, 60 * 60 * 24))

                    if word is not None:
                        if self.channel is not None:
                            self.channel.send(json.dumps(dumps(word)))
                            await self.channel._RTCDataChannel__transport._data_channel_flush()
                            await self.channel._RTCDataChannel__transport._transmit()



            self.frames.pop(0)

        return frame
