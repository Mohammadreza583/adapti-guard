from src.adapti_guard.runtime import AdaptiGuard


class AdaptiGuardPipeline:

    def __init__(self):

        self.guard = AdaptiGuard()

    def run(self, text: str):

        return self.guard.run(text)
