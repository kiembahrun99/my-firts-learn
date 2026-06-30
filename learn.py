import os
import time
import re
import json
import random
from flask.cli import load_dotenv
import requests
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException

load_dotenv()
# ===================== VARIABEL =====================
# Ambil dari environment variables atau isi statis
PHONE = os.getenv("RECOVERY_PHONE", "")
EMAIL = os.getenv("RECOVERY_EMAIL", "")
NEW_PASSWORD = os.getenv("NEW_PASSWORD", "")
# ====================================================

# ===================== VARIABEL =====================
link = "https://admin.google.com/ac/home?ecid=C00wa7t59" 
# email = "student@goog-test.reseller.gappslabs.co.s-57h4rxr1.qwiklabs-gsuite.net"
# password = "4bbbeadc95ec02b2db38"
email = input("Masukkan email: ")
password = input("Masukkan password: ")
variabel_domain = email.split("@")[1] if "@" in email else ""
variabel_domain = "@" + variabel_domain if variabel_domain else ""
path_file_csv = "/Users/athiyyahzulfa/Documents/ROSYID/Affiliate/ffmpeg/users_updated.csv"
# ====================================================


def safe_get_title(driver):
    """Ambil title dengan aman, kembalikan string kosong jika gagal (misal saat redirect)."""
    try:
        return driver.title
    except WebDriverException:
        return ""


def safe_get_page_source(driver):
    """Ambil page_source dengan aman, kembalikan string kosong jika gagal."""
    try:
        return driver.page_source
    except WebDriverException:
        return ""


def direct_verif(driver):
    current_title = safe_get_title(driver)
    print(f"[DIRECT VERIF] Title saat ini: {current_title}")

    # if "Admin console" in current_title:
    #     print("[DIRECT VERIF] Sudah di admin.google.com — skip login, langsung verif_domain.")
    #     verif_domain(driver)
    # else:
    #     print("[DIRECT VERIF] Belum di admin.google.com — jalankan login dulu.")
    #     login(driver)


def init_driver():
    driver = Driver(
        uc=True,
        incognito=True,
        locale_code="id-ID",
        no_sandbox=True,
        disable_gpu=True
    )
    # driver.maximize_window()
    driver.implicitly_wait(10)
    return driver


def wait_for_text(driver, text, timeout=30):
    """Tunggu sampai teks tertentu muncul di halaman."""
    WebDriverWait(driver, timeout).until(
        lambda d: text in d.page_source
    )


def scroll_and_click(driver, element):
    """Scroll ke elemen lalu klik."""
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.3)
    element.click()


def login(driver):
    global link
    print("[LOGIN] Membuka halaman login...")

    # 1. Buka link
    driver.get(link)

    # 2. Tunggu loading halaman selesai
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    # 3. Tunggu title "Login - Akun Google"
    WebDriverWait(driver, 30).until(EC.title_contains("Login"))
    print("[LOGIN] Halaman login terbuka.")

    # 4. Sleep 0.5
    time.sleep(0.5)

    # 5. Isi email
    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "identifierId"))
    )
    email_input.clear()
    email_input.send_keys(email)
    print("[LOGIN] Email diisi.")

    # 6. Sleep 0.5
    time.sleep(0.5)

    # 7. Klik tombol "Berikutnya" (setelah email)
    next_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@jsname='V67aGc' and text()='Berikutnya']/.."))
    )
    next_btn.click()
    print("[LOGIN] Klik Berikutnya (email).")

    # 8. Tunggu sampai ada teks "Masukkan sandi"
    wait_for_text(driver, "Masukkan sandi")
    print("[LOGIN] Halaman password muncul.")

    # 9. Isi password
    password_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "Passwd"))
    )
    password_input.clear()
    password_input.send_keys(password)
    print("[LOGIN] Password diisi.")

    # 10. Sleep 0.5
    time.sleep(0.5)

    # 11. Klik tombol "Berikutnya" (setelah password)
    next_btn2 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@jsname='V67aGc' and text()='Berikutnya']/.."))
    )
    next_btn2.click()
    print("[LOGIN] Klik Berikutnya (password).")

    # Tunggu halaman selesai load setelah login Google
    try:
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("[LOGIN] Halaman selesai loading setelah login.")
    except Exception:
        print("[LOGIN] Timeout menunggu readyState, lanjut tetap.")

    time.sleep(2)  # Tunggu redirect setelah login

    skip_to_getsetup = False
    try:
        btn = driver.find_element(By.XPATH, "//button[@jscontroller='soHxf']")
        driver.execute_script("arguments[0].click();", btn)
        print("BERHASIL: Tombol berhasil diklik.")
    except Exception as e:
        print(f"GAGAL: {e}")

    if not skip_to_getsetup:
        try:
            # Tunggu "Terms of Service"
            wait_for_text(driver, "Terms of Service")
            print("[LOGIN] Halaman Terms of Service muncul.")
        except Exception:
            print("[LOGIN] Halaman Terms of Service tidak muncul.")

        time.sleep(0.5)

        try:
            # Scroll ke bawah dan klik "Accept Terms of Service"
            accept_tos = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Accept Terms of Service')]/.."))
            )
            scroll_and_click(driver, accept_tos)
            print("[LOGIN] Klik 'Accept Terms of Service'.")
        except Exception:
            print("[LOGIN] Halaman 'Accept Terms of Service' tidak muncul.")

        try:
            # Tunggu "Make Workspace work for you"
            wait_for_text(driver, "Make Workspace work for you")
            print("[LOGIN] Halaman 'Make Workspace work for you' muncul.")
        except Exception:
            print("[LOGIN] Halaman 'Make Workspace work for you' tidak muncul.")

        time.sleep(3)
    else:
        print("[LOGIN] Skip langsung ke 'Get set up' karena tombol awal gagal diklik.")

    try:
        # Klik "Get set up"
        get_setup_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@jsname='V67aGc' and text()='Get set up']/.."))
        )
        get_setup_btn.click()
        print("[LOGIN] Klik 'Get set up'.")
    except Exception:
        print("[LOGIN] Halaman 'Get set up' tidak muncul.")

    time.sleep(3)

    try:
        # Klik "Get set up"
        get_setup_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@jsname='V67aGc' and text()='Get set up']/.."))
        )
        get_setup_btn.click()
        print("[LOGIN] Klik 'Get set up'.")
    except Exception:
        print("[LOGIN] Halaman 'Get set up' tidak muncul.")

    time.sleep(5)

    driver.get("https://admin.google.com/")
    time.sleep(2)

    # Tunggu tombol Verify muncul
    wait = WebDriverWait(driver, 10)

    try:
        link = driver.find_element(By.CSS_SELECTOR, 'a.UywwFc-mRLv6.UywwFc-RLmnJb')
        driver.execute_script("arguments[0].click();", link)
        print("BERHASIL: Tombol Verify berhasil diklik.")
    except Exception as e:
        print(f"GAGAL: {e}")

    # Tutup tab lama, pindah ke tab baru
    time.sleep(2)
    original_window = driver.window_handles[0]
    new_window = driver.window_handles[-1]
    driver.close()
    driver.switch_to.window(new_window)
    print("[VERIF DOMAIN] Pindah ke tab baru.")

    print("[LOGIN] Ekstraksi session cookies untuk request API...")

    time.sleep(5)
    
    # 1. Dapatkan semua cookies dari Selenium
    selenium_cookies = driver.get_cookies()
    
    # Format ke dictionary agar mudah dipakai oleh module `requests`
    request_cookies = {}
    for cookie in selenium_cookies:
        request_cookies[cookie['name']] = cookie['value']

    # 2. Dapatkan User-Agent dari browser Selenium
    user_agent = driver.execute_script("return navigator.userAgent;")

    print("[LOGIN] Selesai & Berhasil mengambil session.")
    
    # Return dictionary cookies dan string User-Agent
    return {
        "cookies": request_cookies,
        "user_agent": user_agent
    }

    # Setelah selesai setup akun baru, lanjut cek/verif domain


def verif_domain(driver):
    time.sleep(3)
    wait = WebDriverWait(driver, 10)
    print("[VERIF DOMAIN] Memulai verifikasi domain...")

    driver.get("https://admin.google.com/")

    # Klik link Verify (dibatasi hanya di dalam alert banner verifikasi domain)
    verify_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[@data-analytics-id='DOMAINVERIFY']//a[@jsname='hSRGPd']"
        ))
    )
    verify_link.click()
    print("[VERIF DOMAIN] Klik link Verify.")

    # Tutup tab lama, pindah ke tab baru
    time.sleep(2)
    original_window = driver.window_handles[0]
    new_window = driver.window_handles[-1]
    driver.close()
    driver.switch_to.window(new_window)
    print("[VERIF DOMAIN] Pindah ke tab baru.")

    # Tunggu "Let's set up your domain"
    wait_for_text(driver, "set up your domain")
    print("[VERIF DOMAIN] Halaman setup domain muncul.")

    time.sleep(0.5)

    # Klik "Get started"
    get_started_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@jsname='V67aGc' and text()='Get started']/.."))
    )
    get_started_btn.click()
    print("[VERIF DOMAIN] Klik 'Get started'.")

    # 1. Tunggu sampai ada text "To automatically" di halaman
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//*[contains(text(), 'To automatically')]")
    ))

    # 2. Sleep 0.5
    time.sleep(0.5)

    # 3. Klik tombol "Other verification options"
    btn_other_verification = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[contains(text(), 'Other verification options')]/ancestor::button")
    ))
    btn_other_verification.click()

    # 4. Tunggu sampai ada text "Your organization will be able"
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//*[contains(text(), 'Your organization will be able')]")
    ))

    # 5. Sleep 0.5
    time.sleep(0.5)

    # 6. Klik tombol "Continue"
    btn_continue = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[contains(text(), 'Continue')]/ancestor::button")
    ))
    btn_continue.click()

    time.sleep(0.5)

    try:
        # Klik checkbox "Code entry complete"
        label = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//label[contains(., 'Come back here and confirm once you have updated the code on your domain host')]"
                )
            )
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            label
        )
        time.sleep(0.5)
        label.click()
    except Exception:
        print("[VERIF DOMAIN] Checkbox 'Code entry complete' tidak muncul.")

    time.sleep(0.5)

    checkbox = driver.find_element(
        By.XPATH,
        "//input[@aria-label='Code entry complete']"
    )
    print("selected =", checkbox.is_selected())

    confirm_btn = driver.find_element(
        By.XPATH,
        "//button[.//span[normalize-space()='Confirm']]"
    )
    print("disabled =", confirm_btn.get_attribute("disabled"))

    # Klik "Confirm"
    try:
        confirm_btn = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@jsname='V67aGc' and text()='Confirm']/.."))
        )
        confirm_btn.click()
        print("[VERIF DOMAIN] Klik 'Confirm'.")
    except Exception:
        confirm_btn = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[.//span[text()='Confirm']]")
            )
        )
        driver.execute_script("""
        arguments[0].scrollIntoView({block:'center'});
        arguments[0].click();
        """, confirm_btn)

    # Tunggu "Your domain is verified!" dengan while True
    print("[VERIF DOMAIN] Menunggu verifikasi domain selesai...")
    while True:
        if "Your domain is verified!" in driver.page_source:
            print("[VERIF DOMAIN] Domain berhasil diverifikasi!")
            break
        time.sleep(2)

    time.sleep(0.5)
    print("[VERIF DOMAIN] Selesai.")

def verify_domain_with_requests(session_data, domain_name, customer_id):
    print("[API] Memulai verifikasi domain via API Requests...")
    
    session = requests.Session()
    session.cookies.update(session_data["cookies"])
    
    headers = {
        "User-Agent": session_data["user_agent"],
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "X-Same-Domain": "1",
        "Origin": "https://workspace.google.com",
        "Referer": "https://workspace.google.com/u/0/getsetup"
    }

    # 1. SCRAPE TOKEN DARI HALAMAN SETUP AWAL
    setup_url = "https://workspace.google.com/u/0/getsetup"
    print("[API] Membaca dashboard untuk mencari Token...")
    resp = session.get(setup_url, headers=headers)
    
    at_token_match = re.search(r'"(AD3Kn[a-zA-Z0-9_\-\%]+:[0-9]+)"', resp.text)
    f_sid_match = re.search(r'"f\.sid","(-?[0-9]+)"', resp.text)
    bl_match = re.search(r'"bl","([^"]+)"', resp.text)
    
    if not at_token_match:
        print("[API] Gagal mendapatkan XSRF Token ('at'). Tidak bisa lanjut.")
        # Coba fallback scrape dari URL /domain/verification/status
        resp2 = session.get("https://workspace.google.com/u/0/getsetup/domain/verification/status", headers=headers)
        at_token_match = re.search(r'"(AD3Kn[a-zA-Z0-9_\-\%]+:[0-9]+)"', resp2.text)
        if not at_token_match:
            return False
            
    at_token = at_token_match.group(1)
    f_sid = f_sid_match.group(1) if f_sid_match else "-123456789"
    bl_version = bl_match.group(1) if bl_match else "boq_dasher-growth-unified-setup-frontend"
    
    print(f"[API] Token didapat! at: {at_token[:10]}... f.sid: {f_sid}")

    post_headers = headers.copy()
    post_headers["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"
    base_post_url = "https://workspace.google.com/u/0/_/DasherGrowthUnifiedSetupUi/data/batchexecute"
    req_id_counter = random.randint(100000, 900000)

    def send_rpc(rpcid, inner_array_data, source_path, envelope_flag="generic"):
        nonlocal req_id_counter
        req_id_counter += 100000 # increment simulasi
        
        inner_str = json.dumps(inner_array_data)
        f_req = [[ [rpcid, inner_str, None, envelope_flag] ]]
        
        data = {
            "f.req": json.dumps(f_req, separators=(',', ':')),
            "at": at_token
        }
        params = {
            "rpcids": rpcid,
            "source-path": source_path,
            "f.sid": f_sid,
            "bl": bl_version,
            "_reqid": str(req_id_counter),
            "rt": "c"
        }
        
        print(f"[API] -> Mengirim RPC {rpcid} (source: {source_path})")
        res = session.post(base_post_url, headers=post_headers, params=params, data=data)
        if res.status_code != 200:
            print(f"[API] Error {res.status_code} pada {rpcid}")
        return res

    # Eksekusi State Machine berurutan:
    
    # RPC 1: mm0hqc
    send_rpc("mm0hqc", 
             [[domain_name, None, None, None, customer_id, "student"]],
             "/u/0/getsetup")
    time.sleep(1)
    
    # RPC 2: Oh9ldf
    send_rpc("Oh9ldf", 
             [[domain_name, None, None, None, customer_id], 2],
             "/u/0/getsetup")
    time.sleep(1)

    # RPC 3: mjixe
    send_rpc("mjixe", 
             [None, [domain_name, None, None, None, customer_id, "student"]],
             "/u/0/getsetup/domain/verification/entri")
    time.sleep(1)

    # RPC 4: HJ9Qad
    send_rpc("HJ9Qad", 
             [2, None, [domain_name, None, None, None, customer_id, "student"], 1],
             "/u/0/getsetup/domain/verification/status")
    time.sleep(1)

    # RPC 5: wVC6Yb (Init, flag "1")
    send_rpc("wVC6Yb", 
             [[domain_name, None, None, None, customer_id], None, None, 0],
             "/u/0/getsetup/domain/verification/status", 
             envelope_flag="1")
    time.sleep(1)

    # RPC 6: wVC6Yb (Confirm, flag "generic")
    res_final = send_rpc("wVC6Yb", 
                         [[domain_name, None, None, None, customer_id], None, None, 0],
                         "/u/0/getsetup/domain/verification/confirmation")
    
    if "wrb.fr" in res_final.text and "wVC6Yb" in res_final.text:
        # Cek apakah ada error array misal "e", 4, 107
        if "107" in res_final.text and "[\"e\"" in res_final.text:
             print("[API] GAGAL: Masih mendeteksi Error 107 (State Invalid/Out of sequence).")
             print(res_final.text[:500])
             return False
        else:
             print("[API] SUKSES: Verifikasi domain berhasil dikirim tanpa Error 107.")
             return True
    else:
        print("[API] Kemungkinan gagal, format balikan tidak dikenali.")
        print(res_final.text[:500])
        return False

def manage_google(driver):
    try:
        # Asumsi: Akun sudah dalam keadaan login sebelum script ini dijalankan
        # (Anda mungkin perlu menambahkan fungsi login Google di sini jika script berjalan dari nol)

        # 1. Buka myaccount.google.com
        print("Membuka Google Account...")
        driver.get("https://myaccount.google.com/")

        # Tunggu sampai teks "Wallet & subscriptions" muncul di page source.
        WebDriverWait(driver, 30).until(lambda d: "Wallet & subscriptions" in d.page_source)
        time.sleep(0.5)

        # ==========================================================
        # BAGIAN 1: RECOVERY PHONE & EMAIL
        # ==========================================================
        print("Membuka Recovery Options...")
        driver.get("https://myaccount.google.com/signinoptions/recoveryoptions")

        # Tunggu halaman terbuka (misal tunggu text Recovery atau elemen tertentu)
        WebDriverWait(driver, 30).until(lambda d: "Recovery" in d.page_source)
        time.sleep(0.5)

        # --- A. EDIT RECOVERY PHONE ---
        print("Mengedit Recovery Phone...")
        # Klik Edit recovery phone. (Tombol Pr7Yme berdasarkan aria-label)
        el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Edit recovery phone.']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(0.5)
        el.click()
        time.sleep(0.5)

        # Isi Nomor HP
        phone_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='tel']"))
        )
        phone_input.clear()
        phone_input.send_keys(PHONE)
        time.sleep(0.5)

        # Klik Save recovery phone
        el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Save your recovery phone']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(0.5)
        el.click()
        time.sleep(0.5)

        # Tunggu sampai tombol "Remove recovery phone" muncul sebagai tanda save sukses
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Remove recovery phone.']"))
        )
        print("Recovery Phone berhasil disimpan.")
        time.sleep(0.5)

        # --- B. EDIT RECOVERY EMAIL ---
        print("Mengedit Recovery Email...")
        # Klik Edit recovery email
        el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Edit recovery email.']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(0.5)
        el.click()
        time.sleep(0.5)

        # Isi Email
        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
        )
        email_input.clear()
        email_input.send_keys(EMAIL)
        time.sleep(0.5)

        # Klik Save recovery email (Tombol Save)
        el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Save your recovery email.']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(0.5)
        el.click()
        time.sleep(0.5)

        # Tunggu sampai tombol "Remove recovery email." muncul
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Remove recovery email.']"))
        )
        print("Recovery Email berhasil disimpan.")
        time.sleep(0.5)

        # --- C. VERIFIKASI RECOVERY EMAIL ---
        print("Mengirim kode verifikasi ke Recovery Email...")
        # Klik Edit recovery email lagi (atau tombol verify/send code, sesuai pseudo-code Anda)
        el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Edit recovery email.']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(0.5)
        el.click()
        time.sleep(0.5)

        # Tunggu input email muncul lagi
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
        )
        time.sleep(0.5)

        # Klik Send code (Tombol Send a code to your recovery email.)
        el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Send a code to your recovery email.']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(0.5)
        el.click()
        time.sleep(0.5)

        # Tunggu input kode verifikasi (inputmode="numeric")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@inputmode='numeric' or @aria-label='Verification code.']"))
        )
        time.sleep(0.5)

        # Meminta user input kode secara manual di terminal
        print(f"\n[ACTION REQUIRED] Silakan cek email {EMAIL} untuk mendapatkan 6 digit kode.")
        input("Tekan ENTER di terminal ini JIKA Anda SUDAH memasukkan kode di browser... !!! ")
        time.sleep(0.5)

        # Klik Verify (Verify the code sent to your recovery email.)
        el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Verify the code sent to your recovery email.']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(0.5)
        el.click()

        print("Menunggu proses verifikasi email...")
        time.sleep(2)

        # Klik Back (Back to previous page)
        el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Back to previous page']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(0.5)
        el.click()
        time.sleep(0.5)

        # Tunggu text "Security & sign-in"
        WebDriverWait(driver, 30).until(lambda d: "Security & sign-in" in d.page_source)
        time.sleep(0.5)
        print("Verifikasi Recovery Email selesai.")


        # ==========================================================
        # BAGIAN 2: CHANGE PASSWORD
        # ==========================================================
        print("Membuka halaman Ganti Password...")
        # Klik link Google password (jsname="xoE0jb" atau href mengandung password)
        password_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@jsname='xoE0jb' and contains(@href, 'password')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", password_link)
        time.sleep(0.5)
        password_link.click()

        time.sleep(0.5)

        # Note: Google biasanya akan meminta input password lama lagi di sini.
        # Asumsi dalam pseudo code Anda, halaman langsung menuju form password baru
        WebDriverWait(driver, 30).until(lambda d: "Password strength:" in d.page_source)
        time.sleep(0.5)

        # Isi password baru (input dengan name="password")
        print("Mengisi form password baru...")
        new_pwd_input1 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
        )
        new_pwd_input1.clear()
        new_pwd_input1.send_keys(NEW_PASSWORD)
        time.sleep(0.5)

        # Konfirmasi password baru (input dengan name="confirmation_password")
        new_pwd_input2 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='confirmation_password']"))
        )
        new_pwd_input2.clear()
        new_pwd_input2.send_keys(NEW_PASSWORD)
        time.sleep(0.5)

        # Klik tombol Change password (type="submit")
        submit_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and .//span[text()='Change password']]"))
        )
        submit_btn.click()
        time.sleep(0.5)

        # Tunggu sampai diarahkan kembali ke "Security & sign-in"
        WebDriverWait(driver, 30).until(lambda d: "Security & sign-in" in d.page_source)
        print("\n[DONE] Password berhasil diubah.")

    except Exception as e:
        print(f"\n[ERROR] Terjadi kesalahan: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Menahan browser agar bisa diperiksa...")
        time.sleep(1000)
        driver.quit()

def main():
    driver = init_driver()
    try:
        session_data = login(driver)
         # Contoh pemanggilan fungsi verifikasi via request
        domain = variabel_domain  # Misal "@example.com"
        customer_id = "04eequ7l"
        
        verify_domain_with_requests(session_data, domain, customer_id)
        # manage_google(driver)
        print("\n[DONE] Semua proses selesai.")
    except Exception as e:
        print(f"\n[ERROR] Terjadi kesalahan: {e}")
        import traceback
        traceback.print_exc()
    finally:
        time.sleep(10000)
        # driver.quit()


if __name__ == "__main__":
    main()
