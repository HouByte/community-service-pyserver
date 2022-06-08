/*
 Navicat Premium Data Transfer

 Source Server         : pycs
 Source Server Type    : MySQL
 Source Server Version : 50718
 Source Host           : sql.flowboot.cn:28266
 Source Schema         : community_service

 Target Server Type    : MySQL
 Target Server Version : 50718
 File Encoding         : 65001

 Date: 23/05/2022 15:09:03
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for member
-- ----------------------------
DROP TABLE IF EXISTS `member`;
CREATE TABLE `member`  (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `nickname` varchar(108) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '会员名',
  `mobile` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '会员手机号码',
  `gender` tinyint(1) NOT NULL DEFAULT 0 COMMENT '1:男 2：女 0：没填写',
  `avatar` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '会员头像',
  `status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '1:有效 0：无效',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后一次时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '会员表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of member
-- ----------------------------
INSERT INTO `member` VALUES (1, 'Vincent·Vic', '', 0, 'https://thirdwx.qlogo.cn/mmopen/vi_32/CgJFxdvSibybL4tdhWmiaaiaD1yvur7FbzK8Nt4T38fq8u8uAa7bowXaaRb6H3lKkeGMbibiakKWDQSKQVibwLw7JHWQ/132', 1, '2022-05-23 14:52:02', '2022-05-04 20:02:28');
INSERT INTO `member` VALUES (2, 'Vincent', '', 0, 'https://thirdwx.qlogo.cn/mmopen/vi_32/CgJFxdvSibybL4tdhWmiaaiaD1yvur7FbzK8Nt4T38fq8u8uAa7bowXaaRb6H3lKkeGMbibiakKWDQSKQVibwLw7JHWQ/132', 1, '2022-05-13 15:14:01', '2022-05-04 20:02:28');
INSERT INTO `member` VALUES (3, 'flowboot', '', 0, 'https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLxxemjE8PMuJVctvg11dGYlOtVnrFnxVOibASI5upGTiaNiaYbfHAffZh6pndrpiaumYREQlWE0FX7qA/132', 1, '2022-05-22 13:12:18', '2022-05-22 13:12:13');

-- ----------------------------
-- Table structure for oauth_member_bind
-- ----------------------------
DROP TABLE IF EXISTS `oauth_member_bind`;
CREATE TABLE `oauth_member_bind`  (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id',
  `member_id` int(11) NOT NULL COMMENT '会员id',
  `client_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'wechat_mini' COMMENT '客户端来源类型:web, wechat_mini',
  `type` tinyint(3) NOT NULL DEFAULT 1 COMMENT '类型type 1:wechat ',
  `openid` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '第三方id ',
  `unionid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '跨应用id',
  `extra` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '额外字段',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_type_openid`(`type`, `openid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '第三方登录绑定关系' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of oauth_member_bind
-- ----------------------------
INSERT INTO `oauth_member_bind` VALUES (1, 1, 'wechat_mini', 1, 'ojkIM0R1q9jZlVN9P4XDk8OhZZGw', '', '', '2022-05-04 20:02:28', '2022-05-04 20:02:28');
INSERT INTO `oauth_member_bind` VALUES (2, 3, 'wechat_mini', 1, 'ojkIM0UeKqs1viDiVLNbx79xiYBI', '', '', '2022-05-22 13:12:13', '2022-05-22 13:12:13');

-- ----------------------------
-- Table structure for rating
-- ----------------------------
DROP TABLE IF EXISTS `rating`;
CREATE TABLE `rating`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `mid` int(11) NOT NULL COMMENT '会员id',
  `sid` int(11) NOT NULL COMMENT '服务id',
  `oid` int(11) NOT NULL COMMENT '订单id',
  `content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '评论内容',
  `score` int(5) NOT NULL DEFAULT 0 COMMENT '评分',
  `illustration` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '图片',
  `created` date NOT NULL COMMENT '评论时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of rating
-- ----------------------------
INSERT INTO `rating` VALUES (1, 1, 140, 1, 'xxxxxxxxxxxxxxxxxxxxxxxxxx', 4, 'upload/1652514903.png,upload/1652514910.png', '2022-05-14');
INSERT INTO `rating` VALUES (2, 1, 140, 1, 'xxxxxxxxxxxxxxxxxxxxxx', 4, '', '2022-05-14');
INSERT INTO `rating` VALUES (6, 1, 146, 2, '111111111111111', 4, '', '2022-05-23');
INSERT INTO `rating` VALUES (7, 1, 147, 10, '11', 4, '', '2022-05-23');
INSERT INTO `rating` VALUES (8, 1, 147, 9, '好评', 5, '', '2022-05-23');

-- ----------------------------
-- Table structure for service
-- ----------------------------
DROP TABLE IF EXISTS `service`;
CREATE TABLE `service`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `type` int(5) NOT NULL COMMENT '类型：0 找/ 1 提供',
  `nature` int(5) NOT NULL COMMENT '性质：0 互助，1 收费，2 公益',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '标题',
  `description` tinytext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '详情',
  `coverImage` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '封面',
  `designatedPlace` tinyint(1) NULL DEFAULT NULL COMMENT '指定地点',
  `price` decimal(10, 2) NOT NULL COMMENT '价格，互助和公益为0',
  `status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '状态',
  `p_uid` int(11) NOT NULL COMMENT '发布人id',
  `category` int(11) NOT NULL COMMENT '分类',
  `salesVolume` int(11) NULL DEFAULT 0 COMMENT '使用量',
  `score` float(11, 2) NULL DEFAULT 5.00 COMMENT '评分',
  `created` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `beginDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '服务开始时间',
  `endDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '服务结束时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 151 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of service
-- ----------------------------
INSERT INTO `service` VALUES (140, 1, 1, '上门维修xx', 'http://127.0.0.1:5000 http://127.0.0.1:5000 http://127.0.0.1:5000 ', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/0b2d441b21764788b49ef223667a2735.png', 1, 50.00, 1, 1, 1, 4, 5.00, '2022-05-22 18:57:32', '2022-05-22 20:32:37', '2022-05-22 00:00:00', '2024-05-22 00:00:00');
INSERT INTO `service` VALUES (141, 2, 1, '上门维修服务', 'xxxxhttp://127.0.0.1:5000 http://127.0.0.1:5000 http://127.0.0.1:5000 ', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/0573410b2c124f23858a9af88f1180e6.png', 0, 51.00, 3, 1, 1, 2, 5.00, '2022-05-22 11:02:56', '2022-05-22 20:36:56', '2022-05-22 00:00:00', '2023-05-22 00:00:00');
INSERT INTO `service` VALUES (142, 1, 1, '洗衣机清洗', '洗衣机上门清洗服务，服务范围xx小区，时间8:00～20:00', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/d2f68041611a448faad8e3e22da367d6.png', 1, 50.00, 3, 1, 2, 3, 5.00, '2022-05-22 11:12:35', '2022-05-22 12:55:33', '2022-05-22 00:00:00', '2023-05-22 00:00:00');
INSERT INTO `service` VALUES (143, 1, 1, '洗衣机上门维修服务', '洗衣机上门维修服务，服务范围xx小区，时间8:00～20:00', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/033458e03ba24b5f8d1bbbae1b9208c5.png', 1, 50.00, 2, 1, 1, 4, 5.00, '2022-05-22 12:54:13', '2022-05-22 12:56:41', '2022-05-22 00:00:00', '2023-05-22 00:00:00');
INSERT INTO `service` VALUES (144, 1, 1, '上门厨房保洁', '上门保洁服务，服务范围xx小区，时间8:00～20:00', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/99322d541a7d468d827a41135c83b4e0.jpg', 1, 120.00, 2, 1, 2, 5, 5.00, '2022-05-22 13:05:27', '2022-05-22 13:28:14', '2022-05-22 00:00:00', '2025-05-22 00:00:00');
INSERT INTO `service` VALUES (145, 1, 1, '同城货运(上门取件)', '上门货运服务，服务范围厦门市，时间8:00～20:00', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/6ba9df7c465c4d37974a32c3ffc997fe.jpg', 1, 100.00, 2, 1, 5, 7, 5.00, '2022-05-22 13:11:12', '2022-05-23 07:01:30', '2022-05-22 00:00:00', '2024-05-22 00:00:00');
INSERT INTO `service` VALUES (146, 1, 1, '代拿快递服务(10kg以内)', '代拿快递，服务范围xx小区，时间8:00～20:00，私聊告诉位置和取件码', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/15b295ef990647d08a93dbf7b2df26f1.png', 1, 5.00, 2, 3, 6, 3, 5.00, '2022-05-22 13:15:41', '2022-05-23 07:00:56', '2022-05-22 00:00:00', '2023-05-22 00:00:00');
INSERT INTO `service` VALUES (147, 1, 1, '代拿快递(20kg以内)', '代拿快递，服务范围xx小区，时间8:00～20:00，私聊告诉位置和取件码', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/41e107c56a4f467c83ee253d0bfe02fe.png', 1, 10.00, 2, 3, 6, 8, 5.00, '2022-05-22 13:17:22', '2022-05-23 13:27:49', '2022-05-22 00:00:00', '2023-05-22 00:00:00');
INSERT INTO `service` VALUES (148, 2, 2, '防疫志愿者招募', 'xx小区防疫志愿者招募，需要n人，小程序联系', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/c88b050272ab42b38ff416dce9e14bdf.png', 0, 0.00, 2, 3, 3, 0, 5.00, '2022-05-22 13:19:24', '2022-05-22 13:27:48', '2022-05-22 00:00:00', '2023-05-22 00:00:00');
INSERT INTO `service` VALUES (149, 2, 0, '寻找丢失的宠物猫', 'xx在xx溜猫时不甚弄丢猫咪，看见的联系一下', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/ea1842cd8c8b498380a10795320fb051.jpg', 0, 0.00, 2, 3, 3, 0, 5.00, '2022-05-22 13:26:14', '2022-05-22 13:27:43', '2022-05-22 00:00:00', '2023-05-22 00:00:00');
INSERT INTO `service` VALUES (150, 1, 1, '水果蔬菜配送上门', '水果蔬菜订购，服务范围xx小区，时间8:00～20:00', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/23/355da7821b7b4770a1f0caee5f9db568.jpg', 1, 10.00, 2, 1, 7, 3, 0.00, '2022-05-23 05:46:32', '2022-05-23 06:40:34', '2022-05-23 00:00:00', '2023-05-23 00:00:00');

-- ----------------------------
-- Table structure for service_category
-- ----------------------------
DROP TABLE IF EXISTS `service_category`;
CREATE TABLE `service_category`  (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '类别名称',
  `weight` tinyint(4) NOT NULL DEFAULT 1 COMMENT '权重',
  `status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '1:有效  0：无效',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后一次跟新时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_name`(`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '食品分类' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of service_category
-- ----------------------------
INSERT INTO `service_category` VALUES (1, '家电维修', 1, 1, '2022-05-06 22:44:30', '2022-05-06 09:29:54');
INSERT INTO `service_category` VALUES (2, '卫生保洁', 0, 1, '2022-05-13 21:19:30', '2022-05-13 21:19:30');
INSERT INTO `service_category` VALUES (3, '志愿服务', 0, 1, '2022-05-13 21:20:53', '2022-05-13 21:20:53');
INSERT INTO `service_category` VALUES (4, '水电疏通', 0, 1, '2022-05-13 21:21:09', '2022-05-13 21:21:09');
INSERT INTO `service_category` VALUES (5, '搬家拉货', 0, 1, '2022-05-13 21:21:54', '2022-05-13 21:21:54');
INSERT INTO `service_category` VALUES (6, '社区配送', 0, 1, '2022-05-13 21:22:22', '2022-05-13 21:22:22');
INSERT INTO `service_category` VALUES (7, '便利店超市', 0, 1, '2022-05-22 18:43:26', '2022-05-22 18:43:26');

-- ----------------------------
-- Table structure for service_order
-- ----------------------------
DROP TABLE IF EXISTS `service_order`;
CREATE TABLE `service_order`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `orderNo` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '订单id',
  `status` tinyint(1) NOT NULL COMMENT '状态',
  `p_uid` int(11) NOT NULL COMMENT '提供者id',
  `c_uid` int(11) NOT NULL COMMENT '客户id',
  `sid` int(11) NOT NULL COMMENT '服务id',
  `price` decimal(10, 2) NOT NULL COMMENT '订单金额',
  `pay_num` int(11) NULL DEFAULT 1 COMMENT '支付数量',
  `snap_nature` int(5) NOT NULL COMMENT '性质：0 互助，1 收费，2 公益',
  `snap_title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '服务名称镜像',
  `snap_cover_image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '服务封面镜像',
  `snap_price` decimal(10, 2) NOT NULL COMMENT '服务价格镜像',
  `snap_category` int(11) NOT NULL COMMENT '分类',
  `consumer_snap_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '客户名字镜像',
  `consumer_snap_tel` varchar(14) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '客户电话镜像',
  `consumer_snap_province` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '客户省份镜像',
  `consumer_snap_city` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '客户城市镜像',
  `consumer_snap_county` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '客户区镜像',
  `consumer_snap_description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '客户地址详情镜像',
  `created` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `orderNo`(`orderNo`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of service_order
-- ----------------------------
INSERT INTO `service_order` VALUES (1, '141009521652494192', 4, 1, 3, 136, 50.00, 1, 1, '洗衣机维修', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/033458e03ba24b5f8d1bbbae1b9208c5.png', 50.00, 1, NULL, NULL, NULL, NULL, NULL, NULL, '2022-05-21 10:09:52', '2022-05-21 15:59:45');
INSERT INTO `service_order` VALUES (2, '221340541653226854', 4, 3, 1, 146, 5.00, 1, 1, '代拿快递服务(10kg以内)', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/15b295ef990647d08a93dbf7b2df26f1.png', 5.00, 6, '张三', '020-81167888', '广东省', '广州市', '海珠区', '新港中路397号', '2022-05-22 13:40:54', '2022-05-23 13:03:57');
INSERT INTO `service_order` VALUES (3, '221341191653226879', 0, 1, 3, 143, 50.00, 1, 1, '洗衣机上门维修服务', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/033458e03ba24b5f8d1bbbae1b9208c5.png', 50.00, 1, 'xx', '18888888888', '福建省', '厦门市', '集美区', '后溪镇厦门理工学院', '2022-05-22 13:41:19', '2022-05-22 13:41:19');
INSERT INTO `service_order` VALUES (4, '221430261653229826', 4, 3, 1, 147, 10.00, 1, 1, '代拿快递(20kg以内)', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/41e107c56a4f467c83ee253d0bfe02fe.png', 10.00, 6, '张三', '020-81167888', '广东省', '广州市', '海珠区', '新港中路397号', '2022-05-22 14:30:26', '2022-05-23 13:15:28');
INSERT INTO `service_order` VALUES (5, '221433381653230018', 4, 3, 1, 147, 10.00, 1, 1, '代拿快递(20kg以内)', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/41e107c56a4f467c83ee253d0bfe02fe.png', 10.00, 6, '张三', '020-81167888', '广东省', '广州市', '海珠区', '新港中路397号', '2022-05-22 14:33:38', '2022-05-23 13:11:30');
INSERT INTO `service_order` VALUES (6, '230129131653269353', 2, 3, 1, 147, 10.00, 1, 1, '代拿快递(20kg以内)', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/41e107c56a4f467c83ee253d0bfe02fe.png', 10.00, 6, '张三', '020-81167888', '广东省', '广州市', '海珠区', '新港中路397号', '2022-05-22 01:29:13', '2022-05-23 07:00:32');
INSERT INTO `service_order` VALUES (7, '230154431653270883', 3, 3, 1, 147, 10.00, 1, 1, '代拿快递(20kg以内)', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/41e107c56a4f467c83ee253d0bfe02fe.png', 10.00, 6, '张三', '020-81167888', '广东省', '广州市', '海珠区', '新港中路397号', '2022-05-23 01:54:43', '2022-05-23 07:00:19');
INSERT INTO `service_order` VALUES (8, '230223461653272626', 0, 3, 1, 147, 20.00, 2, 1, '代拿快递(20kg以内)', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/41e107c56a4f467c83ee253d0bfe02fe.png', 10.00, 6, '张三', '020-81167888', '广东省', '广州市', '海珠区', '新港中路397号', '2022-05-23 02:23:46', '2022-05-23 02:23:46');
INSERT INTO `service_order` VALUES (9, '230439541653280794', 4, 3, 1, 147, 30.00, 3, 1, '代拿快递(20kg以内)', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/41e107c56a4f467c83ee253d0bfe02fe.png', 10.00, 6, '侯国强', '18850163751', '福建省', '厦门市', '集美区', '理工路600号厦门理工学院一期宿舍', '2022-05-23 04:39:54', '2022-05-23 13:26:53');
INSERT INTO `service_order` VALUES (10, '230454061653281646', 4, 3, 1, 147, 10.00, 1, 1, '代拿快递(20kg以内)', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/41e107c56a4f467c83ee253d0bfe02fe.png', 10.00, 6, '侯国强', '18850163751', '福建省', '厦门市', '集美区', '理工路600号厦门理工学院一期宿舍', '2022-05-24 04:54:06', '2022-05-24 12:58:25');
INSERT INTO `service_order` VALUES (11, '231327241653283644', 6, 3, 1, 146, 5.00, 1, 1, '代拿快递服务(10kg以内)', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/15b295ef990647d08a93dbf7b2df26f1.png', 5.00, 6, '张三', '020-81167888', '广东省', '广州市', '海珠区', '新港中路397号', '2022-05-24 14:27:24', '2022-05-24 06:59:50');
INSERT INTO `service_order` VALUES (12, '231327481653283668', 5, 3, 1, 147, 10.00, 1, 1, '代拿快递(20kg以内)', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/41e107c56a4f467c83ee253d0bfe02fe.png', 10.00, 6, '张三', '020-81167888', '广东省', '广州市', '海珠区', '新港中路397号', '2022-05-25 13:27:48', '2022-05-24 13:53:47');
INSERT INTO `service_order` VALUES (13, '230549371653284977', 2, 1, 3, 150, 10.00, 1, 1, '水果蔬菜配送上门', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/23/355da7821b7b4770a1f0caee5f9db568.jpg', 10.00, 7, 'xx', '18888888888', '福建省', '厦门市', '集美区', '后溪镇厦门理工学院', '2022-05-25 05:49:37', '2022-05-25 06:39:53');
INSERT INTO `service_order` VALUES (14, '230640341653288034', 6, 1, 3, 150, 20.00, 2, 1, '水果蔬菜配送上门', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/23/355da7821b7b4770a1f0caee5f9db568.jpg', 10.00, 7, 'xx', '18888888888', '福建省', '厦门市', '集美区', '后溪镇厦门理工学院', '2022-05-25 06:40:34', '2022-05-25 14:54:53');
INSERT INTO `service_order` VALUES (15, '230700561653289256', 1, 3, 1, 146, 5.00, 1, 1, '代拿快递服务(10kg以内)', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/15b295ef990647d08a93dbf7b2df26f1.png', 5.00, 6, '侯国强', '18850163751', '福建省', '厦门市', '集美区', '理工路600号厦门理工学院一期宿舍', '2022-05-25 07:00:56', '2022-05-25 07:01:13');
INSERT INTO `service_order` VALUES (16, '230701301653289290', 1, 1, 3, 145, 100.00, 1, 1, '同城货运(上门取件)', 'https://flowboot-1301252068.cos.ap-guangzhou.myqcloud.com/2022/05/22/6ba9df7c465c4d37974a32c3ffc997fe.jpg', 100.00, 5, 'xx', '18888888888', '福建省', '厦门市', '集美区', '后溪镇厦门理工学院', '2022-05-25 07:01:30', '2022-05-25 07:01:47');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `uid` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '用户uid',
  `nickname` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户名',
  `mobile` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '手机号码',
  `email` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `sex` tinyint(1) NOT NULL DEFAULT 0 COMMENT '1:男,2:女,0:没填写',
  `avatar` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '头像',
  `login_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '登录用户名',
  `login_pwd` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '登录密码',
  `login_salt` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '登录密码的随机加密秘钥',
  `status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '1:有效,0:无效',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`uid`) USING BTREE,
  UNIQUE INDEX `login_name`(`login_name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '用户表(管理员)' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'Vincent Vic', '18899009912', '192391297@qq.com', 1, NULL, 'root', '37b7f14b8af3ebb7dc18b6477bf956db', 'root', 1, '2022-05-13 22:59:48', '2022-05-13 22:59:48');
INSERT INTO `user` VALUES (2, 'admin', '18850163751', '192391297@qq.com', 2, NULL, 'admin', '', '', 1, '2022-05-13 22:57:08', '2022-05-13 22:57:08');
INSERT INTO `user` VALUES (4, 'VincentVic', '18850163751', '192391297@qq.com', 2, NULL, '11111', '', '', 1, '2022-05-07 09:10:45', '2022-05-07 09:10:45');

SET FOREIGN_KEY_CHECKS = 1;
