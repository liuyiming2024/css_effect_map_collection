#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每次从上游同步后，重建 README 顶部的版权与来源声明。

设计要点（幂等）：
  1. 总是以「上游 README 原文」为底本，再叠加声明块 —— 上游更新 README 时声明不丢，也不会重复叠加。
  2. 直接重写整个 README.md，因此无论上一轮是什么状态，结果都一致。
"""
import os
import subprocess

UPSTREAM_REF = 'upstream/master'
UPSTREAM_URL = 'https://gitee.com/qm1989/css_effect_map_collection'
AUTHOR_NAME = 'qianming'
AUTHOR_URL = 'https://gitee.com/qm1989'
SEPARATOR_MARK = '以下内容为**原仓库 README 原文'

NOTICE = """> [!IMPORTANT]
> ## 📌 版权与来源声明 / Attribution
>
> 本仓库是 Gitee 开源项目 **[css效果图收集]({origin})** 的**镜像副本**，仅用于学习研究与访问加速。
>
> | 项目 | 信息 |
> | --- | --- |
> | **原项目名称** | css效果图收集（css_effect_map_collection） |
> | **原作者** | [{author}]({author_url})（Gitee ID：`qm1989`） |
> | **原仓库地址** | {origin} |
> | **开源许可证** | [MIT License](./LICENSE) |
> | **版权声明** | Copyright (c) 2021 {author} |
>
> **郑重声明：**
>
> 1. 本仓库内全部代码、图片及文档的著作权均归**原作者 {author}** 所有，镜像者不对其中任何内容主张权利。
> 2. 所有 Git 提交历史均**原样保留**原作者的署名与提交信息，未作任何删改。
> 3. `LICENSE` 文件为原仓库 MIT 许可证原文，`Copyright (c) 2021 {author}` 完整保留。
> 4. 本仓库**仅作单向镜像**，不接受 Issue 与 Pull Request；如需交流或贡献代码，请前往[原仓库]({origin})。
> 5. 若您是原作者且不希望本镜像继续存在，请通过 Issue 告知，本人将立即删除。
>
> ---

"""

SEPARATOR = """
> ⬆️ 以上为镜像声明，由仓库维护者自动添加。以下内容为**原仓库 README 原文，未作任何修改**。

"""


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def main():
    # 1. 取上游 README 原文作为底本
    r = sh(f'git show {UPSTREAM_REF}:README.md')
    if r.returncode == 0 and r.stdout.strip():
        body = r.stdout
        source = 'upstream'
    else:
        # 上游没有 README：剥离当前文件里已存在的声明块，保留正文
        cur = open('README.md', encoding='utf-8').read() if os.path.exists('README.md') else ''
        body = cur.split(SEPARATOR_MARK, 1)[1] if SEPARATOR_MARK in cur else cur
        source = 'local (upstream 无 README)'

    # 2. 叠加声明（声明块在前，原文在后）
    notice = NOTICE.format(origin=UPSTREAM_URL, author=AUTHOR_NAME, author_url=AUTHOR_URL)
    new = notice + SEPARATOR + body.lstrip('\n')

    old = open('README.md', encoding='utf-8').read() if os.path.exists('README.md') else ''
    if new == old:
        print('README 无变化，跳过写入')
        return 0

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new)
    print(f'README 已重建（底本来源: {source}），共 {len(new)} 字符')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
