__version__ = "0.0.1"

import math
import cv2
import numpy as np

from cvzoomwindow import affine

class CvZoomWindow:

    def __init__(self, winname : str, back_color = (128, 128, 0), inter = cv2.INTER_NEAREST):
        '''Instantiate the CvZoomWindow class.

        Parameters
        ----------
        winname : str
            Name of the window
        back_color : tuple, optional
            background color, by default (128, 128, 0)
        inter : optional
            interpolation methods, by default cv2.INTER_NEAREST
        '''

        self.__winname = winname        # namedWindowのタイトル
        self.__back_color = back_color  # 背景色
        self.__inter = inter            # 補間表示モード

        self.__src_image = None
        self.__disp_image = None
        self.__affine_matrix = affine.identityMatrix()
        self.__old_affine_matrix = affine.identityMatrix()

        self.__zoom_delta = 1.5
        self.__min_scale = 0.01
        self.__max_scale = 300

        self.__bright_disp_enabled = True # 輝度値の表示／非表示設定
        self.__min_bright_disp_scale = 30 # 輝度値を表示する最小倍率
        self.__grid_disp_enabled = True # グリッド線の表示／非表示設定
        self.__grid_color = (128, 128, 0) # グリッド線の色
        self.__min_grid_disp_scale = 20 # グリッド線を表示する最小倍率

        # 鼠标事件相关属性 - 确保全部正确初始化
        self.__mouse_event_enabled = True
        self.__mouse_down_flag = False  # 鼠标按下标志
        self.__old_point_x = 0          # 上次鼠标位置X - 使用私有属性
        self.__old_point_y = 0          # 上次鼠标位置Y - 使用私有属性
        self.__current_mouse_x = 0      # 当前鼠标位置X - 用于滚轮缩放中心
        self.__current_mouse_y = 0      # 当前鼠标位置Y - 用于滚轮缩放中心
        self.__mouse_callback_func = None
        
        # 旋转相关属性
        self.__rotation_center_x = 0    # 旋转中心X坐标（窗口坐标）
        self.__rotation_center_y = 0    # 旋转中心Y坐标（窗口坐标）
        self.__rotation_center_set = False  # 旋转中心是否已设置
        self.__rotation_in_progress = False  # 是否正在旋转
        self.__old_rotation_angle = 0   # 上次的旋转角度
        self.__old_rotation_angle_for_drag = 0  # 用于拖动旋转的旧角度
        self.__right_button_down_pos = (0, 0)  # 右键按下的位置

        # Window creation with debugging
        print(f"Creating window: {winname}")
        try:
            cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
            print("Window created successfully")
        except Exception as e:
            print(f"Error creating window: {e}")

        # コールバック関数の登録 with debugging
        try:
            cv2.setMouseCallback(winname, self._onMouse, winname)
            print("Mouse callback set successfully")
        except Exception as e:
            print(f"Error setting mouse callback: {e}")

    @property
    def winname(self) -> str:
        '''Get window name

        Returns
        -------
        str
            window name
        '''
        return self.__winname
    
    @property
    def zoom_delta(self) -> float:
        return self.__zoom_delta
    @zoom_delta.setter
    def zoom_delta(self, value : float):
        '''Get and set the zoom factor per notch of the mouse wheel.

        Parameters
        ----------
        value : float
            zoom factor per notch of the mouse wheel.( > 1)
        '''
        self.__zoom_delta = value

    @property
    def scale(self) -> float:
        '''Gets the current image display zoom factor.
        '''      
        return self.__affine_matrix[0, 0]

    @property
    def min_scale(self) -> float:
        return self.__min_scale
    @min_scale.setter
    def min_scale(self, value : float):
        '''Gets and sets the minimum display zoom factor.

        Parameters
        ----------
        value : float
            minimum zoom factor
        '''
        self.__min_scale = value

    @property
    def max_scale(self) -> float:
        return self.__max_scale
    @max_scale.setter
    def max_scale(self, value : float):
        '''Gets and sets the maximum display zoom factor.

        Parameters
        ----------
        value : float
            maximum zoom factor.
        '''
        self.__max_scale = value

    @property
    def inter(self):
        return self.__inter 
    @inter.setter
    def inter(self, value):
        '''Gets and sets the interpolation mode.(OpenCV enum cv::InterpolationFlags)
        '''
        self.__inter = value

    @property
    def mouse_event_enabled(self) -> bool:
        return self.__mouse_event_enabled
    @mouse_event_enabled.setter
    def mouse_event_enabled(self, value : bool):
        '''Enables(True)/disables(False) image scaling and movement by mouse operation.

        Parameters
        ----------
        value : bool
            mouse operation enable
        '''
        self.__mouse_event_enabled = value

    @property
    def affine_matrix(self):
        return self.__affine_matrix 
    @affine_matrix.setter
    def affine_matrix(self, value):
        '''Gets and sets the affine transformation matrix.

        Parameters
        ----------
        value : np.ndarray
            affine matrix
        '''
        self.__affine_matrix = value

    @property
    def bright_disp_enabled(self) -> bool:
        return self.__bright_disp_enabled 
    @bright_disp_enabled.setter
    def bright_disp_enabled(self, value : bool):
        '''Gets and sets the display/non-display settings for luminance values.

        Parameters
        ----------
        value : bool
            True : display
            False : non-display
        '''
        self.__bright_disp_enabled = value

    @property
    def grid_disp_enabled (self) -> bool:
        return self.__grid_disp_enabled 
    @grid_disp_enabled .setter
    def grid_disp_enabled (self, value : bool):
        '''Gets and sets the display/non-display settings for grid lines

        Parameters
        ----------
        value : bool
            True : display
            False : non-display
        '''
        self.__grid_disp_enabled  = value

    @property
    def grid_color (self):
        return self.__grid_color 
    @grid_color .setter
    def grid_color (self, value):
        '''Gets and sets the color of the grid lines.

        Parameters
        ----------
        value : 
            Line color.
        '''
        self.__grid_color  = value   

    @property
    def min_grid_disp_scale(self) -> float:
        return self.__min_grid_disp_scale
    @min_grid_disp_scale.setter
    def min_grid_disp_scale(self, value : float):
        '''Minimum scale factor for displaying grid lines

        Parameters
        ----------
        value : float
            Minimum scale
        '''
        self.__min_grid_disp_scale = value

    @property
    def min_bright_disp_scale(self) -> float:
        return self.__min_bright_disp_scale
    @min_bright_disp_scale.setter
    def min_bright_disp_scale(self, value : float):
        '''Gets or sets the minimum scale factor at which luminance values are to be displayed.

        Parameters
        ----------
        value : float
            minimum scale
        '''
        self.__min_bright_disp_scale = value

    @property
    def displayed_image(self):
        '''Gets the image displayed in the window.
        '''
        return self.__disp_image
        
    def imshow(self, image, zoom_fit : bool = True):
        '''Image display

        Parameters
        ----------
        image : np.ndarray
            Image data to display
        zoom_fit : bool
            True : Display images in the entire window (default)     
            False :Do not display images in the entire window         
        '''
        # 移除过多的打印语句以提高性能
        if image is None:
            return

        # 只有当图像改变时才更新源图像和执行zoom_fit
        # 如果是同一图像的重复调用，只重绘
        if self.__src_image is None or not np.array_equal(self.__src_image, image):
            self.__src_image = image
            if zoom_fit:
                self.zoom_fit()
            else:
                self.redraw_image()
        else:
            # 对于重复调用同一图像，只重绘
            self.redraw_image()

    def redraw_image(self):
        '''Image redraw
        '''

        if self.__src_image is None:
            return
        
        try:
            rect = cv2.getWindowImageRect(self.__winname)
            if rect[2] == 0 or rect[3] == 0:
                # 设置默认窗口大小
                win_width, win_height = 800, 600
                cv2.resizeWindow(self.__winname, win_width, win_height)
                # 再次尝试获取窗口大小
                rect = cv2.getWindowImageRect(self.__winname)
                if rect[2] == 0 or rect[3] == 0:
                    win_width, win_height = 800, 600
                else:
                    _, _, win_width, win_height = rect
            else:
                _, _, win_width, win_height = rect
        except Exception:
            win_width, win_height = 800, 600

        try:
            self.__disp_image = cv2.warpAffine(self.__src_image, self.__affine_matrix[:2,], (win_width, win_height), 
                                             flags = self.__inter, borderValue = self.__back_color)
        except Exception:
            return
        
        if self.__grid_disp_enabled is True:
            if self.__affine_matrix[0, 0] > self.__min_grid_disp_scale:
                # Grid線を表示する条件が揃っているとき
                try:
                    self._draw_grid_line()
                except Exception:
                    pass

        if self.__bright_disp_enabled is True:
            if self.__affine_matrix[0, 0] > self.__min_bright_disp_scale:
                # 輝度値を表示する条件が揃っているとき
                try:
                    self._draw_bright_value()
                except Exception:
                    pass
                
        # 如果设置了旋转中心，绘制标记
        if self.__rotation_center_set and self.__disp_image is not None:
            try:
                # 确保坐标在有效范围内
                h, w = self.__disp_image.shape[:2]
                cx = max(0, min(int(self.__rotation_center_x), w-1))
                cy = max(0, min(int(self.__rotation_center_y), h-1))
                
                # 绘制红色十字标记，更明显的样式
                center_size = 15
                # 横线
                cv2.line(self.__disp_image, 
                         (cx - center_size, cy),
                         (cx + center_size, cy),
                         (0, 0, 255), 3, cv2.LINE_AA)
                # 竖线
                cv2.line(self.__disp_image, 
                         (cx, cy - center_size),
                         (cx, cy + center_size),
                         (0, 0, 255), 3, cv2.LINE_AA)
                # 绘制红色圆圈
                cv2.circle(self.__disp_image, 
                          (cx, cy),
                          8, (0, 0, 255), -1)
                # 绘制白色边框，使标记更突出
                cv2.circle(self.__disp_image, 
                          (cx, cy),
                          8, (255, 255, 255), 2, cv2.LINE_AA)
            except Exception as e:
                print(f"绘制旋转中心标记出错: {e}")
        
        try:
            # 确保disp_image不为None
            if self.__disp_image is not None:
                cv2.imshow(self.__winname, self.__disp_image)
                # 必须调用waitKey以允许窗口刷新，但只返回键值而不打印
                cv2.waitKey(1)  # 最小等待时间，确保窗口刷新
        except Exception as e:
            print(f"Error displaying image: {e}")
        

    def zoom_fit(self, image_width : int = 0, image_height : int = 0):
        '''Display the image in the entire window

        Parameters
        ----------
        image_width : int, optional
            Image Width, by default 0
        image_height : int, optional
            Image Height, by default 0
        '''
        # 移除过多的打印语句以提高性能
        if self.__src_image is not None:
            # 画像データが表示されているとき
            # 画像のサイズ
            image_width = self.__src_image.shape[1]
            image_height = self.__src_image.shape[0]
        else:
            # 画像データが表示されていないとき
            if image_width == 0 or image_height == 0:
                # 画像サイズが指定されていないときは、何もしない
                return   

        # 画像表示領域のサイズ
        try:
            _, _, win_width, win_height = cv2.getWindowImageRect(self.__winname)
        except Exception:
            # 使用默认窗口尺寸作为回退
            win_width, win_height = 800, 600

        if (image_width * image_height <= 0):
            return
            
        # 如果窗口尺寸无效，使用默认值
        if (win_width * win_height <= 0):
            win_width, win_height = 800, 600

        # アフィン変換の初期化
        self.__affine_matrix = affine.identityMatrix()

        scale = 1.0
        offsetx = 0.0
        offsety = 0.0

        if (win_width * image_height) > (image_width * win_height):
            # ウィジェットが横長（画像を縦に合わせる）
            scale = win_height / image_height
            # あまり部分の半分を中央に寄せる
            offsetx = (win_width - image_width * scale) / 2.0
        else:
            # ウィジェットが縦長（画像を横に合わせる）
            scale = win_width / image_width
            # あまり部分の半分を中央に寄せる
            offsety = (win_height - image_height * scale) / 2.0

        # 画素の中心分(0.5画素)だけ移動する。
        self.__affine_matrix = affine.translateMatrix(0.5, 0.5).dot(self.__affine_matrix)
        # 拡大縮小
        self.__affine_matrix = affine.scaleMatrix(scale).dot(self.__affine_matrix)
        # あまり部分を中央に寄せる
        self.__affine_matrix = affine.translateMatrix(offsetx, offsety).dot(self.__affine_matrix)

        # 描画
        self.redraw_image()
        
    def zoom(self, delta : float):
        '''Zoom in/out the image based on the center of the window.

        Parameters
        ----------
        delta : _type_
            relative zoom factor
            value > 1 : zoom up
            value < 1 : zoom down
        '''
        print(f"zoom called with delta: {delta}")
        # 画像表示領域のサイズ
        try:
            _, _, win_width, win_height = cv2.getWindowImageRect(self.__winname)
            center_x = win_width/2.0
            center_y = win_height/2.0
            print(f"Window center: ({center_x}, {center_y})")
        except:
            print('zoom error - window not available')
            return

        self.zoom_at(delta, win_width/2.0, win_height/2.0)

    def zoom_at(self, delta: float, wx : float, wy : float):
        '''Scale up/down the image based on the specified coordinates of the window.

        Parameters
        ----------
        delta : float
            relative zoom factor
        wx : float
            Window X-coordinate
        wy : float
            Window Y-coordinate
        '''
        print(f"zoom_at called with delta: {delta}, center: ({wx}, {wy})")
        print(f"Current scale: {self.__affine_matrix[0, 0]}")

        if delta >= 1.0:
            # マウスホイールを上に回したとき、画像の拡大
            new_scale = self.__affine_matrix[0, 0] * delta
            print(f"Zooming in: new_scale = {new_scale}, max_scale = {self.__max_scale}")
            if new_scale > self.__max_scale:
                print("Scale exceeds maximum limit, not zooming")
                return
            self.__affine_matrix = affine.scaleAtMatrix(delta, wx, wy).dot(self.__affine_matrix)
              
        elif delta > 0.0:
            # マウスホイールを下に回したとき、画像の縮小
            new_scale = self.__affine_matrix[0, 0] * delta
            print(f"Zooming out: new_scale = {new_scale}, min_scale = {self.__min_scale}")
            if new_scale < self.__min_scale:
                print("Scale below minimum limit, not zooming")
                return
            self.__affine_matrix = affine.scaleAtMatrix(delta, wx, wy).dot(self.__affine_matrix)
        else:
            print("Invalid delta value, not zooming")
            return

        print(f"New affine matrix: {self.__affine_matrix}")
        self.redraw_image()

    def pan(self, tx : float, ty : float):
        '''Moves and displays images.

        Parameters
        ----------
        tx : float
            Amount of movement in X direction
        ty : float
            Amount of movement in Y direction
        '''
        print(f"pan called with tx: {tx}, ty: {ty}")
        print(f"Affine matrix before pan: {self.__affine_matrix}")
        # 平行移動用行列の取得
        self.__affine_matrix = affine.translateMatrix(tx, ty).dot(self.__affine_matrix)
        print(f"Affine matrix after pan: {self.__affine_matrix}")
        self.redraw_image()

    def destroyWindow(self):
        '''Delete Window
        '''
        cv2.destroyWindow(self.__winname)

    def resizeWindow(self, width : int, height : int):
        '''Sets the window size.

        Parameters
        ----------
        width : int
            Window Width
        height : int
            Window Height
        '''
        cv2.resizeWindow(self.__winname, width, height)

    def _callback_handler(self, func, *args):
        return func(*args)
    
    def set_mouse_callback(self, callback_func):
        '''Registers a callback function for mouse operations.

        Parameters
        ----------
        callback_func : 
            callback function
        '''
        self.__mouse_callback_func = callback_func

    def image_to_window_point(self, img_x : float, img_y : float):
        '''Converts image coordinates to window coordinates.

        Parameters
        ----------
        img_x : float
            X coordinate of image
        img_y : float
            Y coordinate of image

        Returns
        -------
        (win_x : float, win_y : float)
        win_x : float
            X coordinate of window
        win_y : float
            Y coordinate of window
        '''
        point = affine.afiinePoint(self.__affine_matrix , img_x, img_y)
        return point[0], point[1]

    def window_to_image_point(self, w_x, w_y):
        '''Converts window coordinates to image coordinates.

        Parameters
        ----------
        w_x : float
            X coordinate of window
        w_y : float
            Y coordinate of window

        Returns
        -------
        (img_x : float, img_y : float)
        img_x : float
            X coordinate of image
        img_y : float
            Y coordinate of image
        '''
        invMat = affine.inverse(self.__affine_matrix)
        point = affine.afiinePoint(invMat , w_x, w_y)
        return point[0], point[1]

    def _onMouse(self, event, x, y, flags, params):
        '''マウスのコールバック関数

        Parameters
        ----------
        event : int
            押されたマウスボタンの種類
        x : int
            マウスポインタの画像上のX座標
        y : int
            マウスポインタの画像上のY座標
        flags : int
            Shift, Ctrl, Altキーの押された種類
        params : 
            コールバック関数登録時に渡された値
        '''
        # 添加详细的事件调试信息，确保函数被调用和self正确绑定
        print(f"📌 _onMouse CALLED - event: {event}, x: {x}, y: {y}, flags: {flags}, params: {params}")
        print(f"  Self reference: {self}")
        
        # 确保所有必要的属性都已初始化
        if not hasattr(self, '_CvZoomWindow__mouse_down_flag'):
            print("  ⚠️ WARNING: __mouse_down_flag not found, initializing...")
            self.__mouse_down_flag = False
        
        if not hasattr(self, '_CvZoomWindow__old_point_x'):
            print("  ⚠️ WARNING: __old_point_x not found, initializing...")
            self.__old_point_x = 0
            self.__old_point_y = 0
            
        if not hasattr(self, '_CvZoomWindow__old_affine_matrix'):
            print("  ⚠️ WARNING: __old_affine_matrix not found, initializing...")
            self.__old_affine_matrix = affine.identityMatrix()
            
        if not hasattr(self, '_CvZoomWindow__affine_matrix'):
            print("  ⚠️ WARNING: __affine_matrix not found, initializing...")
            self.__affine_matrix = affine.identityMatrix()
        
        # 事件类型翻译
        event_names = {
            cv2.EVENT_MOUSEMOVE: "EVENT_MOUSEMOVE",
            cv2.EVENT_LBUTTONDOWN: "EVENT_LBUTTONDOWN",
            cv2.EVENT_LBUTTONUP: "EVENT_LBUTTONUP",
            cv2.EVENT_RBUTTONDOWN: "EVENT_RBUTTONDOWN",
            cv2.EVENT_RBUTTONUP: "EVENT_RBUTTONUP",
            cv2.EVENT_MBUTTONDOWN: "EVENT_MBUTTONDOWN",
            cv2.EVENT_MBUTTONUP: "EVENT_MBUTTONUP",
            cv2.EVENT_LBUTTONDBLCLK: "EVENT_LBUTTONDBLCLK",
            cv2.EVENT_RBUTTONDBLCLK: "EVENT_RBUTTONDBLCLK",
            cv2.EVENT_MBUTTONDBLCLK: "EVENT_MBUTTONDBLCLK",
            cv2.EVENT_MOUSEWHEEL: "EVENT_MOUSEWHEEL",
            cv2.EVENT_MOUSEHWHEEL: "EVENT_MOUSEHWHEEL"
        }
        event_name = event_names.get(event, f"UNKNOWN({event})")
        print(f"  🎯 Event type: {event_name}")
        
        # 检查self.__disp_image状态和鼠标按下标志
        print(f"  📊 self.__disp_image is None: {self.__disp_image is None}")
        print(f"  📊 self.__mouse_event_enabled: {self.__mouse_event_enabled}")
        print(f"  📊 self.__mouse_down_flag: {self.__mouse_down_flag}")
        print(f"  📊 self.__old_point_x, self.__old_point_y: {self.__old_point_x}, {self.__old_point_y}")
        
        # 移除这个条件，确保即使没有显示图像也能处理鼠标事件
        # if self.__disp_image is None:
        #     return

        print(f"  🔄 Processing mouse event...")
        print(f"[{x}, {y}] event = {event} flags = {flags} params = {params}")

        if self.__mouse_callback_func is not None:
            invMat = affine.inverse(self.__affine_matrix)
            point = affine.afiinePoint(invMat , x, y)
            self._callback_handler(self.__mouse_callback_func, self, event, x, y, flags, params, point[0], point[1], self.affine_matrix[0,0])        

        if self.__mouse_event_enabled is False:
            # マウスイベントが無効の場合
            return

        if event == cv2.EVENT_LBUTTONDOWN:
            # マウスの左ボタンが押されたとき
            print(f"EVENT_LBUTTONDOWN detected at ({x}, {y})")
            self.__mouse_down_flag = True
            print(f"  Set __mouse_down_flag = {self.__mouse_down_flag}")
            # 保存当前矩阵状态
            self.__old_affine_matrix = affine.identityMatrix()
            self.__old_affine_matrix[:] = self.__affine_matrix  # 深拷贝矩阵
            print(f"  Saved __affine_matrix to __old_affine_matrix")
            # 设置初始拖动点 - 使用私有属性
            self.__old_point_x = x
            self.__old_point_y = y
            print(f"  Set __old_point to ({self.__old_point_x}, {self.__old_point_y})")

        elif event == cv2.EVENT_LBUTTONUP:
            # マウスの左ボタンが離されたとき
            print(f"EVENT_LBUTTONUP detected at ({x}, {y})")
            self.__mouse_down_flag = False
            print(f"  Set __mouse_down_flag = {self.__mouse_down_flag}")
            
        elif event == cv2.EVENT_RBUTTONDOWN:
            # 右键按下时，只记录位置，不立即创建旋转中心
            print(f"EVENT_RBUTTONDOWN detected at ({x}, {y}) - 记录右键按下位置")
            self.__right_button_down_pos = (x, y)
            print(f"  右键按下位置已记录: ({self.__right_button_down_pos[0]}, {self.__right_button_down_pos[1]})")
            
        elif event == cv2.EVENT_RBUTTONUP:
            # 右键释放时创建旋转中心（如果位置没有大幅移动）
            print(f"EVENT_RBUTTONUP detected at ({x}, {y}) - 创建旋转中心")
            # 检查是否是点击而不是拖动（位置变化很小）
            dx = x - self.__right_button_down_pos[0]
            dy = y - self.__right_button_down_pos[1]
            if dx*dx + dy*dy < 10:  # 距离小于3px认为是点击
                # 创建新的旋转中心
                self.__rotation_center_x = x
                self.__rotation_center_y = y
                self.__rotation_center_set = True
                print(f"  创建新的旋转中心: ({self.__rotation_center_x}, {self.__rotation_center_y})")
                self.redraw_image()
            # 无论如何都重置旋转状态
            if hasattr(self, '_CvZoomWindow__old_rotation_angle_for_drag'):
                delattr(self, '_CvZoomWindow__old_rotation_angle_for_drag')
            print(f"  已重置旋转状态")
            
        elif event == cv2.EVENT_MBUTTONDOWN:
            # 中键点击取消旋转并清除标记
            print(f"EVENT_MBUTTONDOWN detected at ({x}, {y}) - 取消旋转")
            self.__rotation_center_set = False
            self.__rotation_in_progress = False
            print(f"  已取消旋转，清除旋转中心标记")
            self.redraw_image()

        elif event == cv2.EVENT_MOUSEMOVE:
            # マウスが動いているとき
            print(f"EVENT_MOUSEMOVE detected at ({x}, {y}), down_flag: {self.__mouse_down_flag}")
            # 始终更新当前鼠标位置，用于滚轮缩放的中心点
            self.__current_mouse_x = x
            self.__current_mouse_y = y
            print(f"  🎯 Updated current mouse position to ({x}, {y}) - 用于滚轮缩放中心")
            
            # 检查是否是右键拖动并且已设置旋转中心
            is_right_button_down = flags & cv2.EVENT_FLAG_RBUTTON
            if is_right_button_down and self.__rotation_center_set:
                print("  🔄 右键拖动 - 执行旋转操作")
                # 计算当前旋转角度
                dx = x - self.__rotation_center_x
                dy = y - self.__rotation_center_y
                current_angle = math.degrees(math.atan2(dy, dx))
                
                # 应用旋转变换
                try:
                    # 如果是第一次旋转，初始化旧角度
                    if not hasattr(self, '_CvZoomWindow__old_rotation_angle_for_drag'):
                        self.__old_rotation_angle_for_drag = current_angle
                        return
                    
                    # 计算旋转角度差
                    angle_diff = current_angle - self.__old_rotation_angle_for_drag
                    
                    # 处理角度环绕问题
                    if angle_diff > 180:
                        angle_diff -= 360
                    elif angle_diff < -180:
                        angle_diff += 360
                    
                    # 限制单次旋转角度，使旋转更平滑
                    max_angle_step = 5.0  # 单次最大旋转角度
                    if abs(angle_diff) > max_angle_step:
                        angle_diff = max_angle_step * (1 if angle_diff > 0 else -1)
                    
                    # 应用旋转变换
                    self.__affine_matrix = affine.rotateAtMatrix(angle_diff, self.__rotation_center_x, self.__rotation_center_y).dot(self.__affine_matrix)
                    print(f"  🔄 Applied rotation matrix, angle_diff={angle_diff:.2f} degrees")
                    
                    # 更新旧角度
                    self.__old_rotation_angle_for_drag = current_angle
                    
                    # 重绘图像
                    print("  🖼️ Calling redraw_image() after rotation")
                    self.redraw_image()
                    print("  ✅ Image redrawn successfully")
                except Exception as e:
                    print(f"  ❌ Error during rotation: {e}")
            elif self.__mouse_down_flag is True:
                print("  🚀 Mouse is dragging - processing pan")
                
                # 确保必要的属性已初始化
                if not hasattr(self, '_CvZoomWindow__old_point_x'):
                    print("  ⚠️ __old_point_x not found, initializing")
                    self.__old_point_x = x
                    self.__old_point_y = y
                    return
                    
                # 计算移动增量
                dx = x - self.__old_point_x
                dy = y - self.__old_point_y
                print(f"  📏 Calculated delta: dx={dx}, dy={dy}")
                
                # 确保仿射矩阵已初始化
                if not hasattr(self, '_CvZoomWindow__affine_matrix'):
                    print("  ⚠️ __affine_matrix not found, initializing")
                    self.__affine_matrix = affine.identityMatrix()
                
                # 应用平移变换
                try:
                    self.__affine_matrix = affine.translateMatrix(dx, dy).dot(self.__affine_matrix)
                    print(f"  🔄 Applied translation matrix, dx={dx}, dy={dy}")
                    
                    # 如果设置了旋转中心，让它也跟随平移
                    if self.__rotation_center_set:
                        self.__rotation_center_x += dx
                        self.__rotation_center_y += dy
                        print(f"  🔄 Updated rotation center: ({self.__rotation_center_x}, {self.__rotation_center_y})")
                    
                    # 更新当前位置
                    self.__old_point_x = x
                    self.__old_point_y = y
                    print(f"  🎯 Updated __old_point to ({self.__old_point_x}, {self.__old_point_y})")
                    
                    # 重绘图像
                    print("  🖼️ Calling redraw_image() after pan")
                    self.redraw_image()
                    print("  ✅ Image redrawn successfully")
                except Exception as e:
                    print(f"  ❌ Error during pan: {e}")
            else:
                print("  🚫 Mouse is not dragging - skipping pan")

        elif event == cv2.EVENT_MOUSEWHEEL:
            # 使用保存的当前鼠标位置作为缩放中心，而不是事件中的x,y参数
            zoom_x = self.__current_mouse_x
            zoom_y = self.__current_mouse_y
            print(f"EVENT_MOUSEWHEEL detected - 滚轮方向参数y: {y}, flags: {flags}")
            print(f"  🎯 使用当前鼠标位置作为缩放中心: ({zoom_x}, {zoom_y})")
            
            # ホイール回転方向による倍率変更 - 使用y参数判断方向
            if y > 0:
                scale_factor = self.__zoom_delta
                print(f"  🔼 Wheel UP detected, scale factor: {scale_factor}")
                print(f"  Calling zoom_at({scale_factor}, {zoom_x}, {zoom_y}) - 以鼠标位置为中心缩放")
                self.zoom_at(scale_factor, zoom_x, zoom_y)  # 以保存的鼠标位置为中心缩放
                print(f"  Zoom IN completed - 已在鼠标位置进行放大")
            else:
                scale_factor = 1 / self.__zoom_delta
                print(f"  🔽 Wheel DOWN detected, scale factor: {scale_factor}")
                print(f"  Calling zoom_at({scale_factor}, {zoom_x}, {zoom_y}) - 以鼠标位置为中心缩放")
                self.zoom_at(scale_factor, zoom_x, zoom_y)  # 以保存的鼠标位置为中心缩放
                print(f"  Zoom OUT completed - 已在鼠标位置进行缩小")

        elif event == cv2.EVENT_LBUTTONDBLCLK:
            # 左ボタンをダブルクリックしたとき、画像全体を表示(zoom_fit)
            self.zoom_fit()

        elif event == cv2.EVENT_RBUTTONDBLCLK:
            # マウスの右ボタンがダブルクリックされたとき、等倍表示にする
            self.__affine_matrix = affine.scaleAtMatrix(1/self.__affine_matrix[0, 0], x, y).dot(self.__affine_matrix)
            self.redraw_image()

    def _image_disp_rect(self):
        '''画像を表示している領域を取得する

        Returns
        -------
        _type_
            _description_
        '''

        if self.__src_image is None:
            return False, 0, 0, 0, 0

        # ウィンドウの座標 -> 画像の座標のアフィン変換行列
        invMat = affine.inverse(self.__affine_matrix)

        # 画像の端のウィンドウ上の座標
        # 左上側
        image_top_left_win = affine.afiinePoint(self.__affine_matrix, -0.5, -0.5)
        # 右下側
        image_width = self.__src_image.shape[1]
        image_height = self.__src_image.shape[0]
        image_bottom_right_win = affine.afiinePoint(self.__affine_matrix, image_width-0.5, image_height-0.5)    

        # ウィンドウの端の画像上の座標
        # 画像表示領域のサイズ
        try:
            _, _, win_width, win_height = cv2.getWindowImageRect(self.__winname)
        except:
            print('_image_disp_rect error')
            return

        # 左上側
        win_top_left_img = affine.afiinePoint(invMat, -0.5, -0.5)
        # 右下側
        win_bottom_right_img = affine.afiinePoint(invMat, win_width-0.5, win_height-0.5)

        # 画像のはみ出し確認
        # 左側
        if image_top_left_win[0] < 0:
            # 画像の左側がウィンドウの外にはみ出している
            #print("画像の左側がウィンドウの外にはみ出している")

            # ウィンドウの左上の座標の画像上の座標を計算
            #point = affine.afiinePoint(invMat, 0, 0)
            image_left = invMat[0, 2]
            image_left = math.floor(image_left + 0.5) - 0.5

        else:
            # 画像の左側がウィンドウの外にはみ出していない
            #print("画像の左側がウィンドウの外にはみ出していない")
            image_left = -0.5

         # 上側
        if image_top_left_win[1] < 0:
            # 画像の上側がウィンドウの外にはみ出している
            #print("画像の上側がウィンドウの外にはみ出している")

            # ウィンドウの左上の座標の画像上の座標を計算
            #point = affine.afiinePoint(invMat, 0, 0)
            image_top = invMat[1, 2]
            image_top = math.floor(image_top + 0.5) - 0.5
            
        else:
            # 画像の上側がウィンドウの外にはみ出していない
            #print("画像の上側がウィンドウの外にはみ出していない")
            image_top = -0.5

         # 右側
        if image_bottom_right_win[0] > win_width-1:
            # 画像の右側がウィンドウの外にはみ出している
            #print("画像の右側がウィンドウの外にはみ出している")
            # ウィンドウの右下の座標の画像上の座標を計算
            #point = affine.afiinePoint(invMat, win_width-1, win_height-1)
            image_right = invMat[0, 0] * (win_width-1) + invMat[0, 2]
            image_right = math.floor(image_right + 0.5) + 0.5
            pass
        else:
            # 画像の右側がウィンドウの外にはみ出していない
            #print("画像の右側がウィンドウの外にはみ出していない")
            image_right = image_width - 0.5
            pass

         # 下側
        if image_bottom_right_win[1] > win_height-1:
            # 画像の下側がウィンドウの外にはみ出している
            #print("画像の下側がウィンドウの外にはみ出している")
            image_bottom = invMat[1, 1] * (win_height-1) + invMat[1, 2]
            image_bottom = math.floor(image_bottom + 0.5) + 0.5
        else:
            # 画像の下側がウィンドウの外にはみ出していない
            #print("画像の下側がウィンドウの外にはみ出していない")
            image_bottom = image_height - 0.5

        return True, image_left, image_top, image_right, image_bottom

    def _draw_grid_line(self):

        # グリッドの線の表示領域の画像の範囲を計算する
        ret, x0, y0, x1, y1 = self._image_disp_rect()

        if ret is False:
            return

        # 画像の座標-> ウィンドウ座標のアフィン変換行列
        m = self.__affine_matrix

        # 縦線
        py0 = m[1, 1] * y0+ m[1, 2]
        py1 = m[1, 1] * y1+ m[1, 2]
        py0 = math.floor(py0+0.5)
        py1 = math.floor(py1+0.5)
        for x in range(int(x0+0.5), int(x1+0.5)):
            px = m[0, 0] * (x-0.5)+ m[0, 2]
            cv2.line(
                self.__disp_image, 
                (math.floor(px+0.5), py0), 
                (math.floor(px+0.5), py1), 
                self.__grid_color, 
                1)

        # 横線
        px0 = m[0, 0] * x0+ m[0, 2]
        px1 = m[0, 0] * x1+ m[0, 2]
        px0 = math.floor(px0+0.5)
        px1 = math.floor(px1+0.5)
        for y in range(int(y0+0.5), int(y1+0.5)):
            py = m[1, 1] * (y-0.5)+ m[1, 2]
            cv2.line(
                self.__disp_image, 
                (px0, math.floor(py+0.5)), 
                (px1, math.floor(py+0.5)), 
                self.__grid_color, 
                1)

    def _draw_bright_value(self):

        # 輝度値の表示領域の画像の範囲を計算する
        ret, x0, y0, x1, y1 = self._image_disp_rect()

        if ret is False:
            return

        # 画像の座標-> ウィンドウ座標のアフィン変換行列
        m = self.__affine_matrix

        py0 = m[1, 1] * y0+ m[1, 2]
        py1 = m[1, 1] * y1+ m[1, 2]
        py0 = math.floor(py0+0.5)
        py1 = math.floor(py1+0.5)

        px0 = m[0, 0] * x0+ m[0, 2]
        px1 = m[0, 0] * x1+ m[0, 2]
        px0 = math.floor(px0+0.5)
        px1 = math.floor(px1+0.5)

        offset_x = int(m[0, 0] / 90)
        offset_y = int(m[0, 0] / 6)

        offset_r = int(m[0, 0] / 1.58)
        offset_g = int(m[0, 0] / 1.24)
        offset_b = int(m[0, 0] / 1.03)

        fore_r = (0, 0, 200)
        fore_g = (0, 200, 0)
        fore_b = (200, 0, 0)

        if self.__affine_matrix[0, 0] > 100:
            thick = 2
        else:
            thick = 1


        if self.__disp_image.ndim == 3:
            # カラーのとき
            for y in range(int(y0+0.5), int(y1+0.5)):
                for x in range(int(x0+0.5), int(x1+0.5)):
                    px = m[0, 0] * (x-0.5)+ m[0, 2]
                    py = m[1, 1] * (y-0.5)+ m[1, 2]

                    bright = self.__src_image[y, x, :]

                    if bright.max() > 127:
                        fore_color = (0, 0, 0)
                    else:
                        fore_color = (255, 255, 255)

                    # 座標
                    cv2.putText(
                        self.__disp_image,
                        text=f"({x},{y})",
                        org=(math.floor(px+0.5) + offset_x, math.floor(py+0.5) + offset_y),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,#cv2.FONT_HERSHEY_DUPLEX, #cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=m[0, 0] / 200,
                        color=fore_color,
                        thickness = thick)

                    # B
                    cv2.putText(
                        self.__disp_image,
                        text=f"{str(bright[0]).rjust(11)}",
                        org=(math.floor(px+0.5) + offset_x, math.floor(py+0.5) + offset_b),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,#cv2.FONT_HERSHEY_DUPLEX, #cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=m[0, 0] / 200,
                        color=fore_b,
                        thickness = thick)

                    # G
                    cv2.putText(
                        self.__disp_image,
                        text=f"{str(bright[1]).rjust(11)}",
                        org=(math.floor(px+0.5) + offset_x, math.floor(py+0.5) + offset_g),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,#cv2.FONT_HERSHEY_DUPLEX, #cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=m[0, 0] / 200,
                        color=fore_g,
                        thickness = thick)

                    # R
                    cv2.putText(
                        self.__disp_image,
                        text=f"{str(bright[2]).rjust(11)}",
                        org=(math.floor(px+0.5) + offset_x, math.floor(py+0.5) + offset_r),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,#cv2.FONT_HERSHEY_DUPLEX, #cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=m[0, 0] / 200,
                        color=fore_r,
                        thickness = thick)

        else:
            # モノクロのとき
            for y in range(int(y0+0.5), int(y1+0.5)):
                for x in range(int(x0+0.5), int(x1+0.5)):
                    px = m[0, 0] * (x-0.5)+ m[0, 2]
                    py = m[1, 1] * (y-0.5)+ m[1, 2]

                    bright = self.__src_image[y, x]

                    if bright > 127:
                        fore_color = (0, 0, 0)
                    else:
                        fore_color = (255, 255, 255)

                    # 座標
                    cv2.putText(
                        self.__disp_image,
                        text=f"({x},{y})",
                        org=(math.floor(px+0.5) + offset_x, math.floor(py+0.5) + offset_y),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,#cv2.FONT_HERSHEY_DUPLEX, #cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=m[0, 0] / 200,
                        color=fore_color,
                        thickness = thick)

                    # 輝度値
                    cv2.putText(
                        self.__disp_image,
                        text=f"{str(bright).rjust(11)}",
                        org=(math.floor(px+0.5) + offset_x, math.floor(py+0.5) + offset_b),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,#cv2.FONT_HERSHEY_DUPLEX, #cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=m[0, 0] / 200,
                        color=fore_color,
                        thickness = thick)