# apkpuller
A tool for extracting (Splitted) APK files from installed applications on Android devices. It automates the boring stuff when performing mobile penetration testing, especially for static analysis.

## Features
1. Automatic pulling of installed apk
2. Support pulling splitted apk
3. It make life easier haha

## Usage
```
% python apkpuller.py -h
usage: apkpuller.py [-h] [-o OUTPUT] [-p PACKAGE]

Extracting installed apk from android device

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Custom output folder(default to packagename/*.apk)
  -p PACKAGE, --package PACKAGE
                        Specify package to pull(default will lis all package)
```

- You can run the app without specifying -o/--output and -p/--package, and the app will display an interactive dialog:

```
% python apkpuller.py
Fetching list of installed packages...
Select a package to pull the APK:
1. com.amazon.mShop.android.shopping
2. icu.nullptr.applistdetector
3. com.example.app
4. com.logame.eliminateintruder3d
5. com.crazy.juicer.xm
6. qsrv.ainfld

Enter the number of the package: 3
Pulling base APK: com.example.app/base.apk
Base APK pulled successfully: com.example.app/base.apk
Pulling split APK: com.example.app/split_config.arm64_v8a.apk
Split APK pulled successfully: com.example.app/split_config.arm64_v8a.apk
Pulling split APK: com.example.app/split_config.xxhdpi.apk
Split APK pulled successfully: com.example.app/split_config.xxhdpi.apk
```

- If you know the package name, you can specify it directly with -p/--package. This will bypass the interactive dialog:

```
% python apkpuller.py -p com.example.app
Pulling base APK: com.example.app/base.apk
Base APK pulled successfully: com.example.app/base.apk
Pulling split APK: com.example.app/split_config.arm64_v8a.apk
Split APK pulled successfully: com.example.app/split_config.arm64_v8a.apk
Pulling split APK: com.example.app/split_config.xxhdpi.apk
Split APK pulled successfully: com.example.app/split_config.xxhdpi.apk
```

- If you'd like to specify a custom output folder, simply use the -o/--output option:

```
% python apkpuller.py -p com.example.app -o out_dir
Pulling base APK: out_dir/base.apk
Base APK pulled successfully: out_dir/base.apk
Pulling split APK: out_dir/split_config.arm64_v8a.apk
Split APK pulled successfully: out_dir/split_config.arm64_v8a.apk
Pulling split APK: out_dir/split_config.xxhdpi.apk
Split APK pulled successfully: out_dir/split_config.xxhdpi.apk
```