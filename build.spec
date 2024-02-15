[app]

# (str) Title of your application
title = SelfPaceLearning

# (str) Package name
package.name = selfpacelearning

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py lives
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
requirements = python3,kivy

# (str) Android entry point, default is okay for Kivy-based app
android.entrypoint = org.renpy.android.PythonActivity

# (str) Android app theme, default is okay for Kivy-based app
android.app_theme = @android:style/Theme.NoTitleBar

# (list) Pattern to whitelist for the whole project
android.whitelist = ./*

# (str) Android NDK version to use
android.ndk = 21.4.7075529

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK version to use
android.sdk = 27

# (int) Minimum API your APK will support.
android.minapi = 21

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Default orientation if not specified
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY
