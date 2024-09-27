-- 创建拉链表
create table dw_zipper
(
    userid    string,
    phone     string,
    nick      string,
    gender    int,
    addr      string,
    starttime string,
    endtime   string
) row format delimited fields terminated by '\t';

-- 创建增量表
create table ods_zipper_update
(
    userid    string,
    phone     string,
    nick      string,
    gender    int,
    addr      string,
    starttime string,
    endtime   string
) row format delimited fields terminated by '\t';
-- 上传两表的数据
select *
from dw_zipper;
select *
from ods_zipper_update;

-- 创建中间表
create table tmp_zipper
(
    userid    string,
    phone     string,
    nick      string,
    gender    int,
    addr      string,
    starttime string,
    endtime   string
) row format delimited fields terminated by '\t';

select * from dw_zipper;
-- 拉链表的操作 (旧表 left join 增量表) union all 增量表
-- 主要是修改endtime
insert overwrite table tmp_zipper
select * from ods_zipper_update
union all
select
    a.userid,
    a.phone,
    a.nick,
    a.gender,
    a.addr,
    a.starttime,
    if(b.userid is NULL or a.endtime < '9999-12-31',a.endtime ,date_add(b.starttime,-1)) as endtime
from
    dw_zipper as a
left join
    ods_zipper_update as b
on a.userid = b.userid;

select * from tmp_zipper;

-- 拉链表的操作


