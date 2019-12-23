function Prepre-env {
    pip install requests

    mkdir "$(pwd)\dist"
    mkdir "$(pwd)\$env:KIVY_BUILD_DIR"
    if (!(Test-Path "$(pwd)\$env:KIVY_BUILD_CACHE")) {
      mkdir "$(pwd)\$env:KIVY_BUILD_CACHE"
    }
}


function Download-Packages() {
    python -m pip install pip wheel setuptools --upgrade
    python "win/$env:PACKAGE_TARGET.py" build_path "$(pwd)\$env:KIVY_BUILD_DIR" arch $env:PACKAGE_ARCH package $env:PACKAGE_TARGET output "$(pwd)\dist" cache "$(pwd)\$env:KIVY_BUILD_CACHE" download_only "1"
}


function Create-Packages() {
    python -m pip install pip wheel setuptools --upgrade
    python "win/$env:PACKAGE_TARGET.py" build_path "$(pwd)\$env:KIVY_BUILD_DIR" arch $env:PACKAGE_ARCH package $env:PACKAGE_TARGET output "$(pwd)\dist" cache "$(pwd)\$env:KIVY_BUILD_CACHE"
}


function Upload-windows-wheels-to-server($ip) {
    echo "Uploading wheels*:"
    dir "$(pwd)\dist"
    C:\tools\msys64\usr\bin\bash --login -c ".ci/windows-server-upload.sh $ip '$(pwd)\dist' 'kivy_deps.$env:PACKAGE_TARGET`_dev-*' ci/win/deps/$env:PACKAGE_TARGET`_dev/"
    C:\tools\msys64\usr\bin\bash --login -c ".ci/windows-server-upload.sh $ip '$(pwd)\dist' 'kivy_deps.$env:PACKAGE_TARGET-*' ci/win/deps/$env:PACKAGE_TARGET/"
}