# uvicorn fast:app --host 0.0.0.0 --port 8000
from fastapi import FastAPI
import pynvml

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # NVIDIAドライバーと関連ライブラリを初期化
    pynvml.nvmlInit()

@app.on_event("shutdown")
async def shutdown_event():
    # NVIDIAドライバーと関連ライブラリをクリーンアップ
    pynvml.nvmlShutdown()

@app.get("/erie")
async def get_gpu_info():
    gpu_info = []

    # 利用可能なGPUの数を取得
    device_count = pynvml.nvmlDeviceGetCount()

    # 各GPUの情報を取得
    for i in range(device_count):
        gpu_data = {}
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        gpu_name = pynvml.nvmlDeviceGetName(handle)
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
        fan_speed = pynvml.nvmlDeviceGetFanSpeed(handle)
        temperature = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)

        gpu_data["GPU"] = f"GPU{i}"
        gpu_data["Name"] = gpu_name.decode()
        gpu_data["Memory"] = f"{memory_info.total / 1024**2} MB"
        gpu_data["Utilization"] = f"{utilization.gpu}%"
        gpu_data["Fan Speed"] = f"{fan_speed}%"
        gpu_data["Temperature"] = f"{temperature}°C"

        gpu_info.append(gpu_data)
        print(gpu_info)

    return gpu_info

