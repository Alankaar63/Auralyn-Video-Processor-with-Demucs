import os
import subprocess
import shutil

def extract_audio(videopath:str,audio_output_path:str):
    cmd = [
        "ffmpeg", #powerful tool to extract audio from video
        "-y",
        "-i",videopath, #tells ffmpeg which input to process
        "-vn", #means jsut ignore video and just extract audio
        "-acodec","pcm_s16le", #uncompressed wav file
        "-ar","44100",
        "-ac","2",
        audio_output_path #audio is saved to this path in .wav format
    ]
    subprocess.run(cmd,check=True)

def seperate_voice(audio_output_path:str, output_dir:str):
    cmd=[
        "demucs",
        "--two-stems","vocals", #seperate vocals from other sounds
        "-o",output_dir,
        audio_output_path
    ]
    subprocess.run(cmd,check=True)

    base = os.path.splitext(os.path.basename(audio_output_path))[0]
    demucs_dir = os.path.join(output_dir,"htdemucs")
    vocals_path = os.path.join(demucs_dir,base,"vocals.wav")

    if not os.path.exists(vocals_path):
        raise FileNotFoundError(f"Vocals file not found at {vocals_path}")

    return vocals_path


def recombine_audio_with_video(original_video_path:str, audio_output_path:str, final_output_path:str):
    cmd = [
        "ffmpeg",
        "-y",
        "-i",original_video_path,
        "-i",audio_output_path,
        "-c:v","copy", #dont touch the video just copy it as it is
        "-map","0:v:0", #take video from first input file
        "-map","1:a:0", #take audio from second input file
        "-shortest", #ensures video and audio are trimmed to shortest length
        final_output_path
    ]
    subprocess.run(cmd,check=True)
