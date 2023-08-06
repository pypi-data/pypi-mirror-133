from eisenradio.api import ghettoApi


def measure_meta():

    request_time = ''
    request_suffix = ''
    play_station = ''
    request_icy_genre = ''
    request_icy_name = ''
    station_id = ''
    request_icy_view_id = ''
    request_icy_br = ''

    try:
        # listen key pressed
        for radio_id, btn_down in ghettoApi.listen_dict.items():
            if btn_down:
                station_id = radio_id
                play_station = ghettoApi.radios_in_view_dict[radio_id]
                request_time = ghettoApi.ghetto_measure_dict[play_station + ',request_time']

                content_type = ghettoApi.ghetto_measure_dict[play_station + ',suffix']
                if content_type == 'audio/aacp' or content_type == 'application/aacp':
                    request_suffix = 'aacp'
                if content_type == 'audio/aac':
                    request_suffix = 'aac'
                if content_type == 'audio/ogg' or content_type == 'application/ogg':
                    request_suffix = 'ogg'
                if content_type == 'audio/mpeg':
                    request_suffix = 'mp3'
                if content_type == 'audio/x-mpegurl' or content_type == 'text/html':
                    request_suffix = 'm3u'
    except KeyError:
        pass
    try:
        request_icy_genre = ghettoApi.ghetto_measure_dict[play_station + ',icy_genre']
        request_icy_name = ghettoApi.ghetto_measure_dict[play_station + ',icy_name']
        request_icy_view_id = str(station_id)
        request_icy_br = ghettoApi.ghetto_measure_dict[play_station + ',icy_br']
    except KeyError:
        pass
    if not request_time:
        request_time = '---'
        request_suffix = '---'

    return request_time, request_suffix, request_icy_genre, request_icy_name, request_icy_view_id, request_icy_br
