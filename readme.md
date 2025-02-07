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
    - 普通查询：`.m [mNum] ([point] [where])`
    - `mNum`：需要查询的商品ID，或带有ID的链接
    - `point` `where`参数同上
    - 功能更强大的查询：`.mm [mNum]`
        - 带有简介和机器翻译结果
- 查卡
    - 查略缩图：`.findcard [角色名]` 或 `.查卡 [角色名]`
        - `[角色名]`可以使用昵称，下同
    - 大图：`.card [cardID]`
        - 也可以使用 `.cardnn [角色名] [卡面别名]`
        - 例：`.card 541` 和 `.cardnn knd 原宿` 都会有同样的结果
    - 其他：
        - 更新卡面数据：`.cardupdate`
        - 添加角色昵称：`.addcharann [角色名] [角色昵称]` 或 `.昵称 [角色名] [角色昵称]` 
            - 注：此处的`[角色名]`必须为标准角色名缩写
        - 添加卡面昵称： `.addcardnn [角色名] [卡面别名] [cardID]` 或 `.柄图 [角色名] [卡面别名] [cardID]`

        

- 更多开发中...


## 娱乐功能
- 对话
    - `@bot [关键词]`
- 戳一戳
    - 即拍一拍，双击头像可触发
- 更多开发中...


## 说明
- 代码目录下有`/plugins/Config/`文件夹，用于存放配置文件（bot自有配置文件，不会公开）
- 代码目录下有`/Database/`文件夹，用于存放代码运行中需要的数据库文件
- 代码目录下有`/Temp/`文件夹，用于存放公共配置文件（非bot自有，来源于互联网的数据整理而得）和图片缓存