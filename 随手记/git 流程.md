标准流程（以后直接套）

假设你现在有：

~/Documents/mengjie/学习库/Photonics

想上传到 GitHub。

1. 进入文件夹
cd ~/Documents/mengjie/学习库/Photonics
2. 初始化 Git（只需第一次）
git init
3. 添加文件
git add .
4. 提交
git commit -m "Initial commit"
5. GitHub 创建同名仓库

去 GitHub
：

新建：

Photonics

不要勾选 README。

6. 连接远程仓库
git remote add origin https://github.com/mengjiewang4-maker/Photonics.git
7. 上传
git push -u origin main

完成。

以后更新：

git add .
git commit -m "更新内容"
git push

即可。