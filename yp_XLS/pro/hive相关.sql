-- 进行数仓的分层 逻辑分层 ODS层
-- 创建数据库
create database yp_ods;  --
use yp_ods;

--分区
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;
set hive.exec.max.dynamic.partitions.pernode=10000;
set hive.exec.max.dynamic.partitions=100000;
set hive.exec.max.created.files=150000;
--hive压缩
set hive.exec.compress.intermediate=true;
set hive.exec.compress.output=true;
--写入时压缩生效
set hive.exec.orc.compression.strategy=COMPRESSION;

create database yp_dwd;
use yp_dwd;

-- ods使用sqoop导入数据


