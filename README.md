# 将简书日记迁移到 Day One

很久之前，曾把简书当做一个日记平台，在上面写了很多东西，但后面遗弃了简书，改用 Day One 写日记。

最近想把简书上的日记迁移到 Day One 上，发现简书文章导出的格式和 Day One 的导入格式不一致，没办法直接导入。

于是决定自己用 GitHub Copilot 写一个脚本来完成这个工作。


## 1. 简书导出

简书官方提供了导出功能，可以将所有的文章导出为一个 rar 压缩包，解压后会得到一个 `user-xxx` 文件夹，该文件夹包含多个子文件夹，每个文件夹对应一个简书文集名称，里面保存的是该文集下所有 html 格式的文章。

## 2. 文件格式转换

简书导出的文件是 html 格式，Day One 支持导入的是 [纯文本格式](https://dayoneapp.com/blog/help_guides/importing-data-from-plain-text/) 的 txt 文件，而且这个 txt 文件需要符合一定的格式要求，例如必须包含一个特定格式的 Date 字段。

如果想一次导入多个文件到 Day One 中，还需将这些文件合并成一个 txt 文件，每篇文章都要包含一个 Date 字段，并用 `\n\n` 分隔。

比较蛋疼的一点是，简书导出的 html 文件中并没有 Date 字段，我们只能自己想办法补全 Date，或者简单使用一个固定的日期。

只是如果使用一个固定的日期，那么所有的文章都会显示为同一天的日期，这样就没办法在 Day One 中按日期排序了。

### 2.1 html 转换为 markdown

首先实现一个 html2markdown.py 脚本，用于递归遍历简书导出的文件夹，在当前目录下生成一个 html2markdown 文件夹，里面是将 html 转换为 markdown 的文件，并确保前后文件目录结构一致。

Usage: 

```bash
python html2markdown.py <path_to_jian_shu_exported_folder>
```

### 2.2 合并 markdown 文件

接下来实现一个 merge_markdown.py 脚本，用于将 html2markdown 文件夹中的所有 markdown 文件合并成一个 merged_result.txt 文件，并在每个文件前添加一个 Date 字段。

Usage:
```bash
python merge_markdown.py <path_to_html2markdown_folder>
```

### 3. Day One 导入

前面我为省事，使用了固定日期，这里为了避免导入的简书文章扰乱现有的 Day One 日记，我选择新建一个日记本，专门用来存放这些迁移过来的文章。

将新建的简书日志日记本放到第一个位置，因为 Day One 会默认将第一个日记本作为当前日记本，所以在导入时会自动选择这个日记本。

然后就是常规的 Day One 导入操作了，【文件】->【导入】->【纯文本文件】-> 选择刚刚生成的 merged_result.txt 文件即可。

![](https://raw.githubusercontent.com/tisfeng/ImageBed/main/uPic/ITc0IY.png)