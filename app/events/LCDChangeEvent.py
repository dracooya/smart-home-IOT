from events.Event import Event as Evnt


class LCDChangeEvent(Evnt):
    def __init__(self):
        super().__init__()
