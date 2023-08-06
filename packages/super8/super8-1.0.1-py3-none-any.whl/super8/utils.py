import cv2
import subprocess
import argparse


def parse_args(args=sys.argv[1:]):
		"""Parses commandline arugments"""
		parser = argparse.ArgumentParser(prog='super8', description='super8 is an open-source toolset for video analysis')
		subparsers = parser.add_subparsers(help='sub-command help')
		
		add_detect_subparser(subparsers)
		
		return parser.parse_args(args)

def add_detect_subparser(subparsers):
		parser = subparsers.add_parser('detect', help='detect faces in the video')
		parser.add_argument('-i', action="store", dest='filename',
                    help='filename of video to process')
		parser.add_argument('--m', dest='multiprocessing', default=False,
                    help='add multiprocessing')
		parser.add_argument('--num_workers', dest='num_workers', default=mp.cpu_count(),
                    help='specify number of threads, that you want to utilize(optional)')
		parser.add_argument('--to_csv', dest='to_csv',
                    help='creates a csv with detection readings')
		parser.add_argument('--visualize', dest='visualize',
                    help='creates a new video with visualization')
		args = parser.parse_args()	
		parser.set_defaults(command='detect')

def get_video_frame_details(file_name):
    cap = cv2.VideoCapture(file_name)
    width, height = (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    return width, height, frame_count, fps


def detect_face_multiprocessing(worker_i):

    torch.set_num_threads(1)
    # initialize the process group
    # torch.distributed.init_process_group("gloo", rank=worker_i, world_size=mp.cpu_count())
    print(f"worker #{worker_i} spawned")
    # worker_i - current worker
    file_name = "../test57.mp4"
    cap = cv2.VideoCapture(file_name)
    width, height = (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    # num_workers = mp.cpu_count()
    num_workers = 12
    print(f"frame_count:  {frame_count}")
    print(f"num_workers:  {num_workers}")
    frame_jump_unit =  frame_count // num_workers
    print(f"frame_jump_unit:   {frame_jump_unit}")
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_jump_unit * worker_i)


    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter()
    out.open("output_{}.mp4".format(worker_i), fourcc, fps, (width, height), True)

    i = 0
    #  device=torch.device("cpu"),
    # dsfd = importlib.import_module("DSFD-Pytorch-Inference")
    # print(dsfd)
    print("before detector")
    detector = dsfd.face_detection.build_detector("RetinaNetMobileNetV1", device=torch.device("cpu"), confidence_threshold=.5, nms_iou_threshold=.3)
    print(f"detector:    {detector}")
    print("after detector")
    rectangles = []


def combine_output_files(num_workers, output_file_name):
    print("combinging output files...")
    # Create a list of output files and store the file names in a txt file
    list_of_output_files = ["output_{}.mp4".format(i) for i in range(num_workers)]
    with open("list_of_output_files.txt", "w") as f:
        for t in list_of_output_files:
            f.write("file {} \n".format(t))

    # use ffmpeg to combine the video output files
    ffmpeg_cmd = "ffmpeg -y -loglevel error -f concat -safe 0 -i list_of_output_files.txt -vcodec copy " + output_file_name
    subprocess.Popen(ffmpeg_cmd, shell=True).wait()

    # Remove the temperory output files
    for f in list_of_output_files:
        os.remove(f)
    os.remove("list_of_output_files.txt")
