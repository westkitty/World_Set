#!/usr/bin/env python3
"""Encode walkthrough frames -> MP4 (+ small GIF preview) via static ffmpeg."""
import os
import glob
import subprocess
import imageio_ffmpeg
from PIL import Image

FRAMES = sorted(glob.glob('/home/user/World_Set/work/frames/walk_*.png'))
OUT = '/home/user/World_Set/WorldKit/video'
os.makedirs(OUT, exist_ok=True)
assert FRAMES, 'no frames found'
print(len(FRAMES), 'frames')

exe = imageio_ffmpeg.get_ffmpeg_exe()
mp4 = os.path.join(OUT, 'walkthrough.mp4')
subprocess.run([exe, '-y', '-framerate', '12', '-i',
                '/home/user/World_Set/work/frames/walk_%04d.png',
                '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p',
                '-movflags', '+faststart', mp4], check=True)
print('mp4 done', os.path.getsize(mp4) // 1024, 'KB')

# GIF preview: every 2nd frame at 480px
ims = []
for f in FRAMES[::2]:
    im = Image.open(f).resize((480, 270), Image.LANCZOS).convert('P', palette=Image.ADAPTIVE,
                                                                 colors=128)
    ims.append(im)
ims[0].save(os.path.join(OUT, 'walkthrough_preview.gif'), save_all=True, append_images=ims[1:],
            duration=166, loop=0)
print('gif done')
