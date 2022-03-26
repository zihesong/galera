export ANDROID_SDK_ROOT=/home/zoooe/Android/Sdk
export PATH=$PATH:$ANDROID_SDK_ROOT/build-tools/33.0.0-rc2:$ANDROID_SDK_ROOT/platform-tools:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/emulator



cd workspaces/github/themis/scripts
python3 themis.py --avd themis1 --apk ../APhotoManager/APhotoManager-0.6.4.180314-debug-#116.apk -n 1 --repeat 3 --time 1h -o ../monkey-results/ --monkey 


python3 themis.py --avd themis2 --apk ../AmazeFileManager/AmazeFileManager-3.4.2-#1837.apk -n 1 --repeat 3 --time 30m -o ../monkey-results/ --monkey --offset 1 


python3 themis.py --avd themis3 --apk ../AnkiDroid/AnkiDroid-debug-2.9-#4977.apk -n 1 --repeat 3 --time 30m -o ../monkey-results/ --monkey --offset 2


python3 themis.py --avd themis4 --apk ../Frost/Frost-debug-2.2.1-#1323.apk -n 1 --repeat 3 --time 30m -o ../monkey-results/ --login ../Frost/login.py --monkey --offset 3


python3 themis.py --avd themis5 --apk ../WordPress/WordPress-vanilla-debug--#11135.apk -n 1 --repeat 3 --time 30m -o ../monkey-results/ --login ../WordPress/login-#4026.py --monkey  --offset 4


python3 themis.py --avd themis6 --apk ../nextcloud/nextcloud-#4026.apk -n 1 --repeat 3 --time 30m -o ../monkey-results/ --login ../nextcloud/login-#11135.py --monkey  --offset 5


python3 check_crash.py --monkey -o ../monkey-results/ --app and-bible --id \#697 --simple
0

python3 check_crash.py --monkey -o ../monkey-results/ --app AmazeFileManager --id \#1837 --simple
00100

python3 check_crash.py --monkey -o ../monkey-results/ --app FirefoxLite --id \#4881 --simple
0

python3 check_crash.py --monkey -o ../monkey-results/ --app openlauncher --id \#67 --simple

0
python3 check_crash.py --monkey -o ../monkey-results/ --app AnkiDroid --id \#4977 --simple
48611

python3 check_crash.py --monkey -o ../monkey-results/ --app APhotoManager --id \#116 --simple
29 24 1 3 10

python3 check_crash.py --monkey -o ../monkey-results/ --app commons --id \#2123 --simple
0

python3 check_crash.py --monkey -o ../monkey-results/ --app nextcloud --id \#4026 --simple
00100

python3 check_crash.py --monkey -o ../monkey-results/ --app WordPress --id \#11135 --simple
0
