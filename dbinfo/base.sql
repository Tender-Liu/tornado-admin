/*
Navicat MySQL Data Transfer

Source Server         : docker-mysql
Source Server Version : 50641
Source Host           : 192.168.8.96:3306
Source Database       : nginx_admin

Target Server Type    : MYSQL
Target Server Version : 50641
File Encoding         : 65001

Date: 2020-02-19 17:42:04
*/

SET FOREIGN_KEY_CHECKS=0;


-- ----------------------------
-- Table structure for user_info
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `group_id` int(11) DEFAULT NULL COMMENT '用户组Id',
  `user_name` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(120) NOT NULL COMMENT '密码',
  `phone` varchar(50) NOT NULL COMMENT '手机号码',
  `email` varchar(50) NOT NULL COMMENT '邮箱',
  `state` int(11) NOT NULL DEFAULT '1' COMMENT '是否予许登录',
  `token` varchar(50) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `modify_date` datetime DEFAULT NULL COMMENT '变更时间',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_info
-- ----------------------------
INSERT INTO `user_info` VALUES ('1', null, 'admin', '0192023a7bbd73250516f069df18b500', '15658896942', '1053098364@qq.com', '1', '', '2019-08-12 14:08:28', '0000-00-00 00:00:00');
