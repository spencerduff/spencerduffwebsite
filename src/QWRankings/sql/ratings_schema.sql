--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.1

-- Started on 2025-01-30 13:41:12

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 218 (class 1259 OID 16469)
-- Name: current_ratings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.current_ratings (
    name text NOT NULL,
    mode text NOT NULL,
    map text NOT NULL,
    rating double precision NOT NULL,
    ratings_deviation double precision NOT NULL
);


ALTER TABLE public.current_ratings OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16387)
-- Name: per_game_ratings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.per_game_ratings (
    match_id text NOT NULL,
    date timestamp with time zone NOT NULL,
    mode text NOT NULL,
    name text NOT NULL,
    rating double precision NOT NULL,
    win integer NOT NULL,
    map text NOT NULL,
    ratings_deviation double precision NOT NULL
);


ALTER TABLE public.per_game_ratings OWNER TO postgres;

--
-- TOC entry 4650 (class 2606 OID 16475)
-- Name: current_ratings current_ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.current_ratings
    ADD CONSTRAINT current_ratings_pkey PRIMARY KEY (name, mode, map);


--
-- TOC entry 4651 (class 1259 OID 16476)
-- Name: current_ratings_rating_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX current_ratings_rating_idx ON public.current_ratings USING btree (rating) WITH (deduplicate_items='true');


--
-- TOC entry 4642 (class 1259 OID 16452)
-- Name: date_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX date_idx ON public.per_game_ratings USING btree (date DESC) WITH (deduplicate_items='true');


--
-- TOC entry 4643 (class 1259 OID 16398)
-- Name: map_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX map_idx ON public.per_game_ratings USING btree (map) WITH (deduplicate_items='true');


--
-- TOC entry 4644 (class 1259 OID 16392)
-- Name: match_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX match_id_idx ON public.per_game_ratings USING btree (match_id DESC) WITH (deduplicate_items='true');


--
-- TOC entry 4645 (class 1259 OID 16394)
-- Name: mode_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mode_idx ON public.per_game_ratings USING btree (mode NULLS FIRST) WITH (deduplicate_items='true');


--
-- TOC entry 4646 (class 1259 OID 16395)
-- Name: name_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX name_idx ON public.per_game_ratings USING btree (name) WITH (deduplicate_items='true');


--
-- TOC entry 4647 (class 1259 OID 16396)
-- Name: rating_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rating_idx ON public.per_game_ratings USING btree (rating DESC) WITH (deduplicate_items='true');


--
-- TOC entry 4648 (class 1259 OID 16397)
-- Name: win_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX win_idx ON public.per_game_ratings USING btree (win) WITH (deduplicate_items='true');


-- Completed on 2025-01-30 13:41:13

--
-- PostgreSQL database dump complete
--

