--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.1

-- Started on 2025-02-02 18:13:45

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

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 4831 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


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
-- TOC entry 219 (class 1259 OID 16527)
-- Name: per_game_item_stats; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.per_game_item_stats (
    match_user_id text NOT NULL,
    name text NOT NULL,
    hp_15_took double precision,
    hp_25_took double precision,
    hp_100_took double precision,
    ga_took double precision,
    ga_time double precision,
    ya_took double precision,
    ya_time double precision,
    ra_took double precision,
    ra_time double precision,
    q_took double precision,
    q_time double precision,
    p_took double precision,
    p_time double precision,
    r_took double precision,
    r_time double precision
);


ALTER TABLE public.per_game_item_stats OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16534)
-- Name: per_game_per_weapon_stats; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.per_game_per_weapon_stats (
    match_user_id_weapon text NOT NULL,
    name text NOT NULL,
    acc_attacks double precision,
    acc_hits double precision,
    acc_real double precision,
    acc_virtual double precision,
    kills_total double precision,
    kills_team double precision,
    kills_enemy double precision,
    kills_self double precision,
    deaths double precision,
    pickups_dropped double precision,
    pickups_taken double precision,
    pickups_total_taken double precision,
    pickups_spawn_taken double precision,
    pickups_spawn_total_taken double precision,
    dmg_enemy double precision,
    dmg_team double precision
);


ALTER TABLE public.per_game_per_weapon_stats OWNER TO postgres;

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
-- TOC entry 221 (class 1259 OID 16541)
-- Name: per_game_stats; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.per_game_stats (
    match_user_id text NOT NULL,
    name text NOT NULL,
    win text NOT NULL,
    date timestamp with time zone NOT NULL,
    mode text NOT NULL,
    map text NOT NULL,
    ping double precision,
    frags double precision,
    deaths double precision,
    tk double precision,
    spawn_frags double precision,
    kills double precision,
    suicides double precision,
    dmg_taken double precision,
    dmg_given double precision,
    dmg_team double precision,
    dmg_self double precision,
    dmg_team_weap double precision,
    dmg_enemy_weap double precision,
    dmg_taken_to_die double precision,
    xfer_rl double precision,
    xfer_lg double precision,
    spree_max double precision,
    spree_quad double precision,
    control double precision,
    speed_max double precision,
    speed_avg double precision,
    axe_stats text,
    sg_stats text,
    ssg_stats text,
    ng_stats text,
    sng_stats text,
    gl_stats text,
    rl_stats text,
    lg_stats text
);


ALTER TABLE public.per_game_stats OWNER TO postgres;

--
-- TOC entry 4664 (class 2606 OID 16475)
-- Name: current_ratings current_ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.current_ratings
    ADD CONSTRAINT current_ratings_pkey PRIMARY KEY (name, mode, map);


--
-- TOC entry 4667 (class 2606 OID 16533)
-- Name: per_game_item_stats per_game_item_stats_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.per_game_item_stats
    ADD CONSTRAINT per_game_item_stats_pkey PRIMARY KEY (match_user_id);


--
-- TOC entry 4669 (class 2606 OID 16555)
-- Name: per_game_per_weapon_stats per_game_per_weapon_stats_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.per_game_per_weapon_stats
    ADD CONSTRAINT per_game_per_weapon_stats_pkey PRIMARY KEY (match_user_id_weapon);


--
-- TOC entry 4671 (class 2606 OID 16547)
-- Name: per_game_stats per_game_stats_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.per_game_stats
    ADD CONSTRAINT per_game_stats_pkey PRIMARY KEY (match_user_id);


--
-- TOC entry 4665 (class 1259 OID 16476)
-- Name: current_ratings_rating_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX current_ratings_rating_idx ON public.current_ratings USING btree (rating) WITH (deduplicate_items='true');


--
-- TOC entry 4656 (class 1259 OID 16452)
-- Name: date_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX date_idx ON public.per_game_ratings USING btree (date DESC) WITH (deduplicate_items='true');


--
-- TOC entry 4657 (class 1259 OID 16398)
-- Name: map_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX map_idx ON public.per_game_ratings USING btree (map) WITH (deduplicate_items='true');


--
-- TOC entry 4658 (class 1259 OID 16392)
-- Name: match_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX match_id_idx ON public.per_game_ratings USING btree (match_id DESC) WITH (deduplicate_items='true');


--
-- TOC entry 4659 (class 1259 OID 16394)
-- Name: mode_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mode_idx ON public.per_game_ratings USING btree (mode NULLS FIRST) WITH (deduplicate_items='true');


--
-- TOC entry 4660 (class 1259 OID 16395)
-- Name: name_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX name_idx ON public.per_game_ratings USING btree (name) WITH (deduplicate_items='true');


--
-- TOC entry 4661 (class 1259 OID 16396)
-- Name: rating_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rating_idx ON public.per_game_ratings USING btree (rating DESC) WITH (deduplicate_items='true');


--
-- TOC entry 4662 (class 1259 OID 16397)
-- Name: win_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX win_idx ON public.per_game_ratings USING btree (win) WITH (deduplicate_items='true');


--
-- TOC entry 4672 (class 2606 OID 16556)
-- Name: per_game_stats axe_stats; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.per_game_stats
    ADD CONSTRAINT axe_stats FOREIGN KEY (axe_stats) REFERENCES public.per_game_per_weapon_stats(match_user_id_weapon) NOT VALID;


--
-- TOC entry 4673 (class 2606 OID 16581)
-- Name: per_game_stats gl_stats; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.per_game_stats
    ADD CONSTRAINT gl_stats FOREIGN KEY (gl_stats) REFERENCES public.per_game_per_weapon_stats(match_user_id_weapon) NOT VALID;


--
-- TOC entry 4674 (class 2606 OID 16548)
-- Name: per_game_stats item_stats; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.per_game_stats
    ADD CONSTRAINT item_stats FOREIGN KEY (match_user_id) REFERENCES public.per_game_item_stats(match_user_id);


--
-- TOC entry 4675 (class 2606 OID 16591)
-- Name: per_game_stats lg_stats; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.per_game_stats
    ADD CONSTRAINT lg_stats FOREIGN KEY (lg_stats) REFERENCES public.per_game_per_weapon_stats(match_user_id_weapon) NOT VALID;


--
-- TOC entry 4676 (class 2606 OID 16571)
-- Name: per_game_stats ng_stats; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.per_game_stats
    ADD CONSTRAINT ng_stats FOREIGN KEY (ng_stats) REFERENCES public.per_game_per_weapon_stats(match_user_id_weapon) NOT VALID;


--
-- TOC entry 4677 (class 2606 OID 16586)
-- Name: per_game_stats rl_stats; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.per_game_stats
    ADD CONSTRAINT rl_stats FOREIGN KEY (rl_stats) REFERENCES public.per_game_per_weapon_stats(match_user_id_weapon) NOT VALID;


--
-- TOC entry 4678 (class 2606 OID 16561)
-- Name: per_game_stats sg_stats; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.per_game_stats
    ADD CONSTRAINT sg_stats FOREIGN KEY (sg_stats) REFERENCES public.per_game_per_weapon_stats(match_user_id_weapon) NOT VALID;


--
-- TOC entry 4679 (class 2606 OID 16576)
-- Name: per_game_stats sng_stats; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.per_game_stats
    ADD CONSTRAINT sng_stats FOREIGN KEY (sng_stats) REFERENCES public.per_game_per_weapon_stats(match_user_id_weapon) NOT VALID;


--
-- TOC entry 4680 (class 2606 OID 16566)
-- Name: per_game_stats ssg_stats; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.per_game_stats
    ADD CONSTRAINT ssg_stats FOREIGN KEY (ssg_stats) REFERENCES public.per_game_per_weapon_stats(match_user_id_weapon) NOT VALID;


-- Completed on 2025-02-02 18:13:46

--
-- PostgreSQL database dump complete
--

