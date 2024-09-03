from pydantic import BaseModel, ConfigDict, StrictBool, StrictInt


class StampRallySpot(BaseModel):
    model_config = ConfigDict(extra="allow")

    isPublicSpot: StrictBool  # =True
    useCheckinSurvey: StrictBool  # =False
    isExternalCheckin: StrictBool  # =False
    isRewardRequiredSpot: StrictBool  # =False
    isCheckinDisabled: StrictBool  # =False
    hasSpotReward: StrictBool  # =False
    useGps: StrictBool  # =False
    # maxCheckinCountForUser=0
    # quizTryAnswerLimit=0
    # keywordLength=0
    # checkinPoints=3
    # checkinKey=0
    # sortOrder=0
    # gpsAcceptableRange=0
    id: StrictInt  # =58023
    stampRallyId: StrictInt  # =852
    # spotLng=139.982586996195
    # spotLat=35.6965389476619
    spotId: StrictInt  # =337568
    spotRewards: None  # =None
    survey: None  # =None
    # quizSelectorTexts=[]
    spotGroupIds: list[StrictInt]  # =[]
    # stampType='QRCode'
    # spotRewardType='Application'
    # pointCurrencyType='Unset'
    # spotShareType='Public'
    # stampTypeText='QRCode'
    # pointCurrencyTypeText='Unset'
    # spotShareTypeText='Public'
    samplePhotoDescription: None  # =None
    samplePhotoUrl: None  # =None
    # spotTitle='街のピザ屋\u3000コンパーレ\u3000コマーレ'
    keywordImageUrl: None  # =None
    keywordDescription: None  # =None
    keywordTitle: None  # =None
    # spotRewardSubType='Normal'
    spotRewardDescription: None  # =None
    spotRewardTitle: None  # =None
    spotRewardBannerUrl: None  # =None
    stampRallyBaseIcon: None  # =None
    # stampRallyIcon='https://platinumaps.blob.core.windows.net/maps/857/spots/337568/stamprally/852.webp?v=638604079352646211'


class BootOptions(BaseModel):
    model_config = ConfigDict(extra="allow")

    stampRallySpots: list[StampRallySpot]
