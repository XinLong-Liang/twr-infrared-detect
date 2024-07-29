from PySide6.QtWidgets import QStyle, QLabel
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QAction
import numpy as np
import cv2, json, time
from scipy.signal import savgol_filter, hilbert
from ultralytics import YOLOv10

# 特征提取子线程
class FeatureExtractionThread(QThread):
    # 自定义信号：用于传递2个ndarray类型的数据
    feature_extracted = Signal(np.ndarray, np.ndarray)
    feProgress = Signal(int) # 发送进度信号

    def __init__(self, temp_3d:np.ndarray, f_c=0.05, f_s=4.0):
        super().__init__()

        self.pwm_path = './data/pwm/pwm_fpm2_fc0.05_fs4.0_n400.json'

        self.temp_3d = temp_3d
        self.f_c = f_c
        self.f_s = f_s


    def run(self):
        print("Feature extracting...")
        self.feProgress.emit(10)
        try:
            with open(self.pwm_path, 'r') as f:
                pwm_data = np.array(json.load(f))
        except FileNotFoundError:
            print("PWM file not found or error reading the file.")
            return
        pwm_data = (pwm_data - np.min(pwm_data)) / (np.max(pwm_data) - np.min(pwm_data)) * 2 - 1
        # print(f'pwm_shape:{pwm_data.shape}')
        self.feProgress.emit(20)
    
        N_s, img_h, img_w = self.temp_3d.shape
    
        # 时间间隔
        time_interval = 1.0 / self.f_s
        total_time = N_s * time_interval
        # 创建时间点数组
        time_points = np.arange(0, total_time, time_interval)  
        # 将time_points拓展相同长度的负数时间点
        times = np.arange(-total_time + time_interval, total_time, time_interval) 
    
        temp_2d = self.temp_3d.reshape((N_s, img_h*img_w))

        self.feProgress.emit(40)
    
        # Savitzky-Golay滤波，按列处理
        filt_temp = savgol_filter(temp_2d, window_length=7, polyorder=2, axis=0)
        self.feProgress.emit(60)
    
        # 去趋势项，按列(默认)处理
        dtrend_temp = self.batch_trend_remove(time_points, filt_temp, 2)
        self.feProgress.emit(80)

        # 滞后时间和相位差
        time_lag, phase_diff = self.mat_lag_pha(dtrend_temp, pwm_data, times)
        time_lag = time_lag.reshape((img_h, img_w))
        phase_diff = phase_diff.reshape((img_h, img_w))

        self.feProgress.emit(100)
        # 特征提取完成后，可以发出信号（如果需要）
        self.feature_extracted.emit(time_lag, phase_diff)
    
    
    # 多项式拟合(最小二乘)去除趋势项, 并归一化成-1到1
    def batch_trend_remove(self, t, sig, degree): # degree为拟合阶数
        num_curves = sig.shape[1]  # 获取曲线的数量:列数
        sig_res_batch = np.zeros_like(sig)  # 初始化一个与输入相同形状的数组来存储结果
    
        for i in range(num_curves):
            model = np.polyfit(t, sig[:, i], degree)  # 对每一列进行拟合
            sig_predict = np.polyval(model, t)  # 计算每一列的多项式值，即趋势项
            sig_res_batch[:, i] = sig[:, i] - sig_predict  # 减去趋势项
            # 归一化成-1到1
            sig_res_batch[:, i] = (sig_res_batch[:, i] - np.min(sig_res_batch[:, i])) / (np.max(sig_res_batch[:, i]) - np.min(sig_res_batch[:, i])) * 2 - 1
    
        return sig_res_batch
    
    def process_hilbert(self, sig:np):
        # 对原始信号进行 Hilbert Transform
        analytic_signal = hilbert(sig)
        # 计算 Hilbert Transform 后的相位
        phase = np.angle(analytic_signal)
        # 将相位推迟 90 度
        phase_delayed = phase - np.pi / 2
        # 根据相位和幅值计算修正后的信号
        corrected_signal = np.abs(analytic_signal) * np.exp(1j * phase_delayed)
        # 修正后的信号
        sig_hil = np.real(corrected_signal)
        return sig_hil

    # 计算互相关的滞后时间和相位差函数
    def cal_lag_pha(self, sig_res:np, sig_ori:np, times:np):
        # 计算同相相关和正交相关
        inpha_corr = np.correlate(sig_res, sig_ori, mode='full') # 同相相关
        sig_hil = self.process_hilbert(sig_ori) # Hilbert变换：将原信号所有频率分量相位推迟90度
        quadr_corr = np.correlate(sig_res, sig_hil, mode='full') # 正交相关

        # 计算滞后时间：同相相关取最大值处的时间点索引
        max_idx = np.argmax(inpha_corr)
        time_lag = round(times[max_idx], 2)
        # 计算相位差：time_points索引为0时的arctan(inpha_corr/quadr_corr)
        idx = len(sig_ori) - 1
        phase_diff = np.arctan(quadr_corr[idx] / inpha_corr[idx])
        phase_diff = round(phase_diff, 4)

        return time_lag, phase_diff

    # 计算矩阵的互相关的滞后时间和相位差
    def mat_lag_pha(self, sig_mat:np, sig_ori:np, times:np, axis:int=-1):
        num_curves = sig_mat.shape[axis]  # 获取曲线的数量
        # 储存滞后时间和相位差的数组
        time_lag = np.zeros(num_curves)
        phase_diff = np.zeros(num_curves)

        for i in range(num_curves):
            # 计算滞后时间和相位差
            time_lag[i], phase_diff[i] = self.cal_lag_pha(sig_mat[:, i], sig_ori, times)
        
        return time_lag, phase_diff


# 缺陷检测子线程
class DefectDtectionThread(QThread):
    detect_info = Signal(str) # 发送检测信息
    defects_info = Signal(np.ndarray, int) # 发送缺陷信息
    detProgress = Signal(int) # 发送进度信号

    def __init__(self, ndarray:np.ndarray):
        super().__init__()

        self.model_path = './weights/inf_imz640_ep500_bat16_10n_SCConv.pt'

        self.feature_array = ndarray


    def run(self):
        print("Defect detecting...")
        self.detProgress.emit(10)
        try:
            with open(self.model_path, 'r') as f:
                model = YOLOv10(self.model_path)
        except FileNotFoundError:
            print("Model file not found or error reading the file.")
            return
        
        self.detProgress.emit(20)
        # 记录开始时间
        start_time = time.time()

        # Perform object detection on the array
        results = model.predict(self.feature_array.astype(np.uint8), iou=0.9)

        # 记录结束时间
        end_time = time.time()

        self.detProgress.emit(60)

        # 计算运行时间
        elapsed_time = end_time - start_time

        self.detProgress.emit(80)
        

        # extract the boxes, confidences, and image from the results
        img = results[0].orig_img
        boxes = results[0].boxes.data.cpu().numpy()
        confs = results[0].boxes.conf.data.cpu().numpy()
        speed = results[0].speed
        
        time_data = f"{speed['preprocess']:.1f}ms preprocess, {speed['inference']:.1f}ms inference, {speed['postprocess']:.1f}ms postprocess"
        self.detProgress.emit(90)
        # draw the boxes and confs on the image
        img = self.drawBoxes(img, boxes, confs)
        self.detProgress.emit(100)

        # 发送信号
        self.detect_info.emit(f"Run time: {elapsed_time:.4f}s, {boxes.shape[0]} defects detected, speed: {time_data} per image at shape {img.shape}.")

        self.defects_info.emit(img, len(boxes))


    def drawBoxes(self, img:np, boxes:np, confs:np):
        for i in range(len(boxes)):
            box = boxes[i]
            conf = confs[i]

            img = cv2.rectangle(img, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 0, 255), 2)

            # 计算文本大小
            text = f'{conf:.2f}'
            (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)

            # 计算矩形左上角和右下角的坐标
            top_left = (int(box[0]), int(box[1] - text_height - 2))
            bottom_right = (int(box[0] + text_width), int(box[1]))

            # 绘制红色背景矩形
            img = cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), -1)

            # 在红色背景上绘制白色文字
            img = cv2.putText(img, text, (int(box[0]), int(box[1] - 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

        return img
        
# 自定义QAction，用于保存图像
class SaveAction(QAction):
    triggered_with_label = Signal(QLabel)  # 自定义信号，传递QLabel
    
    def __init__(self, label, parent=None):
        super().__init__(parent)
        self.label = label
        # self.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        self.setText('保存图像')
        self.triggered.connect(self.emit_label)

    def emit_label(self):
        self.triggered_with_label.emit(self.label)  # 触发时发出信号，传递QLabel

    def setIconWithStyle(self, style):
        self.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))

