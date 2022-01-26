import bson
from bson.json_util import dumps
import cv2
import pandas
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request, Depends
import uuid
import numpy as np
import logging
import os

from app.config.container import Container
from app.config.database import db
from app.core.VideoTransform import VideoTransform

from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole

from pydantic import BaseModel

from app.services.cache import CacheService

router = APIRouter()

ROOT = os.path.dirname(__file__)

logger = logging.getLogger("pc")
pcs = set()


class Offer(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    sdp: str
    type: str
    video_transform: str = None

@router.post("/offer")
@inject
async def offer(params: Offer, request: Request, cache: CacheService = Depends(Provide[Container.cache_service])):
    offer = RTCSessionDescription(sdp=params.sdp, type=params.type)

    pc = RTCPeerConnection()
    pcs.add(pc)
    pc_id = "PeerConnection(%s)" % uuid.uuid4()

    pcs.add(pc)

    def log_info(msg, *args):
        logger.info(pc_id + " " + msg, *args)

    log_info("Created for %s", request.client.host)

    recorder = MediaBlackhole()

    @pc.on("datachannel")
    def on_datachannel(channel):
        global new_video_track
        new_video_track.channel = channel
        new_video_track.frames = []

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        log_info("ICE connection state is %s", pc.iceConnectionState)
        if pc.iceConnectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        log_info("Track %s received", track.kind)

        if track.kind == "video":
            global new_video_track
            new_video_track = VideoTransform(track, db, cache)

            pc.addTrack(new_video_track)

        @track.on("ended")
        async def on_ended():
            log_info("Track %s ended", track.kind)
            await recorder.stop()

    # handle offer
    await pc.setRemoteDescription(offer)
    await recorder.start()

    # send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}

container = Container()
container.wire(modules=[__name__])