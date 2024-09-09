from typing import Annotated, Literal, NewType

from pydantic import (
    BaseModel,
    ConfigDict,
    StrictFloat,
    StrictInt,
    StrictStr,
)

SpotId = NewType("SpotId", int)
StampId = NewType("StampId", int)
Longitude = NewType("Longitude", float)
Latitude = NewType("Latitude", float)

StampType = Literal["QRCode", "GPS"]


class StampRallySpot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    isPublicSpot: Literal[True] = True
    useCheckinSurvey: Literal[False] = False
    isExternalCheckin: Literal[False] = False
    isRewardRequiredSpot: Literal[False] = False
    isCheckinDisabled: Literal[False] = False
    hasSpotReward: Literal[False] = False
    useGps: Literal[False] = False
    maxCheckinCountForUser: Literal[0] = 0
    quizTryAnswerLimit: Literal[0] = 0
    keywordLength: Literal[0] = 0
    checkinPoints: StrictInt  # =3
    checkinKey: Literal[0] = 0
    sortOrder: Literal[0] = 0
    gpsAcceptableRange: Literal[0] = 0
    id: StrictInt  # =58023
    stampRallyId: Literal[852] = 852
    spotLng: Annotated[Longitude, StrictFloat]  # =139.982586996195
    spotLat: Annotated[Latitude, StrictFloat]  # =35.6965389476619
    spotId: Annotated[SpotId, StrictInt]  # =337568
    spotRewards: None = None
    survey: None = None
    quizSelectorTexts: list[StrictStr] = []
    spotGroupIds: list[StrictInt] = []
    stampType: StampType  # ='QRCode'
    spotRewardType: Literal["Application"] = "Application"
    pointCurrencyType: Literal["Unset"] = "Unset"
    spotShareType: Literal["Public"] = "Public"
    stampTypeText: StampType  # ='QRCode'
    pointCurrencyTypeText: Literal["Unset"] = "Unset"
    spotShareTypeText: Literal["Public"] = "Public"
    samplePhotoDescription: None = None
    samplePhotoUrl: None = None
    spotTitle: StrictStr  # ='街のピザ屋\u3000コンパーレ\u3000コマーレ'
    keywordImageUrl: None = None
    keywordDescription: None = None
    keywordTitle: None = None
    spotRewardSubType: Literal["Normal"] = "Normal"
    spotRewardDescription: None = None
    spotRewardTitle: None = None
    spotRewardBannerUrl: None = None
    stampRallyBaseIcon: None = None
    stampRallyIcon: StrictStr  # ='https://platinumaps.blob.core.windows.net/maps/857/spots/337568/stamprally/852.webp?v=638604079352646211'


class EventHubContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sas: str  # ="SharedAccessSignature sr=https%3a%2f%2fplatinumaps.servicebus.windows.net%2fevents%2fpublishers%2fc7878c34-bbf3-42b0-ab9a-13c5720e7ebf%2fmessages&sig=AbvgHJvLupMRszjLZUaamGrs38fVEZRL2YFH6pJY%2fA4%3d&se=1728439583&skn=BrowserSendPolicy"  # noqa: E501
    uri: str  # ="https://platinumaps-proxy.azurewebsites.net/eventhubs/events/publishers/c7878c34-bbf3-42b0-ab9a-13c5720e7ebf/messages"


class BootOptions(BaseModel):
    model_config = ConfigDict(extra="allow")

    stampRallySpots: list[StampRallySpot]

    # mapId: int
    eventHubContext: EventHubContext | None = (
        None  # NOTE: 実行のたびに変化するので省略可能
    )
    # area: ...
