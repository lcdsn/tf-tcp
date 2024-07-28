class Note:
    def __init__(self, instrument=0, pitch=0, volume=0, bpm=0):
        self.instrument = instrument
        self.pitch = pitch
        self.volume = volume
        self.bpm = bpm

    def __str__(self):
        return (
            f"instrument: {self.instrument}, pitch: {self.pitch}, "
            f"volume: {self.volume}, bpm: {self.bpm}"
        )


class Rest:
    def __init__(self, bpm=60):
        self.bpm = bpm

    def __str__(self):
        return f"rest for {60 / self.bpm} seconds"
