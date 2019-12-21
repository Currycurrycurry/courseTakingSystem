/*
 Navicat Premium Data Transfer

 Source Server         : db
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 21/12/2019 20:40:26
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for application
-- ----------------------------
DROP TABLE IF EXISTS "application";
CREATE TABLE "application" (
  "course_id" text(255) NOT NULL,
  "section_id" integer(5) NOT NULL,
  "student_id" text(255) NOT NULL,
  "status" integer(5) NOT NULL DEFAULT 0,
  "application_reason" text(255),
  "if_drop" integer(5) DEFAULT 0,
  PRIMARY KEY ("course_id", "section_id", "student_id"),
  FOREIGN KEY ("student_id") REFERENCES "student" ("student_id") ON DELETE CASCADE ON UPDATE NO ACTION,
  FOREIGN KEY ("course_id", "section_id") REFERENCES "section" ("course_id", "section_id") ON DELETE CASCADE ON UPDATE NO ACTION
);

PRAGMA foreign_keys = true;
