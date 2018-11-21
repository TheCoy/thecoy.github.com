# Hexo 博客配置说明

1. Git
    - 安装git
    - 克隆仓库
        ```shell
        git clone git@github.com:TheCoy/thecoy.github.com.git
        ```
    - 切换到deploy分支
2. Node
    - 添加PPA
        ```shell
        curl -sLttps://deb.nodesource.com/setup_8.x | sudo -E bash -
        ```
    - 安装NodeJs和npm, apt-get install nodejs
    - 换源
        ```shell
        npm config set registry https://registry.npm.taobao.org
        ```
3. [Hexo](https://hexo.io/zh-cn/docs/)
    - npm install hexo-cli -g
    - npm install hexo-server
    - npm install hexo-deployer-git --save
4. themes下面的主题需要重新克隆
    - 如[yilia](https://github.com/litten/hexo-theme-yilia.git)