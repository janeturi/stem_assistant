import subprocess, time, requests, os

LLAMA = os.path.expanduser("~/.llama-app/llama")

server = subprocess.Popen(
    [
        LLAMA, "serve",
        "-hf", "unsloth/gemma-4-E2B-it-GGUF:Q4_K_M",
        "--alias", "gemma-4-e2b",
        "-c", "4096",
        "-ngl", "99",
        "--jinja",
        "--port", "8000",
    ],
    stdout=open("llama.log", "w"),
    stderr=subprocess.STDOUT,
)

def wait_for_server(url="http://localhost:8000/health", timeout=900):
    start = time.time()
    while time.time() - start < timeout:
        if server.poll() is not None:
            raise RuntimeError("Server exited early. Run the log cell below to see why.")
        try:
            if requests.get(url, timeout=2).status_code == 200:
                print(f"Server ready after {time.time() - start:.0f}s")
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(3)
    raise TimeoutError("Server didn't start in time. Run the log cell below.")

wait_for_server()