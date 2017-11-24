switcher
========

used to get switch infomations , snmp tools 

you can use this tools collect switch infomations every easy.





运维管理说明文档
===

# 主机标注说明：

## 广电机房

### 主机标注说明：

#### DB

| 主机名             | IP 地址                   |  运行服务                |  域名              |       
| :---------------: | :-----------------------:| :---------------------: | :---------------: |
| web 3             |    10.210.1.11           |    mysql 5.7  slave     |                   |
| web 4             |    10.210.1.12            | mysql 5.7 master       |                   |

- - - 

PHP web 主机


|主机名              |     IP 地址                               |        运行服务           |      域名           |  
| :---------------: | :--------------------------------------: | :----------------------: | :----------------: |
| Rock1             | 10.210.1.13,10.10.10.13,211.146.5.32     |   PHP ,python 网站服务     |                   |
| Rock2             | 10.210.1.14,10.10.10.14,211.146.5.33     |   R1 备机                 |                    |
| Rock3             | 10.210.1.15,10.10.10.15                  |   手机客户端web 服务主机     |                   |
| Rock4             | 10.210.1.16，10.10.10.16                 |   手机客户端热备主机         |                   |


Rock1       10.210.1.13,10.10.10.13,211.146.5.32 
| 域名 | 服务 | 开发语言 | 代码物理地址 | 联系人 |
| :--: | :--:| :-----: | :--------: | :----: |
| web.huayingjuhe.com.conf |                项目管理 （新版）                     |  PHP          |  /usr/local/www/website/www | 建华 |
|        secondary.huayingjuhe.com.conf          二级市场                                PHP             /usr/local/www/website/
|            producer.huayingjuhe.com.conf           制片方                                  PHP
|            pro.huayingjuhe.com.conf                项目管理                                PHP
|            dcp.huayingjuhe.com.conf                证书管理(index),数字制作(/project)        PHP
|           mis.huayingjuhe.com.conf                院线管理                                PHP
|            report.hxfilm.com.conf                  原有华夏电影域名，手机端报表                PHP
            ucs.huayingjuhe.com.conf                文件上传部分（戴楠）                      Python
            cinema.huayingjuhe.com.conf             跳转到mis，原先管理页面                   PHP
            bo.cgstheater.cn.conf                   中国巨幕（戴楠）                          Python
            s.huayingjuhe.com.conf                  静态文件服务(戴楠)                        Python
            report.huayingjuhe.com.conf             手机报文服务（老应用）                     PHP
            passport.huayingjuhe.com.conf           统一登录                                PHP
            www.huayingjuhe.com.conf                官网首页                                PHP
            passport.hxfilm.com.conf                支持原有老应用的passport                  PHP
            m.hxfilm.com.conf                       老版手机页面接入域名                       PHP



Rock1 账户以及Crontab

dainan
liutao
scp4file
work
40 1 * * * php /home/work/website/pro/webroot/index.php data_manage create_report_table
40 */6 * * * php /home/work/website/doc/cert_cinema.php
50 * * * * php /home/work/website/doc/project_synchronize.php
10 0 * * * php /home/work/website/doc/cinemas_block.php
30 */6 * * * php /home/work/website/doc/everyday_tools.php
5 * * * * php /home/work/website/doc/cinemas_halls_status.php
* * * * * php /home/work/website/doc/disk_manage_check.php > /dev/null
xiaochen
zhangli



Rock2       10.210.1.14,10.10.10.14,211.146.5.33            php  python 网站服务
            
            ucs.huayingjuhe.com.conf
            secondary.huayingjuhe.com.conf
            report.hxfilm.com.conf
            report.huayingjuhe.com.conf
            producer.huayingjuhe.com.conf
            mis.huayingjuhe.com.conf
            dcp.huayingjuhe.com.conf
            cinema.huayingjuhe.com.conf
            bo.cgstheater.cn.conf
            
            pro.huayingjuhe.com.conf
            s.huayingjuhe.com.conf
            www.huayingjuhe.com.conf
            passport.huayingjuhe.com.conf
            m.hxfilm.com.conf

            mobile.huayingjuhe.com.conf                 新版手机客户端                         PHP 反向代理到 Rock3
            box.huayingjuhe.com.conf                    下载盒子的访问站站点                  Python
            zabbix.conf                                 监控主机zabbix                      php
            ems.com                                     顺风和ems 接收 快递路由地址           php
            wintrans.huayingjuhe.com.conf               下载盒子transform 站点，长链接        Python



用户和crontab
xiaochen
work
liutao
reverse
dainan
均无crontab 

Rock3       10.210.1.15，10.10.10.15 
            devs.huayingjuhe.com                        手机客户端反向代理具体服务主机             PHP         /usr/local/www/issuer


Rock4       10.210.1.16，10.10.10.16
            无服务





midas 主机
_____________________________________________________________________________________________
|主机名              |     IP 地址              |        运行服务           |      域名          |       
|____________________________________________________________________________________________|
| web 1                 10.210.1.17 10.10.10.17|     midas fe,be
|____________________________________________________________________________________________
| web2              |   10.210.1.18，10.10.10.18|    midas fe
|____________________________________________________________________________________________|

web1        10.210.1.17，10.10.10.17
            midas fe,be
用户和crontab

xiaochen
    1 1 * * * /usr/bin/sh /data0/cron/rsync_etl.sh > /dev/null  2>&1
work
    30 3 * * * cd /home/work/crontabs/ && sh export_taopiaopiao_cinemas_shows.sh
liutao
dainan




web 2       10.210.1.18,10.10.10.18
            midas,fe,be                         数据分析系统
            nginx dmax                                中国巨幕
            

用户和crontab

xiaochen
    1 1 * * * /usr/bin/sh /data0/cron/backup_tables.sh > /dev/null 2>&1
work

# etl
#30 9,16 * * * cd /home/work/etl && python3.4 update_midas.py >> /home/work/etl/log/etl.log_`date +"\%F"` 2>&1
#0 12   * * * cd /home/work/etl && python3.4 update_molap.py >> /home/work/etl/log/etl.molap_log_`date +"\%F"` 2>&1

0  3   * * * cd /home/work/etl && python3.4 prepare_data.py >> /home/work/etl/log/etl_prepare.log_`date +"\%F"` 2>&1
0  */1 * * * cd /home/work/etl && python3.4 export_data.py >> /home/work/etl/log/etl_export.log_`date +"\%F"` 2>&1

# dimension
30 5  * * * cd /home/work/etl && python3.4 update_zhuanzi_dimension.py >> /home/work/etl/log/update_zhuanzi_dimension.log_`date +"\%F"` 2>&1
40 5  * * * cd /home/work/dimension_maintain && python3.4 run.py all >> /home/work/dimension_maintain/log/log_`date +"\%F"` 2>&1
30 11 * * * cd /home/work/dimension_maintain && python3.4 get_cbooo_info.py >> /home/work/dimension_maintain/log/get_cbooo_log_`date +"\%F"` 2>&1

# get holidays
30 0 1 1 * cd /home/work/dimension_maintain && python3.4 get_holidays.py >> /home/work/dimension_maintain/log/get_holidays 2>&1

# get poster from mtime
30 0    * * * cd /home/work/posters_collector && python3.4 run.py all >> /home/work/posters_collector/log/log_`date +"\%F"` 2>&1

# get wangpiao
#0 8,10,12,14,16,20    * * * cd /home/work/wangpiao_collector && python3.4 get_taopiaopiao_info.py shows >> /home/work/wangpiao_collector/log/get_taopiaopiao_show_info_log_`date +"\%F"` 2>&1
#0 8,12,20    * * * cd /home/work/wangpiao_collector && python3.4 get_meituan_info.py shows >> /home/work/wangpiao_collector/log/get_meituan_show_info_log_`date +"\%F"` 2>&1
0 8,10,12,14,16,20    * * * cd /home/work/wangpiao_collector && python3.4 get_wepiao_info.py shows >> /home/work/wangpiao_collector/log/get_wepiao_show_info_log_`date +"\%F"` 2>&1
0 8,10,12,14,16,20    * * * cd /home/work/wangpiao_collector && python3.4 get_nuomi_info.py shows >> /home/work/wangpiao_collector/log/get_nuomi_show_info_log_`date +"\%F"` 2>&1

#10 0 * * 6 cd /home/work/wangpiao_collector && python3.4 get_taopiaopiao_info.py cinemas >> /home/work/wangpiao_collector/log/get_taopiaopiao_cinemas_info_log_`date +"\%F"` 2>&1
10 0 * * 6 cd /home/work/wangpiao_collector && python3.4 get_meituan_info.py     cinemas >> /home/work/wangpiao_collector/log/get_meituan_cinemas_info_log_`date +"\%F"`     2>&1
10 0 * * 6 cd /home/work/wangpiao_collector && python3.4 get_wepiao_info.py      cinemas >> /home/work/wangpiao_collector/log/get_wepiao_cinemas_info_log_`date +"\%F"`      2>&1
10 0 * * 6 cd /home/work/wangpiao_collector && python3.4 get_nuomi_info.py       cinemas >> /home/work/wangpiao_collector/log/get_nuomi_cinemas_info_log_`date +"\%F"`       2>&1

0 22 * * 6 cd /home/work/wangpiao_collector && python3.4 match_cinemas.py >> /home/work/wangpiao_collector/log/match_cinemas_log_`date +"\%F"` 2>&1

# get wangpiao taopiaopiao price
#0 3 * * * cd /home/work/wangpiao_collector && sh run_get_taopiaopiao_sold_seats_shell

# wangpiao merge date
50 7-22/1 * * *  cd /home/work/wangpiao_collector && python3.4 wangpiao_merge_data.py >> /home/work/wangpiao_collector/log/wangpiao_merge_data_log_`date +"\%F"` 2>&1

# fill db[fdm]/table[fdm_project] uni_movie_code and name
0 23 * * * cd /home/work/dimension_maintain && python3.4 match_fdm_movies.py >> /home/work/dimension_maintain/log/match_fdm_movies_log_`date +"\%F"` 2>&1

# fectch kdmchina
#0 20 * * * cd /home/work/kdmchina_collector && python3.4 fetch_kdm_distribute.py >> /home/work/kdmchina_collector/log/fetch_kdm_distribute_log_`date +"\%F"` 2>&1
#0 21 * * * cd /home/work/kdmchina_collector && python3.4 match_kdm_infos.py >> /home/work/kdmchina_collector/log/match_kdm_infos_log_`date +"\%F"` 2>&1

# zhuanzi interface
30 */1 * * * cd /home/work/new_zhuanzi_test && python3.4 zhuanzi_interface.py

# manyan yushou piaofang
40  */1 * * * cd /home/work/boxoffice_spider && python3.4 fetch_maoyan.py

liutao
dainan
chenxi


华影9层机房

web 5       10.110.1.81,10.10.10.81
            KVM

web 6       10.110.1.82,10.10.10.82,192.168.1.211
            dms                                             硬盘快递系统
            ems/财务NC服务                                   财务NC 推送服务

用户和crontab

xiaochen
liutao
#30 */1 * * * cd /home/liutao/etl_zhuanzi && python3.4 prepare_data.py >> /home/liutao/etl_zhuanzi/log/etl_prepare.log_`date +"\%F"` 2>&1
#40 */1 * * * cd /home/liutao/etl_zhuanzi && python3.4 export_data.py >> /home/liutao/etl_zhuanzi/log/etl_export.log_`date +"\%F"` 2>&1

15 */4 * * * cd /home/liutao/new_etl_zhuanzi && python3.4 prepare_data_increase.py >> /home/liutao/new_etl_zhuanzi/log/etl_prepare.log_`date +"\%F"` 2>&1
30 */4 * * * cd /home/liutao/new_etl_zhuanzi && python3.4 export_data_increase.py >> /home/liutao/new_etl_zhuanzi/log/etl_export.log_`date +"\%F"` 2>&1
dainan

bpm
scp4file
xupengzhuo

root
30 10,17 * * *   cd /home/tatooine/tatooine-server && python3 serve_mos_zhuanzi.py > /var/log/tatooine/serve_mos_zhuanzi.log 2>&1
30 6 * * *   cd /home/tatooine/tatooine-server && python3 clean_remote_report.py > clean_remote.out 2>&1
0 * * * * cd /usr/local/www/cron && php56 syncMaterials.php > /dev/null 2>&1
