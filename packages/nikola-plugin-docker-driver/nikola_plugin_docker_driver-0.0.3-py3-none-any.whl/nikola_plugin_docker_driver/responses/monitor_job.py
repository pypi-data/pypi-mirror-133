class MonitorJobResponse:
    def __init__(self, raw: dict[str, str]) -> None:
        self._monitor = raw['monitor']

    @property
    def id(self) -> str:
        return self._monitor.id

    @property
    def name(self) -> str:
        return self._monitor.name

    @property
    def status(self) -> str:
        return self._monitor.status

    @property
    def image(self) -> str:
        return self._monitor.image

    @property
    def monitor(self) -> str:
        return self._monitor
