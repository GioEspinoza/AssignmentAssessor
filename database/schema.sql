-- Exported from the authoritative DataGrip-connected PostgreSQL database.
-- Keep this file synchronized with the database design; do not edit it independently.

CREATE TABLE public.tasks (
    task_id integer NOT NULL,
    user_id integer NOT NULL,
    task_name character varying(100) NOT NULL,
    course_name character varying(100) NOT NULL,
    estimated_hours numeric(4,2),
    hours_used numeric(4,2),
    completion_status boolean DEFAULT false NOT NULL,
    difficulty_level integer NOT NULL,
    due_date date,
    date_completed date,
    date_created date DEFAULT CURRENT_DATE,
    CONSTRAINT tasks_difficulty_level_check
        CHECK (((difficulty_level >= 1) AND (difficulty_level <= 5)))
);

CREATE SEQUENCE public.tasks_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.tasks_task_id_seq OWNED BY public.tasks.task_id;

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

ALTER TABLE ONLY public.tasks
    ALTER COLUMN task_id
    SET DEFAULT nextval('public.tasks_task_id_seq'::regclass);

ALTER TABLE ONLY public.users
    ALTER COLUMN user_id
    SET DEFAULT nextval('public.users_user_id_seq'::regclass);

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (task_id);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_user_id_fkey
    FOREIGN KEY (user_id) REFERENCES public.users(user_id);
