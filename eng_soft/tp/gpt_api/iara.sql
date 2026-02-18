-- DROP SCHEMA iara;

CREATE SCHEMA iara AUTHORIZATION postgres;

-- DROP SEQUENCE iara.reservation_res_id_seq;

CREATE SEQUENCE iara.reservation_res_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE iara.reservation_res_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE iara.reservation_res_id_seq TO postgres;
-- iara.site definition

-- Drop table

-- DROP TABLE iara.site;

CREATE TABLE iara.site (
	id varchar(15) NOT NULL,
	site_name varchar(255) NULL,
	CONSTRAINT site_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE iara.site OWNER TO postgres;
GRANT ALL ON TABLE iara.site TO postgres;


-- iara."user" definition

-- Drop table

-- DROP TABLE iara."user";

CREATE TABLE iara."user" (
	id varchar(15) NOT NULL,
	"name" varchar(255) NULL,
	confirmation_flag _bool NULL,
	ctt_time timestamptz NULL,
	CONSTRAINT user_pkey PRIMARY KEY (id),
	CONSTRAINT user_un UNIQUE (id)
);

-- Permissions

ALTER TABLE iara."user" OWNER TO postgres;
GRANT ALL ON TABLE iara."user" TO postgres;


-- iara.last_messages definition

-- Drop table

-- DROP TABLE iara.last_messages;

CREATE TABLE iara.last_messages (
	user_id varchar(15) NULL,
	lm text NULL,
	ailm text NULL,
	lmdt timestamptz NULL,
	CONSTRAINT last_messages_user_id_key UNIQUE (user_id),
	CONSTRAINT last_messages_user_id_fkey FOREIGN KEY (user_id) REFERENCES iara."user"(id) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE iara.last_messages OWNER TO postgres;
GRANT ALL ON TABLE iara.last_messages TO postgres;




-- Permissions

GRANT ALL ON SCHEMA iara TO postgres;
