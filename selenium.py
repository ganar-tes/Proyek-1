import os
import platform
import subprocess
import sys
import requests
from zipfile import ZipFile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def install_selenium():
    print("Menginstal Selenium...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "selenium"])
    print("Selenium berhasil diinstal.\n")

def install_dependencies():
    print("Memastikan dependencies dasar diinstal...")
    subprocess.run(["sudo", "apt", "update", "-y"])
    subprocess.run(["sudo", "apt", "install", "-y", "wget", "unzip", "curl"])
    print("Dependencies berhasil diinstal.\n")

def get_chrome_version():
    system_name = platform.system()
    if system_name == "Windows":
        try:
            # Mendapatkan versi Chrome di Windows
            result = subprocess.run(
                r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True,
            )
            version = result.stdout.split("REG_SZ")[-1].strip()
            return version.split(".")[0]
        except Exception as e:
            print("Gagal mendapatkan versi Chrome:", e)
    elif system_name == "Linux":
        try:
            # Mendapatkan versi Chrome di Linux
            result = subprocess.run(
                ["google-chrome", "--version"], stdout=subprocess.PIPE, text=True
            )
            version = result.stdout.split(" ")[2]
            return version.split(".")[0]
        except Exception as e:
            print("Gagal mendapatkan versi Chrome:", e)
    else:
        print("Sistem operasi tidak didukung.")
        sys.exit(1)

def download_chromedriver(chrome_version):
    print("Mendownload ChromeDriver versi terbaru...")
    base_url = "https://chromedriver.storage.googleapis.com/"
    latest_url = f"{base_url}LATEST_RELEASE_{chrome_version}"

    try:
        latest_version = requests.get(latest_url).text.strip()
        print(f"Versi ChromeDriver terbaru: {latest_version}")

        # Tentukan file yang sesuai dengan OS
        system_name = platform.system()
        if system_name == "Windows":
            download_url = f"{base_url}{latest_version}/chromedriver_win32.zip"
        elif system_name == "Linux":
            download_url = f"{base_url}{latest_version}/chromedriver_linux64.zip"
        else:
            print("Sistem operasi tidak didukung untuk ChromeDriver.")
            sys.exit(1)

        # Download file
        response = requests.get(download_url, stream=True)
        with open("chromedriver.zip", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print("ChromeDriver berhasil didownload.\n")
        return "chromedriver.zip"
    except Exception as e:
        print("Gagal mendownload ChromeDriver:", e)
        sys.exit(1)

def extract_and_setup_chromedriver(zip_file_path):
    print("Ekstraksi dan pemasangan ChromeDriver...")
    with ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(".")
    chromedriver_path = os.path.abspath("chromedriver")

    # Pindahkan ke direktori PATH agar bisa diakses
    target_dir = "/usr/local/bin" if platform.system() == "Linux" else "C:\\Windows\\System32"
    try:
        shutil.move(chromedriver_path, target_dir)
        print(f"ChromeDriver berhasil dipasang di {target_dir}.\n")
    except Exception as e:
        print("Gagal memindahkan ChromeDriver:", e)
    finally:
        os.remove(zip_file_path)

def install_google_chrome():
    print("Menginstal Google Chrome...")
    system_name = platform.system()
    try:
        if system_name == "Windows":
            chrome_installer = "chrome_installer.exe"
            download_url = "https://dl.google.com/chrome/install/latest/chrome_installer.exe"
        elif system_name == "Linux":
            chrome_installer = "google-chrome-stable_current_amd64.deb"
            download_url = "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
        else:
            print("Sistem operasi tidak didukung untuk Google Chrome.")
            sys.exit(1)

        # Download installer
        response = requests.get(download_url, stream=True)
        with open(chrome_installer, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print("Google Chrome berhasil didownload.\n")

        # Pasang Chrome
        if system_name == "Windows":
            subprocess.run([chrome_installer], check=True)
        elif system_name == "Linux":
            subprocess.run(["sudo", "dpkg", "-i", chrome_installer])
            subprocess.run(["sudo", "apt", "-f", "install", "-y"])
        print("Google Chrome berhasil dipasang.\n")

        # Hapus installer
        os.remove(chrome_installer)
    except Exception as e:
        print("Gagal menginstal Google Chrome:", e)
        sys.exit(1)

def setup_selenium_headless():
    print("Mengonfigurasi Selenium untuk berjalan dalam mode headless...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    print("Selenium berhasil dikonfigurasi untuk mode headless.\n")
    return driver

if __name__ == "__main__":
    # Instal dependencies dasar
    install_dependencies()

    # Instal Selenium
    install_selenium()

    # Instal Google Chrome
    install_google_chrome()

    # Download dan pasang ChromeDriver
    chrome_version = get_chrome_version()
    if chrome_version:
        zip_file = download_chromedriver(chrome_version)
        extract_and_setup_chromedriver(zip_file)
    else:
        print("Gagal mendapatkan versi Chrome.")

    # Setup Selenium untuk mode headless
    setup_selenium_headless()
