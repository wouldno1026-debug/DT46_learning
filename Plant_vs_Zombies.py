class Plant:

    # 基础信息与数值
    def __init__(self, name, hp, cost, cooldown, plantable_on):
        self.name = name
        self.hp = hp
        self.cost = cost
        self.cooldown = cooldown
        self.plantable_on = plantable_on

    # 种植方法
    @classmethod
    def set(cls):
        global sunshine

        plant = cls()

        if sunshine < plant.cost:
            print("阳光不够，无法种植")
            return None

        sunshine -= plant.cost

        print(f"{plant.name}种植成功，剩余阳光：{sunshine}")

        return plant

    # 受到伤害
    def take_damage(self, damage):

        # 如果植物已经死亡，不再处理伤害
        if self.hp <= 0:
            return self.hp

        self.hp -= damage

        if self.hp <= 0:
            self.hp = 0
            self.die()

        return self.hp


    # 植物行为
    def action(self):
        pass

    # 死亡信息
    def die(self):
        print(f"你的{self.name}已阵亡")


# 豌豆射手
class Peashooter(Plant):

    def __init__(self):
        super().__init__("豌豆射手", 300, 100, 7.5, ["草地", "睡莲", "花盆"])

        self.hurt = 20

    def action(self):
        print(f"{self.name}射出了豌豆, 对僵尸造成{self.hurt}点伤害")

# 向日葵
class Sunflower(Plant):

    def __init__(self):
        super().__init__("向日葵", 300, 50, 7.5, ["草地", "睡莲", "花盆"])

        self.sunlight = 25

    def action(self):
        global sunshine
        sunshine += self.sunlight
        print(f"{self.name}产生了{self.sunlight}的阳光，剩余{sunshine}的阳光")

# 坚果
class WallNut(Plant):

    def __init__(self):
        super().__init__("坚果", 4000, 50, 30, ["草地", "睡莲", "花盆"])

        self.max_hp = self.hp
        self.damage_level = "完好"

    # 更新受损等级
    def update_damage_level(self):
        if self.hp > 0:
            if self.hp > self.max_hp * 2/3:
                self.damage_level = "完好"
            elif self.hp > self.max_hp * 1/3:
                self.damage_level = "轻度受损"
            else:
                self.damage_level = "严重受损"

        else:
            self.damage_level = None

        return self.damage_level

    # 重写受到伤害的方法
    def take_damage(self, damage):
        super().take_damage(damage)

        self.update_damage_level()

        print(f"受到{damage}点伤害，受损程度为{self.damage_level}")

        return self.hp

if __name__ == "__main__":
    # 初始阳光1000
    sunshine = 1000
    # 调用方法，扣除对应阳光创建实例
    peashooter1 = Peashooter.set()
    sunflower1 = Sunflower.set()
    wallnut1 = WallNut.set()

    # 植物行动
    if sunflower1:
        sunflower1.action()

    peashooter1.action()

    wallnut1.take_damage(2700)
    