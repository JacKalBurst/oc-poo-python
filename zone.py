from position import Position


class Zone:
    EARTH_RADIUS_KILOMETERS = 6371
    MIN_LONGITUDE_DEGREES = -180
    MAX_LONGITUDE_DEGREES = 180
    MIN_LATITUDE_DEGREES = -90
    MAX_LATITUDE_DEGREES = 90
    WIDTH_DEGREES = 1  # degrees of longitude
    HEIGHT_DEGREES = 1  # degrees of latitude
    ZONES = []

    def __init__(self, bottom_left_corner, top_right_corner):
        self.bottom_left_corner = bottom_left_corner
        self.top_right_corner = top_right_corner
        self.inhabitants = []

    @property
    def width(self):
        return abs(self.bottom_left_corner.longitude - self.top_right_corner.longitude) * self.EARTH_RADIUS_KILOMETERS

    @property
    def height(self):
        return abs(self.bottom_left_corner.latitude - self.top_right_corner.latitude) * self.EARTH_RADIUS_KILOMETERS

    @property
    def area(self):
        return self.height * self.width

    def population_density(self):
        return self.population / self.area

    def average_agreeableness(self):
        if not self.inhabitants:
            return 0
        return sum([inhabitant.agreeableness for inhabitant in self.inhabitants]) / self.population

    def add_inhabitant(self, inhabitant):
        self.inhabitants.append(inhabitant)

    @property
    def population(self):
        return len(self.inhabitants)

    @classmethod
    def _initialize_zones(cls):
        for latitude in range(cls.MIN_LATITUDE_DEGREES, cls.MAX_LATITUDE_DEGREES, cls.HEIGHT_DEGREES):
            for longitude in range(cls.MIN_LONGITUDE_DEGREES, cls.MAX_LONGITUDE_DEGREES, cls.WIDTH_DEGREES):
                bottom_left_corner = Position(longitude, latitude)
                top_right_corner = Position(longitude + cls.WIDTH_DEGREES, latitude + cls.HEIGHT_DEGREES)
                zone = Zone(bottom_left_corner, top_right_corner)
                cls.ZONES.append(zone)
        print(len(cls.ZONES))

    def contains(self, position):
        return position.longitude >= min(self.bottom_left_corner.longitude, self.top_right_corner.longitude) and \
               position.longitude < max(self.bottom_left_corner.longitude, self.top_right_corner.longitude) and \
               position.latitude >= min(self.bottom_left_corner.latitude, self.top_right_corner.latitude) and \
               position.latitude < max(self.bottom_left_corner.latitude, self.top_right_corner.latitude)

    @classmethod
    def find_zone_that_contains(cls, position):
        if not cls.ZONES:
            # Initialize zones automatically if necessary
            cls._initialize_zones()
        # Compute the index in the ZONES array that contains the given position
        longitude_index = int((position.longitude_degrees - cls.MIN_LONGITUDE_DEGREES) / cls.WIDTH_DEGREES)
        latitude_index = int((position.latitude_degrees - cls.MIN_LATITUDE_DEGREES) / cls.HEIGHT_DEGREES)
        longitude_bins = int(
            (cls.MAX_LONGITUDE_DEGREES - cls.MIN_LONGITUDE_DEGREES) / cls.WIDTH_DEGREES)  # 180-(-180) / 1
        zone_index = latitude_index * longitude_bins + longitude_index

        # Just checking that the index is correct
        zone = cls.ZONES[zone_index]
        assert zone.contains(position)

        return zone
