/*
 Navicat Premium Data Transfer

 Source Server         : db
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 21/12/2019 20:41:28
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for takes
-- ----------------------------
DROP TABLE IF EXISTS "takes";
CREATE TABLE "takes" (
  "course_id" text(255) NOT NULL,
  "section_id" INTEGER(10) NOT NULL,
  "student_id" text(255) NOT NULL,
  "grade" TEXT(10),
  PRIMARY KEY ("course_id", "section_id", "student_id"),
  FOREIGN KEY ("course_id", "section_id") REFERENCES "section" ("course_id", "section_id") ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY ("student_id") REFERENCES "student" ("student_id") ON DELETE CASCADE ON UPDATE CASCADE
);

PRAGMA foreign_keys = true;
