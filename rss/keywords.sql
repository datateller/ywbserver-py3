--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: rss_tlnewskeyword; Type: TABLE; Schema: public; Owner: wjbb; Tablespace: 
--

CREATE TABLE rss_tlnewskeyword (
    id integer NOT NULL,
    word text NOT NULL,
    age double precision NOT NULL
);


ALTER TABLE public.rss_tlnewskeyword OWNER TO wjbb;

--
-- Name: rss_tlnewskeyword_id_seq; Type: SEQUENCE; Schema: public; Owner: wjbb
--

CREATE SEQUENCE rss_tlnewskeyword_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rss_tlnewskeyword_id_seq OWNER TO wjbb;

--
-- Name: rss_tlnewskeyword_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wjbb
--

ALTER SEQUENCE rss_tlnewskeyword_id_seq OWNED BY rss_tlnewskeyword.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: wjbb
--

ALTER TABLE ONLY rss_tlnewskeyword ALTER COLUMN id SET DEFAULT nextval('rss_tlnewskeyword_id_seq'::regclass);


--
-- Data for Name: rss_tlnewskeyword; Type: TABLE DATA; Schema: public; Owner: wjbb
--

COPY rss_tlnewskeyword (id, word, age) FROM stdin;
1	新生儿	0
2	1岁	1
4	3岁	3
5	4岁	4
3	2岁	2
8	7岁	7
7	6岁	6
9	8岁	8
13	12岁	12
12	11岁	11
11	10岁	10
10	9岁	9
6	5岁	5
14	小升初	12
15	小学生	6


--
-- Name: rss_tlnewskeyword_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wjbb
--

SELECT pg_catalog.setval('rss_tlnewskeyword_id_seq', 6, true);


--
-- Name: rss_tlnewskeyword_pkey; Type: CONSTRAINT; Schema: public; Owner: wjbb; Tablespace: 
--

ALTER TABLE ONLY rss_tlnewskeyword
    ADD CONSTRAINT rss_tlnewskeyword_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

