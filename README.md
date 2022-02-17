# Rin Yuuki (结城凛)


## 简介

**结城凛:** 魔改[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)
的以pcr为主信息聚合推送查询用qq机器人。



## 功能介绍

暂定（

##生产环境配置

**需求**

python3.10+

ffmpeg

debian11/ubuntu20.04LTS

screen

**一些问题的笔记：**

debian乱码

1.启动终端 #apt-get install locales

2.重新配置locale #dpkg-reconfigure locales

3.运行LOCALE命令检查当前的LOCALE环境 #locale

vim /root/.bashrc

export LC_ALL=zh_CN.UTF-8

##部署

sudo apt update

sudo apt upgrade -y

sudo apt install screen ffmpeg git gcc -y

##**python3.10和pip的安装**

sudo add-apt-repository ppa:deadsnakes/ppa 

sudo apt update

sudo apt install python3.10 -y

查看所有python版本 ls -l /usr/bin/python*

sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 2

选择默认版本
sudo update-alternatives --config python3

pip --version 会报错：

ModuleNotFoundError: No module named 'distutils.util'

修复，执行

sudo apt install python3.10-distutils -y

重装 pip

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python3 get-pip.py

以确保为python3.10安装了pip。

(可能需要加sudo)，或者需要在下一步的配置虚拟环境中安装

如果您看到任何权限错误，您可能需要使用

python3 get-pip.py --user

修改pip指向

sudo vi /usr/local/bin/pip3

把第一行/usr/bin/python 换成 python3


##克隆目录并配置venv

git clone https://github.com/oralvi/rinyuuki.git

cd rinyuuki

python3 -m venv rinvenv

若报错加 --without-pip 随后再安装pip

激活环境 source rinvenv/bin/activate

python即可

安装依赖 pip install -r requirements.txt

可能的报错 

sudo apt install python3.10-dev -y

screen 分两个，一个framework，一个rin

随后run.py即可

更新：git pull https://github.com/oralvi/rinyuuki.git --no-rebase

## 友情链接

**干炸里脊资源站**: https://redive.estertion.win/

**公主连结Re: Dive Fan Club - 硬核的竞技场数据分析站**: https://pcrdfans.com/

**yobot**: https://yobot.win/

**隔壁咖啡佬的HoshinoBot**: https://github.com/Ice-Cirno/HoshinoBot

