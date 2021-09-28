--
-- PostgreSQL database dump
--

-- Dumped from database version 13.3 (Debian 13.3-1.pgdg100+1)
-- Dumped by pg_dump version 13.4

-- Started on 2021-09-27 14:13:47

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 202 (class 1259 OID 254157)
-- Name: counter; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.counter (
    count bigint NOT NULL
);


ALTER TABLE public.counter OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 254147)
-- Name: insert_entrylog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.insert_entrylog (
    id bigint NOT NULL,
    request_id text NOT NULL,
    request_ts timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.insert_entrylog OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 254145)
-- Name: insert_entrylog_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.insert_entrylog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.insert_entrylog_id_seq OWNER TO postgres;

--
-- TOC entry 2952 (class 0 OID 0)
-- Dependencies: 200
-- Name: insert_entrylog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.insert_entrylog_id_seq OWNED BY public.insert_entrylog.id;


--
-- TOC entry 2808 (class 2604 OID 254150)
-- Name: insert_entrylog id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insert_entrylog ALTER COLUMN id SET DEFAULT nextval('public.insert_entrylog_id_seq'::regclass);


--
-- TOC entry 2946 (class 0 OID 254157)
-- Dependencies: 202
-- Data for Name: counter; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.counter (count) FROM stdin;
1
\.


--
-- TOC entry 2945 (class 0 OID 254147)
-- Dependencies: 201
-- Data for Name: insert_entrylog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.insert_entrylog (id, request_id, request_ts) FROM stdin;
1	e415e3ede02948aa9276070a2a1cd246	2021-09-27 07:57:44.776608+00
2	7bd802778b304b6fa27f07302db09a34	2021-09-27 07:57:53.216138+00
3	2824b6d9ac364efea36b011be90abc95	2021-09-27 07:58:24.105082+00
4	3c6fe886b8134b14aa1f4906aa8af7d8	2021-09-27 07:58:26.426272+00
5	3f996de928a84ae0b49af00b1b317fb4	2021-09-27 07:58:27.28533+00
6	4d9b2066dafa40f3ac67986e192951b0	2021-09-27 08:24:16.780843+00
7	00817ed14a0b4139ae0df044c3f0cbc0	2021-09-27 08:26:09.251622+00
\.


--
-- TOC entry 2953 (class 0 OID 0)
-- Dependencies: 200
-- Name: insert_entrylog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.insert_entrylog_id_seq', 7, true);


--
-- TOC entry 2813 (class 2606 OID 254161)
-- Name: counter counter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.counter
    ADD CONSTRAINT counter_pkey PRIMARY KEY (count);


--
-- TOC entry 2811 (class 2606 OID 254156)
-- Name: insert_entrylog insert_entrylog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insert_entrylog
    ADD CONSTRAINT insert_entrylog_pkey PRIMARY KEY (id);


-- Completed on 2021-09-27 14:13:47

--
-- PostgreSQL database dump complete
--

