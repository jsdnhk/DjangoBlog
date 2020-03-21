# 主要功能配置介紹:

## 緩存：
緩存默認使用`memcache`緩存，如果你沒有`memcache`環境，則將`settings.py`中的`locmemcache`改爲`default`,並刪除默認的`default`配置即可。
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'django_test' if TESTING else 'djangoblog',
        'TIMEOUT': 60 * 60 * 10
    },
    'locmemcache': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 10800,
        'LOCATION': 'unique-snowflake',
    }
}
```
## oauth登錄:

現在已經支持QQ，微博，Google，GitHub，Facebook登錄，需要在其對應的開放平臺申請oauth登錄權限，然後在  
**後臺->Oauth** 配置中新增配置，填寫對應的`appkey`和`appsecret`以及回調地址。  
### 回調地址示例：
qq：http://你的域名/oauth/authorize?type=qq  
微博：http://你的域名/oauth/authorize?type=weibo  
type對應在`oauthmanager`中的type字段。

## owntracks：
owntracks是一個位置追蹤軟件，可以定時的將你的座標提交到你的服務器上，現在簡單的支持owntracks功能，需要安裝owntracks的app，然後將api地址設置爲:
`你的域名/owntracks/logtracks`就可以了。然後訪問`你的域名/owntracks/show_dates`就可以看到有經緯度記錄的日期，點擊之後就可以看到運動軌跡了。地圖是使用高德地圖繪製。

## 郵件功能：
同樣，將`settings.py`中的`ADMINS = [('liangliang', 'liangliangyy@gmail.com')]`配置爲你自己的錯誤接收郵箱，另外修改:
```python
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = os.environ.get('DJANGO_EMAIL_USER')
```
爲你自己的郵箱配置。

## 微信公衆號
集成了簡單的微信公衆號功能，在微信後臺將token地址設置爲:`你的域名/robot` 即可，默認token爲`lylinux`，當然你可以修改爲你自己的，在`servermanager/robot.py`中。
然後在**後臺->Servermanager->命令**中新增命令，這樣就可以使用微信公衆號來管理了。  
## 網站配置介紹  
在**後臺->BLOG->網站配置**中,可以新增網站配置，比如關鍵字，描述等，以及谷歌廣告，網站統計代碼及備案號等等。  
其中的*靜態文件保存地址*是保存oauth用戶登錄的頭像路徑，填寫絕對路徑，默認是代碼目錄。
## 代碼高亮
如果你發現你文章的代碼沒有高亮，請這樣書寫代碼塊:  

![](https://resource.lylinux.net/image/codelang.png)  


也就是說，需要在代碼塊開始位置加入這段代碼對應的語言。

## update
如果你發現執行數據庫遷移的時候出現如下報錯：
```python
django.db.migrations.exceptions.MigrationSchemaMissing: Unable to create the django_migrations table ((1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '(6) NOT NULL)' at line 1"))
```
可能是因爲你的mysql版本低於5.6，需要升級mysql版本>=5.6即可。
