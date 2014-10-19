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
-- Name: rss_localnewskeyword; Type: TABLE; Schema: public; Owner: wjbb; Tablespace: 
--

CREATE TABLE rss_localnewskeyword (
    id integer NOT NULL,
    word text NOT NULL,
    city text NOT NULL
);


ALTER TABLE public.rss_localnewskeyword OWNER TO wjbb;

--
-- Name: rss_localnewskeyword_id_seq; Type: SEQUENCE; Schema: public; Owner: wjbb
--

CREATE SEQUENCE rss_localnewskeyword_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rss_localnewskeyword_id_seq OWNER TO wjbb;

--
-- Name: rss_localnewskeyword_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wjbb
--

ALTER SEQUENCE rss_localnewskeyword_id_seq OWNED BY rss_localnewskeyword.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: wjbb
--

ALTER TABLE ONLY rss_localnewskeyword ALTER COLUMN id SET DEFAULT nextval('rss_localnewskeyword_id_seq'::regclass);


--
-- Data for Name: rss_localnewskeyword; Type: TABLE DATA; Schema: public; Owner: wjbb
--

COPY rss_localnewskeyword (id, word, city) FROM stdin;
1	北京,孩子	北京市
2	上海,孩子	上海市
3	广州,孩子	广州市
4	郑州,孩子	郑州市
\.


--
-- Name: rss_localnewskeyword_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wjbb
--

SELECT pg_catalog.setval('rss_localnewskeyword_id_seq', 1, false);


--
-- Name: rss_localnewskeyword_pkey; Type: CONSTRAINT; Schema: public; Owner: wjbb; Tablespace: 
--

ALTER TABLE ONLY rss_localnewskeyword
    ADD CONSTRAINT rss_localnewskeyword_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

