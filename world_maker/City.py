from District import District, Road
from Position import Position
from PIL import Image
import random
from data_analysis import handle_import_image
from typing import Union
import numpy as np


class City:
    """
    Attributes:
        districts (list): The list of districts in the city.
        map_data (list): The 2D list representing the map of the city.
        height_map (list): The 2D list representing the height map of the city.
    """

    def __init__(self):
        """
        The constructor for the City class.
        """
        self.districts = []
        self.map_data = []
        self.height_map = []
        self.init_maps()

    def init_maps(self):
        """
        Initialize the maps of the city. It reads the heightmap and watermap images and converts them into 2D lists.
        """
        heightmap = Image.open('./data/heightmap.png').convert('L')
        watermap = Image.open('./data/watermap.png').convert('L')
        width, height = heightmap.size
        self.map_data = [[-1 if watermap.getpixel((x, y)) > 0 else 0 for x in range(width)] for y in range(height)]
        self.height_map = [[heightmap.getpixel((x, y)) for x in range(width)] for y in range(height)]
        watermap.close()
        heightmap.close()

    def add_district(self, center: Position, district_type: str = ""):
        """
        Add a new district to the city.

        :param district_type:
        :param center: The center position of the new district.
        """
        self.districts.append(District(len(self.districts) + 1, center, district_type))
        self.map_data[center.y][center.x] = len(self.districts)

    def is_expend_finished(self):
        """
        Check if the expansion of all districts in the city is finished.

        :return: True if the expansion is finished, False otherwise.
        """
        for district in self.districts:
            if len(district.area_expend_from_point) > 0:
                return False
        return True

    def choose_expend_point(self, point: Position, index_district: int):
        """
        Choose a point to expand a district based on the distance between the center of the district and the point itself.

        :param point: The point to be expanded.
        :param index_district: The index of the district to be expanded.
        """
        min_distance = point.distance_to(self.districts[index_district].center_expend)
        index_district_chosen = index_district
        for index in range(index_district + 1, len(self.districts)):
            if point in self.districts[index].area_expend:
                distance = point.distance_to(self.districts[index].center_expend)
                if distance < min_distance:
                    min_distance = distance
                    self.districts[index_district_chosen].area_expend.remove(point)
                    index_district_chosen = index
                else:
                    self.districts[index].area_expend.remove(point)
        self.districts[index_district_chosen].area_expend_from_point.append(point)
        self.districts[index_district_chosen].area_expend.remove(point)
        self.map_data[point.y][point.x] = index_district_chosen + 1

    def update_expend_district(self):
        """
        Update the expansion points of all districts in the city.
        """
        for district in self.districts:
            if len(district.area_expend_from_point) > 0:
                district.update_expend_points(district.area_expend_from_point[0], self.map_data, self.height_map)
        for district in self.districts:
            for point in district.area_expend:
                self.choose_expend_point(point, district.tile_id - 1)

    def loop_expend_district(self):
        """
        Loop the expansion of all districts in the city until all districts are fully expanded.
        """
        print("[City] Start expanding districts...")
        while not self.is_expend_finished():
            self.update_expend_district()
        print("[City] Finished expanding districts.")

    def district_draw_map(self):
        """
        Draw the map of the city with different colors for each district.
        """
        width, height = len(self.map_data[0]), len(self.map_data)
        img = Image.new('RGB', (width, height))
        colors = {id_district: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                  for id_district in range(1, len(self.districts) + 1)}

        for y in range(height):
            for x in range(width):
                if self.map_data[y][x] <= 0:
                    img.putpixel((x, y), (0, 0, 0))
                else:
                    img.putpixel((x, y), colors[self.map_data[y][x]])

        img.save('./data/district.png')
        print("[City] District map created.")

    def draw_roads(self, image: Union[str, Image], size: int = 1) -> Image:
        """
        Draw the roads of the city on the image.

        :param size:
        :param image: The image to draw the roads on.
        """
        image = handle_import_image(image)
        for district in self.districts:
            district.draw_roads(image, size)
        return image

    def district_generate_road(self) -> list[Road]:
        """
        Generate the roads of the city for each district.

        :return: The list of roads of the city.
        """
        roads = []
        for district in self.districts:
            district.generate_roads(self.map_data)
            roads.extend(district.roads)
        return roads

    def point_in_which_district(self, point: Union[Position, tuple[int, int]]) -> int:
        """
        Get the index of the district in which the point is located.

        :param point: The point to check.
        :return: The index of the district in which the point is located.
        """
        if isinstance(point, Position):
            point = (point.x, point.y)
        return self.map_data[point[1]][point[0]]

    def get_district_mountain_map(self) -> Image:
        """
        Get the map of a district.

        :param district_id: The id of the district.
        :return: The map of the district.
        """
        district_id = [district.tile_id for district in self.districts if district.type == "mountain"]
        array = np.array([[True if self.map_data[y][x] in district_id else False for x in range(len(self.map_data[0]))]
                          for y in range(len(self.map_data))])
        image = Image.fromarray(array)
        image.save('./data/mountain_map.png')
        return image


if __name__ == '__main__':
    city = City()
    for i in range(10):
        city.add_district(Position(random.randint(0, 400), random.randint(0, 400)))
    city.loop_expend_district()
    city.district_draw_map()
    city.district_generate_road()
    image = city.draw_roads(Image.new('RGB', (401, 401)),4)
    image.save('./data/roadmap.png')
