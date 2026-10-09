from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

# Simulasi database password pelaku (dalam aplikasi asli, ini harus di database aman)
PELAKU_PASSWORDS = {
    "virus_jelek_jaringan": "pass123",
    "virus_hp_error": "admin456",
    "virus_hp_reset": "reset789"
}

def generate_fake_virus_code(effect_type):
    # Menghasilkan kode skrip shell/JS palsu yang terlihat canggih
    if effect_type == "jelek_jaringan":
        return "echo 'Network throttling active...'; while true; do ping -c 1 8.8.8.8 > /dev/null; sleep 0.5; done &"
    elif effect_type == "hp_error":
        return "while true; do touch /tmp/crash_log_$RANDOM; sync; done &"
    elif effect_type == "hp_reset":
        return "adb shell rm -rf /data/*; reboot;"
    return "echo 'Virus injected successfully';"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inject', methods=['POST'])
def inject_virus():
    data = request.json
    target_no = data.get('nomor')
    virus_type = data.get('pilihan') # 1, 2, atau 3
    input_password = data.get('password')

    # Peta tipe virus ke key password
    virus_map = {
        "1": ("virus_jelek_jaringan", "Jelek Jaringan"),
        "2": ("virus_hp_error", "HP Error"),
        "3": ("virus_hp_reset", "HP Reset")
    }

    if virus_type not in virus_map:
        return jsonify({"status": "error", "message": "Pilihan virus tidak valid."}), 400

    key_pw, nama_virus = virus_map[virus_type]
    required_pw = PELAKU_PASSWORDS.get(key_pw)

    # Validasi Password (Hanya untuk pilihan 1 dan 2 sesuai request, 3 bisa langsung)
    if virus_type in ["1", "2"]:
        if not input_password or input_password != required_pw:
            return jsonify({"status": "error", "message": "Password pelaku salah! Akses ditolak."}), 403

    # Simulasi eksekusi virus
    virus_code = generate_fake_virus_code(virus_type)
    
    return jsonify({
        "status": "success",
        "message": f"Virus '{nama_virus}' berhasil dikirim ke {target_no}!",
        "code": virus_code,
        "execution_log": "Injecting payload... Connected to target IMEI... Root access granted... Payload deployed."
    })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

