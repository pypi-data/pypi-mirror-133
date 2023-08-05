import datetime
import pytz


class GPSParser:
    def __init__(self, local_time_zone = 'Asia/Taipei') -> None:
        self.is_GPS_normal = False
        
        self.local_time_zone = local_time_zone
        self.local_datetime = None

        self.__MIN_LAT_LEN = 3
        self.__MIN_LON_LEN = 4
        # self.__NUM_SATELLITES                = 12
        self.__MAX_NUM_SATELLITES_IN_MESSGAE = 4
        self.__NUM_FIELDS_IN_SATELLITE       = 4
        # self.__DIRECTION_MAP = {'N': '北緯', 'S': '南緯', 'E': '東經', 'W': '西經'}
        self.__MODE1_MAP = {'M': 'Manual', 'A': 'Automatic'}
        self.__MODE2_MAP = {1: 'Fix not available', 2: '2D', 3: '3D'}

        self.latitude_degree = None
        self.latitude_minute = None
        self.longitude_degree = None
        self.longitude_minute = None
        self.latlon_radian_RMC = []
        self.latlon_radian_GGA = []
        self.gsa_obj = {}
        self.gsv_obj_map = {}

    def parse_NMEA(self, messages) -> bool:
        if messages == '':
            return False
        
        str_line_slice = messages.split('\n')
        if len(str_line_slice) == 0:
            return False

        flag_latlon_ready = False
        for one_line in str_line_slice:
            if len(one_line) == 0:
                continue

            if one_line[0] != '$':
                continue

            if (one_line.find('*') == -1):
                continue

            if (one_line.find('RMC') != -1):
                # print(one_line)
                local_datetime = self.parse_datetime(one_line)
                if local_datetime is not None:
                    self.local_datetime = local_datetime
                if self.parse_latlon(one_line, 3, 5) is False:
                    continue
                flag_latlon_ready = True
            
            if (one_line.find('GGA') != -1):
                if self.parse_latlon(one_line, 2, 4):
                    continue
                flag_latlon_ready = True
            
            if (one_line.find('GSA') != -1):
                self.parse_active_satellites(one_line)
            
            if (one_line.find('GSV') != -1):
                if self.parse_satellites_in_view(one_line) is False:
                    continue

        if flag_latlon_ready is True:
            self.is_GPS_normal = True
        
        return self.is_GPS_normal
    
    def parse_date(self, date_token) -> str:
        # UTC Date format ddmmyy
        year = int('20' + date_token[4:6])
        month = int(date_token[2:4])
        day = int(date_token[0:2])

        month_str = f'0{month}' if month < 10 else f'{month}'
        day_str = f'0{day}' if day < 10 else f'{day}'
        # print(f'{year}-{month_str}-{day_str}')

        return f'{year}-{month_str}-{day_str}'
    
    def parse_time(self, time_token) -> str:
        # UTC time format hhmmss.sss (000000.000 ~ 235959.999)
        hour = int(time_token[:2])
        minute = int(time_token[2:4])
        second = int(time_token[4:6])
        # msec = int(time_token[7:9])
        # nsec = 1000 * msec

        hour_str = f'0{hour}' if hour < 10 else f'{hour}'
        minute_str = f'0{minute}' if minute < 10 else f'{minute}'
        second_str = f'0{second}' if second < 10 else f'{second}'
        # print(f'{hour_str}:{minute_str}:{second_str}')

        return f'{hour_str}:{minute_str}:{second_str}'
    
    def parse_datetime(self, one_line):
        str_slice = one_line.split(',')

        time_token = str_slice[1]
        date_token = str_slice[9]

        if len(date_token) < 6:
            return None
        
        # time_string = self.parse_date(date_token) + ' ' + self.parse_time(time_token)
        # print(time_string)

        date_tokens = self.parse_date(date_token).split('-')
        time_tokens = self.parse_time(time_token).split(':')
        ori_datetime = datetime.datetime(
            int(date_tokens[0]), int(date_tokens[1]), int(date_tokens[2]),
            int(time_tokens[0]), int(time_tokens[1]), int(time_tokens[2]),
            tzinfo=datetime.timezone.utc
        )
        # print(ori_datetime)

        time_zone = pytz.timezone(self.local_time_zone)
        local_datetime = ori_datetime.astimezone(time_zone)

        return str(local_datetime)
    
    def parse_latlon(self, one_line, i_lat, i_lon) -> bool:
        str_slice = one_line.split(',')
        if len(str_slice[i_lat]) < self.__MIN_LAT_LEN or len(str_slice[i_lon]) < self.__MIN_LON_LEN:
            return False

        # i_lat_direction = i_lat + 1
        # i_lon_direction = i_lon + 1
        # lat_direction = str_slice[i_lat_direction]  # N/S
        # lon_direction = str_slice[i_lon_direction]  # E/W

        self.latitude_degree = float(str_slice[i_lat][:2])
        self.latitude_minute = float(str_slice[i_lat][2:])
        self.longitude_degree = float(str_slice[i_lon][:3])
        self.longitude_minute = float(str_slice[i_lon][3:])

        # latitude_str = self.__DIRECTION_MAP[lat_direction] + str(self.latitude_degree) + '度' + str(self.latitude_minute) + '分'
        # longitude_str = self.__DIRECTION_MAP[lon_direction] + str(self.longitude_degree) + '度' + str(self.longitude_minute) + '分'
        # print(latitude_str, longitude_str)

        latitude_radian = self.latitude_degree + self.latitude_minute / 60
        longitude_radian = self.longitude_degree + self.longitude_minute / 60

        if i_lat == 3 and i_lon == 5:
            self.latlon_radian_RMC = [latitude_radian, longitude_radian]
        elif i_lat == 2 and i_lon == 4:
            self.latlon_radian_GGA = [latitude_radian, longitude_radian]

            self.quality_indicator_GGA = int(str_slice[6])
            self.satellites_used_GGA = int(str_slice[7])
            self.hdop_GGA = float(str_slice[8])
            self.altitude_GGA = float(str_slice[9])
            self.geoidal_separation_GGA = float(str_slice[11])
            self.dgps_station_id_GGA = str_slice[14].split('*')[0]

        return True
    
    def parse_active_satellites(self, one_line) -> bool:
        str_slice = one_line.split(',')

        talker_ID = str_slice[0][1:3]

        self.gsa_obj['talker_ID'] = talker_ID
        self.gsa_obj['mode_1'] = self.__MODE1_MAP[str_slice[1]]
        self.gsa_obj['mode_2'] = self.__MODE2_MAP[int(str_slice[2])]

        # TODO: Check which satellite ID belongs to which GNSS
        satellite_IDs = str_slice[3:15]
        for index in range(len(satellite_IDs)):
            satellite_ID = satellite_IDs[index]
            if satellite_ID == '':
                continue

            if 'active_satellites' not in self.gsa_obj:
                self.gsa_obj['active_satellites'] = [satellite_ID]
                continue
            
            if satellite_ID in self.gsa_obj['active_satellites']:
                continue

            self.gsa_obj['active_satellites'].append(satellite_ID)

        self.gsa_obj['pdop'] = float(str_slice[15])
        self.gsa_obj['hdop'] = float(str_slice[16])
        self.gsa_obj['vdop'] = float(str_slice[17].split('*')[0])
        # print(self.gsa_obj)

        return 'active_satellites' in self.gsa_obj
    
    def create_satellite(self, str_slice, i_token):
        satellite_ID = str_slice[i_token * self.__NUM_FIELDS_IN_SATELLITE + 4]
        satellite_elevation = int(str_slice[i_token * self.__NUM_FIELDS_IN_SATELLITE + 5])
        satellite_azimuth = int(str_slice[i_token * self.__NUM_FIELDS_IN_SATELLITE + 6])
        satellite_SNR = str_slice[i_token * self.__NUM_FIELDS_IN_SATELLITE + 7].split('*')[0]
        satellite_SNR = None if satellite_SNR == '' else int(satellite_SNR)

        satellite = {'ID': satellite_ID, 'Elevation': satellite_elevation, 'Azimuth': satellite_azimuth, 'SNR': satellite_SNR}

        return satellite
    
    def parse_satellites_in_view(self, one_line) -> bool:
        str_slice = one_line.split(',')

        talker_ID = str_slice[0][1:3]
        num_sequences = int(str_slice[1])
        sequence_number = int(str_slice[2])
        satellites_in_view = int(str_slice[3])
        # print(f'{talker_ID}GSV {sequence_number}/{num_sequences}: {satellites_in_view} satellites')

        if talker_ID in self.gsv_obj_map:
            gsv_obj = self.gsv_obj_map[talker_ID]
            if sequence_number > 1:
                # Ignore the first receiving message if its sequence number is not 1
                if gsv_obj['index_satellite'] == 0:
                    return False

                # Ignore the message that is not in the same GSV group
                if num_sequences != gsv_obj['num_sequences'] and satellites_in_view != gsv_obj['satellites_in_view']:
                    return False

            # Ignore the message is not in order in the same GSV group
            if gsv_obj['index_sequence'] >= sequence_number:
                return False

            if sequence_number == 1:
                gsv_obj['talker_ID'] = talker_ID
                gsv_obj['num_sequences'] = num_sequences
                gsv_obj['index_sequence'] = 1
                gsv_obj['satellites_in_view'] = satellites_in_view
                gsv_obj['index_satellite'] = 0
                gsv_obj['satellites'] = []

            gsv_obj['index_sequence'] = sequence_number
            if sequence_number < num_sequences:
                gsv_obj['num_remaining_satellites'] = self.__MAX_NUM_SATELLITES_IN_MESSGAE
            else:
                gsv_obj['num_remaining_satellites'] = satellites_in_view % self.__MAX_NUM_SATELLITES_IN_MESSGAE

            for i_token in range(gsv_obj['num_remaining_satellites']):
                satellite = self.create_satellite(str_slice, i_token)
                gsv_obj['satellites'].append(satellite)
                gsv_obj['index_satellite'] += 1
        else:
            # Ignore the GSV message if it does not exist in the map and its sequence number is not 1
            if sequence_number != 1:
                return False

            gsv_obj = {
                'talker_ID': talker_ID,
                'num_sequences': num_sequences,
                'satellites_in_view': satellites_in_view,
                'index_satellite': 0,
                'satellites': []
            }

            gsv_obj['index_sequence'] = sequence_number
            if sequence_number < num_sequences:
                gsv_obj['num_remaining_satellites'] = self.__MAX_NUM_SATELLITES_IN_MESSGAE
            else:
                gsv_obj['num_remaining_satellites'] = satellites_in_view % self.__MAX_NUM_SATELLITES_IN_MESSGAE

            for i_token in range(gsv_obj['num_remaining_satellites']):
                satellite = self.create_satellite(str_slice, i_token)
                gsv_obj['satellites'].append(satellite)
                gsv_obj['index_satellite'] += 1

            self.gsv_obj_map[talker_ID] = gsv_obj

        return True
