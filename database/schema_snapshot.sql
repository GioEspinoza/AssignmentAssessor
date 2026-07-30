-- GENERATED SNAPSHOT — DO NOT EDIT MANUALLY.
-- Exported from the authoritative DataGrip-connected PostgreSQL database.
-- Make schema changes in DataGrip, then regenerate this file from the live database.

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100),
    password_hash character varying(255) NOT NULL,
    join_date date DEFAULT CURRENT_DATE
);

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;

CREATE TABLE public.courses (
    course_id integer GENERATED ALWAYS AS IDENTITY,
    user_id integer NOT NULL,
    course_name character varying(100) NOT NULL,
    course_code character varying(30),
    is_active boolean DEFAULT true NOT NULL,
    date_created date DEFAULT CURRENT_DATE NOT NULL
);

CREATE TABLE public.tasks (
    task_id integer NOT NULL,
    user_id integer NOT NULL,
    task_name character varying(100) NOT NULL,
    estimated_hours numeric(4,2),
    hours_used numeric(4,2),
    difficulty_level integer NOT NULL,
    due_date date,
    date_completed date,
    date_created date DEFAULT CURRENT_DATE,
    course_id integer NOT NULL,
    status character varying(20) DEFAULT 'not_started'::character varying NOT NULL,
    short_description text,
    CONSTRAINT tasks_difficulty_level_check
        CHECK (((difficulty_level >= 1) AND (difficulty_level <= 5))),
    CONSTRAINT tasks_status_check
        CHECK (((status)::text = ANY ((ARRAY[
            'not_started'::character varying,
            'in_progress'::character varying,
            'completed'::character varying
        ])::text[])))
);

CREATE SEQUENCE public.tasks_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.tasks_task_id_seq OWNED BY public.tasks.task_id;

CREATE TABLE public.tags (
    tag_id integer GENERATED ALWAYS AS IDENTITY,
    user_id integer NOT NULL,
    tag_name character varying(50) NOT NULL,
    color_hex character varying(7) DEFAULT '#3B82F6'::character varying NOT NULL,
    date_created timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT tags_color_hex_check
        CHECK (((color_hex)::text ~ '^#[0-9A-Fa-f]{6}$'::text)),
    CONSTRAINT tags_name_not_blank_check
        CHECK ((length(TRIM(BOTH FROM tag_name)) > 0))
);

CREATE TABLE public.task_tags (
    user_id integer NOT NULL,
    task_id integer NOT NULL,
    tag_id integer NOT NULL
);

ALTER TABLE ONLY public.users
    ALTER COLUMN user_id
    SET DEFAULT nextval('public.users_user_id_seq'::regclass);

ALTER TABLE ONLY public.tasks
    ALTER COLUMN task_id
    SET DEFAULT nextval('public.tasks_task_id_seq'::regclass);

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (course_id);

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_user_course_unique UNIQUE (user_id, course_id);

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_user_name_unique UNIQUE (user_id, course_name);

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (tag_id);

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_user_tag_unique UNIQUE (user_id, tag_id);

ALTER TABLE ONLY public.task_tags
    ADD CONSTRAINT task_tags_pkey PRIMARY KEY (task_id, tag_id);

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (task_id);

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_user_task_unique UNIQUE (user_id, task_id);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);

CREATE UNIQUE INDEX tags_user_name_case_insensitive_unique
    ON public.tags USING btree (user_id, lower((tag_name)::text));

CREATE INDEX task_tags_user_tag_idx
    ON public.task_tags USING btree (user_id, tag_id);

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_user_id_fkey
    FOREIGN KEY (user_id)
    REFERENCES public.users(user_id)
    ON DELETE CASCADE;

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_user_id_fkey
    FOREIGN KEY (user_id)
    REFERENCES public.users(user_id)
    ON DELETE CASCADE;

ALTER TABLE ONLY public.task_tags
    ADD CONSTRAINT task_tags_tag_fkey
    FOREIGN KEY (user_id, tag_id)
    REFERENCES public.tags(user_id, tag_id)
    ON DELETE CASCADE;

ALTER TABLE ONLY public.task_tags
    ADD CONSTRAINT task_tags_task_fkey
    FOREIGN KEY (user_id, task_id)
    REFERENCES public.tasks(user_id, task_id)
    ON DELETE CASCADE;

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_user_course_fkey
    FOREIGN KEY (user_id, course_id)
    REFERENCES public.courses(user_id, course_id)
    ON DELETE RESTRICT;

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_user_id_fkey
    FOREIGN KEY (user_id)
    REFERENCES public.users(user_id);
