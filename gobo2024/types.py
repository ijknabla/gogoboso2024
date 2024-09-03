from pydantic import BaseModel, ConfigDict, StrictInt


class StampRallySpot(BaseModel):
    model_config = ConfigDict(extra="allow")

    isPublicSpot: bool  # =True
    useCheckinSurvey: bool  # =False
    isExternalCheckin: bool  # =False
    isRewardRequiredSpot: bool  # =False
    isCheckinDisabled: bool  # =False
    hasSpotReward: bool  # =False
    useGps: bool  # =False
    # maxCheckinCountForUser=0
    # quizTryAnswerLimit=0
    # keywordLength=0
    # checkinPoints=3
    # checkinKey=0
    # sortOrder=0
    # gpsAcceptableRange=0
    id: StrictInt  # =58023
    # stampRallyId=852
    # spotLng=139.982586996195
    # spotLat=35.6965389476619
    # spotId=337568
    # spotRewards=None
    # survey=None
    # quizSelectorTexts=[]
    # spotGroupIds=[]
    # stampType='QRCode'
    # spotRewardType='Application'
    # pointCurrencyType='Unset'
    # spotShareType='Public'
    # stampTypeText='QRCode'
    # pointCurrencyTypeText='Unset'
    # spotShareTypeText='Public'
    # samplePhotoDescription=None
    # samplePhotoUrl=None
    # spotTitle='街のピザ屋\u3000コンパーレ\u3000コマーレ'
    # keywordImageUrl=None
    # keywordDescription=None
    # keywordTitle=None
    # spotRewardSubType='Normal'
    # spotRewardDescription=None
    # spotRewardTitle=None
    # spotRewardBannerUrl=None
    # stampRallyBaseIcon=None
    # stampRallyIcon='https://platinumaps.blob.core.windows.net/maps/857/spots/337568/stamprally/852.webp?v=638604079352646211'


class BootOptions(BaseModel):
    model_config = ConfigDict(extra="allow")

    stampRallySpots: list[StampRallySpot]
