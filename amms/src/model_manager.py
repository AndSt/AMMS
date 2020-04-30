from src.config import Config
from src.version_manager import VersionManager
from src.loader import Loader
from src.servables.servable_base import Servable, ServableStatus


class ModelManager:
    def __init__(self):
        self.config = Config()
        self.loader = Loader()
        self.version_manager = VersionManager()
        self.servables = []
        print("Reload models")
        self.update()

    def available_versions(self):
        result = []
        for loaded_model in self.servables:
            result.append(loaded_model.as_dict())
        return {'available_models': result}

    def model_meta_data(self):
        if len(self.servables) > 0:
            return self.servables[0].as_dict()
        return RuntimeError("No model is loaded in cache yet.")

    def predict(self, model_name: str, version: str, input=None):
        if (model_name, version) in self.servables:
            return self.servables[(model_name, version)].predict(input)
        else:
            raise Exception  # TODO model doesn't exist error

    def model_predict(self, text: str):
        pred = self.model.predict([text])[0]
        pred_proba = self.model.predict_proba([text])[0]
        return {
            "version": self.loaded_version,
            "class": int(pred),
            "class_proba": pred_proba.tolist()
        }

    def update(self):
        self.version_manager.update()
        update_policies = self.version_manager.retrieve_update_policies()

        for update_policy in update_policies:
            print(update_policy)  # TODO reload model
            if update_policy.type == 'shared':
                self.loader.load_from_shared(update_policy.url, self.config.model_dir, update_policy.file_name)
            else:
                print('Error')  # TODO error handling

            servable = Servable(update_policy.model_name, update_policy.version, update_policy.timestamp,
                                update_policy.model_dir)
            if servable.status == ServableStatus.IDLE:
                self.servables[(update_policy.model_name, update_policy.version)] = servable
