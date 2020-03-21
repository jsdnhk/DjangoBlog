# DjangoBlog

🌍
*[English](/docs/README-en.md) ∙ [簡體中文](README.md)*

基於`python3.8`和`Django3.0`的博客。   

[![Build Status](https://travis-ci.org/liangliangyy/DjangoBlog.svg?branch=master)](https://travis-ci.org/liangliangyy/DjangoBlog) [![codecov](https://codecov.io/gh/liangliangyy/DjangoBlog/branch/master/graph/badge.svg)](https://codecov.io/gh/liangliangyy/DjangoBlog) [![Requirements Status](https://requires.io/github/liangliangyy/DjangoBlog/requirements.svg?branch=master)](https://requires.io/github/liangliangyy/DjangoBlog/requirements/?branch=master)  [![license](https://img.shields.io/github/license/liangliangyy/djangoblog.svg)]()  

## 主要功能：
- 文章，頁面，分類目錄，標籤的添加，刪除，編輯等。文章及頁面支持`Markdown`，支持代碼高亮。
- 支持文章全文搜索。
- 完整的評論功能，包括髮表回覆評論，以及評論的郵件提醒，支持`Markdown`。
- 側邊欄功能，最新文章，最多閱讀，標籤雲等。
- 支持Oauth登陸，現已有Google,GitHub,facebook,微博,QQ登錄。
- 支持`Memcache`緩存，支持緩存自動刷新。
- 簡單的SEO功能，新建文章等會自動通知Google和百度。
- 集成了簡單的圖牀功能。
- 集成`django-compressor`，自動壓縮`css`，`js`。
- 網站異常郵件提醒，若有未捕捉到的異常會自動發送提醒郵件。
- 集成了微信公衆號功能，現在可以使用微信公衆號來管理你的vps了。

## 安裝
mysql客戶端從`pymysql`修改成了`mysqlclient`，具體請參考 [pypi](https://pypi.org/project/mysqlclient/) 查看安裝前的準備。

使用pip安裝： `pip install -Ur requirements.txt`

如果你沒有pip，使用如下方式安裝：
- OS X / Linux 電腦，終端下執行: 

    ```
    curl http://peak.telecommunity.com/dist/ez_setup.py | python
    curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python
    ```

- Windows電腦：

    下載 http://peak.telecommunity.com/dist/ez_setup.py 和 https://raw.github.com/pypa/pip/master/contrib/get-pip.py 這兩個文件，雙擊運行。 

### 配置
配置都是在 `setting.py` 中，部分配置遷移到了後臺配置中。

很多 `setting` 配置我都是寫在環境變量裏面的.並沒有提交到 `github` 中來.例如`SECRET_KEY`,`OAHUTH`,`mysql`以及郵件部分的配置等.你可以直接修改代碼成你自己的,或者在環境變量裏面加入對應的配置就可以了.

`test`目錄中的文件都是爲了`travis`自動化測試使用的.不用去關注.或者直接使用.這樣就可以集成`travis`自動化測試了.

`bin`目錄是在`linux`環境中使用`Nginx`+`Gunicorn`+`virtualenv`+`supervisor`來部署的腳本和`Nginx`配置文件.可以參考我的文章:

>[DjangoBlog部署教程](https://www.lylinux.net/article/2019/8/5/58.html)

有詳細的部署介紹.


## 運行

 修改`DjangoBlog/setting.py` 修改數據庫配置，如下所示：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangoblog',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'host',
        'PORT': 3306,
    }
}
```

### 創建數據庫
mysql數據庫中執行:
```sql
CREATE DATABASE `djangoblog` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
```

然後終端下執行:
```bash
./manage.py makemigrations
./manage.py migrate
```

**注意：** 在使用 `./manage.py` 之前需要確定你係統中的 `python` 命令是指向 `python 3.6` 及以上版本的。如果不是如此，請使用以下兩種方式中的一種：

- 修改 `manage.py` 第一行 `#!/usr/bin/env python` 爲 `#!/usr/bin/env python3`
- 直接使用 `python3 ./manage.py makemigrations`

### 創建超級用戶

 終端下執行:
```bash
./manage.py createsuperuser
```

### 創建測試數據
終端下執行:
```bash
./manage.py create_testdata
```

### 收集靜態文件
終端下執行:  
```bash
./manage.py collectstatic --noinput
./manage.py compress --force
```

### 開始運行：
執行： `./manage.py runserver`


瀏覽器打開: http://127.0.0.1:8000/  就可以看到效果了。
## 更多配置:
[更多配置介紹](/docs/config.md)

## 問題相關

有任何問題歡迎提Issue,或者將問題描述發送至我郵箱 `liangliangyy#gmail.com`.我會盡快解答.推薦提交Issue方式.  

---
 ## 致大家🙋‍♀️🙋‍♂️
 如果本項目幫助到了你，請在[這裏](https://github.com/liangliangyy/DjangoBlog/issues/214)留下你的網址，讓更多的人看到。
您的回覆將會是我繼續更新維護下去的動力。 

🙏🙏🙏
