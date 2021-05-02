--Group 6 added table 5-1-2021
CREATE TABLE IF NOT EXISTS "augur_data"."repo_libyear" (
  "repo_libyear_id" serial8 NOT NULL,
  "repo_id" int8,
  "repo_libyears" int4,
  "repo_path" varchar(255),
  "tool_source" varchar(255) COLLATE "pg_catalog"."default",
  "tool_version" varchar(255) COLLATE "pg_catalog"."default",
  "data_source" varchar(255) COLLATE "pg_catalog"."default",
  "data_collection_date" timestamp(0),
  CONSTRAINT "repo_libyear_pkey" PRIMARY KEY ("repo_libyear_id")
);