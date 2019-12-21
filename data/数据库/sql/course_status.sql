/*
 Navicat Premium Data Transfer

 Source Server         : db
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 21/12/2019 20:40:49
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for course_status
-- ----------------------------
DROP TABLE IF EXISTS "course_status";
CREATE TABLE "course_status" (
  "status" integer(4) NOT NULL DEFAULT 0
);

-- ----------------------------
-- Records of course_status
-- ----------------------------
INSERT INTO "course_status" VALUES (2);

PRAGMA foreign_keys = true;
