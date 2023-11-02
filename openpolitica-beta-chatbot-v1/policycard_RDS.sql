-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "UserNeeds" (
    "id" int   NOT NULL,
    "text" string   NOT NULL,
    "timestamp" datetime   NOT NULL,
    "user_id" int   NOT NULL,
    "context" string   NOT NULL,
    "asc_pc_id" int   NOT NULL,
    CONSTRAINT "pk_UserNeeds" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "PolicyCards" (
    "id" int   NOT NULL,
    "content" string   NOT NULL,
    "userneed_id" int   NOT NULL,
    "category" string   NOT NULL,
    "effective_date" datetime   NOT NULL,
    "policy_makers" string   NOT NULL,
    "voting_status" boolean   NOT NULL,
    "regional_info" string   NOT NULL,
    CONSTRAINT "pk_PolicyCards" PRIMARY KEY (
        "id"
     )
);

ALTER TABLE "UserNeeds" ADD CONSTRAINT "fk_UserNeeds_id" FOREIGN KEY("id")
REFERENCES "PolicyCards" ("userneed_id");

ALTER TABLE "PolicyCards" ADD CONSTRAINT "fk_PolicyCards_id" FOREIGN KEY("id")
REFERENCES "UserNeeds" ("asc_pc_id");

