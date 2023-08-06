# __main__.py

import cv2
import numpy as np
import glob
import tqdm
import importlib
import pathlib
import shutil
import os
import subprocess
import time
import torch.multiprocessing as mp
import torch
import dsfd
import dsfd.face_detection
from utils import parse_arg, detect_face_multiprocessing, get_video_frame_details, combine_output_files
import argparse


def main():
		"""main"""
		torch.multiprocessing.set_start_method('spawn', force=True)
		
		args = parse_args()
		filename = args.filename	
		num_workers = args.num_workers 
		output_file_name = f"{filename.split('.')[0]}_fd.{filename.split('.')[1]}"
		width, height, frame_count, fps = get_video_frame_details(filename)
		frame_jump_unit =  frame_count // (num_workers)
		
		print(f"Video frame count = {frame_count}")
		print(f"Width = {width}, Height = {height}, FPS = {fps}")
		print(f"Number of CPUs: 		{num_workers}")
		print(f"frame_jump_unit:		{frame_jump_unit}")
		"""
		start_time = time.time()
		
		# Paralle the execution of a function across multiple input values
		with mp.Pool(processes=num_workers) as p:
				print(p)
				p.map(detect_face_multiprocessing, range(num_workers))

		combine_output_files(num_workers, output_file_name)
		end_time = time.time()
		total_processing_time = end_time - start_time
		inf_fps = frame_count/total_processing_time
		print(f"Time taken: {total_processing_time}")
		print(f"Inference FPS : {inf_fps}")
		"""

if __name__ == '__main__':
		main()
