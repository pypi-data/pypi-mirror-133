import os
import glob

import cv2
import numpy as np
import time
import re
import h5py
import matplotlib.pyplot as plt
from functools import partial
from tqdm import tqdm
from PIL import Image
from whacc.image_tools import h5_iterative_creator
from sklearn.preprocessing import normalize
from whacc import utils, image_tools, analysis
import matplotlib.pyplot as plt
import numpy as np
import copy
from scipy.signal import medfilt


def track_h5(template_image, h5_file, match_method='cv2.TM_CCOEFF', ind_list=None):
    with h5py.File(h5_file, 'r') as h5:
        if isinstance(template_image, int):  # if termplate is an ind to the images in the h5
            template_image = h5['images'][template_image, ...]
        elif len(template_image.shape) == 2:
            template_image = np.repeat(template_image[:, :, None], 3, axis=2)

        if ind_list is None:
            ind_list = range(len(h5['labels'][:]))
        # width and height of img_stacks will be that of template (61x61)
        max_match_val = []
        try:
            method_ = eval(match_method)
        except:
            method_ = match_method
        max_match_val = []
        for frame_i in tqdm(ind_list):
            img = h5['images'][frame_i, ...]
            # Apply template Matching
            if isinstance(method_, str):
                print('NOOOOOOOOOOOOOOO')
                if method_ == 'calc_diff':
                    max_val = np.sum(np.abs(img.flatten() - template_image.flatten()))
                elif method_ == 'mse':
                    max_val = np.mean((img.flatten() - template_image.flatten()) ** 2)
            else:
                res = cv2.matchTemplate(img, template_image, method_)
                min_val, max_val, min_loc, top_left = cv2.minMaxLoc(res)
            max_match_val.append(max_val)
            # top_left = np.flip(np.asarray(top_left))
    return max_match_val, template_image


x = '/Users/phil/Downloads/test_pole_tracker/AH0667x170317.h5'
utils.print_h5_keys(x)
max_val_stack = image_tools.get_h5_key_and_concatenate(x, 'max_val_stack')
locations_x_y = image_tools.get_h5_key_and_concatenate(x, 'locations_x_y')
trial_nums_and_frame_nums = image_tools.get_h5_key_and_concatenate(x, 'trial_nums_and_frame_nums')
template_img = image_tools.get_h5_key_and_concatenate(x, 'template_img')
frame_nums = trial_nums_and_frame_nums[1, :].astype(int)
trial_nums = trial_nums_and_frame_nums[0, :].astype(int)
asdfasdfasdf
method = 'TM_CCOEFF_NORMED'
ind_list = None
max_match_val_new, template_image_out = track_h5(template_img, x, match_method='cv2.' + method, ind_list=ind_list)

method = 'calc_diff'
ind_list = None
template_img = 2000
max_match_val_new, template_image_out = track_h5(template_img, x, match_method=method, ind_list=ind_list)

method = 'mse'
ind_list = None
template_img = 2000
max_match_val_new, template_image_out = track_h5(template_img, x, match_method=method, ind_list=ind_list)

for k1, k2 in utils.loop_segments(frame_nums):
    plt.plot(max_match_val_new[k1:k2], linewidth=.3)
plt.legend(trial_nums)

match_list = ['TM_SQDIFF_NORMED', 'TM_CCORR_NORMED', 'TM_CCOEFF_NORMED', 'TM_SQDIFF', 'TM_CCORR', 'TM_CCOEFF']

h5_file = '/Users/phil/Downloads/test_pole_tracker/AH0667x170317.h5'
meth_dict = dict()
meth_dict['h5_file'] = h5_file
ind_list = None
for template_image_ind in [0, 2000]:
    for method in match_list:
        max_match_val_new, template_image = track_h5(template_image_ind, h5_file, match_method='cv2.' + method,
                                                     ind_list=ind_list)
        meth_dict['ind_' + str(template_image_ind) + '_' + method] = max_match_val_new

for method in match_list:
    max_match_val_new, template_image = track_h5(template_img, h5_file, match_method='cv2.' + method, ind_list=ind_list)
    meth_dict['ind_template_img_' + method] = max_match_val_new

fig, ax = plt.subplots(nrows=3, ncols=3, sharex=True, sharey=False)
ax_list = fig.axes
cnt = -1
for k in meth_dict:
    if 'h5_file' not in k and 'NORM' in k:
        cnt += 1
        if len(ax_list) == cnt:
            cnt = 0
            fig, ax = plt.subplots(nrows=2, ncols=3, sharex=True, sharey=False)
            ax_list = fig.axes
        ax1 = ax_list[cnt]
        ax1.set_title(k)
        # plt.title(k)
        for k1, k2 in utils.loop_segments(frame_nums):
            try:
                x = np.asarray(meth_dict[k][k1:k2])
                # ax1.plot(x-x[0],linewidth=.3, alpha = 1)
                ax1.plot(x, linewidth=.3, alpha=1)
            except:
                break
plt.legend(trial_nums)

# plt.imshow(image_tools.get_h5_key_and_concatenate(h5_file, 'images'))

a = analysis.pole_plot('/Users/phil/Downloads/test_pole_tracker/AH0667x170317.h5')

a.current_frame = 0
a.plot_it()

a.current_frame = 1000
a.plot_it()
""""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""

h5_file = '/Users/phil/Downloads/test_pole_tracker/AH0667x170317.h5'
method = 'cv2.TM_CCOEFF'
method = 'cv2.TM_CCOEFF_NORMED'
method = 'cv2.TM_SQDIFF_NORMED'
ind_list = None
template_image_ind = 2000  # know this is a good starting point with no whiskers in it
ls = np.asarray(utils.loop_segments(frame_nums, returnaslist=True))
all_maxes = []
trial_inds = range(len(frame_nums))
self_references_frame_compares = np.zeros(np.sum(frame_nums))
max_match_all = []
max_match_all2 = []
trial_ind_all = []
template_img_all = []
template_image_ind_all = []
for k in range(len(frame_nums)):
    template_image_ind_all.append(template_image_ind)
    max_match, template_img = track_h5(int(template_image_ind), h5_file, match_method=method, ind_list=ind_list)
    template_img_all.append(template_img)
    max_match_all.append(np.asarray(max_match))
    max_match_all2.append(np.asarray(max_match))
    trial_ind = np.where(template_image_ind < np.cumsum(frame_nums))[0][0]
    trial_ind_all.append(trial_ind)
    self_references_frame_compares[ls[0, trial_ind]:ls[1, trial_ind]] = max_match[ls[0, trial_ind]:ls[1, trial_ind]]
    if k == len(frame_nums)-1:
        break
    for kt in trial_ind_all:
        for kk in max_match_all:
            kk[ls[0, kt]:ls[1, kt]] = np.nan
            kk[ls[0, kt]:ls[1, kt]] = np.nan
    _val = -99999999999
    _ind = -99999999999
    for kk in max_match_all:
        tmp1 = np.nanmax(kk)
        tmp2 = np.nanargmax(kk)
        if tmp1 > _val:
            _val = copy.deepcopy(tmp1)
            _ind = copy.deepcopy(tmp2)
    # template_image_ind = copy.deepcopy(_ind)
    template_image_ind = template_image_ind+4000

kernel_size = 1
for k1, k2 in utils.loop_segments(frame_nums):
    plt.plot(medfilt(self_references_frame_compares[k1:k2], kernel_size=kernel_size), linewidth = 0.3)
plt.legend(range(len(frame_nums)))
plt.title(method)


# pred_bool_smoothed = medfilt(copy.deepcopy(pred_bool_temp), kernel_size=kernel_size)

fig, ax = plt.subplots(nrows=1, ncols=5, sharex=True, sharey=False)
ax_list = fig.axes
for i, k in enumerate(ax_list):
    k.imshow(template_img_all[i])
    k.set_title(template_image_ind_all[i])



x = np.mean(np.asarray(max_match_all2), axis = 0)
kernel_size = 1
for k1, k2 in utils.loop_segments(frame_nums):
    plt.plot(medfilt(x[k1:k2], kernel_size=kernel_size), linewidth = 0.3)
plt.legend(range(len(frame_nums)))
plt.title(method)
"""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""

h5_file = '/Users/phil/Dropbox/HIRES_LAB/curation_for_auto_curator/Data/Jon/AH0667/170317/AH0667x170317.h5'
trial_nums_and_frame_nums = image_tools.get_h5_key_and_concatenate(h5_file, 'trial_nums_and_frame_nums')
frame_nums = trial_nums_and_frame_nums[1, :].astype(int)

method = 'cv2.TM_CCORR_NORMED'
frame_to_compare = 2000
testing_frames_start = 1250
testing_frames_len = 50

method = 'cv2.TM_CCOEFF'#console regular# best
frame_to_compare = 1
testing_frames_start = 1250
testing_frames_len = 50

# method = 'cv2.TM_CCOEFF' #console (1)
# frame_to_compare = 2000
# testing_frames_start = 1250
# testing_frames_len = 50

ind_list = None
all_tests = []
for ktrial, _ in utils.loop_segments(frame_nums):
    template_image_ind = frame_to_compare+ktrial
    max_match_all = []
    for k1, k2 in utils.loop_segments(frame_nums):
        ind_list = np.arange(testing_frames_start, testing_frames_start+testing_frames_len) + k1
        max_match, template_img = track_h5(int(template_image_ind), h5_file, match_method=method, ind_list=ind_list)
        max_match = np.asarray(max_match).astype(float)
        max_match_all.append(max_match-max_match[0])
    all_tests.append(np.asarray(max_match_all).flatten())

all_var = []
for i, k in enumerate(all_tests):
    addto = (10**6)*i*2
    k = k[(k>np.quantile(k,0.1)) & (k<np.quantile(k,0.9))]
    plt.plot(k+addto, '.', markersize = 0.3)
    # plt.plot(k+addto, '-k', linewidth = 0.05)
    all_var.append(np.var(k))
plt.legend(np.argsort(all_var))

plt.figure()
for i, k in enumerate(all_tests):
    addto = (10**6)*i*2
    plt.plot(k+addto, '.', markersize = 0.3)





k1, k2 = utils.loop_segments(frame_nums, returnaslist=True)
template_image_ind = frame_to_compare+k1[np.argmin(all_var)]

ind_list = None
max_match, template_img = track_h5(int(template_image_ind), h5_file, match_method=method, ind_list=ind_list)

locations_x_y = image_tools.get_h5_key_and_concatenate(h5_file, 'locations_x_y')
tmp1 = np.argsort(locations_x_y[:, 0][2000::4000])

k1, k2 = utils.loop_segments(frame_nums, returnaslist = True)

for i, k in enumerate(tmp1):
    addto = i*10**6
    plt.plot(np.asarray(max_match[k1[k]:k2[k]])+addto, linewidth=0.3)


for i, k in enumerate(tmp1):
    addto = i*10**-3
    plt.plot(np.asarray(max_match[k1[k]:k2[k]])+addto, linewidth=0.3)



"""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""
k1, k2 = utils.loop_segments(frame_nums, returnaslist=True)
all_var_inds = np.argsort(all_var)
all_max = []
for ii in range(4):
    template_image_ind = frame_to_compare+k1[all_var_inds[ii]]
    ind_list = None
    max_match, template_img = track_h5(int(template_image_ind), h5_file, match_method=method, ind_list=ind_list)
    all_max.append(max_match)


max_match_mean = np.nanmean(np.asarray(all_max), axis = 0)
tmp1 = np.argsort(locations_x_y[:, 0][2000::4000])
for i, k in enumerate(tmp1):
    addto = i*10**6
    plt.plot(np.asarray(max_match_mean[k1[k]:k2[k]])+addto, linewidth=0.3)


x = np.asarray(all_max)
for i, k in enumerate(tmp1):
    addto = i*10**6
    x1  = x[0][k1[k]:k2[k]]+addto
    x2  = x[1][k1[k]:k2[k]]+addto
    plt.plot(x1-x2, linewidth=0.3)











"""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""
"""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""
"""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""
"""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""
"""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""


from IPython.utils import io

vit = dict()
vit['all_acc_before_no_pole_mask'] = []
vit['all_acc_after_no_pole_mask'] = []
vit['all_acc_before'] = []
vit['all_acc_after'] = []
vit['h5_img_file'] = []
vit['h5_img_file_full_dir'] = []

vit['m_name'] = m_names
vit['L_key']= label_key
vit['vm_name'] = vit_m_names
vit['h5_img_file_full_dir']= to_pred_h5s
for k in vit['h5_img_file_full_dir']:
  vit['h5_img_file'].append(os.path.basename(k))

for h5_img_file in to_pred_h5s:
  in_range = image_tools.get_h5_key_and_concatenate([h5_img_file], 'in_range')
  tmp1 = []
  tmp2 = []
  tmp3 = []
  tmp4 = []
  for iii, (vm_name, m_name, L_key) in enumerate(tzip(vit_m_names, m_names, label_key)):
    pred_m_raw = image_tools.get_h5_key_and_concatenate([h5_img_file], key_name=m_name)
    pred_v = image_tools.get_h5_key_and_concatenate([h5_img_file], key_name=vm_name)
    real = image_tools.get_h5_key_and_concatenate([h5_img_file], key_name=L_key)
    if pred_m_raw.shape[1] ==1:
      pred_m = ((pred_m_raw>0.5)*1).flatten()
    else:
      pred_m = np.argmax(pred_m_raw, axis = 1)# turn into integers instead of percentages

    # get everything back to binary (if possible)
    with io.capture_output() as captured:#prevents crazy printing

      pred_m_bool = utils.convert_labels_back_to_binary(pred_m, L_key)
      real_bool = utils.convert_labels_back_to_binary(real, L_key)
      pred_v_bool = utils.convert_labels_back_to_binary(pred_v, L_key)
    if real_bool is None: # convert labels will return None if it cant convert
    #it back to the normal format. i.e. only onset or only offsets...
      tmp1.append(0)
      tmp2.append(0)
      tmp3.append(0)
      tmp4.append(0)
    else:
      tmp1.append(np.mean(real_bool == pred_m_bool))
      tmp2.append(np.mean(real_bool == pred_v_bool))
      tmp3.append(np.mean(real_bool*in_range == pred_m_bool*in_range))
      tmp4.append(np.mean(real_bool*in_range == pred_v_bool*in_range))

  vit['all_acc_before_no_pole_mask'].append(tmp1)
  vit['all_acc_after_no_pole_mask'].append(tmp2)
  vit['all_acc_before'].append(tmp3)
  vit['all_acc_after'].append(tmp4)
  # vit['m_name'] = list(dict.fromkeys(vit['m_name']))
  # vit['L_key'] = list(dict.fromkeys(vit['L_key']))
  # vit['h5_img_file_full_dir'].append(h5_img_file)


vit2 = copy.deepcopy(vit)
