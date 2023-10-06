import cv2
import time
import datetime
import numpy as np
import openpifpaf
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects

class RealTimeStream:
    def __init__(self):
        # Initialize the network and predictor
        self.pre_trained_datset = 'shufflenetv2k30'
        self.net_cpu, _ = openpifpaf.network.Factory(checkpoint=self.pre_trained_datset, download_progress=True).factory()
        self.net = self.net_cpu.cuda()
        self.decoder = openpifpaf.decoder.factory([hn.meta for hn in self.net_cpu.head_nets])
        openpifpaf.decoder.CifCaf.force_complete = True
        self.annotation_painter = openpifpaf.show.AnnotationPainter(xy_scale=1)
        # Set Canvas show to True
        openpifpaf.show.Canvas.show = True
        # Load Predictor
        self.pre_trained_datset = 'shufflenetv2k30'
        self.predictor = openpifpaf.Predictor(checkpoint=self.pre_trained_datset)


        # Initialize RTSP stream configuration
        self.username = 'smartcam'
        self.password = 'ceebridge'
        self.endpoint = 'live'
        self.ip = '172.16.121.60'
        self.stream = cv2.VideoCapture(f'rtsp://{self.username}:{self.password}@{self.ip}/{self.endpoint}')
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.stream.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

        # Load UIUC banner
        self.uiuc = cv2.imread("uiuc_my_540_30.png")
        self.uiuc_h = 30
        self.uiuc_v = 720
        self.uiuc_re = cv2.cvtColor(
            cv2.resize(self.uiuc, None, fx=self.uiuc_v/np.shape(self.uiuc)[1], fy=self.uiuc_h/np.shape(self.uiuc)[0], interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2RGB)

        # Initialize plan view visualization variables
        self.bridgeplanimg = cv2.imread('bridge_plan_new.png', 1)
        self.bridgeplanimg = cv2.rotate(self.bridgeplanimg, cv2.cv2.ROTATE_90_CLOCKWISE)
        self.bridgepts = np.array([[315, 225], [315, 892], [558, 892], [558, 225]])
        self.measurepts = np.array([[206, 143], [158, 269], [490, 274], [366, 147]])
        self.h, self.status = cv2.findHomography(self.bridgepts, self.measurepts)
        self.hplan, self.wplan, _ = self.bridgeplanimg.shape

    def visualize_in_plan_view(self, frame_list):
        capture = cv2.VideoCapture('video_run_v1.avi')
        feedimg = cv2.imread('sstl_static.png', 1)
        hratio = 540*2/self.hplan
        wratio = 720*2/self.wplan
        ratio = min(hratio, wratio)

        for framenum, frame in enumerate(frame_list):
            success, feedframe = capture.read()
            bridgeplanframe = self.bridgeplanimg.copy()
            if framenum == 0:
                bridgeplanframe1 = cv2.resize(bridgeplanframe, (int(bridgeplanframe.shape[1]*ratio), int(bridgeplanframe.shape[0]*ratio)), interpolation=cv2.INTER_AREA)
                height, width, _ = bridgeplanframe1.shape
                combivid = cv2.VideoWriter('combi_pose_new.avi', 0, 3, (width, height))
            for person in frame:
                if person[0, 2] > 0 or person[1, 2] > 0:
                    if person[0, 2] == 0:
                        x, y = person[1, :2]
                    elif person[1, 2] == 0:
                        x, y = person[0, :2]
                    else:
                        x, y = np.mean(person[:, 0:2], 0)
                    p = (x, y)
                    matrix = np.linalg.inv(self.h)
                    px = (matrix[0][0] * p[0] + matrix[0][1] * p[1] + matrix[0][2]) / (
                    (matrix[2][0] * p[0] + matrix[2][1] * p[1] + matrix[2][2]))
                    py = (matrix[1][0] * p[0] + matrix[1][1] * p[1] + matrix[1][2]) / (
                    (matrix[2][0] * p[0] + matrix[2][1] * p[1] + matrix[2][2]))
                    xp, yp = (int(px), int(py))

                    cv2.circle(bridgeplanframe, (xp, yp), 10, (0, 0, 255), -1)

            bridgeplanframeres = cv2.resize(bridgeplanframe, (int(bridgeplanframe.shape[1]*ratio), int(bridgeplanframe.shape[0]*ratio)), interpolation=cv2.INTER_AREA)
            combivid.write(bridgeplanframeres)
            print(framenum)

        cv2.destroyAllWindows()
        combivid.release()

    def start(self):
        try:
            i = 0
            m = 0
            fig, ax = plt.subplots(figsize=(10, 8))
            plt.rcParams['toolbar'] = 'None'
            fig.canvas.header_visible = False
            frame_list =[]
            while True:
                start_time = time.time()
                cur_time = datetime.datetime.now()
                
                # Read frames from the RTSP stream
                ret, Images = self.stream.read()
                if ret:
                    Images = cv2.cvtColor(Images, cv2.COLOR_BGR2RGB)
                    Images = Images[:, 240:1680, :]  # Crop to 1080 x 1440
                    image = cv2.resize(Images, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
                    
                    # Perform predictions using the network
                    predictions, gt_anns, meta = self.predictor.numpy_image(image)
                    frame_pose=[]
                    for num in range(len(predictions)):
                        frame_pose.append(predictions[num].data[15:17])
                    frame_list.append(frame_pose) # for plan view visualization

                    # Overlay UIUC banner on the frame
                    img_uiuc = image.copy()
                    img_uiuc[0:self.uiuc_h, np.shape(image)[1] - self.uiuc_v:, :] = self.uiuc_re

                    # Display the frame with predictions
                    plt.imshow(img_uiuc)
                    plt.axis('off')
                    plt.tight_layout()
                    plt.ioff()
                    plt.show(block=False)
                    plt.autoscale(False)
                    
                    # Visualize predictions on the frame
                    self.annotation_painter.annotations(ax, predictions)
                    plt.ioff()
                    fig.canvas.draw_idle()
                    fig.canvas.flush_events()

                    if plt.waitforbuttonpress(timeout=0.00000001):
                        break
                    plt.cla()
                    
                    # Display the number of people detected and frame details
                    t = plt.text(8, 18, "# PEOPLE ON BRIDGE = %.i " %
                                 (len(predictions)), fontsize=12, color='orange', fontname='serif')
                    t.set_path_effects([PathEffects.withStroke(
                        linewidth=0.5, foreground='w')])
                    tfps = plt.text(150, 18, " |  Time :  %02d : %02d : %02d  |  FPS : %5.1f" %
                                    (cur_time.hour, cur_time.minute, cur_time.second, 1.0 / (time.time() - start_time),), fontsize=12, color='white', fontname='serif')
                    print("%3d, FPS : %5.2f, Pred: %3d " %
                          (i, 1.0 / (time.time() - start_time), len(predictions)))
                    i = i + 1
                    m = m + 1
                    if m > 5:
                        self.stream.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
                        m = 0
                        continue
        except Exception as e:
            print("ERROR:", e)
        
        finally:
            cv2.destroyAllWindows()
            plt.close()
            self.stream.release()
            # Example of using visualize_in_plan_view
            self.visualize_in_plan_view(frame_list)

