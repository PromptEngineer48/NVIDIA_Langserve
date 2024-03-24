from getpass import getpass
import requests
import os
from dotenv import load_dotenv


def fetch_nvapi_key():
    # Load environment variables from .env file
    load_dotenv()

    hard_reset = False  ## <-- Set to True if you want to reset your NVIDIA_API_KEY
    while "nvapi-" not in os.environ.get("NVIDIA_API_KEY", "") or hard_reset:
        try:
            assert not hard_reset
            response = requests.get("http://docker_router:8070/get_key").json()
            assert response.get("nvapi_key")
        except:
            response = {"nvapi_key": getpass("NVIDIA API Key: ")}
        os.environ["NVIDIA_API_KEY"] = response.get("nvapi_key")
        try:
            requests.post(
                "http://docker_router:8070/set_key/",
                json={"nvapi_key": os.environ["NVIDIA_API_KEY"]},
            ).json()
        except:
            pass
        hard_reset = False
        if "nvapi-" not in os.environ.get("NVIDIA_API_KEY", ""):
            print(
                "[!] API key assignment failed. Make sure it starts with `nvapi-` as generated from the model pages."
            )

    print(
        f"Retrieved NVIDIA_API_KEY beginning with \"{os.environ.get('NVIDIA_API_KEY')[:9]}...\""
    )

    return os.environ.get("NVIDIA_API_KEY")


from langchain_nvidia_ai_endpoints._common import NVEModel


def get_available_models():
    nve_model = NVEModel()
    print(nve_model.available_models)
    return nve_model.available_models
