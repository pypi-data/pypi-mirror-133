class Api:
    def init_app(self, app):
        self.config = app.config


class GhettoApi:
    def init_listen(self, listen_dict):
        self.listen_dict = listen_dict

    def init_radios_in_view(self, radios_in_view_dict):
        self.radios_in_view_dict = radios_in_view_dict

    def init_ghetto_measurements(self, ghetto_measure_dict):
        self.ghetto_measure_dict = ghetto_measure_dict


api = Api()
ghettoApi = GhettoApi()
