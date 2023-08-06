from PIL.Image import MODES
from ingradient_library.dataloads import *
import matplotlib.pyplot as plt
from tqdm import tqdm
from torchvision.transforms import CenterCrop
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import cc3d
import SimpleITK as sitk
import time
import os

def get_kernel(patch_size, sigma = 1e+3):
    kernel_shape = (patch_size[0], patch_size[1], patch_size[2])
    tmp = tuple([torch.arange(i) for i in kernel_shape])
    gx, gy, gz = torch.meshgrid(*tmp)
    gx = torch.abs(gx - kernel_shape[0]//2)
    gy = torch.abs(gy - kernel_shape[1]//2)
    gz = torch.abs(gz - kernel_shape[2]//2)
    kernel = torch.exp(-((gx**2 + gy**2 + gz**2)/(2*(sigma))))

    return kernel

def get_pad_images(images, patch_size):
    #이미지가 patch 보다 작을 경우 padding
    images = torch.tensor(images)
    if len(patch_size) == 3:
        image_shape = torch.tensor([images.shape[-3], images.shape[-2], images.shape[-1]])
    else:
        image_shape = torch.tensor([images.shape[-2], images.shape[-1]])
    prev_shape = torch.tensor(image_shape)
    patch_size = torch.tensor(patch_size)
    while len(images.shape) < 5:
        images = images.unsqueeze(0)
    
    new_shape = torch.tensor([0,0,0])
    for i in range(len(patch_size)):
        if patch_size[i] > image_shape[i]:
            new_shape[i] = (patch_size[i]) - prev_shape[i]
    is_div_two = new_shape % 2 != 0
    pad_shape = new_shape.repeat_interleave(2) // 2
    for i in range(len(is_div_two)):
        if is_div_two[i]:
            pad_shape[i*2] += 1

    images = F.pad(images, pad_shape.tolist()[::-1], "constant", 0)

    while len(images.shape) > 4:
        images = images.squeeze(0)

    return images

def get_coords_arr(images, patch_size, step_size):
    #image와 patch, step size를 통해 patch를 뽑는 위치를 grid 단위로 나타냄. 
    grid_list = []
    image_shape = torch.tensor([images.shape[-3], images.shape[-2], images.shape[-1]])
    for i in range(3):
        step = 1+(image_shape[i] - patch_size[i])/(patch_size[i] * step_size[i])
        if step < 1:
            step = 1.0
        grid_list.append(torch.arange(step))
    grid_x, grid_y, grid_z = torch.meshgrid(*grid_list)
    grid_x = torch.round(grid_x * step_size[0] * patch_size[0]).long()
    grid_y = torch.round(grid_y * step_size[1] * patch_size[1]).long()
    grid_z = torch.round(grid_z * step_size[2] * patch_size[2]).long()
    max_gx = grid_x.max()
    max_gy = grid_y.max()
    max_gz = grid_z.max()

    grid_x[torch.where(grid_x == max_gx)] = images.shape[-3] - patch_size[0]
    grid_y[torch.where(grid_y == max_gy)] = images.shape[-2] - patch_size[1]
    grid_z[torch.where(grid_z == max_gz)] = images.shape[-1] - patch_size[2]
    grid_x = grid_x.reshape(-1, 1)
    grid_y = grid_y.reshape(-1, 1)
    grid_z = grid_z.reshape(-1, 1)
    
    grids = torch.cat((grid_x, grid_y, grid_z), -1)
    patch_coords = []
    for i in range(grids.shape[0]):
        patch_coords.append((torch.arange(grids[i][0], grids[i][0]  + patch_size[0]), torch.arange(grids[i][1], grids[i][1] + patch_size[1]), torch.arange(grids[i][2], grids[i][2] + patch_size[2]) ) )
    return patch_coords


def get_patch_from_coords(image, patch_coords, index):
    #위의 함수에서 얻어진 image당 patch의 coords에서 image와 coords가 주어졌을 대 patch를 뽑아냄
    for i in range(image.shape[0]):
        if i == 0:
            patch = image[0][torch.meshgrid(*patch_coords[index])].unsqueeze(0)
        else:
            patch = torch.cat((patch, image[i][torch.meshgrid(*patch_coords[index])].unsqueeze(0)))
    return patch

def change_value_from_coords(image, patch_coords, index, patch):
    #patch의 값으로 image와 해당하는 coords 의 값을 바꿈
    for i in range(image.shape[0]):
        image[i][torch.meshgrid(*patch_coords[index])] += patch[i]
    return image
"""

class TTA(object):
    def __init__(self, flip = [0,1,2], permute = [[1,0,2]]):
        self.flip = flip
        self.permute = permute

    def transform(self, image):
        images = [image]
        transformed_log = [] # {'image':, 'flip':, 'permute': 

        if self.permute != None:
            for p in self.permute:
                permutted_img = image.permute(p[0],p[1],p[2])
                image.append(permutted_img)

        for f in self.flip:
            flipped_img = torch.flip(image, f)
            images.append(flipped_img)
            if self.permute != None:
                for p in self.permute:
                    permutted_img = flipped_img.permute(p[0],p[1],p[2])
                    image.append(permutted_img)

        return images
        
    def inverse_transform(self):

"""

class CC_Remover(object):
    # remain num => 남길 connected components label의 수
    # frequency order => connected component labeling 된 것 중 택할 빈도 수를 정함. 1은 보통 background 임.
    def __init__(self, remain_num = 2, frequency_order = [2,3], distance = True, axis_z = 2, cc_label_counts = 1500, distance_weight = 20.0):
        self.remain_num = remain_num
        self.frequency_order = frequency_order
        self.distance = distance
        self.axis_z = axis_z
        self.cc_label_counts = cc_label_counts
        self.distance_weight = distance_weight

    def __call__(self, mask):
        conected_component_mask = cc3d.connected_components(mask, connectivity = 26)
        count = np.unique(conected_component_mask, return_counts = True)[1]
        result = torch.zeros(mask.shape)

        if self.distance != False:
            component_length = (count > self.cc_label_counts).sum()
            remained_components_indices = np.argsort(count)[::-1][:component_length]
            center_coords = []
            min_max_coords = []
            for r_i in remained_components_indices:
                min_max_coords.append([np.where(conected_component_mask == r_i)[0].max() - np.where(conected_component_mask == r_i)[0].min(), np.where(conected_component_mask == r_i)[1].max() - np.where(conected_component_mask == r_i)[1].min(), np.where(conected_component_mask == r_i)[2].max()- np.where(conected_component_mask == r_i)[2].min()])
                center_coords.append([np.where(conected_component_mask == r_i)[self.axis_z].mean()])
            center_coords = np.array(center_coords)
            min_max_coords = np.array(min_max_coords)
            n_clusters = center_coords.shape[0]
            distance = np.zeros((n_clusters, n_clusters))

            for i in range(n_clusters):
                for j in range(n_clusters):
                    if i == j:
                        distance[i][j] = 1e+10
                    else:
                        distance[i][j] = self.distance_weight * numpy.linalg.norm(center_coords[i]-center_coords[j]) + numpy.linalg.norm(min_max_coords[i]-min_max_coords[j])

            x, y = np.unravel_index(np.argmin(distance, axis=None), distance.shape)
            return torch.tensor((remained_components_indices[x] == conected_component_mask) + (remained_components_indices[y] == conected_component_mask))
        else:
            for i in range(self.remain_num):
                try:
                    result += (np.argsort(count)[::-1][self.frequency_order[i]-1] == conected_component_mask)
                except IndexError as e:
                    print(e)
                
            return torch.tensor(result)

class InferenceV2(object):
    """
    dataset : torch.utils.data 의 dataset 또는 해당 class를 상속받은 개체.
    patch_size : inference 시에 적용 할 patch size를 설정
    n_classes : softmax output의 channel 수
    mode : 저장할 데이터셋 포멧 npy와 nifti만 지원 됨.
    deep_supervision : 모델에 deep_supervision이 적용 될 경우, True
    padding : patch size에 맞게 padding
    """
    def __init__(self, dataset, model, patch_size, n_classes, mode = 'npy and nifti', step_size = [0.5, 0.5, 0.5], postprocessing = None, device = None, softmax_threshold = 0.99, tta = None,
                 batch_size = 1, gaussian_filter = True, deep_supervision = False, save_path = None, arg_max = False, padding = False, is_2d = False, sigma = 1e+3):
        self.dataset = dataset
        self.model = model.to(device)
        self.bs = batch_size
        self.patch_size = patch_size
        self.step_size = step_size
        self.n_classes = n_classes
        self.deep_supervision = deep_supervision
        self.device = device
        self.postprocessing = postprocessing
        self.mode = mode
        self.save_path = save_path
        if save_path != None:
            self.make_dir(save_path)
        self.arg_max = arg_max
        self.padding = padding
        self.is_2d = is_2d
        self.softmax_threshold = softmax_threshold
        if gaussian_filter == True:
            self.gaussian_kernel = get_kernel(patch_size, sigma = sigma)
            self.gaussian_kernel = self.gaussian_kernel.to(device)
        
        self.tta = tta
        
    def valid_run(self):
        #전체 데이터에 대해 inference 시작.
        print('start valid run')
        final_score = []
        self.model = self.model.eval()
        for data_index in range(len(self.dataset)):
            if isinstance(self.dataset, CustomDataset):
                current_name = self.dataset.image_name[data_index][:-4]
            else:
                current_name = 'result'
            image = self.dataset[data_index][0]
            seg = self.dataset[data_index][1]
            if self.padding:
                seg = get_pad_images(seg, self.patch_size)
            
            if isinstance(seg, np.ndarray):
                seg = torch.from_numpy(seg)
            
            #if self.tta != None:
            #    input_list = self.tta.transform(image)
            #    output_list = []
            #    for input in input_list:
            result = self.get_result(image, data_index, current_name)

            dice_score = []
            for i in range(1, self.n_classes):
                temp_seg = (seg == i).long()
                temp_img = (result == i).long()
                intersection = (temp_seg * temp_img).sum()
                union = temp_seg.sum() + temp_img.sum()
                dice = 2 * intersection / union
                dice_score.append(dice.numpy())
            print("file_name : ", self.dataset.image_name[data_index], "dice : ", dice_score[0].item())
            final_score.append(dice_score)
        
        self.final_score = final_score
        return final_score

    def make_dir(self, save_path):
        now = time.localtime()
        now = "%04d%02d%02d_%02d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

        self.save_path = os.path.join(save_path, now)
        self.soft_path = os.path.join(self.save_path, r'soft_result')
        self.model_path = os.path.join(self.save_path, r'result')
        self.postprocessing_path = os.path.join(self.save_path, r'postprocessing_result')
        self.image_path = os.path.join(self.save_path, r'image')
        self.nii_img_path = os.path.join(self.save_path, r'nifti_image')

        try:
            os.mkdir(self.save_path)
            os.mkdir(self.soft_path)
            os.mkdir(self.image_path)
            os.mkdir(self.model_path)
            os.mkdir(self.postprocessing_path)
            os.mkdir(self.nii_img_path)
        
        except FileExistsError as e:
            print('Folders already exist. Please be careful to overwrite exising files.')

    def save(self, image, path, index, identifier, mode = 'seg', is_nifti = False):
        if 'npy' in self.mode:
            np.save(os.path.join(path, identifier + mode + '{0:03}.npy'.format(index)),image.detach().cpu().numpy())
        
        if is_nifti:
            nii_img = sitk.GetImageFromArray(image.detach().cpu().numpy())
            sitk.WriteImage(nii_img, os.path.join(self.nii_img_path, identifier + mode + '{0:03}.nii.gz'.format(index)))

    def test_run(self):
        for data_index in range(len(self.dataset)):
            if isinstance(self.dataset, CustomDataset):
                current_name = self.dataset.image_name[data_index][:-4]
            image = self.dataset[data_index][0]
            result = self.get_result(image, data_index, current_name)
            
        return result
    
    def get_result(self, image, data_index = None, current_name = None):
        # 각 이미지 별로 result를 구함.
        if self.padding:
            image = get_pad_images(image, self.patch_size)
        coords = get_coords_arr(image, self.patch_size, self.step_size)
        self.model.eval()

        for coords_index in range(len(coords)):
            if coords_index == 0:
                patch_bundle = get_patch_from_coords(image, coords, coords_index).unsqueeze(0)
                index_bundle = torch.tensor(coords_index).reshape(1,)
            else:
                patch_bundle = torch.cat((patch_bundle, get_patch_from_coords(image, coords, coords_index).unsqueeze(0)), 0)
                index_bundle = torch.cat((index_bundle, torch.tensor(coords_index).reshape(1,)))

        patch_bundle = torch.split(patch_bundle, self.bs)
        index_bundle = torch.split(index_bundle, self.bs)
        result = torch.zeros((self.n_classes, image.shape[-3], image.shape[-2], image.shape[-1]))
        for mini_batch_patch, mini_batch_index in tqdm(zip(patch_bundle, index_bundle)):
            with torch.no_grad():
                output = self.model(mini_batch_patch.to(self.device).float())
                if self.deep_supervision:
                    output = output[0]
                output = torch.softmax(output, dim = 1) * self.gaussian_kernel.unsqueeze(0).unsqueeze(0)
                output = output.detach().cpu()
                for batch_index in range(mini_batch_index.shape[0]):
                    result = change_value_from_coords(result, coords, mini_batch_index[batch_index], output[batch_index])
        
        if self.save_path != None:
            self.save(result, self.soft_path, data_index, current_name)
        
        if self.arg_max:
            result = torch.argmax(result, 0)
        else:
            result = torch.softmax(result, dim = 0)
            result[1:] = result[1:] >= self.softmax_threshold
            result = torch.argmax(result, 0)

        if self.save_path != None:
            argmax_result = torch.argmax(result, 0), 
            self.save(argmax_result, self.model_path, data_index, current_name, mode = 'seg', is_nifti = True)
            self.save(image[0], self.image_path, data_index, current_name, mode = 'image', is_nifti = True)

            if self.postprocessing != None:
                mask = self.postprocessing((argmax_result != 0).detach().cpu().numpy())
                argmax_result = mask * argmax_result
                self.save(argmax_result, self.model_path, data_index, current_name, mode = 'postprocessing', is_nifti = True)
        
        return result
    



class Inference2D(InferenceV2):
    def __init__(self, model, dataset, axis = 2, patch_size = (512, 512), save_path = None, n_classes = 2, padding = True, deepsupervision = False, softmax_threshold = 0.99):
        if isinstance(dataset, Dataset2D):
            dataset.oversampling = False
        
        self.model = model
        self.dataset = dataset
        self.axis = axis
        self.centercrop = CenterCrop(size = patch_size)
        self.save_path = save_path
        self.n_classes = n_classes
        self.padding = padding
        self.patch_size = patch_size
        self.deepsupervision = deepsupervision
        self.softmax_threshold = softmax_threshold
        if save_path != None:
            self.make_dir(save_path)
    
    def save(self, image, path, index, identifier, mode='seg', is_nifti=False):
        return super().save(image, path, index, identifier, mode=mode, is_nifti=is_nifti)
    
    def make_dir(self, save_path):
        return super().make_dir(save_path)

    def get_value_by_index(self, tensor, index):
        if self.axis == 0:
            result = tensor[:, index]
        elif self.axis == 1:
            result = tensor[:, :, index]
        elif self.axis == 2:
            result = tensor[:, :, :, index]
        return result
    
    def save_value_by_index(self, tensor, input, index):
        if self.axis == 0:
            tensor[:, index] = input
        elif self.axis == 1:
            tensor[:, :, index] = input
        elif self.axis == 2:
            tensor[:, :, :, index] = input
        return tensor

    def valid_run(self):
        return super().valid_run()
        
    def get_result(self, image, data_index, current_name):
        result = torch.zeros(image.shape)
        
        if self.axis == 0:
            axis_range = image.shape[-3]
        elif self.axis == 1:
            axis_range = image.shape[-2]
        elif self.axis == 2:
            axis_range = image.shape[-1]

        
        for i in range(axis_range):
            input_img = self.get_value_by_index(image, i) # bs, n_modality, x, y 
            while len(input_img.shape) < 4:
                input_img = input_img.unsqueeze(0)
            
            if self.deepsupervision:
                output = self.model(input_img)[0]
            else:
                output = self.model(input_img)
            result = self.save_value_by_index(result, output, i)
        

        if self.arg_max:
            result = torch.argmax(result, 0)
        else:
            result[:, 1:] = (result[:, 1:] >= self.softmax_threshold)
            result = torch.softmax(result, dim = 1)

        if self.save_path != None:
            self.save(result, self.model_path, data_index, current_name, mode = 'seg', is_nifti = True)
            self.save(image[0], self.image_path, data_index, current_name, mode = 'image', is_nifti = True)
        
        return result