import os 
import random
resolutions_pc = [
    (800, 600),
    (1024, 768),
    (1280, 720),
    (1366, 768),
    (1600, 900),
    (1920, 1080),
    (2560, 1440),
    (2560, 1600),
    (3440, 1440),
    (3840, 2160),
    (5120, 2880),
    (5120, 2160),
    (7680, 4320),
    (7680, 2160)
]

resolution_choice = [x for x in range(len(resolutions_pc))]

chrome_vendor_gpu = [


    ("Google Inc. (Intel)", "ANGLE (Intel, Intel(R) HD Graphics 520 (0x1916) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (Intel)", "ANGLE (Intel, Intel(R) HD Graphics 530 (0x191B) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (Intel)", "ANGLE (Intel, Intel(R) HD Graphics 5500 (0x1616) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (Intel)", "ANGLE (Intel, Intel(R) UHD Graphics 620 (0x5917) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (Intel)", "ANGLE (Intel, Intel(R) UHD Graphics 630 (0x3E9B) Direct3D11 vs_5_0 ps_5_0, D3D11)"),


]
temp = [
        ("Google Inc. (AMD)", "ANGLE (AMD, AMD Radeon RX 5600 XT (0x731F) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (AMD)", "ANGLE (AMD, AMD Radeon RX 5700 XT (0x731F) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (AMD)", "ANGLE (AMD, AMD Radeon RX 580 (0x67DF) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (AMD)", "ANGLE (AMD, AMD Radeon RX 6700 XT (0x73DF) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (AMD)", "ANGLE (AMD, AMD Radeon RX 6800 (0x73BF) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (AMD)", "ANGLE (AMD, AMD Radeon RX 6900 XT (0x73BF) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (AMD)", "ANGLE (AMD, AMD Radeon R9 380 (0x6938) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (AMD)", "ANGLE (AMD, AMD Radeon Pro 560X (0x67EF) Direct3D11 vs_5_0 ps_5_0, D3D11)") ,
    
        ("Google Inc. (NVIDIA Corporation)", "ANGLE (NVIDIA, NVIDIA GeForce GTX 750 Ti (0x1380) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (NVIDIA Corporation)", "ANGLE (NVIDIA, NVIDIA GeForce GTX 960 (0x1401) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (NVIDIA Corporation)", "ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 (0x1C8D) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (NVIDIA Corporation)", "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 (0x1C03) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (NVIDIA Corporation)", "ANGLE (NVIDIA, NVIDIA GeForce GTX 1070 (0x1B81) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (NVIDIA Corporation)", "ANGLE (NVIDIA, NVIDIA GeForce GTX 1080 (0x1B80) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (NVIDIA Corporation)", "ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 Ti (0x2182) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (NVIDIA Corporation)", "ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 (0x1F12) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (NVIDIA Corporation)", "ANGLE (NVIDIA, NVIDIA GeForce RTX 2070 Super (0x1E84) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (NVIDIA Corporation)", "ANGLE (NVIDIA, NVIDIA GeForce RTX 2080 Ti (0x1E04) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (NVIDIA Corporation)", "ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 (0x2503) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (NVIDIA Corporation)", "ANGLE (NVIDIA, NVIDIA GeForce RTX 3070 (0x2484) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
    ("Google Inc. (NVIDIA Corporation)", "ANGLE (NVIDIA, NVIDIA GeForce RTX 3090 (0x2204) Direct3D11 vs_5_0 ps_5_0, D3D11)"),
]
user_agents = [
    #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.188 Safari/537.36",
    #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36",
    #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
    #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.129 Safari/537.36",
    #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
]

def combinaison() :
    combinaison_value = [] 
    for x in resolutions_pc : 
         for y in user_agents : 
            for z in chrome_vendor_gpu :
                combinaison_value.append((x,y ,z))
    return combinaison_value

combinaison_choice = [x for x in range(len(user_agents) * len(resolution_choice)*len(chrome_vendor_gpu))]

def get_random_combination() -> tuple[tuple[int, int], str, tuple[str, str]]:
    resolution = random.choice(resolutions_pc)
    user_agent = random.choice(user_agents)
    gpu = random.choice(chrome_vendor_gpu)
    return (resolution, user_agent, gpu)


current_dir = os.path.dirname(os.path.abspath(__file__))

PATH_EXTENSION = os.path.join(current_dir , "extension_nopecha")
