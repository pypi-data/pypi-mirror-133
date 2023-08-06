class TwilioActivity:
    """
    Twilio Activity representation as an object.
    It contains all the values that are relevant for an Activity on Twilio platform.
    """

    def __init__(self, friendly_name: str, availability: bool, default: bool = False):
        self.__friendly_name = friendly_name
        self.__availability = availability
        self.__default = default

    @property
    def friendly_name(self) -> str:
        return self.__friendly_name

    @property
    def availability(self) -> bool:
        return self.__availability

    @property
    def default(self) -> bool:
        return self.__default
