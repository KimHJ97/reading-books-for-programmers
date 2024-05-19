# 개발 환경 구축

 - 학습 순서
    - 개발 환경 구축하기
    - 안드로이드 스튜디오 설치하기
    - 설치 문제 해결하기
    - 예제 코드 내려받기
 - 테스트 환경 안내
    - 플러터 SDK: 3.3.5
    - 안드로이드 스튜디오: 2021.3.1 Dolphin

<br/>

## 1. MacOS 개발 환경 구축하기

### 1-1. SDK 

 - 공식 사이트: https://www.flutter.dev/get-started/install
```sh
# Documents 폴더로 이동하고, 해당 폴더에 압축파일 해제
cd $HOME/Documents
unzip $HOME/Downloads/flutter_macos_3.30.5-stable.zip

# 쉘 확인
echo $SHELL

# Bash 쉘 사용시: vi ~/.bashrc
vi ~/.zshrc

export PATH="$PATH:/$HOME/Documents/flutter/bin" 
```
<br/>

### 1-2. Xcode 설치

 - 앱 스토어에서 Xcode 설치
```sh
# 설치 완료 후 아래 명령어 실행
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -runFirstLaunch
```
<br/>

### 1-3. 안드로이드 스튜디오 설치

안드로이드 스튜디오 IDE를 설치한 후에 flutter 플러그인을 설치한다.  
 - 공식 홈페이지: https://developer.android.com/studio

<br/>

### 1-4. 설치 문제 해결하기

터미널에서 flutter doctor 명령어를 입력하면, 어떠한 문제가 있는지 확인할 수 있습니다.  
Flutter, Android toolchain은 필수적으로 활성화되어야 하고, MacOS 환경에서 Mac 전용 애플리케이션을 개발하기 위해서는 Xcode도 정상적으로 활성화되어야 합니다.  

<br/>

#### cmdline-tools component is missing 문제 해결

해당 문제는 Android SDK Command Line Tools가 설치되지 않아서 생기는 문제입니다.  
Android Studio IDE에서 클릭을 통해 설치가 가능합니다.  

```
Settings.. > Android SDK
 - Android SDK Command-line Tools 설치
```
<br/>

#### Android license status unknown 문제 해결

안드로디으 스튜디오를 사용하려면 라이센스 동의를 해야합니다.  
아래 명령어를 통해 라이센스 동의를 합니다.  

```sh
flutter doctor --android-licenses
```

