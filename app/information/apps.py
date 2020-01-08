from django.apps import AppConfig
from watson import search as watson


class InformationConfig(AppConfig):
    name = 'information'

    def ready(self):
        HFI = self.get_model("HFI")
        HFA = self.get_model("HFA")
        HFC = self.get_model("HFC")
        FNI = self.get_model("FNI")
        watson.register(HFI)
        watson.register(HFA)
        watson.register(HFC)
        watson.register(FNI)
