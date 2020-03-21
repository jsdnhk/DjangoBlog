# Docker 支持

## 使用 docker-compose 快速搭建開發環境（MySQL / Memcached）

我們提供了 `dev-environment-setup.yml` 用於快速搭建開發環境。

```shell script
docker-compose -f ./docker-support/dev-environment-setup.yml up
```

運行這條命令後，可以快速搭建起以下環境：

- MySQL 5.7 - 端口 `3306`，用戶名 `root`，密碼 `djangoblog_123`，自動以 UTF8MB4 編碼創建 `djangoblog` 數據庫
- Memcached - 端口 `11211`

## 構建鏡像

```shell script
docker build -f .\docker-support\Dockerfile -t <你的 Docker Hub 用戶名>/django_blog:latest .
```

## 運行自定義指令（例如數據庫遷移）

```shell script
docker run -it --rm <你的 Docker Hub 用戶名>/django_blog:latest <指令>
```

例如：

```shell script
docker run -it --rm -e DJANGO_MYSQL_HOST=192.168.231.50 django_blog/django_blog:latest makemigrations
docker run -it --rm -e DJANGO_MYSQL_HOST=192.168.231.50 django_blog/django_blog:latest migrate
docker run -it --rm -e DJANGO_MYSQL_HOST=192.168.231.50 django_blog/django_blog:latest createsuperuser
```

## 環境變量清單

| 環境變量名稱              | 默認值                                                                     | 備註                                                                                           |
|---------------------------|----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| DJANGO_DEBUG              | False                                                                      |                                                                                                |
| DJANGO_SECRET_KEY         | DJANGO_BLOG_CHANGE_ME                                                      | 請務必修改，建議[隨機生成](https://www.random.org/passwords/?num=5&len=24&format=html&rnd=new) |
| DJANGO_MYSQL_DATABASE     | djangoblog                                                                 |                                                                                                |
| DJANGO_MYSQL_USER         | root                                                                       |                                                                                                |
| DJANGO_MYSQL_PASSWORD     | djangoblog_123                                                             |                                                                                                |
| DJANGO_MYSQL_HOST         | 127.0.0.1                                                                  |                                                                                                |
| DJANGO_MYSQL_PORT         | 3306                                                                       |                                                                                                |
| DJANGO_MEMCACHED_ENABLE   | True                                                                       |                                                                                                |
| DJANGO_MEMCACHED_LOCATION | 127.0.0.1:11211                                                            |                                                                                                |
| DJANGO_BAIDU_NOTIFY_URL   | http://data.zz.baidu.com/urls?site=https://www.example.org&token=CHANGE_ME | 請在[百度站長平臺](https://ziyuan.baidu.com/linksubmit/index)獲取接口地址                      |
| DJANGO_EMAIL_TLS          | False                                                                      |                                                                                                |
| DJANGO_EMAIL_SSL          | True                                                                       |                                                                                                |
| DJANGO_EMAIL_HOST         | smtp.example.org                                                           |                                                                                                |
| DJANGO_EMAIL_PORT         | 465                                                                        |                                                                                                |
| DJANGO_EMAIL_USER         | SMTP_USER_CHANGE_ME                                                        |                                                                                                |
| DJANGO_EMAIL_PASSWORD     | SMTP_PASSWORD_CHANGE_ME                                                    |                                                                                                |
| DJANGO_ADMIN_EMAIL        | admin@example.org                                                          |                                                                                                |
| DJANGO_WEROBOT_TOKEN      | DJANGO_BLOG_CHANGE_ME                                                      | 請使用自己的微信公衆號通信令牌（Token）                                                        |