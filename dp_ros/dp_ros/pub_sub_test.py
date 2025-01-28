import os
import sys
import time
import math
from multiprocessing.managers import SharedMemoryManager
import click
import cv2
import numpy as np
import torch
import dill
import hydra
import pathlib
import skvideo.io
from omegaconf import OmegaConf
import scipy.spatial.transform as st
from diffusion_policy.common.precise_sleep import precise_wait
# from diffusion_policy.diffusion_policy.real_word.real_inference_utils import get_real_obs_resolution, get_real_obs_dict
from diffusion_policy.common.pytorch_util import dict_apply
from diffusion_policy.workspace.base_workspace import BaseWorkspace
from diffusion_policy.policy.base_image_policy import BaseImagePolicy
from diffusion_policy.common.cv2_util import get_image_transform

from diffusion_policy.shared_memory.shared_memory_ring_buffer import SharedMemoryRingBuffer

import rclpy
from rclpy.node import Node
import message_filters
from arm_control.msg import PosCmd
from arx5_arm_msg.msg import RobotCmd, RobotStatus
from sensor_msgs.msg import Image
import threading
from cv_bridge import CvBridge
import matplotlib.pyplot as plt

def main():
    rclpy.init()
    img1_topic = "/camera/camera/color/image_rect_raw"
    arm_control_node = rclpy.create_node("arm_control_node")
    arm_control_pub = arm_control_node.create_publisher(PosCmd, 'arm_control', 10)
    img1 = message_filters.Subscriber(arm_control_node,Image, img1_topic)
    arm_status = message_filters.Subscriber(arm_control_node, RobotStatus, "arm_status")
    ats = message_filters.ApproximateTimeSynchronizer(
        [arm_status, img1], queue_size=10, slop=0.1
    )
    ats.registerCallback(
        lambda *msg: callback(*msg)
    )

    cmd = PosCmd()
    cmd.x = 0.1
    cmd.time_count = 0
    while rclpy.ok():
        cmd.x += 0.1
        cmd.time_count += 1
        arm_control_pub.publish(cmd)
        precise_wait(1)


    rclpy.shutdown()

def callback(arm_status, img1):
    
    
    # global obs_ring_buffer
    # obs_data = dict()
    # obs_data["eef_qpos"] = np.array(
    #     [
    #         eef_qpos.x,
    #         eef_qpos.y,
    #         eef_qpos.z,
    #         eef_qpos.roll,
    #         eef_qpos.pitch,
    #         eef_qpos.yaw,
    #         eef_qpos.gripper,
    #     ]
    # )
    # gripper_width = qpos.joint_pos[6]