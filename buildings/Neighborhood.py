from buildings.BuildingBlock import BuildingBlock
from buildings.geometry.Rectangle import Rectangle
from buildings.geometry.Point import Point

class Neighborhood:
    def __init__(self, buildings: list[tuple[tuple[int,int,int], tuple[int,int,int]]]):
        self.buildings = self.format_buildings(buildings)
        self.blocks = self.get_blocks()
        
    def format_buildings(self, buildings):
        return [Rectangle(Point(p=building[0]), Point(p=building[1])) for building in buildings]
    
    def get_blocks(self) -> list[BuildingBlock]:
        blocks = [] 
        remaining = self.buildings.copy()
        for building in remaining:
            blocks.append(self.get_block(building, remaining))
            
        return blocks
    
    def get_block(self, building : Rectangle, remaining : list[Rectangle]) -> BuildingBlock:
        block = []
        for rect in remaining:
            if building.is_adjacent(rect):
                block.append(rect)
                remaining.remove(rect)
                
        return BuildingBlock(block) 
        
        