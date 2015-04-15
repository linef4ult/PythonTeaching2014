CREATE TABLE "Electoral_Divisions" (
    id integer NOT NULL,
    geom geometry(MultiPolygon,29902),
    nuts1 character varying(3),
    nuts1name character varying(10),
    nuts2 character varying(4),
    nuts2name character varying(30),
    nuts3 character varying(5),
    nuts3name character varying(20),
    county character varying(2),
    countyname character varying(35),
    csoed character varying(15),
    osied character varying(15),
    edname character varying(80),
    male2011 numeric,
    female2011 numeric,
    total2011 numeric,
    ppocc2011 numeric,
    unocc2011 numeric,
    hs2011 numeric,
    vacant2011 numeric,
    pcvac2011 numeric,
    total_area numeric,
    land_area numeric,
    createdate character varying(10),
    geogid character varying(100)
);


ALTER TABLE public."Electoral_Divisions" OWNER TO root;

--
-- Name: TABLE "Electoral_Divisions"; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE "Electoral_Divisions" IS 'There are 3,440 Electoral Divisions (EDs) which are the smallest legally defined administrative areas in the State. One
ED, St. Mary''s, straddles the Louth-Meath county border, and is presented in two parts in the SAPS 1 tables, with one
part in Louth and the other in Meath. There are 32 EDs with low population, which for reasons of confidentiality have
been amalgamated into neighbouring EDs giving a total of 3,409 EDs which appear in the SAPS tables.';


--
-- Name: Census2011_Electoral_Divisions_Modified_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE "Census2011_Electoral_Divisions_Modified_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Census2011_Electoral_Divisions_Modified_id_seq" OWNER TO root;

--
-- Name: Census2011_Electoral_Divisions_Modified_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE "Census2011_Electoral_Divisions_Modified_id_seq" OWNED BY "Electoral_Divisions".id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY "Electoral_Divisions" ALTER COLUMN id SET DEFAULT nextval('"Census2011_Electoral_Divisions_Modified_id_seq"'::regclass);


--
-- Name: Census2011_Electoral_Divisions_Modified_pkey; Type: CONSTRAINT; Schema: public; Owner: root; Tablespace: 
--

ALTER TABLE ONLY "Electoral_Divisions"
    ADD CONSTRAINT "Census2011_Electoral_Divisions_Modified_pkey" PRIMARY KEY (id);


--
-- Name: sidx_Census2011_Electoral_Divisions_Modified_geom; Type: INDEX; Schema: public; Owner: root; Tablespace: 
--

CREATE INDEX "sidx_Census2011_Electoral_Divisions_Modified_geom" ON "Electoral_Divisions" USING gist (geom);



