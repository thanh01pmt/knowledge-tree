-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.activities (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  description text,
  activity_type text NOT NULL,
  sequence_order integer NOT NULL DEFAULT 0,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  assignment_id uuid UNIQUE,
  parent_activity_id uuid,
  scope text NOT NULL DEFAULT 'organization'::text CHECK (scope = ANY (ARRAY['organization'::text, 'classroom'::text])),
  classroom_id uuid,
  organization_code text,
  CONSTRAINT activities_pkey PRIMARY KEY (id),
  CONSTRAINT fk_activities_assignment FOREIGN KEY (assignment_id) REFERENCES public.assignments(id),
  CONSTRAINT activities_parent_activity_id_fkey FOREIGN KEY (parent_activity_id) REFERENCES public.activities(id),
  CONSTRAINT activities_classroom_id_fkey FOREIGN KEY (classroom_id) REFERENCES public.classrooms(id),
  CONSTRAINT activities_activity_type_fkey FOREIGN KEY (activity_type) REFERENCES public.activity_types(code),
  CONSTRAINT activities_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code)
);
CREATE TABLE public.activity_default_resources (
  activity_id uuid NOT NULL,
  resource_id uuid NOT NULL,
  sequence_order integer NOT NULL DEFAULT 0,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by uuid,
  CONSTRAINT activity_default_resources_pkey PRIMARY KEY (activity_id, resource_id),
  CONSTRAINT fk_adr_activity FOREIGN KEY (activity_id) REFERENCES public.activities(id),
  CONSTRAINT fk_adr_resource FOREIGN KEY (resource_id) REFERENCES public.learning_resources(id),
  CONSTRAINT fk_adr_created_by FOREIGN KEY (created_by) REFERENCES public.profiles(id)
);
CREATE TABLE public.activity_learning_objectives (
  activity_id uuid NOT NULL,
  learning_objective_code text NOT NULL,
  CONSTRAINT activity_learning_objectives_pkey PRIMARY KEY (activity_id, learning_objective_code),
  CONSTRAINT activity_learning_objectives_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activities(id),
  CONSTRAINT activity_learning_objectives_learning_objective_code_fkey FOREIGN KEY (learning_objective_code) REFERENCES public.learning_objectives(code)
);
CREATE TABLE public.activity_types (
  code text NOT NULL,
  name text NOT NULL,
  description text,
  icon text,
  category text NOT NULL CHECK (category = ANY (ARRAY['acquisition'::text, 'practice'::text, 'assessment'::text])),
  CONSTRAINT activity_types_pkey PRIMARY KEY (code)
);
CREATE TABLE public.ai_tasks (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  submission_id uuid NOT NULL,
  status text NOT NULL DEFAULT 'pending'::text CHECK (status = ANY (ARRAY['pending'::text, 'processing'::text, 'completed'::text, 'failed'::text])),
  created_by uuid,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  error_message text,
  CONSTRAINT ai_tasks_pkey PRIMARY KEY (id),
  CONSTRAINT ai_tasks_submission_id_fkey FOREIGN KEY (submission_id) REFERENCES public.submissions(id),
  CONSTRAINT ai_tasks_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.profiles(id),
  CONSTRAINT fk_submission FOREIGN KEY (submission_id) REFERENCES public.submissions(id),
  CONSTRAINT fk_created_by FOREIGN KEY (created_by) REFERENCES public.profiles(id)
);
CREATE TABLE public.approach_contexts (
  approach_code text NOT NULL,
  context_code text NOT NULL,
  CONSTRAINT approach_contexts_pkey PRIMARY KEY (approach_code, context_code),
  CONSTRAINT approach_contexts_approach_code_fkey FOREIGN KEY (approach_code) REFERENCES public.approaches(code),
  CONSTRAINT approach_contexts_context_code_fkey FOREIGN KEY (context_code) REFERENCES public.contexts(code)
);
CREATE TABLE public.approach_difficulties (
  approach_code text NOT NULL,
  difficulty_code text NOT NULL,
  CONSTRAINT approach_difficulties_pkey PRIMARY KEY (approach_code, difficulty_code),
  CONSTRAINT approach_difficulties_approach_code_fkey FOREIGN KEY (approach_code) REFERENCES public.approaches(code),
  CONSTRAINT approach_difficulties_difficulty_code_fkey FOREIGN KEY (difficulty_code) REFERENCES public.difficulties(code)
);
CREATE TABLE public.approaches (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  verb_en text NOT NULL,
  verb_vi text NOT NULL,
  knowledge_dimension_code text,
  bloom_level_code text NOT NULL,
  question_type_code text NOT NULL,
  example_en text,
  example_vi text,
  organization_code text,
  CONSTRAINT approaches_pkey PRIMARY KEY (id),
  CONSTRAINT approaches_knowledge_dimension_code_fkey FOREIGN KEY (knowledge_dimension_code) REFERENCES public.knowledge_dimension(code),
  CONSTRAINT approaches_question_type_code_fkey FOREIGN KEY (question_type_code) REFERENCES public.question_types(code),
  CONSTRAINT approaches_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT approaches_bloom_level_code_fkey FOREIGN KEY (bloom_level_code) REFERENCES public.bloom_levels(code)
);
CREATE TABLE public.assignments (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  classroom_id uuid NOT NULL,
  exam_code text NOT NULL,
  title text NOT NULL,
  due_date timestamp with time zone,
  assigned_at timestamp with time zone NOT NULL DEFAULT now(),
  assignment_type text NOT NULL CHECK (assignment_type = ANY (ARRAY['homework'::text, 'live_exam'::text])),
  start_time timestamp with time zone,
  questions_snapshot jsonb,
  organization_code text,
  created_by uuid,
  CONSTRAINT assignments_pkey PRIMARY KEY (id),
  CONSTRAINT assignments_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT assignments_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.profiles(id),
  CONSTRAINT assignments_exam_fk FOREIGN KEY (exam_code) REFERENCES public.exams(code),
  CONSTRAINT assignments_exam_fk FOREIGN KEY (organization_code) REFERENCES public.exams(code),
  CONSTRAINT assignments_exam_fk FOREIGN KEY (exam_code) REFERENCES public.exams(organization_code),
  CONSTRAINT assignments_exam_fk FOREIGN KEY (organization_code) REFERENCES public.exams(organization_code)
);
CREATE TABLE public.bloom_levels (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  description text,
  difficulty_weight integer,
  CONSTRAINT bloom_levels_pkey PRIMARY KEY (id)
);
CREATE TABLE public.categories (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  description text,
  organization_code text NOT NULL,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  subject_codes ARRAY DEFAULT '{}'::text[],
  field_codes ARRAY DEFAULT '{}'::text[],
  created_by uuid,
  CONSTRAINT categories_pkey PRIMARY KEY (organization_code, code),
  CONSTRAINT categories_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT categories_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.profiles(id)
);
CREATE TABLE public.category_topics (
  category_code text NOT NULL,
  topic_code text NOT NULL,
  sequence_order integer NOT NULL DEFAULT 0,
  organization_code text NOT NULL,
  CONSTRAINT category_topics_pkey PRIMARY KEY (organization_code, category_code, topic_code),
  CONSTRAINT category_topics_category_fkey FOREIGN KEY (category_code) REFERENCES public.categories(code),
  CONSTRAINT category_topics_category_fkey FOREIGN KEY (organization_code) REFERENCES public.categories(code),
  CONSTRAINT category_topics_category_fkey FOREIGN KEY (category_code) REFERENCES public.categories(organization_code),
  CONSTRAINT category_topics_category_fkey FOREIGN KEY (organization_code) REFERENCES public.categories(organization_code),
  CONSTRAINT category_topics_topic_fkey FOREIGN KEY (topic_code) REFERENCES public.topics(code),
  CONSTRAINT category_topics_topic_fkey FOREIGN KEY (organization_code) REFERENCES public.topics(code),
  CONSTRAINT category_topics_topic_fkey FOREIGN KEY (topic_code) REFERENCES public.topics(organization_code),
  CONSTRAINT category_topics_topic_fkey FOREIGN KEY (organization_code) REFERENCES public.topics(organization_code)
);
CREATE TABLE public.classroom_curriculum (
  classroom_id uuid NOT NULL,
  learning_objective_code text NOT NULL,
  added_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT classroom_curriculum_pkey PRIMARY KEY (classroom_id, learning_objective_code),
  CONSTRAINT fk_classroom_curriculum_classroom FOREIGN KEY (classroom_id) REFERENCES public.classrooms(id),
  CONSTRAINT fk_classroom_curriculum_lo FOREIGN KEY (learning_objective_code) REFERENCES public.learning_objectives(code)
);
CREATE TABLE public.classroom_members (
  classroom_id uuid NOT NULL,
  student_id uuid NOT NULL,
  joined_at timestamp with time zone NOT NULL DEFAULT now(),
  status text NOT NULL DEFAULT 'pending'::text CHECK (status = ANY (ARRAY['pending'::text, 'approved'::text, 'rejected'::text])),
  CONSTRAINT classroom_members_pkey PRIMARY KEY (classroom_id, student_id),
  CONSTRAINT classroom_members_classroom_id_fkey FOREIGN KEY (classroom_id) REFERENCES public.classrooms(id),
  CONSTRAINT classroom_members_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.profiles(id)
);
CREATE TABLE public.classroom_pinned_resources (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  classroom_id uuid NOT NULL,
  resource_id uuid NOT NULL,
  pinned_by uuid,
  pinned_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT classroom_pinned_resources_pkey PRIMARY KEY (id),
  CONSTRAINT classroom_pinned_resources_classroom_id_fkey FOREIGN KEY (classroom_id) REFERENCES public.classrooms(id),
  CONSTRAINT classroom_pinned_resources_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES public.learning_resources(id),
  CONSTRAINT classroom_pinned_resources_pinned_by_fkey FOREIGN KEY (pinned_by) REFERENCES public.profiles(id)
);
CREATE TABLE public.classroom_teachers (
  classroom_id uuid NOT NULL,
  teacher_id uuid NOT NULL,
  role USER-DEFINED NOT NULL DEFAULT 'co-teacher'::classroom_teacher_role,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT classroom_teachers_pkey PRIMARY KEY (classroom_id, teacher_id),
  CONSTRAINT classroom_teachers_classroom_id_fkey FOREIGN KEY (classroom_id) REFERENCES public.classrooms(id),
  CONSTRAINT classroom_teachers_teacher_id_fkey FOREIGN KEY (teacher_id) REFERENCES public.profiles(id)
);
CREATE TABLE public.classrooms (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  class_code text NOT NULL UNIQUE,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  organization_code text,
  created_by uuid,
  course_id uuid,
  CONSTRAINT classrooms_pkey PRIMARY KEY (id),
  CONSTRAINT classrooms_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT classrooms_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.profiles(id),
  CONSTRAINT fk_classrooms_course FOREIGN KEY (course_id) REFERENCES public.courses(id)
);
CREATE TABLE public.concept_learning_objectives (
  organization_code text NOT NULL,
  concept_code text NOT NULL,
  learning_objective_code text NOT NULL,
  sequence_order integer NOT NULL DEFAULT 0,
  CONSTRAINT concept_learning_objectives_pkey PRIMARY KEY (organization_code, concept_code, learning_objective_code),
  CONSTRAINT concept_learning_objectives_organization_code_concept_code_fkey FOREIGN KEY (organization_code) REFERENCES public.concepts(code),
  CONSTRAINT concept_learning_objectives_organization_code_concept_code_fkey FOREIGN KEY (concept_code) REFERENCES public.concepts(code),
  CONSTRAINT concept_learning_objectives_organization_code_concept_code_fkey FOREIGN KEY (organization_code) REFERENCES public.concepts(organization_code),
  CONSTRAINT concept_learning_objectives_organization_code_concept_code_fkey FOREIGN KEY (concept_code) REFERENCES public.concepts(organization_code),
  CONSTRAINT concept_learning_objectives_organization_code_learning_obj_fkey FOREIGN KEY (organization_code) REFERENCES public.learning_objectives(code),
  CONSTRAINT concept_learning_objectives_organization_code_learning_obj_fkey FOREIGN KEY (learning_objective_code) REFERENCES public.learning_objectives(code),
  CONSTRAINT concept_learning_objectives_organization_code_learning_obj_fkey FOREIGN KEY (organization_code) REFERENCES public.learning_objectives(organization_code),
  CONSTRAINT concept_learning_objectives_organization_code_learning_obj_fkey FOREIGN KEY (learning_objective_code) REFERENCES public.learning_objectives(organization_code)
);
CREATE TABLE public.concepts (
  id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
  code text NOT NULL,
  name text NOT NULL,
  description text,
  organization_code text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by uuid,
  topic_codes ARRAY NOT NULL DEFAULT '{}'::text[],
  category_codes ARRAY NOT NULL DEFAULT '{}'::text[],
  subject_codes ARRAY NOT NULL DEFAULT '{}'::text[],
  field_codes ARRAY NOT NULL DEFAULT '{}'::text[],
  CONSTRAINT concepts_pkey PRIMARY KEY (organization_code, code),
  CONSTRAINT concepts_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT concepts_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.profiles(id)
);
CREATE TABLE public.contexts (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  description text,
  difficulty_weight integer,
  CONSTRAINT contexts_pkey PRIMARY KEY (id)
);
CREATE TABLE public.course_curriculum (
  course_code text NOT NULL,
  learning_objective_code text NOT NULL,
  week integer NOT NULL CHECK (week > 0),
  sequence_order integer NOT NULL DEFAULT 0,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT course_curriculum_pkey PRIMARY KEY (course_code, learning_objective_code),
  CONSTRAINT fk_course_curriculum_course FOREIGN KEY (course_code) REFERENCES public.courses(code),
  CONSTRAINT fk_course_curriculum_lo FOREIGN KEY (learning_objective_code) REFERENCES public.learning_objectives(code)
);
CREATE TABLE public.courses (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  description text,
  organization_code text,
  created_by uuid,
  curriculum_id uuid,
  sequence_order integer NOT NULL DEFAULT 0,
  CONSTRAINT courses_pkey PRIMARY KEY (id),
  CONSTRAINT courses_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT courses_curriculum_id_fkey FOREIGN KEY (curriculum_id) REFERENCES public.curriculums(id),
  CONSTRAINT courses_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.profiles(id)
);
CREATE TABLE public.curriculums (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL,
  name text NOT NULL,
  description text,
  organization_code text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by uuid,
  CONSTRAINT curriculums_pkey PRIMARY KEY (id),
  CONSTRAINT curriculums_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT curriculums_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.profiles(id)
);
CREATE TABLE public.difficulties (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  description text,
  CONSTRAINT difficulties_pkey PRIMARY KEY (id)
);
CREATE TABLE public.exam_blueprints (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL,
  name text NOT NULL,
  teacher_id uuid NOT NULL,
  organization_code text NOT NULL,
  exam_type_code text NOT NULL,
  blueprint_data jsonb NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT exam_blueprints_pkey PRIMARY KEY (id),
  CONSTRAINT exam_blueprints_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT exam_blueprints_teacher_id_fkey FOREIGN KEY (teacher_id) REFERENCES public.profiles(id),
  CONSTRAINT exam_blueprints_exam_type_code_fkey FOREIGN KEY (organization_code) REFERENCES public.exam_types(code),
  CONSTRAINT exam_blueprints_exam_type_code_fkey FOREIGN KEY (exam_type_code) REFERENCES public.exam_types(code),
  CONSTRAINT exam_blueprints_exam_type_code_fkey FOREIGN KEY (organization_code) REFERENCES public.exam_types(organization_code),
  CONSTRAINT exam_blueprints_exam_type_code_fkey FOREIGN KEY (exam_type_code) REFERENCES public.exam_types(organization_code)
);
CREATE TABLE public.exam_types (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL,
  name text NOT NULL,
  description text,
  exam_type text NOT NULL,
  question_range int4range NOT NULL,
  duration_range int4range NOT NULL,
  organization_code text NOT NULL,
  grade_codes ARRAY NOT NULL DEFAULT '{}'::text[],
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT exam_types_pkey PRIMARY KEY (id),
  CONSTRAINT exam_types_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code)
);
CREATE TABLE public.exams (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL,
  name text NOT NULL,
  description text,
  question_codes ARRAY NOT NULL,
  settings jsonb NOT NULL,
  last_modified timestamp with time zone NOT NULL DEFAULT now(),
  organization_code text,
  exam_blueprint_code text,
  exam_type_code text,
  created_by uuid,
  CONSTRAINT exams_pkey PRIMARY KEY (id),
  CONSTRAINT exams_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT exams_exam_blueprint_code_fkey FOREIGN KEY (organization_code) REFERENCES public.exam_blueprints(code),
  CONSTRAINT exams_exam_blueprint_code_fkey FOREIGN KEY (exam_blueprint_code) REFERENCES public.exam_blueprints(code),
  CONSTRAINT exams_exam_blueprint_code_fkey FOREIGN KEY (organization_code) REFERENCES public.exam_blueprints(organization_code),
  CONSTRAINT exams_exam_blueprint_code_fkey FOREIGN KEY (exam_blueprint_code) REFERENCES public.exam_blueprints(organization_code),
  CONSTRAINT exams_exam_type_code_fkey FOREIGN KEY (organization_code) REFERENCES public.exam_types(code),
  CONSTRAINT exams_exam_type_code_fkey FOREIGN KEY (exam_type_code) REFERENCES public.exam_types(code),
  CONSTRAINT exams_exam_type_code_fkey FOREIGN KEY (organization_code) REFERENCES public.exam_types(organization_code),
  CONSTRAINT exams_exam_type_code_fkey FOREIGN KEY (exam_type_code) REFERENCES public.exam_types(organization_code),
  CONSTRAINT exams_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.profiles(id)
);
CREATE TABLE public.field_subjects (
  organization_code text NOT NULL,
  field_code text NOT NULL,
  subject_code text NOT NULL,
  sequence_order integer NOT NULL DEFAULT 0,
  CONSTRAINT field_subjects_pkey PRIMARY KEY (organization_code, field_code, subject_code),
  CONSTRAINT field_subjects_organization_code_field_code_fkey FOREIGN KEY (organization_code) REFERENCES public.fields(code),
  CONSTRAINT field_subjects_organization_code_field_code_fkey FOREIGN KEY (field_code) REFERENCES public.fields(code),
  CONSTRAINT field_subjects_organization_code_field_code_fkey FOREIGN KEY (organization_code) REFERENCES public.fields(organization_code),
  CONSTRAINT field_subjects_organization_code_field_code_fkey FOREIGN KEY (field_code) REFERENCES public.fields(organization_code),
  CONSTRAINT field_subjects_organization_code_subject_code_fkey FOREIGN KEY (organization_code) REFERENCES public.subjects(code),
  CONSTRAINT field_subjects_organization_code_subject_code_fkey FOREIGN KEY (subject_code) REFERENCES public.subjects(code),
  CONSTRAINT field_subjects_organization_code_subject_code_fkey FOREIGN KEY (organization_code) REFERENCES public.subjects(organization_code),
  CONSTRAINT field_subjects_organization_code_subject_code_fkey FOREIGN KEY (subject_code) REFERENCES public.subjects(organization_code)
);
CREATE TABLE public.fields (
  id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
  code text NOT NULL,
  name text NOT NULL,
  description text,
  organization_code text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by uuid,
  CONSTRAINT fields_pkey PRIMARY KEY (organization_code, code),
  CONSTRAINT fields_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT fields_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.profiles(id)
);
CREATE TABLE public.glossaries (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  description text,
  content jsonb,
  organization_code text,
  CONSTRAINT glossaries_pkey PRIMARY KEY (id),
  CONSTRAINT glossaries_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code)
);
CREATE TABLE public.grade_levels (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  organization_code text,
  description text,
  CONSTRAINT grade_levels_pkey PRIMARY KEY (id),
  CONSTRAINT grade_levels_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code)
);
CREATE TABLE public.iostem_questions (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT iostem_questions_pkey PRIMARY KEY (id)
);
CREATE TABLE public.knowledge_dimension (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  description text,
  difficulty_weight integer,
  CONSTRAINT knowledge_dimension_pkey PRIMARY KEY (id)
);
CREATE TABLE public.learning_objective_glossaries (
  learning_objective_code text NOT NULL,
  glossary_code text NOT NULL,
  CONSTRAINT learning_objective_glossaries_pkey PRIMARY KEY (learning_objective_code, glossary_code),
  CONSTRAINT learning_objective_glossaries_lo_code_fkey FOREIGN KEY (learning_objective_code) REFERENCES public.learning_objectives(code),
  CONSTRAINT learning_objective_glossaries_glossary_code_fkey FOREIGN KEY (glossary_code) REFERENCES public.glossaries(code)
);
CREATE TABLE public.learning_objective_prerequisites (
  learning_objective_code text NOT NULL,
  prerequisite_lo_code text NOT NULL,
  CONSTRAINT learning_objective_prerequisites_pkey PRIMARY KEY (learning_objective_code, prerequisite_lo_code),
  CONSTRAINT learning_objective_prerequisites_learning_objective_code_fkey FOREIGN KEY (learning_objective_code) REFERENCES public.learning_objectives(code),
  CONSTRAINT learning_objective_prerequisites_prerequisite_lo_code_fkey FOREIGN KEY (prerequisite_lo_code) REFERENCES public.learning_objectives(code)
);
CREATE TABLE public.learning_objective_resources (
  learning_objective_code text NOT NULL,
  resource_code text NOT NULL,
  CONSTRAINT learning_objective_resources_pkey PRIMARY KEY (learning_objective_code, resource_code),
  CONSTRAINT learning_objective_resources_learning_objective_code_fkey FOREIGN KEY (learning_objective_code) REFERENCES public.learning_objectives(code),
  CONSTRAINT learning_objective_resources_resource_code_fkey FOREIGN KEY (resource_code) REFERENCES public.learning_resources(code)
);
CREATE TABLE public.learning_objectives (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  description text,
  keywords ARRAY,
  organization_code text NOT NULL,
  lo_type text NOT NULL DEFAULT 'SPECIFIC_IMPL'::text CHECK (lo_type = ANY (ARRAY['UNIVERSAL'::text, 'CONCEPTUAL_IMPL'::text, 'SPECIFIC_IMPL'::text])),
  parent_lo_code text,
  context_codes ARRAY NOT NULL DEFAULT '{}'::text[],
  bloom_level_codes ARRAY NOT NULL DEFAULT '{}'::text[],
  updated_at timestamp with time zone DEFAULT now(),
  topic_codes ARRAY DEFAULT '{}'::text[],
  category_codes ARRAY DEFAULT '{}'::text[],
  subject_codes ARRAY DEFAULT '{}'::text[],
  field_codes ARRAY DEFAULT '{}'::text[],
  created_at timestamp with time zone DEFAULT now(),
  created_by uuid,
  concept_codes ARRAY DEFAULT '{}'::text[],
  CONSTRAINT learning_objectives_pkey PRIMARY KEY (organization_code, code),
  CONSTRAINT learning_objectives_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT learning_objectives_parent_fkey FOREIGN KEY (parent_lo_code) REFERENCES public.learning_objectives(code),
  CONSTRAINT learning_objectives_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.profiles(id)
);
CREATE TABLE public.learning_resources (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL UNIQUE,
  title text NOT NULL,
  description text,
  resource_type text NOT NULL,
  url text,
  storage_path text,
  file_metadata jsonb,
  organization_code text,
  created_by uuid,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT learning_resources_pkey PRIMARY KEY (id),
  CONSTRAINT learning_resources_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT learning_resources_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.profiles(id),
  CONSTRAINT learning_resources_resource_type_fkey FOREIGN KEY (resource_type) REFERENCES public.resource_types(code)
);
CREATE TABLE public.lesson_activities (
  lesson_id uuid NOT NULL,
  activity_id uuid NOT NULL,
  sequence_order integer NOT NULL DEFAULT 0,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT lesson_activities_pkey PRIMARY KEY (lesson_id, activity_id),
  CONSTRAINT lesson_activities_lesson_id_fkey FOREIGN KEY (lesson_id) REFERENCES public.lessons(id),
  CONSTRAINT lesson_activities_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activities(id)
);
CREATE TABLE public.lesson_resources (
  lesson_id uuid NOT NULL,
  resource_id uuid NOT NULL,
  sequence_order integer NOT NULL DEFAULT 0,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT lesson_resources_pkey PRIMARY KEY (lesson_id, resource_id),
  CONSTRAINT lesson_resources_lesson_id_fkey FOREIGN KEY (lesson_id) REFERENCES public.lessons(id),
  CONSTRAINT lesson_resources_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES public.learning_resources(id)
);
CREATE TABLE public.lessons (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  module_id uuid NOT NULL,
  name text NOT NULL,
  description text,
  sequence_order integer NOT NULL DEFAULT 0,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  organization_code text NOT NULL,
  code text NOT NULL,
  CONSTRAINT lessons_pkey PRIMARY KEY (id),
  CONSTRAINT lessons_module_id_fkey FOREIGN KEY (module_id) REFERENCES public.modules(id),
  CONSTRAINT lessons_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code)
);
CREATE TABLE public.live_exam_participants (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  session_id uuid NOT NULL,
  real_name text,
  nickname text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  participant_id text NOT NULL DEFAULT replace((gen_random_uuid())::text, '-'::text, ''::text) UNIQUE,
  CONSTRAINT live_exam_participants_pkey PRIMARY KEY (id),
  CONSTRAINT live_exam_participants_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.live_exam_sessions(id)
);
CREATE TABLE public.live_exam_sessions (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  short_code text NOT NULL UNIQUE,
  exam_code text NOT NULL,
  teacher_id uuid NOT NULL,
  organization_code text NOT NULL,
  status USER-DEFINED NOT NULL DEFAULT 'lobby'::live_session_status,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  closed_at timestamp with time zone,
  name text NOT NULL,
  challenge_starts_at timestamp with time zone,
  CONSTRAINT live_exam_sessions_pkey PRIMARY KEY (id),
  CONSTRAINT live_exam_sessions_teacher_id_fkey FOREIGN KEY (teacher_id) REFERENCES public.profiles(id),
  CONSTRAINT live_exam_sessions_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT live_exam_sessions_exam_fk FOREIGN KEY (exam_code) REFERENCES public.exams(code),
  CONSTRAINT live_exam_sessions_exam_fk FOREIGN KEY (organization_code) REFERENCES public.exams(code),
  CONSTRAINT live_exam_sessions_exam_fk FOREIGN KEY (exam_code) REFERENCES public.exams(organization_code),
  CONSTRAINT live_exam_sessions_exam_fk FOREIGN KEY (organization_code) REFERENCES public.exams(organization_code)
);
CREATE TABLE public.live_session_progress (
  participant_id text NOT NULL,
  session_id uuid NOT NULL,
  completed_count integer NOT NULL DEFAULT 0,
  total_count integer NOT NULL DEFAULT 0,
  last_updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT live_session_progress_pkey PRIMARY KEY (participant_id),
  CONSTRAINT live_session_progress_participant_id_fkey FOREIGN KEY (participant_id) REFERENCES public.live_exam_participants(participant_id),
  CONSTRAINT live_session_progress_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.live_exam_sessions(id)
);
CREATE TABLE public.modules (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  unit_id uuid NOT NULL,
  name text NOT NULL,
  description text,
  sequence_order integer NOT NULL DEFAULT 0,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  organization_code text NOT NULL,
  code text NOT NULL,
  CONSTRAINT modules_pkey PRIMARY KEY (id),
  CONSTRAINT modules_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.units(id),
  CONSTRAINT modules_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code)
);
CREATE TABLE public.notifications (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  message text NOT NULL,
  link_href text,
  is_read boolean NOT NULL DEFAULT false,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  organization_code text,
  CONSTRAINT notifications_pkey PRIMARY KEY (id),
  CONSTRAINT notifications_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.profiles(id)
);
CREATE TABLE public.organizations (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  code text NOT NULL UNIQUE,
  created_by uuid,
  CONSTRAINT organizations_pkey PRIMARY KEY (id),
  CONSTRAINT organizations_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.profiles(id)
);
CREATE TABLE public.profiles (
  id uuid NOT NULL,
  full_name text,
  avatar_url text,
  updated_at timestamp with time zone,
  role text DEFAULT 'user'::text CHECK (role = ANY (ARRAY['user'::text, 'student'::text, 'teacher'::text, 'editor'::text, 'admin'::text, 'org_admin'::text])),
  personal_settings jsonb,
  organization_code text,
  permissions jsonb DEFAULT '{}'::jsonb,
  CONSTRAINT profiles_pkey PRIMARY KEY (id),
  CONSTRAINT profiles_id_fkey FOREIGN KEY (id) REFERENCES auth.users(id),
  CONSTRAINT profiles_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code)
);
CREATE TABLE public.question_glossary_links (
  question_code text NOT NULL,
  glossary_code text NOT NULL,
  organization_code text,
  CONSTRAINT question_glossary_links_pkey PRIMARY KEY (question_code, glossary_code),
  CONSTRAINT question_glossary_links_glossary_code_fkey FOREIGN KEY (glossary_code) REFERENCES public.glossaries(code),
  CONSTRAINT question_glossary_links_question_fkey FOREIGN KEY (question_code) REFERENCES public.questions(code),
  CONSTRAINT question_glossary_links_question_fkey FOREIGN KEY (organization_code) REFERENCES public.questions(code),
  CONSTRAINT question_glossary_links_question_fkey FOREIGN KEY (question_code) REFERENCES public.questions(organization_code),
  CONSTRAINT question_glossary_links_question_fkey FOREIGN KEY (organization_code) REFERENCES public.questions(organization_code)
);
CREATE TABLE public.question_learning_objectives (
  question_code text NOT NULL,
  learning_objective_code text NOT NULL,
  organization_code text,
  CONSTRAINT question_learning_objectives_pkey PRIMARY KEY (question_code, learning_objective_code),
  CONSTRAINT question_learning_objectives_lo_code_fkey FOREIGN KEY (learning_objective_code) REFERENCES public.learning_objectives(code),
  CONSTRAINT question_learning_objectives_question_fkey FOREIGN KEY (question_code) REFERENCES public.questions(code),
  CONSTRAINT question_learning_objectives_question_fkey FOREIGN KEY (organization_code) REFERENCES public.questions(code),
  CONSTRAINT question_learning_objectives_question_fkey FOREIGN KEY (question_code) REFERENCES public.questions(organization_code),
  CONSTRAINT question_learning_objectives_question_fkey FOREIGN KEY (organization_code) REFERENCES public.questions(organization_code)
);
CREATE TABLE public.question_types (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  description text,
  difficulty_weight integer,
  CONSTRAINT question_types_pkey PRIMARY KEY (id)
);
CREATE TABLE public.questions (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL,
  text text NOT NULL,
  last_modified timestamp with time zone NOT NULL DEFAULT now(),
  question_type_code text,
  question_config jsonb NOT NULL,
  difficulty_code text NOT NULL,
  organization_code text,
  subject_codes ARRAY NOT NULL DEFAULT '{}'::text[],
  category_codes ARRAY NOT NULL DEFAULT '{}'::text[],
  topic_codes ARRAY NOT NULL DEFAULT '{}'::text[],
  knowledge_dimension_code text,
  learning_objective_codes ARRAY NOT NULL DEFAULT '{}'::text[],
  grade_level_codes ARRAY DEFAULT '{}'::text[],
  created_by uuid,
  created_at timestamp with time zone DEFAULT (now() AT TIME ZONE 'utc'::text),
  field_codes ARRAY DEFAULT '{}'::text[],
  context_code text,
  concept_codes ARRAY NOT NULL DEFAULT '{}'::text[],
  bloom_level_code text,
  CONSTRAINT questions_pkey PRIMARY KEY (id),
  CONSTRAINT questions_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT questions_question_type_code_fkey FOREIGN KEY (question_type_code) REFERENCES public.question_types(code),
  CONSTRAINT questions_difficulty_code_fkey FOREIGN KEY (difficulty_code) REFERENCES public.difficulties(code),
  CONSTRAINT questions_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.profiles(id),
  CONSTRAINT questions_context_code_fkey FOREIGN KEY (context_code) REFERENCES public.contexts(code)
);
CREATE TABLE public.resource_types (
  code text NOT NULL,
  name text NOT NULL,
  description text,
  icon text,
  CONSTRAINT resource_types_pkey PRIMARY KEY (code)
);
CREATE TABLE public.role_permissions (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  role USER-DEFINED NOT NULL,
  permission USER-DEFINED NOT NULL,
  CONSTRAINT role_permissions_pkey PRIMARY KEY (id)
);
CREATE TABLE public.student_mastery (
  student_id uuid NOT NULL,
  learning_objective_code text NOT NULL,
  mastery_level text NOT NULL DEFAULT 'not_started'::text CHECK (mastery_level = ANY (ARRAY['not_started'::text, 'in_progress'::text, 'mastered'::text])),
  mastery_score numeric CHECK (mastery_score >= 0::numeric AND mastery_score <= 100::numeric),
  assessed_at timestamp with time zone,
  evidence_submission_id uuid,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  attempt_count integer NOT NULL DEFAULT 0,
  correct_attempts integer NOT NULL DEFAULT 0,
  confidence_score numeric,
  last_attempt_correct boolean,
  CONSTRAINT student_mastery_pkey PRIMARY KEY (student_id, learning_objective_code),
  CONSTRAINT student_mastery_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.profiles(id),
  CONSTRAINT student_mastery_lo_code_fkey FOREIGN KEY (learning_objective_code) REFERENCES public.learning_objectives(code),
  CONSTRAINT student_mastery_submission_id_fkey FOREIGN KEY (evidence_submission_id) REFERENCES public.submissions(id)
);
CREATE TABLE public.subject_categories (
  subject_code text NOT NULL,
  category_code text NOT NULL,
  sequence_order integer NOT NULL DEFAULT 0,
  organization_code text NOT NULL,
  CONSTRAINT subject_categories_pkey PRIMARY KEY (organization_code, subject_code, category_code),
  CONSTRAINT subject_categories_subject_fkey FOREIGN KEY (subject_code) REFERENCES public.subjects(code),
  CONSTRAINT subject_categories_subject_fkey FOREIGN KEY (organization_code) REFERENCES public.subjects(code),
  CONSTRAINT subject_categories_subject_fkey FOREIGN KEY (subject_code) REFERENCES public.subjects(organization_code),
  CONSTRAINT subject_categories_subject_fkey FOREIGN KEY (organization_code) REFERENCES public.subjects(organization_code),
  CONSTRAINT subject_categories_category_fkey FOREIGN KEY (category_code) REFERENCES public.categories(code),
  CONSTRAINT subject_categories_category_fkey FOREIGN KEY (organization_code) REFERENCES public.categories(code),
  CONSTRAINT subject_categories_category_fkey FOREIGN KEY (category_code) REFERENCES public.categories(organization_code),
  CONSTRAINT subject_categories_category_fkey FOREIGN KEY (organization_code) REFERENCES public.categories(organization_code)
);
CREATE TABLE public.subjects (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  description text,
  organization_code text NOT NULL,
  field_codes ARRAY DEFAULT '{}'::text[],
  created_by uuid,
  CONSTRAINT subjects_pkey PRIMARY KEY (organization_code, code),
  CONSTRAINT subjects_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT subjects_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.profiles(id)
);
CREATE TABLE public.submission_reviews (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  submission_id uuid NOT NULL UNIQUE,
  review_content jsonb,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT submission_reviews_pkey PRIMARY KEY (id),
  CONSTRAINT submission_reviews_submission_id_fkey FOREIGN KEY (submission_id) REFERENCES public.submissions(id)
);
CREATE TABLE public.submissions (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  student_id uuid,
  context_code text NOT NULL,
  score real,
  started_at timestamp with time zone NOT NULL DEFAULT now(),
  completed_at timestamp with time zone,
  session_data jsonb,
  submitted_at timestamp with time zone NOT NULL DEFAULT now(),
  assignment_id uuid,
  submission_type text NOT NULL DEFAULT 'assignment'::text CHECK (submission_type = ANY (ARRAY['assignment'::text, 'practice'::text, 'exam'::text, 'live_exam'::text])),
  classroom_id uuid,
  organization_code text,
  live_exam_session_id uuid,
  live_exam_participant_id text,
  CONSTRAINT submissions_pkey PRIMARY KEY (id),
  CONSTRAINT submissions_assignment_id_fkey FOREIGN KEY (assignment_id) REFERENCES public.assignments(id),
  CONSTRAINT submissions_classroom_id_fkey FOREIGN KEY (classroom_id) REFERENCES public.classrooms(id),
  CONSTRAINT submissions_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT fk_student_test_attempts_student FOREIGN KEY (student_id) REFERENCES public.profiles(id),
  CONSTRAINT submissions_live_exam_session_id_fkey FOREIGN KEY (live_exam_session_id) REFERENCES public.live_exam_sessions(id),
  CONSTRAINT submissions_live_exam_participant_id_fkey FOREIGN KEY (live_exam_participant_id) REFERENCES public.live_exam_participants(participant_id)
);
CREATE TABLE public.topic_concepts (
  organization_code text NOT NULL,
  topic_code text NOT NULL,
  concept_code text NOT NULL,
  sequence_order integer NOT NULL DEFAULT 0,
  CONSTRAINT topic_concepts_pkey PRIMARY KEY (organization_code, topic_code, concept_code),
  CONSTRAINT topic_concepts_organization_code_topic_code_fkey FOREIGN KEY (organization_code) REFERENCES public.topics(code),
  CONSTRAINT topic_concepts_organization_code_topic_code_fkey FOREIGN KEY (topic_code) REFERENCES public.topics(code),
  CONSTRAINT topic_concepts_organization_code_topic_code_fkey FOREIGN KEY (organization_code) REFERENCES public.topics(organization_code),
  CONSTRAINT topic_concepts_organization_code_topic_code_fkey FOREIGN KEY (topic_code) REFERENCES public.topics(organization_code),
  CONSTRAINT topic_concepts_organization_code_concept_code_fkey FOREIGN KEY (organization_code) REFERENCES public.concepts(code),
  CONSTRAINT topic_concepts_organization_code_concept_code_fkey FOREIGN KEY (concept_code) REFERENCES public.concepts(code),
  CONSTRAINT topic_concepts_organization_code_concept_code_fkey FOREIGN KEY (organization_code) REFERENCES public.concepts(organization_code),
  CONSTRAINT topic_concepts_organization_code_concept_code_fkey FOREIGN KEY (concept_code) REFERENCES public.concepts(organization_code)
);
CREATE TABLE public.topics (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  description text,
  organization_code text NOT NULL,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  category_codes ARRAY DEFAULT '{}'::text[],
  subject_codes ARRAY DEFAULT '{}'::text[],
  field_codes ARRAY DEFAULT '{}'::text[],
  created_by uuid,
  CONSTRAINT topics_pkey PRIMARY KEY (organization_code, code),
  CONSTRAINT topics_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code),
  CONSTRAINT topics_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.profiles(id)
);
CREATE TABLE public.units (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  course_id uuid NOT NULL,
  name text NOT NULL,
  description text,
  sequence_order integer NOT NULL DEFAULT 0,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  organization_code text NOT NULL,
  code text NOT NULL,
  CONSTRAINT units_pkey PRIMARY KEY (id),
  CONSTRAINT units_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id),
  CONSTRAINT units_organization_code_fkey FOREIGN KEY (organization_code) REFERENCES public.organizations(code)
);