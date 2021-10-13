-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION "user";
-- public.tb_exemplo definition

-- Drop table

-- DROP TABLE public.tb_exemplo;

CREATE TABLE public.tb_exemplo (
	"name" varchar NULL,
	description varchar NULL,
	quantidade_legal int4 NULL
);
