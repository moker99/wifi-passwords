# 用于執行系统命令併獲取其输出
import subprocess
# 用于自動檢測命令输出的编碼，以确保正确解碼
import chardet

def get_saved_wifi_passwords():
    try:
        # 執行命令獲取所有已保存的 WiFi 配置文件名稱
        output_bytes = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
        
        # 使用 chardet 檢測命令输出的編碼
        result = chardet.detect(output_bytes)
        encoding = result['encoding']
        
        # 解碼命令输出為字符串
        output = output_bytes.decode(encoding)
        
        # 打印命令输出以进行調試
        print("Profiles Output:", output)
        
        # 處理輸出，提取所有 WiFi 配置文件名稱
        # 這里假設 "所有使用者設定檔" 是 WiFi 配置文件的前缀
        wifi_profiles = [line.split(':')[1].strip() for line in output.split('\n') if "所有使用者設定檔" in line]
        
        # 打印提取到的 WiFi 配置文件名稱列表
        print("WiFi Profiles:", wifi_profiles)
        
        wifi_passwords = {}
        
        for profile in wifi_profiles:
            try:
                # 對每个配置文件，執行命令獲取其詳細信息和密碼
                # 使用引号以處理包含空格或特殊字符的配置文件名稱
                profile_info = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'])
                
                # 解碼配置文件信息
                profile_info = profile_info.decode(encoding)
                
                # 打印配置文件詳细信息以進行調試
                print(f"Profile Info for {profile}:", profile_info)
                
                # 處理配置文件信息，提取密碼
                profile_info = profile_info.split('\n')
                for line in profile_info:
                    if "金鑰內容" in line:  # "金鑰內容" 是密碼的關鍵字
                        wifi_passwords[profile] = line.split(':')[1].strip()
                        break
            except subprocess.CalledProcessError as e:
                # 打印錯誤信息，如果獲取密碼失敗
                print(f"Error retrieving info for profile {profile}: {e}")

        return wifi_passwords

    except subprocess.CalledProcessError as e:
        # 打印總體錯誤信息，如果獲取配置文件失敗
        print("Error:", e)
        return {}

if __name__ == "__main__":
    # 執行獲取 WiFi 密碼的函数
    passwords = get_saved_wifi_passwords()
    
    if passwords:
        # 打印每个 WiFi 配置文件及其密碼
        for wifi, password in passwords.items():
            print(f'WiFi SSID: {wifi}, Password: {password}')
    else:
        # 如果没有找到任何 WiFi 密碼，打印相應信息
        print("No WiFi passwords found.")
