from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QStyle, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage, QAction
from ui.Ui_twr import Ui_TWR_Form
import numpy as np
import cv2
import copy, re


from twr_utils import FeatureExtractionThread, DefectDtectionThread, SaveAction



# 主线程
class MyWindow(QWidget, Ui_TWR_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.temp_imgs = None
        self.N_s = 400
        self.temp_rois = None

        # 全局变量，用于存储用户选择的截取区域
        self.selected_roi = None
        self.started_roi = (-1, -1)
        self.selecting_roi = False

        # self.npy_save = './data/npy/temp_roi_1.npy'  # 温度数据二进制文件保存路径

        self.time_lag = None
        self.phase_diff = None

        # self.img_save_path = './data/img/'

        self.initUI()

        self.blind()

    def initUI(self):
        # 初始设置按钮为不可点击
        self.pushButton_drawROI.setEnabled(False)
        self.pushButton_featureExtract.setEnabled(False)
        self.pushButton_detect.setEnabled(False)


        # self.pushButton_drawROI鼠标悬停显示文字
        self.pushButton_drawROI.setToolTip("按回车键确认ROI区域")

        self.oriSave = SaveAction(self.label_ori, self) # 创建自定义QAction
        self.oriSave.setIconWithStyle(self.style()) # 设置图标
        self.label_ori.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu) # 设置右键菜单
        self.label_ori.addAction(self.oriSave) # 添加Action

        self.lagSave = SaveAction(self.label_lag, self)
        self.lagSave.setIconWithStyle(self.style())
        self.label_lag.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.label_lag.addAction(self.lagSave)

        self.phaSave = SaveAction(self.label_pha, self)
        self.phaSave.setIconWithStyle(self.style())
        self.label_pha.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.label_pha.addAction(self.phaSave)

        self.detectSave = SaveAction(self.label_detect, self)
        self.detectSave.setIconWithStyle(self.style())
        self.label_detect.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.label_detect.addAction(self.detectSave)

        self.plainTextEdit_logs.setReadOnly(True)
        self.saveLogs = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveAllButton), '导出日志')
        self.plainTextEdit_logs.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.plainTextEdit_logs.addAction(self.saveLogs)

    def blind(self):
        self.toolButton_loadFile.clicked.connect(self.loadFile)
        self.pushButton_showPic.clicked.connect(self.showPic)
        self.pushButton_drawROI.clicked.connect(self.drawROI)
        self.pushButton_featureExtract.clicked.connect(self.startFeatureExtraction)
        self.pushButton_detect.clicked.connect(self.startDefectDetection)
        self.oriSave.triggered_with_label.connect(self.qlabelSave)
        self.lagSave.triggered_with_label.connect(self.qlabelSave)
        self.phaSave.triggered_with_label.connect(self.qlabelSave)
        self.detectSave.triggered_with_label.connect(self.qlabelSave)
        self.saveLogs.triggered.connect(self.saveLogsToFile)


    def loadFile(self):
        print('loadFile')
        self.plainTextEdit_logs.appendPlainText("Data file loading ...")
        filePath, _ = QFileDialog.getOpenFileName(self, '加载温度数据', './data/', 'All Files(*);;Binary Files(*.dat *.npy);;Text Files(*.txt)')
        if filePath:
            self.lineEdit_fileName.setText(filePath)
            match = re.search(r"n(\d+)", filePath)
            if match:
                self.N_s = int(match.group(1)) # 要截取的帧
            else:
                print("无法提取变量值")
            try:
                # 读取.dat文件
                data = np.fromfile(filePath, dtype='>f8') # float64大端读取
                num_frames = int(data.shape[0] / (512 * 640))
                data = data.reshape((num_frames, 512, 640))
                self.temp_imgs = data[0:self.N_s, :, :]
                self.plainTextEdit_logs.appendPlainText(f"Data loaded successfully, showing image...")
                scaled_pixmap = self.scaled_pixmap(self.temp_imgs[int(self.N_s/2)])
                self.label_ori.setPixmap(scaled_pixmap)
                self.pushButton_drawROI.setEnabled(True)
                self.plainTextEdit_logs.appendPlainText(f"Image shape: {self.temp_imgs.shape}, totalframes N_s: {self.N_s}")
            except Exception as e:
                print(f"Error loading data: {e}")
                self.plainTextEdit_logs.appendPlainText(f"Error loading data!!!")
                QMessageBox.warning(self, 'Warning', '请选择正确的文件！')
        

    # 数组线性映射为图像
    def process_frame(self, frame_array:np):
        # 将数据映射到灰度值范围（0, 255）
        min_temp = np.min(frame_array)
        max_temp = np.max(frame_array)
        # 添加额外的检查，确保分母不为零
        if (max_temp - min_temp) != 0:
            normalized_data = ((frame_array - min_temp) / (max_temp - min_temp) * 255).astype(np.uint8)
        else:
        # 处理分母为零的情况，例如设定默认值
            normalized_data = np.zeros_like(frame_array).astype(np.uint8)   
        # 创建一个INFERNO映射的图像
        image = cv2.applyColorMap(normalized_data, cv2.COLORMAP_INFERNO)

        return image

    '''
    # 保存图片8bit
    def img_save(self, frame:np, path:str):
        image = self.process_frame(frame)
        # 保存图片为.png格式
        output_image_path = f'{path}.png'
        cv2.imwrite(output_image_path, image)
        print("保存成功")
    '''
    

    # ndarray转QPixmap
    def ndarray_to_qpixmap(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # cv2读取的图片是BGR格式，转换为RGB格式
        height, width, channels = image.shape
        bytesPerLine = 3 * width
        qImage = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        qpixmap = QPixmap.fromImage(qImage)
        return qpixmap

    def scaled_pixmap(self, image:np, width=280, height=280):
        '''缩放图片到QLabel的合适尺寸'''
        image = self.process_frame(image)
        qpixmap = self.ndarray_to_qpixmap(image)
        scaled_pixmap = qpixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return scaled_pixmap


    def showPic(self):
        print('showPic')
        self.plainTextEdit_logs.appendPlainText("Showing picture...")
        filePath = self.lineEdit_fileName.text()
        if not self.temp_imgs is None: # 如果已经加载了数据
            scaled_pixmap = self.scaled_pixmap(self.temp_imgs[int(self.N_s/2)])
            self.label_ori.setPixmap(scaled_pixmap)
            self.pushButton_drawROI.setEnabled(True)
            self.plainTextEdit_logs.appendPlainText(f"Image shape: {self.temp_imgs.shape}, totalframes N_s: {self.N_s}")
        elif filePath:
            match = re.search(r"n(\d+)", filePath)
            if match:
                self.N_s = int(match.group(1)) # 要截取的帧数
            else:
                print("无法提取变量值")
            
            try:
                # 读取.dat文件
                data = np.fromfile(filePath, dtype='>f8') # float64大端读取
                num_frames = int(data.shape[0] / (512 * 640))
                data = data.reshape((num_frames, 512, 640))
                self.temp_imgs = data[0:self.N_s, :, :]
                self.plainTextEdit_logs.appendPlainText(f"Data loaded successfully, showing image...")
                scaled_pixmap = self.scaled_pixmap(self.temp_imgs[int(self.N_s/2)])
                self.label_ori.setPixmap(scaled_pixmap)
                self.pushButton_drawROI.setEnabled(True)
                self.plainTextEdit_logs.appendPlainText(f"Image shape: {self.temp_imgs.shape}, totalframes N_s: {self.N_s}")
            except Exception as e:
                print(f"Error loading data: {e}")
                self.plainTextEdit_logs.appendPlainText(f"Error loading data!!!")
                QMessageBox.warning(self, 'Warning', '请输入正确的文件名！')
        else:
            print('No file selected')
            self.plainTextEdit_logs.appendPlainText("No file selected!")
            QMessageBox.warning(self, 'Warning', '请先选择文件！')


    def drawROI(self):
        print('drawROI')
        self.plainTextEdit_logs.appendPlainText("Draw an ROI on the picture...")
        # self.plainTextEdit_logs.appendPlainText("(Press Enter to Confirm, ESC to Cancel)")
        # 截取ROI区域回调函数
        def mouse_callback(event, x, y, flags, param):
            # global self.selected_roi, self.selecting_roi, self.started_roi
            # 当鼠标按下左键时记录起始坐标
            if event == cv2.EVENT_LBUTTONDOWN:
                self.started_roi = (x, y)
                self.selecting_roi = True
            # 当鼠标移动时更新终止坐标
            elif event == cv2.EVENT_MOUSEMOVE:
                if self.selecting_roi:
                    img_copy = copy.deepcopy(image) # 深拷贝：拷贝到新变量
                    width = abs(x - self.started_roi[0])
                    height = abs(y - self.started_roi[1])
                    resolution_text = f'Resolution: {width}x{height}'
                    cv2.rectangle(img_copy, self.started_roi, (x, y), (255, 255, 255), 2)
                    cv2.putText(img_copy, resolution_text, (self.started_roi[0], self.started_roi[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.imshow('cropping', img_copy)
            # 当鼠标松开左键时绘制ROI矩形
            elif event == cv2.EVENT_LBUTTONUP:
                self.selecting_roi = False
                self.selected_roi = (self.started_roi[0], self.started_roi[1], x, y)
                
                width = abs(x - self.started_roi[0])
                height = abs(y - self.started_roi[1])
                resolution_text = f'Resolution: {width}x{height}'
                img_copy = copy.deepcopy(image)
                cv2.rectangle(img_copy, self.started_roi, (x, y), (255, 255, 255), 2)
                cv2.putText(img_copy, resolution_text, (self.started_roi[0], self.started_roi[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.imshow('cropping', img_copy)

        image = self.process_frame(self.temp_imgs[int(self.N_s/2)]) # 第n/2张IR图片
        # 创建窗口并设置鼠标回调
        cv2.namedWindow('cropping')
        cv2.imshow('cropping', image)
        cv2.setMouseCallback('cropping', mouse_callback)

        while True:    
            key = cv2.waitKey(1) & 0xFF
            # 检查窗口是否被关闭
            try:
                cv2.getWindowProperty('cropping', cv2.WND_PROP_AUTOSIZE)
            except Exception as e:
                print(f"Close cropping window: {e}")
                self.plainTextEdit_logs.appendPlainText("Close cropping window")
                break
            # 按下Enter键确认ROI区域
            if key == 13 and self.selected_roi is not None:
                print(self.selected_roi)
                # 截取区域的位置
                start_x, start_y, end_x, end_y = self.selected_roi
                # 切片：对第二维和第三维进行截取
                self.temp_rois = self.temp_imgs[:, start_y:end_y, start_x:end_x]
                print(self.temp_rois.shape)
                # 存储为.npy文件
                # np.save(self.npy_save, self.temp_rois)
                
                scaled_pixmap = self.scaled_pixmap(self.temp_rois[int(self.N_s/2)])
                self.label_ori.setPixmap(scaled_pixmap)
                self.pushButton_featureExtract.setEnabled(True)
                self.plainTextEdit_logs.appendPlainText(f"ROI: {self.selected_roi}, tensor shape: {self.temp_rois.shape}")
                break
            # 按下ESC键退出
            elif key == 27:
                self.plainTextEdit_logs.appendPlainText("Exit draw ROI")
                break
            
        cv2.destroyAllWindows()
        
    
    def startFeatureExtraction(self):
        # 判断self.temp_imgs.shape[0]是否为400
        if self.temp_rois.shape[0] != 400:
            self.plainTextEdit_logs.appendPlainText("Frame wrong!")
            QMessageBox.warning(self, 'Warning', '请确保帧数正确！')
            return
        self.FE_thread = FeatureExtractionThread(self.temp_rois)
        self.plainTextEdit_logs.appendPlainText("Feature extraction...")
        # 接受子线程的信号发送的ndarray
        self.FE_thread.feProgress.connect(lambda x: self.label_lag.setText(f"Progress: {x}%"))
        self.FE_thread.feProgress.connect(lambda x: self.label_pha.setText(f"Progress: {x}%"))
        self.FE_thread.feature_extracted.connect(self.showFeature)
        self.FE_thread.start()    

    def showFeature(self, time_lag, phase_diff):
        self.time_lag = time_lag
        self.phase_diff = phase_diff
        
        self.label_lag.setPixmap(self.scaled_pixmap(time_lag))
        self.label_pha.setPixmap(self.scaled_pixmap(phase_diff))
        self.pushButton_detect.setEnabled(True)

    def startDefectDetection(self):
        # 判断当前选项卡是否为tab_lag
        if self.tabWidget.currentWidget() == self.tab_lag:
            self.DD_thread = DefectDtectionThread(self.process_frame(self.time_lag))
        elif self.tabWidget.currentWidget() == self.tab_pha:
            self.DD_thread = DefectDtectionThread(self.process_frame(self.phase_diff))
        self.plainTextEdit_logs.appendPlainText("Defect detecting...")
        self.DD_thread.detProgress.connect(lambda x: self.label_detect.setText(f"Progress: {x}%"))
        self.DD_thread.detect_info.connect(self.showDefectInfo)
        self.DD_thread.defects_info.connect(self.getDefectsInfo)
        self.DD_thread.start()

    def showDefectInfo(self, msg):
        self.plainTextEdit_logs.appendPlainText(msg)

    def getDefectsInfo(self, detect_img, defect_num):
        # self.detect_img = detect_img
        # self.defect_num = defect_num
        
        qpixmap = self.ndarray_to_qpixmap(detect_img)
        scaled_pixmap = qpixmap.scaled(280, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_detect.setPixmap(scaled_pixmap)
        self.lineEdit_numDefects.setText(str(defect_num))

    
    def qlabelSave(self, label:QLabel):
        print('qlabelSave')
        save_path, _ = QFileDialog.getSaveFileName(self, '保存图片', './data/img/', '图像文件(*.jpg *.png);;All Files(*)')
        if save_path:
            # 判断当前QLabel中是否有图像
            if label.pixmap().isNull():
                print("No image to save")
                self.plainTextEdit_logs.appendPlainText("No image to save")
                return
            # 保存图像
            label.pixmap().save(save_path)
            print("保存成功")
            self.plainTextEdit_logs.appendPlainText(f"Save image to {save_path}")
        else:
            print("No file selected")
            self.plainTextEdit_logs.appendPlainText("No file selected")
            QMessageBox.warning(self, 'Warning', '请先选择保存路径！')
        
    def saveLogsToFile(self):
        # 获取日志文本
        logText = self.plainTextEdit_logs.toPlainText()
        
        # 打开文件保存对话框
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,"导出日志文件","","文本文件 (*.txt);;All Files(*)", options=options)
        
        if fileName:
            try:
                # 将日志写入文件
                with open(fileName, 'w', encoding='utf-8') as file:
                    file.write(logText)
                QMessageBox.information(self, "导出成功", f"日志已成功导出。")
                self.plainTextEdit_logs.appendPlainText(f"Save image to {fileName}")
            except Exception as e:
                QMessageBox.critical(self, "导出失败", f"无法导出日志。\n错误信息: {str(e)}")


if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
    