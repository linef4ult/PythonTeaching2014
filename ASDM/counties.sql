CREATE TABLE "Counties" (
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
    male2011 numeric,
    female2011 numeric,
    total2011 numeric,
    ppocc2011 numeric,
    unocc2011 numeric,
    hs2011 numeric,
    vacant2011 numeric,
    pcvac20111 numeric,
    total_area numeric,
    land_area numeric,
    createdate character varying(10),
    geogid character varying(10)
);


ALTER TABLE public."Counties" OWNER TO root;

--
-- Name: TABLE "Counties"; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE "Counties" IS 'Administrative counties
In census reports the country is divided into 29 counties/administrative counties and the five Cities which represent the
local authority areas. Outside Dublin there are 26 administrative counties (North Tipperary and South Tipperary each
ranks as a separate county for administrative purposes) and four Cities, i.e. Cork, Limerick, Waterford and Galway. In
Dublin the four local authority areas are identified separately, i.e. Dublin City and the three administrative counties of
Dún Laoghaire-Rathdown, Fingal and South Dublin.';


--
-- Name: Census2011_Counties_Modified_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE "Census2011_Counties_Modified_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Census2011_Counties_Modified_id_seq" OWNER TO root;

--
-- Name: Census2011_Counties_Modified_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE "Census2011_Counties_Modified_id_seq" OWNED BY "Counties".id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY "Counties" ALTER COLUMN id SET DEFAULT nextval('"Census2011_Counties_Modified_id_seq"'::regclass);


--
-- Name: Census2011_Counties_Modified_pkey; Type: CONSTRAINT; Schema: public; Owner: root; Tablespace: 
--

ALTER TABLE ONLY "Counties"
    ADD CONSTRAINT "Census2011_Counties_Modified_pkey" PRIMARY KEY (id);


--
-- Name: sidx_Census2011_Counties_Modified_geom; Type: INDEX; Schema: public; Owner: root; Tablespace: 
--

CREATE INDEX "sidx_Census2011_Counties_Modified_geom" ON "Counties" USING gist (geom);


--
-- Name: Counties; Type: ACL; Schema: public; Owner: root
--

