使用 `python` 写一个操作 `git`  的命令行工具 `gfix`
可以接收以下参数：

-b --branch 分支名字
-m --message 提交信息

运行后 `gfix -b fix/ca-12345 -m "fix: fix a ui issue"`

1, 可以运行以下git flow

git checkout -b 'fix/ca-12345' (-b 参数传入)
git commit -m ''fix: fix a ui issue" （-m 参数传入）
git push origin fix/ca-12345


2, 打开浏览器 提交pr （使用 playwright 脚本完成）
    2.1,  打开项目的 github pull request 网址
    2.2,  选择合并分支和 合并方向  fix/ca-12345 -> staging
    2.3,  填入 pr title ：“fix: fix a ui issue”
    2.4,  确定按钮

3, done

注意：
本项目使用 poetry new 初始化脚手架
需要有main 函数，方便脚本构建后，在任意地方执行
生成一个项目 gitignore 文件
遵循编码最佳实践，合理拆分代码功能
假如命令为 gfix
为 pyproject.toml 增加调用命令

```
[tool.poetry.scripts]
gfix = "gfix.main:main"
```