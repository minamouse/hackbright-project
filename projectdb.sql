--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.5
-- Dumped by pg_dump version 9.5.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: songs; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE songs (
    song_id integer NOT NULL,
    user_id integer NOT NULL,
    name character varying(40),
    song_path character varying(40)
);


ALTER TABLE songs OWNER TO "user";

--
-- Name: songs_song_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE songs_song_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE songs_song_id_seq OWNER TO "user";

--
-- Name: songs_song_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE songs_song_id_seq OWNED BY songs.song_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE users (
    user_id integer NOT NULL,
    username character varying(30) NOT NULL,
    password character varying(30) NOT NULL
);


ALTER TABLE users OWNER TO "user";

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO "user";

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: song_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY songs ALTER COLUMN song_id SET DEFAULT nextval('songs_song_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Data for Name: songs; Type: TABLE DATA; Schema: public; Owner: user
--

COPY songs (song_id, user_id, name, song_path) FROM stdin;
\.


--
-- Name: songs_song_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('songs_song_id_seq', 1, false);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: user
--

COPY users (user_id, username, password) FROM stdin;
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('users_user_id_seq', 1, false);


--
-- Name: songs_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY songs
    ADD CONSTRAINT songs_pkey PRIMARY KEY (song_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users_username_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: songs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY songs
    ADD CONSTRAINT songs_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

