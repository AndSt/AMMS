from src.config import Config
from src.version_manager import VersionManager
from src.loader import Loader


class ModelManager:
    def __init__(self):
        self.config = Config()
        self.loader = Loader()
        self.version_manager = VersionManager()
        self.loaded_models = []
        print("Reload models")
        self.update()

    def loaded_versions(self):
        result = []
        for loaded_model in self.loaded_models:
            result.append(loaded_model.as_dict())
        return {'available_models': result}

    def version_details(self):
        if len(self.loaded_models) > 0:
            return self.loaded_models[0].as_dict()
        return RuntimeError("No model is loaded in cache yet.")

    def model_predict(self, text: str):
        pred = self.model.predict([text])[0]
        pred_proba = self.model.predict_proba([text])[0]
        return {
            "version": self.loaded_version,
            "class": int(pred),
            "class_proba": pred_proba.tolist()
        }

    def new_model_predict(self, text: str):
        return 1

    def update(self):
        self.version_manager.reload_available_versions()
        reload_models, new_models = self.version_manager.specify_update_policy(self.loaded_models)
        #
        # new_loaded_models = []
        #
        # for load_model in load_models:
        #     new_loaded_models.append(LoadedModel.from_dict(load_model))
        # self.loaded_models = new_loaded_models

    #     newest_version = {"version": "1.0.1", "date": "25.03.2020"}
    #     if newest_version == self.loaded_version:
    #         return
    #
    #     date_string = "".join(newest_version["date"].split("."))
    #     version_string = "-".join(newest_version["version"].split("."))
    #     file_name = "{}_version_{}_{}.p.pbz2".format(self.model_name, version_string, date_string)
    #     try:
    #         with open("{}/{}".format(self.model_dir, file_name), "rb") as handle:
    #             self.new_model = joblib.load(handle)
    #             print(type(self.new_model))
    #             # Test the model
    #             self.model = self.new_model
    #             self.new_model = None
    #             self.model_loaded = True
    #             self.loaded_version = newest_version
    #
    #     except Exception as e:
    #         print("error", str(e))
