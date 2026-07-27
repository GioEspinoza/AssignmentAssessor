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
    status character varying(20) DEFAULT 'not_started'::character varying NOT NULL,
    difficulty_level integer NOT NULL,
    due_date date,
    date_completed date,
    date_created date DEFAULT CURRENT_DATE,
    course_id integer NOT NULL,
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

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (task_id);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_user_id_fkey
    FOREIGN KEY (user_id)
    REFERENCES public.users(user_id)
    ON DELETE CASCADE;

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_user_course_fkey
    FOREIGN KEY (user_id, course_id)
    REFERENCES public.courses(user_id, course_id)
    ON DELETE RESTRICT;

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_user_id_fkey
    FOREIGN KEY (user_id) REFERENCES public.users(user_id);
