-- 进入pgsql数据库
--root@loongson-pc:~# su - postgres
--postgres@loongson-pc:~$ psql
--psql (11.7 (Debian 11.7-0+deb10u1.lnd.2))
--输入 "help" 来获取帮助信息.
--
--postgres=#

-- 创建loongson用户，指定密码为loongson
--postgres=# create user loongson with password 'loongson';
---- 创建数据库performance_data指定所属者为loongson
--postgres=# create database performance_data owner loongson;
---- 授予loongson用户performance_data数据库权限
--postgres=# grant all privileges on database performance_data to loongson;
---- 切换数据库
--postgres=# \c performance_data;

-- 创建iozone表
create table iozone (
    ip varchar(255) not null,
    exec_date timestamp(6) not null,
    read varchar(255) not null,
    ran_read varchar(255) not null,
    write varchar(255) not null,
    ran_write varchar(255) not null
);
-- 添加 ip, exec_date 为主键
alter table iozone add constraint iozone_pkey primary key(ip, exec_date);
-- 授予loongson用户查看performance_data数据库的iozone表的权限
grant all privileges on table iozone to loongson;

-- 创建stream表
create table stream (
    ip varchar(255) not null,
    exec_date timestamp(6) not null,
    thread_num varchar(255) not null,
    copy varchar(255) not null,
    scale varchar(255) not null,
    add varchar(255) not null,
    triad varchar(255) not null
);
-- 添加 ip, exec_date, thread_num 为主键
alter table stream add constraint stream_pkey primary key(ip, exec_date, thread_num);
-- 授予loongson用户查看performance_data数据库的stream表的权限
grant all privileges on table stream to loongson;

-- 创建netperf表
create table netperf (
    ip varchar(255) not null,
    exec_date timestamp(6) not null,
    test_way varchar(255) not null,
    tcp_stream varchar(255) not null,
    udp_stream varchar(255) not null,
    tcp_rr varchar(255) not null,
    udp_rr varchar(255) not null,
    tcp_crr varchar(255) not null
);
-- 添加 ip, exec_date, test_way 为主键
alter table netperf add constraint netperf_pkey primary key(ip, exec_date, test_way);
-- 授予loongson用户查看performance_data数据库的netperf表的权限
grant all privileges on table netperf to loongson;

--创建unixbench表
create table unixbench (
    ip varchar(255) not null,
    exec_date timestamp(6) not null,
    test_way varchar(255) not null,
    Dhrystone_2_using_register_variables varchar(255) not null,
    Execl_Throughput varchar(255) not null,
    File_Copy_1024_bufsize_2000_maxblocks varchar(255) not null,
    File_Copy_256_bufsize_500_maxblocks varchar(255) not null,
    File_Copy_4096_bufsize_8000_maxblocks varchar(255) not null,
    Pipe_based_Context_Switching varchar(255) not null,
    Pipe_Throughput varchar(255) not null,
    Process_Creation varchar(255) not null,
    Shell_Scripts_1_concurrent varchar(255) not null,
    Shell_Scripts_8_concurrent varchar(255) not null,
    System_Call_Overhead varchar(255) not null,
    System_Benchmarks_Index_Score varchar(255) not null
);
--添加 ip, exec_date, test_way 为主键
alter table unixbench add constraint unixbench_pkey primary key(ip, exec_date, test_way);
--授予loongson用户查看performance_data数据库的unixbench表的权限
grant all privileges on table unixbench to loongson;

--创建unixbench_2d表
--S => 2
--T => 3
create table unixbench_2d (
    ip varchar(255) not null,
    exec_date timestamp(6) not null,
    SD_graphics__aa_polygons varchar(255) not null,
    SD_graphics__ellipses varchar(255) not null,
    SD_graphics__images_and_blits varchar(255) not null,
    SD_graphics__rectangles varchar(255) not null,
    SD_graphics__text varchar(255) not null,
    SD_graphics__windows varchar(255) not null,
    SD_Graphics_Benchmarks_Index_Score varchar(255) not null,
    TD_graphics__gears varchar(255) not null,
    TD_Graphics_Benchmarks_Index_Score varchar(255) not null
);
--添加 ip, exec_date 为主键
alter table unixbench_2d add constraint unixbench_2d_pkey primary key(ip, exec_date);
--授予loongson用户查看performance_data数据库的unixbench_2d表的权限
grant all privileges on table unixbench_2d to loongson;

--创建specjvm表
create table specjvm (
    ip varchar(255) not null,
    exec_date timestamp(6) not null,
    compiler varchar(255) not null,
    compress varchar(255) not null,
    crypto varchar(255) not null,
    derby varchar(255) not null,
    mpegaudio varchar(255) not null,
    scimark_large varchar(255) not null,
    scimark_small varchar(255) not null,
    serial varchar(255) not null,
    startup varchar(255) not null,
    sunflow varchar(255) not null,
    xml varchar(255) not null,
    Composite_result varchar(255) not null
);
--添加 ip, exec_date 为主键
alter table specjvm add constraint specjvm_pkey primary key(ip, exec_date);
--授予loongson用户查看performance_data数据库的specjvm表的权限
grant all privileges on table specjvm to loongson;

--创建spec2000_cint表
create table spec2000_cint (
    ip varchar(255) not null,
    exec_date timestamp(6) not null,
    thread_status varchar(255) not null,
    gzip_164 varchar(255) not null,
    vpr_175 varchar(255) not null,
    gcc_176 varchar(255) not null,
    mcf_181 varchar(255) not null,
    crafty_186 varchar(255) not null,
    parser_197 varchar(255) not null,
    eon_252 varchar(255) not null,
    perlbmk_253 varchar(255) not null,
    gap_254 varchar(255) not null,
    vortex_255 varchar(255) not null,
    bzip2_256 varchar(255) not null,
    twolf_300 varchar(255) not null,
    SPECint_rate_base2000 varchar(255) not null
);
--添加 ip, exec_date, thread_status 为主键
alter table spec2000_cint add constraint spec2000_cint_pkey primary key(ip, exec_date, thread_status);
--授予loongson用户查看performance_data数据库的spec2000_cint表的权限
grant all privileges on table spec2000_cint to loongson;

--创建spec2000_cfp表
create table spec2000_cfp (
    ip varchar(255) not null,
    exec_date timestamp(6) not null,
    thread_status varchar(255) not null,
    wupwise_168 varchar(255) not null,
    swim_171 varchar(255) not null,
    mgrid_172 varchar(255) not null,
    applu_173 varchar(255) not null,
    mesa_177 varchar(255) not null,
    galgel_178 varchar(255) not null,
    art_179 varchar(255) not null,
    equake_183 varchar(255) not null,
    facerec_187 varchar(255) not null,
    ammp_188 varchar(255) not null,
    lucas_189 varchar(255) not null,
    fma3d_191 varchar(255) not null,
    sixtrack_200 varchar(255) not null,
    apsi_301 varchar(255) not null,
    SPECfp_rate_base2000 varchar(255) not null
);
--添加 ip, exec_date, thread_status 为主键
alter table spec2000_cfp add constraint spec2000_cfp_pkey primary key(ip, exec_date, thread_status);
--授予loongson用户查看performance_data数据库的spec2000_cfp表的权限
grant all privileges on table spec2000_cfp to loongson;

--创建spec2006_cint表
create table spec2006_cint (
    ip varchar(255) not null,
    exec_date timestamp(6) not null,
    thread_status varchar(255) not null,
    perlbench_400 varchar(255) not null,
    bzip2_401 varchar(255) not null,
    gcc_403 varchar(255) not null,
    mcf_429 varchar(255) not null,
    gobmk_445 varchar(255) not null,
    hmmer_456 varchar(255) not null,
    sjeng_458 varchar(255) not null,
    libquantum_462 varchar(255) not null,
    h264ref_464 varchar(255) not null,
    omnetpp_471 varchar(255) not null,
    astar_473 varchar(255) not null,
    xalancbmk_483 varchar(255) not null,
    SPECint_R__base2006 varchar(255) not null
);
--添加 ip, exec_date, thread_status 为主键
alter table spec2006_cint add constraint spec2006_cint_pkey primary key(ip, exec_date, thread_status);
--授予loongson用户查看performance_data数据库的spec2006_cint表的权限
grant all privileges on table spec2006_cint to loongson;

--创建spec2006_cfp表
create table spec2006_cfp (
    ip varchar(255) not null,
    exec_date timestamp(6) not null,
    thread_status varchar(255) not null,
    bwaves_410 varchar(255) not null,
    gamess_416 varchar(255) not null,
    milc_433 varchar(255) not null,
    zeusmp_434 varchar(255) not null,
    gromacs_435 varchar(255) not null,
    cactusADM_436 varchar(255) not null,
    leslie3d_437 varchar(255) not null,
    namd_444 varchar(255) not null,
    dealII_447 varchar(255) not null,
    soplex_450 varchar(255) not null,
    povray_453 varchar(255) not null,
    calculix_454 varchar(255) not null,
    GemsFDTD_459 varchar(255) not null,
    tonto_465 varchar(255) not null,
    lbm_470 varchar(255) not null,
    wrf_481 varchar(255) not null,
    sphinx3_482 varchar(255) not null,
    SPECfp_R__base2006 varchar(255) not null
);
--添加 ip, exec_date, thread_status 为主键
alter table spec2006_cfp add constraint spec2006_cfp_pkey primary key(ip, exec_date, thread_status);
--授予loongson用户查看performance_data数据库的spec2006_cfp表的权限
grant all privileges on table spec2006_cfp to loongson;
