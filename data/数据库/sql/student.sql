/*
 Navicat Premium Data Transfer

 Source Server         : db
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 21/12/2019 20:41:19
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS "student";
CREATE TABLE "student" (
  "student_id" TEXT(255) NOT NULL,
  "student_name" TEXT(255) NOT NULL,
  "student_major" TEXT(255) NOT NULL,
  "student_dept_name" TEXT(255) NOT NULL,
  "student_total_credit" INTEGER(10) DEFAULT 0,
  PRIMARY KEY ("student_id")
);

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO "student" VALUES (17302010032, '于志昊', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17302010028, '李玎善', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17302010034, '杜东方', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17302010015, '黄鼎竣', '软件工程', '软件学院', 20);
INSERT INTO "student" VALUES (17302010047, '符根', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17302010016, '金毅铭', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17302010046, '陈裕', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17302010018, '周钰承', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17302010049, '刘佳兴', '软件工程', '软件学院', 25);
INSERT INTO "student" VALUES (17302010060, '陈国华', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17302010029, '卢永强', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17302010014, '陈昂伸', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17307110010, '顾淳宇', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17307130025, '崔欣宇', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17302010031, '王永立', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17302010011, '吴新铭', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17302010042, '夏禹天', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17302010039, '王尚', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17302010008, '李璠', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17302010033, '于志昊', '软件工程', '软件学院', 0);
INSERT INTO "student" VALUES (17302010001, '小软', '软件工程', '软件学院', 0);

PRAGMA foreign_keys = true;
