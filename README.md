# linux-in-practice-2nd

실습과 그림으로 배우는 리눅스 구조 개정판 실습 코드입니다. 원 출처는 [저자 힛허브](https://github.com/satoru-takeuchi/linux-in-practice-2nd)입니다.

# 실습 프로그램 실행 환경 작성법

우분투 20.04 실행 환경에서 실습 프로그램을 실행하려면, 다음 명령어를 실행해서 필요한 패키지를 설치하고 사용자 설정을 끝내기 바랍니다.

```console
$ sudo apt update
$ sudo apt install binutils build-essential golang sysstat python3-matplotlib python3-pil 'fonts-nanum*' fio qemu-kvm virt-manager libvirt-clients virtinst jq docker.io containerd libvirt-daemon-system
$ sudo adduser `id -un` libvirt
$ sudo adduser `id -un` libvirt-qemu
$ sudo adduser `id -un` kvm
```
