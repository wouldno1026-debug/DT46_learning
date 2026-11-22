import cv2
import numpy as np

# ========== 模式开关 ==========
# True  = 进入调参模式
# False = 进入正常识别模式
DEBUG_MODE = False

# ========== 调参类 ==========
class ThresholdTuner():

    def __init__(self, image_path):
        self.image_path = image_path
        self.photo = None
        self.hsv = None

    @staticmethod
    def nothing(x):
        """滑动条回调函数"""
        pass

    def debug_threshold_separated(self):
        self.photo = cv2.imread(self.image_path)
        if self.photo is None:
            print("图片读取失败，请检查图片路径！")
            return

        self.hsv = cv2.cvtColor(self.photo, cv2.COLOR_BGR2HSV)

        # --- 红色调参窗口 ---
        win_red = 'Red Tuner (红色调参)'
        cv2.namedWindow(win_red, cv2.WINDOW_NORMAL)
        cv2.createTrackbar('R_H1_Min', win_red, 0, 179, self.nothing)
        cv2.createTrackbar('R_H1_Max', win_red, 10, 179, self.nothing)
        cv2.createTrackbar('R_H2_Min', win_red, 170, 179, self.nothing)
        cv2.createTrackbar('R_H2_Max', win_red, 179, 179, self.nothing)
        cv2.createTrackbar('R_S_Min', win_red, 43, 255, self.nothing)
        cv2.createTrackbar('R_S_Max', win_red, 255, 255, self.nothing)
        cv2.createTrackbar('R_V_Min', win_red, 46, 255, self.nothing)
        cv2.createTrackbar('R_V_Max', win_red, 255, 255, self.nothing)

        # --- 蓝色调参窗口 ---
        win_blue = 'Blue Tuner (蓝色调参)'
        cv2.namedWindow(win_blue, cv2.WINDOW_NORMAL)
        cv2.createTrackbar('B_H_Min', win_blue, 100, 179, self.nothing)
        cv2.createTrackbar('B_H_Max', win_blue, 124, 179, self.nothing)
        cv2.createTrackbar('B_S_Min', win_blue, 43, 255, self.nothing)
        cv2.createTrackbar('B_S_Max', win_blue, 255, 255, self.nothing)
        cv2.createTrackbar('B_V_Min', win_blue, 46, 255, self.nothing)
        cv2.createTrackbar('B_V_Max', win_blue, 255, 255, self.nothing)

        print("=" * 60)
        print("🔧 分色调参模式已启动！按 'q' 或 'ESC' 键退出。")
        print("=" * 60)

        while True:
            # 获取滑块值
            r_h1_min = cv2.getTrackbarPos('R_H1_Min', win_red)
            r_h1_max = cv2.getTrackbarPos('R_H1_Max', win_red)
            r_h2_min = cv2.getTrackbarPos('R_H2_Min', win_red)
            r_h2_max = cv2.getTrackbarPos('R_H2_Max', win_red)
            r_s_min = cv2.getTrackbarPos('R_S_Min', win_red)
            r_s_max = cv2.getTrackbarPos('R_S_Max', win_red)
            r_v_min = cv2.getTrackbarPos('R_V_Min', win_red)
            r_v_max = cv2.getTrackbarPos('R_V_Max', win_red)

            b_h_min = cv2.getTrackbarPos('B_H_Min', win_blue)
            b_h_max = cv2.getTrackbarPos('B_H_Max', win_blue)
            b_s_min = cv2.getTrackbarPos('B_S_Min', win_blue)
            b_s_max = cv2.getTrackbarPos('B_S_Max', win_blue)
            b_v_min = cv2.getTrackbarPos('B_V_Min', win_blue)
            b_v_max = cv2.getTrackbarPos('B_V_Max', win_blue)

            # 生成红色掩膜
            mask_red1 = cv2.inRange(self.hsv, np.array([r_h1_min, r_s_min, r_v_min]), np.array([r_h1_max, r_s_max, r_v_max]))
            mask_red2 = cv2.inRange(self.hsv, np.array([r_h2_min, r_s_min, r_v_min]), np.array([r_h2_max, r_s_max, r_v_max]))
            red_mask = cv2.bitwise_or(mask_red1, mask_red2)

            # 生成蓝色掩膜
            blue_mask = cv2.inRange(self.hsv, np.array([b_h_min, b_s_min, b_v_min]), np.array([b_h_max, b_s_max, b_v_max]))

            cv2.imshow('Original', self.photo)
            cv2.imshow('Red Mask', red_mask)
            cv2.imshow('Blue Mask', blue_mask)

            # 终端实时打印
            print("\n" + "-"*80)
            print(f"[RED 红色] 段1: np.array([{r_h1_min:3d}, {r_s_min:3d}, {r_v_min:3d}]) ~ np.array([{r_h1_max:3d}, {r_s_max:3d}, {r_v_max:3d}])")
            print(f"[RED 红色] 段2: np.array([{r_h2_min:3d}, {r_s_min:3d}, {r_v_min:3d}]) ~ np.array([{r_h2_max:3d}, {r_s_max:3d}, {r_v_max:3d}])")
            print(f"[BLUE蓝色] 单段: np.array([{b_h_min:3d}, {b_s_min:3d}, {b_v_min:3d}]) ~ np.array([{b_h_max:3d}, {b_s_max:3d}, {b_v_max:3d}])")
            print("\033[F" * 4, end="")

            if cv2.waitKey(1) & 0xFF in [ord('q'), 27]:
                # 打印最终结果
                print("\n\n" + "="*60)
                print("✅ 最终调参结果（请直接复制替换）：")
                print(f"lower_red0 = np.array([{r_h1_min}, {r_s_min}, {r_v_min}], dtype=np.uint8)")
                print(f"upper_red0 = np.array([{r_h1_max}, {r_s_max}, {r_v_max}], dtype=np.uint8)")
                print(f"lower_red1 = np.array([{r_h2_min}, {r_s_min}, {r_v_min}], dtype=np.uint8)")
                print(f"upper_red1 = np.array([{r_h2_max}, {r_s_max}, {r_v_max}], dtype=np.uint8)")
                print("-" * 30)
                print(f"lower_blue = np.array([{b_h_min}, {b_s_min}, {b_v_min}], dtype=np.uint8)")
                print(f"upper_blue = np.array([{b_h_max}, {b_s_max}, {b_v_max}], dtype=np.uint8)")
                print("="*60)
                break

        cv2.destroyAllWindows()

# 数值存放
class Config():
    # ---------- 图片路径 ----------
    IMAGE_PATH = "photo.jpeg"

    # ---------- 颜色分割阈值 ----------

    LOWER_RED0 = np.array([0, 22, 228], dtype=np.uint8)
    UPPER_RED0 = np.array([51, 239, 255], dtype=np.uint8)

    LOWER_RED1 = np.array([166, 22, 228], dtype=np.uint8)
    UPPER_RED1 = np.array([179, 239, 255], dtype=np.uint8)

    LOWER_BLUE = np.array([0, 0, 100], dtype=np.uint8)
    UPPER_BLUE = np.array([118, 33, 255], dtype=np.uint8)

    MIN_PIXELS = 50

    # ---------- 灯条筛选参数 ----------

    W_H_RATIO = 2.0
    AREA_THRESHOLD = 50
    ANGLE_THRESHOLD = 30

    # ---------- 装甲板配对参数 ----------
    PAIR_ANGLE_DIFF = 20.0
    PAIR_HEIGHT_DIFF = 1.5
    PAIR_LENGTH_DIFF = 0.3
    PAIR_THICK_DIFF = 0.6

    ARMOR_RATIO_MIN = 1.8
    ARMOR_RATIO_MAX = 4.5

# 颜色分割
class ColorSegmenter:

    def color_segmentation(self, photo):

        hsv = cv2.cvtColor(photo, cv2.COLOR_BGR2HSV)

        mask_red0 = cv2.inRange(hsv, Config.LOWER_RED0, Config.UPPER_RED0)
        mask_red1 = cv2.inRange(hsv, Config.LOWER_RED1, Config.UPPER_RED1)
        red_mask = cv2.bitwise_or(mask_red0, mask_red1)

        blue_mask = cv2.inRange(hsv, Config.LOWER_BLUE, Config.UPPER_BLUE)

        red_px = cv2.countNonZero(red_mask)
        blue_px = cv2.countNonZero(blue_mask)

        red_detected = red_px >= Config.MIN_PIXELS
        blue_detected = blue_px >= Config.MIN_PIXELS

        color_data = {
            'hsv': hsv,

            'red': {
                'mask': red_mask,
                'pixel_count': red_px,
                'is_detected': bool(red_detected)
            },

            'blue': {
                'mask': blue_mask,
                'pixel_count': blue_px,
                'is_detected': bool(blue_detected)
            }
        }

        return color_data

# 形态学处理
class ImageProcessor:

    # ---------- 开运算 ----------
    def open_morphology(self, binary_photo, size):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, size)
        result = cv2.morphologyEx(binary_photo, cv2.MORPH_OPEN, kernel)
        return result

    # ---------- 闭运算 ----------
    def close_morphology(self, binary_photo, size):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, size)
        result = cv2.morphologyEx(binary_photo, cv2.MORPH_CLOSE, kernel)
        return result

    # ---------- 腐蚀 ----------
    def erode_morphology(self, binary_photo, size):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, size)
        result = cv2.erode(binary_photo, kernel)
        return result

    # ---------- 膨胀 ----------
    def dilate_morphology(self, binary_photo, size):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, size)
        result = cv2.dilate(binary_photo, kernel)
        return result

# 轮廓检测
class LightBarDetector:

    # ---------- 轮廓检测 ----------
    def find_contours(self, color_data):
        for color in ['red', 'blue']:

            if not color_data[color]['is_detected']:
                color_data[color]['contours'] = []
                continue

            mask = color_data[color]['mask']

            # 提取外轮廓
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 提取每个轮廓的矩形信息
            color_data[color]['contours'] = self.data_insert(contours)

        return color_data

    # ---------- 提取轮廓数据 ----------
    def data_insert(self, contours):
        """提取每个轮廓的矩形信息并记录。"""

        data_list = []

        for contour in contours:

            area = cv2.contourArea(contour)

            if area < 20:
                continue

            rect = cv2.minAreaRect(contour)
            (rect_x, rect_y), (rect_w, rect_h), z = rect

            if rect_w < rect_h:
                rect_w, rect_h = rect_h, rect_w
                z = float(z) + 90

            # 使用调整后的参数重新构造矩形
            rect = ((rect_x, rect_y), (rect_w, rect_h), z)

            coor = cv2.boxPoints(rect)

            data_list.append({
                "area": area,
                "rx": rect_x,
                "ry": rect_y,
                "rh": rect_h,
                "rw": rect_w,
                "z": z,
                "coo": coor
            })

        return data_list

    # ---------- 灯条筛选 ----------
    def filter_light_bars(
        self,
        color_data,
        w_h_ratio=Config.W_H_RATIO,
        area_threshold=Config.AREA_THRESHOLD,
        angle_threshold=Config.ANGLE_THRESHOLD
    ):
        """
        灯条筛选：对红蓝两路分别执行灯条筛选。
        将筛选结果存入 color_data[color]['selected'] 中。
        """

        for color in ['red', 'blue']:

            if not color_data[color]['is_detected']:
                color_data[color]['selected'] = []
                continue

            contours = color_data[color].get('contours', [])
            selected_list = []

            for cnt in contours:

                # 1. 面积过滤
                if cnt['area'] < area_threshold:
                    continue

                # 2. 长宽比过滤
                ratio = cnt['rw'] / (cnt['rh'] + 0.1)

                if ratio < w_h_ratio:
                    continue

                # 3. 角度过滤
                angle_dev = abs(cnt['z'] % 180 - 90)

                if angle_dev > angle_threshold:
                    continue

                selected_list.append(cnt)

            # 存入字典
            color_data[color]['selected'] = selected_list

        return color_data

# 灯条检测
class ArmorMatcher:

    def pair_lights(self, color_data,
                    pair_angle_diff = Config.PAIR_ANGLE_DIFF,
                    pair_height_diff = Config.PAIR_HEIGHT_DIFF,
                    pair_length_diff = Config.PAIR_LENGTH_DIFF,
                    pair_thick_diff = Config.PAIR_THICK_DIFF,
                    armor_ratio_min = Config.ARMOR_RATIO_MIN,
                    armor_ratio_max = Config.ARMOR_RATIO_MAX):

        armor_list = []

        # 分别处理红色和蓝色灯条
        for color in ['red', 'blue']:

            if not color_data[color]['is_detected']:
                continue

            lights = color_data[color].get('selected', [])
            n = len(lights)

            if n < 2:
                continue

            # 遍历所有可能的灯条组合
            for i in range(n):
                for j in range(i + 1, n):

                    light_i = lights[i]
                    light_j = lights[j]

                    rxi, ryi = light_i['rx'], light_i['ry']
                    rwi, rhi = light_i['rw'], light_i['rh']
                    zi = light_i['z']

                    rxj, ryj = light_j['rx'], light_j['ry']
                    rwj, rhj = light_j['rw'], light_j['rh']
                    zj = light_j['z']

                    # 1. 判断两根灯条的角度差
                    angle_diff = abs(zi - zj) % 180
                    angle_diff = min(angle_diff, 180 - angle_diff)

                    if angle_diff > pair_angle_diff:
                        continue

                    # 2. 判断两根灯条的中心高度差
                    avg_length = (rwi + rwj) / 2

                    if abs(ryi - ryj) > pair_height_diff * avg_length:
                        continue

                    # 3. 判断两根灯条的长度差
                    if abs(rwi - rwj) > pair_length_diff * max(rwi, rwj):
                        continue

                    # 4. 判断两根灯条的宽度差
                    if abs(rhi - rhj) > pair_thick_diff * max(rhi, rhj):
                        continue

                    # 5. 计算两根灯条中心之间的距离
                    l_w = ((rxi - rxj) ** 2 + (ryi - ryj) ** 2) ** 0.5
                    l_h = (rwi + rwj) / 2

                    if l_h <= 0:
                        continue

                    # 6. 判断装甲板的宽高比例
                    ratio = l_w / l_h

                    if ratio < armor_ratio_min or ratio > armor_ratio_max:
                        continue

                    # 7. 确定左右灯条
                    if rxi < rxj:
                        left, right = light_i, light_j
                    else:
                        left, right = light_j, light_i

                    # 8. 计算装甲板中心
                    cx = (rxi + rxj) / 2
                    cy = (ryi + ryj) / 2

                    armor_list.append({
                        'color': color,
                        'center': (cx, cy),
                        'left': left,
                        'right': right,
                        'width': l_w,
                        'height': l_h,
                        'ratio': ratio
                    })

        return self.deduplicate_armors(armor_list)


    def deduplicate_armors(self, armor_list):

        if not armor_list:
            return []

        # 优先保留面积较大的候选装甲板
        armor_list.sort(key=lambda a: a['width'] * a['height'], reverse=True)

        used_lights = set()
        result = []

        for armor in armor_list:

            left_id = id(armor['left'])
            right_id = id(armor['right'])

            # 如果两根灯条都没有被使用过
            if left_id not in used_lights and right_id not in used_lights:

                result.append(armor)

                used_lights.add(left_id)
                used_lights.add(right_id)

        return result

# 绘制图像
class Visualizer:

    def draw_results(self, photo, color_data, armors):

        result = photo.copy()

        # 1. 绘制筛选后的灯条
        for color in ['red', 'blue']:

            selected = color_data[color].get('selected', [])

            for light in selected:

                # 获取灯条的四个顶点
                corners = np.int32(light['coo'])

                # 根据灯条颜色选择绘制颜色
                if color == 'red':
                    draw_color = (0, 0, 255)
                else:
                    draw_color = (255, 0, 0)

                # 绘制灯条矩形
                cv2.drawContours(result, [corners], -1, draw_color, 2)

                # 绘制灯条中心点
                center = (int(light['rx']), int(light['ry']))

                cv2.circle(result, center, 3, draw_color, -1)

        # 2. 绘制装甲板
        for armor in armors:

            cx, cy = armor['center']
            center = (int(cx), int(cy))

            # 绘制装甲板中心点
            cv2.circle(result, center, 5, (0, 255, 0), -1)

            # 显示装甲板中心坐标
            text = f"({int(cx)}, {int(cy)})"

            cv2.putText(result,
                text,
                (int(cx) + 10, int(cy) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        return result

# 识别总流程
class ArmorDetector:

    def __init__(self):

        # 创建各个功能模块的对象
        self.segmenter = ColorSegmenter()
        self.processor = ImageProcessor()
        self.light_detector = LightBarDetector()
        self.matcher = ArmorMatcher()
        self.visualizer = Visualizer()

    def detect(self, photo):

        # 1. 颜色分割
        color_data = self.segmenter.color_segmentation(photo)

        # 2. 对红色和蓝色掩膜进行形态学处理

        # 红色：开运算 -> 闭运算
        color_data['red']['mask'] = self.processor.open_morphology(color_data['red']['mask'], (3, 3))
        color_data['red']['mask'] = self.processor.close_morphology(color_data['red']['mask'], (3, 3))

        # 蓝色：开运算 -> 闭运算
        color_data['blue']['mask'] = self.processor.open_morphology(color_data['blue']['mask'], (3, 3))
        color_data['blue']['mask'] = self.processor.close_morphology(color_data['blue']['mask'], (3, 3))

        # 3. 提取轮廓
        color_data = self.light_detector.find_contours(color_data)

        # 4. 筛选灯条
        color_data = self.light_detector.filter_light_bars(color_data)

        # 5. 灯条配对，寻找装甲板
        armors = self.matcher.pair_lights(color_data)

        # 6. 绘制检测结果
        result = self.visualizer.draw_results(photo, color_data, armors)

        return color_data, armors, result

# 主程序
def main():

    # 调参模式
    if DEBUG_MODE:
        tuner = ThresholdTuner(Config.IMAGE_PATH)
        tuner.debug_threshold_separated()
        return

    # 读取图片
    photo = cv2.imread(Config.IMAGE_PATH)

    if photo is None:
        raise ValueError("无法读取图片，请检查图片路径")

    # 创建装甲板检测器
    detector = ArmorDetector()

    # 执行检测
    color_data, armors, result = detector.detect(photo)

    # 输出检测信息
    print("红色灯条数量：", len(color_data['red']['selected']))
    print("蓝色灯条数量：", len(color_data['blue']['selected']))
    print("检测到的装甲板数量：", len(armors))

    # 显示检测结果
    cv2.imshow("Detection Result", result)

    # 保存检测结果
    cv2.imwrite("result_output.jpg", result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()