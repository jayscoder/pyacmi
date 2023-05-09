import zipfile
import datetime
import sortedcontainers
import bisect
import json
import io
from constantly import ValueConstant

_ACMI_FILE_ENCODING = 'utf-8-sig'
_FLOAT_OBJECT_KEYS = {
    "Importance", "Length", "Width", "Height",
    "IAS", "CAS", "TAS", "Mach", "AOA", "HDG",
    "HDM", "Throttle", "RadarAzimuth", "RadarElevation",
    "RadarRange", "LockedTargetAzimuth",
    "LockedTargetElevation", "LockedTargetRange", "Flaps", "LandingGear",
    "AirBrakes",
    "PilotHeadRoll", "PilotHeadPitch", "PilotHeadYaw",
    "RollControlPosition", "PitchControlPosition", "YawControlPosition" }
_INT_OBJECT_KEYS = { "Slot", "Afterburner", "Tailhook",
                     "Parachute", "DragChute", "RadarMode",
                     "LockedTargetMode" }
_STR_OBJECT_KEYS = { "Pilot", "Group", "Country", "Coalition",
                     "Color", "Registration", "Squawk", "Debug", "Label" }


class AcmiType(ValueConstant):
    Plane = 'Plane'
    Helicopter = 'Helicopter'
    AntiAircraft = 'AntiAircraft'
    Armor = 'Armor'
    Tank = 'Tank'
    GroundVehicle = 'GroundVehicle'
    Watercraft = 'Watercraft'
    Warship = 'Warship'
    AircraftCarrier = 'AircraftCarrier'
    Submarine = 'Submarine'
    Sonobuoy = 'Sonobuoy'
    Human = 'Human'
    Infantry = 'Infantry'
    Parachutist = 'Parachutist'
    Missile = 'Missile'
    Rocket = 'Rocket'
    Bomb = 'Bomb'
    Projectile = 'Projectile'
    Beam = 'Beam'
    Shell = 'Shell'
    Bullet = 'Bullet'
    BallisticShell = 'BallisticShell'
    Grenade = 'Grenade'
    Decoy = 'Decoy'
    Flare = 'Flare'
    Chaff = 'Chaff'
    SmokeGrenade = 'SmokeGrenade'
    Building = 'Building'
    Aerodrome = 'Aerodrome'
    Bullseye = 'Bullseye'
    Waypoint = 'Waypoint'
    Container = 'Container'
    Shrapnel = 'Shrapnel'
    MinorObject = 'MinorObject'
    Explosion = 'Explosion'
    F16C = 'F16C'
    Bicycle = 'Bicycle'
    AIM120C = 'AIM-120C'


ACMI_TYPE_TAGS = {
    AcmiType.Plane          : ['Air+FixedWing'],
    AcmiType.Helicopter     : ['Air+Rotorcraft'],
    AcmiType.AntiAircraft   : ['Ground+AntiAircraft'],
    AcmiType.Armor          : ['Ground+Heavy+Armor+Vehicle'],
    AcmiType.Tank           : ['Ground+Heavy+Armor+Vehicle+Tank'],
    AcmiType.GroundVehicle  : ['Ground+Vehicle'],
    AcmiType.Watercraft     : ['Sea+Watercraft'],
    AcmiType.Warship        : ['Sea+Watercraft+Warship'],
    AcmiType.AircraftCarrier: ['Sea+Watercraft+AircraftCarrier', 'Heavy+Sea+Watercraft+AircraftCarrier'],
    AcmiType.Submarine      : ['Sea+Watercraft+Submarine'],
    AcmiType.Sonobuoy       : ['Sea+Sensor'],
    AcmiType.Human          : ['Ground+Light+Human'],
    AcmiType.Infantry       : ['Ground+Light+Human+Infantry'],
    AcmiType.Parachutist    : ['Ground+Light+Human+Air+Parachutist'],
    AcmiType.Missile        : ['Weapon+Missile'],
    AcmiType.Rocket         : ['Weapon+Rocket'],
    AcmiType.Bomb           : ['Weapon+Bomb'],
    AcmiType.Projectile     : ['Weapon+Projectile'],
    AcmiType.Beam           : ['Weapon+Beam'],
    AcmiType.Shell          : ['Projectile+Shell'],
    AcmiType.Bullet         : ['Projectile+Bullet'],
    AcmiType.BallisticShell : ['Projectile+Shell+Heavy'],
    AcmiType.Grenade        : ['Projectile+Grenade'],
    AcmiType.Decoy          : ['Misc+Decoy'],
    AcmiType.Flare          : ['Misc+Decoy+Flare'],
    AcmiType.Chaff          : ['Misc+Decoy+Chaff'],
    AcmiType.SmokeGrenade   : ['Misc+Decoy+SmokeGrenade'],
    AcmiType.Building       : ['Ground+Static+Building'],
    AcmiType.Aerodrome      : ['Ground+Static+Aerodrome'],
    AcmiType.Bullseye       : ['Navaid+Static+Bullseye'],
    AcmiType.Waypoint       : ['Navaid+Static+Waypoint'],
    AcmiType.Container      : ['Misc+Container'],
    AcmiType.Shrapnel       : ['Misc+Shrapnel'],
    AcmiType.MinorObject    : ['Misc+Minor'],
    AcmiType.Explosion      : ['Misc+Explosion'],
    AcmiType.F16C           : ['Medium+Air+FixedWing'],
    AcmiType.Bicycle        : ['Light+Ground+Vehicle'],
    AcmiType.AIM120C        : ['Medium+Weapon+Missile'],
}

# 将_ACMI_TYPE_TAGS预处理（内部按照顺序排序，方便后续匹配）
for k in ACMI_TYPE_TAGS:
    tags = ACMI_TYPE_TAGS[k]
    ACMI_TYPE_TAGS[k] = ['+'.join(sorted(tag.split('+'))) for tag in tags]


class AcmiObject:

    def __init__(self, obj_id: str):
        self.id = obj_id
        self.removed_at = None

        self.data = { }

        self.tags = ''
        self.type = ''  # 多个类型用+连接

        # 对象的名称。用于标识该对象。例如，F-16飞机的名称为“Viper”。
        self.name = None
        # Country：对象所属的国家。用于标识对象所属的国家。例如，F-16飞机所属的国家为“美国”。
        self.country = None

    # 飞机
    @property
    def is_plane(self):
        return AcmiType.Plane in self.type

    # 导弹，是一种可以自行控制运动轨迹、并击中目标的武器。
    @property
    def is_missile(self):
        return AcmiType.Missile in self.type

    # 箭状烟雾弹，是一种烟雾弹的类型，可以用于干扰敌方导弹、火箭炮或飞机系统。
    @property
    def is_flare(self):
        return AcmiType.Flare in self.type

    # 箔条干扰弹，是一种用于干扰雷达信号的武器，通常由一些金属箔条组成。
    @property
    def is_chaff(self):
        return AcmiType.Chaff in self.type

    # 弹片，是爆炸物体爆炸时产生的金属碎片和碎片。
    @property
    def is_shrapnel(self):
        return AcmiType.Shrapnel in self.type

    # 牛眼: 空战中心点的位置，用来方便飞行员报告目标位置和距离
    @property
    def is_bullseye(self):
        return AcmiType.Bullseye in self.type

    def set_value(self, field, timeframe, val):
        if field == 'Type':
            match_tags = '+'.join(sorted(val.split('+')))
            match_types = []
            self.tags = val
            if not self.type:
                for _type in ACMI_TYPE_TAGS:
                    if match_tags in ACMI_TYPE_TAGS[_type]:
                        match_types.append(_type)
                self.type = '+'.join(match_types)
            return
        elif field == 'Name':
            self.name = val
            return
        elif field == 'Country':
            self.country = val
            return

        if field not in self.data:
            self.data[field] = sortedcontainers.SortedDict()
        self.data[field][timeframe] = val

    # 该类的get_value函数用于获取指定场景下（field）的数据值。
    # 如果指定了timeframe参数，
    #   如果timeframe存在，则返回对应时间点的值或
    #   否则，返回timeframe上一条时间点的值（不存在则返回第一条数据）
    # 否则，返回场景最近一条数据的值。
    def get_value(self, field: str, timeframe=None):
        if field not in self.data:
            return None
        data = self.data[field]
        timeframe_keys = data.keys()
        if len(timeframe_keys) == 0:
            return None

        if timeframe is not None:
            if timeframe in timeframe_keys:
                return data[timeframe]
            pos = bisect.bisect_left(timeframe_keys, timeframe)
            if pos == 0:
                return data[timeframe_keys[0]]
            else:
                return data[timeframe_keys[pos - 1]]
        return data[timeframe_keys[-1]]

    # Latitude：对象的纬度。用于标识对象所在的位置。例如，F-16飞机的纬度为“32.1234”。
    def latitude(self, time=None):
        return self.get_value("Latitude", time)

    # Longitude：对象的经度。用于标识对象所在的位置。例如，F-16飞机的经度为“-117.2345”。
    def longitude(self, time=None):
        return self.get_value("Longitude", time)

    # Altitude：对象的高度。用于标识对象所在的高度。例如，F-16飞机的高度为“10000”。
    def altitude(self, time=None):
        return self.get_value("Altitude", time)

    # Heading：对象的航向。用于标识对象的方向。例如，F-16飞机的航向为“280”。
    def heading(self, time=None):
        return self.get_value("Heading", time)

    # Pitch：对象的俯仰角。用于标识对象的俯仰角度。例如，F-16飞机的俯仰角为“10”。
    def pitch(self, time=None):
        return self.get_value("Pitch", time)

    # Roll：对象的横滚角。用于标识对象的横滚角度。例如，F-16飞机的横滚角为“20”。
    def roll(self, time=None):
        return self.get_value("Roll", time)

    # IAS：对象的空速。用于标识对象的速度。例如，F-16飞机的空速为“300”。
    def ias(self, time=None):
        return self.get_value("IAS", time)

    # Flaps：对象的襟翼状态。用于标识对象襟翼的状态。例如，F-16飞机的襟翼状态为“放下”。
    def flaps(self, time=None):
        return self.get_value("Flaps", time)

    # LandingGear：对象的起落架状态。用于标识对象起落架的状态。例如，F-16飞机的起落架状态为“收起”。
    def landing_gear(self, time=None):
        return self.get_value("LandingGear", time)

    # AirBrakes：对象的空气刹车状态。用于标识对象空气刹车的状态。例如，F-16飞机的空气刹车状态为“关闭”。
    def air_brakes(self, time=None):
        return self.get_value("AirBrakes", time)

    # PitchControlPosition：对象的俯仰控制杆位置。用于标识对象的俯仰控制杆位置。例如，F-16飞机的俯仰控制杆位置为“中间”。
    def pitch_control_position(self, time=None):
        return self.get_value("PitchControlPosition", time)

    # RollControlPosition：对象的横滚控制杆位置。用于标识对象的横滚控制杆位置。例如，F-16飞机的横滚控制杆位置为“左”。
    def roll_control_position(self, time=None):
        return self.get_value("RollControlPosition", time)

    # YawControlPosition：对象的偏航控制杆位置。用于标识对象的偏航控制杆位置。例如，F-16飞机的偏航控制杆位置为“右”。
    def yaw_control_position(self, time=None):
        return self.get_value("YawControlPosition", time)

    # Yaw：对象的偏航角。用于标识对象的偏航角度。例如，F-16飞机的偏航角为“30”。
    def yaw(self, time=None):
        return self.get_value("Yaw", time)

    # Pilot：对象的驾驶员。用于标识对象的驾驶员。例如，F-16飞机的驾驶员为“Tom”。
    def pilot(self, time=None):
        return self.get_value("Pilot", time)

    # PilotHeadPitch：驾驶员的头部俯仰角。用于标识驾驶员的头部俯仰角度。例如，驾驶员的头部俯仰角为“-10”。
    def pilot_head_pitch(self, time=None):
        return self.get_value("PilotHeadPitch", time)

    # PilotHeadRoll：驾驶员的头部横滚角。用于标识驾驶员的头部横滚角度。例如，驾驶员的头部横滚角为“0”。
    def pilot_head_roll(self, time=None):
        return self.get_value("PilotHeadRoll", time)

    # PilotHeadYaw：驾驶员的头部偏航角。用于标识驾驶员的头部偏航角度。例如，驾驶员的头部偏航角为“20”。
    def pilot_head_yaw(self, time=None):
        return self.get_value("PilotHeadYaw", time)

    def json(self):
        return {
            'ID'                  : self.id,
            'Name'                : self.name,
            'Tags'                : self.tags,
            'Type'                : self.type,
            'Country'             : self.country,
            'Latitude'            : self.latitude(),
            'Longitude'           : self.longitude(),
            'Altitude'            : self.altitude(),
            'Heading'             : self.heading(),
            'Pitch'               : self.pitch(),
            'Roll'                : self.roll(),
            'IAS'                 : self.ias(),
            'Flaps'               : self.flaps(),
            'LandingGear'         : self.landing_gear(),
            'AirBrakes'           : self.air_brakes(),
            'PitchControlPosition': self.pitch_control_position(),
            'RollControlPosition' : self.roll_control_position(),
            'YawControlPosition'  : self.yaw_control_position(),
            'Yaw'                 : self.yaw(),
            'Pilot'               : self.pilot(),
            'PilotHeadPitch'      : self.pilot_head_pitch(),
            'PilotHeadRoll'       : self.pilot_head_roll(),
            'PilotHeadYaw'        : self.pilot_head_yaw()
        }

    def __str__(self):
        return json.dumps(self.json(), ensure_ascii=False, indent=2)

    # class Frame:


#     def __init__(self, time):
#         self.time = time
#         self.objects = { }

class AcmiFileReader:
    """Stream reading class that correctly line escaped acmi files."""

    def __init__(self, fh):
        self.fh = fh

    def __iter__(self):
        return self

    def __next__(self):
        line = self.fh.readline()
        # line = rl.decode(AcmiFileReader._codec)
        if len(line) == 0:
            raise StopIteration

        while line.strip().endswith('\\'):
            line = line.strip()[:-1] + '\n' + self.fh.readline().decode(_ACMI_FILE_ENCODING)

        return line


class Acmi:

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.file_version = None
        self.file_type = None

        # global properties
        self.data_source = None
        self.data_recorder = None
        self.reference_time = None
        self.recording_time = None
        self.author = None
        self.title = None
        self.category = None
        self.briefing = None
        self.debriefing = None
        self.comments = None
        self.reference_longitude = 0
        self.reference_latitude = 0

        self.objects: dict[str, AcmiObject] = { }
        self.timeframes = []
        # 加载

        self._parse(filepath=filepath)

    @staticmethod
    def parse_obj_id(val: str) -> str:
        # return int(val, 16)
        return val

    @staticmethod
    def strptime(val: str):
        if len(val) < 22:
            return datetime.datetime.strptime(val, "%Y-%m-%dT%H:%M:%SZ")
        else:
            return datetime.datetime.strptime(val, "%Y-%m-%dT%H:%M:%S.%fZ")

    @staticmethod
    def split_fields(line):
        fields = []
        i = 1
        lastfield = 0
        while i < len(line):
            if line[i - 1] != '\\' and line[i] == ',':
                fields.append(line[lastfield:i])
                lastfield = i + 1
            i += 1

        fields.append(line[lastfield:i])
        return fields

    # 解析Global Property
    def _parse_global_property(self, fields: list):
        for field in fields[1:]:  # skip objid (0)
            (prop, val) = field.split('=', 1)
            if prop == "ReferenceTime":
                self.reference_time = self.strptime(val)
            elif prop == "RecordingTime":
                self.recording_time = self.strptime(val)
            elif prop == "ReferenceLongitude":
                self.reference_longitude = float(val)
            elif prop == "ReferenceLatitude":
                self.reference_latitude = float(val)
            elif prop == "DataSource":
                self.data_source = val
            elif prop == "DataRecorder":
                self.data_recorder = val
            elif prop == "Author":
                self.author = val
            elif prop == "Title":
                self.title = val
            elif prop == "Category":
                self.category = val
            elif prop == "Briefing":
                self.briefing = val
            elif prop == "Debriefing":
                self.debriefing = val
            elif prop == "Comments":
                self.comments = val
            else:
                raise RuntimeError("Unknown global property: " + prop)

    # 解析Object Property
    def _parse_object_property(self, obj_id: str, timeframe: float, fields):
        if obj_id not in self.objects:
            self.objects[obj_id] = AcmiObject(obj_id)

        obj = self.objects[obj_id]
        for field in fields[1:]:
            (prop, val) = field.split('=', 1)

            if prop == "T":
                pos_list = val.split('|')
                if pos_list:
                    if pos_list[0]:
                        obj.set_value("Longitude", timeframe, self.reference_longitude + float(pos_list[0]))
                    if pos_list[1]:
                        obj.set_value("Latitude", timeframe, self.reference_latitude + float(pos_list[1]))
                    if pos_list[2]:
                        obj.set_value("Altitude", timeframe, float(pos_list[2]))

                    if len(pos_list) == 5:
                        if pos_list[3]:
                            obj.set_value("x", timeframe, float(pos_list[3]))
                        if pos_list[4]:
                            obj.set_value("y", timeframe, float(pos_list[4]))
                    if len(pos_list) == 6:
                        if pos_list[3]:
                            obj.set_value("Roll", timeframe, float(pos_list[3]))
                        if pos_list[4]:
                            obj.set_value("Pitch", timeframe, float(pos_list[4]))
                        if pos_list[5]:
                            obj.set_value("Yaw", timeframe, float(pos_list[5]))
                    if len(pos_list) == 9:
                        if pos_list[3]:
                            obj.set_value("Roll", timeframe, float(pos_list[3]))
                        if pos_list[4]:
                            obj.set_value("Pitch", timeframe, float(pos_list[4]))
                        if pos_list[5]:
                            obj.set_value("Yaw", timeframe, float(pos_list[5]))
                        if pos_list[6]:
                            obj.set_value("x", timeframe, float(pos_list[6]))
                        if pos_list[7]:
                            obj.set_value("y", timeframe, float(pos_list[7]))
                        if pos_list[8]:
                            obj.set_value("Heading", timeframe, float(pos_list[8]))

            elif prop == "Name":
                obj.set_value(prop, timeframe, val)
            elif prop == "Parent" or prop == "FocusTarget" or prop == "LockedTarget":
                obj.set_value(prop, timeframe, self.parse_obj_id(val))
            elif prop == "Type":
                obj.set_value(prop, timeframe, val)
            elif prop in _STR_OBJECT_KEYS:
                obj.set_value(prop, timeframe, val)
            # numeric except coordinates start here
            # floats
            elif prop in _FLOAT_OBJECT_KEYS:
                obj.set_value(prop, timeframe, float(val))
            # int
            elif prop in _INT_OBJECT_KEYS:
                obj.set_value(prop, timeframe, int(val))
            else:
                obj.set_value(prop, timeframe, val)
                print("Unknown property:", prop)

    def _parse(self, filepath: str):

        def do_parse(f):
            ar = AcmiFileReader(f)
            rawline = next(ar)
            if rawline.startswith('FileType='):
                self.file_type = rawline[len('FileType='):].strip()
            else:
                raise RuntimeError("ACMI file doesn't start with FileType.")

            rawline = next(ar)
            if rawline.startswith('FileVersion='):
                self.file_version = float(rawline[len('FileVersion='):].strip())
                if self.file_version < 2.1:
                    raise RuntimeError("Unsupported file version: {v}".format(v=self.file_version))
            else:
                raise RuntimeError("ACMI file missing FileVersion.")

            cur_reftime = 0.0
            linenr = 2
            for rawline in ar:
                linenr += 1
                line = rawline.strip()  # type: str
                if not line or line.startswith('//'):
                    continue  # ignore comments

                if line.startswith('#'):
                    cur_reftime = float(line[1:])
                    self.timeframes.append(cur_reftime)
                    continue

                if line.startswith('-'):
                    obj_id = self.parse_obj_id(line[1:])
                    self.objects[obj_id].removed_at = cur_reftime
                else:
                    fields = self.split_fields(line)
                    obj_id = self.parse_obj_id(fields[0])

                    # print(obj_id, fields)
                    if obj_id == '0' or obj_id == 0:
                        self._parse_global_property(fields)
                    else:
                        self._parse_object_property(obj_id, cur_reftime, fields)

        # if zipfile.is_zipfile(filepath):
        #     raise RuntimeError("这是一个zip文件，请先将其解压（如果后缀是acmi，将acmi改成zip即可）: " + filepath)
        # 打开zip文件
        if zipfile.is_zipfile(filepath):
            with zipfile.ZipFile(file=filepath) as my_zip:
                # 打印zip文件中的文件列表

                # 读取zip文件中的一个文件
                for name in my_zip.namelist():
                    with my_zip.open(name) as f:
                        do_parse(io.TextIOWrapper(f, encoding=_ACMI_FILE_ENCODING))
        else:
            with open(filepath, 'r', encoding=_ACMI_FILE_ENCODING) as f:
                do_parse(f)

    def object_ids(self):
        return self.objects.keys()

    def alive_objects(self):
        return [self.objects[obj_key] for obj_key in self.objects if self.objects[obj_key].removed_at is None]

    def removed_objects(self):
        return [self.objects[objkey] for objkey in self.objects if self.objects[objkey].removed_at is not None]

    def json(self):
        return {
            "FileType"          : self.file_type,
            "FileVersion"       : self.file_version,
            "DataSource"        : self.data_source,
            "DataRecorder"      : self.data_recorder,
            "ReferenceTime"     : self.reference_time.isoformat(),
            "RecordingTime"     : self.recording_time.isoformat(),
            "Author"            : self.author,
            "Title"             : self.title,
            "Category"          : self.category,
            "Briefing"          : self.briefing,
            "Debriefing"        : self.debriefing,
            "Comments"          : self.comments,
            "ReferenceLongitude": self.reference_longitude,
            "ReferenceLatitude" : self.reference_latitude,
            "Objects"           : len(self.objects),
            "TimeFrames"        : len(self.timeframes),
        }

    def __str__(self):
        return json.dumps(obj=self.json(), indent=2, ensure_ascii=False)

    def export(self, export_filepath: str):
        with open(export_filepath, 'w', encoding='utf-8') as f:
            data = { "Global": self.json(), "Objects": [self.objects[k].json() for k in self.objects] }
            json.dump(data, f, ensure_ascii=False, indent=2)
