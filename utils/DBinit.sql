DROP DATABASE ihome;

CREATE DATABASE ihome CHARSET utf8;

USE ihome;

CREATE TABLE cl_user_profile(
  up_user_id INT unsigned NOT NULL auto_increment comment '用户id',
  up_name VARCHAR(32) NOT NULL comment '昵称',
  up_mobile CHAR(11) NULL comment '手机号',
  up_password VARCHAR(40) NOT NULL comment '密码',
  up_real_name VARCHAR(32) NULL comment '真实姓名',
  up_id_card CHAR(20) NULL  comment '身份证号',
  up_avatar VARCHAR(128) NULL comment '头像',
  up_admin tinyint NOT NULL DEFAULT '0' comment '是否是管理员 0：不是，1：是',
  up_utime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '最后更新时间',
  up_ctime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
  PRIMARY KEY(up_user_id),
  UNIQUE(up_name),
  UNIQUE(up_mobile)
)AUTO_INCREMENT=10000 comment='用户信息表';

CREATE TABLE cl_area_info(
  ai_area_id INT NOT NULL auto_increment PRIMARY KEY comment '区域id',
  ai_name VARCHAR(32) NOT NULL comment '区域名称',
  ai_ctime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间'

)comment='房源区域表';

CREATE TABLE cl_house_info(
  hi_house_id INT UNSIGNED NOT NULL PRIMARY KEY auto_increment comment '房屋id',
  hi_user_id INT UNSIGNED NOT NULL comment '用户id',
  hi_title VARCHAR(64) NOT NULL comment '房屋名称',
  hi_price int NOT NULL DEFAULT 0 comment '房屋价格，单位：分',
  hi_area_id INT NOT NULL comment '房屋区域id',
  hi_address VARCHAR(512) NOT NULL DEFAULT '' comment '地址',
  hi_room_count tinyint unsigned NOT NULL DEFAULT '1' comment '房间数',
  hi_acreage INT unsigned NOT NULL DEFAULT '0' comment '房屋面积',
  hi_house_unit VARCHAR(32) NOT NULL DEFAULT '' comment '房屋户型',
  hi_capacity INT unsigned not NULL DEFAULT '1' comment '容纳人数',
  hi_beds VARCHAR(64) NOT NULL DEFAULT '' comment '床的配置',
  hi_deposit INT NOT NULL DEFAULT '0' comment '押金，单位：分',
  hi_mid_days INT NOT NULL DEFAULT '1' comment '最短入住时间',
  hi_max_days INT NOT NULL DEFAULT '0' comment '最长入住时间，0：不限制',
  hi_order_count INT NOT NULL DEFAULT '0' comment '下单数量',
  hi_verify_status tinyint NOT NULL DEFAULT '0' comment '审核状态，0：带审核，1：审核未通过，2：审核通过',
  hi_online_status tinyint NOT NULL DEFAULT '1' comment '0：下线，1：上线',
  hi_index_image_url VARCHAR(256) NULL comment '房屋主图片url',
  hi_utime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '最后更新时间',
  hi_ctime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
#   KEY hi_status (hi_verify_status,hi_online_status),
  FOREIGN KEY(hi_user_id) REFERENCES cl_user_profile(up_user_id),
  FOREIGN KEY(hi_area_id) REFERENCES cl_area_info(ai_area_id)
)comment='房屋信息表';


CREATE TABLE cl_house_facility(
  hf_id INT NOT NULL auto_increment PRIMARY KEY comment '自增id',
  hf_house_id INT UNSIGNED NOT NULL comment '房屋id',
  hf_facility_id INT NOT NULL comment '房屋设施',
  hi_ctime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
  FOREIGN KEY(hf_house_id) REFERENCES cl_house_info(hi_house_id)
)comment='房屋设施表';

CREATE TABLE cl_facility_catelog(
  fc_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '自增id',
  fc_name VARCHAR(32) NOT NULL COMMENT '设置名称',
  fc_ctime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
)COMMENT='设施型录表';

CREATE TABLE cl_order_info(
  oi_order_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '订单id',
  oi_user_id INT UNSIGNED NOT NULL COMMENT '用户',
  oi_house_id INT UNSIGNED NOT NULL COMMENT '房屋id',
  oi_begin_date DATE NOT NULL COMMENT '入住时间',
  oi_end_date DATE NOT NULL COMMENT '离开时间',
  oi_days INT NOT NULL COMMENT '入住天数',
  oi_house_price INT NOT NULL COMMENT '房屋单价，单位：分',
  oi_amount INT NOT NULL COMMENT '订单金额，单位：分',
  oi_status TINYINT NOT NULL DEFAULT '0' COMMENT '订单状态，0：待接单，1：待支付，2：已支付，3：待评价，4：已完成，5：已取消，6：拒接单',
  oi_comment TEXT NULL COMMENT '订单评论',
  oi_utime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  oi_ctime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
  KEY oi_status (oi_status),
  FOREIGN KEY(oi_user_id) REFERENCES cl_user_profile(up_user_id),
  FOREIGN KEY (oi_house_id) REFERENCES cl_house_info(hi_house_id)
)COMMENT='订单表';

CREATE TABLE cl_house_image(
  hi_image_id INT NOT NULL AUTO_INCREMENT  PRIMARY KEY COMMENT '图片id',
  hi_house_id INT UNSIGNED NOT NULL COMMENT '房屋id',
  hi_url VARCHAR(256) NULL COMMENT '图片url',
  hi_ctime DATETIME NOT NULL DEFAULT current_timestamp ON UPDATE current_timestamp COMMENT '最后更新时间',
  FOREIGN KEY (hi_house_id) REFERENCES cl_house_info(hi_house_id)
)COMMENT='房屋图片表';