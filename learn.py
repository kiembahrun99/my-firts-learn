import time
import csv
import requests
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ===================== VARIABEL =====================
link = "https://admin.google.com/ac/home?ecid=C00wa7t59" 
email = "student@goog-test.reseller.gappslabs.co.s-lddnabha.qwiklabs-gsuite.net"
password = "9fec17d4d13b3eaf46b0"
variabel_domain = email.split("@")[1] if "@" in email else ""
variabel_domain = "@" + variabel_domain if variabel_domain else ""
path_file_csv = "/Users/athiyyahzulfa/Documents/ROSYID/Affiliate/ffmpeg/users_updated.csv"
# ====================================================

def direct_verif(driver):
    current_title = driver.title
    print(f"[DIRECT VERIF] Title saat ini: {current_title}")

    if current_title == "Admin Console":
        print("[DIRECT VERIF] Sudah di admin.google.com — skip login, langsung verif_domain.")
        verif_domain(driver)
    else:
        print("[DIRECT VERIF] Belum di admin.google.com — jalankan login dulu.")
        # login(driver)
        verif_domain(driver)

def init_driver():
    driver = Driver(
        uc=True,
        incognito=True,
        locale_code="id-ID",
        no_sandbox=True,
        disable_gpu=True
    )
    driver.maximize_window()
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

    time.sleep(2)  # Tunggu redirect setelah login
    while True:
        current_title = driver.title
        print(f"[LOGIN] Title saat ini: {current_title}")

        if "Admin console" in current_title:
            print("[LOGIN] Berhasil masuk ke Admin Console!")
            verif_domain(driver)
        elif "Selamat datang di akun baru Anda" in driver.page_source:
            print("[LOGIN] Halaman 'Selamat datang' muncul.")
            break
        else:
            print("[LOGIN] Menunggu halaman 'Admin Console' atau 'Selamat datang' muncul...")
            time.sleep(2)

    try:
        # 12. Tunggu "Selamat datang di akun baru Anda"
        wait_for_text(driver, "Selamat datang di akun baru Anda")
        print("[LOGIN] Halaman 'Selamat datang' muncul.")
    except:
        print("[LOGIN] Halaman 'Selamat datang' tidak muncul.")
        direct_verif(driver) 

    # 13. Sleep 0.5
    time.sleep(0.5)

    try:
        # 14. Scroll ke bawah dan klik "Saya mengerti"
        confirm_btn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "confirm"))
        )
        scroll_and_click(driver, confirm_btn)
        print("[LOGIN] Klik 'Saya mengerti'.")
    except:
        print("[LOGIN] Halaman 'Saya mengerti' tidak muncul.")
        direct_verif(driver)

    try:
        # 15. Tunggu "Terms of Service"
        wait_for_text(driver, "Terms of Service")
        print("[LOGIN] Halaman Terms of Service muncul.")
    except:
        print("[LOGIN] Halaman Terms of Service tidak muncul.")
        direct_verif(driver)

    # 16. Sleep 0.5
    time.sleep(0.5)

    try:
        # 17. Scroll ke bawah dan klik "Accept Terms of Service"
        accept_tos = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Accept Terms of Service')]/.."))
        )
        scroll_and_click(driver, accept_tos)
        print("[LOGIN] Klik 'Accept Terms of Service'.")
    except:
        print("[LOGIN] Halaman 'Accept Terms of Service' tidak muncul.")
        direct_verif(driver)

    try:
        # 18. Tunggu "Make Workspace work for you"
        wait_for_text(driver, "Make Workspace work for you")
        print("[LOGIN] Halaman 'Make Workspace work for you' muncul.")
    except:
        print("[LOGIN] Halaman 'Make Workspace work for you' tidak muncul.")
        direct_verif(driver)

    # 19. Sleep 0.5
    time.sleep(0.5)

    try:
        # 20. Klik "Get set up"
        get_setup_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@jsname='V67aGc' and text()='Get set up']/.."))
        )
        get_setup_btn.click()
        print("[LOGIN] Klik 'Get set up'.")
    except:
        print("[LOGIN] Halaman 'Get set up' tidak muncul.")
        direct_verif(driver)

    # 21. Sleep 0.5
    time.sleep(0.5)
    print("[LOGIN] Selesai.")


def verif_domain(driver):
    print("[VERIF DOMAIN] Memulai verifikasi domain...")

    driver.get("https://admin.google.com/")

    # 22. Klik link Verify
    verify_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@jsname='hSRGPd']"))
    )
    verify_link.click()
    print("[VERIF DOMAIN] Klik link Verify.")

    # 23. Tutup tab lama, pindah ke tab baru
    time.sleep(2)
    original_window = driver.window_handles[0]
    new_window = driver.window_handles[-1]
    driver.close()
    driver.switch_to.window(new_window)
    print("[VERIF DOMAIN] Pindah ke tab baru.")

    # 24. Tunggu "Let's set up your domain"
    wait_for_text(driver, "set up your domain")
    print("[VERIF DOMAIN] Halaman setup domain muncul.")

    # 25. Sleep 0.5
    time.sleep(0.5)

    # 26. Klik "Get started"
    get_started_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@jsname='V67aGc' and text()='Get started']/.."))
    )
    get_started_btn.click()
    print("[VERIF DOMAIN] Klik 'Get started'.")

    # 27. Tunggu "Your organization will be able"
    wait_for_text(driver, "Your organization will be able")
    print("[VERIF DOMAIN] Halaman konfirmasi organisasi muncul.")

    # 28. Sleep 0.5
    time.sleep(0.5)

    # 29. Klik "Switch to manual verification"
    try:
        manual_btn = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@jsname='V67aGc' and text()='Switch to manual verification']/.."))
        )
        manual_btn.click()
        print("[VERIF DOMAIN] Klik 'Switch to manual verification'.")
    except:
        continue_btn = WebDriverWait(driver, 4).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[text()='Continue']]")
            )
        )
        continue_btn.click()
        print("[VERIF DOMAIN] Klik 'Continue' (manual verification tidak muncul).")

    # 30. Tunggu "Add verification code"
    wait_for_text(driver, "Add verification code")
    print("[VERIF DOMAIN] Halaman 'Add verification code' muncul.")

    # 31. Sleep 0.5
    time.sleep(0.5)

    try:
        # 32. Klik checkbox "Code entry complete"
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
    except:
        print("[VERIF DOMAIN] Checkbox 'Code entry complete' tidak muncul.")

    # 33. Sleep 0.5
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

    # 34. Klik "Confirm"
    try:
        confirm_btn = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@jsname='V67aGc' and text()='Confirm']/.."))
        )
        confirm_btn.click()
        print("[VERIF DOMAIN] Klik 'Confirm'.")
    except:
        confirm_btn = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[.//span[text()='Confirm']]")
            )
        )

        driver.execute_script("""
        arguments[0].scrollIntoView({block:'center'});
        arguments[0].click();
        """, confirm_btn)

    # 35. Tunggu "Your domain is verified!" dengan while True
    print("[VERIF DOMAIN] Menunggu verifikasi domain selesai...")
    while True:
        if "Your domain is verified!" in driver.page_source:
            print("[VERIF DOMAIN] Domain berhasil diverifikasi!")
            break
        time.sleep(2)

    # 36. Sleep 0.5
    time.sleep(0.5)
    print("[VERIF DOMAIN] Selesai.")


def main():
    driver = init_driver()
    try:
        login(driver)
        # HAPUS panggilan verif_domain(driver) di sini,
        # karena sudah dipanggil di dalam fungsi login() dan direct_verif()
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
