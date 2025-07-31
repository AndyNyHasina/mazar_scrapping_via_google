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
"Google Inc. (NVIDIA Corporation)",
"Google Inc. (Intel)",
"Google Inc. (AMD)",
"Google Inc. (ATI Technologies Inc.)"
]
firefox_vendor_gpu = [
"Mozilla (NVIDIA Corporation)",
"Mozilla (Intel Open Source Technology Center)",
"Mozilla (Intel)",
"Mozilla (ATI Technologies Inc.)"
]
Apple_vendor_gpu = [
"Apple Inc."
]
user_agents = [
    # ==== Chrome (Windows) ====
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.129 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.121 Safari/537.36",

    # ==== Chrome (Mac) ====
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.92 Safari/537.36",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.102 Safari/537.36",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36",

    # ==== Firefox (Windows) ====
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:114.0) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:113.0) Gecko/20100101 Firefox/113.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0",

    # ==== Firefox (Mac) ====
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 13.4; rv:116.0) Gecko/20100101 Firefox/116.0",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 12.6; rv:115.0) Gecko/20100101 Firefox/115.0",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 11.7; rv:114.0) Gecko/20100101 Firefox/114.0",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:113.0) Gecko/20100101 Firefox/113.0",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:112.0) Gecko/20100101 Firefox/112.0",

    # ==== Microsoft Edge ====
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36 Edg/115.0.1901.183",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36 Edg/114.0.1823.67",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.129 Safari/537.36 Edg/113.0.1774.57",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.121 Safari/537.36 Edg/112.0.1722.64",

    # ==== Safari (macOS) ====
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15",

    # ==== Opera (Windows) ====
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36 OPR/101.0.4843.43",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.92 Safari/537.36 OPR/102.0.4880.56",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36 OPR/100.0.4815.54",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36 OPR/99.0.4788.77",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36 OPR/98.0.4759.39",




]

def combinaison() :
    combinaison_value = [] 
    for x in resolutions_pc : 
         for y in user_agents : 
            z=check_str(y)
            combinaison_value.append((x,y ,z))
    return combinaison_value

combinaison_choice = [x for x in range(len(user_agents) * len(resolution_choice))]


def check_str(user_agent: str):
    if "OPR" in user_agent or "Edg" in user_agent:
        return random.choice(chrome_vendor_gpu)
    elif "Safari" in user_agent and "Chrome" not in user_agent:
        return random.choice(Apple_vendor_gpu)
    elif "Firefox" in user_agent:
        if "Windows" in user_agent:
            return random.choice(firefox_vendor_gpu)
        elif "Macintosh" in user_agent:
            return "Mozilla (Apple GPU vendor)" 
        else:
            return "Mozilla (Unknown GPU vendor)"
    elif "Chrome" in user_agent:
        if "Windows" in user_agent:
            return random.choice(chrome_vendor_gpu)
        elif "Macintosh" in user_agent:
            return random.choice(Apple_vendor_gpu)
        else:
            return random.choice(chrome_vendor_gpu)
    else:
        return "Unknown GPU vendor"


    



current_dir = os.path.dirname(os.path.abspath(__file__))

PATH_EXTENSION = os.path.join(current_dir , "extension_nopecha")
