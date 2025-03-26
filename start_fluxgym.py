import subprocess
import os

def clone_repositories():
    """克隆 fluxgym 和 sd-scripts 仓库"""
    try:
        subprocess.run(["git", "clone", "https://github.com/cocktailpeanut/fluxgym"], check=True)
        os.chdir("fluxgym")
        subprocess.run(["git", "clone", "-b", "sd3", "https://github.com/kohya-ss/sd-scripts"], check=True)
        print("仓库克隆成功")
    except subprocess.CalledProcessError as e:
        print(f"克隆仓库时出错: {e}")

def create_venv():
    """创建虚拟环境并激活"""
    try:
        if os.name == "nt":  # Windows
            subprocess.run(["python", "-m", "venv", "env"], check=True)
            activate_script = os.path.join("env", "Scripts", "activate")
            subprocess.run([activate_script], shell=True, check=True)
        else:  # Linux
            subprocess.run(["python", "-m", "venv", "env"], check=True)
            subprocess.run(["source", "env/bin/activate"], shell=True, check=True)
        print("虚拟环境创建并激活成功")
    except subprocess.CalledProcessError as e:
        print(f"创建或激活虚拟环境时出错: {e}")

def install_dependencies():
    """安装依赖"""
    try:
        os.chdir("sd-scripts")
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        os.chdir("..")
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        subprocess.run(["pip", "install", "--pre", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cu121"], check=True)
        print("依赖安装成功")
    except subprocess.CalledProcessError as e:
        print(f"安装依赖时出错: {e}")

def start_app():
    """启动应用程序"""
    try:
        if os.name == "nt":  # Windows
            subprocess.run(["python", "app.py"], check=True)
        else:  # Linux
            subprocess.run(["bash", "app-launch.sh"], check=True)
        print("应用程序启动成功")
    except subprocess.CalledProcessError as e:
        print(f"启动应用程序时出错: {e}")

if __name__ == "__main__":
    #克隆项目
    clone_repositories()
    #创建虚拟环境
    create_venv()
    #安装依赖
    install_dependencies()
    #启动app
    start_app()
