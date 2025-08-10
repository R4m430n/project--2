# buildozer.spec for "Zamonaviy Kalkulyator"
# Save this file as buildozer.spec in the same folder as your main .py and .kv files
# Edit package.name, package.domain, version, and any file names (icon/presplash) to match your project.

[app]
# (str) Title of your application
title = Zamonaviy Kalkulyator

# (str) Package name (no spaces, use lowercase)
package.name = zm_kalkulyator

# (str) Package domain (reverse DNS style)
package.domain = org.example

# (str) Source dir where your main.py lives
source.dir = .

# (list) Source file extensions to include
source.include_exts = py,kv,png,jpg,atlas,ttf,otf

# (str) Application versioning (x.y.z)
version = 1.0.0

# (str) Orientation: portrait, landscape or all
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (str) Presplash & icon files (place appropriate png in project root)
presplash.filename = presplash.png
icon.filename = icon.png

# (str) Supported platforms - keep default
# (keep blank to use default android)

# (list) Application requirements
# Pick versions carefully: kivy 2.1.0 is stable for many KivyMD versions.
# If you encounter compatibility issues, try pinning kivymd to a commit or version that matches kivy.
requirements = python3,kivy==2.1.0,kivymd

# (str) Supported orientation for python-for-android
# (leave blank if orientation above is enough)

# (int) Minimum API your app will support
# Android API 33 (Android 13) is a safe modern default. Adjust if required.
android.api = 33


[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if running as root
warn_on_root = 1

# (str) Path for bin folder and .buildozer
#build_dir = ./.buildozer


[python]
# (str) Python version selection for the build
# Use python3 (p4a will pick a supported hostpython). If you need a specific hostpython, set hostpython explicitly.
#hostpython = python3


[android]
# (int) Android API to build against (same as android.api above)
android.api = 33

# (str) Android NDK version. Common stable choice is 23b or 25b depending on p4a compatibility.
# If you run into NDK errors, try switching between 23b and 25b. Example: android.ndk = 23b
android.ndk = 23b

# (int) Android NDK API (lowest Android API you want to support when building native code)
android.ndk_api = 21

# (str) Specify architecture(s) to build for. Use both ARM and ARM64 for wider device support.
android.arch = armeabi-v7a,arm64-v8a

# (list) Permissions your app needs
# Calculator doesn't require network, but VIBRATE is often useful for button haptics
android.permissions = VIBRATE

# (str) Android entrypoint and app module (usually default)
#android.entrypoint = org.kivy.android.PythonActivity
#android.apptitle = Zamonaviy Kalkulyator

# (str) Android extra gradle dependencies (if needed). Keep empty for this project.
#android.gradle_dependencies = 

# (str) Additional Java .jars to add
#android.add_jars = 

# (str) Java sources to add (deprecated in many cases)
#android.add_src = 

# (str) Choose p4a branch; 'master' often works, but pinning to a stable release may help reproducible builds
p4a.branch = master

# (bool) Copy libraries instead of using ndk's default linking
#android.copy_libs = 1


[app:package]
# (str) If you need to include additional data files or folders, list them here
# For example: source.include_patterns = assets/*, data/*.json
source.include_patterns = assets/*, locales/*


[buildozer:android]
# (str) Additional requirements for the distribution (if you need e.g. pillow, requests)
# You can extend requirements like: requirements = python3,kivy==2.1.0,kivymd,Pillow


# ----------------------------------
# Helpful build notes (not part of spec parsing):
# ----------------------------------
# 1) Put this buildozer.spec in the same folder as your main.py (or change source.dir accordingly).
# 2) Ensure you have Java JDK, Android SDK, Android NDK and Cython installed. On Ubuntu you can use
#    apt to install openjdk-11-jdk and then follow Buildozer docs for SDK/NDK installation (buildozer will help download many components automatically).
# 3) Recommended build steps (Ubuntu):
#    - sudo apt update && sudo apt install -y python3-pip python3-venv openjdk-11-jdk git
#    - python3 -m pip install --user buildozer
#    - pip install --user cython
#    - buildozer init
#    - Replace the created buildozer.spec with this file (or merge changes).
#    - buildozer -v android debug
# 4) If you hit NDK/SDK issues, try changing android.ndk between 23b and 25b, or pin p4a.branch to a recent stable tag.
# 5) If using KivyMD, ensure the versions are compatible. If you see UI errors, try:
#    requirements = python3,kivy==2.1.0,kivymd==1.1.1
#    (or pin to the kivymd commit known to work with the kivy version)
# 6) To build a release-ready APK/AAB, follow buildozer docs to sign the app (key.jks) and run:
#    buildozer android release
# 7) Place icon.png and presplash.png in the project root (recommend size: icon 192x192 and presplash 1280x720 or larger).

# End of file
