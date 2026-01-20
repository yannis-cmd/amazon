[app]

# Informations de l'application
title = Amazon Tracker Pro
package.name = amazontracker
package.domain = org.amazontracker

# Source
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# Version
version = 1.0.0
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/amazon_tracker_mobile.py

# Requirements
requirements = python3,kivy,requests,beautifulsoup4

# Permissions Android
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Orientation
orientation = portrait

# Icône et splash
android.icon = icon.png
android.presplash = presplash.png

# Orientation Lock
orientation = portrait

# Permissions Firebase (optionnel)
android.gradle_dependencies = com.google.firebase:firebase-analytics

# Architecture
android.archs = arm64-v8a,armeabi-v7a

# API Level
android.api = 31
android.minapi = 21
android.ndk = 23b

# Compilateur
android.accept_sdk_license = True

# Gradle
android.gradle_options = org.gradle.jvmargs=-Xmx4096m

# Bootstrap
p4a.bootstrap = sdl2

# Fullscreen
fullscreen = 0

# Dépendances Python
requirements = python3==3.11,kivy==2.2.1,requests==2.31.0,beautifulsoup4==4.12.2

# Orientation
orientation = portrait
osx_requirements = python3.11

# iOS (optionnel)
ios.codesign.allowed = false

# Environnement
log_level = 2

# Modules à inclure
android.add_src = .

# Services
android.services = .

# Notification
android.add_permissions = SEND_SMS,READ_CONTACTS

# Firebase
android.gradle_dependencies = 

# Chemin de sortie
bin_dir = ./bin

# Métadonnées
metadata.author = Development Team
metadata.author.email = support@amazontracker.com
metadata.description = Application de suivi des prix Amazon avec support client
metadata.url = https://amazontracker.com

# Profiler
#android.profiler_startup_delay = 30

# Logique de lancement
#android.logcat_filters = *:S python:D

# Permissions
android.features = android.hardware.screen.portrait

# Métadonnées supplémentaires
android.meta_data = 

# Resources
resources.excludes = tests,docs

# Manifest permissions
#android.manifest_permissions = android.permission.INTERNET,android.permission.ACCESS_NETWORK_STATE

# Compilateur JDK
java.compiler = javac

# Cibles de compilation
android.release_artifact = aab
