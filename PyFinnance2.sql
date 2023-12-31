PGDMP     
                  
    {            PyFinanceDB    15.4    15.4 .    +           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            ,           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            -           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            .           1262    16398    PyFinanceDB    DATABASE     �   CREATE DATABASE "PyFinanceDB" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Spain.1252';
    DROP DATABASE "PyFinanceDB";
                postgres    false            /           0    0    DATABASE "PyFinanceDB"    COMMENT     P   COMMENT ON DATABASE "PyFinanceDB" IS 'Base de datos para pagina web PyFinance';
                   postgres    false    3374            �            1259    16433    Grupos    TABLE     �   CREATE TABLE public."Grupos" (
    "ID_grupo" bigint NOT NULL,
    "Nombre_grupo" character varying(50) NOT NULL,
    "ID_administrador" bigint NOT NULL,
    "Descripción" text,
    "Contrasena" character varying(30) NOT NULL
);
    DROP TABLE public."Grupos";
       public         heap    postgres    false            0           0    0    TABLE "Grupos"    COMMENT     �   COMMENT ON TABLE public."Grupos" IS 'Tabla que contiene a los grupos en los que están los usuarios registrados en PyFinance.';
          public          postgres    false    218            �            1259    16432    Grupos_ID_administrador_seq    SEQUENCE     �   CREATE SEQUENCE public."Grupos_ID_administrador_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public."Grupos_ID_administrador_seq";
       public          postgres    false    218            1           0    0    Grupos_ID_administrador_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public."Grupos_ID_administrador_seq" OWNED BY public."Grupos"."ID_administrador";
          public          postgres    false    217            �            1259    16431    Grupos_ID_grupo_seq    SEQUENCE     ~   CREATE SEQUENCE public."Grupos_ID_grupo_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public."Grupos_ID_grupo_seq";
       public          postgres    false    218            2           0    0    Grupos_ID_grupo_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public."Grupos_ID_grupo_seq" OWNED BY public."Grupos"."ID_grupo";
          public          postgres    false    216            �            1259    16536    Paga    TABLE     �   CREATE TABLE public."Paga" (
    "ID_usr" bigint NOT NULL,
    "ID_pag" bigint NOT NULL,
    "Fecha" date NOT NULL,
    "Cantidad" real NOT NULL
);
    DROP TABLE public."Paga";
       public         heap    postgres    false            �            1259    16453    Pagos    TABLE     h  CREATE TABLE public."Pagos" (
    "ID_pago" bigint NOT NULL,
    "Nombre_pago" character varying(50) NOT NULL,
    "Fecha_creacion" date NOT NULL,
    "Fecha_pago" date NOT NULL,
    "Estatus_pago" boolean DEFAULT false NOT NULL,
    "Progreso_pago" real DEFAULT 0.00 NOT NULL,
    "ID_grupo" integer,
    "Cantidad_a_pagar" real,
    "Cantidad_total" real
);
    DROP TABLE public."Pagos";
       public         heap    postgres    false            �            1259    16452    Pagos_ID_pago_seq    SEQUENCE     |   CREATE SEQUENCE public."Pagos_ID_pago_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public."Pagos_ID_pago_seq";
       public          postgres    false    220            3           0    0    Pagos_ID_pago_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public."Pagos_ID_pago_seq" OWNED BY public."Pagos"."ID_pago";
          public          postgres    false    219            �            1259    16551 	   Pertenece    TABLE     �   CREATE TABLE public."Pertenece" (
    "ID_usr" bigint NOT NULL,
    "ID_gru" bigint NOT NULL,
    "Fecha" date NOT NULL,
    "Administra" boolean DEFAULT false NOT NULL
);
    DROP TABLE public."Pertenece";
       public         heap    postgres    false            �            1259    16420    Usuarios    TABLE     \  CREATE TABLE public."Usuarios" (
    "ID_usuario" bigint NOT NULL,
    "Nickname" character varying(50) NOT NULL,
    "Nombre" character varying(30) NOT NULL,
    "Apellidos" character varying(50) NOT NULL,
    "Correo" character varying(60) NOT NULL,
    "Contrasena" character varying(30) NOT NULL,
    "Estatus" boolean DEFAULT true NOT NULL
);
    DROP TABLE public."Usuarios";
       public         heap    postgres    false            4           0    0    TABLE "Usuarios"    COMMENT     W   COMMENT ON TABLE public."Usuarios" IS 'Tabla que contendra los datos de los usuarios';
          public          postgres    false    215            �            1259    16419    Usuarios_ID_usuario_seq    SEQUENCE     �   CREATE SEQUENCE public."Usuarios_ID_usuario_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public."Usuarios_ID_usuario_seq";
       public          postgres    false    215            5           0    0    Usuarios_ID_usuario_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public."Usuarios_ID_usuario_seq" OWNED BY public."Usuarios"."ID_usuario";
          public          postgres    false    214            z           2604    16436    Grupos ID_grupo    DEFAULT     x   ALTER TABLE ONLY public."Grupos" ALTER COLUMN "ID_grupo" SET DEFAULT nextval('public."Grupos_ID_grupo_seq"'::regclass);
 B   ALTER TABLE public."Grupos" ALTER COLUMN "ID_grupo" DROP DEFAULT;
       public          postgres    false    218    216    218            {           2604    16437    Grupos ID_administrador    DEFAULT     �   ALTER TABLE ONLY public."Grupos" ALTER COLUMN "ID_administrador" SET DEFAULT nextval('public."Grupos_ID_administrador_seq"'::regclass);
 J   ALTER TABLE public."Grupos" ALTER COLUMN "ID_administrador" DROP DEFAULT;
       public          postgres    false    217    218    218            |           2604    16456    Pagos ID_pago    DEFAULT     t   ALTER TABLE ONLY public."Pagos" ALTER COLUMN "ID_pago" SET DEFAULT nextval('public."Pagos_ID_pago_seq"'::regclass);
 @   ALTER TABLE public."Pagos" ALTER COLUMN "ID_pago" DROP DEFAULT;
       public          postgres    false    219    220    220            x           2604    16423    Usuarios ID_usuario    DEFAULT     �   ALTER TABLE ONLY public."Usuarios" ALTER COLUMN "ID_usuario" SET DEFAULT nextval('public."Usuarios_ID_usuario_seq"'::regclass);
 F   ALTER TABLE public."Usuarios" ALTER COLUMN "ID_usuario" DROP DEFAULT;
       public          postgres    false    214    215    215            $          0    16433    Grupos 
   TABLE DATA           p   COPY public."Grupos" ("ID_grupo", "Nombre_grupo", "ID_administrador", "Descripción", "Contrasena") FROM stdin;
    public          postgres    false    218   R7       '          0    16536    Paga 
   TABLE DATA           I   COPY public."Paga" ("ID_usr", "ID_pag", "Fecha", "Cantidad") FROM stdin;
    public          postgres    false    221   �7       &          0    16453    Pagos 
   TABLE DATA           �   COPY public."Pagos" ("ID_pago", "Nombre_pago", "Fecha_creacion", "Fecha_pago", "Estatus_pago", "Progreso_pago", "ID_grupo", "Cantidad_a_pagar", "Cantidad_total") FROM stdin;
    public          postgres    false    220   �7       (          0    16551 	   Pertenece 
   TABLE DATA           P   COPY public."Pertenece" ("ID_usr", "ID_gru", "Fecha", "Administra") FROM stdin;
    public          postgres    false    222   8       !          0    16420    Usuarios 
   TABLE DATA           x   COPY public."Usuarios" ("ID_usuario", "Nickname", "Nombre", "Apellidos", "Correo", "Contrasena", "Estatus") FROM stdin;
    public          postgres    false    215   ;8       6           0    0    Grupos_ID_administrador_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public."Grupos_ID_administrador_seq"', 1, false);
          public          postgres    false    217            7           0    0    Grupos_ID_grupo_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public."Grupos_ID_grupo_seq"', 1, true);
          public          postgres    false    216            8           0    0    Pagos_ID_pago_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."Pagos_ID_pago_seq"', 2, true);
          public          postgres    false    219            9           0    0    Usuarios_ID_usuario_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public."Usuarios_ID_usuario_seq"', 7, true);
          public          postgres    false    214            �           2606    16568    Usuarios Correo 
   CONSTRAINT     R   ALTER TABLE ONLY public."Usuarios"
    ADD CONSTRAINT "Correo" UNIQUE ("Correo");
 =   ALTER TABLE ONLY public."Usuarios" DROP CONSTRAINT "Correo";
       public            postgres    false    215            :           0    0 !   CONSTRAINT "Correo" ON "Usuarios"    COMMENT     X   COMMENT ON CONSTRAINT "Correo" ON public."Usuarios" IS 'El correo no se puede repetir';
          public          postgres    false    3201            �           2606    16441    Grupos Grupos_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public."Grupos"
    ADD CONSTRAINT "Grupos_pkey" PRIMARY KEY ("ID_grupo");
 @   ALTER TABLE ONLY public."Grupos" DROP CONSTRAINT "Grupos_pkey";
       public            postgres    false    218            �           2606    16462    Pagos Pagos_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public."Pagos"
    ADD CONSTRAINT "Pagos_pkey" PRIMARY KEY ("ID_pago");
 >   ALTER TABLE ONLY public."Pagos" DROP CONSTRAINT "Pagos_pkey";
       public            postgres    false    220            �           2606    16428    Usuarios Usuarios_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public."Usuarios"
    ADD CONSTRAINT "Usuarios_pkey" PRIMARY KEY ("ID_usuario");
 D   ALTER TABLE ONLY public."Usuarios" DROP CONSTRAINT "Usuarios_pkey";
       public            postgres    false    215            �           2606    16555    Pertenece usr_gru_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public."Pertenece"
    ADD CONSTRAINT usr_gru_pkey PRIMARY KEY ("ID_usr", "ID_gru");
 B   ALTER TABLE ONLY public."Pertenece" DROP CONSTRAINT usr_gru_pkey;
       public            postgres    false    222    222            �           2606    16540    Paga usr_pag_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY public."Paga"
    ADD CONSTRAINT usr_pag_pkey PRIMARY KEY ("ID_usr", "ID_pag");
 =   ALTER TABLE ONLY public."Paga" DROP CONSTRAINT usr_pag_pkey;
       public            postgres    false    221    221            �           2606    16676    Grupos FK_ID_administrador    FK CONSTRAINT     �   ALTER TABLE ONLY public."Grupos"
    ADD CONSTRAINT "FK_ID_administrador" FOREIGN KEY ("ID_administrador") REFERENCES public."Usuarios"("ID_usuario") ON UPDATE CASCADE ON DELETE CASCADE;
 H   ALTER TABLE ONLY public."Grupos" DROP CONSTRAINT "FK_ID_administrador";
       public          postgres    false    3203    215    218            �           2606    16706    Pagos FK_ID_grupo    FK CONSTRAINT     �   ALTER TABLE ONLY public."Pagos"
    ADD CONSTRAINT "FK_ID_grupo" FOREIGN KEY ("ID_grupo") REFERENCES public."Grupos"("ID_grupo") ON UPDATE CASCADE ON DELETE CASCADE;
 ?   ALTER TABLE ONLY public."Pagos" DROP CONSTRAINT "FK_ID_grupo";
       public          postgres    false    218    220    3205            �           2606    16681    Paga Paga_ID_pag_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Paga"
    ADD CONSTRAINT "Paga_ID_pag_fkey" FOREIGN KEY ("ID_pag") REFERENCES public."Pagos"("ID_pago") ON UPDATE CASCADE ON DELETE CASCADE;
 C   ALTER TABLE ONLY public."Paga" DROP CONSTRAINT "Paga_ID_pag_fkey";
       public          postgres    false    221    3207    220            �           2606    16686    Paga Paga_ID_usr_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Paga"
    ADD CONSTRAINT "Paga_ID_usr_fkey" FOREIGN KEY ("ID_usr") REFERENCES public."Usuarios"("ID_usuario") ON UPDATE CASCADE ON DELETE CASCADE;
 C   ALTER TABLE ONLY public."Paga" DROP CONSTRAINT "Paga_ID_usr_fkey";
       public          postgres    false    3203    221    215            �           2606    16691    Pertenece Pertenece_ID_gru_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Pertenece"
    ADD CONSTRAINT "Pertenece_ID_gru_fkey" FOREIGN KEY ("ID_gru") REFERENCES public."Grupos"("ID_grupo") ON UPDATE CASCADE ON DELETE CASCADE;
 M   ALTER TABLE ONLY public."Pertenece" DROP CONSTRAINT "Pertenece_ID_gru_fkey";
       public          postgres    false    3205    222    218            �           2606    16696    Pertenece Pertenece_ID_usr_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Pertenece"
    ADD CONSTRAINT "Pertenece_ID_usr_fkey" FOREIGN KEY ("ID_usr") REFERENCES public."Usuarios"("ID_usuario") ON UPDATE CASCADE ON DELETE CASCADE;
 M   ALTER TABLE ONLY public."Pertenece" DROP CONSTRAINT "Pertenece_ID_usr_fkey";
       public          postgres    false    3203    222    215            $   :   x�3�tN,NT0�4����I�QH/*-�WHIU((*MMJ,�4426153��4������ c�      '       x�3�4�4202�54�52�440������ 0z�      &   1   x�3�tL/M�4202�50�50�0u��9�889@4W� �d      (      x�3�4�4202�54�52�,����� *1�      !   �   x�m��N�0Eד��T�y�-U���$&�؞b;<������`3���93#i;�у<��՜�aᔦQG��r���B�Uϖ.dQVu�R�JB����j� �'۟a��cN�m�Tu�+�Bt��v�"�[�]
�L�����N�ES.hM��m�v�Q&7�{?�9L�Sx��g�}��^�N�r�]�^�zĜN>zFL?���ӝH��*˲_�7cO     