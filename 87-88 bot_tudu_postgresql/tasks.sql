PGDMP                       |         	   bot_tasks    16.6    16.6     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    32954 	   bot_tasks    DATABASE     }   CREATE DATABASE bot_tasks WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE bot_tasks;
                postgres    false            �            1259    32956    task    TABLE     �   CREATE TABLE public.task (
    name character varying(500),
    id integer NOT NULL,
    user_id integer,
    status character varying
);
    DROP TABLE public.task;
       public         heap    postgres    false            �            1259    32955    task_id_seq    SEQUENCE     �   ALTER TABLE public.task ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.task_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    216            �            1259    32969    user    TABLE     m   CREATE TABLE public."user" (
    id integer NOT NULL,
    telegram_id integer,
    name character varying
);
    DROP TABLE public."user";
       public         heap    postgres    false            �          0    32956    task 
   TABLE DATA           9   COPY public.task (name, id, user_id, status) FROM stdin;
    public          postgres    false    216   �       �          0    32969    user 
   TABLE DATA           7   COPY public."user" (id, telegram_id, name) FROM stdin;
    public          postgres    false    217   1       �           0    0    task_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('public.task_id_seq', 7, true);
          public          postgres    false    215                       2606    32960    task task_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.task DROP CONSTRAINT task_pkey;
       public            postgres    false    216            !           2606    32975    user user_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public."user" DROP CONSTRAINT user_pkey;
       public            postgres    false    217            "           2606    32976    task task_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) NOT VALID;
 @   ALTER TABLE ONLY public.task DROP CONSTRAINT task_user_id_fkey;
       public          postgres    false    4641    216    217            �   t   x���162�4�?�0��)�4�2rRS8M ��/��$7\l���i
�~a�ņ{/��4�*�ra��6���., 26�5]��i����b7� ���v������ ��?      �      x�3�44�,*�2�427765�pc���� NQD     