import cv2
import os
import cc3d
import SimpleITK as sitk
import numpy as np
import time

class Manual_Labeling(object):
    """
    왼쪽 화면 : predicted mask
    오른쪽 화면 : grount truth
    p : 이전 파일
    n : 다음 파일
    좌클릭 : 선택할 component
    우클릭 : 삭제할 component
    r : 현재 선택 된 component
    s : 결과 저장
    """
    def __init__(self, root_dir, save_dir, gt_path = None):
        self.root_dir = root_dir
        self.save_dir = save_dir
        self.gt_path = gt_path
        self.file_list = sorted(os.listdir(root_dir))
        if gt_path != None:
            self.gt_list = sorted([f for f in os.listdir(gt_path) if 'npz' in f ])
            self.sorted_by_gt()
    
    def sorted_by_gt(self):
        temp = []
        for g in self.gt_list:
            for f in self.file_list:
                prefix_g = g.split('.')[0]
                prefix_f = f.split('s')[0]
            
                if prefix_g == prefix_f:
                    temp.append(f)
                    break
        
        self.file_list = temp
        
    def get_coordinates(self, x, y):
        if self.selected_axis == 0:
            return [self.axis_index, y, x]
        
        if self.selected_axis == 1:
            return [y, self.axis_index, x]
        
        if self.selected_axis == 2:
            return [y, x, self.axis_index]
        
    

    def mouse_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.update_result(self.get_coordinates(x, y))
        
        elif event == cv2.EVENT_RBUTTONDBLCLK:
            self.update_result(self.get_coordinates(x, y), mode = 'right')
    
        elif event == cv2.EVENT_MOUSEWHEEL:
            if flags > 0 and self.axis_index < self.image.shape[self.selected_axis]:
                self.axis_index += 1
                self.imshow_by_axis(self.image, self.axis_index, self.selected_axis, self.name)
            elif self.axis_index > 0 and flags < 0:
                self.axis_index -= 1
                self.imshow_by_axis(self.image, self.axis_index, self.selected_axis, self.name)
        
    def save(self, image, index):
        print("Start saving the file. file name : ", self.file_list[index])
        nii_img = sitk.GetImageFromArray(image)
        sitk.WriteImage(nii_img, os.path.join(self.save_dir, self.file_list[index]))
        print("File saving is complete. file name : ", self.file_list[index])
    
    def update_result(self, point, mode = 'left'):
        if mode == 'left':
            self.result += (self.cc_mask == self.cc_mask[point[0]][point[1]][point[2]])
        
        else:
            self.result[np.where(self.cc_mask == self.cc_mask[point[0]][point[1]][point[2]])] = 0
    
    def run(self, name = 'left = pred || right = gt'):
        self.name = name
        cv2.namedWindow(name)
        cv2.setMouseCallback(name, self.mouse_event)
        index = 0
        self.selected_axis = 0
        self.load_nifti_img(index)
        self.axis_index = self.image.shape[self.selected_axis] // 2

        while isinstance(self.image, np.ndarray):
            self.imshow_by_axis(self.image, self.axis_index, self.selected_axis, self.name)
            key = cv2.waitKey()
            if key == ord('n'):
                print('next image')
                index += 1
                self.load_nifti_img(index)
                self.axis_index = self.image.shape[self.selected_axis] // 2
                self.imshow_by_axis(self.image, self.axis_index, self.selected_axis, self.name)
            
            if key == ord('p'):
                if index > 0:
                    print('prev image')
                    index -= 1
                    self.load_nifti_img(index)
                    self.axis_index = self.image.shape[self.selected_axis] // 2
                    self.imshow_by_axis(self.image, self.axis_index, self.selected_axis, self.name)
            
            if key == ord('v'):
                self.selected_axis += 1
                self.selected_axis %= 3
                self.axis_index = self.image.shape[self.selected_axis] // 2
                self.imshow_by_axis(self.image, self.axis_index, self.selected_axis, self.name)
            
            if key == ord('r'):
                self.imshow_by_axis(self.result, self.axis_index, self.selected_axis, self.name)
                wait_key = cv2.waitKey(3000)#pauses for 3 seconds before fetching next image
                if wait_key == 27:#if ESC is pressed, exit loop
                    cv2.destroyAllWindows()
                    break
                elif wait_key == ord('s'):
                    self.save(self.result, index)
                    time.sleep(1)
            if key == ord('s'):
                self.save(self.result, index)
                time.sleep(1)
                


    def imshow_by_axis(self, image, axis_index, selected_axis, name):
        if selected_axis == 0:
            img_to_show = image[axis_index]
            gt = self.gt[axis_index]
        if selected_axis == 1:
            img_to_show = image[:, axis_index]
            gt = self.gt[:, axis_index]
        if selected_axis == 2:
            img_to_show = image[:, :, axis_index]
            gt = self.gt[:, :, axis_index]
        mean_val = img_to_show.mean()
        std_val = img_to_show.std()
        img_to_show = (img_to_show - mean_val) / std_val
        img_to_show = np.hstack((img_to_show, gt))
        cv2.imshow(name, img_to_show)


    def load_nifti_img(self, index):
        if index >= len(self.file_list) :
            return False
        print('predicted file name : ', self.file_list[index])
        sitk_img = sitk.ReadImage(os.path.join(self.root_dir, self.file_list[index]))
        img_arr = sitk.GetArrayFromImage(sitk_img)
        mask = (img_arr != 0)
        conected_component_mask = cc3d.connected_components(mask, connectivity = 26)
        self.result = np.zeros(conected_component_mask.shape)
        
        self.image = img_arr
        self.cc_mask = conected_component_mask
        
        if self.gt_path != None:
            print('gt file name : ', self.gt_list[index])
            self.gt = np.load(os.path.join(self.gt_path, self.gt_list[index]))
            self.gt = self.gt['y']