# Yoisaki Kanade on **NoneBot**
为了让走走多休息而开发的替身机器人（并不是）。

## 简介
基于[NoneBot](https://github.com/nonebot/nonebot)和[NapCatQQ](https://github.com/NapNeko/NapCatQQ)开发的群机器人。

## 基本功能
- 查常用链接
    - `.l[LinkNum]`
    - `LinkNum`：需要获取的链接序号
- 查实时汇率
    - `.汇率` `。汇率`
- 算价格
    - `.y [price] ([point] [where])`
    - `price`：需要计算的价格。必须参数
    - `point`：需要均摊的点数。非必须参数，默认值为1
    - `where`：计算均摊时使用的价格。如使用则必须有`point`参数，默认值为1
- 查煤炉
    - `.m [mNum] ([point] [where])`
    - `mNum`：需要查询的商品ID，或带有ID的链接
    - `point` `where`参数同上
- 更多开发中...


## 娱乐功能
- 对话
    - `@bot [关键词]`
- 戳一戳
    - 即拍一拍，双击头像可触发
- 更多开发中...


## 说明
代码目录下有`/plugins/Config/`文件夹，用于存放配置文件