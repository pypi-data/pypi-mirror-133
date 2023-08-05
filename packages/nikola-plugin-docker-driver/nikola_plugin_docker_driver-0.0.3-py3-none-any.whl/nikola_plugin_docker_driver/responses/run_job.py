class RunJobResponse:
    def __init__(self, raw: dict[str, str]) -> None:
        self._job = raw['job']
        self._correlation_id = raw['correlationId']

    @property
    def id(self) -> str:
        return self._correlation_id

    @property
    def name(self) -> str:
        return self._job.name

    @property
    def status(self) -> str:
        return self._job.status

    @property
    def image(self) -> str:
        return self._job.image

    @property
    def job(self) -> str:
        """
            This will be useful when doing things like logs() or get_archive()/export() to get files
            or stats() to get info about the running jobs or pause(), etc, etc, etc...
        """
        return self._job
