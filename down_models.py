import requests
import os
import time
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, SpinnerColumn


def format_speed(speed):
    """将字节每秒转换为合适的单位"""
    if speed < 1024:
        return f"{speed:.2f} B/s"
    elif speed < 1024 ** 2:
        return f"{speed / 1024:.2f} KB/s"
    elif speed < 1024 ** 3:
        return f"{speed / (1024 ** 2):.2f} MB/s"
    else:
        return f"{speed / (1024 ** 3):.2f} GB/s"


def download_file(url, local_filename):
    # 创建保存文件的目录
    directory = os.path.dirname(local_filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        # 发送请求并设置流模式
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            BarColumn(),
            TimeElapsedColumn(),
            TextColumn("{task.fields[speed]}")
        ) as progress:
            task = progress.add_task("Downloading", total=total_size, speed="0 B/s")
            start_time = time.time()
            downloaded_size = 0
            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(block_size):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        current_time = time.time()
                        elapsed_time = current_time - start_time
                        if elapsed_time > 0:
                            speed = downloaded_size / elapsed_time
                            progress.update(task, advance=len(chunk), speed=format_speed(speed))
    except requests.RequestException as e:
        print(f"下载 {url} 时出现网络错误: {e}")
    except FileNotFoundError:
        print(f"无法创建或写入文件 {local_filename}，请检查路径和权限。")
    except Exception as e:
        print(f"下载 {url} 时出现未知错误: {e}")


def main():
    file_info = [
        (
            "https://www.modelscope.cn/models/MAILAND/majicflus_v1/resolve/v1.0/majicflus_v134.safetensors",
            "fluxgym/models/unet/majicflus_v134.safetensors"
        ),
        (
            "https://www.modelscope.cn/models/muse/flux_clip_l/resolve/master/clip_l_bf16.safetensors",
            "fluxgym/models/clip/clip_l_bf16.safetensors"
        ),
        (
            "https://www.modelscope.cn/models/muse/t5xxl_fp16/resolve/master/t5xxl_fp16.safetensors",
            "fluxgym/models/clip/t5xxl_fp16.safetensors"
        ),
        (
            "https://www.modelscope.cn/models/muse/flux_vae/resolve/master/ae.safetensors",
            "fluxgym/models/vae/ae.safetensors"
        )
    ]

    for url, path in file_info:
        download_file(url, path)

main()