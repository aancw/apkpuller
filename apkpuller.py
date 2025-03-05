import subprocess
import os 
import argparse

def list_installed_packages():
    # Only list 3rd party app
    result = subprocess.run(['adb', 'shell', 'pm', 'list', 'packages', '-3'], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error listing packages. Make sure ADB is set up correctly.")
        return []
    
    packages = result.stdout.splitlines()
    package_names = [pkg.replace("package:", "") for pkg in packages]
    
    # Filter out system packages, add more package here if needed
    system_package_prefixes = [
        "android.", "com.android", "com.google", "com.miui", 
        "com.qualcomm", "com.xiaomi", "com.mi"
    ]
    
    filtered_packages = [pkg for pkg in package_names if not any(pkg.startswith(prefix) for prefix in system_package_prefixes)]
    
    return filtered_packages

def choose_package(packages):
    print("Select a package to pull the APK:")
    for idx, pkg in enumerate(packages):
        print(f"{idx + 1}. {pkg}")
    
    try:
        choice = int(input("Enter the number of the package: ")) - 1
        if 0 <= choice < len(packages):
            return packages[choice]
        else:
            print("Invalid choice.")
            return None
    except ValueError:
        print("Invalid input.")
        return None

def pull_apk(package_name, output=None):
    
    if output is None:
        output_folder = package_name
    else:
        output_folder = output

    result = subprocess.run(['adb', 'shell', 'pm', 'path', package_name], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Failed to find APK paths for package: {package_name}")
        return
    
    apk_paths = result.stdout.strip().splitlines()
    
    if not apk_paths:
        print(f"No APKs found for package: {package_name}")
        return

    base_apk_path = None
    split_apks = []

    for apk_path in apk_paths:
        apk_path = apk_path.replace("package:", "")

        if "base.apk" in apk_path:
            base_apk_path = apk_path 
        elif "split_config" in apk_path:
            split_apks.append(apk_path)
    
    os.makedirs(f'./{output_folder}', exist_ok=True)

    if base_apk_path:
        base_apk_filename = os.path.basename(base_apk_path)
        print(f"Pulling base APK: {output_folder}/{base_apk_filename}")
        pull_result = subprocess.run(['adb', 'pull', base_apk_path, f'./{output_folder}/{base_apk_filename}'], capture_output=True, text=True)

        if pull_result.returncode == 0:
            print(f"Base APK pulled successfully: {output_folder}/{base_apk_filename}")
        else:
            print(f"Failed to pull base APK: {output_folder}/{base_apk_filename}")
    else:
        print("No base APK found for this package.")
    
    if split_apks:
        for split_apk_path in split_apks:
            split_apk_filename = os.path.basename(split_apk_path)
            print(f"Pulling split APK: {output_folder}/{split_apk_filename}")
            pull_result = subprocess.run(['adb', 'pull', split_apk_path, f'./{output_folder}/{split_apk_filename}'], capture_output=True, text=True)

            if pull_result.returncode == 0:
                print(f"Split APK pulled successfully: {output_folder}/{split_apk_filename}")
            else:
                print(f"Failed to pull split APK: {output_folder}/{split_apk_filename}")
    else:
        print("No split APKs found for this package.")

def main():
    parser = argparse.ArgumentParser(description="Extracting installed apk from android device")
    parser.add_argument('-o', '--output', type=str, help="Custom output folder(default to packagename/*.apk)")
    parser.add_argument('-p', '--package', type=str, help="Specify package to pull(default will lis all package)")
    args = parser.parse_args()

    if args.package:
        if args.output:
            pull_apk(args.package, args.output)
        else:
            pull_apk(args.package)
    else:
        print("Fetching list of installed packages...")
        packages = list_installed_packages()
        
        if not packages:
            print("No packages found.")
            return
        
        package_name = choose_package(packages)
        
        if package_name:
            if args.output:
                pull_apk(package_name, args.output)
            else:
                pull_apk(package_name)

if __name__ == "__main__":
    main()
