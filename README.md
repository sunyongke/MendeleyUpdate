# MendeleyUpdate


更新Mendeley中的文章信息，数据来源为http://dx.doi.org. Mendeley自带的doi更新功能只支持coressref doi的数据查询，
但是很多的中文文章在coressref中查找不到。该脚本可以通过doi.org网站更新文章的信息。


# 依赖
1. python2或者python3
2. 目前支持Mac系统，linux用户需要修改代码中的sqlite文件地址。

# 使用方法
python --doi=10.3969/j.issn.1001-7461.2012.06.33



# 文档

## sqlite数据库文件名

数据库地址： `<<yourEmailAddress>>@www.mendeley.com.sqlite`,
或者 `online.sqlite` if no email address used with Mendeley.

## Mac 系统

数据库地址：
`/Users/<<Your Name>>/Library/Application Support/Mendeley Desktop/`

## windows

1. Windows Vista/Windows 7：`%LOCALAPPDATA%\Mendeley Ltd.\Mendeley Desktop`
2. Windows XP: `C:\Documents and Settings\<<Your Name>>\Local Settings\Application Data\Mendeley Ltd\Mendeley Desktop`

## Linux:
数据库地址：~/.local/share/data/Mendeley Ltd./Mendeley Desktop/
